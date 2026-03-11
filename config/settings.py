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
EMAIL_CONFIG = {
    "smtp_host":       os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "smtp_port":       int(os.getenv("SMTP_PORT", 587)),
    "sender_email":    os.getenv("SENDER_EMAIL"),
    "sender_password": os.getenv("SENDER_PASSWORD"),
}
ADMIN_EMAILS = [
    EMAIL_CONFIG["sender_email"],
    "nitishtics@gmail.com",
]
DEFAULT_RATE_LIMIT = "20 per minute"
SUBMIT_RATE_LIMIT  = "5 per minute"

