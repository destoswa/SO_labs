from src.kalman import KalmanFilter
from src.Noise import WhiteNoise, white_noise
from src.showing_results import show_trajectory, show_innovation, show_error
from src import reference as ref
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

tunnel_prefix = "_tunnel" if ref.INCLUDE_TUNNEL else ""

def main():
    # Apply random seed for repeatability
    np.random.seed(22)

    # Reference (Position and velocities in N-E frame)
    ref_states = ref.generate_ref_states(ref.FREQ)

    # Generate realizations
    time = ref.generate_time_serie(ref.FREQ)
    for real in range(ref.NUMBER_REALIZATION):

        # Gps = ref + noise 
        time_gps = ref.generate_time_serie(freq=ref.GPS_FREQ)
        gps_states = ref.generate_ref_states(freq=ref.GPS_FREQ)[:, :2]
        gps_ref_states = gps_states.copy()
        size = int(ref.GPS_FREQ * ref.SIMULATION_TIME)
        gps_states[:, 0] = gps_states[:, 0] + white_noise(size, sd=0.5)  # x
        gps_states[:, 1] = gps_states[:, 1] + white_noise(size, sd=0.5)  # y

        # Initial conditions
        x0 = ref_states[0, :]

        # Uncertainties for initial conditions
        sigma_p0 = 10  # m
        sigma_v0 = 0.1  # m/s
        p0 = np.array([
            [sigma_p0 ** 2, 0, 0, 0],
            [0, sigma_p0 ** 2, 0, 0],
            [0, 0, sigma_v0 ** 2, 0],
            [0, 0, 0, sigma_v0 ** 2],
        ])

        # Motion model
        dt = ref.DT
        f = np.array([  # dx/dt = f * x     [vx, vy, ax, ay] = f * [x ,y , vx , vy]
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        g = np.array([
            [0, 0],
            [0, 0],
            [1, 0],
            [0, 1]
        ])
        sigma_a = 0.05 * np.sqrt(ref.FREQ)  # m/s² / sqrt(Hz)
        w = np.eye(2, 2) * sigma_a
        n = f.shape[0]
        A = np.zeros((2 * n, 2 * n))
        A[:n, :n] = -f
        A[:n, n:] = g @ w @ g.T
        A[n:, n:] = f.T
        A = A * ref.DT
        B = sp.linalg.expm(A)
        phi = B[n:, n:].T
        q = phi @ B[:n, n:]

        # Measurment model   z [2x1] = H[2X4] @ x[4x1] + v[2x1]
        h = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        sigma_gps = 0.5  # m
        r = np.eye(2) * sigma_gps**2

        # Kalman filter
        kf = KalmanFilter(x0, p0, phi, q, h, r)
        
        kf_states = []
        kf_covar_states = []
        
        kf_states.append(kf.x_est)
        kf_covar_states.append(kf.p_est)
        
        time_gps = [round(x,5) for x in time_gps]
        time = [round(x, 5) for x in time]
        for t in time[1:]:  # The initial position is not corrected, start at time[1]
            kf.predict()
            # Condition to add gps measure to kf
            if round(t,5) in time_gps and (t<ref.TUNNEL_TIME_START or t>= ref.TUNNEL_TIME_STOP or ref.INCLUDE_TUNNEL == False):
                ind = time_gps.index(t)
                z = gps_states[ind]
                kf.update(z)
            else:
                kf.no_meas_update()  # x_est, p_est = x_pred, p_pred
            kf_states.append(kf.x_est)
            kf_covar_states.append(kf.p_est)
        kf_states = np.array(kf_states)
        kf_covar_states = np.array(kf_covar_states)

        # Show trajectories
        show_trajectory(kf_states, gps_states, f"kf_state_{real}{tunnel_prefix}", ref.FREQ, "results/trajectory", do_save_fig=True)

        # Errors and standard deviations
        # 4.a
        diff_gps_ref = gps_states - gps_ref_states
        std_real_gps = np.sqrt(np.std(diff_gps_ref[:, 0])**2 + np.std(diff_gps_ref[:, 1])**2)

        # 4.b
        diff_kf_ref = kf_states[:, :2] - ref_states[:, :2]
        std_filtered = np.sqrt(np.std(diff_kf_ref[:, 0])**2 + np.std(diff_kf_ref[:, 1])**2)

        # 4.c
        p_var_x = kf_covar_states[:, 0, 0]
        p_var_y = kf_covar_states[:, 1, 1]
        kf_predicted_positioning_quality = np.sqrt(p_var_x + p_var_y)
        stabilized_value = np.mean(kf_predicted_positioning_quality[-10:])

        #fig = plt.figure(figsize=(10, 4))
        #plt.loglog(kf_predicted_positioning_quality)
        #fig.savefig(f"./results/kf_position_quality/{real}.jpg")

        print(f"==== Realization {real} ====")
        print(f"\tEmpirical std characterizing real GPS positioning quality: {std_real_gps}")
        print(f"\tEmpirical std characterizing filtered positioning quality: {std_filtered}")
        print(f"\tEmpirical std characterizing KF-predicted positioning quality : {stabilized_value}")
        
  
        # Position and Velocity errors alongside 3-sigma bounds
        sigma_pos = stabilized_value
        p_var_vx = kf_covar_states[:, 2, 2]
        p_var_vy = kf_covar_states[:, 3, 3]
        show_error(kf_states, ref_states, kf_covar_states, ref.FREQ, ref.GPS_FREQ, f"{real}{tunnel_prefix}", 'results/errors', True)

        # Innovation histogram
        innovation_sequence = gps_states - kf_states[::int(ref.FREQ/ref.GPS_FREQ), :2]
        show_innovation(innovation_sequence, f"{real}{tunnel_prefix}", ref.FREQ, 'results/innovation', True)
        

if __name__ == '__main__':
    main()
    #plt.show()
