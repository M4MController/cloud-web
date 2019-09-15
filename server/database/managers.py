from sqlalchemy.exc import InternalError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import DateTime

from server.database.models import (
    Object,
    Controller,
	  Sensor,
	  SensorData,
)

from server.errors import ConflictError, ObjectNotFoundError
from datetime import datetime

time_field = 'timestamp'


class BaseSqlManager:
    model = None

    def __init__(self, session):
        self.session = session

    def create(self, data):
        obj = self.model(**data)
        try:
            self.session.add(obj)
            self.session.flush()
        except InternalError:
            raise ConflictError()

        self.session.refresh(obj)
        return obj

    def get_all(self):
        return self.session.query(self.model).all()

    def get_by_id(self, id_):
        try:
            return self.session.query(self.model).filter_by(id=id_).one()
        except NoResultFound:
            raise ObjectNotFoundError(object='Record')


class ObjectManager(BaseSqlManager):
    model = Object


class ControllerManager(BaseSqlManager):
    model = Controller


class SensorManager(BaseSqlManager):
    model = Sensor


class SensorDataManager(BaseSqlManager):
    model = SensorData

    def save_new(self, sensor_id, data):
        now = datetime.now()
        s = SensorData(data={
            time_field: now.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            'value': data,
        }, sensor_id=sensor_id)
        self.session.add(s)
        self.session.commit()
        return s

    def get_sensor_data(self, sensor_id, time_from=None, field=None):
        query = self.session.query(self.model.data).filter(self.model.sensor_id == sensor_id)

        if time_from is not None:
            try:
                from_date = datetime.strptime(time_from, '%Y-%m-%dT%H:%M:%S')
                query = query.filter(self.model.data[time_field].astext.cast(DateTime) > from_date)
            except ValueError as error:
                print('from field has incorrect format: ', error, '; Expected: %Y-%m-%dT%H:%M:%S')

        if field is not None:
            if field == 'time_stamp':
                field = time_field

            query = query.with_entities(self.model.data[time_field], self.model.data['value'][field])

            if field == time_field:
                return [{time_field: x[0]} for x in query.all()]

            return [{time_field: x[0], 'value': {field: x[1]}} for x in query.all()]

        return [x[0] for x in query.all()]

    def get_last_record(self, sensor_id):
        return self.session.query(self.model.data) \
            .filter(self.model.sensor_id == sensor_id) \
            .order_by(self.model.id.desc()).first()[0]
