from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models import User
from flask import jsonify, request


def verified_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        if not user:
            return jsonify({
                'error': 'Authentication error',
                'message': 'User not found'}), 404
        if not user.is_verified:
            return jsonify({
                'error': 'Authorization error',
                'message': 'Account not verified. Please verify your account first.'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


def require_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST' and not request.is_json:
            return jsonify({
                'error': 'JSON error',
                'message': 'Missing JSON in request'
            }), 400
        return f(*args, **kwargs)
    return decorated_function
