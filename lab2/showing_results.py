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


def show_trajectory(res, prefix, src):
    # Estimated trajectory
    plt.figure(figsize=(10, 10))
    plt.scatter(res['pos_E'], res['pos_N'], label='estimated trajectory', alpha=0.8, marker=',', linewidths=0.1)
    plt.savefig(src + '/' + prefix + 'trajectory.jpg')
    plt.savefig(src + '/' + prefix + 'trajectory.svg')
