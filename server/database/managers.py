import m4m_sync

from sqlalchemy.exc import InternalError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import func

from server.database.models import (
	Object,
	Controller,
	Sensor,
	User,
	UserInfo,
	UserSocialTokens,
)

from server.errors import (
	ConflictError,
	ObjectNotFoundError,
	ObjectExistsError,
	UserNoAccessError,
)
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
		except IntegrityError:
			raise ObjectExistsError(object='Record', property='Property')
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

	def delete(self, id_):
		self.session.query(self.model).filter_by(id=id_).delete()


class ObjectManager(BaseSqlManager):
	model = Object

	def get_all_for_user(self, user_id: int):
		return self.session.query(self.model) \
			.filter_by(user_id=user_id) \
			.options(joinedload(Object.controllers).joinedload(Controller.sensors)) \
			.all()

	def get_by_id_for_user(self, object_id: int, user_id: int):
		return self.session.query(self.model) \
			.filter_by(user_id=user_id) \
			.filter_by(id=object_id) \
			.one()

	def update_for_user(self, object_id: int, user_id: int, data: dict):
		return self.session.query(self.model) \
			.filter_by(id=object_id) \
			.filter_by(user_id=user_id) \
			.update(data)

	def delete_for_user(self, object_id: int, user_id: int):
		return self.session.query(self.model) \
			.filter_by(id=object_id) \
			.filter_by(user_id=user_id) \
			.delete()


class ControllerManager(BaseSqlManager):
	model = Controller

	def get_for_user(self, controller_id: int, user_id: int):
		return self.session.query(self.model) \
			.join(Controller.object) \
			.filter_by(id=controller_id) \
			.filter_by(user_id=user_id).one()

	def create_for_user(self, user_id: int, data: dict):
		object_id = data['object_id']
		can_access = self.session.query(func.count(Object.id)) \
			.filter_by(id=object_id) \
			.filter_by(user_id=user_id)

		if can_access == 0:
			raise UserNoAccessError()

		return self.create(data)

	def __can_access(self, controller_id: int, user_id: int):
		return self.session.query(func.count(self.model.id)) \
				   .join(Controller.object) \
				   .filter_by(id=controller_id) \
				   .filter_by(user_id=user_id) != 0

	def delete_for_user(self, controller_id: int, user_id: int):
		if not self.__can_access(controller_id, user_id):
			raise UserNoAccessError()

		self.session.query(self.model) \
			.filter_by(id=controller_id) \
			.delete()

	def update_for_user(self, controller_id: int, user_id: int, data: dict):
		can_access = self.session.query(func.count(self.model.id)) \
						 .join(self.model.object) \
						 .filter(self.model.id == controller_id) \
						 .filter_by(user_id=user_id) != 0

		if not self.__can_access(controller_id, user_id) or not can_access:
			raise UserNoAccessError()

		return self.session.query(self.model) \
			.filter_by(id=controller_id) \
			.update(data)


class SensorManager(BaseSqlManager):
	model = Sensor

	default_names = {
		5: 'OBD',
		6: 'GPS',
	}

	def create_or_update(self, _id: str, data: dict):
		query = self.session.query(self.model).filter_by(id=_id)
		if query.scalar():
			query.update(data)
		else:
			name = data.pop('name', self.default_names[data['sensor_type']])
			self.session.add(
				Sensor(
					id=_id,
					name=name,
					activation_date=datetime.now(),
					controller_id=1,
					**data,
				),
			)

	def create_for_user(self, user_id: int, data: dict):
		controller_id = data['controller_id']
		can_access = self.session.query(func.count(Controller.id)) \
						 .join(Controller.object) \
						 .filter(Controller.id == controller_id) \
						 .filter(Object.user_id == user_id) != 0

		if not can_access:
			raise UserNoAccessError()

		return self.create(data)

	def __can_access(self, sensor_id: str, user_id: int):
		return self.session.query(func.count(self.model.id)) \
				   .join(self.model.controller) \
				   .join(Controller.object) \
				   .filter(self.model.id == sensor_id) \
				   .filter(Object.user_id == user_id) != 0

	def get_for_user(self, sensor_id: str, user_id: int):
		return self.session.query(self.model) \
			.join(self.model.controller) \
			.join(Controller.object) \
			.filter(self.model.id == sensor_id) \
			.filter(Object.user_id == user_id) \
			.one()

	def delete_for_user(self, sensor_id: str, user_id: int):
		if not self.__can_access(sensor_id, user_id):
			raise UserNoAccessError()

		return self.session.query(self.model) \
			.filter_by(id=sensor_id) \
			.delete()

	def update_for_user(self, sensor_id: str, user_id: int, data: dict):
		can_access = self.session.query(func.count(self.model.id)) \
						 .join(self.model.controller) \
						 .join(Controller.object) \
						 .filter(self.model.id == sensor_id) \
						 .filter(Object.user_id == user_id) != 0

		if not self.__can_access(sensor_id, user_id) or not can_access:
			raise UserNoAccessError()

		return self.session.query(self.model) \
			.filter_by(id=sensor_id) \
			.update(data)


class UserManager(BaseSqlManager):
	model = User

	def save_new(self, login, pwd_hash):
		user = self.create({
			'login': login,
			'pwd_hash': pwd_hash,
		})

		UserInfoManager(self.session).create({
			'user_id': user.id
		})

		UserSocialTokensManager(self.session).create({
			'user_id': user.id
		})

		ObjectManager(self.session).create({
			'name': 'default',
			'user_id': user.id,
		})

		return user

	def get_by_login(self, login):
		try:
			return self.session.query(self.model).filter_by(login=login).one()
		except NoResultFound:
			raise ObjectNotFoundError(object='User')


class UserInfoManager(BaseSqlManager):
	model = UserInfo

	def get_by_user_id(self, user_id):
		try:
			return self.session.query(self.model).filter_by(user_id=user_id).one()
		except NoResultFound:
			raise ObjectNotFoundError(object='user_info')

	def get_all(self, with_login=False):
		return self.session.query(self.model).options(joinedload(UserInfo.user)).all()

	def update(self, user_id, info):
		return self.session.query(self.model).filter_by(user_id=user_id).update(info)


class UserSocialTokensManager(BaseSqlManager):
	model = UserSocialTokens

	def get_by_user_id(self, user_id: int) -> UserInfo:
		return self.session.query(self.model).filter_by(user_id=user_id).one()

	def update(self, user_id: int, data: dict):
		return self.session.query(self.model).filter_by(user_id=user_id).update(data)

	def sync_user(self, user_token: UserSocialTokens):
		if user_token.yandex_disk:
			store = m4m_sync.YaDiskStore(token=user_token.yandex_disk)
			self.__sync(user_token.user_id, store)
		else:
			controllers = self.session.query(Controller) \
				.options(joinedload(Controller.sensors)) \
				.filter(Object.user_id == user_token.user_id) \
				.all()
			for controller in controllers:
				for sensor in controller.sensors:
					self.session.delete(sensor)
				self.session.delete(controller)

	def __sync(self, user_id: int, store: m4m_sync.stores.BaseStore):
		remote_controllers = store.get_controllers()
		local_controllers = self.session.query(Controller) \
			.options(joinedload(Controller.object), joinedload(Controller.sensors)) \
			.filter(Object.user_id == user_id) \
			.all()

		local_controllers_macs = [local_controller.mac for local_controller in local_controllers]
		remote_controllers_macs = [remote_controller.mac for remote_controller in remote_controllers]

		for local_controller in local_controllers:
			if local_controller.mac not in remote_controllers_macs:
				for local_sensor in local_controller.sensors:
					self.session.delete(local_sensor)
				self.session.delete(local_controller)

		for remote_controller in remote_controllers:
			if remote_controller.mac in local_controllers_macs:
				local_controller = next(filter(lambda x: x.mac == remote_controller.mac, local_controllers))
				if local_controller.name != remote_controller.name:
					local_controller.name = remote_controller.name
			else:
				object_id, = self.session.query(Object.id).filter_by(user_id=user_id).first()
				local_controller = Controller(
					name=remote_controller.name,
					mac=remote_controller.mac,
					object_id=object_id,
				)
				self.session.add(local_controller)

			remote_sensors = store.get_sensors(remote_controller)
			local_sensors = self.session.query(Sensor).filter_by(controller_id=local_controller.id)

			local_sensor_ids = [local_sensor.id for local_sensor in local_sensors]
			remote_sensor_ids = [remote_sensor.id for remote_sensor in remote_sensors]

			for local_sensor in local_sensors:
				if local_sensor.id not in remote_sensor_ids:
					self.session.delete(local_sensor)

			for remote_sensor in remote_sensors:
				if remote_sensor.id in local_sensor_ids:
					local_sensor = next(filter(lambda x: x.id == remote_sensor.id, local_sensors))
					if local_sensor.name != remote_sensor.name:
						local_sensor.name = remote_sensor.name
				else:
					local_sensor = Sensor(
						name=remote_sensor.name,
						id=remote_sensor.id,
						controller_id=local_controller.id,
					)
					self.session.add(local_sensor)
