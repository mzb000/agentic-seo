# Security & External API Integration Protocols

## 1. Network & SSRF Defenses (`url_safety.py`)

To prevent agents from exploiting external crawl tools to attack internal networks or local host services, `claude-seo` enforces strict pre-flight checks:

* **Private IP Blocking:** Rejects IP ranges under RFC 1918 (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), `127.0.0.0/8` (Loopback), and link-local addresses (`169.254.0.0/16`).
* **DNS Rebinding Protection:** Resolves hostnames before request dispatch and validates resolved IPs against blocklists prior to connection establishment.
* **Protocol Whitelisting:** Enforces `http://` and `https://` only; rejects `file://`, `gopher://`, `ftp://`.

---

## 2. Token & Secret Redaction (`runtime.py`)

Before stdout/stderr streams are handed back to the AI model context, `runtime.py` applies redaction filters:
* Regex scrubbing of API keys, Bearer tokens, and basic auth credentials (`http://user:pass@...` becomes `http://<redacted>@...`).

---

## 3. Post-Tool Validation Hooks (`hooks/hooks.json`)

When an agent modifies files (e.g., generating JSON-LD schemas), a `PostToolUse` lifecycle hook runs:
```json
{
  "command": "node",
  "args": ["hooks/run-python-hook.js", "hooks/validate-schema.py", "${tool_input.file_path}"]
}
```
This guarantees that invalid schema markup cannot be committed without immediate automated feedback.
