import matplotlib.pyplot as plt
import numpy as np
from param import TIME_UNIT, LENGTH_UNIT, ANGLE_UNIT
import os

"""
Folders for plots
"""

EXTENSIONS = ['jpg', 'svg']


def create_folder(folder):
	if not os.path.exists(folder):
		os.mkdir(path=folder)


def create_folders(prefix, src, extensions=None):
	if extensions is None:
		extensions = EXTENSIONS

	extensions_folders = [f"{src}{extension}/" for extension in extensions]
	for extensions_folder in extensions_folders:
		create_folder(extensions_folder)

	folders = [f"{extensions_folder}{prefix}/" for extensions_folder in extensions_folders]
	for folder in folders:
		create_folder(folder)


"""
Plots
"""


def save_fig(fig, src, prefix, plot_name, extensions=None):
	if extensions is None:
		extensions = EXTENSIONS
	paths = [f"{src}/{extension}/{prefix}/{prefix}_{plot_name}.{extension}" for extension in extensions]
	for path in paths:
		fig.savefig(path)


def show_evolution(true_res, res, prefix, src, add_acc=False):
	# Evolution of state
	plot_name = 'states'
	fig, axs = plt.subplots(4 if add_acc else 3, 2, figsize=(10, 8))

	# Orientation
	axs[0, 0].plot(true_res['time'], res['orientation'], label='estimated orientation')
	axs[0, 0].set_ylabel(f'Orientation [{ANGLE_UNIT}]')
	axs[0, 0].set_xlabel(f'Time [{TIME_UNIT}]')
	axs[0, 0].legend()

	axs[0, 1].plot(true_res['time'], true_res['orientation'], label='true orientation')
	axs[0, 1].set_ylabel(f'Orientation[{ANGLE_UNIT}]')
	axs[0, 1].set_xlabel(f'Time [{TIME_UNIT}]')
	axs[0, 1].legend()

	# Position
	axs[1, 0].plot(true_res['time'], res['pos_N'], label="estimated pos_N")
	axs[1, 0].plot(true_res['time'], res['pos_E'], label="estimated pos_E")
	axs[1, 0].set_ylabel(f'Position [{LENGTH_UNIT}]')
	axs[1, 0].set_xlabel(f'Time [{TIME_UNIT}]')
	axs[1, 0].legend()

	axs[1, 1].plot(true_res['time'], true_res['pos_N'], label="true pos_N")
	axs[1, 1].plot(true_res['time'], true_res['pos_E'], label="true pos_E")
	axs[1, 1].set_ylabel(f'Position [{LENGTH_UNIT}]')
	axs[1, 1].set_xlabel(f'Time [{TIME_UNIT}]')
	axs[1, 1].legend()

	# Velocity
	axs[2, 0].plot(true_res['time'], res['vel_N'], label="estimated vel_N")
	axs[2, 0].plot(true_res['time'], res['vel_E'], label="estimated vel_E")
	axs[2, 0].set_ylabel(f'Velocity [{LENGTH_UNIT}/{TIME_UNIT}]')
	axs[2, 0].set_xlabel(f'Time [{TIME_UNIT}]')
	axs[2, 0].legend()

	axs[2, 1].plot(true_res['time'], true_res['vel_N'], label="true vel_N")
	axs[2, 1].plot(true_res['time'], true_res['vel_E'], label="true vel_E")
	axs[2, 1].set_ylabel(f'Velocity [{LENGTH_UNIT}/{TIME_UNIT}]')
	axs[2, 1].set_xlabel(f'Time [{TIME_UNIT}]')
	axs[2, 1].legend()

	# Acceleration
	if add_acc:
		axs[3, 0].plot(true_res['time'], res['acc_N'], label='estimated acc_N')
		axs[3, 0].plot(true_res['time'], res['acc_E'], label='estimated acc_E')
		axs[3, 0].set_ylabel(f'Acceleration [{LENGTH_UNIT}/{TIME_UNIT}²]')
		axs[3, 0].set_xlabel(f'Time [{TIME_UNIT}]')
		axs[3, 0].legend()

		axs[3, 1].plot(true_res['time'], true_res['acc_N'], label='true acc_N')
		axs[3, 1].plot(true_res['time'], true_res['acc_E'], label='true acc_E')
		axs[3, 1].set_ylabel(f'Acceleration [{LENGTH_UNIT}/{TIME_UNIT}²]')
		axs[3, 1].set_xlabel(f'Time [{TIME_UNIT}]')
		axs[3, 1].legend()

	fig.align_ylabels()
	save_fig(fig, src, prefix, plot_name=plot_name)
	plt.close()


def show_trajectory(res, prefix, src):
	# Estimated trajectory
	plt.rcParams.update({'font.size': 22})
	fig = plt.figure(figsize=(10, 10))
	plt.scatter(res['pos_E'], res['pos_N'], label='estimated trajectory', marker='.', alpha=0.8, linewidths=0.1)
	plt.xlabel(f'E axis [{LENGTH_UNIT}]')
	plt.ylabel(f'N axis [{LENGTH_UNIT}]')
	plt.title(prefix + 'Trajectory')
	plt.tight_layout()
	save_fig(fig, src, prefix, plot_name='trajectory')

	fig = plt.figure(figsize=(10, 4))
	plt.scatter(res['pos_E'], res['pos_N'], label='estimated trajectory', marker='.', alpha=0.8, linewidths=0.1)
	plt.xlabel(f'E axis [{LENGTH_UNIT}]')
	plt.ylabel(f'N axis [{LENGTH_UNIT}]')
	plt.ylim([480, 520])
	plt.xlim([-100, 100])
	plt.tight_layout()
	plt.title(prefix + 'Trajectory - Zoom')
	save_fig(fig, src, prefix, plot_name='trajectory_zoom')
	plt.close()
	plt.rcParams.update({'font.size': 10})


def show_error(true_res, res, prefix, src, add_acc=False):
	plot_name = 'errors'

	plt.rcParams.update({'font.size': 16})
	fig, axs = plt.subplots(4 if add_acc else 3, 1, figsize=(10, 8))
	# Azimuth
	axs[0].plot(true_res['time'], res['orientation'] - true_res['orientation'])
	axs[0].set_ylabel(f'Azimuth [{ANGLE_UNIT}]')
	axs[0].set_xlabel(f'Time [{TIME_UNIT}]')
	# Position
	axs[1].plot(true_res['time'], res['pos_E'] - true_res['pos_E'], label='pos_E')
	axs[1].plot(true_res['time'], res['pos_N'] - true_res['pos_N'], label='pos_N')
	axs[1].set_ylabel(f'Position [{LENGTH_UNIT}]')
	axs[1].set_xlabel(f'Time [{TIME_UNIT}]')
	axs[1].legend()
	# Velocity
	axs[2].plot(true_res['time'], res['vel_E'] - true_res['vel_E'], label="vel_E")
	axs[2].plot(true_res['time'], res['vel_N'] - true_res['vel_N'], label="vel_N")
	axs[2].set_ylabel(f'Velocity [{LENGTH_UNIT}/{TIME_UNIT}]')
	axs[2].set_xlabel(f'Time [{TIME_UNIT}]')
	axs[2].legend()
	# Acceleration
	if add_acc:
		axs[3].plot(true_res['time'], res['acc_E'] - true_res['acc_E'], label='acc_E')
		axs[3].plot(true_res['time'], res['acc_N'] - true_res['acc_N'], label='acc_N')
		axs[3].set_ylabel(f'Acceleration [{LENGTH_UNIT}/{TIME_UNIT}²]')
		axs[3].set_xlabel(f'Time [{TIME_UNIT}]')
		axs[3].legend()

	fig.align_ylabels()
	plt.tight_layout()
	save_fig(fig, src, prefix, plot_name=plot_name)
	plt.close()
	plt.rcParams.update({'font.size': 10})

	# Maximal error report
	max_error_report = (f"MAX ERROR - {prefix}"
						f"\n\t- On azimuth "
						f"\n\t\t {np.max(np.abs(true_res['theta'] - (res['orientation'] - np.pi / 2))):.3E} [{ANGLE_UNIT}]"
						f"\n\t- On position"
						f"\n\t\t P_E : {np.max((np.abs(true_res['pos_E'] - res['pos_E']))):.3E} [{LENGTH_UNIT}]"
						f"\n\t\t P_N : {np.max((np.abs(true_res['pos_N'] - res['pos_N']))):.3E} [{LENGTH_UNIT}]"
						f"\n\t- On velocity"
						f"\n\t\t V_E : {np.max((np.abs(true_res['vel_E'] - res['vel_E']))):.3E} [{LENGTH_UNIT}/{TIME_UNIT}]"
						f"\n\t\t V_N : {np.max((np.abs(true_res['vel_N'] - res['vel_N']))):.3E} [{LENGTH_UNIT}/{TIME_UNIT}]")

	if add_acc:
		max_error_report += (
						f"\n\t- On acceleration"
						f"\n\t\t A_E : {np.max((np.abs(true_res['acc_E'] - res['acc_E']))):.3E} [{LENGTH_UNIT}/{TIME_UNIT}²]"
						f"\n\t\t A_N : {np.max((np.abs(true_res['acc_N'] - res['acc_N']))):.3E} [{LENGTH_UNIT}/{TIME_UNIT}²]")
	max_error_report += "\n"

	# Print and save the max error report
	print(max_error_report)
	with open(src + 'max_error_report.txt', 'w') as f:
		f.write(max_error_report)


def show_results(src, prefix, res, true_res, include_acc, true_case=False):
	""" Create plots for each case
			- Trajectory
			- States over time (azimuth, position, velocity)
			- Errors (deviation with true values) for all states
			- Print maximal errors for each state

			Optional : you can also include acceleration in plots with the include_acc boolean argument
			Optional : you can specify if the case is a true case to avoid printing the trivial null errors
	"""
	create_folders(prefix=prefix, src=src)
	show_trajectory(res, prefix=prefix, src=src)
	show_evolution(true_res, res, prefix=prefix, src=src,
				   add_acc=include_acc)
	if not true_case:
		show_error(true_res, res, prefix=prefix, src=src,
				   add_acc=include_acc)
