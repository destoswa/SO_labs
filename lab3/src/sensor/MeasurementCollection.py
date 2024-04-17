class MeasurementCollection:
    """
    Represents a collection of synchronized measurements from multiple sensors.

    Args:
        measurements (dict): Dictionary of sensor IDs mapped to Measurement objects.

    Methods:
        __getitem__(sensor_id): Returns noisy measurements for a specific sensor.
        get_nominal(sensor_id): Returns reference measurements for a specific sensor.
        __copy__(): Creates a copy of the measurement collection.
        filter_noise(ids): Removes noise from measurements for specified sensor IDs.
        isolate_noise(sensor_id): Removes noise from measurements for a specific sensor.

    """

    def __init__(self, measurements):
        self.measurements = measurements
        _, measurement_0 = list(measurements.items())[0]
        self.time = measurement_0.time.copy()  # Should be the same for all measurements
        self.freq = measurement_0.freq         # Should be the same for all measurements

    def __getitem__(self, sensor_id):
        """
        Returns noisy measurements for a specific sensor.

        Args:
            sensor_id: ID of the sensor.

        Returns:
            ndarray: Noisy measurements for the specified sensor.

        """
        return self.measurements[sensor_id].noisy.copy()

    def get_nominal(self, sensor_id):
        """
        Returns reference measurements for a specific sensor.

        Args:
            sensor_id: ID of the sensor.

        Returns:
            ndarray: Nominal measurements for the specified sensor.

        """
        return self.measurements[sensor_id].nominal.copy()

    def __copy__(self):
        """
        Creates a copy of the measurement collection.

        Returns:
            MeasurementCollection: A copy of the measurement collection.

        """
        measurements_copy = {}
        for sensor_id, measurement in self.measurements.items():
            measurements_copy[sensor_id] = measurement.__copy__()
        return MeasurementCollection(measurements_copy)

    def filter_noise(self, ids=None):
        """
        Removes noise from measurements for specified sensor IDs.

        Args:
            ids (list, optional): List of sensor IDs. If None, noise is removed from all sensors. Defaults to None.

        Returns:
            MeasurementCollection: A new MeasurementCollection with noise removed.

        """
        ids = self.measurements.keys() if ids is None else ids
        new_meas_collection = self.__copy__()
        for sensor_id, measurement in new_meas_collection.measurements.items():
            if sensor_id in ids:
                measurement.remove_noise(inplace=True)
        return new_meas_collection

    def isolate_noise(self, sensor_id):
        """
        Keeps the noisy measurements for a specific sensor.

        Args:
            sensor_id: ID of the sensor to isolate noise from.

        Returns: MeasurementCollection: A new MeasurementCollection with noise removed for all sensors except
        specified sensor.

        """
        ids = list(self.measurements.keys())
        ids.remove(sensor_id)
        isolated_noise_meas_collection = self.filter_noise(ids=ids)
        return isolated_noise_meas_collection
