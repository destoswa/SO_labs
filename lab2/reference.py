import param
import numpy as np


def generate_ref(freq):
	"""
	The method may be a bit overkilled, but generalize well to many cases
	Parameters
	----------
	freq : frequency of sampling

	Returns
	-------
	true states of the case (orientation, position, velocity, time, ...), sampled at given frequency

	"""

	# Perfect measurements, we know acc_x, acc_y, gyro are constants
	dt = 1 / freq
	time = np.arange(0, param.SIMULATION_TIME + dt, dt)
	acc_x = 0
	acc_y = param.OMEGA ** 2 * param.RADIUS
	gyro = param.OMEGA

	# Perfect theta and azimuth
	theta = param.THETA_0 + time * gyro
	azimuth = param.AZIMUTH_0 + theta

	# Perfect accelerations in N and E
	acc_N = acc_x * np.cos(azimuth) - acc_y * np.sin(azimuth)
	acc_E = acc_x * np.sin(azimuth) + acc_y * np.cos(azimuth)

	# Perfect velocities and positions in N and E,
	# based on integration (resp. double integration) of acceleration over time and initial conditions

	# 	Vel_N and Pos_N
	def integral_acc_north(acc_x, acc_y, gyro, azimuth):
		d_azimuth_dt = gyro
		return acc_x * np.sin(azimuth) / d_azimuth_dt + acc_y * np.cos(azimuth) / d_azimuth_dt

	def double_integral_acc_north(acc_x, acc_y, gyro, azimuth):
		d_azimuth_dt = gyro
		return - acc_x * np.cos(azimuth) / d_azimuth_dt ** 2 + acc_y * np.sin(azimuth) / d_azimuth_dt ** 2

	vel_N = integral_acc_north(acc_x, acc_y, gyro, azimuth) - integral_acc_north(acc_x, acc_y, gyro,
																				 param.AZIMUTH_0) + param.V_0_NORTH
	pos_N = (
			double_integral_acc_north(acc_x, acc_y, gyro, azimuth)
			- double_integral_acc_north(acc_x, acc_y, gyro, param.AZIMUTH_0)
			+ param.P_0_NORTH
	)

	# 	Vel_E and Pos_E
	def integral_acc_east(acc_x, acc_y, gyro, azimuth):
		d_azimuth_dt = gyro
		return - acc_x * np.cos(azimuth) / d_azimuth_dt + acc_y * np.sin(azimuth) / d_azimuth_dt

	def double_integral_acc_east(acc_x, acc_y, gyro, azimuth):
		d_azimuth_dt = gyro
		return - acc_x * np.sin(azimuth) / d_azimuth_dt ** 2 - acc_y * np.cos(azimuth) / d_azimuth_dt ** 2

	vel_E = integral_acc_east(acc_x, acc_y, gyro, azimuth) - integral_acc_east(acc_x, acc_y, gyro,
																			   param.AZIMUTH_0) + param.V_0_EAST
	pos_E = (
			double_integral_acc_east(acc_x, acc_y, gyro, azimuth)
			- double_integral_acc_east(acc_x, acc_y, gyro, param.AZIMUTH_0)
			+ param.P_0_EAST
	)

	# All references states in a dictionary
	results = {
		'time': time,
		'theta': theta,
		'orientation': azimuth,
		'pos_E': pos_E,
		'pos_N': pos_N,
		'vel_E': vel_E,
		'vel_N': vel_N,
		'acc_E': acc_E,
		'acc_N': acc_N,
		'angular_vel': gyro,
	}
	return results
