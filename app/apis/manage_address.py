from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request
from app.utils.validators import AddressForm
from app.models import Address, User
from app import db
from datetime import datetime, timezone

manage_address = Blueprint('manage_address', __name__)


@manage_address.route('/addresses/<int:address_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@handle_request('PUT')
def manage_address_by_id(address_id):
    current_user_id = get_jwt_identity()
    address = Address.query.filter_by(
        id=address_id,
        user_id=current_user_id
    ).first()

    if not address:
        return jsonify({
            'status': 'error',
            'error': 'Not found',
            'message': 'Address not found or does not belong to you'
        }), 404

    if request.method == 'PUT':
        data = request.get_json()
        form = AddressForm(data=data)
        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            address.label = data['label']
            address.address = data['address']
            address.details = data.get('details')
            address.contact_person = data['contact_person']

            user = User.query.get(current_user_id)
            user.last_activity = datetime.now(timezone.utc)

            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Address updated successfully',
                'data': address.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'error': 'Server error',
                'message': str(e)
            }), 500
    # DELETE
    try:
        # Check if address is being used by any products
        if address.products.count() > 0:
            return jsonify({
                'status': 'error',
                'error': 'Validation error',
                'message': 'Cannot delete address that is being used by products'
            }), 422

        db.session.delete(address)

        user = User.query.get(current_user_id)
        user.last_activity = datetime.now(timezone.utc)

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Address deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'error': 'Server error',
            'message': str(e)
        }), 500
