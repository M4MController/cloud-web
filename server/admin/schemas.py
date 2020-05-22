from marshmallow import Schema, fields

from server.schemas import BaseWithNameSchema


class UserResponse(Schema):
	id = fields.Integer(attribute='user_id')
	first_name = fields.String()
	last_name = fields.String()


class SensorResponse(Schema):
	email = fields.String()
	name = fields.String()
	sensor_id = fields.String()


class CompanyResponse(BaseWithNameSchema):
	pass
