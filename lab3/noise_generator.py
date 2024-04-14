import numpy as np


class NoiseModel:
	"""
	A NoiseModel instance allows to generate a noise w.r.t to the noise characteristics (noise_specs) and add to signal
	"""

	def __init__(self, noise_type, noise_specs):
		self.noise_type = noise_type
		self.noise_specs = noise_specs

	def generate_and_add_to_signal(self, signal, freq):
		size = np.size(signal)

		if self.noise_type == 'B':
			bias = self.noise_specs['bias']
			noise = bias_noise(size, bias)
		elif self.noise_type == 'WN':
			sd_psd = self.noise_specs['sd_wn_psd']
			noise = white_noise(size, sd=sd_psd)
		elif self.noise_type == 'RW':
			sd_psd = self.noise_specs['sd_wn_psd']
			noise = random_walk(size, sd= sd_psd)
		elif self.noise_type == 'GM':
			sd_psd = self.noise_specs['sd_gm_psd']
			tau = self.noise_specs['tau']
			noise = gauss_markov(size=size, tau=tau, dt=1/freq, sd=sd_psd)
		else:
			print(f'This noise type is not implemented : {self.noise_type}')
			raise ValueError

		noisy_signal = signal + noise

		return noisy_signal


class NoiseGenerator:
	"""
	Acts as a collection of noises models to apply to a signal
	Example :
		Specify the noises specifics for
		 - White noise : sd_pds = 4
		 - Bias : bias_sd = 2

		Then the NoiseGenerator instantiate a NoiseModel per specified noise
		When adding the noises, each NoiseModel produce a noise and add it to the signal
	"""

	def __init__(self, noises_specs):
		self.noises_specs = noises_specs

	def add_noises(self, signal, freq):
		noisy_signal = signal.copy()
		for noise_type, noise_specs in self.noises_specs.items():
			noise_model = NoiseModel(noise_type=noise_type, noise_specs=noise_specs)
			noisy_signal = noise_model.generate_and_add_to_signal(signal=signal, freq=freq)
		return noisy_signal


def bias_noise(size, bias):
	return np.random.normal(size=size, scale=bias)


def white_noise(size, sd):
	return sd * np.random.randn(size)


def random_walk(size, sd):
	wn = white_noise(size, sd=sd)
	rw = np.cumsum(wn)
	return rw


def gauss_markov(size, tau, dt, sd):
	wn = white_noise(size, sd=sd)
	length = wn.shape[1]
	beta = 1 / tau
	gm = np.zeros_like(wn)  # Assume gm[0] = 0
	for i in range(1, length):
		gm[:, i] = gm[:, i - 1] * np.exp(-beta * dt) + wn[:, i - 1]
	return gm