import re
from email_validator import validate_email, EmailNotValidError


def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def is_valid_phone(phone: str) -> bool:
    """Accepts exactly 10 digits (extend the pattern as needed)."""
    return bool(re.match(r'^[0-9]{10}$', phone))


def is_spam(data: dict) -> bool:
    """Honeypot check — bots fill hidden 'company' field."""
    return bool(data.get("company"))
