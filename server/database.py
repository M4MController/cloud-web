from pymongo import MongoClient, DESCENDING
from config.config import config

database_config = config["database"]

client = MongoClient(database_config["host"], database_config["port"])
database = client[database_config["name"]]

obd = database["OBD"]


class DatabaseManager:
    @staticmethod
    def get_last_gps():
        return {"lat": 1, "lon": 2}

    @staticmethod
    def get_last_obd():
        record = obd.find_one({}, sort=[('_id', DESCENDING)])
        return record["value"]
