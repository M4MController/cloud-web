from datetime import datetime

from flask import request

import m4m_sync
from m4m_sync import AesStreamWrapper
from m4m_sync.utils import StreamWrapper

from marshmallow import Schema, fields
from sqlalchemy.orm import joinedload

from server.database.models import Sensor, Controller, Object, User
from server.resources.base import BaseResource
from server.resources.utils import provide_db_session, schematic_response


class SensorsResource(BaseResource):
    class Response(Schema):
        email = fields.String()
        sensor_id = fields.String()

    @provide_db_session
    @schematic_response(Response(many=True))
    def get(self):
        rows = self.db_session.query(Sensor, User.login) \
            .options(joinedload(Sensor.controller).joinedload(Controller.object).joinedload(Object.user)) \
            .all()

        return [{'sensor_id': data[0].id, 'email': data[1]} for data in rows]


class SensorsDataResource(BaseResource):
    @provide_db_session
    def get(self, sensor_id: str, year: int, month: int, day: int):
        key = request.args.get('key')

        data = self.db_session.query(Sensor)\
            .options(
            joinedload(Sensor.controller)
                .joinedload(Controller.object)
                .joinedload(Object.user)
                .joinedload(User.social_tokens),
        ).filter(Sensor.id == sensor_id).all()

        if not len(data):
            return 404

        sensor = data[0]
        token = sensor.controller.object.user.social_tokens.yandex_disk
        if not token:
            return 403

        store = m4m_sync.YaDiskStore(token=token)
        data = store.get(
            m4m_sync.stores.Sensor(id=sensor_id, controller=m4m_sync.stores.Controller(mac=sensor.controller.mac)),
            stream_wrapper=AesStreamWrapper(key=key) if key else StreamWrapper(),
            range=m4m_sync.stores.DateTimeRange.day(datetime(year=year, month=month, day=day))
        )

        if not len(data):
            return '', 404
        return data[0], 200


def register_routes(app):
    app.register_route(SensorsResource, 'admin_sensors', '/admin/sensors')
    app.register_route(SensorsDataResource, 'admin_sensors_data', '/admin/sensors/<string:sensor_id>/<int:year>/<int:month>/<int:day>')
