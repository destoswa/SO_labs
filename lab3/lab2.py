import simulation_case as sc
import sensor as sr
import param as pm


# WIP
def compare_order_and_freq():  # Lab2 Adaptation to new code

	# Define the sensors without noise, and group them in a sensor collection for better manipulation
	sensor_acc_x = sr.Sensor(sensor_id='acc_x', nominal_fct=pm.get_nominal_acc_x)
	sensor_acc_y = sr.Sensor(sensor_id='acc_y', nominal_fct=pm.get_nominal_acc_y)
	sensor_gyro = sr.Sensor(sensor_id='gyro', nominal_fct=pm.get_nominal_gyro)
	sensor_collection = sr.SensorCollection(sensors=[sensor_acc_x, sensor_acc_y, sensor_gyro])

	# Nominal measurements
	meas_10 = sensor_collection.measure(freq=10)
	meas_100 = sensor_collection.measure(freq=100)
	meas_100_nominal = meas_100.filter_noise()

	# Simulation cases
	case_reference = sc.SimulationCase(prefix='True_100', measurements=meas_100_nominal, reference=True)
	case_o1_10 = sc.SimulationCase(prefix='O1_10', measurements=meas_10)
	case_o2_10 = sc.SimulationCase(prefix='O2_10', measurements=meas_10)
	case_o1_100 = sc.SimulationCase(prefix='O1_100', measurements=meas_100)
	case_o2_100 = sc.SimulationCase(prefix='O2_100', measurements=meas_100)

	# Compute trajectories
	case_o1_10.compute_trajectory(order=1)
	case_o2_10.compute_trajectory(order=2)
	case_o1_100.compute_trajectory(order=1)
	case_o2_100.compute_trajectory(order=2)

	# Plot
	result_dir = 'data/lab2/'
	case_o1_10.plot_trajectory(result_dir)
	case_o2_10.plot_trajectory(result_dir)
	case_o1_100.plot_trajectory(result_dir)
	case_o2_100.plot_trajectory(result_dir)
	case_reference.plot_trajectory(result_dir)


if __name__ == '__main__':
	compare_order_and_freq()
