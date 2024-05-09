import numpy as np
from lab3.src.reference import constants as cst


def get_time_serie(freq):
    dt = 1 / freq
    time = np.arange(0, cst.SIMULATION_TIME + dt, dt)
    return time


# Nominal measurements
def get_nominal_acc_x(freq):
    time = get_time_serie(freq)
    nominal_acc_x = np.full_like(a=time, fill_value=0)
    return nominal_acc_x


def get_nominal_acc_y(freq):
    time = get_time_serie(freq)
    nominal_acc_x = np.full_like(a=time, fill_value=cst.OMEGA ** 2 * cst.RADIUS)
    return nominal_acc_x


def get_nominal_gyro(freq):
    time = get_time_serie(freq)
    nominal_gyro = np.full_like(a=time, fill_value=cst.OMEGA)
    return nominal_gyro
