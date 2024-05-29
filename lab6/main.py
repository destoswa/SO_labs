import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

import reference as ref
import sensors as sen

IMU_FREQ = 100
GNSS_FREQ = 0.5

def main():

    # Reference
    ref_states = ref.generate_states()  # PVA, error acc_x, error acc_y, error_gyro
    ref_imu = ref.generate_imu()        # Accs, gyro

    # Sensors
    gps = sen.generate_gps(ref_states)  # None when no measurement
    imu = sen.generate_imu(ref_imu)
    
    # Initialize Kalman matrices (time invariant)
    
    n = ref_states.shape[1]
    
    #   dz = H dx
    H = np.zeros((n, n))
    H[0, 0], H[1, 1] = 1, 1

    
    # Initialize states matrix
    states_tild = np.zeros_like(ref_states)
    P_tild = np.zeros_like(ref_states)
    states_tild[0] = ref_states[0, :]
    R_bm = np.array([[0, -1],[1, 0]])

    # Kalman Filter
    #for t, _ in enumerate(ref.TIME_SEQUENCE[1:]):
    cmp = 0
    for t in range(1, len(ref.TIME_SEQUENCE)):
        # Strapdown
        alpha_dot = imu[t,2]
        Omega = np.array([[0, -alpha_dot], [ alpha_dot, 0]])
        R_bm = R_bm @ np.exp(Omega * ref.DT)
        alpha = states_tild[t-1, 0] + alpha_dot * ref.DT
        v = states_tild[t-1, 1:3].T + R_bm @ imu[t, :2] * ref.DT
        x = states_tild[t-1, 3::].T + v * ref.DT
        states_tild[t] = [alpha, v[0], v[1], x[0], x[1]]

        # Initialize Kalman matrices
        attitude = states_tild[t - 1, 0]
        R_bm = np.array([[np.cos(attitude), -np.sin(attitude)],
                         [np.sin(attitude), np.cos(attitude)]])
        acc_t_m = R_bm @ imu[t, :2].T
        F = np.zeros((9, 9))
        # F11
        F[1, 0] = -acc_t_m[1]
        F[2, 0] = acc_t_m[0]
        F[0, 5:7] = 1
        # F12
        F[1, 7] = np.cos(attitude)
        F[1, 8] = -np.sin(attitude)
        F[2, 7] = np.sin(attitude)
        F[2, 8] = np.cos(attitude)
        # F22
        F[6, 6] = -1 / sen.TAU_GYRO_GM
        F[7, 7] = -1 / sen.TAU_ACC_GM
        F[8, 8] = -1 / sen.TAU_ACC_GM

        G = np.zeros((9, 6))
        # G11
        G[0, 0] = 1
        G[1, 1] = np.cos(attitude)
        G[1, 2] = -np.sin(attitude)
        G[2, 1] = np.sin(attitude)
        G[2, 2] = np.cos(attitude)
        # G22
        G[6::, 3::] = np.eye(3)

        W = np.diag([sen.SIGMA_GYRO_WN ** 2, sen.SIGMA_ACC_WN ** 2, sen.SIGMA_ACC_WN ** 2,
                     2 * sen.SIGMA_GYRO_GM ** 2 / sen.TAU_GYRO_GM,
                     2 * sen.SIGMA_ACC_GM ** 2 / sen.TAU_ACC_GM,
                     2 * sen.SIGMA_ACC_GM ** 2 / sen.TAU_ACC_GM])

        n = F.shape[0]
        A = np.zeros((2 * n, 2 * n))
        A[:n, :n] = -F
        A[:n, n:] = G @ W @ G.T
        A[n:, n:] = F.T
        A = A * ref.DT
        B = sp.linalg.expm(A)
        phi = B[n:, n:].T
        Q = phi @ B[:n, n:]

        # =========== continuer kalman filter ici ==========
        #...

        # Update with dz
        if not np.isnan(gps[t,0]):
            cmp += 1
            print(cmp)


        #   d(dx)/dt = F * dx + G * w  -> L11_INSGPS-dEKF-blackboard.pdf
        # Prediction dx
        """states_tild[t] = strapdown(states_tild[t-1], imu[])  #  dPVA

        # Update with dz
        if gps[t] != None:
            
            delta_state = update(states_tild[t], gps[t]) #

            # Gain
            # Update dx
            # Update P
        
        # Update state
        states_tild[t] = states_tild[t-1] + delta_state"""


def strapdown(states, Q):
    return


def update(states, gps):
    return


if __name__ == "__main__":
    main()