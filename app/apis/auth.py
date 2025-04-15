from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from app import db
from app.models import User
from app.utils.decorators import require_json
from app.utils.helpers import send_user_activation_email, validate_credentials


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
@require_json
def login():
    user, error_response, status_code = validate_credentials()
    if error_response:
        return error_response, status_code

    try:
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(minutes=15),
            additional_claims={'type': 'access'})
        refresh_token = create_refresh_token(
            identity=str(user.id),
            expires_delta=timedelta(days=30),
            additional_claims={'type': 'refresh'})
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500


@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    jwt_claims = get_jwt()

    if jwt_claims['type'] != 'refresh':
        return jsonify({
            "error": "Authentication error",
            "message": "Invalid token type"
        }), 401

    current_user_id = get_jwt_identity()

    access_token = create_access_token(
        identity=current_user_id,
        expires_delta=timedelta(minutes=15),
        additional_claims={'type': 'access'}
    )

    return jsonify({
        "status": "success",
        "message": "Token refreshed successfully",
        "data": {
            "access_token": access_token,
            "token_type": "bearer"
        }
    }), 200


@auth.route('/send-activation', methods=['POST'])
@require_json
def send_activation():
    user, error_response, status_code = validate_credentials()
    if error_response:
        return error_response, status_code

    if user.is_verified:
        return jsonify({
            "error": "Validation error",
            "message": "Account already activated"
        }), 401
    else:
        send_user_activation_email(user)
        return jsonify({
            "status": "success",
            "message": "Verification email has been sent"
        }), 200


@auth.route('/activate/<token>', methods=['GET'])
def activate_account(token):
    user = User.query.filter_by(activation_token=token).first()
    if not user:
        return jsonify({
            "error": "Validation error",
            "message": "Invalid activation token"
        }), 400

    try:
        user.activate_account()
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Account activated successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500
