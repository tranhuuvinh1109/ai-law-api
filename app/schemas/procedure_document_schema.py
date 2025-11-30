from marshmallow import Schema, fields

class ProcedureDocumentSchema(Schema):
    id = fields.Int()
    procedure_id = fields.Int()

    name = fields.Str()
    description = fields.Str()
    required = fields.Bool()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
