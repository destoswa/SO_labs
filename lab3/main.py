import simulation_case as sc
import param as pm
import sensor as sr
import numpy as np


def main():
	# Apply random seed for repeatability
	np.random.seed(pm.RANDOM_SEED)

	# Define the sensors with their noises models, and group them in a sensor collection for better manipulation
	sensor_acc_x = sr.Sensor(sensor_id='acc_x', nominal_fct=pm.get_nominal_acc_x, noise_models=pm.ACC_NOISE_MODELS)
	sensor_acc_y = sr.Sensor(sensor_id='acc_y', nominal_fct=pm.get_nominal_acc_y, noise_models=pm.ACC_NOISE_MODELS)
	sensor_gyro = sr.Sensor(sensor_id='gyro', nominal_fct=pm.get_nominal_gyro, noise_models=pm.GYRO_NOISE_MODELS)
	sensor_collection = sr.SensorCollection(sensors=[sensor_acc_x, sensor_acc_y, sensor_gyro])

	# Create the measurements
	meas_noisy_all = sensor_collection.measure(pm.FREQ)
	meas_nominal = meas_noisy_all.filter_noise()
	meas_noisy_acc_x = meas_noisy_all.isolate_noise(sensor_id='acc_x')
	meas_noisy_acc_y = meas_noisy_all.isolate_noise(sensor_id='acc_y')
	meas_noisy_gyro = meas_noisy_all.isolate_noise(sensor_id='gyro')

	# Instantiate the simulation cases of interest
	case_reference = sc.SimulationCase(prefix='Reference', measurements=meas_nominal, reference=True)
	case_all_noise = sc.SimulationCase(prefix='Noisy', measurements=meas_noisy_all)
	case_noisy_acc_x = sc.SimulationCase(prefix='Noisy acc_x', measurements=meas_noisy_acc_x)
	case_noisy_acc_y = sc.SimulationCase(prefix='Noisy acc_y', measurements=meas_noisy_acc_y)
	case_noisy_gyro = sc.SimulationCase(prefix='Noisy gyro', measurements=meas_noisy_gyro)
	cases = [case_reference, case_all_noise, case_noisy_acc_x, case_noisy_acc_y, case_noisy_gyro]

	# Compute trajectories for each case
	[case.compute_trajectory(order=pm.ORDER) for case in cases]

	# Plot trajectories (2D trajectory, states evolution in time, errors)
	[case.plot_trajectory(verbose=True) for case in cases]


if __name__ == '__main__':
	main()


