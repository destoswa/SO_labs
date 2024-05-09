from src.navigation import Navigation as Nv
from src.sensor import Sensor as Sr, SensorSystem as SrS
from src.kalman import Kalman
from src.reference import constants as cst, nominal_fct as nf
import numpy as np


def main():
    # Apply random seed for repeatability
    np.random.seed(cst.RANDOM_SEED)

    # Define the sensor
    time_fct = nf.get_time_serie
    sensor = Sr.Sensor(sensor_id='gps_x', time_fct=time_fct, nominal_fct=nf.get_nominal_acc_x,
                  noise_models=cst.ACC_NOISE_MODELS),


if __name__ == '__main__':
    main()
