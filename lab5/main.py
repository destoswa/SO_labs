#from src.kalman import Kalman
from src.Noise import Bias, WhiteNoise, RandomWalk, GaussMarkov
import reference as ref
import numpy as np


def main():
    # Apply random seed for repeatability
    np.random.seed(42)

    # Define the sensor
    GPS_noise_x = Bias(freq=1, duration=ref.SIMULATION_TIME, bias_sd=0.5)
    GPS_noise_y = Bias(freq=1, duration=ref.SIMULATION_TIME, bias_sd=0.5)


if __name__ == '__main__':
    main()
