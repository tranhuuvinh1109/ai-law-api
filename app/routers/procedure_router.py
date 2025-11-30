from flask.views import MethodView
from flask_smorest import Blueprint
from app.db import db
from app.models.procedure_documents_model import ProcedureDocumentModel
from app.schemas.procedure_document_schema import ProcedureDocumentSchema
from app.schemas.procedure_schema import ProcedureSchema, ProcedureCreateSchema, ProcedureDetailSchema
from app.services.procedure_service import ProcedureService

blp = Blueprint("ProcedureDocument", __name__, description="Documents API")

@blp.route("/procedures")
class ProcedureList(MethodView):

    @blp.response(200, ProcedureSchema(many=True))
    def get(self):
        return ProcedureService.get_all()

    @blp.arguments(ProcedureCreateSchema)
    @blp.response(201, ProcedureDetailSchema)
    def post(self, data):
        return ProcedureService.create_details(data)


@blp.route("/procedures/<int:id>")
class ProcedureDetail(MethodView):

    @blp.response(200, ProcedureDetailSchema)
    def get(self, id):
        return ProcedureService.get_by_id(id)

    @blp.arguments(ProcedureCreateSchema)
    @blp.response(200, ProcedureDetailSchema)
    def put(self, data, id):
        return ProcedureService.update(id, data)

    def delete(self, id):
        ProcedureService.delete(id)
        return {"message": "Deleted"}