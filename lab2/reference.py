import param
import numpy as np


def generate_ref(freq):

	# Perfect measurements, we know acc_x, acc_y, gyro are constants
	dt = 1 / freq
	time = np.arange(0, param.SIMULATION_TIME + dt, dt)
	acc_x = 0
	acc_y = param.OMEGA ** 2 * param.RADIUS
	gyro = param.OMEGA

	# Theoretical values
	theta = param.THETA_0 + time * gyro
	azimuth = param.AZIMUTH_0 + theta

	# Accelerations in N and E
	acc_N = acc_x * np.cos(azimuth) - acc_y * np.sin(azimuth)
	acc_E = acc_x * np.sin(azimuth) + acc_y * np.cos(azimuth)

	# Velocities and positions in N and E, based on (double) integration of acceleration over time and initial conditions
	def integ_acc_N(acc_x, acc_y, gyro, azimuth):
		d_azimuth_dt = gyro
		return acc_x * np.sin(azimuth) / d_azimuth_dt + acc_y * np.cos(azimuth) / d_azimuth_dt

	vel_N = integ_acc_N(acc_x, acc_y, gyro, azimuth) - integ_acc_N(acc_x, acc_y, gyro, param.AZIMUTH_0) + param.V_0_NORTH

	def double_integ_acc_N(acc_x, acc_y, gyro, azimuth):
		d_azimuth_dt = gyro
		return - acc_x * np.cos(azimuth) / d_azimuth_dt ** 2 + acc_y * np.sin(azimuth) / d_azimuth_dt ** 2

	pos_N = (
			double_integ_acc_N(acc_x, acc_y, gyro, azimuth)
			- double_integ_acc_N(acc_x, acc_y, gyro, param.AZIMUTH_0)
			+ param.P_0_NORTH
	)

	# 	integration of acc_E and vel_E
	def integ_acc_E(acc_x, acc_y, gyro, azimuth):
		d_azimuth_dt = gyro
		return - acc_x * np.cos(azimuth) / d_azimuth_dt + acc_y * np.sin(azimuth) / d_azimuth_dt

	vel_E = integ_acc_E(acc_x, acc_y, gyro, azimuth) - integ_acc_E(acc_x, acc_y, gyro, param.AZIMUTH_0) + param.V_0_EAST

	def double_integ_acc_E(acc_x, acc_y, gyro, azimuth):
		d_azimuth_dt = gyro
		return - acc_x * np.sin(azimuth) / d_azimuth_dt ** 2 - acc_y * np.cos(azimuth) / d_azimuth_dt ** 2

	pos_E = (
			double_integ_acc_E(acc_x, acc_y, gyro, azimuth)
			- double_integ_acc_E(acc_x, acc_y, gyro, param.AZIMUTH_0)
			+ param.P_0_EAST
	)
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