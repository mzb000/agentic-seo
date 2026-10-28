"""DOM and SEO Meta Parser for MZ SEO Agent."""

import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import Dict, Any, List


def parse_html(html: str, base_url: str = "") -> Dict[str, Any]:
    """
    Parses HTML content to extract SEO elements, structured data, links, and content metrics.
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1. Title Tag
    title_tag = soup.find("title")
    title_text = title_tag.get_text().strip() if title_tag else ""

    # 2. Meta Tags
    meta_desc = ""
    meta_desc_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
    if meta_desc_tag and meta_desc_tag.get("content"):
        meta_desc = meta_desc_tag["content"].strip()

    meta_robots = ""
    meta_robots_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "robots"})
    if meta_robots_tag and meta_robots_tag.get("content"):
        meta_robots = meta_robots_tag["content"].strip().lower()

    viewport_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "viewport"})
    has_viewport = viewport_tag is not None

    # Canonical Link
    canonical_url = ""
    canonical_tag = soup.find("link", attrs={"rel": lambda x: x and "canonical" in [r.lower() for r in (x if isinstance(x, list) else [x])]})
    if canonical_tag and canonical_tag.get("href"):
        canonical_url = urljoin(base_url, canonical_tag["href"].strip())

    # 3. Heading Hierarchy
    headings: Dict[str, List[str]] = {
        "h1": [h.get_text().strip() for h in soup.find_all("h1")],
        "h2": [h.get_text().strip() for h in soup.find_all("h2")],
        "h3": [h.get_text().strip() for h in soup.find_all("h3")],
    }

    # 4. Links Extraction
    base_domain = urlparse(base_url).netloc.lower() if base_url else ""
    internal_links: List[str] = []
    external_links: List[str] = []
    nofollow_count = 0

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        full_url = urljoin(base_url, href)
        parsed_href = urlparse(full_url)
        rel = a_tag.get("rel", [])
        if isinstance(rel, str):
            rel = [rel]
        if any("nofollow" in r.lower() for r in rel):
            nofollow_count += 1

        if parsed_href.netloc.lower() == base_domain:
            internal_links.append(full_url)
        else:
            external_links.append(full_url)

    # 5. Images & Alt Attributes
    images = soup.find_all("img")
    images_count = len(images)
    missing_alt_count = 0
    for img in images:
        alt = img.get("alt")
        if alt is None or not alt.strip():
            missing_alt_count += 1

    # 6. JSON-LD Schemas
    json_ld_schemas: List[Dict[str, Any]] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw_text = script.string
        if raw_text:
            try:
                parsed_schema = json.loads(raw_text.strip())
                json_ld_schemas.append(parsed_schema)
            except Exception:
                json_ld_schemas.append({"error": "Invalid JSON-LD payload", "raw": raw_text[:200]})

    # 7. Text Metrics
    # Remove script, style, and noscript elements
    for element in soup(["script", "style", "noscript", "svg", "header", "footer", "nav"]):
        element.extract()
    body_text = soup.get_text(separator=" ", strip=True)
    words = body_text.split()
    word_count = len(words)
    text_length = len(body_text)
    html_length = len(html)
    text_ratio = round((text_length / html_length) * 100, 2) if html_length > 0 else 0

    return {
        "title": title_text,
        "title_length": len(title_text),
        "meta_description": meta_desc,
        "meta_description_length": len(meta_desc),
        "meta_robots": meta_robots,
        "has_viewport": has_viewport,
        "canonical_url": canonical_url,
        "headings": headings,
        "links": {
            "internal_count": len(internal_links),
            "external_count": len(external_links),
            "nofollow_count": nofollow_count,
            "internal_sample": internal_links[:10],
            "external_sample": external_links[:10],
        },
        "images": {
            "total_count": images_count,
            "missing_alt_count": missing_alt_count,
        },
        "schemas": json_ld_schemas,
        "content_metrics": {
            "word_count": word_count,
            "text_ratio_percent": text_ratio,
        },
    }
