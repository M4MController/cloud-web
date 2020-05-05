# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timezone
from gpiozero import Buzzer
from time import sleep
from server.database.managers import SensorDataManager
from m4m_client import send_data
from config import config
import requests

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

session = None


def get_db():
    global session
    if session is not None:
        return session

    session = Session(create_engine(config['database']['objects']['uri']))

    return session


def json_send(sensor_id, data):
    return requests.post(
        'http://backend:5000/private/sensor/{sensor_id}/data'.format(sensor_id=sensor_id),
        json={'value': data},
    )
    # Return Promise?
    # return SensorDataManager(get_db()).save_new(sensor_id, {
    #     'timestamp': timestamp,
    #     'value': data,
    # })


def cur_date():
    return datetime.now().replace(tzinfo=timezone.utc).strftime("%b %d %H:%M:%S m4m: ")


def beep():
    buzzer = Buzzer(17)
    buzzer.on()
    sleep(1)
    buzzer.off()
    sleep(1)
