import numpy as np

"""
Define all params of Lab 2
"""

# Simulation parameter
FREQ = 10 # Hz
DELTA_T = 1/FREQ # s
OMEGA = np.pi / 100
SIMULATION_TIME = 200

# Rotation of frame b around frame l
RADIUS = 500 # m
THETA_0 = 0 # Angle with north axis
V_0_NORTH = 0
V_0_EAST = OMEGA*RADIUS
P_0_NORTH = RADIUS
P_0_EAST = 0

# Body
AZIMUTH_0 = np.pi/2 # 90° Clockwise
