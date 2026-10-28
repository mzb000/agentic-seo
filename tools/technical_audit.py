"""Technical SEO Audit Tool for MZ SEO Agent."""

from typing import Dict, Any, List


def run_technical_audit(fetch_result: Dict[str, Any], parse_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates HTTP status, indexing directives, canonical tags, title/description lengths,
    and mobile readiness.
    """
    issues: List[Dict[str, str]] = []
    score = 100

    # 1. HTTP Status & Protocol
    status_code = fetch_result.get("status_code", 0)
    if status_code != 200:
        score -= 40
        issues.append({
            "severity": "HIGH",
            "check": "HTTP Status",
            "message": f"Page returned non-200 status code: {status_code}"
        })

    final_url = fetch_result.get("final_url", "")
    if not final_url.startswith("https://"):
        score -= 20
        issues.append({
            "severity": "HIGH",
            "check": "HTTPS Security",
            "message": "URL is not served over secure HTTPS protocol."
        })

    # 2. Meta Robots & Indexability
    robots = parse_result.get("meta_robots", "")
    if "noindex" in robots:
        score -= 30
        issues.append({
            "severity": "HIGH",
            "check": "Robots Indexability",
            "message": "Page contains 'noindex' directive, blocking search engine indexing."
        })

    # 3. Canonical Tag
    canonical = parse_result.get("canonical_url", "")
    if not canonical:
        score -= 10
        issues.append({
            "severity": "MEDIUM",
            "check": "Canonical Tag",
            "message": "Missing rel=canonical link tag."
        })
    elif canonical.rstrip("/") != final_url.rstrip("/"):
        issues.append({
            "severity": "LOW",
            "check": "Canonical Tag",
            "message": f"Canonical points to alternative URL: {canonical}"
        })

    # 4. Title Tag
    title_len = parse_result.get("title_length", 0)
    title_text = parse_result.get("title", "")
    if not title_text:
        score -= 20
        issues.append({
            "severity": "HIGH",
            "check": "Title Tag",
            "message": "Missing <title> tag."
        })
    elif title_len < 30:
        score -= 5
        issues.append({
            "severity": "LOW",
            "check": "Title Tag Length",
            "message": f"Title tag is too short ({title_len} chars). Optimal range: 30-60 characters."
        })
    elif title_len > 60:
        score -= 5
        issues.append({
            "severity": "LOW",
            "check": "Title Tag Length",
            "message": f"Title tag is too long ({title_len} chars). May be truncated in SERPs."
        })

    # 5. Meta Description
    desc_len = parse_result.get("meta_description_length", 0)
    if desc_len == 0:
        score -= 15
        issues.append({
            "severity": "MEDIUM",
            "check": "Meta Description",
            "message": "Missing meta description."
        })
    elif desc_len < 120 or desc_len > 160:
        score -= 5
        issues.append({
            "severity": "LOW",
            "check": "Meta Description Length",
            "message": f"Meta description length ({desc_len} chars) is outside optimal 120-160 range."
        })

    # 6. Mobile Viewport
    if not parse_result.get("has_viewport", False):
        score -= 15
        issues.append({
            "severity": "HIGH",
            "check": "Mobile Viewport",
            "message": "Missing viewport meta tag; page may fail mobile-friendly tests."
        })

    # 7. Images Alt Attributes
    images = parse_result.get("images", {})
    missing_alt = images.get("missing_alt_count", 0)
    total_images = images.get("total_count", 0)
    if missing_alt > 0:
        score -= min(10, missing_alt * 2)
        issues.append({
            "severity": "MEDIUM",
            "check": "Image Alt Attributes",
            "message": f"{missing_alt} out of {total_images} images are missing descriptive alt text."
        })

    score = max(0, min(100, score))
    return {
        "score": score,
        "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 50 else "F",
        "issues_count": len(issues),
        "issues": issues,
    }
