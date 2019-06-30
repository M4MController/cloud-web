# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone
from gpiozero import Buzzer
from time import sleep
from pymongo import MongoClient
from server.database.managers import SensorDataManager
from server.config import config

database = None


def get_db():
    global database
    if database is not None:
        return database

    client = MongoClient(config['database']['data']['host'], config['database']['data']["port"])
    database = client[config['database']['data']["name"]]

    return database


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
