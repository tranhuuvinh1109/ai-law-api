from flask_smorest import Api

from app.routers.user_router import blp as UserBlueprint
from app.routers.blog_router import blp as BlogBlueprint
from app.routers.conversation_router import blp as ConversationBlueprint
from app.routers.procedure_router import blp as ProcedureBlueprint


# Register Blueprint
def register_routing(app):
    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(BlogBlueprint)
    api.register_blueprint(ConversationBlueprint)
    api.register_blueprint(ProcedureBlueprint)
