import bcrypt
from flask import request
from flask_jwt_extended import jwt_required, create_access_token

from server.resources.base import BaseResource
from server.database.schemas import (
	SensorDataSchema,
	ResourceSchema,
	RegisterSchema,
	AuthSchema,
	UserInfoSchema,
	UserListSchema,
)

from server.resources.utils import (
	provide_db_session,
	schematic_response,
	schematic_request,
	safe_handler,
	with_user_id
)

from server.database.managers import (
	SensorManager,
	SensorDataManager,
	ObjectManager,
	ControllerManager,
	UserManager,
	UserInfoManager,
)

from server.validation.schema import (
	RegisterRequestSchema,
	AuthRequestSchema,
	UserInfoRequestSchema,
)

from server.errors import InvalidArgumentError


class Registration(BaseResource):
	@safe_handler
	@provide_db_session
	@schematic_request(RegisterRequestSchema())
	@schematic_response(RegisterSchema())
	def post(self, request_obj=None):
		login = request_obj['login']
		pwd = request_obj['password'].encode('utf-8')

		pwd_hash = bcrypt.hashpw(pwd, bcrypt.gensalt()).decode('utf-8')

		user = UserManager(self.db_session).save_new(login, pwd_hash)
		UserInfoManager(self.db_session).save_new(user.id)

		return {'token': create_access_token(identity={'email': login, 'id': user.id})}, 201


class Auth(BaseResource):
	@safe_handler
	@provide_db_session
	@schematic_request(AuthRequestSchema())
	@schematic_response(AuthSchema())
	def post(self, request_obj=None):
		login = request_obj['login']
		pwd = request_obj['password'].encode('utf-8')

		user = UserManager(self.db_session).get_by_login(login)

		if bcrypt.checkpw(pwd, user.pwd_hash.encode('utf-8')):
			return {'token': create_access_token(identity={'email': login, 'id': user.id})}

		raise InvalidArgumentError(message='invalid password')


class User(BaseResource):
	@safe_handler
	@jwt_required
	@provide_db_session
	@schematic_response(UserInfoSchema())
	@with_user_id()
	def get(self, user_id=None):
		return UserInfoManager(self.db_session).get_by_user_id(user_id)

	@safe_handler
	@jwt_required
	@provide_db_session
	@schematic_request(UserInfoRequestSchema())
	@schematic_response(UserInfoSchema())
	@with_user_id(True)
	def patch(self, user_id=None, request_obj=None):
		return UserInfoManager(self.db_session).update(user_id, request_obj)


class Users(BaseResource):
	@safe_handler
	@provide_db_session
	@schematic_response(UserListSchema())
	def get(self):
		return UserInfoManager(self.db_session).get_all()


class ObjectsResource(BaseResource):
	def _insert_last_value(self, sensors):
		data_manager = SensorDataManager(self.db_session)

		for sensor in sensors:
			last_value = data_manager.get_last_record(sensor.id)
			sensor.last_value = last_value and last_value['value']

	@safe_handler
	@jwt_required
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
	@safe_handler
	@jwt_required
	@provide_db_session
	@schematic_response(SensorDataSchema(many=True))
	def get(self, sensor_id):
		result = SensorDataManager(self.db_session)\
			.get_sensor_data(sensor_id, request.args.get('from'), request.args.get('field'))

		return result


class AllObjectsInfoResource(BaseResource):
	@safe_handler
	@jwt_required
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


class SensorDataPrivateResource(BaseResource):
	@safe_handler
	@jwt_required
	@provide_db_session
	@schematic_response(SensorDataSchema())
	def post(self, sensor_id):
		return SensorDataManager(self.db_session).save_new(sensor_id, request.json['sensor_data'])


def register_routes(app):
	app.register_route(Auth, 'sign_in', '/sign_in')
	app.register_route(Registration, 'sign_up', '/sign_up')
	app.register_route(ObjectsResource, 'objects', '/objects')
	app.register_route(SensorDataResource, 'sensor_data', '/sensor/<int:sensor_id>/data')
	app.register_route(SensorDataResource, 'sensor_data_private', '/private/sensor/<int:sensor_id>/data/add')
	app.register_route(User, 'user_info', '/user/info/<int:user_id>')
	app.register_route(User, 'user_info_self', '/user/info')
	app.register_route(Users, 'users_list', '/user/list')
