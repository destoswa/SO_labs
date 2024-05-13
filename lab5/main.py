from src.kalman import KalmanFilter
from src.Noise import WhiteNoise, white_noise
from src.showing_results import show_trajectory
from src import reference as ref
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


def main():
    # Apply random seed for repeatability
    np.random.seed(42)

    # Reference position
    ref_states = ref.generate_ref_states()

    # Generate realizations
    time = ref.generate_time_serie()
    for real in range(ref.NUMBER_REALIZATION):

        # Gps
        time_gps = ref.generate_time_serie(freq=ref.GPS_FREQ)
        size = ref.GPS_FREQ * ref.SIMULATION_TIME
        gps_states = ref.generate_ref_states(freq=ref.GPS_FREQ)[:, :2]
        gps_states[:, 0] = gps_states[:, 0] + white_noise(size, sd=0.5)  # x
        gps_states[:, 1] = gps_states[:, 1] + white_noise(size, sd=0.5)  # y

        # Initial conditions
        x0 = ref_states[0, :]

        # Uncertainties for initial conditions
        sigma_p0 = 10  # m
        sigma_v0 = 0.1  # m/s
        p0 = np.array([
            [sigma_p0 ** 2, 0, 0, 0],
            [0, sigma_p0 ** 2, 0, 0],
            [0, 0, sigma_v0 ** 2, 0],
            [0, 0, 0, sigma_v0 ** 2],
        ])

        # Motion model
        dt = ref.DT
        f = np.array([  # dx/dt = f * x     [vx, vy, ax, ay] = f * [x ,y , vx , vy]
            [0, 0, dt, 0],
            [0, 0, 0, dt],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        g = np.array([
            [0, 0],
            [0, 0],
            [1, 0],
            [0, 1]
        ])
        sigma_a = 0.05 * np.sqrt(ref.FREQ)  # m/s² / sqrt(Hz)
        w = np.eye(2, 2) * sigma_a
        n = f.shape[0]
        A = np.zeros((2 * n, 2 * n))
        A[:n, :n] = -f
        A[:n, n:] = g @ w @ g.T
        A[n:, n:] = f.T
        B = sp.linalg.expm(A)
        phi = B[n:, n:].T
        q = phi * B[:n, n:]

        # Measurment model   z [2x1] = H[2X4] @ x[4x1] + v[2x1]
        h = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        sigma_gps = 0.5  # m
        r = np.eye(2) * sigma_gps**2

        # Kalman filter
        kf = KalmanFilter(x0, p0, phi, q, h, r)
        kf_states = []
        kf_states.append(kf.x_est)
        time_gps = list(time_gps)
        for t in time[:-1]:
            kf.predict()
            # Condition to add gps measure to kf
            if t in time_gps:
                ind = time_gps.index(t)
                z = gps_states[ind]
                kf.update(z)
            kf_states.append(kf.x_est)
        kf_states = np.array(kf_states)

        # Show trajectories
        show_trajectory(kf_states, gps_states, f"kf_state_{real}", "results/trajectory", do_save_fig=True)

        # STDs of error
        # 4.a
        diff_gps_ref = ref_states[::100, :2] - gps_states
        std_real_gps = np.sqrt(np.std(diff_gps_ref[:, 0])**2 + np.std(diff_gps_ref[:, 1])**2)

        # 4.b
        diff_kf_ref = ref_states[:, :2] - kf_states[:, :2]
        std_filtered = np.sqrt(np.std(diff_kf_ref[:, 0])**2 + np.std(diff_kf_ref[:, 1])**2)

        # 4.c
        # PAS COMPRIS!!

        print(f"==== Realization {real} ====")
        print(f"\tEmpirical std characterizing real GPS positioning quality: {std_real_gps}")
        print(f"\tEmpirical std characterizing filtered positioning quality: {std_filtered}")
        print(f"\tEmpirical std characterizing KF-predicted positioning quality (PAS COMPRIS!): {None}")


if __name__ == '__main__':
    main()
    #plt.show()
