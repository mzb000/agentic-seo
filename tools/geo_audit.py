"""Generative Engine Optimization (GEO) & AI Search Audit Tool for MZ SEO Agent."""

import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup


def run_geo_audit(html: str, parse_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates page readiness for AI search engine citation (Google AI Overviews, Perplexity, ChatGPT).
    Analyzes question headings, definition paragraphs, structured lists, and data citations.
    """
    issues: List[Dict[str, str]] = []
    score = 100
    soup = BeautifulSoup(html, "html.parser")

    # 1. Question-Based Headings (Query Matching for AI)
    headings = parse_result.get("headings", {})
    all_headings = headings.get("h1", []) + headings.get("h2", []) + headings.get("h3", [])
    question_regex = re.compile(r"^(what|how|why|when|where|who|is|can|are|best|top)\b", re.I)
    question_headings = [h for h in all_headings if question_regex.search(h) or "?" in h]

    if len(question_headings) == 0:
        score -= 25
        issues.append({
            "severity": "HIGH",
            "check": "AI Query Headings",
            "message": "Zero question-based headings found. AI search engines extract answers directly below query-framed headings."
        })
    elif len(question_headings) < 2:
        score -= 10
        issues.append({
            "severity": "MEDIUM",
            "check": "AI Query Headings",
            "message": "Only 1 question-based heading found. Add explicit question headers (e.g., 'What is...', 'How to...')."
        })

    # 2. Structured Lists & Tables (Information Extraction)
    lists_count = len(soup.find_all(["ul", "ol"]))
    tables_count = len(soup.find_all("table"))

    if lists_count == 0 and tables_count == 0:
        score -= 20
        issues.append({
            "severity": "HIGH",
            "check": "Structured Lists/Tables",
            "message": "No HTML lists or tables detected. LLMs preferentially cite structured tabular and bulleted data."
        })

    # 3. Direct Definition Format (Snippet extraction)
    # Check if any paragraph starts with a definition phrase
    paragraphs = [p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 30]
    has_concise_definition = any(len(p) <= 300 and (" is " in p or " refers to " in p or " means " in p) for p in paragraphs[:5])

    if not has_concise_definition:
        score -= 15
        issues.append({
            "severity": "MEDIUM",
            "check": "Direct Answer Snippet",
            "message": "Missing concise 40-60 word definition paragraph in opening section for featured snippet capture."
        })

    # 4. Schema Verification for AI
    has_schema = parse_result.get("schemas", [])
    if not has_schema:
        score -= 20
        issues.append({
            "severity": "HIGH",
            "check": "AI Entity Recognition",
            "message": "Missing structured schema; AI search models require entity metadata to confirm source authority."
        })

    score = max(0, min(100, score))
    return {
        "score": score,
        "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 50 else "F",
        "question_headings_count": len(question_headings),
        "structured_lists_count": lists_count,
        "tables_count": tables_count,
        "issues_count": len(issues),
        "issues": issues,
    }
