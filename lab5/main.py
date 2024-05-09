from src.kalman import KalmanFilter
from src.Noise import WhiteNoise
from src import reference as ref
import numpy as np

# Uncertainties for initial conditions
sigma_p0 = 10  # m
sigma_v0 = 0.1  # m/s

# Uncertainties of motion model
sigma_v = 0.05  # m/s² / Hz


def main():
    # Apply random seed for repeatability
    np.random.seed(42)

    # Reference position
    ref_states = ref.generate_ref_states()

    # Generate realizations
    time = ref.generate_time_serie()
    for real in range(ref.NUMBER_REALIZATION):

        # Gps
        gps_noise = WhiteNoise(freq=ref.FREQ, duration=ref.SIMULATION_TIME, sd=0.5)
        gps_states = np.copy(ref_states)
        gps_states[:, 0] = gps_noise.add_noise(ref_states[:, 0])  # x
        gps_states[:, 1] = gps_noise.add_noise(ref_states[:, 1])  # y
        # gps_states[:, 2:]                                       # v_ref    x and y
        # Set all states out of gps frequency to None


        # Kalman filter
        x0 = np.array([
            ref.X_0, ref.Y_0, ref.V_X_0, ref.V_Y_0
        ])

        p0 = np.array([
            [sigma_p0, 0, 0, 0],
            [0, sigma_p0, 0, 0],
            [0, 0, sigma_v0, 0],
            [0, 0, 0, sigma_v0],
        ])

        phi = None
        q = None
        h = None
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
