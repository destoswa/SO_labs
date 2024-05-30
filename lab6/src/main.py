import scipy as sp
import numpy as np
from tqdm import tqdm 
import matplotlib.pyplot as plt

import reference as ref
import sensors as sen
import showing_results as sr

""" Simulation choice
The IMU frequency is the frequency of the simulation
We assume that the GPS has a lower or equal frequency
We also assume the frequency are easily syncronisable 
--> all the timestamp of the gps are included in the timestamp of the imu
"""


def main():

    """ Reference """ 
    ref_states = ref.generate_states()  # attitude, v_N, v_E, p_N, p_E, gyro_bias, gyro_noise, acc_x_noise, acc_y_noise
    ref_imu = ref.generate_imu()        # acc_x, acc_x, gyro

    plt.clf()
    plt.plot(ref_states[:, 4], ref_states[:, 3])
    plt.savefig("lab6/results/reference.jpg")

    plt.clf()
    plt.plot(ref_imu[:, 4], ref_imu[:, 3])
    plt.savefig("lab6/results/reference.jpg")



    """ Sensors """ 
    gps = sen.generate_gps(ref_states)  # None when no measurement
    imu = sen.generate_imu(ref_imu)
    
    plt.plot(gps[::200,1], gps[::200, 0])
    plt.savefig("lab6/results/gps.jpg")

    """ Initialize X, dX and P matrices, see 6.4, 6.5 """
    T, N = ref_states.shape
    dN = N + 4 # + 4 error states

    X = np.zeros_like(ref_states)
    dX = np.zeros((T,dN))
    P = np.zeros((T, dN, dN))
    X[0] = np.array([
        (90+3)*np.pi/180,
        (0-2),
        (ref.OMEGA*ref.RADIUS - 1),
        gps[0,0],
        gps[0,1],
    ])

    P[0] = np.diag([
        2*np.pi/180,
        5,
        5,
        10,
        10,
        0.05*np.pi/180,
        0.01*np.pi/180,
        300E-6*ref.GRAVITY_CST,
        300E-6*ref.GRAVITY_CST
    ])**2

    # R_bm = np.array([[0, -1],[1, 0]])
    """ Time loop / Simulation """
    for t, _ in enumerate(ref.TIME_SEQUENCE[1:], start=1):
        """ Strapdown from X[t-1] to X[t] using IMU[t-1] integration in NE frame """
        
        # Attitude : a[t] = a[t-1] * w[t-1] * dt
        attitude_prev = X[t-1, 0]
        gyro = -imu[t-1, 2]
        attitude_next = attitude_prev + gyro * ref.DT

        # IMU to NE frame
        R_bm = np.array([[np.cos(attitude_prev), -np.sin(attitude_prev)],
                    [np.sin(attitude_prev), np.cos(attitude_prev)]])
        accs_m = R_bm @ imu[t-1,:2].T
        
        # Velocity : v[t] = v[t-1] + a[t-1] * dt
        v_prev = X[t-1, 1:3]
        v_next = v_prev + accs_m * ref.DT
        
        # Position : p[t] = p[t-1] + v[t-1] * dt + 0.5 * a[t-1] * dt**2
        p_prev = X[t-1, 3:5]
        p_next = p_prev + v_prev.T * ref.DT + 0.5 * accs_m * ref.DT**2

        X[t, :] = np.array([attitude_next, v_next[0], v_next[1], p_next[0], p_next[1]])

        """ Extended Kalman Filter """
    
        F = np.zeros((dN,dN))   
        # F11
        F[1, 0] = -accs_m[1]
        F[2, 0] = -accs_m[0]
        F[3, 1] = 1
        F[4, 2] = 1
        
        # F12
        F[0, 5:7] = 1
        F[1:3, 7:] = R_bm.copy()
        
        # F22
        F[6, 6] = -1 / sen.TAU_GYRO_GM
        F[7, 7] = -1 / sen.TAU_ACC_GM
        F[8, 8] = -1 / sen.TAU_ACC_GM

        G = np.zeros((dN, 6))
        # G11
        G[0, 0] = 1
        G[1:3, 1:3] = R_bm.copy()

        # G22
        G[6:, 3:] = np.eye(3)

        W = np.diag([                                           # CONSTANT 
            sen.SIGMA_GYRO_WN ** 2, 
            sen.SIGMA_ACC_WN ** 2, 
            sen.SIGMA_ACC_WN ** 2,
            2 * sen.SIGMA_GYRO_GM ** 2 / sen.TAU_GYRO_GM,
            2 * sen.SIGMA_ACC_GM ** 2 / sen.TAU_ACC_GM,
            2 * sen.SIGMA_ACC_GM ** 2 / sen.TAU_ACC_GM
            ])

        H = np.zeros((2,dN))                                    # CONSTANT 
        H[0,4] = 1
        H[1,5] = 1

        A = np.zeros((2 * dN, 2 * dN))
        A[:dN, :dN] = -F
        A[:dN, dN:] = G @ W @ G.T
        A[dN:, dN:] = F.T
        A = A * ref.DT
        B = sp.linalg.expm(A)
        phi = B[dN:, dN:].T
        Q = phi @ B[:dN, dN:]

        # Predict dX
        dX[t] = phi @ dX[t]   # Trivial == 0, No ???
        P[t] = phi @ P[t-1] @ phi.T + Q

        # Update with dZ (GPS - State X)
        if not np.isnan(gps[t,0]):
            
            dZ = gps[t] - X[t, 4:6]

            # Gain K
            # TODO Avoid inversion with solving instead
            R = np.diag([sen.SIGMA_GPS**2, sen.SIGMA_GPS**2])     # CONSTANT
            A = (H @ P[t] @ H.T + R).T
            b = (P[t] @ H.T).T
            K = np.linalg.solve(A, b).T

            # State update
            dX[t] = dX[t] + K @ (dZ - H @ dX[t])

            # Covariance update
            P[t] = (np.eye(9,9) - K @ H) @ P[t]
        
        """ Apply correction """
        X[t] += dX[t, :5]


if __name__ == "__main__":
    main()