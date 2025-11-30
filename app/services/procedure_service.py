from app.models.procedure_model import ProcedureModel
from app.models.procedure_steps_model import ProcedureStepModel
from app.models.procedure_documents_model import ProcedureDocumentModel
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class ProcedureService:

    @staticmethod
    def get_all():
        return ProcedureModel.query.all()

    @staticmethod
    def get_by_id(id):
        return ProcedureModel.query.get_or_404(id)

    @staticmethod
    def create(data):
        try:
            steps_data = data.pop("steps", [])
            documents_data = data.pop("documents", [])

            procedure = ProcedureModel(**data)
            db.session.add(procedure)
            db.session.commit()  # commit to get procedure.id

            # create steps
            for step in steps_data:
                new_step = ProcedureStepModel(
                    procedure_id=procedure.id,
                    step_number=step.get("step_number"),
                    title=step.get("title"),
                    description=step.get("description")
                )
                db.session.add(new_step)

            # create documents
            for doc in documents_data:
                new_doc = ProcedureDocumentModel(
                    procedure_id=procedure.id,
                    name=doc.get("name"),
                    description=doc.get("description"),
                    required=doc.get("required", False)
                )
                db.session.add(new_doc)

            db.session.commit()
            return procedure
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def create_details(data):
        try:
            return ProcedureService.create(data)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update(id, data):
        procedure = ProcedureModel.query.get_or_404(id)
        try:
            for key, value in data.items():
                setattr(procedure, key, value)

            procedure.updated_at = datetime.utcnow()
            db.session.commit()
            return procedure
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(id):
        procedure = ProcedureModel.query.get_or_404(id)
        try:
            db.session.delete(procedure)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
