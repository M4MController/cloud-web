import hjson
from flask import jsonify

from .server import app
from .config.config import config
from .config.sensors import sensor_ids
from .database import DatabaseManager


class Routing:
    @staticmethod
    @app.route('/sign_in', methods=['POST'])
    def sign_in():
        try:
            return jsonify({'token': config['user_token']})

        except:
            app.logger.error('Unable to get user_token value from config!')

            return jsonify({}), 500

    @staticmethod
    @app.route('/data')
    def data():
        try:
            return jsonify([
                              {
                                "id": sensor_ids["GPS"],
                                "name": "GPS",
                                "last_value": hjson.dumpsJSON(DatabaseManager.get_last_gps()),
                                "status": 1,
                                "type": 0
                              },
                              {
                                "id": sensor_ids["OBD"],
                                "name": "OBD",
                                "last_value": hjson.dumpsJSON(DatabaseManager.get_last_obd()),
                                "status": 1,
                                "type": 0
                              }
                            ])
        except:
            app.logger.error('Unable to return data!')

            return jsonify({}), 500
