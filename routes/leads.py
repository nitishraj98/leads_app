from flask import Blueprint, request, jsonify

from config.settings import API_KEY
from db.database import fetch_leads

leads_bp = Blueprint("leads", __name__)


@leads_bp.route("/leads", methods=["GET"])
def get_leads():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        website_key = request.args.get("website_key", "").strip()
        limit       = int(request.args.get("limit",  50))
        offset      = int(request.args.get("offset",  0))

        leads, total = fetch_leads(website_key or None, limit, offset)

        return jsonify({
            "success": True,
            "total":   total,
            "limit":   limit,
            "offset":  offset,
            "leads":   leads,
        })

    except Exception as e:
        print(f"Error fetching leads: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
