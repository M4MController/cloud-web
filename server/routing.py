import bcrypt
import itertools
from flask_jwt_extended import create_access_token

from server.resources.base import BaseResource
from server.schemas import (
	ResourceSchema,
	RegisterSchema,
	AuthSchema,
	UserInfoSchema,
	UserSocialTokensSchema,
	ObjectSchema,
	ControllerSchema,
	SensorSchema,
)

from server.resources.utils import (
	provide_db_session,
	schematic_response,
	schematic_request,
	with_user_id,
	authorized,
)

from server.database.managers import (
	ObjectManager,
	ControllerManager,
	SensorManager,
	UserManager,
	UserInfoManager,
	UserSocialTokensManager,
)

from server.validation.schema import (
	RegisterRequestSchema,
	AuthRequestSchema,
	UserInfoRequestSchema,
	ObjectRequestSchema,
	ControllerRequestSchema,
	SensorRequestSchema,
)

from server.errors import InvalidArgumentError


class Registration(BaseResource):
	@provide_db_session
	@schematic_request(RegisterRequestSchema())
	@schematic_response(RegisterSchema())
	def post(self, request_obj=None):
		login = request_obj['login']
		pwd = request_obj['password'].encode('utf-8')

		pwd_hash = bcrypt.hashpw(pwd, bcrypt.gensalt()).decode('utf-8')

		user = UserManager(self.db_session).save_new(login, pwd_hash)

		return {'token': create_access_token(identity={'email': login, 'id': user.id})}, 201


class Auth(BaseResource):
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
	@authorized
	@provide_db_session
	@schematic_response(UserInfoSchema())
	@with_user_id()
	def get(self, user_id=None):
		return UserInfoManager(self.db_session).get_by_user_id(user_id)

	@authorized
	@provide_db_session
	@schematic_request(UserInfoRequestSchema())
	@schematic_response(UserInfoSchema())
	@with_user_id(True)
	def patch(self, user_id=None, request_obj=None):
		return UserInfoManager(self.db_session).update(user_id, request_obj)


class UserTokens(BaseResource):
	@authorized
	@provide_db_session
	@schematic_response(UserSocialTokensSchema())
	@with_user_id()
	def get(self, user_id=None):
		return UserSocialTokensManager(self.db_session).get_by_user_id(user_id)

	@authorized
	@provide_db_session
	@schematic_request(UserSocialTokensSchema())
	@schematic_response(UserSocialTokensSchema())
	@with_user_id(True)
	def patch(self, user_id=None, request_obj=None):
		return UserSocialTokensManager(self.db_session).update(user_id, request_obj)


class ObjectsResource(BaseResource):
	@authorized
	@provide_db_session
	@schematic_response(ResourceSchema())
	@with_user_id(True)
	def get(self, user_id=None):
		objects = ObjectManager(self.db_session).get_all_for_user(user_id)
		controllers = list(itertools.chain(*[obj.controllers for obj in objects]))
		sensors = list(itertools.chain(*[ctrlr.sensors for ctrlr in controllers]))

		return {
			'objects': objects,
			'controllers': controllers,
			'sensors': sensors,
		}


class ObjectCResource(BaseResource):
	@authorized
	@provide_db_session
	@schematic_response(ObjectSchema())
	@schematic_request(ObjectRequestSchema())
	@with_user_id(True)
	def post(self, user_id=None, request_obj=None):
		return ObjectManager(self.db_session).create({
			'name': request_obj['name'],
			'user_id': user_id,
		})


class ObjectRUDResource(BaseResource):
	@authorized
	@provide_db_session
	@with_user_id(True)
	def delete(self, object_id, user_id=None):
		ObjectManager(self.db_session).delete_for_user(object_id, user_id)

		return 200

	@authorized
	@provide_db_session
	@schematic_response(ObjectSchema())
	@with_user_id(True)
	def get(self, object_id, user_id=None):
		return ObjectManager(self.db_session).get_by_id_for_user(object_id, user_id)

	@authorized
	@provide_db_session
	@schematic_response(ObjectSchema())
	@schematic_request(ObjectSchema())
	@with_user_id(True)
	def patch(self, object_id, user_id=None, request_obj=None):
		return ObjectManager(self.db_session).update_for_user(object_id, user_id, request_obj)


class ControllerCResource(BaseResource):
	@authorized
	@provide_db_session
	@schematic_request(ControllerRequestSchema())
	@schematic_response(ControllerSchema())
	@with_user_id(True)
	def post(self, user_id=None, request_obj=None):
		return ControllerManager(self.db_session).create_for_user(user_id, request_obj)


class ControllerRUDResource(BaseResource):
	@authorized
	@provide_db_session
	@with_user_id(True)
	def delete(self, controller_id, user_id=None):
		ControllerManager(self.db_session).delete_for_user(controller_id, user_id)

		return 200

	@authorized
	@provide_db_session
	@schematic_response(ControllerSchema())
	@with_user_id(True)
	def get(self, controller_id, user_id=None):
		return ControllerManager(self.db_session).get_for_user(controller_id, user_id)

	@authorized
	@provide_db_session
	@schematic_request(ControllerRequestSchema())
	@with_user_id(True)
	def patch(self, controller_id, user_id=None, request_obj=None):
		ControllerManager(self.db_session).update_for_user(controller_id, user_id, request_obj)

		return 200


class SensorCResource(BaseResource):
	@authorized
	@provide_db_session
	@schematic_request(SensorRequestSchema())
	@schematic_response(SensorSchema())
	@with_user_id(True)
	def post(self, user_id=None, request_obj=None):
		return SensorManager(self.db_session).create_for_user(user_id, request_obj)


class SensorRUDResource(BaseResource):
	@authorized
	@provide_db_session
	@with_user_id(True)
	def delete(self, sensor_id, user_id=None):
		SensorManager(self.db_session).delete_for_user(sensor_id, user_id)

		return 200

	@authorized
	@provide_db_session
	@schematic_response(SensorSchema())
	@with_user_id(True)
	def get(self, sensor_id, user_id=None):
		return SensorManager(self.db_session).get_for_user(sensor_id, user_id)

	@authorized
	@provide_db_session
	@schematic_request(SensorRequestSchema())
	@with_user_id(True)
	def patch(self, sensor_id, user_id=None, request_obj=None):
		SensorManager(self.db_session).update_for_user(sensor_id, user_id, request_obj)

		return 200


def register_routes(app):
	app.register_route(Auth, 'sign_in', '/sign_in')
	app.register_route(Registration, 'sign_up', '/sign_up')
	app.register_route(ObjectsResource, 'objects', '/objects')
	app.register_route(ObjectCResource, 'create_object', '/object')
	app.register_route(ObjectRUDResource, 'retrieve_update_delete_object', '/object/<int:object_id>')
	app.register_route(ControllerCResource, 'create_controller', '/controller')
	app.register_route(ControllerRUDResource, 'retrieve_update_delete_controller', '/controller/<int:controller_id>')
	app.register_route(SensorCResource, 'create_sensor', '/sensor')
	app.register_route(SensorRUDResource, 'retrieve_update_delete_sensor', '/sensor/<int:sensor_id')
	app.register_route(User, 'user_info_self', '/user/info')
	app.register_route(UserTokens, 'user_social_tokens', '/user_social_tokens')
