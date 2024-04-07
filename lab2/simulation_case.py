import param
from reference import generate_ref
from meas import generate_measurements
from methods import integration
from showing_results import *


class SimulationCase:
	"""
	Class defining a simulation case by its frequency and order of integration
	All other parameters are defined in param.py and are common to all cases
	It is also possible to instantiate true cases (no estimation, only true values)

	This class implement all methods useful to a simulation case :
		- Generate measurements in instantiation of the case
		- Generate estimation of (orientation, position, velocity) via integration
		- Generate results/plots with the estimations
	"""

	def __init__(self, result_dir, freq=1, order=1, true_case=False, include_acc=False):

		self.result_dir = result_dir
		self.freq = freq
		self.order = order
		self.true_res = generate_ref(freq)

		self.true_case = true_case
		self.include_acc = include_acc

		if true_case:
			self.prefix = f"{freq}Hz_true"
			self.res = self.true_res
		else:
			self.prefix = f"{freq}Hz_order{order}"
			time, acc_x, acc_y, gyro = generate_measurements(freq=freq)
			self.res = {'time': time, 'acc_x': acc_x, 'acc_y': acc_y, 'gyro': gyro}

	def integrate(self):
		"""
		Estimate the states of the simulation via integration of measurements with method of order self.order
		"""
		if self.true_case:
			return

		self.res = integration(
			acc_x=self.res['acc_x'],
			acc_y=self.res['acc_y'],
			gyro=self.res['gyro'],
			tetha_0=param.THETA_0,
			orientation_0=param.AZIMUTH_0,
			pos_N_0=param.P_0_NORTH,
			pos_E_0=param.P_0_EAST,
			vel_N_0=param.V_0_NORTH,
			vel_E_0=param.V_0_EAST,
			freq=self.freq,
			order=self.order
		)

	def compute_results(self):
		"""
		Create folder for plots
		Create plots
			Trajectory (+ zoom on start point)
			States (azimuth, position, velocity, OPTIONAL acceleration) over time
			Errors (deviation with true values) for all states (for non-true case)
			Print maximal errors for each state (for non-true case)
		"""
		create_folders(prefix=self.prefix, src=self.result_dir)
		show_trajectory(self.res, prefix=self.prefix, src=self.result_dir)
		show_evolution(self.true_res, self.res, prefix=self.prefix, src=self.result_dir,
					   add_acc=self.include_acc)
		if not self.true_case:
			show_error(self.true_res, self.res, prefix=self.prefix, src=self.result_dir,
					   add_acc=self.include_acc)
