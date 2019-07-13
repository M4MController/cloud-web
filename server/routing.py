from server.config import config
from server.resources.base import BaseResource
from server.database.schemas import SensorDataSchema, ResourceSchema

from server.resources.utils import provide_db_session, schematic_response

from server.database.managers import SensorManager, SensorDataManager, ObjectManager, ControllerManager


class Auth(BaseResource):
    def post(self):
        return {'token': config['user_token']}


class User(BaseResource):
    def get(self):
        return config['user_info']


class ObjectsResource(BaseResource):
    def _insert_last_value(self, sensors):
        data_manager = SensorDataManager(self.db_data)

        for sensor in sensors:
            last_value = data_manager.get_last_record(sensor.id)
            sensor.last_value = last_value and last_value['value']

    @provide_db_session
    @schematic_response(ResourceSchema())
    def get(self):
        sensors = SensorManager(self.db_session).get_all()
        objects = ObjectManager(self.db_session).get_all()
        controllers = ControllerManager(self.db_session).get_all()
        self._insert_last_value(sensors)

        return {
            'objects': objects,
            'controllers': controllers,
            'sensors': sensors,
        }


class SensorDataResource(BaseResource):
    @provide_db_session
    @schematic_response(SensorDataSchema(many=True))
    def get(self, sensor_id):
        return SensorDataManager(self.db_data).get_sensor_data(sensor_id)


class AllObjectsInfoResource(BaseResource):
    @provide_db_session
    @schematic_response(ResourceSchema())
    def get(self):
        objects = ObjectManager(self.db_session).get_all()
        sensors = SensorManager(self.db_session).get_all()
        controllers = ControllerManager(self.db_session).get_all()

        return {
            'objects': objects,
            'sensors': sensors,
            'controllers': controllers
        }


def register_routes(app):
    app.register_route(Auth, 'sign_in', '/sign_in')
    app.register_route(ObjectsResource, 'objects', '/objects')
    app.register_route(SensorDataResource, 'sensor_data', '/sensor/<int:sensor_id>/data')
    app.register_route(User, 'user_info', '/user/info')
