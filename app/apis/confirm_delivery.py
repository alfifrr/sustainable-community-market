from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.utils.decorators import handle_request, role_required, verified_only
from app.utils.validators import ConfirmDeliveryForm
from app.models import (
    ItemTransaction,
    StatusType,
    TransactionHistory,
    TransactionType,
    User,
)
from datetime import datetime, timezone
from decimal import Decimal

confirm_delivery = Blueprint("confirm_delivery", __name__)


@confirm_delivery.route("/confirm-delivery", methods=["POST"])
@jwt_required()
@verified_only
@handle_request("POST")
@role_required(["admin", "expedition"])
def confirm():
    data = request.get_json()
    form = ConfirmDeliveryForm(data=data)
    if not form.validate():
        return jsonify(form.get_validation_error()), 400
    try:
        current_user = User.query.get(get_jwt_identity())
        item_transaction = ItemTransaction.query.get(data["transaction_id"])
        item_transaction.delivery_status = StatusType.DELIVERED

        # Store confirmation details
        now = datetime.now(timezone.utc)
        item_transaction.confirmed_by_id = current_user.id
        item_transaction.confirmation_date = now
        amount = item_transaction.total_price

        # Create transaction histories for seller and buyer
        seller_transaction_history = TransactionHistory(
            user_id=item_transaction.seller_id,
            amount=amount,
            type=TransactionType.SELL,
            details={
                "description": f"Payment received for order #{item_transaction.id}",
                "product_name": item_transaction.product.name,
                "quantity": item_transaction.quantity,
                "buyer_name": f"{item_transaction.buyer.first_name} {item_transaction.buyer.last_name}",
                "confirmed_by": f"{current_user.first_name} {current_user.last_name}",
                "timestamp": now.isoformat(),
            },
        )
        buyer_transaction_history = TransactionHistory(
            user_id=item_transaction.buyer_id,
            amount=amount,
            type=TransactionType.BUY,
            details={
                "description": f"Order #{item_transaction.id} delivery confirmed",
                "product_name": item_transaction.product.name,
                "quantity": item_transaction.quantity,
                "seller_name": f"{item_transaction.seller.first_name} {item_transaction.seller.last_name}",
                "confirmed_by": f"{current_user.first_name} {current_user.last_name}",
                "timestamp": now.isoformat(),
            },
        )

        # Add expedition payment and transaction history
        expedition_payment = Decimal("14000")
        expedition_transaction_history = TransactionHistory(
            user_id=item_transaction.assigned_expedition_id,
            amount=expedition_payment,
            type=TransactionType.SELL,
            details={
                "description": f"Delivery payment for order #{item_transaction.id}",
                "product_name": item_transaction.product.name,
                "seller_name": f"{item_transaction.seller.first_name} {item_transaction.seller.last_name}",
                "buyer_name": f"{item_transaction.buyer.first_name} {item_transaction.buyer.last_name}",
                "timestamp": now.isoformat(),
            },
        )

        # Update balances
        seller = User.query.get(item_transaction.seller_id)
        seller.balance += amount
        expedition = User.query.get(item_transaction.assigned_expedition_id)
        expedition.balance += expedition_payment

        current_user.last_activity = now

        # Add all transaction histories
        db.session.add(seller_transaction_history)
        db.session.add(buyer_transaction_history)
        db.session.add(expedition_transaction_history)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Delivery confirmed successfully",
                    "data": {
                        "transaction": item_transaction.to_dict(),
                        "buyer_history": buyer_transaction_history.to_dict(),
                        "seller_history": seller_transaction_history.to_dict(),
                        "expedition_history": expedition_transaction_history.to_dict(),
                    },
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "error": "Server error", "message": str(e)}),
            500,
        )
