from flask import Blueprint, request, jsonify
from app.models import Product, User, Category, ProductCertification
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import handle_request, role_required
from app.utils.validators import ProductForm
from datetime import datetime, timezone

product = Blueprint("product", __name__)


@product.route("/products", methods=["POST"])
@jwt_required()
@handle_request("POST")
@role_required("seller")
def manage_products():
    if request.method == "POST":
        data = request.get_json()
        form = ProductForm(data=data)

        if not form.validate():
            return jsonify(form.get_validation_error()), 400

        try:
            sustainability_certifications = data.get(
                "sustainability_certifications", []
            )
            # Automatically determine is_sustainable based on certifications
            is_sustainable = len(sustainability_certifications) > 0

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
                is_sustainable=is_sustainable,
                sustainability_certifications=sustainability_certifications,
            )
            user = User.query.get(get_jwt_identity())
            user.last_activity = datetime.now(timezone.utc)

            db.session.add(new_product)
            db.session.flush()  # This ensures new_product gets its ID

            # Create certification entries if sustainability_certifications array is not empty
            if sustainability_certifications:
                for cert_id in sustainability_certifications:
                    cert_entry = ProductCertification(
                        product_id=new_product.id, certification_id=cert_id
                    )
                    db.session.add(cert_entry)

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
                    {"status": "error", "error": "Server error", "message": str(e)}
                ),
                500,
            )


@product.route("/products", methods=["GET"])
@handle_request()
def get_products():
    query = request.args.get("q", "").strip()
    if query:
        search_term = f"%{query.lower()}%"
        products = (
            Product.query.join(Product.category)
            .filter(
                db.or_(
                    db.func.lower(Product.name).like(search_term),
                    db.func.lower(Product.description).like(search_term),
                    db.func.lower(Category.name).like(search_term),
                )
            )
            .all()
        )
    else:
        products = Product.query.all()
    if not products:
        return (
            jsonify({"status": "success", "message": "No products found", "data": []}),
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


@product.route("/products/<int:id>", methods=["GET"])
@handle_request()
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return (
            jsonify({"status": "error", "message": f"Product with id {id} not found"}),
            404,
        )
    return (
        jsonify(
            {
                "status": "success",
                "message": "Product retrieved successfully",
                "data": product.to_dict(),
            }
        ),
        200,
    )
