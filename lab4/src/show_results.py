import matplotlib.pyplot as plt
import numpy as np
from .constants import deg


def print_stats(gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z):

    print("\t+--------------+-------------+----------------+----------------+")
    print("\t| Gyro signals | mean        | sd             | units          |")
    print("\t+--------------+-------------+----------------+----------------+")
    print(
        f"\t| gyro_x       |  {deg(gyro_x.mean()) * 1000:.5}     | {deg(np.std(gyro_x)) * 1000:.5}          | [mdeg/s]       |")
    print(
        f"\t| gyro_y       | {deg(gyro_y.mean()) * 1000:.5}     | {deg(np.std(gyro_x)) * 1000:.5}          | [mdeg/s]       |")
    print(
        f"\t| gyro_z       | {deg(gyro_z.mean()) * 1000:.5}     | {deg(np.std(gyro_x)) * 1000:.5}          | [mdeg/s]       |")
    print("\t+--------------+-------------+----------------+----------------+")
    print("\n")
    print("\t+--------------+-------------+----------------+----------------+")
    print("\t| Acc signals  | mean        | sd             | units          |")
    print("\t+--------------+-------------+----------------+----------------+")
    print(f"\t| acc_x        | {acc_x.mean():.5}    | {np.std(acc_x):.5}      | [m/s²]         |")
    print(f"\t| acc_y        | {acc_y.mean():.5}    | {np.std(acc_y):.5}      | [m/s²]         |")
    print(f"\t| acc_z        | {acc_z.mean():.5}     | {np.std(acc_z):.5}      | [m/s²]         |")
    print("\t+--------------+-------------+----------------+----------------+")
    print("\n")


def plot_IMU(time, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z):
    # Plot measurements
    fig, axs = plt.subplots(3, 2, figsize=(10, 4), sharex=True)
    time_p = time - time.iloc[0]

    axs[0, 0].plot(time_p, gyro_x, label='gyro_x')
    axs[1, 0].plot(time_p, gyro_y, label='gyro_y')
    axs[2, 0].plot(time_p, gyro_z, label='gyro_z')

    axs[0, 1].plot(time_p, acc_x, label='acc_x')
    axs[1, 1].plot(time_p, acc_y, label='acc_y')
    axs[2, 1].plot(time_p, acc_z, label='acc_z')

    for i in range(3):
        for j in range(2):
            axs[i, j].legend(loc="upper right")
    fig.savefig("result/IMU.jpg")


def plot_IMU_mean_dev(time, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z):
    # Mean measurements
    gyro_x_m = np.mean(gyro_x)
    gyro_y_m = np.mean(gyro_y)
    gyro_z_m = np.mean(gyro_z)
    acc_x_m = np.mean(acc_x)
    acc_y_m = np.mean(acc_y)
    acc_z_m = np.mean(acc_z)

    # Plot deviation from noise
    fig, axs = plt.subplots(3, 2, figsize=(10, 4), sharex=True)
    time_p = time - time.iloc[0]

    axs[0, 0].plot(time_p, gyro_x - gyro_x_m, label='gyro_x')
    axs[1, 0].plot(time_p, gyro_y - gyro_y_m, label='gyro_y')
    axs[2, 0].plot(time_p, gyro_z - gyro_z_m, label='gyro_z')

    axs[0, 1].plot(time_p, acc_x - acc_x_m, label='acc_x')
    axs[1, 1].plot(time_p, acc_y - acc_y_m, label='acc_y')
    axs[2, 1].plot(time_p, acc_z - acc_z_m, label='acc_z')

    for i in range(3):
        for j in range(2):
            axs[i, j].legend(loc="upper right")
    fig.savefig("result/IMU_deviations.jpg")


def plot_IMU_mean_rel_dev(time, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z):
    # Mean measurements
    gyro_x_m = np.mean(gyro_x)
    gyro_y_m = np.mean(gyro_y)
    gyro_z_m = np.mean(gyro_z)
    acc_x_m = np.mean(acc_x)
    acc_y_m = np.mean(acc_y)
    acc_z_m = np.mean(acc_z)

    # Plot deviation from noise
    fig, axs = plt.subplots(3, 2, figsize=(10, 4), sharex=True)
    time_p = time - time.iloc[0]

    axs[0, 0].plot(time_p, gyro_x/gyro_x_m - 1, label='gyro_x')
    axs[1, 0].plot(time_p, gyro_y/gyro_y_m - 1, label='gyro_y')
    axs[2, 0].plot(time_p, gyro_z/gyro_z_m - 1, label='gyro_z')

    axs[0, 1].plot(time_p, acc_x/acc_x_m - 1, label='acc_x')
    axs[1, 1].plot(time_p, acc_y/acc_y_m - 1, label='acc_y')
    axs[2, 1].plot(time_p, acc_z/acc_z_m - 1, label='acc_z')

    for i in range(3):
        for j in range(2):
            axs[i, j].legend(loc="upper right")
    fig.savefig("result/IMU_rel_deviations.jpg")