from marshmallow import Schema, fields, EXCLUDE


class TodoCreationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True)
    description = fields.String(required=True)
    due = fields.DateTime(format='%Y-%m-%d %H:%M:%S', required=True)
    status_id = fields.Integer(required=True)


class TodoUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=False)
    description = fields.String(required=False)
    due = fields.DateTime(format='%Y-%m-%d %H:%M:%S', required=False)
    status_id = fields.Integer(required=False)
