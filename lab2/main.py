import matplotlib.pyplot as plt
import numpy as np
import param
from reference import generate_ref
from meas import generate_measurements

# Initial conditions, assume known
initial_orientation = param.AZIMUTH_0 
initial_pos_N = param.RADIUS 
initial_pos_E = 0 
initial_vel_N = 0
initial_vel_E = param.OMEGA_L*param.RADIUS

# Measurements 
acc_x, acc_y, gyro = generate_measurements()

# Integration
orientation = initial_orientation + np.cumsum(gyro*param.DELTA_T)
theta_serie = orientation - initial_orientation  # Can we assume this relation as known ?

acc_N = acc_x * np.cos(orientation) - acc_y * np.sin(orientation)
acc_E = acc_x * np.sin(orientation) + acc_y * np.cos(orientation)

vel_N = initial_vel_N + np.cumsum(acc_N*param.DELTA_T)
vel_E = initial_vel_E + np.cumsum(acc_E*param.DELTA_T)

pos_N = initial_pos_N + np.cumsum(vel_N*param.DELTA_T)
pos_E = initial_pos_E + np.cumsum(vel_E*param.DELTA_T)

# Plots

# True values
true_time, true_theta, true_pos_E, true_pos_N, true_vel_E, true_vel_N, true_acc_E, true_acc_N, true_angular_vel = generate_ref()

# Evolution of state
fig, axs = plt.subplots(4, 1, figsize=(10, 8))

axs[0].plot(true_time, orientation, label='orientation')
axs[0].plot(true_time, true_theta+param.AZIMUTH_0 , label='true_orientation')
axs[0].legend()

axs[1].plot(true_time, acc_N, label='estimated acc_N')
axs[1].plot(true_time, acc_E, label='estimated acc_E')
axs[1].plot(true_time, true_acc_N, label='true acc_N')
axs[1].plot(true_time, true_acc_E, label='true acc_E')
axs[1].legend()

axs[2].plot(true_time, vel_N, label="vel_N")
axs[2].plot(true_time, vel_E, label="vel_E")
axs[2].plot(true_time, true_vel_N, label="true vel_N")
axs[2].plot(true_time, true_vel_E, label="true vel_E")
axs[2].legend()

axs[3].plot(true_time, pos_N, label="estimated pos_N")
axs[3].plot(true_time, pos_E, label="estimated pos_E")
axs[3].plot(true_time, true_pos_N, label="true pos_N")
axs[3].plot(true_time, true_pos_E, label="true pos_E")
axs[3].legend()

fig.savefig('data/states.jpg')


# Deviation of state
fig, axs = plt.subplots(4, 1, figsize=(10, 8))

axs[0].plot(true_time, orientation-(true_theta+param.AZIMUTH_0), label='orientation')
axs[0].legend()

axs[1].plot(true_time, acc_N-true_acc_N, label=' acc_N')
axs[1].plot(true_time, acc_E-true_acc_E, label=' acc_E')
axs[1].legend()

axs[2].plot(true_time, vel_N-true_vel_N, label="vel_N")
axs[2].plot(true_time, vel_E-true_vel_E, label="vel_E")
axs[2].legend()

axs[3].plot(true_time, pos_N-true_pos_N, label="pos_N")
axs[3].plot(true_time, pos_E-true_pos_E, label="pos_E")
axs[3].legend()

fig.savefig('data/deviation.jpg')

# Estimated trajectory
plt.clf()
plt.scatter(pos_E, pos_N, label='estimated trajectory', alpha=0.8, marker=',', linewidths=0.1)
plt.savefig('data/trajectory.jpg')
plt.savefig('data/trajectory.svg')


