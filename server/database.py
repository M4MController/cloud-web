from pymongo import MongoClient, DESCENDING

from .config.config import config

database_config = config["database"]

client = MongoClient(database_config["host"], database_config["port"])
database = client[database_config["name"]]


def get_last(collection):
    return collection.find_one({}, sort=[('_id', DESCENDING)])


class DatabaseManager:
    @staticmethod
    def get_last_gps():
        return get_last(database["sensor_7"])["value"]

    @staticmethod
    def get_last_obd():
        return get_last(database["sensor_8"])["value"]
