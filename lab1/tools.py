import numpy as np
from scipy import signal
from allan_variance import allan_variance, params_from_avar


def white_noise(n_series, length, mean=0, std=1):
    return mean + std * np.random.randn(n_series, length)


def random_walk(WN):
    return np.cumsum(WN, axis=1)


def gauss_markov(WN, tau, dt=1):
    length = WN.shape[1]
    beta = 1/tau
    GM = np.zeros_like(WN)  #   Assume GM[0] = 0
    for i in range(1, length):
        GM[:, i] = GM[:, i-1] * np.exp(-beta*dt) + WN[:, i-1]
    return GM


def AC(X):
    return np.correlate(X, X, mode='full')


def PSD(X, dt=1):
    return signal.welch(X, fs=dt, return_onesided=False, scaling='spectrum')


def AVar(X, dt=1):
    tau, av = allan_variance(X, dt, input_type='increment')
    return tau, av


