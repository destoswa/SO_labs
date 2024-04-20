import numpy as np
import pandas as pd
from src.readimu import readimu


def main():
    # ==========================================
    # ================= Part I =================
    print("========== PART I ===========\n")

    # Read data
    columns = ['Time', 'g_N', 'g_W', 'g_D', 'a_N', 'a_W', 'a_D']
    full_data = readimu('./data/0419_1553_PostProBinaryDecoded.imu', "IXSEA")
    df_full_data = pd.DataFrame(full_data, columns=columns)

    # Select the data correponding to the right time
    df_data = df_full_data[df_full_data['Time'].between(482303, 482358)]
    df_acc = df_data[['Time', 'a_N', 'a_W', 'a_D']]
    df_gyro = df_data[['Time', 'g_N', 'g_W', 'g_D']]
    s_time = df_data.Time
    print("DATA :")
    print(df_data.head())

    # ==========================================
    # ================= Part II =================
    print("\n\n========== PART II ===========\n")
    s_norm_gyro = (df_gyro.g_N**2 + df_gyro.g_W**2 + df_gyro.g_D**2)**0.5
    print("Gyro : Mean of norm serie", s_norm_gyro.mean())
    print("Gyro : Std of norm serie", s_norm_gyro.std())

    # ==========================================
    # ================= Part III =================
    print("\n\n========== PART III ===========\n")
    s_norm_acc = (df_acc.a_N**2 + df_acc.a_W**2 + df_acc.a_D**2)**0.5
    print("Acc: Mean of norm serie", s_norm_acc.mean())
    print("Acc: Std of norm serie", s_norm_acc.std())

    # ==========================================
    # ================= Part IV =================


    # ==========================================
    # ================= Part V =================




if __name__ == '__main__':
    main()
