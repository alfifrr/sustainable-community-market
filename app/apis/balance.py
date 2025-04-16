from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request, verified_only
from app.utils.validators import DepositForm
from app.models import User
from app import db
from datetime import datetime, timezone

balance = Blueprint('balance', __name__)


@balance.route('/deposit', methods=['POST'])
@jwt_required()
@verified_only
@handle_request('POST')
def manage_balance():
    if request.method == 'POST':
        data = request.get_json()
        form = DepositForm(data=data)
        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            user = User.query.get(get_jwt_identity())
            user.balance += data['amount']
            user.last_activity = datetime.now(timezone.utc)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Balance deposited successfully',
                'data': {
                    'balance': float(user.balance)
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'error': 'Server error',
                'message': str(e)
            }), 500
