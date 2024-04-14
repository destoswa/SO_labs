import plot_results as sr
import trajectory as tr


class SimulationCase:
	def __init__(self, prefix, measurements):
		self.prefix = prefix
		self.measurements = measurements
		self.true_trajectory = None
		self.trajectory = None

	def compute_trajectory(self, order):
		self.true_trajectory = tr.TrueTrajectory(measurements=self.measurements)
		self.true_trajectory.compute_trajectory()
		self.trajectory = tr.Trajectory(measurements=self.measurements)
		self.trajectory.compute_trajectory(order=order)

	def plot_trajectory(self, result_dir, include_acc=False):
		"""
		Create folder for plots
		Create plots
			Trajectory (+ zoom on start point)
			States (azimuth, position, velocity, OPTIONAL acceleration) over time
			Errors (deviation with true values) for all states
			Print maximal errors for each state (for non-true case)
		"""
		sr.create_folders(prefix=self.prefix, result_dir=result_dir)
		sr.show_error(result_dir=result_dir, simulation_case=self, add_acc=include_acc)
		sr.show_evolution(result_dir=result_dir, simulation_case=self, add_acc=include_acc)
		sr.show_trajectory(result_dir=result_dir, simulation_case=self)

	def __copy__(self):
		new_case = SimulationCase(self.prefix, self.measurements)
		new_case.trajectory = self.trajectory  # TODO : DeepCopy ?
		new_case.true_trajectory = self.true_trajectory  # TODO : DeepCopy ?
		return new_case

	def plot_reference_trajectory(self, result_dir, include_acc=False, prefix=None):
		reference_case = self.__copy__()
		reference_case.prefix = 'True trajectory' if prefix is None else prefix
		reference_case.trajectory = reference_case.true_trajectory
		reference_case.plot_trajectory(result_dir=result_dir, include_acc=include_acc)
