from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request
from app.utils.validators import ProcessForm, CancelForm, ConfirmDeliveryForm, RatingForm
from app.models import ItemTransaction, StatusType, User, Product
from app import db
from decimal import Decimal

manage_status = Blueprint('manage_status', __name__)


@manage_status.route('/process', methods=['POST'])
@jwt_required()
@handle_request('POST')
def process_product():
    data = request.get_json()
    form = ProcessForm(data=data)
    if not form.validate():
        return jsonify(form.get_validation_error()), 400
    try:
        item_transaction = ItemTransaction.query.get(data['transaction_id'])
        item_transaction.delivery_status = StatusType.PROCESSED
        db.session.commit()
        return jsonify(item_transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": "Server error",
            "message": str(e)
        }), 500


@manage_status.route('/cancel', methods=['POST'])
@jwt_required()
@handle_request('POST')
def cancel_product():
    data = request.get_json()
    form = CancelForm(data=data)
    if not form.validate():
        return jsonify(form.get_validation_error()), 400
    try:
        item_transaction = ItemTransaction.query.get(data['transaction_id'])
        item_transaction.delivery_status = StatusType.CANCELLED
        # refund
        user = User.query.get(get_jwt_identity())
        delivery_fee = Decimal('15000')
        total_refund = item_transaction.total_price + delivery_fee
        user.balance += total_refund
        # return stock
        product = Product.query.get(item_transaction.product_id)
        product.stock += int(item_transaction.quantity)

        db.session.commit()
        return jsonify(item_transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": "Server error",
            "message": str(e)
        }), 500


@manage_status.route('/rate', methods=['POST'])
@jwt_required()
@handle_request('POST')
def rate_product():
    data = request.get_json()
    form = RatingForm(data=data)
    if not form.validate():
        return jsonify(form.get_validation_error()), 400
    try:
        item_transaction = ItemTransaction.query.get(data['transaction_id'])
        item_transaction.delivery_status = StatusType.RATED
        item_transaction.rating = data['rating']
        db.session.commit()
        return jsonify(item_transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": "Server error",
            "message": str(e)
        }), 500
