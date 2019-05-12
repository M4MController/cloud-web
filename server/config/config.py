import hjson
from os.path import join, dirname

from ..server import app

config_file = join(dirname(__file__) + './config.hjson')
config = {}

try:
    with open(config_file) as file:
        config = hjson.loads(file.read())
except:
    app.logger.warning('Unable to load configuration file %s!', config_file)
