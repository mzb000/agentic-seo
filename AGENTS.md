# MZ SEO Agent Platform

> Autonomous Multi-Agent SEO Engine inspired by Claude SEO.
> Built for Google Antigravity, Claude Code, Cursor, and Gemini CLI.

## Quick CLI Reference

From `G:\mz` root:

| Command | Action |
|---|---|
| `python cli.py audit <url>` | Full 5-pillar SEO audit with score and grades |
| `python cli.py audit <url> --json` | Machine-readable JSON output |
| `python cli.py technical <url>` | Check crawlability, canonicals, status, mobile readiness |
| `python cli.py content <url>` | Evaluate E-E-A-T, word count, heading hierarchy |
| `python cli.py performance <url>` | Measure TTFB, payload size, compression headers |
| `python cli.py schema <url>` | Validate JSON-LD structured data |
| `python cli.py geo <url>` | Generative Engine Optimization (AI Overviews, Perplexity) |

## System Layout

```
G:\mz\
  ├── core/                # Core engine modules
  │     ├── security.py    # SSRF & IP blocklists
  │     ├── fetcher.py     # Safe HTTP client
  │     ├── parser.py      # DOM, metadata & schema parser
  │     └── orchestrator.py# Master coordinator
  ├── tools/               # 5 specialized audit tools
  │     ├── technical_audit.py
  │     ├── content_audit.py
  │     ├── performance_audit.py
  │     ├── schema_audit.py
  │     └── geo_audit.py
  ├── agents/              # Markdown agent definitions
  ├── skills/              # Antigravity/Claude skills
  ├── cli.py               # Main CLI runner
  ├── requirements.txt     # Dependencies
  └── pyproject.toml       # Package metadata
```
