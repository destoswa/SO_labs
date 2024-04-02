import param
import numpy as np


def generate_ref():
	# Perfect measurements, we know acc_x, acc_y, gyro are constants
	time = np.arange(0, param.SIMULATION_TIME + param.DELTA_T, param.DELTA_T)
	acc_x = 0
	acc_y = param.OMEGA ** 2 * param.RADIUS
	gyro = param.OMEGA

	# Theorical values
	theta = param.THETA_0 + time * gyro
	azimuth = param.AZIMUTH_0 + theta

	# 	acc_x, acc_y --> acc_N, acc_E
	acc_N = acc_x * np.cos(azimuth) - acc_y * np.sin(azimuth)
	acc_E = acc_x * np.sin(azimuth) + acc_y * np.cos(azimuth)

	# 	integration of acc_N and vel_N
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

	return time, theta, pos_E, pos_N, vel_E, vel_N, acc_E, acc_N, gyro
