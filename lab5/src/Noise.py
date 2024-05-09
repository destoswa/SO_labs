import numpy as np


class Noise():
    def __init__(self, freq, duration):
        self.freq = freq
        self.duration = duration
        self.signal = []

    def generate(self):
        return False

    def add_noise(self, signal):
        self.generate()
        return signal + self.signal


class Bias(Noise):
    def __init__(self, freq, duration, bias_sd):
        Noise.__init__(self, freq, duration)
        self.bias_sd = bias_sd
        self.generate()

    def generate(self):
        self.signal = bias(self.duration * self.freq, self.bias_sd)


class WhiteNoise(Noise):
    def __init__(self, freq, duration, sd):
        Noise.__init__(self, freq, duration)
        self.sd = sd
        self.generate()

    def generate(self):
        self.signal = white_noise(self.duration * self.freq, self.sd)


class RandomWalk(Noise):
    def __init__(self, freq, duration, sd):
        Noise.__init__(self, freq, duration)
        self.sd = sd
        self.generate()

    def generate(self):
        wn = white_noise(self.duration * self.freq, self.sd)
        self.signal = random_walk(wn)


class GaussMarkov(Noise):
    def __init__(self, freq, duration, sd_gm, tau):
        Noise.__init__(self, freq, duration)
        self.sd_gm = sd_gm
        self.tau = tau
        self.beta = 1 / tau
        self.generate()

    def generate(self):
        dt = 1 / self.freq
        sd_wn = np.sqrt(self.sd_gm ** 2 * (1 - np.exp(-2 * self.beta * dt)))
        wn = white_noise(self.duration * self.freq, sd_wn)
        self.signal = gauss_markov(wn=wn, beta=self.beta, dt=1 / self.freq)


# ==== Noise generation ====

def bias(size, bias_sd):
    bias_ = np.random.normal(scale=bias_sd)
    bias_noise = np.ones(shape=size) * bias_
    return bias_noise


def white_noise(size, sd):
    wn = sd * np.random.randn(size)
    return wn


def random_walk(wn):
    rw = np.cumsum(wn, axis=1)
    return rw


def gauss_markov(wn, beta, dt=1):
    size = len(wn)
    gm = np.zeros_like(wn)  # Assume gm[0] = 0
    for i in range(1, size):
        gm[i] = gm[i - 1] * np.exp(-beta * dt) + wn[i - 1]
    return gm
