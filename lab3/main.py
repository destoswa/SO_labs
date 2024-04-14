import simulation_case as sc
import measurements as ms
import param as pm
import noise_generator as ng


def main():
	# Instantiate the noise generator for each sensor
	noise_generators = {
		'acc_x': ng.NoiseGenerator(pm.acc_specs),
		'acc_y': ng.NoiseGenerator(pm.acc_specs),
		'gyro': ng.NoiseGenerator(pm.gyro_specs)
	}

	# Create the (noisy) measurements, and copy the 3 sub measurements with only 1 noisy sensor
	meas_nominal = ms.Measurements(freq=pm.FREQ)
	meas_noisy_all = ms.Measurements(freq=pm.FREQ, noise_generators=noise_generators)
	meas_noisy_acc_x = meas_noisy_all.select_noisy_sensor('acc_x')
	meas_noisy_acc_y = meas_noisy_all.select_noisy_sensor('acc_y')
	meas_noisy_gyro = meas_noisy_all.select_noisy_sensor('gyro')

	# Instantiate the simulation cases of interest
	case_reference = sc.SimulationCase(prefix='Reference', measurements=meas_nominal)
	case_all_noise = sc.SimulationCase(prefix='Noisy all', measurements=meas_noisy_all)
	case_noisy_acc_x = sc.SimulationCase(prefix='Noisy acc_x', measurements=meas_noisy_acc_x)
	case_noisy_acc_y = sc.SimulationCase(prefix='Noisy acc_y', measurements=meas_noisy_acc_y)
	case_noisy_gyro = sc.SimulationCase(prefix='Noisy gyro', measurements=meas_noisy_gyro)
	cases = [case_reference, case_all_noise, case_noisy_acc_x, case_noisy_acc_y, case_noisy_gyro]

	# Compute trajectories for each case
	[case.compute_trajectory(order=pm.ORDER) for case in cases]

	# Plot trajectories (2D trajectory, states evolution in time, errors)
	[case.plot_trajectory() for case in cases]


def compare_order_and_freq():  # Lab2 new code
	# Nominal measurements
	meas_10 = ms.Measurements(freq=10)
	meas_100 = ms.Measurements(freq=100)

	# Simulation cases
	case_reference = sc.SimulationCase(prefix='True_100', measurements=meas_100)
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
	case_reference.plot_trajectory()
	case_o1_10.plot_trajectory()
	case_o2_10.plot_trajectory()
	case_o1_100.plot_trajectory()
	case_o2_100.plot_trajectory()


if __name__ == '__main__':
	main()
	#compare_order_and_freq()  # Lab2
