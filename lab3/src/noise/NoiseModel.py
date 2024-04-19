import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

from lab3.src.noise import noise_utils as nu


class NoiseModel(ABC):
    """
    Abstract base class for noise models.
    """

    def __init__(self, noise_name):
        self.noise_name = noise_name

    @abstractmethod
    def generate_noise(self, size, freq):
        """
        Generate noise.

        Args:
            size (int): Number of samples to generate.
            freq (float): Frequency of the signal.

        Returns:
            ndarray: Array of noise samples.
        """
        pass

    def plot_noise(self, size=100, freq=1, n_serie=1, path=None):
        x = range(size)
        for _ in range(n_serie):
            noise = self.generate_noise(size=size, freq=freq)
            plt.plot(x, noise)
        plt.title(self.noise_name)

        if path is not None:
            plt.savefig(path)
            plt.close()
        else:
            plt.show()


class Bias(NoiseModel):
    """
    Represents a bias noise model.
    """

    def __init__(self, bias_sd):
        super().__init__('bias')
        self.bias_sd = bias_sd

    def generate_noise(self, size, freq=None):
        bias_noise = nu.bias(size=size, bias_sd=self.bias_sd)
        # DEBUG print("Bias : " + str(bias_noise[0]))
        return bias_noise


class WhiteNoise(NoiseModel):
    """
    Represents a white noise model.
    """

    def __init__(self, psd_wn):
        super().__init__('white noise')
        self.psd_wn = psd_wn

    def generate_noise(self, size, freq):
        sd = self.psd_wn * np.sqrt(freq)
        wn_noise = nu.white_noise(size, sd)
        # DEBUG : print("White noise - SD : " + str(sd))
        return wn_noise


class RandomWalk(NoiseModel):
    """
    Represents a random walk noise model.
    """

    def __init__(self, psd_wn):
        super().__init__('random walk')
        self.wn = WhiteNoise(psd_wn=psd_wn)

    def generate_noise(self, size, freq):
        wn_noise = self.wn.generate_noise(size, freq)
        rw_noise = nu.random_walk(wn_noise)
        return rw_noise


class GaussMarkov(NoiseModel):
    """
    Represents a 1st order Gauss-Markov noise model.
    """

    def __init__(self, psd_gm, tau):
        super().__init__('Gauss-Markov')
        self.psd_gm = psd_gm
        self.tau = tau
        self.beta = 1/tau

    def generate_noise(self, size, freq):
        sd_gm = self.psd_gm * np.sqrt(freq)
        sd_wn = nu.sd_gm_to_sd_wn(sd_gm=sd_gm, beta=self.beta, dt=1/freq)
        psd_wn = sd_wn / np.sqrt(freq)
        wn_noise = WhiteNoise(psd_wn=psd_wn).generate_noise(size=size, freq=freq)
        gm_noise = nu.gauss_markov(wn=wn_noise, beta=self.beta, dt=1/freq)
        # DEBUG : print("Gauss markov - SD : " + str(sd_gm))
        return gm_noise


