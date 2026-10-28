"""Master Audit Orchestrator for MZ SEO Agent."""

from typing import Dict, Any
from core.fetcher import fetch_page
from core.parser import parse_html
from tools.technical_audit import run_technical_audit
from tools.content_audit import run_content_audit
from tools.performance_audit import run_performance_audit
from tools.schema_audit import run_schema_audit
from tools.geo_audit import run_geo_audit


class Orchestrator:
    """Coordinates specialist audit modules and compiles holistic SEO evaluations."""

    @staticmethod
    def audit_url(url: str) -> Dict[str, Any]:
        """
        Executes an end-to-end multi-agent SEO audit on the target URL.
        """
        fetch_result = fetch_page(url)
        html = fetch_result["html"]
        parse_result = parse_html(html, base_url=fetch_result["final_url"])

        # Execute specialized audits
        technical = run_technical_audit(fetch_result, parse_result)
        content = run_content_audit(parse_result)
        performance = run_performance_audit(fetch_result)
        schema = run_schema_audit(parse_result)
        geo = run_geo_audit(html, parse_result)

        # Calculate weighted composite health score
        # Technical (30%), Content (25%), Performance (20%), Schema (15%), GEO (10%)
        composite_score = round(
            (technical["score"] * 0.30) +
            (content["score"] * 0.25) +
            (performance["score"] * 0.20) +
            (schema["score"] * 0.15) +
            (geo["score"] * 0.10),
            1
        )

        overall_grade = (
            "A" if composite_score >= 90 else
            "B" if composite_score >= 80 else
            "C" if composite_score >= 70 else
            "D" if composite_score >= 50 else "F"
        )

        total_issues = (
            technical["issues_count"] +
            content["issues_count"] +
            performance["issues_count"] +
            schema["issues_count"] +
            geo["issues_count"]
        )

        return {
            "target_url": url,
            "final_url": fetch_result["final_url"],
            "composite_score": composite_score,
            "grade": overall_grade,
            "total_issues_count": total_issues,
            "audits": {
                "technical": technical,
                "content": content,
                "performance": performance,
                "schema": schema,
                "geo_ai_search": geo,
            },
            "meta_summary": {
                "title": parse_result["title"],
                "meta_description": parse_result["meta_description"],
                "word_count": parse_result["content_metrics"]["word_count"],
                "latency_ms": fetch_result["latency_ms"],
                "detected_schemas": schema["detected_types"],
            }
        }
