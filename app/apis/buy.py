from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request, role_required
from app.utils.validators import BuyProductForm
from app.models import Address, ItemTransaction, Product, User
from app import db
from decimal import Decimal
from datetime import datetime, timezone

buy = Blueprint("buy", __name__)


@buy.route("/buy", methods=["POST"])
@jwt_required()
@handle_request("POST")
@role_required("buyer")
def buy_product():
    if request.method == "POST":
        data = request.get_json()
        form = BuyProductForm(data=data)
        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            user = User.query.get(get_jwt_identity())
            delivery_address = Address.query.get(data["address_id"])
            product = Product.query.get(data["product_id"])
            pickup_address = Address.query.get(product.pickup_address_id)
            quantity = data["quantity"]
            original_total_price = product.price * quantity

            # Calculate discounted price with details
            total_price, discount_details = product.calculate_total_discount(quantity)

            total_price = Decimal(str(total_price))

            delivery_fee = Decimal("15000")
            grand_total = total_price + delivery_fee
            if user.balance < grand_total:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "error": "Insufficient funds",
                            "message": f"Available balance {user.balance} is less than price {grand_total} incl. shipping (15000)",
                        }
                    ),
                    422,
                )

            item_transaction = ItemTransaction(
                quantity=quantity,
                total_price=total_price,
                pickup_address_id=pickup_address.id,
                delivery_address_id=delivery_address.id,
                pickup_address_details=pickup_address.to_dict(),
                delivery_address_details=delivery_address.to_dict(),
                product_id=product.id,
                seller_id=product.user_id,
                buyer_id=user.id,
                original_price=original_total_price,
                product_details={
                    **product.to_dict(),
                    "applied_discounts": discount_details,
                },
            )
            product.stock -= quantity
            user.balance -= grand_total
            user.last_activity = datetime.now(timezone.utc)

            db.session.add(item_transaction)
            db.session.commit()

            response_data = item_transaction.to_dict()
            response_data["discount_details"] = discount_details
            response_data["delivery_fee"] = float(delivery_fee)
            response_data["grand_total"] = float(grand_total)

            return jsonify(response_data), 201
        except Exception as e:
            db.session.rollback()
            return (
                jsonify(
                    {"status": "error", "error": "Server error", "message": str(e)}
                ),
                500,
            )
