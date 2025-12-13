import logging
from math import ceil

from flask_smorest import abort
from sqlalchemy import desc, and_

from app.db import db
from app.models.transaction_model import TransactionModel
from app.models.user_model import UserModel

# Create logger for this module
logger = logging.getLogger(__name__)


def get_all_transactions(filter_data=None):
    """Get all transactions with optional filtering and pagination"""
    query = TransactionModel.query

    if filter_data:
        if filter_data.get("user_id"):
            query = query.filter(TransactionModel.user_id == filter_data["user_id"])
        if filter_data.get("status") is not None:
            query = query.filter(TransactionModel.status == filter_data["status"])
        if filter_data.get("payment_method"):
            query = query.filter(TransactionModel.payment_method == filter_data["payment_method"])

    # Pagination
    page = filter_data.get("page", 1) if filter_data else 1
    page_size = filter_data.get("page_size", 20) if filter_data else 20

    total_transactions = query.count()
    total_page = ceil(total_transactions / page_size)

    transactions = query.order_by(desc(TransactionModel.created_at)) \
                       .offset((page - 1) * page_size) \
                       .limit(page_size) \
                       .all()

    return {
        "results": transactions,
        "total_page": total_page,
        "total_transactions": total_transactions
    }


def get_transaction(transaction_id):
    """Get a single transaction by ID"""
    transaction = TransactionModel.query.filter_by(id=transaction_id).first()
    if not transaction:
        logger.error(f"Transaction with id {transaction_id} not found")
        abort(404, message="Transaction not found")
    return transaction


def create_transaction(transaction_data, user_id):
    """Create a new transaction"""
    try:
        transaction = TransactionModel(
            user_id=user_id,
            status=transaction_data["status"],
            amount=transaction_data["amount"],
            payment_method=transaction_data["payment_method"],
            metadata=transaction_data.get("metadata")
        )

        db.session.add(transaction)
        db.session.commit()

        logger.info(f"Transaction created successfully for user {user_id}")
        return transaction

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating transaction: {str(e)}")
        abort(500, message="Failed to create transaction")


def update_transaction(transaction_data, transaction_id):
    """Update an existing transaction"""
    transaction = TransactionModel.query.filter_by(id=transaction_id).first()
    if not transaction:
        logger.error(f"Transaction with id {transaction_id} not found")
        abort(404, message="Transaction not found")

    try:
        # Update fields if provided
        if "status" in transaction_data and transaction_data["status"] is not None:
            transaction.status = transaction_data["status"]

        if "amount" in transaction_data and transaction_data["amount"] is not None:
            transaction.amount = transaction_data["amount"]

        if "payment_method" in transaction_data and transaction_data["payment_method"]:
            transaction.payment_method = transaction_data["payment_method"]

        if "metadata" in transaction_data:
            transaction.metadata = transaction_data["metadata"]

        db.session.commit()

        logger.info(f"Transaction {transaction_id} updated successfully")
        return transaction

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating transaction {transaction_id}: {str(e)}")
        abort(500, message="Failed to update transaction")


def delete_transaction(transaction_id):
    """Delete a transaction"""
    transaction = TransactionModel.query.filter_by(id=transaction_id).first()
    if not transaction:
        logger.error(f"Transaction with id {transaction_id} not found")
        abort(404, message="Transaction not found")

    try:
        db.session.delete(transaction)
        db.session.commit()

        logger.info(f"Transaction {transaction_id} deleted successfully")
        return {"message": "Transaction deleted successfully"}

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting transaction {transaction_id}: {str(e)}")
        abort(500, message="Failed to delete transaction")


def get_user_transactions(user_id, filter_data=None):
    """Get all transactions for a specific user"""
    query = TransactionModel.query.filter(TransactionModel.user_id == user_id)

    if filter_data:
        if filter_data.get("status") is not None:
            query = query.filter(TransactionModel.status == filter_data["status"])
        if filter_data.get("payment_method"):
            query = query.filter(TransactionModel.payment_method == filter_data["payment_method"])

    # Pagination
    page = filter_data.get("page", 1) if filter_data else 1
    page_size = filter_data.get("page_size", 20) if filter_data else 20

    total_transactions = query.count()
    total_page = ceil(total_transactions / page_size)

    transactions = query.order_by(desc(TransactionModel.created_at)) \
                       .offset((page - 1) * page_size) \
                       .limit(page_size) \
                       .all()

    return {
        "results": transactions,
        "total_page": total_page,
        "total_transactions": total_transactions
    }


def update_transaction_status(transaction_id, status):
    """Update transaction status"""
    transaction = TransactionModel.query.filter_by(id=transaction_id).first()
    if not transaction:
        logger.error(f"Transaction with id {transaction_id} not found")
        abort(404, message="Transaction not found")

    try:
        transaction.status = status
        db.session.commit()

        logger.info(f"Transaction {transaction_id} status updated to {status}")
        return transaction

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating transaction {transaction_id} status: {str(e)}")
        abort(500, message="Failed to update transaction status")


def get_user_balance(user_id):
    """Calculate user balance from completed transactions"""
    user = UserModel.query.filter_by(id=user_id).first()
    if not user:
        abort(404, message="User not found")

    # Sum of all completed transactions (status = 1)
    completed_transactions = TransactionModel.query.filter(
        and_(TransactionModel.user_id == user_id, TransactionModel.status == 1)
    ).all()

    balance = sum(transaction.amount for transaction in completed_transactions)
    return {"user_id": user_id, "balance": balance, "stored_balance": user.balance}
