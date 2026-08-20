"""Email sending utilities for lead notifications."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import DEFAULT_EMAIL_CONFIG, EMAIL_CONFIGS
from mailer.mailgun_sender import send_lead_emails_via_mailgun
from utils.helpers import label, website_slug
from mailer import user_template, admin_template


def get_email_config(website_key: str) -> dict:
    """Return the SMTP config for the given website."""
    slug = website_slug(website_key)
    cfg = EMAIL_CONFIGS.get(slug, EMAIL_CONFIGS["rirabh"])

    if not cfg.get("sender_email") or not cfg.get("sender_password"):
        raise ValueError(f"Missing sender email configuration for website key: {slug}")

    admin_emails = cfg.get("admin_emails") or [cfg["sender_email"]]
    return {**cfg, "admin_emails": admin_emails}

  
def get_default_email_config() -> dict:
    """Return the default SMTP configuration used as the WowPhone fallback."""
    cfg = DEFAULT_EMAIL_CONFIG
    if not cfg.get("sender_email") or not cfg.get("sender_password"):
        raise ValueError("Missing default sender email configuration")

    admin_emails = cfg.get("admin_emails") or [cfg["sender_email"]]
    return {**cfg, "admin_emails": admin_emails}


def send_lead_emails(to_email: str, name: str, phone: str, message: str,
                     website_key: str, product: str, product_type: str,
                     ip_address: str, campaign: str = "", source: str = "") -> None:
    """Send confirmation email to user and notification email to admins."""
    slug = website_slug(website_key)
    if slug == "wowpbx":
        send_lead_emails_via_mailgun(
            to_email, name, phone, message,
            website_key, product, product_type, ip_address, campaign, source,
        )
        return

    cfg = get_email_config(website_key)
    lbl = label(website_key)
    def deliver(active_cfg: dict) -> None:
        user_msg = MIMEMultipart("alternative")
        user_msg["Subject"] = "We received your message"
        user_msg["From"] = f"{lbl} <{active_cfg['sender_email']}>"
        user_msg["To"] = to_email
        user_msg.attach(MIMEText(user_template.build(name, website_key), "html"))

        admin_msg = MIMEMultipart("alternative")
        admin_msg["Subject"] = f"New lead from {name} via {lbl}"
        admin_msg["From"] = f"Lead Alerts <{active_cfg['sender_email']}>"
        admin_msg["To"] = ", ".join(active_cfg["admin_emails"])
        admin_msg.attach(MIMEText(
            admin_template.build(name, to_email, phone, message,
                                 website_key, product, product_type, ip_address,
                                 campaign, source),
            "html",
        ))

        with smtplib.SMTP(active_cfg["smtp_host"], active_cfg["smtp_port"]) as server:
            server.starttls()
            server.login(active_cfg["sender_email"], active_cfg["sender_password"])
            user_refused = server.sendmail(active_cfg["sender_email"], to_email,
                                           user_msg.as_string())
            admin_refused = server.sendmail(active_cfg["sender_email"], active_cfg["admin_emails"],
                                            admin_msg.as_string())
            if user_refused:
                print(f"SMTP refused user recipient: {user_refused}")
            if admin_refused:
                print(f"SMTP refused admin recipients: {admin_refused}")

    try:
        deliver(cfg)
    except (smtplib.SMTPException, OSError) as exc:
        if slug != "wowphone":
            raise

        fallback_cfg = get_default_email_config()
        if fallback_cfg == cfg:
            raise

        print(f"WowPhone SMTP failed ({exc}); retrying with default SMTP")
        cfg = fallback_cfg
        deliver(cfg)

    print(f"Emails sent: user: {to_email} | admins: {', '.join(cfg['admin_emails'])}")

