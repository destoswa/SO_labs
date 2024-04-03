import matplotlib.pyplot as plt
import numpy as np
import param
from reference import generate_ref
from meas import generate_measurements
from methods import integration
from showing_results import *


# Measurements
time_10, acc_x_10, acc_y_10, gyro_10 = generate_measurements(freq=10)
time_100, acc_x_100, acc_y_100, gyro_100 = generate_measurements(freq=100)

# Integration
sr_res_10Hz_order1 = integration(acc_x_10, acc_y_10, gyro_10,
                                           param.RADIUS, param.AZIMUTH_0,
                                           param.OMEGA, freq=10, order=1)
sr_res_100Hz_order1 = integration(acc_x_100, acc_y_100, gyro_100,
                                           param.RADIUS, param.AZIMUTH_0,
                                           param.OMEGA, freq=100, order=1)
sr_res_10Hz_order2 = integration(acc_x_10, acc_y_10, gyro_10,
                                           param.RADIUS, param.AZIMUTH_0,
                                           param.OMEGA, freq=10, order=2)
sr_res_100Hz_order2 = integration(acc_x_100, acc_y_100, gyro_100,
                                           param.RADIUS, param.AZIMUTH_0,
                                           param.OMEGA, freq=100, order=2)

# True values
true_res_10 = generate_ref(freq=10)
true_res_100 = generate_ref(freq=100)

# =============================================
# ======= PLOTTING RESULTS ====================
# =============================================
# order 1 - freq 10Hz
show_evolution(true_res_10, sr_res_10Hz_order1, param.AZIMUTH_0, prefix='10Hz_order1_', src='./data')
show_deviation(true_res_10, sr_res_10Hz_order1, param.AZIMUTH_0, prefix='10Hz_order1_', src='./data')
show_trajectory(sr_res_10Hz_order1, prefix='10Hz_order1_', src='./data')

# order 1 - freq 100Hz
show_evolution(true_res_100, sr_res_100Hz_order1, param.AZIMUTH_0, prefix='100Hz_order1_', src='./data')
show_deviation(true_res_100, sr_res_100Hz_order1, param.AZIMUTH_0, prefix='100Hz_order1_', src='./data')
show_trajectory(sr_res_100Hz_order1, prefix='100Hz_order1_', src='./data')

# order 2 - freq 10Hz
show_evolution(true_res_10, sr_res_10Hz_order2, param.AZIMUTH_0, prefix='10Hz_order2_', src='./data')
show_deviation(true_res_10, sr_res_10Hz_order2, param.AZIMUTH_0, prefix='10Hz_order2_', src='./data')
show_trajectory(sr_res_10Hz_order2, prefix='10Hz_order2_', src='./data')

# order 2 - freq 100Hz
show_evolution(true_res_100, sr_res_100Hz_order2, param.AZIMUTH_0, prefix='100Hz_order2_', src='./data')
show_deviation(true_res_100, sr_res_100Hz_order2, param.AZIMUTH_0, prefix='100Hz_order2_', src='./data')
show_trajectory(sr_res_100Hz_order2, prefix='100Hz_order2_', src='./data')

# true trajectory
show_trajectory(true_res_10, prefix='10Hz_true_', src='./data')
show_trajectory(true_res_100, prefix='100Hz_true_', src='./data')

# Part 4 - compare trajectories to true values
show_error(true_res_10, sr_res_10Hz_order1, prefix='10Hz_order1_', src='./data')
show_error(true_res_100, sr_res_100Hz_order1, prefix='100Hz_order1_', src='./data')
show_error(true_res_10, sr_res_10Hz_order2, prefix='10Hz_order2_', src='./data')
show_error(true_res_100, sr_res_100Hz_order2, prefix='100Hz_order2_', src='./data')
