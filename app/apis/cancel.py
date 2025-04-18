from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import ItemTransaction, User, Product, StatusType
from app.utils.decorators import handle_request
from app.utils.validators import CancelForm
from decimal import Decimal
from datetime import datetime, timezone

cancel = Blueprint('cancel', __name__)


@cancel.route('/cancel', methods=['POST'])
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
        user.last_activity = datetime.now(timezone.utc)
        # return stock if still exists
        product = Product.query.get(item_transaction.product_id)
        if product:
            product.stock += int(item_transaction.quantity)

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Order cancelled and refunded successfully',
            'data': item_transaction.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": "Server error",
            "message": str(e)
        }), 500
