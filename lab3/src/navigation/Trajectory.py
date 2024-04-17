import numpy as np

from lab3.src.navigation import integration as itg


class Trajectory:
    def __init__(self, initial_conditions, measurements):
        """
        Initialize a trajectory object.

        Args:
            initial_conditions (dict): Initial conditions for the trajectory.
            measurements: Measurement data for the trajectory.
        """
        self.initial_conditions = initial_conditions
        self.measurements = measurements

        # Initialize empty trajectory states
        self.time = self.measurements.time
        self.theta = None
        self.azimuth = None
        self.acc_E = None
        self.acc_N = None
        self.v_E = None
        self.v_N = None
        self.p_E = None
        self.p_N = None

    def __copy__(self):
        new_traj = Trajectory(initial_conditions=self.initial_conditions.copy(), measurements=self.measurements.__copy__())
        new_traj.theta = self.theta.copy()
        new_traj.azimuth = self.azimuth.copy()
        new_traj.acc_E = self.acc_E.copy()
        new_traj.acc_N = self.acc_N.copy()
        new_traj.v_E = self.v_E.copy()
        new_traj.v_N = self.v_N.copy()
        new_traj.p_E = self.p_E.copy()
        new_traj.p_N = self.p_N.copy()
        return new_traj

    def compute_trajectory(self, order):
        """
        Compute the trajectory.

        Args:
            order: Order of the trajectory computation.
        """
        # Shorter notation for measurements
        dt = 1 / self.measurements.freq
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

        # Compute trajectory states with integration
        theta = itg.integrate_numerically(dt=dt, signal=gyro, initial_condition=theta_0)
        azimuth = azimuth_0 + theta
        acc_e = - acc_y * np.sin(theta) + acc_x * np.cos(theta)
        acc_n = - acc_y * np.cos(theta) - acc_x * np.sin(theta)
        v_n = itg.integrate_numerically(dt=dt, signal=acc_n, initial_condition=v_n_0, order=order)
        v_e = itg.integrate_numerically(dt=dt, signal=acc_e, initial_condition=v_e_0, order=order)
        p_n = itg.integrate_numerically(dt=dt, signal=v_n, initial_condition=p_n_0, order=order)
        p_e = itg.integrate_numerically(dt=dt, signal=v_e, initial_condition=p_e_0, order=order)

        # Save trajectory states
        self.theta, self.azimuth = theta, azimuth
        self.acc_E, self.acc_N = acc_e, acc_n
        self.v_E, self.v_N = v_e, v_n
        self.p_E, self.p_N = p_e, p_n

