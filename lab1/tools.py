import numpy as np
from scipy import signal

from allan_variance import allan_variance


def white_noise(n_series, length, mean=0, std=1):
    return mean + std * np.random.randn(n_series, length)


def random_walk(wn):
    return np.cumsum(wn, axis=1)


def gauss_markov(wn, tau, dt=1):
    length = wn.shape[1]
    beta = 1/tau
    gm = np.zeros_like(wn)  # Assume gm[0] = 0
    for i in range(1, length):
        gm[:, i] = gm[:, i-1] * np.exp(-beta*dt) + wn[:, i - 1]
    return gm


def autocorr(x):
    return np.correlate(x, x, mode='full')


def psd(x, dt=1):
    return signal.welch(x, fs=dt, return_onesided=False, scaling='spectrum')


def allan_var(x, dt=1):
    tau, av = allan_variance(x, dt, input_type='increment')
    return tau, av
