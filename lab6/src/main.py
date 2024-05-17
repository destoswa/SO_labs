import numpy as np

import reference.signals as rs
import reference.constants as rc
import sensors.constants as sc
import sensors.signals as ss
import strapdown.integration as si
import kalman.kalman_filter as kf

""" 
DISCLAIMER : WIP

-- TODO -- 

# ! FIRST PRIORITY ! 
    - define order in states a, v, p  as in EKF or pva ?

# Not categorized 
    - initial uncertainty = ?

    


# reference constants : DONE 

# reference signals
    - rs.generate_ref_states
    - rs.generate_ref_imu

# noise
    all noise function : wn, rw, ...     

# sensors constants
    - noise models parameters

# sensors signals
    - ss.generate_noise_imu
    - ss.generate_noise_gps

# strapdown integration
    - si.strapdown     # Must convert imu from frame b to frame m

# kalman filter
    - initial delta_error = ?
    - kf_f, kf_g, kf_w
    - kf.ekf


"""

def main_simulation():

    """ Signals """

    # Reference signals
    ref_states = rs.generate_ref_states(rc.SIM_FREQ)

    # Noisy signals - IMU
    ref_imu = rs.generate_ref_imu(sc.IMU_FREQ)
    noise_imu = ss.generate_noise_imu(sc.IMU_FREQ)
    imu = ref_imu + noise_imu

    # Noisy signals - IMU
    ref_gps = rs.generate_ref_states(rc.GPS_FREQ)
    noise_gps = ss.generate_noise_gps(sc.GPS_FREQ)
    gps = ref_gps + noise_gps

    """ Simulation """

    # States arrays
    time_size = rc.SIMULATION_TIME/rc.DT
    states_est = np.zeros(time_size+1, 5)   
    states_pred = np.zeros(time_size+1, 5)  

    gps_size = rc.SIMULATION_TIME/sc.DT_GPS
    delta_z = np.zeros(gps_size+1, 2)  
    delta_states = np.zeros(gps_size+1, 5)  
    delta_error = np.zeros(gps_size+1, 5)  

    # Initial conditions (pN,pE,vN,vE,alpha)
    states_est[0,:] = rc.STATES_0

    # Time iteration
    dt = rc.DT
    time = np.arange(1, rc.SIMULATION_TIME+1, dt)
    for i, t in enumerate(time):
        
        has_new_imu = (t%sc.DT_IMU - 1) == 0
        has_new_gps = (t%sc.DT_GPS == 0)
        
        # precedent time iteration had new IMU values  -> Strapdown - order 1
        if has_new_imu:
            i_imu = (t-dt)/sc.DT_IMU + 1
            states_pred[i] = si.strapdown(states_est[i - 1], imu[i_imu - 1])

            # new GPS values  -> EKF
            if has_new_gps:
                i_gps = t//sc.DT_GPS

                # Kalman parameter  
                kf_f = None
                kf_w = None
                kf_g = None

                # EKF application
                delta_z[i_gps] = states_pred[i] - gps[i_gps]
                delta_states[i_gps], delta_error[i_gps] = kf.ekf(states_est[i], delta_z[i_gps], delta_error[i_gps-1], kf_f, kf_w, kf_g)
                states_est[i] = states_pred[i] + delta_states[i_gps]
            
            else:
                states_est[i] = states_pred[i]
                
        # No new values (never the case here)
        else:
            states_est[i] = states_est[i-1]
            

if __name__ == "__main__":

    # Reproducibility
    np.random.seed(42)

    """
    Could call main simulation with different params ? freq, noise,... -> must adapt function and arguments
    """
    main_simulation()