import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import allantools


def white_noise(n_series, length, mean=0, std=1):
    return mean + std * np.random.randn(n_series, length)


def random_walk(n_series, length, mean=0, std=1):
    WN = white_noise(n_series, length, mean=mean, std=std)
    return np.cumsum(WN, axis=0)


def gauss_markov(n_series, length, tau, mean=0, std=1, dt=1):
    WN = white_noise(n_series, length, mean=mean, std=std)
    length = WN.shape[1]
    beta = 1/tau
    GM = np.zeros_like(WN)  #   Assume GM[0] = 0
    for i in range(1, length):
        GM[:, i] = GM[:, i-1] * np.exp(-beta*dt) + WN[:, i-1]
    return GM


def AC(X):
    return np.correlate(X, X, mode='full')


def PSD(X, dt=1):
    return signal.periodogram(X, dt, scaling='density', return_onesided=False)
    """(S, f) = plt.psd(X, Fs=dt, sides='twosided')
    return f, S"""


def AVar(X):
    a = allantools.Dataset(data=X)
    a.compute("mdev")
    return a


