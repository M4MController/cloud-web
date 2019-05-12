import hjson
from flask import jsonify, request

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

    @staticmethod
    @app.route('/data/sensor/<int:_id>/data')
    def data_query(_id):
        field = request.args.get('field')
        try:
            proj = {"_id": False, "timestamp": True}
            if field is not None:
                proj["value." + str(field)] = True
            else:
                proj["value"] = True

            return jsonify(DatabaseManager.get_available_data(_id, proj))
        except:
            app.logger.error('Unable to retrieve data for query from db!')
            return jsonify({}), 500
