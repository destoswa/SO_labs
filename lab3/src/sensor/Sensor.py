from lab3.src.sensor import Measurements as Ms


class Sensor:
    """
    Represents a sensor that measures physical quantities.

    Args:
        sensor_id (str): The unique identifier of the sensor.
        time_fct (callable): A function that computes the time values.
        nominal_fct (callable): A function that computes the nominal measurements.
        noise_models (list, optional): A list of noise models applied to the measurements.
                                        Defaults to None.

    Attributes:
        sensor_id (str): The unique identifier of the sensor.
        time_fct (callable): A function that computes the time values.
        nominal_fct (callable): A function that computes the nominal measurements.
        noise_models (list): A list of noise models applied to the measurements.

    Methods:
        measure(freq): Generates a measurement from the sensor.

    """

    def __init__(self, sensor_id, time_fct, nominal_fct, noise_models=None):
        self.sensor_id = sensor_id
        self.time_fct = time_fct
        self.nominal_fct = nominal_fct
        self.noise_models = [] if noise_models is None else noise_models

    def measure(self, freq):
        """
        Generates a measurement from the sensor.

        Args:
            freq (float): The frequency of measurement.

        Returns:
            Measurement: An object representing the measurement.

        """
        time = self.time_fct(freq=freq)
        nominal = self.nominal_fct(freq=freq)
        noisy = nominal.copy()
        for noise_model in self.noise_models:
            noise = noise_model.generate_noise(size=len(nominal), freq=freq)
            noisy += noise
        measurement = Ms.Measurement(sensor=self, freq=freq, time=time, nominal=nominal, noisy=noisy)
        return measurement


class SensorCollection:
    """
    Represents a synchronized collection of sensors.

    Args:
        sensors (list): A list of Sensor objects.

    Attributes:
        sensors (list): A list of Sensor objects.

    Methods:
        measure(freq): Generates measurements from all sensors in the collection.

    """

    def __init__(self, sensors):
        self.sensors = sensors

    def measure(self, freq):
        """
        Generates measurements from all sensors in the collection.

        Args:
            freq (float): The frequency of measurement.

        Returns:
            MeasurementCollection: An object representing the collection of measurements.

        """
        measurements = {}
        for sensor in self.sensors:
            measurements[sensor.sensor_id] = sensor.measure(freq)
        measurement_collection = Ms.MeasurementCollection(measurements=measurements)
        return measurement_collection
