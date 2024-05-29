import numpy as np

import reference as ref
import noise

GPS_FREQ = 0.5
DT_GPS = int(1/GPS_FREQ)
OFFSET = int(DT_GPS/ref.DT)
SIGMA_GPS = 1

def generate_gps(ref_states):
    
    gps = np.full_like(ref_states[:, 3::], None)
    #gps[::OFFSET] = ref_states[:, :2:OFFSET].copy()
    gps[::OFFSET] = ref_states[::OFFSET, 3::].copy()
    n = gps[::OFFSET].shape[0]

    assert(n == 100)  # DEBUG

    gps[::OFFSET, 0] += noise.white_noise(n, SIGMA_GPS)
    gps[::OFFSET, 1] += noise.white_noise(n, SIGMA_GPS)
    
    return gps

IMU_FREQ = 100

SIGMA_ACC_WN = 50E-6 * np.sqrt(IMU_FREQ) 
SIGMA_ACC_GM = 200E-6 * np.sqrt(IMU_FREQ) 
TAU_ACC_GM = 60

BIAS_GYRO = -400 * np.pi/180 / 3600
SIGMA_GYRO_WN = 0.1 * np.pi/180 * np.sqrt(IMU_FREQ / 3600) 
SIGMA_GYRO_GM = 1E-2 * np.pi/180 * np.sqrt(IMU_FREQ) 
TAU_GYRO_GM = 30

def generate_imu(ref_imu):

    imu = ref_imu.copy()
    n = ref_imu.shape[0]

    # Acc X,Y
    imu[:, 0] += noise.white_noise(n, SIGMA_ACC_WN) + noise.gauss_markov(noise.white_noise(n, SIGMA_ACC_GM), 1/TAU_ACC_GM, 1/IMU_FREQ)
    imu[:, 1] += noise.white_noise(n, SIGMA_ACC_WN) + noise.gauss_markov(noise.white_noise(n, SIGMA_ACC_GM), 1/TAU_ACC_GM, 1/IMU_FREQ)

    # Gyro
    imu[:, 2] +=  BIAS_GYRO + noise.white_noise(n, SIGMA_GYRO_WN) + noise.gauss_markov(noise.white_noise(n, SIGMA_GYRO_GM), 1/TAU_GYRO_GM, 1/IMU_FREQ)

    return imu