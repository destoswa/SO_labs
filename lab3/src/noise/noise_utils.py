import numpy as np
from scipy import signal
from lab3.src.noise import allan_variance as av


def bias(size, bias_sd):
    bias_ = np.random.normal(scale=bias_sd)
    print("Bias : " + str(bias))
    bias_noise = np.ones(shape=size) * bias_
    return bias_noise


def white_noise(size, sd):
    wn = sd * np.random.randn(size)
    return wn


def random_walk(wn):
    rw = np.cumsum(wn, axis=1)
    return rw


def sd_gm_to_sd_wn(sd_gm, beta, dt):
    sd_wn = np.sqrt(sd_gm ** 2 * (1 - np.exp(-2 * beta * dt)))
    return sd_wn


def gauss_markov(wn, beta, dt=1):
    size = len(wn)
    gm = np.zeros_like(wn)  # Assume gm[0] = 0
    for i in range(1, size):
        gm[i] = gm[i - 1] * np.exp(-beta * dt) + wn[ i - 1]
    return gm


def auto_corr(x):
    ac = np.correlate(x, x, mode='full')
    # ac = (ac - np.min(ac)) / (np.max(ac) - np.min(ac))
    return ac


def psd(x, dt=1):
    return signal.welch(x, fs=dt, return_onesided=False, scaling='density')


def allan_var(x, dt=1):
    tau, a_v = av.allan_variance(x, dt, input_type='increment')
    return tau, av


def find_gm_tau_from_ac(ac_gm):
    ac_gm = ac_gm[len(ac_gm) // 2:]  # Only use the positive x data
    peak = np.max(ac_gm)
    y_tau = peak / np.e
    dif = np.abs(ac_gm - y_tau)
    tau = dif.argmin()
    return tau


def save_noise(name, serie, folder='./data/realizations/'):
    np.savetxt(folder + name + '.txt', serie, delimiter=';', fmt='%.8f')
