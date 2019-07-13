# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone
from gpiozero import Buzzer
from time import sleep
from pymongo import MongoClient
from server.database.managers import SensorDataManager
from server.config import config

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

session = None


def get_db():
    global session
    if session is not None:
        return session

    session = Session(create_engine(config['database']['objects']['uri']))

    return session


def getMAC():
    try:
        try:
            mac = open("/sys/class/net/ppp0/address").read()
        except:
            mac = open("/sys/class/net/eth0/address").read()
    except:
        mac = "00:00:00:00:00:00"
    return mac[0:17]


def json_send(sensor_id, data):
    json_data = {
        "value": json.dumps(data),
        "timestamp": datetime.now().replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    }

    return SensorDataManager(get_db()).save_new(sensor_id, json_data)


def cur_date():
    return datetime.now().replace(tzinfo=timezone.utc).strftime("%b %d %H:%M:%S m4m: ")


def beep():
    buzzer = Buzzer(17)
    buzzer.on()
    sleep(1)
    buzzer.off()
    sleep(1)
