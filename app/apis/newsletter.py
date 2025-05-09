from flask import Blueprint, request, jsonify
from app.utils.email import send_newsletter_email

newsletter_bp = Blueprint('newsletter', __name__)


@newsletter_bp.route('/subscribe', methods=['POST'])
def subscribe_to_newsletter():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        explore_url = "https://sustainable-community-market.com/products"
        unsubscribe_url = f"https://sustainable-community-market.com/unsubscribe?email={email}"
        send_newsletter_email(email, explore_url, unsubscribe_url)
        return jsonify({"message": "Subscription successful. Check your email for details."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
