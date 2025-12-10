from app.models.procedure_model import ProcedureModel as Procedure
from app.db import db


class ProcedureService:
    def get_all(self):
        return Procedure.query.order_by(Procedure.updated_at.desc()).all()

    def get(self, procedure_id):
        return Procedure.query.get(procedure_id)

    def create(self, data):
        procedure = Procedure(**data)
        db.session.add(procedure)
        db.session.commit()
        return procedure

    def update(self, procedure_id, data):
        procedure = self.get(procedure_id)
        if not procedure:
            raise ValueError("Procedure not found")
        for field in [
            "category",
            "title",
            "description",
            "process_time",
            "authority_level",
            "fee_text",
            "process_steps",
            "required_documents",
            "important_notes",
            "creator",
        ]:
            if field in data:
                setattr(procedure, field, data[field])
        db.session.commit()
        return procedure

    def delete(self, procedure_id):
        procedure = self.get(procedure_id)
        if not procedure:
            raise ValueError("Procedure not found")
        db.session.delete(procedure)
        db.session.commit()


procedure_service = ProcedureService()
