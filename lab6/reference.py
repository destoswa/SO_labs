import numpy as np

# Simulation parameter
SIMULATION_TIME = 200
SIMULATION_FREQ = 100
DT = 1/SIMULATION_FREQ
TIME_SEQUENCE = np.arange(0, SIMULATION_TIME, DT)

# Movement parameter
RADIUS = 500
OMEGA = np.pi/100
THETA_0 = 0
ALPHA_0 = np.pi/2

def generate_states(time_sequence=TIME_SEQUENCE):
    theta = THETA_0 + OMEGA * time_sequence    
    
    states = np.zeros(len(time_sequence), 5)  # P_N, P_E, V_N, V_E, Alpha
    states[:, 0] = RADIUS * np.cos(theta)     
    states[:, 1] = RADIUS * np.sin(theta)           
    states[:, 2] = - OMEGA * RADIUS * np.sin(theta)    
    states[:, 3] = OMEGA * RADIUS * np.cos(theta)      
    states[:, 4] = ALPHA_0 + THETA_0 

    return states

def generate_imu(time_sequence=TIME_SEQUENCE):
    theta = THETA_0 + OMEGA * time_sequence    

    imu = np.zeros(len(time_sequence), 5)  # A_X, A_Y, G 
    imu[:,0] = np.full_like(theta, 0)
    imu[:,1] = np.full_like(theta, OMEGA**2 * RADIUS)
    imu[:,2] = np.full_like(theta, OMEGA)

    return imu
