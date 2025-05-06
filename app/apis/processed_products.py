from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import ItemTransaction, StatusType, User
from app.utils.decorators import role_required, handle_request

processed_products = Blueprint("processed_products", __name__, url_prefix="/api")


@processed_products.route("/processed-products", methods=["GET"])
@jwt_required()
@handle_request()
@role_required(["admin", "expedition"])
def get_processed_products():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user.is_admin():
            transactions = ItemTransaction.query.filter_by(
                delivery_status=StatusType.PROCESSED
            ).all()
        else:
            transactions = ItemTransaction.query.filter_by(
                delivery_status=StatusType.PROCESSED,
                assigned_expedition_id=current_user_id,
            ).all()

        if not transactions:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "No processed products found",
                        "data": [],
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Processed products retrieved successfully",
                    "data": [transaction.to_dict() for transaction in transactions],
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": "Server error", "message": str(e)}),
            500,
        )


@processed_products.route("/processed-products/<int:id>", methods=["GET"])
@jwt_required()
@handle_request()
@role_required(["admin", "expedition"])
def get_processed_product(id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user.is_admin():
            transaction = ItemTransaction.query.filter_by(
                id=id,
                delivery_status=StatusType.PROCESSED,
            ).first()
        else:
            transaction = ItemTransaction.query.filter_by(
                id=id,
                delivery_status=StatusType.PROCESSED,
                assigned_expedition_id=current_user_id,
            ).first()

        if not transaction:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Processed product with id {id} not found",
                    }
                ),
                404,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Processed product retrieved successfully",
                    "data": transaction.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": "Server error", "message": str(e)}),
            500,
        )
