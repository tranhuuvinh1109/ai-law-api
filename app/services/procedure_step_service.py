from app.models.procedure_step_model import ProcedureStepModel
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


class ProcedureStepService:

    @staticmethod
    def get_all_by_procedure(procedure_id):
        return ProcedureStepModel.query.filter_by(procedure_id=procedure_id).all()

    @staticmethod
    def get_by_id(id):
        return ProcedureStepModel.query.get_or_404(id)

    @staticmethod
    def create(procedure_id, data):
        try:
            step = ProcedureStepModel(procedure_id=procedure_id, **data)
            db.session.add(step)
            db.session.commit()
            return step
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update(id, data):
        step = ProcedureStepModel.query.get_or_404(id)
        try:
            for key, value in data.items():
                setattr(step, key, value)
            db.session.commit()
            return step
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(id):
        step = ProcedureStepModel.query.get_or_404(id)
        try:
            db.session.delete(step)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
