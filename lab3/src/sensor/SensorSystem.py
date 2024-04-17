from lab3.src.sensor import MeasurementCollection as MsC


class SensorSystem:
    """
    Represents a synchronized collection of sensors as a system of sensor.

    Args:
        sensors (list): A list of Sensor objects.

    Attributes:
        sensors (list): A list of Sensor objects.

    Methods:
        measure(freq): Generates measurements from all sensors in the system.

    """

    def __init__(self, sensors):
        self.sensors = sensors

    def measure(self, freq):
        """
        Generates measurements from all sensors in the system.

        Args:
            freq (float): The frequency of measurement.

        Returns:
            MeasurementCollection.py: An object representing the collection of measurements.

        """
        measurements = {}
        for sensor in self.sensors:
            measurements[sensor.sensor_id] = sensor.measure(freq)
        measurement_collection = MsC.MeasurementCollection(measurements=measurements)
        return measurement_collection
