"""Safe HTTP Page Fetcher for MZ SEO Agent."""

import time
import requests
from typing import Dict, Any
from core.security import validate_url


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 (compatible; MZ-SEO-Agent/1.0)"
)


class PageFetchError(Exception):
    """Raised when page fetching fails or is blocked by security policies."""
    pass


def fetch_page(url: str, timeout: int = 15, user_agent: str = DEFAULT_USER_AGENT) -> Dict[str, Any]:
    """
    Fetches a web page safely with timeout, redirection tracking, and latency metrics.
    """
    is_safe, reason = validate_url(url)
    if not is_safe:
        raise PageFetchError(f"URL Safety Check Failed: {reason}")

    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    start_time = time.perf_counter()
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True,
            verify=True,
        )
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    except requests.exceptions.SSLError as e:
        raise PageFetchError(f"SSL Certificate Verification Failed: {str(e)}")
    except requests.exceptions.Timeout:
        raise PageFetchError(f"Connection Timed Out after {timeout} seconds.")
    except requests.exceptions.RequestException as e:
        raise PageFetchError(f"Network request failed: {str(e)}")

    # Ensure accurate encoding resolution (e.g. for Turkish, UTF-8, etc.)
    if not response.encoding or response.encoding.lower() in ("iso-8859-1", "ascii"):
        response.encoding = response.apparent_encoding or "utf-8"

    redirect_history = [
        {"url": r.url, "status_code": r.status_code} for r in response.history
    ]

    return {
        "requested_url": url,
        "final_url": response.url,
        "status_code": response.status_code,
        "latency_ms": latency_ms,
        "redirect_count": len(response.history),
        "redirect_history": redirect_history,
        "content_type": response.headers.get("Content-Type", ""),
        "content_length": len(response.content),
        "headers": dict(response.headers),
        "html": response.text,
    }
