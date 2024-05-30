import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
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

def fig_ref_traj(ref_states):

    plt.clf()
    plt.plot(ref_states[:, 4], ref_states[:, 3])
    plt.savefig("lab6/results/reference_trajectory.jpg")

def fig_ref_imu(ref_imu):
    plt.clf()
    _, axs = plt.subplots(2,1)
    axs[0].plot(ref_imu[:,:2], label=["acc_x", "acc_y"])
    axs[0].legend()
    
    axs[1].plot(ref_imu[:, 2], label="gyro")
    axs[1].legend()
    plt.savefig("lab6/results/reference_imu.jpg")

def fig_gps(gps):
    plt.clf()
    plt.plot(gps[::200,1], gps[::200, 0])
    plt.savefig("lab6/results/gps.jpg")

def fig_imu(imu):
    plt.clf()
    _, axs = plt.subplots(2,1)
    axs[0].plot(imu[:,:2], label="acc")
    axs[0].legend()
    
    axs[1].plot(imu[:, 2], label="gyro")
    axs[1].legend()
    plt.savefig("lab6/results/imu.jpg")

def fig_traj(X, ref, gps):
    plt.clf()
    plt.plot(X[:, 4], X[:, 3], label="Estimation")
    plt.plot(ref[:, 4], ref[:,3], label="Truth")
    plt.plot(gps[:,0], gps[:,1], label="GPS", marker="x")
    plt.legend()
    plt.savefig("lab6/results/traj.jpg")












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
    #plt.scatter(kf_states[:, 1], kf_states[:, 0], label='estimated trajectory', marker='.', alpha=0.8, linewidths=0.1)
    plt.scatter(gps_states[:, 1], gps_states[:, 0], label='gps', marker='x', color='r', linewidths=1.5)
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
    fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)
    lw = 1.5
    ls = '--'
    sigmas = [sigma_pos, sigma_pos, sigma_vel, sigma_vel]
    y_labels = ['Pos N [m]', 'Pos E [m]', 'Vel N [m/s]', 'Vel E [m/s]', ]
    fig.suptitle(f"Errors on positions and velocities at {freq}Hz")
    for i in range(4):
        axs[i].plot(range(len(diff[:, i])), diff[:, i])
        axs[i].axline((0, -3 * sigmas[i]),(0.1, -3 * sigmas[i]), linewidth=lw, linestyle=ls, color='r')
        axs[i].axline((0, 3 * sigmas[i]),(0.1, 3 * sigmas[i]), linewidth=lw, linestyle=ls, color='r')
        axs[i].set_ylabel(y_labels[i])
        ymax = max(max(diff[:, i]), 3*sigmas[i]) * 1.5
        axs[i].set_ylim([-ymax, ymax])
        axs[i].set_xlim([0, len(diff[:, i])])
        axs[i].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs[-1].set_xlabel("Timestamp [s]")
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