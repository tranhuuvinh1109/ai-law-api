from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.models.procedure_model import ProcedureModel
from app.models.procedure_step_model import ProcedureStepModel
from app.models.procedure_documents_model import ProcedureDocumentModel


class ProcedureService:

    # =========================
    #        GET ALL
    # =========================
    @staticmethod
    def get_all():
        return ProcedureModel.query.all()

    # =========================
    #        GET BY ID
    # =========================
    @staticmethod
    def get_by_id(id):
        return ProcedureModel.query.get_or_404(id)

    # =========================
    #        CREATE
    # =========================
    @staticmethod
    def create(data):
        try:
            steps_data = data.pop("steps", [])
            documents_data = data.pop("documents", [])

            procedure = ProcedureModel(**data)
            db.session.add(procedure)
            db.session.commit()  # cần để lấy procedure.id

            # --- Create Steps ---
            for step in steps_data:
                new_step = ProcedureStepModel(
                    procedure_id=procedure.id,
                    step_number=step["step_number"],
                    title=step["title"],
                    description=step.get("description")
                )
                db.session.add(new_step)

            # --- Create Documents ---
            for doc in documents_data:
                new_doc = ProcedureDocumentModel(
                    procedure_id=procedure.id,
                    name=doc["name"],
                    description=doc.get("description"),
                    required=doc.get("required", False)
                )
                db.session.add(new_doc)

            db.session.commit()
            return procedure

        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    # =========================
    #  CREATE + RELATIONS
    # =========================
    @staticmethod
    def create_details(data):
        try:
            return ProcedureService.create(data)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    # =========================
    #        UPDATE
    # =========================
    @staticmethod
    def update(id, data):
        procedure = ProcedureModel.query.get_or_404(id)
        try:
            steps_data = data.pop("steps", None)
            documents_data = data.pop("documents", None)

            # update basic fields
            for key, value in data.items():
                setattr(procedure, key, value)

            procedure.updated_at = datetime.utcnow()

            # ============================
            #      UPDATE STEPS
            # ============================
            if steps_data is not None:
                ProcedureStepModel.query.filter_by(procedure_id=id).delete()

                for step in steps_data:
                    new_step = ProcedureStepModel(
                        procedure_id=id,
                        step_number=step["step_number"],
                        title=step["title"],
                        description=step.get("description")
                    )
                    db.session.add(new_step)

            # ============================
            #     UPDATE DOCUMENTS
            # ============================
            if documents_data is not None:
                ProcedureDocumentModel.query.filter_by(procedure_id=id).delete()

                for doc in documents_data:
                    new_doc = ProcedureDocumentModel(
                        procedure_id=id,
                        name=doc["name"],
                        description=doc.get("description"),
                        required=doc.get("required", False)
                    )
                    db.session.add(new_doc)

            db.session.commit()
            return procedure

        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    # =========================
    #        DELETE
    # =========================
    @staticmethod
    def delete(id):
        try:
            procedure = ProcedureModel.query.get_or_404(id)

            # Delete steps + documents before deleting procedure
            ProcedureStepModel.query.filter_by(procedure_id=id).delete()
            ProcedureDocumentModel.query.filter_by(procedure_id=id).delete()

            db.session.delete(procedure)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
