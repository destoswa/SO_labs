import numpy as np


class Measurement:
    """
    Represents a single measurement from a sensor.

    Args:
        sensor: The sensor object that generated the measurement.
        freq (float): The frequency of the measurement.
        time (ndarray): Time values of the measurement.
        nominal (ndarray): Nominal measurement values.
        noisy (ndarray): Noisy measurement values.

    Methods:
        __getitem__(item): Returns a subset of noisy measurement values.
        __copy__(): Creates a copy of the measurement object.

    """

    def __init__(self, sensor, freq, time, nominal, noisy):
        self.sensor = sensor
        self.freq = freq
        self.time = time
        self.nominal = nominal
        self.noisy = noisy

    def __getitem__(self, item):
        """
        Returns a subset of noisy measurement values.

        Args:
            item: Index or slice object.

        Returns:
            ndarray: Subset of noisy measurement values.

        """
        return self.noisy[item]

    def __copy__(self):
        """
        Creates a copy of the measurement object.

        Returns:
            Measurement: A copy of the measurement object.

        """
        meas_copy = Measurement(
            sensor=self.sensor,
            freq=self.freq,
            time=self.time.copy(),
            nominal=self.nominal.copy(),
            noisy=self.noisy.copy()
        )
        return meas_copy

    def remove_noise(self, inplace=False):
        """
        Create a copy of the measurement, removes the noise
        """
        if inplace:
            self.noisy = self.nominal.copy()
            return self
        else:
            noiseless_meas = self.__copy__()
            noiseless_meas.noisy = noiseless_meas.nominal.copy()
            return noiseless_meas

    def is_noisy(self):
        return not np.all(self.noisy == self.nominal)