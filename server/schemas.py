import base64

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
    name = fields.String()
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


class UserBriefSchema(Schema):
    login = fields.String()


class UserBriefInfoSchema(Schema):
    user_id = fields.Integer()
    user = fields.Nested(UserBriefSchema)
    name = fields.String()


class UserSocialTokensSchema(Schema):
    yandex_disk = fields.String()


class Base64Field(fields.Field):
    _encoding = 'utf-8'

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        return str(base64.b64encode(value), encoding=self._encoding)

    def _deserialize(self, value, attr, data):
        if value is None:
            return None
        return base64.b64decode(value)


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
    id = fields.String()
    name = fields.String()
    status = fields.Integer()
    type = fields.Integer(attribute='sensor_type')
    controller = fields.Integer(attribute='controller_id')


class ResourceSchema(Schema):
    objects = fields.Nested(ObjectSchema, many=True)
    controllers = fields.Nested(ControllerSchema, many=True)
    sensors = fields.Nested(SensorSchema(), many=True)
