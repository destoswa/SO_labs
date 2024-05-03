import numpy as np

# Reference signal
SIMULATION_TIME = 200
RADIUS = 25  # m
OMEGA = np.pi/100  # rad/s
DELTA_TIME = 1  #s

ALPHA_0 = 0  # rad, Orientation with vertical axis in clockwise direction
X_0 = 0
Y_0 = RADIUS

x_ref = lambda t: RADIUS * np.cos(ALPHA_0 + OMEGA*t)
y_ref = lambda t: RADIUS * np.sin(ALPHA_0 + OMEGA*t)



