from marshmallow import Schema, fields


class BaseAuthSchema(Schema):
	login = fields.String()
	password = fields.String()


class RegisterRequestSchema(BaseAuthSchema):
	pass


class AuthRequestSchema(BaseAuthSchema):
	pass
