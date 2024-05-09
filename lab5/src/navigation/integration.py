import numpy as np

# TODO : Check if function should be taking time as arg instead of azimuth
# TODO : Should the symbolic integration go into the nominal_fct ?
# TODO : Should the numerical integration go into a util module ?


"""
Numerical integration
"""


def integrate_numerically(dt, signal, initial_condition, order=1):
    """
    Integrate a signal numerically.

    Args:
        dt: Time step.
        signal: Input signal to integrate.
        initial_condition: Initial condition.
        order: Order of integration (1 or 2). Defaults to 1.

    Returns:
        Integrated signal.
    """
    assert (order in [1, 2])
    integrated_signal = np.zeros_like(signal)
    integrated_signal[0] = initial_condition  # The first value must be the initial condition

    if order == 1:
        tmp = initial_condition + np.cumsum(signal * dt)
        integrated_signal[1:] = tmp[:-1]  # We cut off the last value, to keep the same length as the original signal
    elif order == 2:
        integrated_signal[1:] = initial_condition + np.cumsum(0.5 * (signal[1:] + signal[:-1]) * dt)
    return integrated_signal


"""
Symbolic integration and evaluation
"""


def evaluate_integration(int_function, initial_condition, acc_x, acc_y, gyro, azimuth, azimuth_0):
    """
    Apply integral evaluation from azimuth_0 to azimuth
    """
    result = (
            initial_condition
            + int_function(acc_x, acc_y, gyro, azimuth)
            - int_function(acc_x, acc_y, gyro, azimuth_0)
    )
    return result


def get_v_n(acc_x, acc_y, gyro, azimuth):
    return acc_x * np.sin(azimuth) / gyro + acc_y * np.cos(azimuth) / gyro


def get_v_e(acc_x, acc_y, gyro, azimuth):
    return - acc_x * np.cos(azimuth) / gyro + acc_y * np.sin(azimuth) / gyro


def get_p_n(acc_x, acc_y, gyro, azimuth):
    return (- acc_x * np.cos(azimuth) + acc_y * np.sin(azimuth)) / gyro ** 2


def get_p_e(acc_x, acc_y, gyro, azimuth):
    return (- acc_x * np.sin(azimuth) - acc_y * np.cos(azimuth)) / gyro ** 2
