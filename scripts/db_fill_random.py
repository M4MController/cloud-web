from datetime import datetime, timedelta
from random import random

from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from server.database.models import (
    Object,
    Controller,
    Sensor,
)

from server.config import config


def main():
    now = datetime.now()

    session = Session(create_engine(config['database']['objects']['uri']))

    session.query(Sensor).delete()
    session.query(Controller).delete()
    session.query(Object).delete()

    car = Object(
        name='Mercedes',
    )
    car_controller = Controller(
        name='Car controller',
        meta='',
        activation_date=now,
        deactivation_date=now,
        controller_type=0,
        status=0,
        mac='00:25:96:FF:FE:12:34:56',
        object=car
    )
    car_obd = Sensor(
        name='OBD',
        controller=car_controller,
    )
    car_gps = Sensor(
        name='GPS',
        controller=car_controller,
    )

    session.add(car)
    session.add(car_controller)
    session.add(car_obd)
    session.add(car_gps)
    session.commit()

    database_config = config["database"]["data"]

    client = MongoClient(database_config["host"], database_config["port"])
    database = client[database_config["name"]]

    for collection in database.list_collection_names():
        database.drop_collection(collection)

    obd_collection = database["sensor_{}".format(car_obd.id)]
    gps_collection = database["sensor_{}".format(car_gps.id)]


    gps_data = []
    for i in range(1000):
        now -= timedelta(seconds=1)
        gps_data.append({
            'timestamp': now,
            'value': {"lon": random() * 360 - 180, "lat": random() * 180 - 90}
        })

    obd_data = []
    for i in range(1000):
        now -= timedelta(seconds=1)
        obd_data.append({
            'timestamp': now,
            'value': {"speed": random() * 10 + 60}
        })

    gps_collection.insert_many(gps_data)
    obd_collection.insert_many(obd_data)


if __name__ == '__main__':
    main()
