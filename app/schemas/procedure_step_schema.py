from marshmallow import Schema, fields

class ProcedureStepSchema(Schema):
    id = fields.Int()
    procedure_id = fields.Int()

    step_number = fields.Int()
    title = fields.Str()
    description = fields.Str()
    time_estimation = fields.Str()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
