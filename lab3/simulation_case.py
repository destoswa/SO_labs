import plot_results as sr
import trajectory as tr
import param as pm


class SimulationCase:
	def __init__(self, prefix, measurements, reference=False):
		self.prefix = prefix
		self.measurements = measurements
		self.reference = reference
		self.true_trajectory = tr.TrueTrajectory(measurements=self.measurements)
		self.true_trajectory.compute_trajectory()
		self.trajectory = self.true_trajectory if reference else None

	def compute_trajectory(self, order):
		if not self.reference:
			self.trajectory = tr.Trajectory(measurements=self.measurements)
			self.trajectory.compute_trajectory(order=order)

	def plot_trajectory(self, result_dir=pm.PLOTS_DIR, include_acc=False, verbose=False):
		"""
		Create folder for plots
		Create plots
			Trajectory (+ zoom on start point)
			States (azimuth, position, velocity, OPTIONAL acceleration) over time
			Errors (deviation with true values) for all states
			Print maximal errors for each state (for non-true case)
		"""
		sr.create_folders(prefix=self.prefix, result_dir=result_dir)
		sr.show_error(result_dir=result_dir, simulation_case=self, add_acc=include_acc, verbose=verbose)
		sr.show_evolution(result_dir=result_dir, simulation_case=self, add_acc=include_acc)
		sr.show_trajectory(result_dir=result_dir, simulation_case=self)
