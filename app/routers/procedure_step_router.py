from flask.views import MethodView
from flask_smorest import Blueprint
from app.db import db
from app.models.procedure_steps_model import ProcedureStepModel
from app.schemas.procedure_step_schema import ProcedureStepSchema

blp = Blueprint("ProcedureStep", __name__, description="Steps API")


@blp.route("/procedures/<int:procedure_id>/steps")
class StepList(MethodView):
    @blp.response(200, ProcedureStepSchema(many=True))
    def get(self, procedure_id):
        return ProcedureStepModel.query.filter_by(procedure_id=procedure_id).all()

    @blp.arguments(ProcedureStepSchema)
    @blp.response(201, ProcedureStepSchema)
    def post(self, data, procedure_id):
        step = ProcedureStepModel(procedure_id=procedure_id, **data)
        db.session.add(step)
        db.session.commit()
        return step


@blp.route("/steps/<int:id>")
class StepDetail(MethodView):
    @blp.response(200, ProcedureStepSchema)
    def get(self, id):
        return ProcedureStepModel.query.get_or_404(id)

    @blp.arguments(ProcedureStepSchema)
    @blp.response(200, ProcedureStepSchema)
    def put(self, data, id):
        step = ProcedureStepModel.query.get_or_404(id)
        for key, val in data.items():
            setattr(step, key, val)
        db.session.commit()
        return step

    def delete(self, id):
        step = ProcedureStepModel.query.get_or_404(id)
        db.session.delete(step)
        db.session.commit()
        return {"message": "Deleted"}
