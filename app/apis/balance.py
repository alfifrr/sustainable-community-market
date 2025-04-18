from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request, verified_only
from app.utils.validators import DepositForm, WithdrawalForm
from app.models import User, TransactionHistory, TransactionType
from app import db
from datetime import datetime, timezone
from decimal import Decimal

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
            amount = Decimal(str(data['amount']))
            transaction_history = TransactionHistory(
                user_id=user.id,
                amount=amount,
                type=TransactionType.DEPOSIT,
                details={
                    'description': f'Deposit of {amount}',
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            )
            user.balance += amount
            user.last_activity = datetime.now(timezone.utc)

            db.session.add(transaction_history)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Balance deposited successfully',
                'data': {
                    'balance': float(user.balance),
                    'transaction': transaction_history.to_dict()
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'error': 'Server error',
                'message': str(e)
            }), 500


@balance.route('/withdraw', methods=['POST'])
@jwt_required()
@verified_only
@handle_request('POST')
def withdraw_balance():
    if request.method == 'POST':
        data = request.get_json()
        form = WithdrawalForm(data=data)
        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            user = User.query.get(get_jwt_identity())
            amount = Decimal(str(data['amount']))
            if user.balance < amount:
                return jsonify({
                    'status': 'error',
                    'error': 'Insufficient funds',
                    'message': f'Available balance {user.balance} is less than requested amount {amount}'
                }), 422
            transaction_history = TransactionHistory(
                user_id=user.id,
                amount=amount,
                type=TransactionType.WITHDRAW,
                details={
                    'description': f'Withdrawal of {amount}',
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            )
            user.balance -= amount
            user.last_activity = datetime.now(timezone.utc)

            db.session.add(transaction_history)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Balance withdrawed successfully',
                'data': {
                    'balance': float(user.balance),
                    'transaction': transaction_history.to_dict()
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'error': 'Server error',
                'message': str(e)
            }), 500
