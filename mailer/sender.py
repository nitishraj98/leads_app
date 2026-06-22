"""Email sending utilities for lead notifications."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import EMAIL_CONFIGS
from mailer.mailgun_sender import send_lead_emails_via_mailgun
from utils.helpers import label, website_slug
from mailer import user_template, admin_template


def get_email_config(website_key: str) -> dict:
    """Return the SMTP config for the given website."""
    slug = website_slug(website_key)
    cfg = EMAIL_CONFIGS["callerspot"] if slug == "callerspot" else EMAIL_CONFIGS["rirabh"]

    if not cfg.get("sender_email") or not cfg.get("sender_password"):
        raise ValueError(f"Missing sender email configuration for website key: {slug}")

    admin_emails = cfg.get("admin_emails") or [cfg["sender_email"]]
    return {**cfg, "admin_emails": admin_emails}


def send_lead_emails(to_email: str, name: str, phone: str, message: str,
                     website_key: str, product: str, product_type: str,
                     ip_address: str) -> None:
    """Send confirmation email to user and notification email to admins."""
    if website_slug(website_key) == "wowpbx":
        send_lead_emails_via_mailgun(
            to_email, name, phone, message,
            website_key, product, product_type, ip_address,
        )
        return

    cfg = get_email_config(website_key)
    lbl = label(website_key)
    user_msg = MIMEMultipart("alternative")
    user_msg["Subject"] = "We received your message"
    user_msg["From"]    = f"{lbl} <{cfg['sender_email']}>"
    user_msg["To"]      = to_email
    user_msg.attach(MIMEText(user_template.build(name, website_key), "html"))
    admin_msg = MIMEMultipart("alternative")
    admin_msg["Subject"] = f"New lead from {name} via {lbl}"
    admin_msg["From"]    = f"Lead Alerts <{cfg['sender_email']}>"
    admin_msg["To"]      = ", ".join(cfg["admin_emails"])
    admin_msg.attach(MIMEText(
        admin_template.build(name, to_email, phone, message,
                             website_key, product, product_type, ip_address),
        "html",
    ))

    with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as server:
        server.starttls()
        server.login(cfg["sender_email"], cfg["sender_password"])
        server.sendmail(cfg["sender_email"], to_email, user_msg.as_string())
        server.sendmail(cfg["sender_email"], cfg["admin_emails"], admin_msg.as_string())

    print(f"Emails sent: user: {to_email} | admins: {', '.join(cfg['admin_emails'])}")

