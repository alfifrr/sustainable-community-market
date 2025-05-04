from flask import Blueprint, jsonify
from app.models import ItemTransaction, StatusType
from app.utils.decorators import handle_request
from sqlalchemy import desc, func

product_review = Blueprint("product_review", __name__, url_prefix="/api")


@product_review.route("/products/<int:product_id>/reviews", methods=["GET"])
@handle_request()
def get_product_reviews(product_id):
    """Get all reviews for a specific product"""
    try:
        # Get all completed transactions (DELIVERED/RATED) with reviews for this product
        reviews = (
            ItemTransaction.query.filter(
                ItemTransaction.product_id == product_id,
                ItemTransaction.rating.isnot(
                    None
                ),  # Only get transactions with ratings
            )
            .order_by(desc(ItemTransaction.review_date))
            .all()
        )

        # Calculate total items sold (including DELIVERED and RATED status)
        total_sold = (
            ItemTransaction.query.with_entities(func.sum(ItemTransaction.quantity))
            .filter(
                ItemTransaction.product_id == product_id,
                ItemTransaction.delivery_status.in_(
                    [StatusType.DELIVERED, StatusType.RATED]
                ),
            )
            .scalar()
            or 0
        )

        if not reviews:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "No reviews found for this product",
                        "data": {
                            "product_id": product_id,
                            "total_items_sold": int(total_sold),
                            "reviews": [],
                        },
                    }
                ),
                200,
            )

        reviews_data = []
        for review in reviews:
            reviews_data.append(
                {
                    "rating": review.rating,
                    "testimonial": review.testimonial,
                    "review_date": (
                        review.review_date.isoformat() if review.review_date else None
                    ),
                    "reviewer": {
                        "id": review.buyer.id,
                        "name": f"{review.buyer.first_name} {review.buyer.last_name}",
                    },
                }
            )

        # Calculate average rating
        avg_rating = sum(review.rating for review in reviews) / len(reviews)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Product reviews retrieved successfully",
                    "data": {
                        "product_id": product_id,
                        "total_items_sold": int(total_sold),
                        "total_reviews": len(reviews),
                        "average_rating": round(avg_rating, 1),
                        "reviews": reviews_data,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": "Server error", "message": str(e)}),
            500,
        )
