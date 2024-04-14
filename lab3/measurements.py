import param
import numpy as np


class Measurements:
	def __init__(self, freq, noise_generators=None):
		# Time
		self.freq = freq
		self.dt = 1 / freq
		self.time = np.arange(0, param.SIMULATION_TIME + self.dt, self.dt)
		self.noise_generators = noise_generators

		# Nominal values from sensors (Unknown, should not be accessed for integration)
		self.nominal_sensors = {
			'acc_x': np.full_like(a=self.time, fill_value=0),
			'acc_y': np.full_like(a=self.time, fill_value=param.OMEGA ** 2 * param.RADIUS),
			'gyro': np.full_like(a=self.time, fill_value=param.OMEGA)
		}
		self.sensors = self.nominal_sensors.copy()

		# Noisy values from sensors
		if self.is_noisy():
			for sensor, signal in self.sensors.items():
				if sensor in noise_generators.keys():
					self.sensors[sensor] = noise_generators[sensor].add_noises(signal=signal, freq=self.freq)

	def __len__(self):
		return len(self.time)

	def __getitem__(self, item):
		return self.sensors[item]

	def __copy__(self):
		new_measurements = Measurements(self.freq)
		new_measurements.noise_generators = self.noise_generators.copy()
		new_measurements.sensors = self.sensors.copy()
		return new_measurements

	def select_noisy_sensor(self, noisy_sensor):
		"""
		Create a copy of the measurements, with only one the measurements being noisy
		"""
		new_measurements = self.__copy__()
		new_measurements.sensors = self.nominal_sensors.copy()
		new_measurements.sensors[noisy_sensor] = self.sensors[noisy_sensor]
		return new_measurements

	def is_noisy(self):
		return self.noise_generators is not None
