"""Validation helpers for form submissions."""

import re

from email_validator import validate_email, EmailNotValidError


def is_valid_email(email: str) -> bool:
    """Return True when the email passes validation."""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def _max_repeated_run(text: str) -> int:
    """Return the longest run of repeated alphabetic characters."""
    run = 1
    max_run = 1
    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 1
    return max_run


def is_gibberish(text: str) -> bool:
    """Return True when a short name-like value looks like keyboard mashing."""
    if not text:
        return False
    stripped = text.strip()
    if not stripped:
        return False

    cleaned = "".join(ch for ch in stripped.lower() if ch.isalpha())
    if len(cleaned) < 6:
        return False
    vowels = sum(ch in "aeiou" for ch in cleaned)
    vowel_ratio = vowels / len(cleaned)
    if vowel_ratio < 0.2 or vowel_ratio > 0.8:
        return True
    return _max_repeated_run(cleaned) >= 3


def is_invalid_message(text: str) -> bool:
    """Return True when a message looks machine-generated or like keyboard mashing."""
    if not text:
        return False

    stripped = text.strip()
    if not stripped:
        return False

    # Allow short structured replies such as ratings or availability notes.
    if len(stripped) <= 10 and any(ch.isdigit() for ch in stripped):
        return False

    cleaned = "".join(ch for ch in stripped.lower() if ch.isalpha())
    if not cleaned:
        return False

    alpha_words = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", stripped)

    # Multi-word human sentences should pass even with typos.
    if len(alpha_words) >= 3 and len(cleaned) >= 12:
        return False

    if len(cleaned) < 6:
        return False

    vowels = sum(ch in "aeiou" for ch in cleaned)
    vowel_ratio = vowels / len(cleaned)
    max_run = _max_repeated_run(cleaned)

    if max_run >= 4:
        return True

    if " " not in stripped and (vowel_ratio < 0.2 or vowel_ratio > 0.8):
        return True

    unique_ratio = len(set(cleaned)) / len(cleaned)
    return " " not in stripped and unique_ratio < 0.3
