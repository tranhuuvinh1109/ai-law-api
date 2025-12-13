from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.transaction_schema import (
    TransactionSchema,
    TransactionCreateSchema,
    TransactionUpdateSchema,
    TransactionFilterSchema,
    TransactionPageSchema,
)
from app.services import transaction_service
from app.utils.decorators import permission_required

blp = Blueprint("Transaction", __name__, description="Transaction API")


@blp.route("/transaction")
class TransactionList(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    @blp.arguments(TransactionFilterSchema, location="query")
    @blp.response(200, TransactionPageSchema)
    def get(self, filter_data):
        """Get all transactions with filtering and pagination"""
        result = transaction_service.get_all_transactions(filter_data)
        return result


@blp.route("/transaction/<int:transaction_id>")
class Transaction(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    @blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        """Get a single transaction by ID"""
        result = transaction_service.get_transaction(transaction_id)
        return result

    @jwt_required()
    @permission_required(permission_name="write")
    @blp.arguments(TransactionUpdateSchema)
    @blp.response(200, TransactionSchema)
    def put(self, transaction_data, transaction_id):
        """Update a transaction"""
        result = transaction_service.update_transaction(transaction_data, transaction_id)
        return result

    @jwt_required()
    @permission_required(permission_name="delete")
    def delete(self, transaction_id):
        """Delete a transaction"""
        result = transaction_service.delete_transaction(transaction_id)
        return result


@blp.route("/transaction/user/<int:user_id>")
class UserTransactions(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    @blp.arguments(TransactionFilterSchema, location="query")
    @blp.response(200, TransactionPageSchema)
    def get(self, filter_data, user_id):
        """Get all transactions for a specific user"""
        result = transaction_service.get_user_transactions(user_id, filter_data)
        return result


@blp.route("/transaction/user/<int:user_id>/create")
class CreateTransaction(MethodView):
    @jwt_required()
    @permission_required(permission_name="write")
    @blp.arguments(TransactionCreateSchema)
    @blp.response(201, TransactionSchema)
    def post(self, transaction_data, user_id):
        """Create a new transaction for a user"""
        result = transaction_service.create_transaction(transaction_data, user_id)
        return result


@blp.route("/transaction/<int:transaction_id>/status/<int:status>")
class UpdateTransactionStatus(MethodView):
    @jwt_required()
    @permission_required(permission_name="write")
    @blp.response(200, TransactionSchema)
    def put(self, transaction_id, status):
        """Update transaction status"""
        result = transaction_service.update_transaction_status(transaction_id, status)
        return result


@blp.route("/user/<int:user_id>/balance")
class UserBalance(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    def get(self, user_id):
        """Get user balance from transactions"""
        result = transaction_service.get_user_balance(user_id)
        return result
