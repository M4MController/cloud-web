from .config import config


def get_sensor_by_name(name):
    for option in config["database"]["initials"]:
        if option["name"].lower() == name.lower():
            return option

    return None


def get_sensor_by_id(id):
    for option in config["database"]["initials"]:
        if option["id"] == id:
            return option

    return None


sensor_ids = {
    "GPS": get_sensor_by_name("GPS")["id"],
    "OBD": get_sensor_by_name("OBD")["id"]
}
