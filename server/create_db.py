from pymongo import MongoClient
import hjson
from config import config

database_config = config["database"]


client = MongoClient(database_config["host"], database_config["port"])
database = client[database_config["name"]]

obd = database["OBD"]

obd_filename = database_config["obd_json"]
with open(obd_filename) as obd_file:
    data = hjson.loads(obd_file.read())
    obd.insert_many(data)
