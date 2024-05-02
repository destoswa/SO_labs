import numpy as np


def rad(deg):
    return deg * np.pi / 180


def deg(rad):
    return rad * 180 / np.pi


# Path
IMU_FILENAME = './data/0419_1553_PostProBinaryDecoded.imu'

# Timespan for our group (Anthony & Swann)
T_0 = 482303
T_F = 482358

# Earth constants
EARTH_GRAVITY = -9.8055  # m/s², with positive axis going away from earth
EARTH_ANGULAR_RATE = 7.2921150E-5  # rad/s, with positive axis is the rotation axis going South to North

# Experiment constants in local frame NWD
LATITUDE = rad(46 + 31 / 60 + 17 / 3600)  # N46°31'17'' Latitude
ROLL = rad(5.172)
PITCH = rad(3.269)
AZIMUTH = rad(57.115)

