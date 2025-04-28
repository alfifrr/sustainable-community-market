from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from app.utils.validators import SignupForm, ProfileUpdateForm
from app.utils.decorators import handle_request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone

user = Blueprint("user", __name__)


@user.route("/users", methods=["GET", "POST"])
@handle_request("POST")
def users():
    if request.method == "POST":
        data = request.get_json()
        form = SignupForm(data=data)

        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        if User.query.filter_by(username=data["username"]).first():
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": "Validation error",
                        "message": "Username already exists",
                    }
                ),
                400,
            )
        if User.query.filter_by(email=data["email"]).first():
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": "Validation error",
                        "message": "Email already exists",
                    }
                ),
                400,
            )
        if User.query.filter_by(phone_number=data["phone_number"]).first():
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": "Validation error",
                        "message": "Phone number already exists",
                    }
                ),
                400,
            )

        try:
            new_user = User(
                username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                phone_number=data["phone_number"],
            )
            new_user.set_password(data["password"])
            new_user.generate_activation_token()

            db.session.add(new_user)
            db.session.commit()
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "User created successfully",
                        "data": new_user.to_credentials(),
                    }
                ),
                201,
            )

        except Exception as e:
            db.session.rollback()
            return (
                jsonify(
                    {"status": "error", "error": "Server error",
                        "message": str(e)}
                ),
                500,
            )
    # GET
    query = request.args.get("q", "").strip()
    if query:
        users = User.query.filter(
            db.or_(
                db.func.lower(User.first_name).like(f"%{query.lower()}%"),
                db.func.lower(User.last_name).like(f"%{query.lower()}%"),
            )
        ).all()
    else:
        users = User.query.all()
    if not users:
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "No users found",
                    "data": [],
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "status": "success",
                "message": "Users retrieved successfully",
                "data": [user.to_dict() for user in users],
            }
        ),
        200,
    )


@user.route("/users/<int:id>", methods=["GET"])
@handle_request("")
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return (
            jsonify({"status": "error", "message": f"User with id {id} not found"}),
            404,
        )
    return (
        jsonify(
            {
                "status": "success",
                "message": "Users retrieved successfully",
                "data": user.to_dict(),
            }
        ),
        200,
    )


@user.route("/users", methods=["PUT"])
@jwt_required()
@handle_request("PUT")
def manage_user():
    if request.method == "PUT":
        current_user_id = get_jwt_identity()

        # Pass user_id to form for username validation
        data = request.get_json()
        form = ProfileUpdateForm(data=data)
        form.user_id = str(current_user_id)

        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            user = User.query.get(current_user_id)
            # Update allowed fields
            user.username = data["username"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.phone_number = data["phone_number"]

            # set using provided model method
            user.set_password(data['password'])

            user.last_activity = datetime.now(timezone.utc)
            db.session.commit()

            return jsonify({
                "status": "success",
                "message": "Profile updated successfully",
                "data": user.to_credentials()
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "status": "error",
                "error": "Server error",
                "message": str(e)
            }), 500
