"""Mailgun email sending utilities for lead notifications."""

import base64
import json
from urllib import error, parse, request

from config.settings import MAILGUN_CONFIGS
from mailer import admin_template, user_template
from utils.helpers import label


def get_mailgun_config(website_key: str) -> dict:
    """Return the Mailgun config for the given website."""
    cfg = MAILGUN_CONFIGS["wowpbx"]
    required_fields = ("api_key", "domain", "from_email")

    missing = [field for field in required_fields if not cfg.get(field)]
    if missing:
        raise ValueError(
            f"Missing Mailgun configuration for wowpbx: {', '.join(missing)}"
        )

    admin_emails = cfg.get("admin_emails") or [cfg["from_email"]]
    return {**cfg, "admin_emails": admin_emails}


def _post_message(cfg: dict, payload: dict) -> None:
    """Send one message through the Mailgun API."""
    data = parse.urlencode(payload, doseq=True).encode()
    api_url = f"https://api.mailgun.net/v3/{cfg['domain']}/messages"
    auth = base64.b64encode(f"api:{cfg['api_key']}".encode()).decode()
    req = request.Request(api_url, data=data, method="POST")
    req.add_header("Authorization", f"Basic {auth}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with request.urlopen(req, timeout=20) as response:
            response.read()
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Mailgun request failed: {exc.code} {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Mailgun connection failed: {exc.reason}") from exc


def send_lead_emails_via_mailgun(to_email: str, name: str, phone: str, message: str,
                                 website_key: str, product: str, product_type: str,
                                 ip_address: str) -> None:
    """Send confirmation and admin emails through Mailgun."""
    cfg = get_mailgun_config(website_key)
    lbl = label(website_key)
    from_header = f"{cfg['from_name']} <{cfg['from_email']}>"

    _post_message(
        cfg,
        {
            "from": from_header,
            "to": [to_email],
            "subject": "We received your message",
            "html": user_template.build(name, website_key),
        },
    )
    _post_message(
        cfg,
        {
            "from": f"Lead Alerts <{cfg['from_email']}>",
            "to": cfg["admin_emails"],
            "subject": f"New lead from {name} via {lbl}",
            "html": admin_template.build(
                name, to_email, phone, message,
                website_key, product, product_type, ip_address,
            ),
        },
    )

    print(
        f"Mailgun emails sent: user: {to_email} | admins: "
        f"{', '.join(cfg['admin_emails'])}"
    )
