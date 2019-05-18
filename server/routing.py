from server.config import config
from server.resources.base import BaseResource
from marshmallow import Schema, fields

from server.resources.utils import provide_db_session, schematic_response

from server.database.managers import SensorManager, SensorDataManager


class SensorDataSchema(Schema):
    time_stamp = fields.DateTime(attribute='timestamp')
    value = fields.Dict()


class SensorSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    status = fields.Integer()
    last_value = fields.Dict(allow_none=True)
    type = fields.Integer()
    controller = fields.Integer(attribute='controller_id')


class ResourceSchema(Schema):
    sensors = fields.Nested(SensorSchema(), many=True)


class Auth(BaseResource):
    def post(self):
        return {'token': config['user_token']}


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
        self._insert_last_value(sensors)

        return {
            'sensors': sensors,
        }


class SensorDataResource(BaseResource):
    @schematic_response(SensorDataSchema(many=True))
    def get(self, sensor_id):
        return SensorDataManager(self.db_data).get_all(sensor_id)


def register_routes(app):
    app.register_route(Auth, 'sign_in', '/sign_in')
    app.register_route(ObjectsResource, 'objects', '/objects')
    app.register_route(SensorDataResource, 'sensor_data', '/sensor/<int:sensor_id>/data')
