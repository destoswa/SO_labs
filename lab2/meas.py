import param
import numpy as np
from reference import generate_ref


def generate_measurements(noise=None):

	# Measurement in B_frame
	time = np.arange(0, param.SIMULATION_TIME + param.DELTA_T, param.DELTA_T)
	acc_x = np.full_like(a=time, fill_value=0)
	acc_y = np.full_like(a=time, fill_value=param.OMEGA**2 * param.RADIUS)
	gyro = np.full_like(a=time, fill_value=param.OMEGA)

	return time, acc_x, acc_y, gyro
