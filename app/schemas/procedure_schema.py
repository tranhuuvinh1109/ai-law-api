from marshmallow import Schema, fields
from app.schemas.procedure_step_schema import ProcedureStepSchema
from app.schemas.procedure_document_schema import ProcedureDocumentSchema
from app.schemas.category_schema import CategorySchema

class ProcedureSchema(Schema):
    id = fields.Int(dump_only=True)
    category_id = fields.Int(required=True)

    title = fields.Str(required=True)
    short_description = fields.Str()
    long_description = fields.Str()

    level_of_authority = fields.Str()
    process_time = fields.Str()

    fee_min = fields.Float()
    fee_max = fields.Float()

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
class ProcedureDetailSchema(ProcedureSchema):
    steps = fields.List(fields.Nested(ProcedureStepSchema))
    documents = fields.List(fields.Nested(ProcedureDocumentSchema))
    category = fields.Nested(CategorySchema)


class ProcedureCreateSchema(Schema):
    id = fields.Int()
    category_id = fields.Int(required=True)
    category = fields.Nested(CategorySchema, required=False)

    title = fields.Str(required=True)
    short_description = fields.Str()
    long_description = fields.Str()

    level_of_authority = fields.Str()
    process_time = fields.Str()

    fee_min = fields.Float()
    fee_max = fields.Float()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    steps = fields.List(fields.Nested(ProcedureStepSchema), required=False)
    documents = fields.List(fields.Nested(ProcedureDocumentSchema), required=False)