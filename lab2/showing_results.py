import matplotlib.pyplot as plt
import numpy as np


def show_evolution(true_res, res, azimuth_0, prefix, src):
    # Evolution of state
    fig, axs = plt.subplots(4, 2, figsize=(10, 8))

    axs[0, 0].plot(true_res['time'], res['orientation'], label='orientation')
    axs[0, 0].legend()

    axs[0, 1].plot(true_res['time'], true_res['theta'] + azimuth_0, label='orientation')
    axs[0, 1].legend()

    axs[1, 0].plot(true_res['time'], res['acc_N'], label='estimated acc_N')
    axs[1, 0].plot(true_res['time'], res['acc_E'], label='estimated acc_E')
    axs[1, 0].legend()

    axs[1, 1].plot(true_res['time'], true_res['acc_N'], label='true acc_N')
    axs[1, 1].plot(true_res['time'], true_res['acc_E'], label='true acc_E')
    axs[1, 1].legend()

    axs[2, 0].plot(true_res['time'], res['vel_N'], label="vel_N")
    axs[2, 0].plot(true_res['time'], res['vel_E'], label="vel_E")
    axs[2, 0].legend()

    axs[2, 1].plot(true_res['time'], true_res['vel_N'], label="true vel_N")
    axs[2, 1].plot(true_res['time'], true_res['vel_E'], label="true vel_E")
    axs[2, 1].legend()

    axs[3, 0].plot(true_res['time'], res['pos_N'], label="estimated pos_N")
    axs[3, 0].plot(true_res['time'], res['pos_E'], label="estimated pos_E")
    axs[3, 0].legend()

    axs[3, 1].plot(true_res['time'], true_res['pos_N'], label="true pos_N")
    axs[3, 1].plot(true_res['time'], true_res['pos_E'], label="true pos_E")
    axs[3, 1].legend()

    fig.savefig(src + '/' + prefix + 'states.jpg')
    plt.close()


def show_deviation(true_res, res, azimuth_0, prefix, src):
    # Deviation of state
    fig, axs = plt.subplots(4, 1, figsize=(10, 8))

    axs[0].plot(true_res['time'], res['orientation'] - (true_res['theta'] + azimuth_0), label='orientation')
    axs[0].legend()

    axs[1].plot(true_res['time'], res['acc_N'] - true_res['acc_N'], label=' acc_N')
    axs[1].plot(true_res['time'], res['acc_E'] - true_res['acc_E'], label=' acc_E')
    axs[1].legend()

    axs[2].plot(true_res['time'], res['vel_N'] - true_res['vel_N'], label="vel_N")
    axs[2].plot(true_res['time'], res['vel_E'] - true_res['vel_E'], label="vel_E")
    axs[2].legend()

    axs[3].plot(true_res['time'], res['pos_N'] - true_res['pos_N'], label="pos_N")
    axs[3].plot(true_res['time'], res['pos_E'] - true_res['pos_E'], label="pos_E")
    axs[3].legend()

    fig.savefig(src + '/' + prefix + 'deviation.jpg')
    plt.close()


def show_trajectory(res, prefix, src):
    # Estimated trajectory
    plt.rcParams.update({'font.size': 22})
    plt.figure(figsize=(10, 10))
    plt.scatter(res['pos_E'], res['pos_N'], label='estimated trajectory', marker='.', alpha=0.8, linewidths=0.1)
    plt.xlabel('E axis [m]')
    plt.ylabel('N axis [m]')
    plt.title(prefix + 'Trajectory')
    plt.tight_layout()
    plt.savefig(src + '/' + prefix + 'trajectory.jpg')
    plt.savefig(src + '/' + prefix + 'trajectory.svg')

    plt.figure(figsize=(10, 4))
    plt.scatter(res['pos_E'], res['pos_N'], label='estimated trajectory', marker='.', alpha=0.8, linewidths=0.1)
    plt.xlabel('E axis [m]')
    plt.ylabel('N axis [m]')
    plt.ylim([480, 520])
    plt.xlim([-100, 100])
    plt.tight_layout()
    plt.title(prefix + 'Trajectory - Zoom')
    plt.savefig(src + '/' + prefix + 'trajectory_zoom.jpg')
    plt.savefig(src + '/' + prefix + 'trajectory_zoom.svg')
    plt.close()


def show_error(true_res, res, prefix, src):
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))
    # Azimuth
    axs[0].plot(true_res['time'], np.abs(true_res['theta'] - res['orientation']))
    axs[0].set_ylabel('Azimuth [rad]')
    # Velocity
    axs[1].plot(true_res['time'], np.abs(true_res['vel_E'] - res['vel_E']), label="vel_E")
    axs[1].plot(true_res['time'], np.abs(true_res['vel_N'] - res['vel_N']), label="vel_N")
    axs[1].set_ylabel('velocity [m/s]')
    axs[1].legend()
    # Position
    axs[2].plot(true_res['time'], np.abs(true_res['pos_E'] - res['pos_E']), label='pos_E')
    axs[2].plot(true_res['time'], np.abs(true_res['pos_N'] - res['pos_N']), label='pos_N')
    axs[2].set_ylabel('Position [m]')
    axs[2].set_xlabel('steps [-]')
    axs[2].legend()

    plt.savefig(src + '/' + prefix + 'errors.jpg')
    plt.savefig(src + '/' + prefix + 'errors.svg')
    plt.close()

    # Print max error:
    print("MAX ERROR - " + prefix)
    print(f"\t- maximum error on Azimuth is {np.max(np.abs(true_res['theta'] - res['orientation']))}")
    print(f"\t- maximum error on Velocity")
    print(f"\t\t V_E : {np.max((np.abs(true_res['vel_E'] - res['vel_E'])))}")
    print(f"\t\t V_N : {np.max((np.abs(true_res['vel_N'] - res['vel_N'])))}")
    print(f"\t- maximum error on Position")
    print(f"\t\t P_E : {np.max((np.abs(true_res['pos_E'] - res['pos_E'])))}")
    print(f"\t\t P_N : {np.max((np.abs(true_res['pos_N'] - res['pos_N'])))}")

