from flask.views import MethodView
from flask_smorest import Blueprint
from app.db import db
from app.models.category_model import CategoryModel
from app.schemas.category_schema import CategorySchema

blp = Blueprint("Category", __name__, description="Category API")


@blp.route("/categories")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, data):
        category = CategoryModel(**data)
        db.session.add(category)
        db.session.commit()
        return category


@blp.route("/categories/<int:id>")
class CategoryDetail(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, id):
        return CategoryModel.query.get_or_404(id)

    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def put(self, data, id):
        category = CategoryModel.query.get_or_404(id)
        for key, val in data.items():
            setattr(category, key, val)
        db.session.commit()
        return category

    def delete(self, id):
        category = CategoryModel.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Deleted"}
