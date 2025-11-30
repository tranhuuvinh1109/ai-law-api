from datetime import datetime
from app.db import db

class ProcedureModel(db.Model):
    __tablename__ = "procedures"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text, nullable=True)
    long_description = db.Column(db.Text, nullable=True)

    level_of_authority = db.Column(db.String(255), nullable=True)  # Tỉnh/TP, Quận/Huyện,...
    process_time = db.Column(db.String(50), nullable=True)         # "3-5 ngày"

    fee_min = db.Column(db.Float, nullable=True)
    fee_max = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    steps = db.relationship("ProcedureStepModel", backref="procedure", lazy=True, cascade="all, delete")
    documents = db.relationship("ProcedureDocumentModel", backref="procedure", lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Procedure {self.title}>"
