from flask import Blueprint, request, jsonify
from app.models import User
from app import db

api = Blueprint('api', __name__)

@api.route('/users', methods=['POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()

        required_fields = ['username', 'password', 'first_name', 'last_name', 
                         'email', 'phone_number', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify(error=f'Missing required field: {field}'), 400
            
        if User.query.filter_by(username=data['username']).first():
            return jsonify(error='Username exists'), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify(error='Email exists'), 400
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return jsonify(error='Phone number exists'), 400
        
        try:
            new_user = User(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone_number=data['phone_number'],
                address=data['address']
            )
            new_user.set_password(data['password'])
            new_user.generate_activation_token()

            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                "message": "User created successfully",
                "user": new_user.to_credentials()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500