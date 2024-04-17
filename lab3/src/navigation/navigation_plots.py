import matplotlib.pyplot as plt
import numpy as np
import os
from lab3.src.nominal.constants import TIME_UNIT, LENGTH_UNIT, ANGLE_UNIT

"""
Folders for plots
"""

EXTENSIONS = ['jpg', 'svg']


def create_folder(folder):
    """
    Create folder if it does not exist
    """
    if not os.path.exists(folder):
        os.mkdir(path=folder)


def create_folders(prefix, result_dir, extensions=None):
    """
    Create all required results folders for a simulation case
    """
    # Result folder
    create_folder(result_dir)

    # Report folders
    report_folder = f'{result_dir}/error_reports/'
    create_folder(report_folder)

    # Plot folders
    if extensions is None:
        extensions = EXTENSIONS
    extensions_folders = [f"{result_dir}{extension}/" for extension in extensions]
    for extensions_folder in extensions_folders:
        create_folder(extensions_folder)

    folders = [f"{extensions_folder}{prefix}/" for extensions_folder in extensions_folders]
    for folder in folders:
        create_folder(folder)


def save_fig(fig, result_dir, prefix, plot_name, extensions=None):
    """
    Save fig with correct pathfile in all specified extensions
    """
    if extensions is None:
        extensions = EXTENSIONS
    paths = [f"{result_dir}/{extension}/{prefix}/{prefix}_{plot_name}.{extension}" for extension in extensions]
    for path in paths:
        fig.savefig(path)


def max_abs_error(a, b):
    """
    Calculate the maximum absolute error between two arrays.

    Args:
        a (ndarray): First array.
        b (ndarray): Second array.

    Returns:
        float: Maximum absolute error.

    """
    return np.max(np.abs(a - b))


def show_error(result_dir, navigation, add_acc=False, verbose=False):
    """
    Plot the difference between states of true_res (true states) and res (approximation of states).

    Saves and display the maximal absolute error for each state.

    Args:
        result_dir (str): Directory to save the plots and reports.
        navigation: Object representing the navigation.
        add_acc (bool, optional): Whether to include acceleration in the plots. Defaults to False.
        verbose (bool, optional): Whether to print the error report. Defaults to False.

    """
    # Define main elements in plot
    plot_name = 'errors'
    prefix = navigation.nav_id
    trajectory = navigation.trajectory
    true_trajectory = navigation.true_trajectory
    time = trajectory.time

    # Subplot + titles
    n_rows = 4 if add_acc else 3
    fig, axs = plt.subplots(nrows=n_rows, ncols=1, figsize=(10, 8), sharex='row')
    fig.suptitle('Deviation from true trajectory (PVA)', fontsize=16)
    axs[n_rows - 1].set_xlabel(f'Time [{TIME_UNIT}]', size='large')

    # Azimuth
    axs[0].plot(time, trajectory.azimuth - true_trajectory.azimuth)
    axs[0].set_ylabel(f'Azimuth [{ANGLE_UNIT}]', rotation=90, size='large')

    # Position
    axs[1].plot(time, trajectory.p_N - true_trajectory.p_N, label='North')
    axs[1].plot(time, trajectory.p_E - true_trajectory.p_E, label='East')
    axs[1].set_ylabel(f'Position [{LENGTH_UNIT}]', rotation=90, size='large')
    axs[1].legend()

    # Velocity
    axs[2].plot(time, trajectory.v_N - true_trajectory.v_N, label='North')
    axs[2].plot(time, trajectory.v_E - true_trajectory.v_E, label='East')
    axs[2].set_ylabel(f'Velocity [{LENGTH_UNIT}/{TIME_UNIT}]', rotation=90, size='large')
    axs[2].legend()

    # Acceleration
    if add_acc:
        axs[3].plot(time, trajectory.acc_N - true_trajectory.acc_N, label='North')
        axs[3].plot(time, trajectory.acc_E - true_trajectory.acc_E, label='East')
        axs[3].set_ylabel(f'Acceleration [{LENGTH_UNIT}/{TIME_UNIT}²]', rotation=90, size='large')
        axs[3].legend()

    fig.align_ylabels()
    plt.tight_layout()
    save_fig(fig, result_dir, prefix, plot_name=plot_name)
    plt.close()
    plt.rcParams.update({'font.size': 10})

    # Maximal error report
    max_azimuth_error = max_abs_error(true_trajectory.azimuth, trajectory.azimuth)
    max_p_E_error = max_abs_error(true_trajectory.p_E, trajectory.p_E)
    max_p_N_error = max_abs_error(true_trajectory.p_N, trajectory.p_N)
    max_v_E_error = max_abs_error(true_trajectory.v_E, trajectory.v_E)
    max_v_N_error = max_abs_error(true_trajectory.v_N, trajectory.v_N)

    max_error_report = (f"MAX ABSOLUTE ERROR - {prefix}"
                        f"\n\t- On azimuth "
                        f"\n\t\t {max_azimuth_error:.3E} [{ANGLE_UNIT}]"
                        f"\n\t- On position"
                        f"\n\t\t P_E : {max_p_E_error:.3E} [{LENGTH_UNIT}]"
                        f"\n\t\t P_N : {max_p_N_error:.3E} [{LENGTH_UNIT}]"
                        f"\n\t- On velocity"
                        f"\n\t\t V_E : {max_v_E_error:.3E} [{LENGTH_UNIT}/{TIME_UNIT}]"
                        f"\n\t\t V_N : {max_v_N_error:.3E} [{LENGTH_UNIT}/{TIME_UNIT}]")

    if add_acc:
        max_acc_E_error = max_abs_error(true_trajectory.acc_E, trajectory.acc_E)
        max_acc_N_error = max_abs_error(true_trajectory.acc_N, trajectory.acc_N)

        max_error_report += (
            f"\n\t- On acceleration"
            f"\n\t\t A_E : {max_acc_E_error:.3E} [{LENGTH_UNIT}/{TIME_UNIT}²]"
            f"\n\t\t A_N : {max_acc_N_error:.3E} [{LENGTH_UNIT}/{TIME_UNIT}²]")
    max_error_report += "\n"

    # Print and save the max error report
    if verbose:
        print(max_error_report)
    path = f'{result_dir}error_reports/max_error_report_{prefix}.txt'
    with open(path, 'w') as f:
        f.write(max_error_report)


def show_evolution(result_dir, navigation, add_acc=False):
    """
    Create subplots with the evolution of states (orientation, position, velocity, OPTIONAL acceleration) in time.
    Comparison between true trajectory states and estimated trajectory states.

    Args:
        result_dir (str): Directory to save the plots.
        navigation: Object representing the navigation case.
        add_acc (bool, optional): Whether to include acceleration in the plots. Defaults to False.

    """
    # Define main elements in plot
    plot_name = 'states'
    prefix = navigation.nav_id
    true_trajectory = navigation.true_trajectory
    trajectory = navigation.trajectory
    time = trajectory.time

    # Subplot + titles
    cols = ['Estimated', 'True']
    rows = [f'Azimuth [{ANGLE_UNIT}]', f'Position [{LENGTH_UNIT}]', f'Velocity [{LENGTH_UNIT}/{TIME_UNIT}]']
    if add_acc:
        rows += f'Acceleration [{LENGTH_UNIT}/{TIME_UNIT}²]'
    fig, axs = plt.subplots(nrows=len(rows), ncols=2, figsize=(10, 8), sharey='row', sharex=True)

    for ax in (axs[-1, 0], axs[-1, 1]):
        ax.set_xlabel(f'Time {TIME_UNIT}', size='large')
    for ax, row in zip(axs[:, 0], rows):
        ax.set_ylabel(row, rotation=90, size='large')
    for ax, col in zip(axs[0], cols):
        ax.set_title(col)

    # Azimuth
    axs[0, 0].plot(time, trajectory.azimuth)
    axs[0, 1].plot(time, true_trajectory.azimuth)

    # Position
    axs[1, 0].plot(time, trajectory.p_N, label="North")
    axs[1, 0].plot(time, trajectory.p_E, label="East")
    axs[1, 0].legend()

    axs[1, 1].plot(time, true_trajectory.p_N, label="North")
    axs[1, 1].plot(time, true_trajectory.p_E, label="East")
    axs[1, 1].legend()

    # Velocity
    axs[2, 0].plot(time, trajectory.v_N, label="North")
    axs[2, 0].plot(time, trajectory.v_E, label="East")
    axs[2, 0].legend()

    axs[2, 1].plot(time, true_trajectory.v_N, label="North")
    axs[2, 1].plot(time, true_trajectory.v_E, label="East")
    axs[2, 1].legend()

    # Acceleration
    if add_acc:
        axs[3, 0].plot(time, trajectory.acc_N, label='North')
        axs[3, 0].plot(time, trajectory.acc_E, label='East')
        axs[3, 0].legend()

        axs[3, 1].plot(time, true_trajectory.acc_N, label='North')
        axs[3, 1].plot(time, true_trajectory.acc_E, label='East')
        axs[3, 1].legend()

    fig.align_ylabels()
    save_fig(fig, result_dir, prefix, plot_name=plot_name)
    plt.close()


def show_trajectory(result_dir, navigation):
    """
    Create plot of 2D trajectory + additional plot zoomed on starting point.

    Args:
        result_dir (str): Directory to save the plots.
        navigation: Object representing the navigation case.

    """
    # Define main elements in plot
    plot_name = 'trajectory'
    plot_name_zoom = 'trajectory_zoom'
    prefix = navigation.nav_id
    trajectory = navigation.trajectory
    plt.rcParams.update({'font.size': 22})

    # Trajectory
    fig = plt.figure(figsize=(10, 10))
    plt.scatter(trajectory.p_E, trajectory.p_N, marker='.', alpha=0.8, linewidths=0.1)
    plt.xlabel(f'East [{LENGTH_UNIT}]')
    plt.ylabel(f'North [{LENGTH_UNIT}]')
    plt.title(f'Trajectory : {prefix}')
    plt.tight_layout()
    save_fig(fig, result_dir, prefix, plot_name=plot_name)

    # Zoom on trajectory
    fig = plt.figure(figsize=(10, 4))
    plt.scatter(trajectory.p_E, trajectory.p_N, marker='.', alpha=0.8, linewidths=0.1)
    plt.xlabel(f'East [{LENGTH_UNIT}]')
    plt.ylabel(f'North [{LENGTH_UNIT}]')
    plt.ylim([480, 520])
    plt.xlim([-100, 100])
    plt.tight_layout()
    plt.title(f'Trajectory - zoom : {prefix}')
    save_fig(fig, result_dir, prefix, plot_name=plot_name_zoom)
    plt.close()

    # Change back font size in plt
    plt.rcParams.update({'font.size': 10})
