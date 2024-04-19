from src.navigation import Navigation as Nv
from src.sensor import Sensor as Sr, SensorSystem as SrS
from src.reference import constants as cst, nominal_fct as nf
import numpy as np


def main():
    # Apply random seed for repeatability
    np.random.seed(cst.RANDOM_SEED)

    # Define the sensors with their noises models, and group them in a sensor collection for better manipulation
    time_fct = nf.get_time_serie
    sensors = [
        Sr.Sensor(sensor_id='acc_x', time_fct=time_fct, nominal_fct=nf.get_nominal_acc_x,
                  noise_models=cst.ACC_NOISE_MODELS),
        Sr.Sensor(sensor_id='acc_y', time_fct=time_fct, nominal_fct=nf.get_nominal_acc_y,
                  noise_models=cst.ACC_NOISE_MODELS),
        Sr.Sensor(sensor_id='gyro', time_fct=time_fct, nominal_fct=nf.get_nominal_gyro,
                  noise_models=cst.GYRO_NOISE_MODELS)
    ]
    sensor_system = SrS.SensorSystem(sensors)

    # Create the collection of measurements for each case
    meas_noisy_all = sensor_system.measure(cst.FREQ)
    meas_nominal = meas_noisy_all.filter_noise()
    meas_noisy_acc_x = meas_noisy_all.isolate_noise(sensor_id='acc_x')
    meas_noisy_acc_y = meas_noisy_all.isolate_noise(sensor_id='acc_y')
    meas_noisy_gyro = meas_noisy_all.isolate_noise(sensor_id='gyro')

    # Instantiate the navigation cases
    ic = cst.INITIAL_CONDITIONS
    cases = [
        Nv.Navigation(nav_id='Reference', initial_conditions=ic, measurements=meas_nominal, reference=True),
        Nv.Navigation(nav_id='Noisy', initial_conditions=ic, measurements=meas_noisy_all),
        Nv.Navigation(nav_id='Noisy acc_x', initial_conditions=ic, measurements=meas_noisy_acc_x),
        Nv.Navigation(nav_id='Noisy acc_y', initial_conditions=ic, measurements=meas_noisy_acc_y),
        Nv.Navigation(nav_id='Noisy gyro', initial_conditions=ic, measurements=meas_noisy_gyro)
    ]

    # Compute trajectories for each case
    [case.compute_trajectory(order=cst.ORDER) for case in cases]

    # Plot trajectories (2D trajectory, states evolution in time, errors)
    [case.plot_trajectory(result_dir=cst.PLOTS_DIR, verbose=True) for case in cases]


if __name__ == '__main__':
    main()
