import numpy as np
from lab3.src.sensor import NoiseModel as Nm

# Simulation parameter
PLOTS_DIR = './data/lab3/'
RANDOM_SEED = 42
SIMULATION_TIME = 200
FREQ = 100
ORDER = 2

# Convention : Units & common constants
LENGTH_UNIT = 'm'
TIME_UNIT = 's'
ANGLE_UNIT = 'rad'
ACC_GRAVITY = 9.81  # m²/s

# Uniform circular motion parameters (UNKNOWN for measurements and numerical integration)
RADIUS = 500
OMEGA = np.pi / 100  # Radial_velocity

# Initial conditions (KNOWN for numerical integration)
INITIAL_CONDITIONS = {
    'theta': 0,  # Angle between object and north axis
    'azimuth': np.pi / 2,  # Orientation of object w.r.t to north axis
    'p_N': RADIUS,
    'p_E': 0,
    'v_N': 0,
    'v_E': OMEGA * RADIUS
}

# Sensor noise models
GYRO_NOISE_MODELS = [
    Nm.Bias(bias_sd=150 * np.pi / 180 * 1 / 3600),  # bias_sd: rad/s
    Nm.GaussMarkov(psd_gm=7E-3 * np.pi / 180, tau=100),  # psd: rad/s/sqrt(Hz), tau: s
    Nm.RandomWalk(psd_wn=1E-1 * np.pi / 180 * 1 / 60)  # psd: rad/(s * sqrt(Hz))
]

ACC_NOISE_MODELS = [
    Nm.Bias(bias_sd=1.3E-3 * ACC_GRAVITY),  # bias_sd: m/s²
    Nm.WhiteNoise(psd_wn=57E-6 * ACC_GRAVITY)  # psd: m/s²/sqrt(Hz)
]
