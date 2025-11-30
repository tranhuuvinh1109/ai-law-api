from flask.views import MethodView
from flask_smorest import Blueprint
from app.db import db
from app.models.procedure_documents_model import ProcedureDocumentModel
from app.schemas.procedure_document_schema import ProcedureDocumentSchema

blp = Blueprint("procedure_document", __name__, description="Documents API")


@blp.route("/procedures/<int:procedure_id>/documents")
class DocumentList(MethodView):
    @blp.response(200, ProcedureDocumentSchema(many=True))
    def get(self, procedure_id):
        return ProcedureDocumentModel.query.filter_by(procedure_id=procedure_id).all()

    @blp.arguments(ProcedureDocumentSchema)
    @blp.response(201, ProcedureDocumentSchema)
    def post(self, data, procedure_id):
        document = ProcedureDocumentModel(procedure_id=procedure_id, **data)
        db.session.add(document)
        db.session.commit()
        return document


@blp.route("/documents/<int:id>")
class DocumentDetail(MethodView):
    @blp.response(200, ProcedureDocumentSchema)
    def get(self, id):
        return ProcedureDocumentModel.query.get_or_404(id)

    @blp.arguments(ProcedureDocumentSchema)
    @blp.response(200, ProcedureDocumentSchema)
    def put(self, data, id):
        doc = ProcedureDocumentModel.query.get_or_404(id)
        for key, val in data.items():
            setattr(doc, key, val)
        db.session.commit()
        return doc

    def delete(self, id):
        doc = ProcedureDocumentModel.query.get_or_404(id)
        db.session.delete(doc)
        db.session.commit()
        return {"message": "Deleted"}
