from flask import Blueprint, request, jsonify
from app.models import Product, Address
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request
from app.utils.validators import ProductForm
from datetime import datetime

product = Blueprint("product", __name__)


@product.route("/products", methods=["POST"])
@jwt_required()
@handle_request("POST")
def manage_products():
    if request.method == "POST":
        data = request.get_json()
        form = ProductForm(data=data)

        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            new_product = Product(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                stock=data["stock"],
                pickup_address_id=data["address_id"],
                category_id=data["category_id"],
                user_id=get_jwt_identity(),
                expiration_date=datetime.fromisoformat(
                    data["expiration_date"].replace("Z", "+00:00")
                ),
            )
            db.session.add(new_product)
            db.session.commit()
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Product created successfully",
                        "data": new_product.to_dict(),
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


@product.route("/products", methods=["GET"])
@handle_request()
def get_products():
    products = Product.query.all()
    if not products:
        return (
            jsonify(
                {"status": "success", "message": "No products found", "data": []}),
            200,
        )
    return (
        jsonify(
            {
                "status": "success",
                "message": "Products retrieved successfully",
                "data": [product.to_dict() for product in products],
            }
        ),
        200,
    )
