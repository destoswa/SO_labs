import numpy as np

"""
Define all params of Lab 2
"""
LENGTH_UNIT = 'm'
TIME_UNIT = 's'
ANGLE_UNIT = 'rad'

# Simulation parameter
OMEGA = np.pi / 100
SIMULATION_TIME = 200

# Rotation of body around frame l
RADIUS = 500  # m
THETA_0 = 0  # Angle with north axis
V_0_NORTH = 0
V_0_EAST = OMEGA * RADIUS
P_0_NORTH = RADIUS
P_0_EAST = 0
AZIMUTH_0 = np.pi / 2  # 90° Clockwise

