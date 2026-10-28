#!/usr/bin/env python3
"""Command Line Interface for MZ SEO Agent."""

import argparse
import json
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from typing import Dict, Any
from core.orchestrator import Orchestrator
from core.fetcher import fetch_page, PageFetchError
from core.parser import parse_html
from tools.technical_audit import run_technical_audit
from tools.content_audit import run_content_audit
from tools.performance_audit import run_performance_audit
from tools.schema_audit import run_schema_audit
from tools.geo_audit import run_geo_audit


def print_banner():
    print("=" * 65)
    print("        [*] MZ SEO AGENT -- AUTONOMOUS AUDIT ENGINE")
    print("=" * 65)


def print_issues(issues):
    if not issues:
        print("  [OK] No issues detected in this category!")
        return

    for item in issues:
        severity = item["severity"]
        color = "\033[91m" if severity == "HIGH" else "\033[93m" if severity == "MEDIUM" else "\033[94m"
        reset = "\033[0m"
        print(f"  [{color}{severity}{reset}] {item['check']}: {item['message']}")


def handle_audit(url: str, as_json: bool, output_file: str = None):
    try:
        result = Orchestrator.audit_url(url)
    except PageFetchError as e:
        print(f"\n[ERROR] Failed to fetch target: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL] Audit execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    if as_json:
        payload = json.dumps(result, indent=2)
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(payload)
            print(f"Audit results written to {output_file}")
        else:
            print(payload)
        return

    print_banner()
    print(f"Target URL: {result['target_url']}")
    print(f"Final URL:  {result['final_url']}")
    print("-" * 65)
    print(f"[SCORE] COMPOSITE SEO HEALTH SCORE: {result['composite_score']}/100 (Grade: {result['grade']})")
    print(f"[ALERT] Total Identified Issues:     {result['total_issues_count']}")
    print("-" * 65)

    audits = result["audits"]

    # Technical
    t = audits["technical"]
    print(f"\n[1] TECHNICAL SEO AUDIT (Score: {t['score']}/100, Grade: {t['grade']})")
    print_issues(t["issues"])

    # Content
    c = audits["content"]
    print(f"\n[2] CONTENT & E-E-A-T AUDIT (Score: {c['score']}/100, Words: {c['word_count']})")
    print_issues(c["issues"])

    # Performance
    p = audits["performance"]
    print(f"\n[3] PERFORMANCE & SPEED (Score: {p['score']}/100, TTFB: {p['latency_ms']} ms, Size: {p['payload_kb']} KB)")
    print_issues(p["issues"])

    # Schema
    s = audits["schema"]
    print(f"\n[4] STRUCTURED DATA & SCHEMA (Score: {s['score']}/100, Types: {', '.join(s['detected_types']) if s['detected_types'] else 'None'})")
    print_issues(s["issues"])

    # GEO
    g = audits["geo_ai_search"]
    print(f"\n[5] AI SEARCH READINESS / GEO (Score: {g['score']}/100, Q-Headings: {g['question_headings_count']})")
    print_issues(g["issues"])

    print("\n" + "=" * 65)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"✓ Full report saved to: {output_file}\n")


def main():
    parser = argparse.ArgumentParser(description="MZ SEO Autonomous Agent CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available audit subcommands")

    # Audit subcommand
    audit_parser = subparsers.add_parser("audit", help="Run full multi-agent SEO audit")
    audit_parser.add_argument("url", help="Target URL to audit")
    audit_parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    audit_parser.add_argument("--output", "-o", help="Save JSON report to file")

    # Specific category commands
    for cat in ["technical", "content", "performance", "schema", "geo"]:
        cat_parser = subparsers.add_parser(cat, help=f"Run {cat} audit specifically")
        cat_parser.add_argument("url", help="Target URL to audit")
        cat_parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "audit":
        handle_audit(args.url, args.json, getattr(args, "output", None))
    else:
        # Run specific audit
        try:
            fetch_res = fetch_page(args.url)
            html = fetch_res["html"]
            parse_res = parse_html(html, base_url=fetch_res["final_url"])

            if args.command == "technical":
                res = run_technical_audit(fetch_res, parse_res)
            elif args.command == "content":
                res = run_content_audit(parse_res)
            elif args.command == "performance":
                res = run_performance_audit(fetch_res)
            elif args.command == "schema":
                res = run_schema_audit(parse_res)
            elif args.command == "geo":
                res = run_geo_audit(html, parse_res)

            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print_banner()
                print(f"Target: {args.url} | Category: {args.command.upper()}")
                print(f"Score: {res['score']}/100 (Grade: {res['grade']})")
                print("-" * 65)
                print_issues(res["issues"])
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
