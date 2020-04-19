import json
import logging

from flask import make_response, request
from flask_jwt_extended import get_jwt_identity
from jwt.exceptions import ExpiredSignatureError

from server.errors import (
    BaseApiError,
    InternalServerError,
    ValidationFailedError,
    UnsupportedMediaTypeError,
)

logger = logging.getLogger(__name__)


def provide_db_session(func):
    # https://docs.sqlalchemy.org/en/rel_1_2/orm/contextual.html#using-thread-local-scope-with-web-applications
    def f(self, *args, **kwargs):
        self.db_session()
        try:
            result = func(self, *args, **kwargs)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e
        finally:
            self.db_session.remove()
        return result

    return f


def safe_handler(func):
    def f(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.exception(str(e))

            if isinstance(e, ExpiredSignatureError):
                return self._flask.redirect('/sign_in', 307)

            if not isinstance(e, BaseApiError):
                e = InternalServerError()

            result = e.to_dict()
            headers = {'Content-Type': 'application/json'}

            return make_response(
                json.dumps(result),
                result['status'],
                headers,
            )

    return f


def schematic_response(schema):
    def decor(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if not isinstance(result, tuple):
                result = (result, 200)

            result, code = result

            return make_response(
                schema.dumps(result).data,
                code,
                {'Content-Type': 'application/json'},
            )

        return wrapper

    return decor


def schematic_request(schema):
    def decor(func):
        def wrapper(*args, **kwargs):
            obj_dict = request.json
            if obj_dict is None:
                raise UnsupportedMediaTypeError(supported='application/json')
            load_result = schema.load(obj_dict)
            if load_result.errors:
                raise ValidationFailedError(load_result.errors)
            return func(*args, **kwargs, request_obj=load_result.data)

        return wrapper

    return decor


def with_user_id(force_override=False):
    def decor(func):
        def wrapper(*args, **kwargs):
            if force_override or 'user_id' not in kwargs or kwargs['user_id'] is None:
                kwargs['user_id'] = get_jwt_identity()['id']

            return func(*args, **kwargs)

        return wrapper

    return decor
