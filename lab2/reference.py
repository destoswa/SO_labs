import param
import numpy as np

def generate_ref():
    time_serie = np.arange(0, param.SIMULATION_TIME + param.DELTA_T, param.DELTA_T)
    theta = time_serie*param.OMEGA_L + param.THETA_0 
    pos_N = np.cos(theta)*param.RADIUS
    pos_E = np.sin(theta)*param.RADIUS
    vel_N = -np.sin(theta)*param.OMEGA_L*param.RADIUS
    vel_E = np.cos(theta)*param.OMEGA_L*param.RADIUS
    azimuth_l = param.AZIMUTH_0 + theta # Orientation of body with respect to North axis

    # Measurements in L_frame
    acc_N = - np.cos(theta)* param.OMEGA_L**2 * param.RADIUS
    acc_E = - np.sin(theta) * param.OMEGA_L**2 * param.RADIUS
    angular_vel = np.full_like(a=time_serie, fill_value=param.OMEGA_L)
    
    return time_serie, theta, pos_E, pos_N, vel_E, vel_N, acc_E, acc_N, angular_vel

