import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

import reference as ref
import sensors as sen



def main():

    # Reference
    ref_states = ref.generate_states()  # PVA, error acc_x, error acc_y, error_gyro
    ref_imu = ref.generate_imu()        # Accs, gyro

    # Sensors
    gps = sen.generate_gps(ref_states)  # None when no measurement
    imu = sen.generate_imu(ref_imu)
    
    # Initialize Kalman matrices (time invariant)
    
    n = ref_states.shape(1)
    
    #   dz = H dx
    H = np.zeroes((n,n))   
    H[0,0], H[1,1] = 1, 1

    #   d(dx)/dt = F * dx + G * w  -> L11_INSGPS-dEKF-blackboard.pdf
    
    F = None  
    
    G = None
    
    w = None

    A = None # | -F   G @ w @ G.T  | 
             # |  0   F.T          |

    B = None # exp(A*dt)   =  # |  -     PHI^-1 * Q        |
                              # |  -     PHI.T             |

    phi = None  # B22.T
    q = None    # phi * B12
    
    # Initialize states matrix
    states_est = np.zeroes_like(ref_states)
    states_est[0] = INITIAL_CONDITIONS

    # Kalman Filter
    for t, _ in enumerate(TIME_SEQUENCE[1:]):

        # Prediction dx
        delta_pred = strapdown(IMU[t])  #  dPVA


        # Update with dz
        if GPS[t] != None: 
            
            delta_z = None #

            # Gain
            # Update dx
            # Update P
        
        # Update state
        states_est[t] = states_est[t-1] + delta_est


if __name__ == "__main__":
    main()