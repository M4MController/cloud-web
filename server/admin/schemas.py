from marshmallow import Schema, fields

from server.schemas import BaseWithNameSchema


class SensorResponse(Schema):
	email = fields.String()
	name = fields.String()
	sensor_id = fields.String()


class CompanyResponse(BaseWithNameSchema):
	pass
