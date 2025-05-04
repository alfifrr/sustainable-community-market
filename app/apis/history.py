from flask import Blueprint, jsonify
from app.models import ItemTransaction, TransactionHistory
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request

history = Blueprint("history", __name__)


@history.route("/product-history", methods=["GET"])
@jwt_required()
@handle_request()
def get_item_history():
    current_user_id = get_jwt_identity()
    product_history = (
        ItemTransaction.query.filter(
            db.or_(
                ItemTransaction.buyer_id == current_user_id,
                ItemTransaction.seller_id == current_user_id,
            )
        )
        .order_by(ItemTransaction.updated_at.desc())
        .all()
    )
    if not product_history:
        return (
            jsonify(
                {"status": "success", "message": "No product history found", "data": []}
            ),
            200,
        )
    return (
        jsonify(
            {
                "status": "success",
                "message": "Product history retrieved successfully",
                "data": [product.to_dict() for product in product_history],
            }
        ),
        201,
    )


@history.route("/product-history/<int:transaction_id>", methods=["GET"])
@jwt_required()
@handle_request()
def get_item_history_by_id(transaction_id):
    current_user_id = get_jwt_identity()

    transaction = ItemTransaction.query.filter(
        db.and_(
            ItemTransaction.id == transaction_id,
            db.or_(
                ItemTransaction.buyer_id == current_user_id,
                ItemTransaction.seller_id == current_user_id,
            ),
        )
    ).first()

    if not transaction:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Transaction not found or you don't have permission to view it",
                }
            ),
            404,
        )

    return (
        jsonify(
            {
                "status": "success",
                "message": "Transaction retrieved successfully",
                "data": transaction.to_dict(),
            }
        ),
        200,
    )


@history.route("/transactions", methods=["GET"])
@jwt_required()
@handle_request()
def get_products():
    transaction_history = (
        TransactionHistory.query.filter_by(user_id=get_jwt_identity())
        .order_by(TransactionHistory.date.desc())
        .all()
    )
    if not transaction_history:
        return (
            jsonify(
                {"status": "success", "message": "No transactions found", "data": []}
            ),
            200,
        )
    return (
        jsonify(
            {
                "status": "success",
                "message": "Transactions retrieved successfully",
                "data": [transaction.to_dict() for transaction in transaction_history],
            }
        ),
        200,
    )
