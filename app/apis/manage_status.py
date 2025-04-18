from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request
from app.utils.validators import ProcessForm, RatingForm
from app.models import ItemTransaction, StatusType, User
from app import db
from datetime import datetime, timezone

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
        user = User.query.get(get_jwt_identity())
        user.last_activity = datetime.now(timezone.utc)

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Order processed successfully',
            'data': item_transaction.to_dict()
        }), 200
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
        user = User.query.get(get_jwt_identity())
        user.last_activity = datetime.now(timezone.utc)

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Order rated successfully',
            'data': item_transaction.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": "Server error",
            "message": str(e)
        }), 500
