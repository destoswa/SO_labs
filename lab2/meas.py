import param
import numpy as np


def generate_measurements(freq, noise=None):
	dt = 1/freq

	# Measurement in B_frame
	time = np.arange(0, param.SIMULATION_TIME + dt, dt)
	acc_x = np.full_like(a=time, fill_value=0)
	acc_y = np.full_like(a=time, fill_value=param.OMEGA**2 * param.RADIUS)
	gyro = np.full_like(a=time, fill_value=param.OMEGA)

	return time, acc_x, acc_y, gyro
