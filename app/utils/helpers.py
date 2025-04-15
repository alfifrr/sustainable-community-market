from flask import url_for, request, jsonify
from app.utils.email import send_activation_email
from app.models import User


def send_user_activation_email(user):
    activation_url = url_for(
        'auth.activate_account',
        token=user.activation_token,
        _external=True
    )
    send_activation_email(user, activation_url)


def validate_credentials():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return None, jsonify({
            'error': 'Validation error',
            'message': 'Missing username or password field'
        }), 400
    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return None, jsonify({
            'error': 'Authentication error',
            'message': 'Invalid username or password'
        }), 401
    return user, None, None
