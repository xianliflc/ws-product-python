from marshmallow import Schema, fields, EXCLUDE

class StatsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    start_date = fields.String(required=True)
    end_date = fields.String(required=True)
    page_number = fields.Integer(required=False)
    page_size = fields.Integer(required=False)
