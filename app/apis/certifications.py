from flask import Blueprint, jsonify, request
from app.models import SustainabilityCertification, ProductCertification, User
from app.utils.decorators import handle_request, role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app import db

certifications = Blueprint("certifications", __name__)


@certifications.route("/certifications", methods=["GET"])
@handle_request()
def get_certifications():
    certifications = SustainabilityCertification.query.all()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Certifications retrieved successfully",
                "data": [cert.to_dict() for cert in certifications],
            }
        ),
        200,
    )


@certifications.route("/product-certifications", methods=["GET"])
@handle_request()
def get_product_certifications():
    certifications = ProductCertification.query.all()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Product certifications retrieved successfully",
                "data": [cert.to_dict() for cert in certifications],
            }
        ),
        200,
    )


@certifications.route("/product-certifications/<int:product_id>", methods=["GET"])
@handle_request()
def get_product_certification(product_id):
    certifications = ProductCertification.query.filter_by(product_id=product_id).all()
    if not certifications:
        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"No certifications found for product {product_id}",
                    "data": [],
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "status": "success",
                "message": "Product certifications retrieved successfully",
                "data": [cert.to_dict() for cert in certifications],
            }
        ),
        200,
    )


@certifications.route(
    "/product-certifications/<int:certification_id>/verify", methods=["POST"]
)
@jwt_required()
@handle_request()
@role_required("admin")  # Only admins can verify certifications
def verify_certification(certification_id):
    certification = ProductCertification.query.get(certification_id)
    if not certification:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Certification with id {certification_id} not found",
                }
            ),
            404,
        )

    try:
        certification.status = "approved"
        certification.verification_date = datetime.now(timezone.utc)
        certification.verified_by = get_jwt_identity()

        # Update the product's sustainable status
        if certification.product:
            certification.product.is_sustainable = True

        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Certification verified successfully",
                    "data": certification.to_dict(),
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
