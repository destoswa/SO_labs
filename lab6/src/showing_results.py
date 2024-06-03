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
EXTENSIONS = [ 'svg']

"""
Plots
"""

def fig_ref_traj(ref_states):

    plt.clf()
    plt.plot(ref_states[:, 4], ref_states[:, 3])
    plt.savefig("results/reference_trajectory.svg")

def fig_ref_imu(ref_imu):
    plt.clf()
    _, axs = plt.subplots(2,1)
    axs[0].plot(ref_imu[:,:2], label=["acc_x", "acc_y"])
    axs[0].legend()
    
    axs[1].plot(ref_imu[:, 2], label="gyro")
    axs[1].legend()
    plt.savefig("results/reference_imu.svg")

def fig_gps(gps):
    plt.clf()
    plt.plot(gps[::200,1], gps[::200, 0])
    plt.savefig("results/gps.svg")

def fig_imu(imu):
    plt.clf()
    _, axs = plt.subplots(2,1)
    axs[0].plot(imu[:,:2], label="acc")
    axs[0].legend()
    
    axs[1].plot(imu[:, 2], label="gyro")
    axs[1].legend()
    plt.savefig("results/imu.svg")

def fig_traj(X, ref, gps):
    plt.clf()
    plt.plot(X[:, 4], X[:, 3], label="Estimation")
    plt.plot(ref[:, 4], ref[:,3], label="Truth")
    plt.plot(gps[:,0], gps[:,1], label="GPS", marker="x")
    plt.legend()
    plt.savefig("results/traj.svg")












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


def show_error(kf_states, ref_states, kf_covar_states, freq, gps_freq,  prefix, src, do_save_fig=True):
    diff = kf_states - ref_states
    
    dt_diff = 1/freq
    time_diff = np.arange(0, len(diff) * dt_diff, dt_diff)
    time_gps = time_diff[::int(freq/gps_freq)]
    simulation_time = time_diff[-1]

    plt.rcParams.update({'font.size':14})
    fig, axs = plt.subplots(5, 1, figsize=(10, 10), sharex=True)
    lw = 1.5
    ls = '--'
    y_labels = ['Attitude [rad]', 'Vel N [m/s]', 'Vel E [m/s]', 'Pos N [m]', 'Pos E [m]']
    fig.suptitle(f"Errors on positions and velocities at {freq}Hz")
    for i in range(5):
        axs[i].plot(time_diff, diff[:, i])
        axs[i].plot(time_gps, 3 * np.sqrt(kf_covar_states[::int(freq/gps_freq), i, i]), linewidth=lw, linestyle=ls, color='r' )
        axs[i].plot(time_gps, -3 * np.sqrt(kf_covar_states[::int(freq/gps_freq), i, i]), linewidth=lw, linestyle=ls, color='r' )
        axs[i].set_ylabel(y_labels[i])
        ymax = np.max(np.quantile(3*np.sqrt(kf_covar_states[:, i, i]), 0.9)) * 1.5
        axs[i].set_ylim([-ymax, ymax])
        axs[i].set_xlim([0, simulation_time])
        axs[i].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs[-1].set_xlabel("Timestamp [s]")
    plt.tight_layout()
    plt.rcParams.update({'font.size':10})
    if do_save_fig:
        save_fig(fig, src, str(freq) + "Hz_" + str(prefix), plot_name='errors')


def show_innovation(seq, prefix, src, do_save_fig= True):
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


def show_imu_error(kf_states, ref_states, kf_covar_states, freq, gps_freq,  prefix, src, do_save_fig=True):
    diff = kf_states - ref_states
    
    dt_diff = 1/freq
    time_diff = np.arange(0, len(diff) * dt_diff, dt_diff)
    time_gps = time_diff[::int(freq/gps_freq)]
    simulation_time = time_diff[-1]

    plt.rcParams.update({'font.size':14})
    fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)
    lw = 1.5
    ls = '--'
    y_labels = ['Gyro bias [rad/s]', 'Gyro [rad/s]', 'Acc N [m/s²]', 'Acc E [m/s²]', ]
    fig.suptitle(f"Errors on imu states at {freq}Hz")
    for i, ax in enumerate(axs, start=5):
        ax.plot(time_diff, diff[:, i])
        ax.plot(time_gps, 3 * np.sqrt(kf_covar_states[::int(freq/gps_freq), i, i]), linewidth=lw, linestyle=ls, color='r' )
        ax.plot(time_gps, -3 * np.sqrt(kf_covar_states[::int(freq/gps_freq), i, i]), linewidth=lw, linestyle=ls, color='r' )
        ax.set_ylabel(y_labels[i-5])
        ymax = np.max(np.quantile(3*np.sqrt(kf_covar_states[:, i, i]), 0.9)) * 1.5
        ax.set_ylim([-ymax, ymax])
        ax.set_xlim([0, simulation_time])
        #ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs[-1].set_xlabel("Timestamp [s]")
    plt.tight_layout()
    plt.rcParams.update({'font.size':10})
    if do_save_fig:
        save_fig(fig, src, str(freq) + "Hz_" + str(prefix), plot_name='errors')