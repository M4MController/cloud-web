from server import app
from flask import jsonify
from config.config import config
from database import DatabaseManager
import hjson


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
                                "id": 1,
                                "name": "GPS",
                                "last_value": hjson.dumpsJSON(DatabaseManager.get_last_gps()),
                                "status": 1,
                                "type": 0
                              },
                              {
                                "id": 2,
                                "name": "OBD",
                                "last_value": hjson.dumpsJSON(DatabaseManager.get_last_obd()),
                                "status": 1,
                                "type": 0
                              }
                            ])
        except:
            app.logger.error('Unable to return data!')

            return jsonify({}), 500
