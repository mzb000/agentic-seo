---
name: mz-seo-audit
description: Full-spectrum autonomous SEO audit skill evaluating technical, content, performance, schema, and AI/GEO readiness.
---

# MZ SEO Audit Skill

Use this skill when the user asks for a website SEO audit, health score, or optimization plan.

## Execution Procedure

Run the CLI tool from `G:\mz`:

```bash
python G:\mz\cli.py audit <url>
```

Or get programmatic JSON output:

```bash
python G:\mz\cli.py audit <url> --json
```

## Review Checklist
1. Review overall composite health score.
2. Address all `HIGH` severity issues first (non-200 status, noindex, missing title, missing viewport).
3. Evaluate AI / GEO score for citation eligibility in Perplexity, Google AI Overviews, and ChatGPT.
