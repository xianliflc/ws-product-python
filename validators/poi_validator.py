from marshmallow import Schema, fields, EXCLUDE

class PoiEventsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    min_revenue = fields.Integer(required=False)
    max_revenue = fields.Integer(required=False)
    min_events = fields.Integer(required=False)
    max_events = fields.Integer(required=False)
    include = fields.String(required=False)
