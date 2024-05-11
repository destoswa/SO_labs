from src.kalman import KalmanFilter
from src.Noise import WhiteNoise
from src import reference as ref
import numpy as np

# Uncertainties for initial conditions
sigma_p0 = 10  # m
sigma_v0 = 0.1  # m/s

# Uncertainties of motion model
sigma_a = 0.05  # m/s² / Hz


def main():
    # Apply random seed for repeatability
    np.random.seed(42)

    # Reference state (x, y, vx, vy)
    time = ref.generate_time_serie()
    ref_states = ref.generate_ref_states()

    # GPS noise model
    gps_noise = WhiteNoise(freq=ref.FREQ, duration=ref.SIMULATION_TIME, sd=0.5)

    # Generate realizations
    for real in range(ref.NUMBER_REALIZATION):

        # Gps measurement, noise on position @ ref freq
        gps_time = ref.generate_time_serie(freq=ref.GPS_FREQ)
        gps_states = ref.generate_ref_states(freq=ref.GPS_FREQ)
        gps_states[:, 0] = gps_noise.add_noise(gps_states[:, 0])  # x
        gps_states[:, 1] = gps_noise.add_noise(gps_states[:, 1])  # y

        # Kalman filter parameters
        x0 = ref_states[0]
        p0 = np.array([
            [sigma_p0, 0, 0, 0],
            [0, sigma_p0, 0, 0],
            [0, 0, sigma_v0, 0],
            [0, 0, 0, sigma_v0],
        ])

        dt = ref.DT


        F =
        phi = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 0, 0],  # Predicted velocity x ?
            [0, 0, 0, 0],  # Predicted velocity y ?

        ])
        q = np.array([

        ])
        h = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ])
        kf = KalmanFilter(x0, p0, phi, q, h)

        for i, t in enumerate(time):
            kf.predict()
            # Condition to add gps measure to kf
            if gps_states[i] is not None:
                z = None
                r = None
                kf.add_measure(z, r)


if __name__ == '__main__':
    main()
