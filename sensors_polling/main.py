# -*- coding: utf-8 -*-
import os
import time

from random import random

from m4m_imu import *
from m4m_utils import *
from m4m_obd import *
from m4m_gsm import *

polling_delay = 1
print(cur_date(), "Power on\n")
print("Current polling delay time: {}s".format(polling_delay))


#redOn()

#IMU START -> thread
imu_ev = threading.Event()
imu_t = threading.Thread(target=imu_connect, args=())
imu_t.do_run = True
imu_t.start()
imu_ev.set()

#GSM START
def get_gsm_con():
    return gsm_start()

#sim check

#eth check

#obd START
def get_obd_con():
    while True:
        obd_con = obd_start()
        if obd_con.is_connected():
            return obd_con
#if not obd_con.is_connected():
#gsm_sendSMS(gsm_con, PHONE, MSG_OBD_DISCONNECT_ENG)

data = {}
lat, lon = 0, 0


#gsm_call(gsm_con, PHONE)
#beep()

try:
    use_stubs = bool(os.environ.get('USE_STUBS', False))
    obd_sensor_id = int(os.environ.get('OBD_SENSOR_ID', 1))
    gsm_sensor_id = int(os.environ.get('GSM_SENSOR_ID', 2))

    if not use_stubs:
        obd_con = get_obd_con()
        gsm_con = get_obd_con()

    while True:
        if use_stubs:
            json_send(obd_sensor_id, {'speed': random() * 100})
        elif obd_con.is_connected():
            try:
                data = obd_read(obd_con)
                json_send(obd_sensor_id, data)
            except Exception as e:
                print("Failed reading data from obd!", e)

        if use_stubs:
            json_send(obd_sensor_id, {'lat': random() * 50, 'lon': random() * 5})
        elif gsm_con:
            try:
                lat, lon = gsm_getGPS(gsm_con)
                json_send(gsm_sensor_id, {'lat': lat, 'lon': lon})
            except:
                print("Failed reading data from gps!")

        time.sleep(polling_delay)
except KeyboardInterrupt:
    if not use_stubs and gsm_con is not None:
        gsm_con.close()
finally:
    # imu_t.do_run = False
    if not use_stubs and gsm_con:
        gsm_con.close()
