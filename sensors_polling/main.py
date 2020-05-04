# -*- coding: utf-8 -*-
import logging
import os
import sys
import time

from random import random

from m4m_utils import *
from m4m_obd import *
from m4m_gsm import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

polling_delay = int(os.environ.get('TIMEOUT', '1'))
logger.info(cur_date(), "Power on\n")
logger.info("Current polling delay time: {}s".format(polling_delay))

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

use_stubs = int(os.environ.get('USE_STUBS', "0"))

try:
    obd_sensor_id = int(os.environ.get('OBD_SENSOR_ID', 1))
    gsm_sensor_id = int(os.environ.get('GSM_SENSOR_ID', 2))
    send_to_server = bool(os.environ.get('SEND_TO_SERVER', True))

    if not use_stubs:
        obd_con = get_obd_con()
        gsm_con = get_gsm_con()

    while True:
        if use_stubs:
            data = {'speed': random() * 100}
            for i in range(use_stubs):
                data[str(i)] = random() * 100
            json_send(obd_sensor_id, data, send_to_server=send_to_server)
        elif obd_con.is_connected():
            try:
                data = obd_read(obd_con)
                json_send(obd_sensor_id, data, send_to_server=send_to_server)
            except Exception as e:
                logger.info("Failed reading data from obd! %s", e)

        if use_stubs:
            json_send(gsm_sensor_id, {'lat': random() * 50, 'lon': random() * 5}, send_to_server=send_to_server)
        elif gsm_con:
            try:
                lat, lon = gsm_getGPS(gsm_con)
                json_send(gsm_sensor_id, {'lat': lat, 'lon': lon}, send_to_server=send_to_server)
            except:
                logger.info("Failed reading data from gps!")

        time.sleep(polling_delay)
except KeyboardInterrupt:
    if not use_stubs and gsm_con is not None:
        gsm_con.close()
finally:
    # imu_t.do_run = False
    if not use_stubs and gsm_con:
        gsm_con.close()
