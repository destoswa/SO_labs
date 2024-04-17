from lab3.src.navigation import Navigation as Nv
from lab3.src.sensor import Sensor as Sr
from lab3.src.nominal import constants as cst, nominal_fct as nf


# WIP
def compare_order_and_freq():  # Lab2 Adaptation to new code

    # Define the sensors without noise, and group them in a sensor collection for better manipulation
    time_fct = nf.get_time_serie
    sensors = [
        Sr.Sensor(sensor_id='acc_x', time_fct=time_fct, nominal_fct=nf.get_nominal_acc_x),
        Sr.Sensor(sensor_id='acc_y', time_fct=time_fct, nominal_fct=nf.get_nominal_acc_y),
        Sr.Sensor(sensor_id='gyro', time_fct=time_fct, nominal_fct=nf.get_nominal_gyro)
    ]
    sensor_collection = Sr.SensorCollection(sensors)

    # Nominal measurements
    meas_10 = sensor_collection.measure(freq=10)
    meas_10_nominal = meas_10.filter_noise()
    meas_100 = sensor_collection.measure(freq=100)
    meas_100_nominal = meas_100.filter_noise()

    # Simulation cases
    ic = cst.INITIAL_CONDITIONS
    case_reference_10 = Nv.Navigation(nav_id='True_10', initial_conditions=ic, measurements=meas_10_nominal,
                                      reference=True)
    case_reference_100 = Nv.Navigation(nav_id='True_100', initial_conditions=ic, measurements=meas_100_nominal,
                                       reference=True)
    case_o1_10 = Nv.Navigation(nav_id='10Hz_order_1', initial_conditions=ic, measurements=meas_10)
    case_o2_10 = Nv.Navigation(nav_id='10Hz_order_2', initial_conditions=ic, measurements=meas_10)
    case_o1_100 = Nv.Navigation(nav_id='100Hz_order_1', initial_conditions=ic, measurements=meas_100)
    case_o2_100 = Nv.Navigation(nav_id='100Hz_order_2', initial_conditions=ic, measurements=meas_100)

    # Compute trajectories
    case_o1_10.compute_trajectory(order=1)
    case_o2_10.compute_trajectory(order=2)
    case_o1_100.compute_trajectory(order=1)
    case_o2_100.compute_trajectory(order=2)

    # Plot
    result_dir = '../data/lab2/'
    case_o1_10.plot_trajectory(result_dir)
    case_o2_10.plot_trajectory(result_dir)
    case_o1_100.plot_trajectory(result_dir)
    case_o2_100.plot_trajectory(result_dir)
    case_reference_10.plot_trajectory(result_dir)
    case_reference_100.plot_trajectory(result_dir)


if __name__ == '__main__':
    compare_order_and_freq()
