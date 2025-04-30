from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request
from app.models import User

profile = Blueprint('profile', __name__)


@profile.route('/profile', methods=['GET'])
@jwt_required()
@handle_request()
def view_profile():
    user = User.query.get(get_jwt_identity())
    if not user:
        return (
            jsonify({
                "status": "error",
                'error': 'Not found',
                "message": "User profile not found"}),
            404,
        )
    return jsonify(
        {
            "status": "success",
            "message": "Profile retrieved successfully",
            "data": user.to_credentials(),
        }
    ), 200
