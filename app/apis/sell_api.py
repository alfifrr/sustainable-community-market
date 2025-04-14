from flask import Blueprint, request, jsonify
from app.models import Category
from app import db
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)


@api.route('/sell', methods=['POST'])
@jwt_required
def sell():
    if request.method == 'POST':
        data = request.get_json()

        required_fields = ['name', 'description', 'category_id', 'stock']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Validation error',
                    'message': f'Missing required field: {field}'
                }), 400

        category = Category.query.filter_by(id=data['category_id']).first()
        if not category:
            return jsonify({
                'error': 'Validation error',
                'message': 'Category does not exist'
            }), 400
