import base64

from marshmallow import Schema, fields


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


class SensorDataRecordSchema(Schema):
    time_stamp = fields.String(attribute='timestamp')
    value = fields.Dict()


class SensorDataSchema(Schema):
    data = fields.Nested(SensorDataRecordSchema)
    signer = Base64Field()
    sign = Base64Field()


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
