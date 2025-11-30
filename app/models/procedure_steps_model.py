from datetime import datetime
from app.db import db


class ProcedureStepModel(db.Model):
    __tablename__ = "procedure_steps"

    id = db.Column(db.Integer, primary_key=True)
    procedure_id = db.Column(db.Integer, db.ForeignKey("procedures.id"), nullable=False)

    step_number = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4,...
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    time_estimation = db.Column(db.String(50), nullable=True)  # "1-2 ngày"

    def __repr__(self):
        return f"<ProcedureStep {self.step_number} - {self.title}>"
