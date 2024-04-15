import numpy as np


class Bias:
	def __init__(self, bias_sd):
		self.noise_name = 'bias'
		self.bias_sd = bias_sd

	def generate_noise(self, size, freq=None):
		bias_noise = np.random.normal(size=size, scale=self.bias_sd)
		return bias_noise


class WhiteNoise:
	def __init__(self, psd_wn):
		self.noise_name = 'white noise'
		self.psd_wn = psd_wn

	def generate_noise(self, size, freq):
		sd = self.psd_wn * np.sqrt(freq)
		wn_noise = sd * np.random.randn(size)
		return wn_noise


class RandomWalk:
	def __init__(self, psd_wn):
		self.noise_name = 'random walk'
		self.wn = WhiteNoise(psd_wn=psd_wn)

	def generate_noise(self, size, freq):
		wn_noise = self.wn.generate_noise(size, freq)
		rw_noise = np.cumsum(wn_noise)
		return rw_noise


class GaussMarkov:
	def __init__(self, psd_gm, tau):
		self.noise_name = 'random walk'
		self.psd_gm = psd_gm
		self.tau = tau
		self.beta = 1 / tau

	def generate_noise(self, size, freq):
		sd_wn = self.psd_gm * self.beta / 2  # TODO Check
		psd_wn = sd_wn / np.sqrt(freq)  # TODO Check
		wn_noise = WhiteNoise(psd_wn=psd_wn).generate_noise(size=size, freq=freq)
		gm_noise = np.zeros(size)
		beta = 1 / self.tau
		dt = 1 / freq
		for i in range(1, size):
			gm_noise[i] = gm_noise[i - 1] * np.exp(-beta * dt) + wn_noise[i - 1]
		return gm_noise
