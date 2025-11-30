from flask_smorest import Api

from app.routers.permission_router import blp as PermissionBlueprint
from app.routers.role_permission_router import blp as RolePermissionBlueprint
from app.routers.role_router import blp as RoleBlueprint
from app.routers.user_role_router import blp as UserRoleBlueprint
from app.routers.user_router import blp as UserBlueprint
from app.routers.blog_router import blp as BlogBlueprint
from app.routers.conversation_router import blp as ConversationBlueprint
from app.routers.category_router import blp as CategoryBlueprint
from app.routers.procedure_router import blp as ProcedureBlueprint
from app.routers.procedure_document_router import blp as ProcedureDocumentBlueprint
from app.routers.procedure_step_router import blp as ProcedureStepBlueprint


# Register Blueprint
def register_routing(app):
    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(RoleBlueprint)
    api.register_blueprint(PermissionBlueprint)
    api.register_blueprint(UserRoleBlueprint)
    api.register_blueprint(RolePermissionBlueprint)
    api.register_blueprint(BlogBlueprint)
    api.register_blueprint(ConversationBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(ProcedureBlueprint)
    api.register_blueprint(ProcedureDocumentBlueprint)
    api.register_blueprint(ProcedureStepBlueprint)
