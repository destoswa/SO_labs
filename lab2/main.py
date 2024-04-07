from simulation_case import SimulationCase

RESULT_DIRECTORY = './data/'
INCLUDE_ACCELERATION_IN_RESULTS = False


def main():
	# Instantiation of simulation cases
	case_10Hz_true = SimulationCase(result_dir=RESULT_DIRECTORY, freq=10, true_case=True, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_100Hz_true = SimulationCase(result_dir=RESULT_DIRECTORY, freq=10, true_case=True, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_10Hz_order1 = SimulationCase(result_dir=RESULT_DIRECTORY, freq=10, order=1, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_10Hz_order2 = SimulationCase(result_dir=RESULT_DIRECTORY, freq=10, order=2, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_100Hz_order1 = SimulationCase(result_dir=RESULT_DIRECTORY, freq=100, order=1, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)
	case_100Hz_order2 = SimulationCase(result_dir=RESULT_DIRECTORY, freq=100, order=2, include_acc=INCLUDE_ACCELERATION_IN_RESULTS)

	# Integration of measurement to get estimation of orientation, position and velocity
	case_10Hz_order1.integrate()
	case_10Hz_order2.integrate()
	case_100Hz_order1.integrate()
	case_100Hz_order2.integrate()

	# =============================================
	# ======= PLOTTING RESULTS ====================
	# =============================================

	case_10Hz_true.compute_results()
	case_100Hz_true.compute_results()
	case_10Hz_order1.compute_results()
	case_10Hz_order2.compute_results()
	case_100Hz_order1.compute_results()
	case_100Hz_order2.compute_results()


if __name__ == '__main__':
	main()
