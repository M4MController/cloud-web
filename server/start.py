from server import app
from routing import Routing
from config.config import config

if __name__ == '__main__':
    app.run(host=config["host"], port=config["port"])
