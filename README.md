# MZ SEO Agent — Autonomous Multi-Agent SEO Engine

> Built directly in `G:\mz`, inspired by the architectural principles of `claude-seo`.  
> Multi-platform compatibility with **Google Antigravity**, **Claude Code**, and standalone CLI.

---

## 🚀 Key Features

* **5-Pillar Comprehensive Audit:**
  1. **Technical SEO:** Status codes, HTTPS, canonical tags, title/meta description length, mobile viewport.
  2. **Content & E-E-A-T:** Heading structure (H1-H3), word count, thin content alerts, text-to-HTML ratio.
  3. **Performance & Speed:** TTFB latency, raw payload size, compression headers (gzip/brotli), redirect hops.
  4. **Structured Data & Schema:** JSON-LD detection, `@context` & `@type` verification, rich result readiness.
  5. **Generative Engine Optimization (GEO):** AI search visibility for ChatGPT, Perplexity, and Google AI Overviews.
* **Hardened Security:** Built-in SSRF protection blocking private networks (RFC 1918), loopback, link-local, and DNS-rebinding attacks.
* **Autonomous Agent Support:** Markdown-based agent definitions in `agents/` and skills in `skills/`.

---

## 💻 How to Run

### 1. Full SEO Audit:
```powershell
python G:\mz\cli.py audit "https://example.com"
```
Or simply:
```powershell
G:\mz\audit.bat "https://example.com"
```

### 2. Export JSON Report to File:
```powershell
python G:\mz\cli.py audit "https://example.com" --json --output "G:\mz\report.json"
```

### 3. Category-Specific Audits:
```powershell
python G:\mz\cli.py technical "https://example.com"
python G:\mz\cli.py content "https://example.com"
python G:\mz\cli.py performance "https://example.com"
python G:\mz\cli.py schema "https://example.com"
python G:\mz\cli.py geo "https://example.com"
```

---

## 📂 Architecture

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
  ├── audit.bat            # One-click audit runner
  ├── requirements.txt     # Dependencies
  └── pyproject.toml       # Package metadata
```
