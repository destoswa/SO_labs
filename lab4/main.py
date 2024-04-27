import numpy as np
import pandas as pd
from src.readimu import readimu
import matplotlib.pyplot as plt

# Reference
g_ref = -9.8055  # m/s²
w_ref = 7.2921150E-5  # rad/s
phi_ref = 46 + 31 / 60 + 17 / 3600  # N46°31'17''

# Reference attitude (NWD, deg)
roll_ref = 5.172
pitch_ref = 3.269
azimuth_ref = 57.115  # TODO : Is it the yaw ? Assumed yes in the code

# ->(NED, rad)
roll_ref = roll_ref * np.pi / 180
pitch_ref = - pitch_ref * np.pi / 180
azimuth_ref = azimuth_ref * np.pi / 180
phi_ref = phi_ref * np.pi / 180


def main():
    # Disable pandas warning
    pd.set_option('mode.chained_assignment', None)

    # ==========================================
    # ================= Part I =================
    print("========== PART I ===========\n")

    # Read data (NWU)
    columns = ['Time', 'g_N', 'g_W', 'g_U', 'a_N', 'a_W', 'a_U']
    full_data = readimu('./data/0419_1553_PostProBinaryDecoded.imu', "IXSEA")
    df_full_data = pd.DataFrame(full_data, columns=columns)

    # Select the data corresponding to the right time
    df_data = df_full_data[df_full_data['Time'].between(482303, 482358)]
    df_acc = df_data[['Time', 'a_N', 'a_W', 'a_U']]
    df_gyro = df_data[['Time', 'g_N', 'g_W', 'g_U']]
    s_time = df_data.Time
    print("DATA :")
    print(df_data.head())

    # Rotate from NWU to NED
    df_acc['a_E'] = - df_acc['a_W']
    df_acc['a_D'] = - df_acc['a_U']
    df_gyro['g_E'] = - df_gyro['g_W']
    df_gyro['g_D'] = - df_gyro['g_U']

    # ==========================================
    # ================= Part II =================
    print("\n\n========== PART II ===========\n")
    s_norm_gyro = (df_gyro.g_N ** 2 + df_gyro.g_E ** 2 + df_gyro.g_D ** 2) ** 0.5
    list_s_norm_gyro = s_norm_gyro.sort_values().to_list()[0:int(len(s_norm_gyro)*.03)]
    #s_norm_gyro.plot()
    print(f"Gyro : reference {w_ref:.5E} [rad/s]")
    #print(f"Gyro : Mean of norm serie {np.mean(list_s_norm_gyro):.5E} [rad/s]")
    print(f"Gyro : Mean of norm serie {s_norm_gyro.mean():.5E} [rad/s]")
    print(f"Gyro : Std of norm serie, {s_norm_gyro.std():.5E} [rad/s]")

    fig = plt.figure(figsize=(10, 4))
    plt.semilogy(s_norm_gyro, alpha=.2, label='Measurements', color='blue', linewidth=.5)
    plt.plot([s_norm_gyro.index[0], s_norm_gyro.index[-1]], [s_norm_gyro.mean(), s_norm_gyro.mean()], color='blue', linewidth=1.5, label="Mean of measurements")
    plt.plot([s_norm_gyro.index[0], s_norm_gyro.index[-1]], [w_ref, w_ref], color='red', linewidth=1.5, label="Reference")
    plt.ylabel('Norm of Gyro [rad/s]')
    plt.xlabel('GPS - Time of week [s]')
    plt.ylim([0, 3e-2])
    plt.legend()
    fig.savefig('result/norm_gyro.svg', format='svg')
    fig.savefig('result/norm_gyro.png', format='png')

    # ==========================================
    # ================= Part III =================
    print("\n\n========== PART III ===========\n")
    s_norm_acc = (df_acc.a_N ** 2 + df_acc.a_E ** 2 + df_acc.a_D ** 2) ** 0.5
    print(f"Acc : reference {g_ref:.5E} [m/s²]")
    print(f"Acc: Mean of norm serie {- s_norm_acc.mean():.5E} [m/s²]")
    print(f"Acc: Std of norm serie {s_norm_acc.std():.5E} [m/s²]")

    # ==========================================
    # ================= Part IV =================
    print("\n\n========== PART IV ===========\n")
    f_x = df_acc.a_N.mean(axis=0)
    f_y = df_acc.a_E.mean(axis=0)
    f_z = df_acc.a_D.mean(axis=0)
    roll_b_l = np.arctan2(-f_y, -f_z)
    pitch_b_l = np.arctan2(f_x, np.sqrt(f_y ** 2 + f_z ** 2))

    print(f'True roll : {roll_ref*360/np.pi:.5E} [deg]')
    print(f'Estimated roll : {roll_b_l*360/np.pi:.5E} [deg]\n')
    print(f'True pitch : {pitch_ref*360/np.pi:.5E} [deg]')
    print(f'Estimated pitch : {pitch_b_l*360/np.pi:.5E} [deg]')

    # ==========================================
    # ================= Part V =================
    print("\n\n========== PART V ===========\n")
    roll_l_b = - roll_b_l
    pitch_l_b = - pitch_b_l

    w_x = df_gyro.g_N.mean(axis=0)
    w_y = df_gyro.g_E.mean(axis=0)
    w_z = df_gyro.g_D.mean(axis=0)

    cos_p = np.cos(pitch_l_b)
    sin_p = np.sin(pitch_l_b)
    cos_r = np.cos(roll_l_b)
    sin_r = np.sin(roll_l_b)

    w = np.array([w_x, w_y, w_z])
    rot_leveled_b = np.array(
        [
            [cos_p, 0, -sin_p],
            [sin_r * sin_p, cos_r, sin_r * cos_p],
            [cos_r * sin_p, -sin_r, cos_r * cos_p]
        ]
    )
    w_leveled = np.matmul(rot_leveled_b, w)
    yaw = np.arctan2(-w_leveled[1], w_leveled[0])
    print(f'True yaw : {azimuth_ref*360/np.pi:.5E} [deg]')
    print(f'Estimated yaw : {yaw*360/np.pi:.5E} [deg]\n')

    phi = np.pi/2 - np.arccos(-w_z / w_ref)
    print(f'True latitude (phi) : {phi_ref*360/np.pi:.5E} [deg]')
    print(f'Estimated latitude (phi) : {phi*360/np.pi:5E} [deg]\n')


if __name__ == '__main__':
    main()
    plt.show()