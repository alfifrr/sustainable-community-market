from flask import Blueprint, jsonify
from app.models import Category
from app.utils.decorators import handle_request

category = Blueprint("category", __name__)


@category.route("/category", methods=["GET"])
@handle_request()
def get_item_history():
    category = Category.query.all()
    if not category:
        return (
            jsonify(
                {"status": "success", "message": "No category found", "data": []}),
            200,
        )
    return (
        jsonify(
            {
                "status": "success",
                "message": "Category retrieved successfully",
                "data": [c.to_dict() for c in category],
            }
        ),
        201,
    )
