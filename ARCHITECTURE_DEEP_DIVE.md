# Architecture Deep Dive: Claude SEO

## 1. System Overview

**Claude SEO** uses a decoupled, agentic architecture built on four primary layers:

```mermaid
graph TD
    User([User Invocations]) --> Orchestrator[Routing Tier: skills/seo/SKILL.md]
    
    subgraph Autonomous_Agents[Tier 2: 19 Specialist Sub-Agents]
        Orchestrator --> TechAgent[seo-technical.md]
        Orchestrator --> ContentAgent[seo-content.md]
        Orchestrator --> GEOAgent[seo-geo.md]
        Orchestrator --> PerfAgent[seo-performance.md]
        Orchestrator --> SchemaAgent[seo-schema.md]
        Orchestrator --> DriftAgent[seo-drift.md]
        Orchestrator --> ClusterAgent[seo-cluster.md]
    end

    subgraph Execution_Engine[Tier 3: Python Runtime & 60 Scripts]
        TechAgent --> Runtime[scripts/runtime.py]
        ContentAgent --> Runtime
        GEOAgent --> Runtime
        PerfAgent --> Runtime
        SchemaAgent --> Runtime
        DriftAgent --> Runtime
        ClusterAgent --> Runtime
        
        Runtime --> SafeFetch[fetch_page.py with SSRF Guard]
        Runtime --> Parser[parse_html.py & render_page.py]
        Runtime --> GoogleSuite[google_report.py & pagespeed_check.py]
        Runtime --> BacklinksEngine[verify_backlinks.py & commoncrawl.py]
    end

    subgraph Integration_Layer[Tier 4: MCP & APIs]
        GoogleSuite --> GSC[Google Search Console & GA4]
        Runtime --> ExtAPIs[DataForSEO, Ahrefs, Moz, Bing, Firecrawl]
    end
```

---

## 2. Orchestration & Delegation Protocol

1. **Progressive Disclosure:** Instead of feeding all skills into the model context at once, the system routes requests via `skills/seo/SKILL.md`.
2. **Deterministic Outputs:** Agents do not guess; each sub-agent delegates execution to Python scripts in `scripts/`, receives JSON output, and formats it into actionable audit tables.
3. **Concurrency:** When running `/seo audit <url>`, the orchestrator initiates up to 17 parallel sub-agent tasks covering performance, technical SEO, mobile friendliness, content E-E-A-T, and structured schema.
