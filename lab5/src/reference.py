import numpy as np

# Simulation parameters
NUMBER_REALIZATION = 5
SIMULATION_TIME = 200
RADIUS = 25  # m
OMEGA = np.pi / 100  # rad/s
FREQ = 100
GPS_FREQ = 1

# Initial conditions
ALPHA_0 = 0  # rad, Orientation with vertical axis in clockwise direction
X_0 = 0  # m
Y_0 = RADIUS  # m
V_X_0 = OMEGA*RADIUS
V_Y_0 = 0


# reference state

def x_ref(t):
    return RADIUS * np.sin(ALPHA_0 + OMEGA * t)  # X : horizontal axis


def y_ref(t):
    return RADIUS * np.cos(ALPHA_0 + OMEGA * t)  # Y : vertical axis


def vx_ref(t):
    v = OMEGA * RADIUS
    return v * np.cos(ALPHA_0 + OMEGA * t)


def vy_ref(t):
    v = OMEGA * RADIUS
    return v * np.sin(ALPHA_0 + OMEGA * t)


def generate_time_serie(freq=None):
    if freq is None:
        freq = FREQ
    time = np.arange(start=0, step=1 / FREQ, stop=SIMULATION_TIME)
    return time


def generate_ref_states(freq=None):
    time = generate_time_serie(freq)
    x = x_ref(time)
    y = y_ref(time)
    v_x = vx_ref(time)
    v_y = vy_ref(time)
    states = np.array([
        x,
        y,
        v_x,
        v_y
    ]).T
    return states
