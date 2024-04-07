from simulation_case import SimulationCase

RESULT_DIRECTORY = './data/'
INCLUDE_ACCELERATION_IN_RESULTS = False


def main():
	# Instantiation of simulation cases
	case_10Hz_true = SimulationCase(freq=10, true_case=True)
	case_100Hz_true = SimulationCase(freq=100, true_case=True)
	case_10Hz_order1 = SimulationCase(freq=10, order=1)
	case_10Hz_order2 = SimulationCase(freq=10, order=2)
	case_100Hz_order1 = SimulationCase(freq=100, order=1)
	case_100Hz_order2 = SimulationCase(freq=100, order=2)

	# Integration of measurement to get estimation of orientation, position and velocity
	case_10Hz_order1.integrate()
	case_10Hz_order2.integrate()
	case_100Hz_order1.integrate()
	case_100Hz_order2.integrate()

	# Compute results : plots (trajectory, states evolution in time, errors) and maximal errors report
	case_10Hz_true.compute_results(result_dir=RESULT_DIRECTORY, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_100Hz_true.compute_results(result_dir=RESULT_DIRECTORY, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_10Hz_order1.compute_results(result_dir=RESULT_DIRECTORY, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_10Hz_order2.compute_results(result_dir=RESULT_DIRECTORY, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_100Hz_order1.compute_results(result_dir=RESULT_DIRECTORY, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_100Hz_order2.compute_results(result_dir=RESULT_DIRECTORY, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)


if __name__ == '__main__':
	main()
