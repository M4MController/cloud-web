import logging

from flask import Flask
from pymongo import MongoClient
from sqlalchemy import create_engine

from server.routing import register_routes

logger = logging.getLogger(__name__)


class App:
    def __init__(self, config):
        self._config = config
        self._flask = Flask(__name__)

        self.db_engine = create_engine(config['database']['objects']['uri'])

        client = MongoClient(config['database']['data']['host'], config['database']['data']["port"])
        self.data_client = client[config['database']['data']["name"]]

        register_routes(self)

    def register_route(self, Resource, view, *endpoints):
        for endpoint in endpoints:
            self._flask.add_url_rule(endpoint, view, Resource.as_view(view, app=self))

    def run(self):
        host = self._config['host']
        port = self._config['port']
        logger.info('Listening {} on {} port'.format(host, port))
        self._flask.run(host=host, port=port)


from server.config import config

app = App(config)
