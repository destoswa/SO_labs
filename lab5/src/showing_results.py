import matplotlib.pyplot as plt
import numpy as np
import os

"""
Folders for plots
"""
TIME_UNIT = 's'
LENGTH_UNIT = 'm'
ANGLE_UNIT = 'rad'
EXTENSIONS = ['jpg', 'svg']

"""
Plots
"""


def save_fig(fig, src, prefix, plot_name, extensions=None):
	"""
	Save fig with correct pathfile in all specified extensions
	"""
	if extensions is None:
		extensions = EXTENSIONS
	paths = [f"{src}/{prefix}_{plot_name}.{extension}" for extension in extensions]
	for path in paths:
		fig.savefig(path)


def show_trajectory(kf_states, gps_states, prefix, src, do_save_fig=False):
	"""
	Create plot with trajectory of res + additional plot zoomed on starting point
	"""
	# Estimated trajectory
	plt.rcParams.update({'font.size': 22})
	fig = plt.figure(figsize=(10, 10))
	plt.scatter(kf_states[:, 0], kf_states[:, 1], label='estimated trajectory', marker='.', alpha=0.8, linewidths=0.1)
	plt.scatter(gps_states[:, 0], gps_states[:, 1], label='estimated trajectory', marker='x', color='r', linewidths=1.5)
	plt.xlabel(f'E axis [m]')
	plt.ylabel(f'N axis [m]')
	plt.title(f'Trajectory : {prefix}')
	plt.tight_layout()
	if do_save_fig:
		save_fig(fig, src, prefix, plot_name='trajectory')
	plt.rcParams.update({'font.size': 10})


def show_error(kf_states, ref_states, sigma_pos, sigma_vel, freq,  prefix, src, do_save_fig=False):
	diff = kf_states - ref_states
	plt.rcParams.update({'font.size':14})
	fig, axs = plt.subplots(1, 2, figsize=(12, 6))
	lw = 3
	ls = '--'
	axs[0].scatter(diff[:, 0], diff[:, 1])
	axs[0].axline((-3*sigma_pos,0),(-3*sigma_pos,0.1), linewidth=lw, linestyle=ls, color='r')
	axs[0].axline((3*sigma_pos,0),(3*sigma_pos,0.1), linewidth=lw, linestyle=ls, color='r')
	axs[0].axline((0, -3*sigma_pos),(0.1, -3*sigma_pos), linewidth=lw, linestyle=ls, color='r')
	axs[0].axline((0, 3*sigma_pos),(0.1, 3*sigma_pos), linewidth=lw, linestyle=ls, color='r')
	axs[0].set_title('Position error')
	axs[0].set_ylabel('Northward [m]')
	axs[0].set_xlabel('Eastward [m]')
	axs[1].scatter(diff[:, 2], diff[:, 3])
	axs[1].axline((-3*sigma_vel,0),(-3*sigma_vel,0.1), linewidth=lw, linestyle=ls, color='r')
	axs[1].axline((3*sigma_vel,0),(3*sigma_vel,0.1), linewidth=lw, linestyle=ls, color='r')
	axs[1].axline((0, -3*sigma_vel),(0.1, -3*sigma_vel), linewidth=lw, linestyle=ls, color='r')
	axs[1].axline((0, 3*sigma_vel),(0.1, 3*sigma_vel), linewidth=lw, linestyle=ls, color='r')
	axs[1].set_title('Velocity error')
	axs[1].set_ylabel('Northward [m/s]')
	axs[1].set_xlabel('Eastward [m/s]')
	fig.suptitle(f"Errors on positions and velocities at {freq}Hz")
	plt.tight_layout()
	plt.rcParams.update({'font.size':10})
	if do_save_fig:
		save_fig(fig, src, str(freq) + "Hz_" + str(prefix), plot_name='errors')


def show_innovation(seq, prefix, src, do_save_fig=False):
	plt.rcParams.update({'font.size':14})
	fig,axs = plt.subplots(1,2, figsize=(12,6))
	axs[0].hist(seq[:,0])
	axs[0].set_title('North coordinates')
	axs[0].set_ylabel('count [-]')
	axs[0].set_xlabel('error [m]')
	axs[0].set_ylim([0, 50])
	axs[1].hist(seq[:,1])
	axs[1].set_title('East coordinates')
	axs[1].set_xlabel('error [m]')
	axs[1].set_ylim([0, 50])
	plt.tight_layout()
	if do_save_fig:
		save_fig(fig, src, prefix, plot_name='innovation')

	plt.rcParams.update({'font.size':10})