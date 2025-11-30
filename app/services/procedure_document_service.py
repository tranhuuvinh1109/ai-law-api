from app.models.procedure_documents_model import ProcedureDocumentModel
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class ProcedureDocumentService:

    @staticmethod
    def get_all_by_procedure(procedure_id):
        return ProcedureDocumentModel.query.filter_by(procedure_id=procedure_id).all()

    @staticmethod
    def get_by_id(id):
        return ProcedureDocumentModel.query.get_or_404(id)

    @staticmethod
    def create(procedure_id, data):
        try:
            doc = ProcedureDocumentModel(procedure_id=procedure_id, **data)
            db.session.add(doc)
            db.session.commit()
            return doc
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update(id, data):
        doc = ProcedureDocumentModel.query.get_or_404(id)
        try:
            for key, value in data.items():
                setattr(doc, key, value)
            db.session.commit()
            return doc
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(id):
        doc = ProcedureDocumentModel.query.get_or_404(id)
        try:
            db.session.delete(doc)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
