from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request
from app.utils.validators import ProductForm
from app.models import Product, User
from app import db
from datetime import datetime, timezone

manage_product = Blueprint('manage_product', __name__)


@manage_product.route('/products/<int:product_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@handle_request('PUT')
def manage_product_by_id(product_id):
    current_user_id = get_jwt_identity()
    product = Product.query.filter_by(
        id=product_id,
        user_id=current_user_id
    ).first()

    if not product:
        return jsonify({
            'status': 'error',
            'error': 'Not found',
            'message': 'Product not found or does not belong to you'
        }), 404

    if request.method == 'PUT':
        data = request.get_json()
        form = ProductForm(data=data)
        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            product.name = data['name']
            product.description = data['description']
            product.price = data['price']
            product.stock = data['stock']
            product.pickup_address_id = data['address_id']
            product.category_id = data['category_id']
            product.expiration_date = datetime.fromisoformat(
                data['expiration_date'].replace('Z', '+00:00')
            )

            user = User.query.get(current_user_id)
            user.last_activity = datetime.now(timezone.utc)

            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Product updated successfully',
                'data': product.to_dict()
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
        db.session.delete(product)

        user = User.query.get(current_user_id)
        user.last_activity = datetime.now(timezone.utc)

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Product deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'error': 'Server error',
            'message': str(e)
        }), 500
