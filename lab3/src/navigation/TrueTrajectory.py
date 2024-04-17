import numpy as np

from lab3.src.navigation import Trajectory as Tr, integration as itg


class TrueTrajectory(Tr.Trajectory):
    def compute_trajectory(self, order=None):
        """
        Compute the true trajectory.

        Args:
            order: Not used.
        """
        # Shorter notation for measurements
        time = self.measurements.time
        acc_x = self.measurements['acc_x']
        acc_y = self.measurements['acc_y']
        gyro = self.measurements['gyro']

        # Shorter notation for initial conditions
        theta_0 = self.initial_conditions['theta']
        azimuth_0 = self.initial_conditions['azimuth']
        v_n_0 = self.initial_conditions['v_N']
        v_e_0 = self.initial_conditions['v_E']
        p_n_0 = self.initial_conditions['p_N']
        p_e_0 = self.initial_conditions['p_E']

        # Compute reference trajectory states
        self.theta = theta_0 + time * gyro
        self.azimuth = azimuth_0 + self.theta
        self.acc_N = acc_x * np.cos(self.azimuth) - acc_y * np.sin(self.azimuth)
        self.acc_E = acc_x * np.sin(self.azimuth) + acc_y * np.cos(self.azimuth)
        self.v_N = itg.evaluate_integration(itg.get_v_n, v_n_0, acc_x, acc_y, gyro, self.azimuth, azimuth_0)
        self.v_E = itg.evaluate_integration(itg.get_v_e, v_e_0, acc_x, acc_y, gyro, self.azimuth, azimuth_0)
        self.p_N = itg.evaluate_integration(itg.get_p_n, p_n_0, acc_x, acc_y, gyro, self.azimuth, azimuth_0)
        self.p_E = itg.evaluate_integration(itg.get_p_e, p_e_0, acc_x, acc_y, gyro, self.azimuth, azimuth_0)