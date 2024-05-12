from src.kalman import KalmanFilter
from src.Noise import WhiteNoise, white_noise
from src import reference as ref
import numpy as np
import scipy as sp


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
            [0, 0, 1, 0],
            [0, 0, 0, 1],
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
        kf = KalmanFilter(x0, p0, phi, q, h)
        time_gps = list(time_gps)
        for t in time:
            kf.predict()
            # Condition to add gps measure to kf
            if t in time_gps:
                ind = time_gps.index(t)
                z = gps_states[ind]
                kf.add_measure(z, r)


if __name__ == '__main__':
    main()
