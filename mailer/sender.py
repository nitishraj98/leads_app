import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import EMAIL_CONFIG, ADMIN_EMAILS
from utils.helpers import label
from mailer import user_template, admin_template


def send_lead_emails(to_email: str, name: str, phone: str, message: str,
                     website_key: str, product: str, product_type: str) -> None:
    cfg = EMAIL_CONFIG
    lbl = label(website_key)

    # ── User confirmation ──────────────────────────────────────────
    user_msg = MIMEMultipart("alternative")
    user_msg["Subject"] = "We received your message ✓"
    user_msg["From"]    = f"{lbl} <{cfg['sender_email']}>"
    user_msg["To"]      = to_email
    user_msg.attach(MIMEText(user_template.build(name, website_key), "html"))

    # ── Admin notification ─────────────────────────────────────────
    admin_msg = MIMEMultipart("alternative")
    admin_msg["Subject"] = f"New lead from {name} via {lbl}"
    admin_msg["From"]    = f"Lead Alerts <{cfg['sender_email']}>"
    admin_msg["To"]      = ", ".join(ADMIN_EMAILS)
    admin_msg.attach(MIMEText(
        admin_template.build(name, to_email, phone, message,
                             website_key, product, product_type),
        "html",
    ))

    with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as server:
        server.starttls()
        server.login(cfg["sender_email"], cfg["sender_password"])
        server.sendmail(cfg["sender_email"], to_email, user_msg.as_string())
        server.sendmail(cfg["sender_email"], ADMIN_EMAILS, admin_msg.as_string())

    print(f"✅ Emails sent → user: {to_email} | admins: {', '.join(ADMIN_EMAILS)}")
