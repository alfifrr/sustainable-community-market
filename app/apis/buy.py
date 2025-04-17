from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request
from app.utils.validators import BuyProductForm
from app.models import Address, ItemTransaction, Product
from app import db

buy = Blueprint("buy", __name__)


@buy.route("/buy", methods=["POST"])
@jwt_required()
@handle_request("POST")
def buy_product():
    if request.method == "POST":
        data = request.get_json()
        form = BuyProductForm(data=data)
        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            delivery_address = Address.query.get(data["address_id"])
            product = Product.query.get(data["product_id"])
            pickup_address = Address.query.get(product.pickup_address_id)
            today_price = product.get_discounted_price()
            quantity = data["quantity"]
            total_price = today_price * quantity

            item_transaction = ItemTransaction(
                quantity=quantity,
                total_price=total_price,
                pickup_address_id=pickup_address.id,
                delivery_address_id=delivery_address.id,
                pickup_address_details=pickup_address.to_dict(),
                delivery_address_details=delivery_address.to_dict(),
                product_id=product.id,
                seller_id=product.user_id,
                buyer_id=get_jwt_identity(),
            )
            product.stock -= quantity
            db.session.add(item_transaction)
            db.session.commit()
            return jsonify(item_transaction.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return (
                jsonify(
                    {"status": "error", "error": "Server error", "message": str(e)}
                ),
                500,
            )
