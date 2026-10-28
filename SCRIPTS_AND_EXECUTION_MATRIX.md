# Execution Tier: 60 Python Scripts Matrix

All automation scripts reside in `scripts/` and run under `runtime.py`.

## 1. Scraping & Rendering Engine
* **`fetch_page.py`:** Fast HTTP/HTTPS fetcher equipped with SSRF defenses and DNS rebinding protections.
* **`render_page.py`:** Headless Chromium renderer for JavaScript-heavy Single Page Applications (SPAs).
* **`parse_html.py`:** Extracts DOM metadata, headings (H1-H6), canonicals, meta robots, open graph tags.
* **`capture_screenshot.py`:** Takes full-page and viewport screenshots for visual audit.

## 2. Google Search & Performance APIs
* **`google_report.py`:** Comprehensive wrapper for Google Search Console & GA4.
* **`gsc_inspect.py` / `gsc_query.py`:** Inspects specific URL indexing status and queries search impressions/clicks.
* **`pagespeed_check.py`:** Evaluates mobile & desktop performance via Google PageSpeed API.
* **`crux_history.py`:** Queries historical real-user experience metrics (CrUX).
* **`indexing_notify.py` / `indexnow_submit.py`:** Submits URLs to Google Indexing API and Bing IndexNow protocol.

## 3. SEO Quality, Content & Drift
* **`content_quality.py` / `nlp_analyze.py`:** Evaluates E-E-A-T score, lexical richness, readability grade.
* **`content_humanize.py`:** Flags repetitive AI sentence structures and suggests human tone adaptations.
* **`drift_baseline.py` / `drift_compare.py` / `drift_report.py`:** Snapshot comparison engine tracking changes in title, headers, canonicals, and speed metrics.

## 4. Backlinks & External Intelligence
* **`verify_backlinks.py`:** Validates if historical backlink URLs are still live and have not added `nofollow`/`noindex`.
* **`commoncrawl_graph.py`:** Queries petabyte-scale web graphs from Common Crawl index.
* **`dataforseo_merchant.py` / `dataforseo_costs.py`:** Manages live keyword volumes and SERP cost calculations.
* **`schema_generate.py` / `schema_ecommerce_validate.py`:** Validates product, breadcrumb, and organization schemas against Google guidelines.
