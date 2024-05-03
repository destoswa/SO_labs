import numpy as np

import src.constants as cst
from src.constants import deg
import src.readimu as rimu
import src.show_results as sr

""" NOTATION 
Angular rate : w_a_b_c, angular rate of frame c relative to frame b expressed in frame a
Rotation matrix : R_a_b, rotation from b to a, or attitude of b expressed in a
    - angle of rotation matrix r_a_b, p_a_b, y_a_b for roll, pitch, yaw
"""

""" FRAMES
Body frame : IMU (X', Y', Z') : 
    - time : time serie in s
    - gyros : angular rate of body relative to inertial frame in body frame w_b_i_b
    - accs : specific forces applied to body in body frame : f_b
    - must be converted  ->  (X, Y, Z) = (X, -Y', -Z')

Local frame : NWD 
    - attitude of reference of body frame (with converted body frame XYZ), R_l_b
    - must be converted to NED 
"""

""" ATTITUDE OF BODY FRAME IN LOCAL FRAME [rad] """

# Attitude of IMU in local frame (NWD)
ROLL_REF_l_b = cst.ROLL
PITCH_REF_l_b = cst.PITCH
YAW_REF_l_b = cst.AZIMUTH  # TODO : Control, see questions

# Change to local frame (NED)
PITCH_REF_l_b = -PITCH_REF_l_b

""" TASK 1 : IMU Measurements [s, rad/s, m/s²] """

# Read IMU measurements in timespan of interest, in IMU frame
time, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z = rimu.read_imu_timespan(cst.IMU_FILENAME, cst.T_0, cst.T_F)

# Change IMU frame (X', Y', Z') to (X' , -Y', -Z') the new (X, Y, Z) frame
gyro_y, gyro_z, acc_y, acc_z = - gyro_y, - gyro_z, - acc_y, - acc_z

# Mean measurements
gyro_x_m = np.mean(gyro_x)
gyro_y_m = np.mean(gyro_y)
gyro_z_m = np.mean(gyro_z)
acc_x_m = np.mean(acc_x)
acc_y_m = np.mean(acc_y)
acc_z_m = np.mean(acc_z)

# Plot IMU and mean deviation
sr.plot_IMU(time, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z)
sr.plot_IMU_mean_dev(time, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z)
sr.plot_IMU_mean_rel_dev(time, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z)

# Statistics
print(" --- TASK 1 : IMU measurements ---  \n")
sr.print_stats(gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z)

""" TASK 2 : Gyro norms """

# Norm of average gyro signals (less noise), assume constant OK
norm_avg_gyro = np.sqrt(gyro_x_m ** 2 + gyro_y_m ** 2 + gyro_z_m ** 2)

# (Avg) Norm of gyro signal at each time step (more sensitive to noise, especiallly bias)
gyro_norms = np.sqrt(gyro_x ** 2 + gyro_y ** 2 + gyro_z ** 2)
avg_gyro_norm = np.mean(gyro_norms)

# Reference earth rotation projection in body frame (XYZ)
EARTH_ROTATION = cst.EARTH_ANGULAR_RATE
"""
earth_rotation_x = 
earth_rotation_y = 
earth_rotation_z =
"""

# Comparison
print(" --- TASK 2 --- \n")
print(f"\tEarth rotation, norm : {deg(EARTH_ROTATION) * 1000:.5} [mdeg/s] ")
print(f"\tAcc, avg norms  : {deg(avg_gyro_norm) * 1000:.5} [mdeg/s] ")
print(f"\tAcc, norm avg : {deg(norm_avg_gyro) * 1000:.5} [mdeg/s] ")
print("\n")

""" TASK 3 : Accs norms """

# Norm of average accs signals (less noise), assume constant OK
norm_avg_acc = np.sqrt(acc_x_m ** 2 + acc_y_m ** 2 + acc_z_m ** 2)

# (Avg) Norm of accs signal at each time step (more sensitive to noise, especiallly bias)
acc_norms = np.sqrt(acc_x ** 2 + acc_y ** 2 + acc_z ** 2)
avg_acc_norm = np.mean(acc_norms)

# Reference earth gravity specific force in body frame
"""
earth_gravity_x = 
earth_gravity_y = 
earth_gravity_z =
"""

# Comparison
print(" --- TASK 3 --- \n")
print(f"\tEarth gravity, norm : {abs(cst.EARTH_GRAVITY):.5} [m/s²]")
print(f"\tAcc, avg norms  : {avg_acc_norm:.5} [m/s²] ")
print(f"\tAcc, norm avg : {norm_avg_acc:.5} [m/s²] ")
print("\n")

""" TASK 4 : Accelerometer leveling -> Roll, Pitch of body in local frame """

# Accelerometer leveling
roll_l_b = np.arctan2(-acc_y_m, -acc_z_m)
pitch_l_b = np.arctan2(acc_x_m, np.sqrt(acc_y_m ** 2 + acc_z_m ** 2))

# Comparison
print(" --- TASK 4 --- \n")
print(f'\tTrue roll : {deg(ROLL_REF_l_b):.5} [deg]')
print(f'\tEstimated roll : {deg(roll_l_b):.5} [deg]\n')
print(f'\tTrue pitch : {deg(PITCH_REF_l_b):.5} [deg]')
print(f'\tEstimated pitch : {deg(pitch_l_b):.5} [deg]')
print("\n")

""" TASK 5 : Gyro-compassing -> yaw of body in local frame and transform the gyroscopic reading to the
leveled frame"""

# Gyro-compassing
roll_b_l = - roll_l_b
pitch_b_l = - pitch_l_b
cos_p = np.cos(pitch_l_b)
sin_p = np.sin(pitch_l_b)
cos_r = np.cos(roll_l_b)
sin_r = np.sin(roll_l_b)

R_leveled_b = np.array(
    [
        [cos_p, 0, -sin_p],
        [sin_r * sin_p, cos_r, sin_r * cos_p],
        [cos_r * sin_p, -sin_r, cos_r * cos_p]
    ]
)

gyro_b_m = np.array([gyro_x_m, gyro_y_m, gyro_z_m])
gyro_leveled = np.matmul(R_leveled_b, gyro_b_m)
yaw_b_l = np.arctan2(-gyro_leveled[1], gyro_leveled[0])

# Latitude estimation
phi = np.pi / 2 - np.arccos(- gyro_z_m / EARTH_ROTATION)

# Comparison
print(" --- TASK 5 --- \n")

print(f'\tTrue yaw : {deg(YAW_REF_l_b):.5} [deg]')
print(f'\tEstimated yaw : {deg(yaw_b_l):.5} [deg]\n')

print(f'\tTrue latitude (phi) : {deg(cst.LATITUDE):.5} [deg]')
print(f'\tEstimated latitude (phi) : {deg(phi):.5} [deg]\n')
