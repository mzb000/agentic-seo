"""Structured Data & Schema.org Audit Tool for MZ SEO Agent."""

from typing import Dict, Any, List


VALID_SCHEMAS = {
    "organization", "website", "webpage", "article", "blogposting",
    "product", "breadcrumblist", "faqpage", "localbusiness", "person"
}


def run_schema_audit(parse_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates JSON-LD schema objects for required contexts, types, and rich-result readiness.
    """
    schemas = parse_result.get("schemas", [])
    issues: List[Dict[str, str]] = []
    detected_types: List[str] = []
    score = 100

    if not schemas:
        score = 0
        issues.append({
            "severity": "HIGH",
            "check": "Structured Data",
            "message": "No JSON-LD structured data detected on page. Schema improves rich snippet eligibility."
        })
        return {
            "score": score,
            "grade": "F",
            "detected_schemas_count": 0,
            "detected_types": [],
            "issues_count": len(issues),
            "issues": issues,
        }

    for idx, item in enumerate(schemas, start=1):
        if "error" in item:
            score -= 30
            issues.append({
                "severity": "HIGH",
                "check": "Schema Syntax",
                "message": f"Block #{idx} contains invalid JSON-LD syntax."
            })
            continue

        # Check @context
        context = item.get("@context", "")
        if "schema.org" not in str(context).lower():
            score -= 15
            issues.append({
                "severity": "MEDIUM",
                "check": "Schema Context",
                "message": f"Block #{idx} has invalid or missing @context (expected 'https://schema.org')."
            })

        # Check @type
        schema_type = item.get("@type", "")
        if isinstance(schema_type, list):
            for t in schema_type:
                detected_types.append(str(t))
        elif schema_type:
            detected_types.append(str(schema_type))
        else:
            score -= 15
            issues.append({
                "severity": "HIGH",
                "check": "Schema Type",
                "message": f"Block #{idx} is missing @type declaration."
            })

    score = max(0, min(100, score))
    return {
        "score": score,
        "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 50 else "F",
        "detected_schemas_count": len(schemas),
        "detected_types": list(set(detected_types)),
        "issues_count": len(issues),
        "issues": issues,
    }
