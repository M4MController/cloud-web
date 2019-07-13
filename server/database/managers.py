from sqlalchemy.exc import InternalError
from sqlalchemy.orm.exc import NoResultFound

from server.database.models import (
	Object,
	Controller,
	Sensor,
	SensorData)

from server.errors import ConflictError, ObjectNotFoundError


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
		return self.create({sensor_id: sensor_id, data: data})

	def get_sensor_data(self, sensor_id):
		return self.session.query(self.model)\
			.select(columns=[self.model.sensor_type])\
			.filter(self.model.sensor_type == sensor_id)

	def get_last_record(self, sensor_id):
		return self.session.query(self.model)\
			.select(columns=[self.model.sensor_type])\
			.filter(self.model.sensor_type == sensor_id)\
			.order_by(self.model.data['_id'].desc())[1]

# class SensorDataManager:
# 	def __init__(self, database):
# 		self._database = database
#
# 	def save_new(self, sensor_id, data):
# 		return self._database['sensor_{}'.format(sensor_id)].insert_one(data)
#
# 	def get_all(self, sensor_id):
# 		return self._database['sensor_{}'.format(sensor_id)].find()
#
# 	def get_last_record(self, sensor_id):
# 		return self._database['sensor_{}'.format(sensor_id)].find_one({}, sort=[('_id', DESCENDING)])
