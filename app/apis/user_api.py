from flask import Blueprint, request, jsonify
from app.models import User
from app import db

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()

        required_fields = ['username', 'password', 'first_name',
                           'last_name', 'email', 'phone_number']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Validation error',
                    'message': f'Missing required field: {field}'}), 400

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

        # TODO: username minimum char, password strength, email validity, first/last name checker, phone number char, address minimum char

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
                "message": "User created successfully",
                "user": new_user.to_credentials()}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': 'Server error',
                'message': f'Failed to create user: {str(e)}'}), 500
    # GET
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({
            'error': 'Exception on GET /users',
            'message': f'Failed to retrieve users: {str(e)}'}), 500
