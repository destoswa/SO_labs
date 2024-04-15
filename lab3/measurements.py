import param as pm


class Measurement:
	def __init__(self, sensor, freq, nominal, noisy):
		self.sensor = sensor
		self.freq = freq
		self.nominal = nominal
		self.noisy = noisy
		self.time = pm.get_time_serie(freq)

	def __getitem__(self, item):
		return self.noisy[item]

	def __copy__(self):
		meas_copy = Measurement(
			sensor=self.sensor,
			freq=self.freq,
			nominal=self.nominal.copy(),
			noisy=self.noisy.copy()
		)
		return meas_copy


class MeasurementCollection:
	"""
	Synchronic measurements
	"""

	def __init__(self, measurements):
		self.measurements = measurements
		_, measurement_0 = list(measurements.items())[0]
		self.time = measurement_0.time.copy()  # Should be the same for all measurements
		self.freq = measurement_0.freq         # Should be the same for all measurements

	def __getitem__(self, sensor_id):
		return self.measurements[sensor_id].noisy.copy()

	def get_nominal(self, sensor_id):
		return self.measurements[sensor_id].nominal.copy()

	def __copy__(self):
		measurements_copy = {}
		for sensor_id, measurement in self.measurements.items():
			measurements_copy[sensor_id] = measurement.__copy__()
		return MeasurementCollection(measurements_copy)

	def filter_noise(self, ids=None):
		ids = self.measurements.keys() if ids is None else ids
		new_meas_collection = self.__copy__()
		for sensor_id, measurement in new_meas_collection.measurements.items():
			if sensor_id in ids:
				nominal = new_meas_collection.measurements[id].nominal.copy()
				new_meas_collection.measurements[id].noisy = nominal
		return new_meas_collection

	def isolate_noise(self, sensor_id):
		ids = list(self.measurements.keys())
		ids.remove(sensor_id)
		isolated_noise_meas_collection = self.filter_noise(ids=ids)
		return isolated_noise_meas_collection
