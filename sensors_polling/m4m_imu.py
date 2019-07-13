# -*- coding: utf-8 -*-
import datetime
import smbus
import math
from m4m_utils import cur_date
from termcolor import colored
import threading, os, time 

FILE = "IMU_log.csv"
GYRO_NORM = 131
ACCEL_NORM = 16384.0

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
address = 0x68       # via i2cdetect
 
def read_word_2c(reg, bus):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    val = (h << 8) + l
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def imu_writelog(bus): 
    gyro_x = read_word_2c(0x43, bus) / GYRO_NORM
    gyro_y = read_word_2c(0x45, bus) / GYRO_NORM
    gyro_z = read_word_2c(0x47, bus) / GYRO_NORM
     
    accel_x = read_word_2c(0x3b, bus) / ACCEL_NORM
    accel_y = read_word_2c(0x3d, bus) / ACCEL_NORM
    accel_z = read_word_2c(0x3f, bus) / ACCEL_NORM

    x_rotation = get_x_rotation(accel_x, accel_y, accel_z)
    y_rotation = get_y_rotation(accel_x, accel_y, accel_z)

    data = [gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, x_rotation, y_rotation]   

    timestamp = str(datetime.datetime.now())
    if not os.path.exists(FILE):
        csv = open(FILE, "w")
        csv.write("timestamp;gyro_x;gyro_y;gyro_z;accel_x;accel_y;accel_z;x_rotation;y_rotation\n")
    else:
        csv = open(FILE, "a")
    csv.write("{};".format(timestamp))
    for key in data:
        csv.write(repr(key))
        csv.write(";")
    csv.write("\n")
    csv.close()

def imu_connect():
    print(cur_date(), "Connecting to IMU...")
    try:
        bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
        bus.write_byte_data(address, power_mgmt_1, 0) # Activate to be able to address the module
    except:
        print(cur_date(), colored("IMU not connected", 'red'))
    else:
        t = threading.currentThread()
        print(cur_date(), "Logging IMU started")
        while getattr(t,'do_run', True):
            imu_writelog(bus)
            time.sleep(1)
    	


