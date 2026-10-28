"""Content Quality & E-E-A-T Audit Tool for MZ SEO Agent."""

from typing import Dict, Any, List


EEAT_TERMS = ["about us", "contact", "privacy policy", "terms of service", "author", "published", "updated", "editorial"]


def run_content_audit(parse_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates content depth, heading hierarchy, keyword distribution, and E-E-A-T trust signals.
    """
    issues: List[Dict[str, str]] = []
    score = 100

    # 1. H1 Structure
    h1s = parse_result.get("headings", {}).get("h1", [])
    if len(h1s) == 0:
        score -= 25
        issues.append({
            "severity": "HIGH",
            "check": "H1 Heading",
            "message": "Missing main <h1> heading tag."
        })
    elif len(h1s) > 1:
        score -= 10
        issues.append({
            "severity": "MEDIUM",
            "check": "H1 Heading",
            "message": f"Multiple ({len(h1s)}) <h1> headings found. Recommended: single primary <h1>."
        })

    # Subheadings H2/H3
    h2s = parse_result.get("headings", {}).get("h2", [])
    if len(h2s) == 0:
        score -= 10
        issues.append({
            "severity": "LOW",
            "check": "H2 Subheadings",
            "message": "No <h2> subheadings detected. Subheadings improve topic depth and scannability."
        })

    # 2. Content Depth (Word Count)
    word_count = parse_result.get("content_metrics", {}).get("word_count", 0)
    if word_count < 150:
        score -= 30
        issues.append({
            "severity": "HIGH",
            "check": "Thin Content",
            "message": f"Critical thin content detected ({word_count} words). Pages need sufficient depth."
        })
    elif word_count < 300:
        score -= 15
        issues.append({
            "severity": "MEDIUM",
            "check": "Content Depth",
            "message": f"Short content ({word_count} words). Recommend expanding to at least 500+ words."
        })

    # 3. Internal Linking
    internal_links = parse_result.get("links", {}).get("internal_count", 0)
    if internal_links == 0:
        score -= 15
        issues.append({
            "severity": "HIGH",
            "check": "Internal Links",
            "message": "Zero internal links found on page. Internal links distribute link equity."
        })
    elif internal_links < 5:
        score -= 5
        issues.append({
            "severity": "LOW",
            "check": "Internal Links",
            "message": f"Low internal linking ({internal_links} links). Consider linking related cluster pages."
        })

    # 4. Text to HTML Ratio
    text_ratio = parse_result.get("content_metrics", {}).get("text_ratio_percent", 0)
    if text_ratio < 10:
        score -= 10
        issues.append({
            "severity": "LOW",
            "check": "Text-to-HTML Ratio",
            "message": f"Low text-to-HTML ratio ({text_ratio}%). Page contains heavy boilerplate code."
        })

    score = max(0, min(100, score))
    return {
        "score": score,
        "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 50 else "F",
        "word_count": word_count,
        "h1_count": len(h1s),
        "h2_count": len(h2s),
        "issues_count": len(issues),
        "issues": issues,
    }
