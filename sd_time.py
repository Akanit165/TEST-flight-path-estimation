import numpy as np
from datetime import datetime
from astrolib import julian_date, siderial_time

def angle():

    omega_earth = 0.261799387799149 # rad/hour

    now = datetime.utcnow()
    year = now.year
    month = now.month
    day = now.day
    utc = now.hour + now.minute/60 + now.second/3600

    long = 0

    # for test with stellarium
    year = 2000
    month = 1
    day = 1
    utc = 12

    jd = julian_date(year, month, day, utc)
    jd_utc = julian_date(year, month, day, utc)
    gmst = siderial_time(year, month, day, utc, 0)
    lmst = siderial_time(year, month, day, utc, long)
    offset_time = 0 # second
    
    print("Current date                       : ", year, month, day)
    print("Universal Time (UTC)               : ", utc)
    print("Julian Date (0h UTC)               : ", jd)
    print("Julian Date + UTC                  : ", jd_utc)
    print("Greenwich Mean Siderial Time (GMST): ", gmst)
    print("Local Mean Siderial Time (LMST)    : ", lmst)

    ecef_angle = omega_earth*((gmst-offset_time)) # rad
    print("Angle with respect to Vernal Equinox", np.degrees(ecef_angle))

    C = np.cos(ecef_angle)
    S = np.sin(ecef_angle)

    # ECEF in term of ECI
    dcm = np.array([[C,  S, 0],
                    [-S,  C, 0],
                    [0,  0, 1]])

    # ECI in term of ECEF
    # dcm = np.array([[C,  -S, 0],
    #                 [S,  C, 0],
    #                 [0,  0, 1]])

    return dcm

if __name__ == "__main__":
    print("Direction Cosine Matrix\n", angle())
