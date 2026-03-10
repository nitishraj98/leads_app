from flask import Blueprint, request, jsonify

from config.settings import SUBMIT_RATE_LIMIT
from db.database import save_lead
from mailer.sender import send_lead_emails
from utils.validators import is_valid_email, is_valid_phone, is_spam

submit_bp = Blueprint("submit", __name__)


@submit_bp.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"success": False, "message": "Invalid or missing JSON body."}), 400

    name         = data.get("name",         "").strip()
    email        = data.get("email",        "").strip()
    phone        = data.get("phone",        "").strip()
    message      = data.get("message",      "").strip()
    website_key  = data.get("website_key",  "").strip()
    product      = data.get("product",      "").strip()
    product_type = data.get("product_type", "").strip()

    # Honeypot
    if is_spam(data):
        return jsonify({"success": False, "message": "Spam detected."}), 422

    # Required fields 
    if not name or not email:
        return jsonify({"success": False, "message": "Name and email are required."}), 400

    # Email format
    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email address."}), 422

    # Phone format (only when provided)
    if phone and not is_valid_phone(phone):
        return jsonify({"success": False, "message": "Invalid phone number."}), 422

    # Message length
    if len(message) > 1000:
        return jsonify({"success": False, "message": "Message too long (max 1000 chars)."}), 422

    try:
        save_lead(name, email, phone, message, website_key, product, product_type)
        send_lead_emails(email, name, phone, message, website_key, product, product_type)
        return jsonify({"success": True,
                        "message": "Submitted! Check your email for confirmation."}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500