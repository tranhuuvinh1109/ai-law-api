# from marshmallow import Schema, fields
# from app.schemas.procedure_step_schema import ProcedureStepSchema
# from app.schemas.procedure_document_schema import ProcedureDocumentSchema
# from app.schemas.category_schema import CategorySchema
# from app.schemas.procedure_schema import ProcedureSchema

# class ProcedureDetailSchema(ProcedureSchema):
#     steps = fields.List(fields.Nested(ProcedureStepSchema))
#     documents = fields.List(fields.Nested(ProcedureDocumentSchema))
#     category = fields.Nested(CategorySchema)