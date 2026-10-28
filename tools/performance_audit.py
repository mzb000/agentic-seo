"""Performance & Latency Audit Tool for MZ SEO Agent."""

from typing import Dict, Any, List


def run_performance_audit(fetch_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates response latency, payload weight, redirect overhead, and compression headers.
    """
    issues: List[Dict[str, str]] = []
    score = 100

    # 1. Latency (TTFB)
    latency_ms = fetch_result.get("latency_ms", 0)
    if latency_ms > 1500:
        score -= 30
        issues.append({
            "severity": "HIGH",
            "check": "Server Response Time (TTFB)",
            "message": f"High response latency ({latency_ms} ms). Target TTFB is under 600 ms."
        })
    elif latency_ms > 600:
        score -= 15
        issues.append({
            "severity": "MEDIUM",
            "check": "Server Response Time (TTFB)",
            "message": f"Moderate response latency ({latency_ms} ms). Can be optimized with caching/CDN."
        })

    # 2. HTML Payload Size
    content_len = fetch_result.get("content_length", 0)
    size_kb = round(content_len / 1024, 2)
    if size_kb > 250:
        score -= 20
        issues.append({
            "severity": "HIGH",
            "check": "HTML Payload Size",
            "message": f"Excessive raw HTML payload ({size_kb} KB). Keep base HTML under 100 KB."
        })
    elif size_kb > 100:
        score -= 10
        issues.append({
            "severity": "LOW",
            "check": "HTML Payload Size",
            "message": f"Large HTML document ({size_kb} KB). Consider minifying DOM nodes."
        })

    # 3. Compression Header Check
    headers = fetch_result.get("headers", {})
    encoding = headers.get("content-encoding", "").lower()
    if not encoding or ("gzip" not in encoding and "br" not in encoding):
        score -= 15
        issues.append({
            "severity": "MEDIUM",
            "check": "Text Compression",
            "message": "Missing Gzip or Brotli compression headers on HTTP response."
        })

    # 4. Redirect Overhead
    redirects = fetch_result.get("redirect_count", 0)
    if redirects > 2:
        score -= 15
        issues.append({
            "severity": "HIGH",
            "check": "Redirect Chains",
            "message": f"Excessive redirect chain ({redirects} hops) delays initial page render."
        })
    elif redirects > 0:
        score -= 5
        issues.append({
            "severity": "LOW",
            "check": "Redirect Chain",
            "message": f"Page redirected {redirects} time(s). Update internal links to point directly to final URL."
        })

    score = max(0, min(100, score))
    return {
        "score": score,
        "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 50 else "F",
        "latency_ms": latency_ms,
        "payload_kb": size_kb,
        "compression": encoding if encoding else "None",
        "redirect_hops": redirects,
        "issues_count": len(issues),
        "issues": issues,
    }
