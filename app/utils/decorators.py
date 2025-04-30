from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models import User
from flask import jsonify, request, abort
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest


def role_required(allowed_roles: list[str] | str):
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)

            if not user:
                return jsonify({
                    'status': 'error',
                    'error': 'Authentication error',
                    'message': 'User not found'
                }), 401

            if not any(user.has_role(role) for role in allowed_roles):
                return jsonify({
                    'status': 'error',
                    'error': 'Authorization error',
                    'message': 'Insufficient permissions for this operation'
                }), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def verified_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'error': 'Authentication error',
                'message': 'User not found'}), 404
        if not user.is_verified:
            return jsonify({
                'status': 'error',
                'error': 'Authorization error',
                'message': 'Account not verified. Please verify your account first.'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


def handle_request(*methods):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method in methods:
                if not request.is_json:
                    return jsonify({
                        'status': 'error',
                        'error': 'JSON error',
                        'message': f'{request.method} request must include JSON data'
                    }), 400
                try:
                    request.get_json()
                except BadRequest:
                    return jsonify({
                        'status': 'error',
                        'error': 'JSON decode error',
                        'message': 'Failed to decode JSON object'
                    }), 400

            if request.method == 'GET':
                try:
                    return f(*args, **kwargs)
                except SQLAlchemyError as e:
                    return jsonify({
                        'status': 'error',
                        'error': 'Database error',
                        'message': str(e)
                    }), 500
                except Exception as e:
                    return jsonify({
                        'status': 'error',
                        'error': 'Server error',
                        'message': str(e)
                    }), 500
            return f(*args, **kwargs)
        return decorated_function
    return decorator
