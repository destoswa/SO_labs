import numpy as np

"""
Define all params of Lab 3
"""
# Simulation parameter
SIMULATION_TIME = 200
PLOTS_DIR = './data/'
RANDOM_SEED = 42
FREQ = 100
ORDER = 2

# Convention : Units & constants
LENGTH_UNIT = 'm'
TIME_UNIT = 's'
ANGLE_UNIT = 'rad'
ACC_GRAVITY = 9.81  # m²/s

# Uniform circular motion parameters (UNKNOWN)
RADIUS = 500
OMEGA = np.pi / 100  # Radial_velocity

# Initial conditions (KNOWN)
INITIAL_CONDITIONS = {
	'theta': 0,  # Angle between object and north axis
	'azimuth': np.pi/2,  # Orientation of object w.r.t to north axis
	'p_N': RADIUS,
	'p_E': 0,
	'v_N': 0,
	'v_E': OMEGA*RADIUS
}

# Sensor noise specs
acc_specs = {
	'B': {'bias': 1.3E-3 * ACC_GRAVITY},  # m/s²
	'WN': {'sd_wn_psd': None}  # m/s²/sample
}

gyro_specs = {
	'B': {'bias': 150 * np.pi / 180 / 3600},  # rad/s
	'RW': {'sd_wn_psd': None},  # rad/s/sample
	'GM': {'sd_gm_psd': None, 'tau': 100}  # resp. rad/s/sample and s
}
