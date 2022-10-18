from math import *
import numpy as np
import pandas as pd
import numpy as np
from datetime import datetime
from astro import julian_date, siderial_time

# Constants
r_e = 6371 # Earth radius [km]
mu = 3.986e5 # Standard gravitational parameter [km3s-2]

# transform month string to int
def month_transform(month_data):

    month2num = {'Jan' : 1,
                 'Feb' : 2,
                 'Mar' : 3,
                 'Apr' : 4,
                 'May' : 5,
                 'Jun' : 6,
                 'Jul' : 7,
                 'Aug' : 8,
                 'Sep' : 9,
                 'Oct' : 10,
                 'Nov' : 11,
                 'Dec' : 12}

    return month2num[month_data]

# import satellite position data from csv file

data = pd.read_csv('data.csv') 
time_data = data['day']

# define index for current and next position: ex. index = 1 is line 2 in csv file
time_index = int(input("Enter time index (more than 0): "))-1
predict_index = int(input("Enter time index to predict (shouldn't more than previous index + 10 for accuracy): "))-1
current_date = time_data[time_index]
predicted_date = time_data[predict_index]

# Extract current time in csv to second
time = time_data[time_index]
time = [float(t) for t in time.split(' ')[4].split(':')]
time = time[0]*3600 + time[1]*60 + time[2]

# Extract date and time to predict
# day, month, year and utc are used to calculate rotation matrix from ECEF to ECI
time_predict = time_data[predict_index]
date_predict = time_predict.split(' ')
day = int(date_predict[1])
month = month_transform(date_predict[2])
year = int(date_predict[3])

time_predict = [float(t) for t in date_predict[4].split(':')]
time_predict = time_predict[0]*3600 + time_predict[1]*60 + time_predict[2]
utc = time_predict/3600

# Calculate interval (delta_t) to calculate predicted position 
time_interval = time_predict - time

# Call current position in ECI frame
x = data['x'][time_index]
y = data['y'][time_index]
z = data['z'][time_index]

r_eci = np.array([x, y, z])

# Call velocity in ECI frame
vx = data['vx'][time_index]
vy = data['vy'][time_index]
vz = data['vz'][time_index]

# Call current position in ECEF frame
r = data['alt'][time_index] + r_e
lat = np.radians(data['lat'][time_index])
long = np.radians(data['long'][time_index])

# Calculate the rotation matrix to transform ECEF to ECI
def angle():

    omega_earth = 0.261799387799149 # rad/hour

    jd = julian_date(year, month, day, 0)
    jd_utc = julian_date(year, month, day, utc)
    gmst = siderial_time(year, month, day, utc, 0)
    offset_time = 0 # second
    
    ecef_angle = omega_earth*((gmst-offset_time)) # rad
    print("angle between ECI", ecef_angle)
    
    C = np.cos(ecef_angle)
    S = np.sin(ecef_angle)

    # ECI in term of ECEF
    dcm = np.array([[C,  -S, 0],
                    [S,  C, 0],
                    [0,  0, 1]])

    return dcm

# Calculate acceleration in ECI frame
def accel_eci(r, lat, long):

    # from MATLAB

    a_x = (mu*cos(lat)*cos(long)*((81*r_e**2*((3*sin(lat)**2)/2 - 1/2))/(25000*r**2) + (3*r_e**2*((7414115378105343*cos(2*long))/4722366482869645213696 - (8528593868062579*sin(2*long))/9444732965739290427392)*(3*sin(lat)**2 - 3))/r**2 - 1))/r**2 + (mu*cos(long)*sin(lat)*((81*r_e**2*cos(lat)*sin(lat))/(25000*r**2) + (6*r_e**2*cos(lat)*sin(lat)*((7414115378105343*cos(2*long))/4722366482869645213696 - (8528593868062579*sin(2*long))/9444732965739290427392))/r**2))/r**2 - (2*mu*r_e**2*sin(long)*((8528593868062579*cos(2*long))/9444732965739290427392 + (7414115378105343*sin(2*long))/4722366482869645213696)*(3*sin(lat)**2 - 3))/(r**4*cos(lat))
    
    a_y = (mu*cos(lat)*sin(long)*((81*r_e**2*((3*sin(lat)**2)/2 - 1/2))/(25000*r**2) + (3*r_e**2*((7414115378105343*cos(2*long))/4722366482869645213696 - (8528593868062579*sin(2*long))/9444732965739290427392)*(3*sin(lat)**2 - 3))/r**2 - 1))/r**2 + (mu*sin(lat)*sin(long)*((81*r_e**2*cos(lat)*sin(lat))/(25000*r**2) + (6*r_e**2*cos(lat)*sin(lat)*((7414115378105343*cos(2*long))/4722366482869645213696 - (8528593868062579*sin(2*long))/9444732965739290427392))/r**2))/r**2 + (2*mu*r_e**2*cos(long)*((8528593868062579*cos(2*long))/9444732965739290427392 + (7414115378105343*sin(2*long))/4722366482869645213696)*(3*sin(lat)**2 - 3))/(r**4*cos(lat))

    a_z = (mu*sin(lat)*((81*r_e**2*((3*sin(lat)**2)/2 - 1/2))/(25000*r**2) + (3*r_e**2*((7414115378105343*cos(2*long))/4722366482869645213696 - (8528593868062579*sin(2*long))/9444732965739290427392)*(3*sin(lat)**2 - 3))/r**2 - 1))/r**2 - (mu*cos(lat)*((81*r_e**2*cos(lat)*sin(lat))/(25000*r**2) + (6*r_e**2*cos(lat)*sin(lat)*((7414115378105343*cos(2*long))/4722366482869645213696 - (8528593868062579*sin(2*long))/9444732965739290427392))/r**2))/r**2
 
    # transform acceleration in ECEF to ECI frame
    dcm = angle()
    a_ecef = np.array([a_x, a_y, a_z])
    a_eci = np.matmul(dcm, np.transpose(a_ecef))

    return a_eci

# Calculate predicted velocity
def velocity(time_interval,accel_eci):

    v_x = vx + accel_eci[0]*time_interval
    v_y = vy + accel_eci[1]*time_interval
    v_z = vz + accel_eci[2]*time_interval

    return np.array([v_x, v_y, v_z])

# Calculate predicted position of satellite
def position(time_interval, accel_eci):

    r_x = x + (vx + accel_eci[0]*time_interval)*time_interval
    r_y = y + (vy + accel_eci[1]*time_interval)*time_interval
    r_z = z + (vz + accel_eci[2]*time_interval)*time_interval

    return np.array([r_x, r_y, r_z])

def position_ecef(sat_position, dcm):

    inv_dcm = np.linalg.inv(dcm)
    r_ecef = np.matmul(inv_dcm,np.transpose(sat_position))
    x_ecef, y_ecef, z_ecef = r_ecef
    new_r = np.linalg.norm(r_ecef)
    new_lat = np.degrees(np.arctan(z_ecef/(sqrt(x_ecef**2+y_ecef**2))))
    new_long = np.degrees(np.arctan(y_ecef/x_ecef))
    
    return np.array([new_r, new_lat, new_long])

if __name__ == "__main__":
    print("Current date: ", current_date)
    print("Predicted date: ", predicted_date)
    print("Satellite position in next", np.float16(time_interval/60),"min :",position(time_interval, accel_eci(r, lat, long)))
    print("Satellite velocity in next", np.float16(time_interval/60),"min :",velocity(time_interval, accel_eci(r, lat, long)))
    
    