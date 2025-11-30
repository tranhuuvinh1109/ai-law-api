from marshmallow import Schema, fields

class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    slug = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
