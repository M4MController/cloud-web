import hjson
from os.path import join, dirname
from random import random


def generate():
    try:
        with open(join(dirname(__file__), "./obd.json")) as file:
            gps = hjson.loads(file.read())
            for elem in gps:
                elem["value"] = {"lon": str(random() * 360 - 180), "lat": str(random() * 180 - 90)}
        with open(join(dirname(__file__), "./gps.json"), "w") as file:
            file.write(hjson.dumpsJSON(gps))
    except:
        print("Unable to load or write file")
