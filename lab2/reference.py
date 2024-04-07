import param
import numpy as np
from measurements import generate_measurements


def generate_ref(freq):
	"""
	The method may be a bit overkilled, but generalize well to many cases
	Returns the true states of the case (orientation, position, velocity, time, ...), sampled at given frequency
	"""
	# Initial conditions
	theta_0 = param.THETA_0
	azimuth_0 = param.AZIMUTH_0

	# Perfect measurements in body frame (x,y)
	time, acc_x, acc_y, gyro = generate_measurements(freq, noise=None)

	# Angles theta and azimuth are identical between inertial frame and body frame
	theta = theta_0 + time * gyro
	azimuth = azimuth_0 + theta

	# Perfect measurements in inertial frame (E,N)
	acc_N = acc_x * np.cos(azimuth) - acc_y * np.sin(azimuth)
	acc_E = acc_x * np.sin(azimuth) + acc_y * np.cos(azimuth)

	# Strapdown for velocities
	def integral_acc_north(acc_x, acc_y, gyro, azimuth):
		return acc_x * np.sin(azimuth) / gyro + acc_y * np.cos(azimuth) / gyro

	def integral_acc_east(acc_x, acc_y, gyro, azimuth):
		return - acc_x * np.cos(azimuth) / gyro + acc_y * np.sin(azimuth) / gyro

	vel_N = param.V_0_NORTH + integral_acc_north(acc_x, acc_y, gyro, azimuth) - integral_acc_north(acc_x, acc_y, gyro,
																				 param.AZIMUTH_0)

	vel_E = param.V_0_EAST + integral_acc_east(acc_x, acc_y, gyro, azimuth) - integral_acc_east(acc_x, acc_y, gyro,
																			   param.AZIMUTH_0) + param.V_0_EAST

	# Strapdown for po
	def double_integral_acc_north(acc_x, acc_y, gyro, azimuth):
		return (- acc_x * np.cos(azimuth) + acc_y * np.sin(azimuth)) / gyro ** 2

	def double_integral_acc_east(acc_x, acc_y, gyro, azimuth):
		return (- acc_x * np.sin(azimuth) - acc_y * np.cos(azimuth)) / gyro ** 2

	pos_N = (
			param.P_0_NORTH
			+ double_integral_acc_north(acc_x, acc_y, gyro, azimuth)
			- double_integral_acc_north(acc_x, acc_y, gyro, param.AZIMUTH_0)
	)

	pos_E = (
			param.P_0_EAST
			+ double_integral_acc_east(acc_x, acc_y, gyro, azimuth)
			- double_integral_acc_east(acc_x, acc_y, gyro, param.AZIMUTH_0)

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