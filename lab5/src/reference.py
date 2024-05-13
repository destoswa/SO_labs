import numpy as np

# Simulation parameters
NUMBER_REALIZATION = 5
SIMULATION_TIME = 200
RADIUS = 25  # m
OMEGA = np.pi / 100  # rad/s
FREQ = 1
DT = 1/FREQ
GPS_FREQ = 1

# Initial conditions
THETA_0 = 0  # rad, Orientation with vertical axis in clockwise direction


def generate_time_serie(freq=FREQ):
    time = np.arange(start=0, step=1 / freq, stop=SIMULATION_TIME)
    return time


def generate_ref_states(freq=FREQ):
    time = generate_time_serie(freq)
    theta = THETA_0 + OMEGA * time
    x = RADIUS * np.sin(theta)
    y = RADIUS * np.cos(theta)

    v = OMEGA * RADIUS
    vx = v * np.cos(theta)
    vy = v * np.sin(theta)

    """    
    a = OMEGA**2 * RADIUS
    ax = - a * np.sin(theta)
    ay = - a * np.cos(theta)"""

    states = np.array([x, y, vx, vy]).T
    return states


if __name__ == "__main__":
    ref_states = generate_ref_states()
    print(ref_states[0:2])
