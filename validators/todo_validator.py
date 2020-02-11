from marshmallow import Schema, fields, EXCLUDE


class TodoCreationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True)
    description = fields.String(required=True)
    due = fields.DateTime(format='YYYY-MM-DD HH:MM:SS', required=True)
    status_id = fields.Integer(required=True)
