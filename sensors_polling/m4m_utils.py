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


def json_send(sensor_id, data, send_to_server=True):
    now = datetime.now()
    timestamp = now.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    try:
        if send_to_server:
            send_data(sensor_id, now, data)
    except Exception as e:
        logger.info("Can not send data", e)

    return requests.post(config.host + ':' + config.port + '/private/sensor/' + sensor_id + '/add', data={
        'timestamp': timestamp,
        'value': data
    })
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
