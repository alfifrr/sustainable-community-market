from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from app.utils.validators import SignupForm

user = Blueprint('user', __name__)


@user.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        form = SignupForm(data=data)

        if not form.validate():
            return jsonify({
                'error': 'Validation error',
                'message': form.errors
            }), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'error': 'Validation error',
                'message': 'Username already exists'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'error': 'Validation error',
                'message': 'Email already exists'}), 400
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return jsonify({
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

            # send_user_activation_email(new_user)

            return jsonify({
                "status": "success",
                "message": "User created successfully",
                "data": new_user.to_credentials()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Server error',
                'message': str(e)}), 500
    # GET
    try:
        users = User.query.all()
        return jsonify({
            "status": "success",
            "message": "Users retrieved successfully",
            "data": [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500
