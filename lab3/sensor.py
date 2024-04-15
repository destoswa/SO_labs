import measurements as ms


class Sensor:
	"""
	A sensor is defined by its noise models (bias, random_walk, ...) lets call them the sensor specs

	"""

	def __init__(self, sensor_id, nominal_fct, noise_models=None):
		self.sensor_id = sensor_id
		self.nominal_fct = nominal_fct
		self.noise_models = [] if noise_models is None else noise_models

	def measure(self, freq):
		nominal = self.nominal_fct(freq=freq)
		noisy = nominal.copy()
		for noise_model in self.noise_models:
			noise = noise_model.generate_noise(size=len(nominal), freq=freq)
			noisy += noise
		measurement = ms.Measurement(sensor=self, freq=freq, nominal=nominal, noisy=noisy)
		return measurement


class SensorCollection:
	"""
	Synchronized collection of sensor
	"""
	def __init__(self, sensors):
		self.sensors = sensors

	def measure(self, freq):
		measurements = {}
		for sensor in self.sensors:
			measurements[sensor.sensor_id] = sensor.measure(freq)
		measurement_collection = ms.MeasurementCollection(measurements=measurements)
		return measurement_collection
