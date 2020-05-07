from sqlalchemy.exc import InternalError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

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
	ObjectExistsError
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


class ObjectManager(BaseSqlManager):
	model = Object


class ControllerManager(BaseSqlManager):
	model = Controller


class SensorManager(BaseSqlManager):
	model = Sensor

	default_names = {
		5: 'OBD',
		6: 'GPS',
	}

	def create_or_update(self, id, data):
		query = self.session.query(self.model).filter_by(id=id)
		if query.scalar():
			query.update(data)
		else:
			name = data.pop('name', self.default_names[data['sensor_type']])
			self.session.add(
				Sensor(
					id=id,
					name=name,
					activation_date=datetime.now(),
					controller_id=1,
					**data,
				),
			)


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
