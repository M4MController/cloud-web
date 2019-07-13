from marshmallow import Schema, fields


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
    type = fields.Integer()
    controller = fields.Integer(attribute='controller_id')


class SensorDataSchema(Schema):
    id = fields.Integer()
    sensor_type = fields.Integer()
    data = fields.Dict()


class ResourceSchema(Schema):
    objects = fields.Nested(ObjectSchema, many=True)
    controllers = fields.Nested(ControllerSchema, many=True)
    sensors = fields.Nested(SensorSchema(), many=True)
