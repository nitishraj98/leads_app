"""Small formatting helpers for emails and labels."""

from urllib.parse import urlparse

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


def website_slug(value: str) -> str:
    """Normalize a website key like rirabh, rirabh.com, or a full URL."""
    raw = (value or "").strip().lower()
    if not raw:
        return "default"

    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = parsed.netloc or parsed.path
    host = host.split("/")[0].replace("www.", "")

    if host.startswith("rirabh"):
        return "rirabh"
    if host.startswith("callerspot"):
        return "callerspot"
    if host.startswith("wowpbx"):
        return "wowpbx"
    return "default"

