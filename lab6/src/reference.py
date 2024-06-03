import numpy as np

# Simulation parameter
GRAVITY_CST = 9.81
SIMULATION_TIME = 200
SIMULATION_FREQ = 100
DT = 1/SIMULATION_FREQ
TIME_SEQUENCE = np.arange(0, SIMULATION_TIME, DT)
NOISY = True

# Movement parameter
RADIUS = 500
OMEGA = np.pi/100
THETA_0 = 0
ALPHA_0 = np.pi/2

# Tunnel
INCLUDE_TUNNEL = False
TUNNEL_THETA_START = 180
TUNNEL_THETA_STOP = 270
TUNNEL_THETA_START = TUNNEL_THETA_START  * np.pi/180
TUNNEL_THETA_STOP = TUNNEL_THETA_STOP  * np.pi/180
TUNNEL_TIME_START = TUNNEL_THETA_START/OMEGA
TUNNEL_TIME_STOP = TUNNEL_THETA_STOP/OMEGA

def generate_time_serie(freq):
    return np.arange(0, SIMULATION_TIME, 1/freq)

def generate_states(time_sequence=TIME_SEQUENCE):
    theta = THETA_0 + OMEGA * time_sequence    
    
    states = np.zeros((len(time_sequence), 5))  # Alpha, V_N, V_E, P_N, P_E
    states[:, 0] = ALPHA_0 + theta
    states[:, 1] = - OMEGA * RADIUS * np.sin(theta)
    states[:, 2] = OMEGA * RADIUS * np.cos(theta)
    states[:, 3] = RADIUS * np.cos(theta)
    states[:, 4] = RADIUS * np.sin(theta)

    return states

def generate_imu(time_sequence=TIME_SEQUENCE):
    theta = THETA_0 + OMEGA * time_sequence    

    imu = np.zeros((len(time_sequence), 5))  # A_X, A_Y, G
    imu[:,0] = np.full_like(theta, 0)
    imu[:,1] = np.full_like(theta, OMEGA**2 * RADIUS)
    imu[:,2] = np.full_like(theta, OMEGA)

    return imu

def is_in_tunnel(t):
    time = TIME_SEQUENCE[t]
    return (time > TUNNEL_TIME_START and t>= TUNNEL_TIME_STOP and INCLUDE_TUNNEL)