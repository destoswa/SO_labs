import param
import numpy as np
from measurements import Measurements


class Trajectory:

	def __init__(self, measurements):
		self.initial_conditions = param.INITIAL_CONDITIONS
		self.measurements = measurements

		# Initialize empty trajectory states
		self.time = self.measurements.time
		self.theta = None
		self.azimuth = None
		self.acc_E = None
		self.acc_N = None
		self.v_E = None
		self.v_N = None
		self.p_E = None
		self.p_N = None

	def compute_trajectory(self, order):
		# Shorter notation for measurements
		dt = self.measurements.dt
		acc_x = self.measurements['acc_x']
		acc_y = self.measurements['acc_y']
		gyro = self.measurements['gyro']

		# Shorter notation for initial conditions
		theta_0 = self.initial_conditions['theta']
		azimuth_0 = self.initial_conditions['azimuth']
		v_N_0 = self.initial_conditions['v_N']
		v_E_0 = self.initial_conditions['v_E']
		p_N_0 = self.initial_conditions['p_N']
		p_E_0 = self.initial_conditions['p_E']

		# Compute trajectory states with integration
		theta = integrate_numerically(dt=dt, signal=gyro, initial_condition=theta_0)
		azimuth = azimuth_0 + theta
		acc_E = - acc_y * np.sin(theta) + acc_x * np.cos(theta)
		acc_N = - acc_y * np.cos(theta) - acc_x * np.sin(theta)
		v_N = integrate_numerically(dt=dt, signal=acc_N, initial_condition=v_N_0, order=order)
		v_E = integrate_numerically(dt=dt, signal=acc_E, initial_condition=v_E_0, order=order)
		p_N = integrate_numerically(dt=dt, signal=v_N, initial_condition=p_N_0, order=order)
		p_E = integrate_numerically(dt=dt, signal=v_E, initial_condition=p_E_0, order=order)

		# Save trajectory states
		self.theta, self.azimuth = theta, azimuth
		self.acc_E, self.acc_N = acc_E, acc_N
		self.v_E, self.v_N = v_E, v_N
		self.p_E, self.p_N = p_E, p_N


def integrate_numerically(dt, signal, initial_condition, order=1):
	assert (order in [1, 2])
	integrated_signal = np.zeros_like(signal)
	integrated_signal[0] = initial_condition  # The first value must be the initial condition

	if order == 1:
		tmp = initial_condition + np.cumsum(signal * dt)
		integrated_signal[1::] = tmp[:-1]  # We cut off the last value, to keep the same length as the original signal
	elif order == 2:
		integrated_signal[1::] = initial_condition + np.cumsum(0.5 * (signal[1::] + signal[0:-1]) * dt)
	return integrated_signal


class TrueTrajectory(Trajectory):
	def __init__(self, measurements):
		freq = measurements.freq
		nominal_measurements = Measurements(freq)
		super().__init__(measurements=nominal_measurements)  # Use nominal sensor values

	def compute_trajectory(self, order=None):
		# Shorter notation for measurements
		time = self.measurements.time
		acc_x = self.measurements['acc_x']
		acc_y = self.measurements['acc_y']
		gyro = self.measurements['gyro']

		# Shorter notation for initial conditions
		theta_0 = self.initial_conditions['theta']
		azimuth_0 = self.initial_conditions['azimuth']
		v_N_0 = self.initial_conditions['v_N']
		v_E_0 = self.initial_conditions['v_E']
		p_N_0 = self.initial_conditions['p_N']
		p_E_0 = self.initial_conditions['p_E']

		# Compute nominal trajectory states
		self.theta = theta_0 + time * gyro
		self.azimuth = azimuth_0 + self.theta
		self.acc_N = acc_x * np.cos(self.azimuth) - acc_y * np.sin(self.azimuth)
		self.acc_E = acc_x * np.sin(self.azimuth) + acc_y * np.cos(self.azimuth)
		self.v_N = int_eval(get_v_n, v_N_0, acc_x, acc_y, gyro, self.azimuth, azimuth_0)
		self.v_E = int_eval(get_v_e, v_E_0, acc_x, acc_y, gyro, self.azimuth, azimuth_0)
		self.p_N = int_eval(get_p_n, p_N_0, acc_x, acc_y, gyro, self.azimuth, azimuth_0)
		self.p_E = int_eval(get_p_e, p_E_0, acc_x, acc_y, gyro, self.azimuth, azimuth_0)


# Theoretical (double) integration of acc_N, acc_E
def int_eval(int_function, initial_condition, acc_x, acc_y, gyro, azimuth, azimuth_0):
	"""
	Apply integral evaluation from azimuth_0 to azimuth
	"""

	result = (
			initial_condition
			+ int_function(acc_x, acc_y, gyro, azimuth)
			- int_function(acc_x, acc_y, gyro, azimuth_0)
	)
	return result


def get_v_n(acc_x, acc_y, gyro, azimuth):
	return acc_x * np.sin(azimuth) / gyro + acc_y * np.cos(azimuth) / gyro


def get_v_e(acc_x, acc_y, gyro, azimuth):
	return - acc_x * np.cos(azimuth) / gyro + acc_y * np.sin(azimuth) / gyro


def get_p_n(acc_x, acc_y, gyro, azimuth):
	return (- acc_x * np.cos(azimuth) + acc_y * np.sin(azimuth)) / gyro ** 2


def get_p_e(acc_x, acc_y, gyro, azimuth):
	return (- acc_x * np.sin(azimuth) - acc_y * np.cos(azimuth)) / gyro ** 2
