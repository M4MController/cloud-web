# -*- coding: utf-8 -*-
import logging
import os
import sys
import time

from random import random

from m4m_utils import *
from m4m_obd import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

polling_delay = int(os.environ.get('TIMEOUT', '1'))
logger.info(cur_date(), "Power on\n")
logger.info("Current polling delay time: {}s".format(polling_delay))

def get_obd_con():
    while True:
        obd_con = obd_start()
        if obd_con.is_connected():
            return obd_con


def main():
    obd_sensor_id = int(os.environ.get('OBD_SENSOR_ID', 1))
    use_stubs = int(os.environ.get('USE_STUBS', "0"))

    if not use_stubs:
        obd_con = get_obd_con()

    while True:
        if use_stubs:
            data = {'speed': random() * 100}
            for i in range(use_stubs):
                data[str(i)] = random() * 100
            json_send(obd_sensor_id, data)
        elif obd_con.is_connected():
            try:
                data = obd_read(obd_con)
                json_send(obd_sensor_id, data)
            except Exception as e:
                logger.info("Failed reading data from obd! %s", e)
        else:
            obd_con = get_obd_con()

        time.sleep(polling_delay)


if __name__ == '__main__':
    main()