"""Small formatting helpers for emails and labels."""

def https(url: str) -> str:
    """Ensure a URL has an https:// scheme."""
    if url and not url.startswith(("http://", "https://")):
        return "https://" + url
    return url or "#"


def label(url: str) -> str:
    """Strip scheme and trailing slash to get a readable domain label."""
    if not url:
        return "our website"
    return url.replace("https://", "").replace("http://", "").rstrip("/")


def dash(value: str) -> str:
    """Return the value or a dash if empty/None."""
    return value if value else "-"

