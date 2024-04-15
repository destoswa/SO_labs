import numpy as np
import scipy


class Bias:
	def __init__(self, bias_sd):
		self.noise_name = 'bias'
		self.bias_sd = bias_sd

	def generate_noise(self, size, freq=None):
		bias = np.random.normal(scale=self.bias_sd)
		bias_noise = np.ones(shape=size)*bias
		return bias_noise


class WhiteNoise:
	def __init__(self, psd_wn):
		self.noise_name = 'white noise'
		self.psd_wn = psd_wn

	def generate_noise(self, size, freq):
		sd = self.psd_wn * np.sqrt(freq)
		wn_noise = np.random.normal(size=size, scale=sd)
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
		dt = 1/freq
		sd_gm = self.psd_gm/np.sqrt(freq)
		sd_wn = np.sqrt(sd_gm*(1-np.exp(-2*self.beta*dt)))
		psd_wn = sd_wn / np.sqrt(freq)
		wn_noise = WhiteNoise(psd_wn=psd_wn).generate_noise(size=size, freq=freq)
		gm_noise = np.zeros(size)
		beta = self.beta
		dt = 1 / freq
		for i in range(1, size):
			gm_noise[i] = gm_noise[i - 1] * np.exp(-beta * dt) + wn_noise[i - 1]
		return gm_noise
