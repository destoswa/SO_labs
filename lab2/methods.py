import numpy as np
from meas import generate_measurements
import param


def integration(acc_x, acc_y, gyro, radius, azimuth_0, omega, freq=10, order=1):
    print(f'============ order {order} - freq {freq} ============')
    dt = 1/freq
    # Initial conditions, assume known
    initial_orientation = azimuth_0
    initial_pos_N = radius
    initial_pos_E = 0
    initial_vel_N = 0
    initial_vel_E = omega * radius

    theta_serie = np.cumsum(gyro * dt)  # Can we assume this relation as known ?
    theta_serie -= theta_serie[0]  # Initial angle at 0 rad
    orientation = initial_orientation + theta_serie

    # computing acceleration in the 2D inertial frame
    acc_E = - acc_y * np.sin(theta_serie) + acc_x * np.cos(theta_serie)
    acc_N = - acc_y * np.cos(theta_serie) - acc_x * np.sin(theta_serie)

    vel_N = np.zeros_like(acc_N)
    vel_E = np.zeros_like(acc_E)
    pos_N = np.zeros_like(acc_N)
    pos_E = np.zeros_like(acc_E)
    if order == 1:
        # computing velocities
        vel_N = initial_vel_N + np.cumsum(acc_N * dt)
        vel_E = initial_vel_E + np.cumsum(acc_E * dt)

        # computing positions
        pos_N = initial_pos_N + np.cumsum(vel_N * dt)
        pos_E = initial_pos_E + np.cumsum(vel_E * dt)

    elif order == 2:
        # computing velocities
        vel_E[0] = initial_vel_E
        vel_N[0] = initial_vel_N
        vel_E[1::] = initial_vel_E + np.cumsum(0.5*(acc_E[1::] + acc_E[0:-1])*dt)
        vel_N[1::] = initial_vel_N + np.cumsum(0.5*(acc_N[1::] + acc_N[0:-1])*dt)

        # computing positions
        pos_E[0] = initial_pos_E
        pos_N[0] = initial_pos_N
        pos_E[1::] = initial_pos_E + np.cumsum(0.5*(vel_E[1::] + vel_E[0:-1])*dt)
        pos_N[1::] = initial_pos_N + np.cumsum(0.5*(vel_N[1::] + vel_N[0:-1])*dt)

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


def main():
    time, acc_x, acc_y, gyro = generate_measurements()
    sr_res_10Hz_order2 = integration(acc_x, acc_y, gyro,
                                     param.RADIUS, param.AZIMUTH_0,
                                     param.OMEGA, freq=10, order=2)


if __name__ == '__main__':
    main()
