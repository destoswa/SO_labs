import numpy as np


# Simulation parameters
SIMULATION_TIME = 200  # 1 turn
SIM_FREQ = 100  # Hz
DT = 1/SIM_FREQ

# Movement constants
"""
Frames :
    frame-m Local/Inertial  Cartesian  : North East
    frame-p Local/Inertial  Polar : radius, phi   , phi = 0 <--> North
    frame-b Body:  x aligned with movement, y points away from rotation axis
"""

RADIUS = 500  # m
OMEGA = np.pi/100  # rad/s

POS_0_N = RADIUS  # m   
POS_0_E = 0  # m   
VEL_0_N = 0  # m/s 
VEL_0_E = OMEGA*RADIUS  # m/s 
ALPHA_0 = np.pi/2         # rad  (Frame-m,  0-rad when aligned with North)
STATES_0 = (POS_0_N, POS_0_E, VEL_0_N, VEL_0_E, ALPHA_0)
