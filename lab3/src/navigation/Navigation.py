from lab3.src.reference import constants as cst
from lab3.src.navigation import Trajectory as Tr, TrueTrajectory as TTr, navigation_plots as nvp


class Navigation:
    def __init__(self, nav_id, initial_conditions, measurements, reference=False):
        """
        Initialize a navigation object.

        Args:
            nav_id (str): Identifier for the navigation instance.
            initial_conditions (dict): Initial conditions for the navigation.
            measurements: Measurement data for navigation.
            reference (bool, optional): Whether the navigation is a reference instance. Defaults to False.
        """
        self.nav_id = nav_id
        self.initial_conditions = initial_conditions
        self.measurements = measurements
        self.reference = reference
        self.true_trajectory = TTr.TrueTrajectory(
            initial_conditions=initial_conditions, measurements=measurements.filter_noise())
        self.true_trajectory.compute_trajectory()
        self.trajectory = self.true_trajectory.__copy__() if reference else None

    def compute_trajectory(self, order):
        """
        Compute the trajectory for the navigation.

        Args:
            order: Order of the trajectory computation.
        """
        if not self.reference:
            self.trajectory = Tr.Trajectory(initial_conditions=self.initial_conditions, measurements=self.measurements)
            self.trajectory.compute_trajectory(order=order)

    def plot_trajectory(self, result_dir=cst.PLOTS_DIR, include_acc=False, verbose=False):
        """
        Create plots for trajectory and associated data.

        Args:
            result_dir (str, optional): Directory to save the plots. Defaults to cst.PLOTS_DIR.
            include_acc (bool, optional): Whether to include acceleration in the plots. Defaults to False.
            verbose (bool, optional): Whether to print verbose output. Defaults to False.
        """
        nvp.create_folders(prefix=self.nav_id, result_dir=result_dir)
        nvp.show_error(result_dir=result_dir, navigation=self, add_acc=include_acc, verbose=verbose)
        nvp.show_evolution(result_dir=result_dir, navigation=self, add_acc=include_acc)
        nvp.show_trajectory(result_dir=result_dir, navigation=self)
