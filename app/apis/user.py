from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from app.utils.validators import SignupForm
from app.utils.decorators import handle_request

user = Blueprint('user', __name__)


@user.route('/users', methods=['GET', 'POST'])
@handle_request('POST')
def users():
    if request.method == 'POST':
        data = request.get_json()
        form = SignupForm(data=data)

        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'status': 'error',
                'error': 'Validation error',
                'message': 'Username already exists'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'status': 'error',
                'error': 'Validation error',
                'message': 'Email already exists'}), 400
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return jsonify({
                'status': 'error',
                'error': 'Validation error',
                'message': 'Phone number already exists'}), 400

        try:
            new_user = User(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone_number=data['phone_number']
            )
            new_user.set_password(data['password'])
            new_user.generate_activation_token()

            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                "status": "success",
                "message": "User created successfully",
                "data": new_user.to_credentials()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'error': 'Server error',
                'message': str(e)}), 500
    # GET
    users = User.query.all()
    return jsonify({
        "status": "success",
        "message": "Users retrieved successfully",
        "data": [user.to_dict() for user in users]
    }), 200


@user.route('/users/<int:id>', methods=['GET'])
@handle_request('')
def get_user(id):
    user = User.query.get(id)
    return jsonify({
        "status": "success",
        "message": "Users retrieved successfully",
        "data": user.to_dict()
    }), 200
