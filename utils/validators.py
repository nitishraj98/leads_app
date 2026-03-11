"""Validation helpers for form submissions."""

from email_validator import validate_email, EmailNotValidError


def is_valid_email(email: str) -> bool:
    """Return True when the email passes validation."""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def is_spam(data: dict) -> bool:
    """Return True when the honeypot field was filled."""
    return bool(data.get("company"))

