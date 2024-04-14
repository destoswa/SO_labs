import numpy as np


def integration(acc_x, acc_y, gyro, tetha_0, orientation_0, pos_N_0, pos_E_0, vel_N_0, vel_E_0, freq=10, order=1):
    """
    Produce estimation of simulation states with integration of measurements and initial conditions known
    """
    dt = 1/freq
    theta_serie = np.cumsum(gyro * dt)
    theta_serie -= (theta_serie[0]- tetha_0)  # Initial angle at tetha_0 rad
    orientation = orientation_0 + theta_serie

    # computing acceleration in the 2D inertial frame
    acc_E = - acc_y * np.sin(theta_serie) + acc_x * np.cos(theta_serie)
    acc_N = - acc_y * np.cos(theta_serie) - acc_x * np.sin(theta_serie)

    vel_N = np.zeros_like(acc_N)
    vel_E = np.zeros_like(acc_E)
    pos_N = np.zeros_like(acc_N)
    pos_E = np.zeros_like(acc_E)
    if order == 1:

        # computing velocities
        vel_N = vel_N_0 + np.cumsum(acc_N * dt)
        vel_E = vel_E_0 + np.cumsum(acc_E * dt)

        # computing positions
        pos_N = pos_N_0 + np.cumsum(vel_N * dt)
        pos_E = pos_E_0 + np.cumsum(vel_E * dt)

    elif order == 2:
        # computing velocities
        vel_E[0] = vel_E_0
        vel_N[0] = vel_N_0
        vel_E[1::] = vel_E_0 + np.cumsum(0.5*(acc_E[1::] + acc_E[0:-1])*dt)
        vel_N[1::] = vel_N_0 + np.cumsum(0.5*(acc_N[1::] + acc_N[0:-1])*dt)

        # computing positions
        pos_E[0] = pos_E_0
        pos_N[0] = pos_N_0
        pos_E[1::] = pos_E_0 + np.cumsum(0.5*(vel_E[1::] + vel_E[0:-1])*dt)
        pos_N[1::] = pos_N_0 + np.cumsum(0.5*(vel_N[1::] + vel_N[0:-1])*dt)

    results = {
        'orientation': orientation,
        'acc_E': acc_E,
        'acc_N': acc_N,
        'vel_E': vel_E,
        'vel_N': vel_N,
        'pos_E': pos_E,
        'pos_N': pos_N,
    }
    return results