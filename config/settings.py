"""Application configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY    = os.getenv("LEADS_API_KEY")
DB_CONFIG = {
    "host":     os.getenv("DB_HOST"),
    "port":     os.getenv("DB_PORT", 5432),
    "dbname":   os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}
DEFAULT_SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
DEFAULT_SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
LEGACY_SENDER_EMAIL = os.getenv("SENDER_EMAIL")
LEGACY_SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
LEGACY_ADMIN_EMAILS = [
    email.strip()
    for email in os.getenv("ADMIN_EMAILS", "").split(",")
    if email.strip()
]
if not LEGACY_ADMIN_EMAILS and LEGACY_SENDER_EMAIL:
    LEGACY_ADMIN_EMAILS = [LEGACY_SENDER_EMAIL, "gautam@rirabh.com"]


def build_email_config(prefix: str, fallback_email=None, fallback_password=None,
                       fallback_admin_emails=None) -> dict:
    """Build one SMTP config block from env vars."""
    return {
        "smtp_host": os.getenv(f"{prefix}_SMTP_HOST", DEFAULT_SMTP_HOST),
        "smtp_port": int(os.getenv(f"{prefix}_SMTP_PORT", DEFAULT_SMTP_PORT)),
        "sender_email": os.getenv(f"{prefix}_SENDER_EMAIL", fallback_email),
        "sender_password": os.getenv(f"{prefix}_SENDER_PASSWORD", fallback_password),
        "admin_emails": [
            email.strip()
            for email in os.getenv(
                f"{prefix}_ADMIN_EMAILS",
                ",".join(fallback_admin_emails or []),
            ).split(",")
            if email.strip()
        ],
    }


DEFAULT_EMAIL_CONFIG = {
    "smtp_host": DEFAULT_SMTP_HOST,
    "smtp_port": DEFAULT_SMTP_PORT,
    "sender_email": LEGACY_SENDER_EMAIL,
    "sender_password": LEGACY_SENDER_PASSWORD,
    "admin_emails": LEGACY_ADMIN_EMAILS,
}


EMAIL_CONFIGS = {
    "rirabh": build_email_config(
        "RIRABH",
        fallback_email=LEGACY_SENDER_EMAIL,
        fallback_password=LEGACY_SENDER_PASSWORD,
        fallback_admin_emails=LEGACY_ADMIN_EMAILS,
    ),
    "callerspot": build_email_config(
        "CALLERSPOT",
        fallback_email=LEGACY_SENDER_EMAIL,
        fallback_password=LEGACY_SENDER_PASSWORD,
        fallback_admin_emails=LEGACY_ADMIN_EMAILS,
    ),
    "wowphone": build_email_config(
        "WOWPHONE",
        fallback_email=LEGACY_SENDER_EMAIL,
        fallback_password=LEGACY_SENDER_PASSWORD,
        fallback_admin_emails=LEGACY_ADMIN_EMAILS,
    ),
}
MAILGUN_CONFIGS = {
    "wowpbx": {
        "api_key": os.getenv("WOWPBX_MAILGUN_API_KEY"),
        "domain": os.getenv("WOWPBX_MAILGUN_DOMAIN"),
        "from_email": os.getenv("WOWPBX_MAILGUN_FROM_EMAIL"),
        "from_name": os.getenv("WOWPBX_MAILGUN_FROM_NAME", "wowpbx"),
        "admin_emails": [
            email.strip()
            for email in os.getenv("WOWPBX_MAILGUN_ADMIN_EMAILS", "").split(",")
            if email.strip()
        ],
    },
}
DEFAULT_RATE_LIMIT = "20 per minute"
SUBMIT_RATE_LIMIT  = "5 per minute"
