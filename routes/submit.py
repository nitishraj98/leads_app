"""Submission endpoint for lead forms."""

from flask import Blueprint, request, jsonify

from db.database import save_lead
from mailer.sender import send_lead_emails
from mailer.zoho_crm import create_lead as create_zoho_lead
from utils.validators import is_valid_email, is_gibberish, is_invalid_message

submit_bp = Blueprint("submit", __name__)


def get_client_ip(req) -> str:
    """Resolve the client IP from common proxy headers or remote address."""
    cf_ip = req.headers.get("CF-Connecting-IP", "").strip()
    if cf_ip:
        return cf_ip
    xff = req.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    xri = req.headers.get("X-Real-IP", "").strip()
    if xri:
        return xri
    return req.remote_addr or ""


@submit_bp.route("/submit", methods=["POST"])
def submit():
    """Accept and persist a lead submission."""
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
    campaign     = data.get("campaign",     "").strip()
    source       = data.get("source",       "").strip()
    ip_address   = get_client_ip(request)

    if not name or not email:
        return jsonify({"success": False, "message": "Name and email are required."}), 400

    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email address."}), 422

    if is_gibberish(name):
        return jsonify({"success": False, "message": "Please enter a valid name."}), 422
           
    if is_invalid_message(message):
        return jsonify({"success": False, "message": "Please enter a valid message."}), 422

    if len(message) > 1000:
        return jsonify({"success": False, "message": "Message too long (max 1000 chars)."}), 422

    try:
        save_lead(name, email, phone, message, website_key, product, product_type,
                  ip_address, campaign, source)
        send_lead_emails(email, name, phone, message, website_key, product, product_type,
                         ip_address, campaign, source)

        try:
            create_zoho_lead(name, email, phone, message, website_key, product, product_type,
                             ip_address, campaign, source)
        except Exception as zoho_exc:
            print(f"Zoho lead sync failed: {zoho_exc}")

        return jsonify({"success": True,
                        "message": "Submitted! Check your email for confirmation."}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
