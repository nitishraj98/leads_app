"""Push lead submissions into Zoho CRM as Leads."""

import json
import time
from urllib import error, parse, request

from config.settings import ZOHO_CONFIG
from utils.helpers import label

_token_cache = {"access_token": None, "expires_at": 0}


def _get_access_token() -> str:
    """Return a cached Zoho OAuth access token, refreshing it if expired."""
    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["access_token"]

    data = parse.urlencode({
        "refresh_token": ZOHO_CONFIG["refresh_token"],
        "client_id": ZOHO_CONFIG["client_id"],
        "client_secret": ZOHO_CONFIG["client_secret"],
        "grant_type": "refresh_token",
    }).encode()
    url = f"{ZOHO_CONFIG['accounts_url']}/oauth/v2/token"
    req = request.Request(url, data=data, method="POST")

    try:
        with request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode())
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Zoho token refresh failed: {exc.code} {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Zoho token refresh connection failed: {exc.reason}") from exc

    if "access_token" not in payload:
        raise RuntimeError(f"Zoho token refresh response missing access_token: {payload}")

    _token_cache["access_token"] = payload["access_token"]
    _token_cache["expires_at"] = time.time() + payload.get("expires_in", 3600) - 60
    return _token_cache["access_token"]


def create_lead(name: str, email: str, phone: str, message: str,
                website_key: str, product: str, product_type: str,
                ip_address: str, campaign: str = "", source: str = "") -> None:
    """Create a Lead record in Zoho CRM for a form submission."""
    if not ZOHO_CONFIG.get("client_id") or not ZOHO_CONFIG.get("refresh_token"):
        return

    access_token = _get_access_token()

    name_parts = name.strip().split(maxsplit=1) 
    first_name = name_parts[0] if name_parts else ""
    last_name = name_parts[1] if len(name_parts) > 1 else name_parts[0]
    

    description_lines = [message]
    if product:
        description_lines.append(f"Product: {product}")
    if product_type:
        description_lines.append(f"Product type: {product_type}")
    if campaign:
        description_lines.append(f"Campaign: {campaign}")
    if source:
        description_lines.append(f"Source: {source}")
    if ip_address:
        description_lines.append(f"IP address: {ip_address}")

    lead = {
        "Last_Name": last_name,
        "First_Name": first_name,
        "Email": email,
        "Phone": phone,
        "Company": label(website_key),
        "Lead_Source": "Website",
        "Description": "\n".join(description_lines),
    }

    body = json.dumps({"data": [lead]}).encode()
    url = f"{ZOHO_CONFIG['api_domain']}/crm/v3/Leads"
    req = request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Zoho-oauthtoken {access_token}")
    req.add_header("Content-Type", "application/json")

    try:
        with request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode())
    except error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Zoho lead creation failed: {exc.code} {body_text}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Zoho lead creation connection failed: {exc.reason}") from exc

    result = (payload.get("data") or [{}])[0]
    if result.get("status") != "success":
        raise RuntimeError(f"Zoho lead creation rejected: {result}")

    zoho_id = result.get("details", {}).get("id")
    print(f"Zoho lead created: {email} -> {zoho_id}")
