import os
from dotenv import load_dotenv

load_dotenv()

# ── Flask ──────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY    = os.getenv("LEADS_API_KEY")

# ── Database ───────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST"),
    "port":     os.getenv("DB_PORT", 5432),
    "dbname":   os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# ── Email / SMTP ───────────────────────────────────────────────────
EMAIL_CONFIG = {
    "smtp_host":       os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "smtp_port":       int(os.getenv("SMTP_PORT", 587)),
    "sender_email":    os.getenv("SENDER_EMAIL"),
    "sender_password": os.getenv("SENDER_PASSWORD"),
}

# ── Admin recipients ───────────────────────────────────────────────
ADMIN_EMAILS = [
    EMAIL_CONFIG["sender_email"],
    "gautam@rirabh.com",
]

# ── Rate limits ────────────────────────────────────────────────────
DEFAULT_RATE_LIMIT = "20 per minute"
SUBMIT_RATE_LIMIT  = "5 per minute"
