import param
import numpy as np
from reference import generate_ref

def generate_measurements():
    _, theta, _, _, _, _, acc_E, acc_N, angular_vel = generate_ref()

    # Measurement in B_frame
    acc_x = acc_E*np.cos(theta) - acc_N*np.sin(theta)
    acc_y = -acc_E*np.sin(theta) - acc_N*np.cos(theta)
    gyro = angular_vel

    return (acc_x, acc_y, gyro)