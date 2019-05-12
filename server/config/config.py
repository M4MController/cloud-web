from server import app
import hjson
import os

config_file = os.path.join(os.path.dirname(__file__) + 'config.hjson')
config = {}

try:
    with open(config_file) as file:
        config = hjson.loads(file.read())
except:
    app.logger.warning('Unable to load configuration file %s!', config_file)
