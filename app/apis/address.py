from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import verified_only, handle_request
from app.utils.validators import AddressForm
from app.models import Address, User
from app import db
from datetime import datetime, timezone

address = Blueprint('address', __name__)


@address.route('/addresses', methods=['GET', 'POST'])
@jwt_required()
@handle_request('POST')
def manage_addresses():
    current_user_id = get_jwt_identity()
    if request.method == 'POST':
        data = request.get_json()
        form = AddressForm(data=data)
        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            user = User.query.get(current_user_id)
            if not user:
                return jsonify({
                    'status': 'error',
                    'error': 'Validation error',
                    'message': 'User not found'
                }), 404
            new_address = Address(
                label=data['label'],
                address=data['address'],
                details=data.get('details'),
                contact_person=data['contact_person'],
                user_id=current_user_id
            )
            user.last_activity = datetime.now(timezone.utc)
            db.session.add(new_address)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Address created successfully',
                'data': new_address.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'error': 'Server error',
                'message': str(e)
            }), 500
    # GET
    addresses = Address.query.filter_by(user_id=current_user_id).all()
    return jsonify({
        'status': 'success',
        'message': 'Addresses retrieved successfully',
        'data': [address.to_dict() for address in addresses]
    }), 200
