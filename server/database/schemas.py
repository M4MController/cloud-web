from marshmallow import Schema, fields


class BaseAuthSchema(Schema):
    token = fields.String()


class RegisterSchema(BaseAuthSchema):
    pass


class AuthSchema(BaseAuthSchema):
    pass


class UserInfoSchema(Schema):
    id = fields.Integer()
    family_name = fields.String()
    name = fields.String(attribute='username')
    second_name = fields.String()
    date_receiving = fields.Integer()
    issued_by = fields.String()
    division_number = fields.String()
    registration_addres = fields.String()
    mailing_addres = fields.String()
    birth_day = fields.String()
    sex = fields.Boolean()
    home_phone = fields.String()
    mobile_phone = fields.String()
    citizenship = fields.String()
    e_mail = fields.String()


class UserBriefInfoSchema(Schema):
    id = fields.Integer()
    email = fields.String()


class UserListSchema(Schema):
    users = fields.Nested(UserBriefInfoSchema, many=True)


class SensorDataSchema(Schema):
    time_stamp = fields.String(attribute='timestamp')
    value = fields.Dict()


class ObjectSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class ControllerSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    object = fields.Integer(attribute='object_id')
    meta = fields.String()
    activation_date = fields.Date()
    status = fields.Integer()
    mac = fields.String()
    deactivation_date = fields.String()
    controller_type = fields.Integer()


class SensorSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    status = fields.Integer()
    last_value = fields.Dict(allow_none=True)
    type = fields.Integer(attribute='sensor_type')
    controller = fields.Integer(attribute='controller_id')


class ResourceSchema(Schema):
    objects = fields.Nested(ObjectSchema, many=True)
    controllers = fields.Nested(ControllerSchema, many=True)
    sensors = fields.Nested(SensorSchema(), many=True)
