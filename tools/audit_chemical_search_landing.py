#!/usr/bin/env python3
"""Check standalone multilingual chemical search landing-page contracts.

This is a static audit, not evidence of Google indexing or chemical verification.
"""
import json
import re
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
LANGS = {"en": ("en-", "name_en"), "hu": ("hu-", "name_hu"), "de": ("de-at-", "name_de")}
SCHEMA = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.I | re.S)
issues = []
blocking = []
stats = {"pages": 0, "cas_visible": 0, "ec_visible": 0, "formula_visible": 0, "cas_schema": 0, "ec_schema": 0, "formula_schema": 0}

def nodes(value):
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from nodes(v)
    elif isinstance(value, list):
        for v in value:
            yield from nodes(v)

def norm(value):
    return re.sub(r"\s+", "", unescape(str(value))).casefold()

for product in PRODUCTS:
    ident = product.get("technical_identity") or {}
    for lang, (prefix, name_field) in LANGS.items():
        filename = prefix + product["id"] + ".html"
        path = ROOT / filename
        if not path.exists():
            blocking.append((filename, "missing_page"))
            continue
        stats["pages"] += 1
        html = path.read_text(encoding="utf-8")
        plain = unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script\b.*?</script>|<style\b.*?</style>", "", html, flags=re.S | re.I)))
        title = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, re.S | re.I)
        expected_name = product.get(name_field, "")
        if not title or not expected_name or norm(expected_name) not in norm(title.group(1)):
            blocking.append((filename, "title_name"))
        if not h1 or norm(expected_name) not in norm(re.sub(r"<[^>]+>", "", h1.group(1))):
            blocking.append((filename, "h1_name"))
        for key in ("cas", "ec", "formula"):
            value = str(ident.get(key) or "").strip()
            if not value or value.lower() in {"unknown", "n/a", "-", "—", "not available"}:
                issues.append((filename, key + "_source_unverified_or_empty"))
                continue
            if norm(value) in norm(plain):
                stats[key + "_visible"] += 1
            else:
                issues.append((filename, key + "_not_visible"))
        graphs = []
        for match in SCHEMA.finditer(html):
            try:
                graphs.extend(nodes(json.loads(match.group(1))))
            except (ValueError, TypeError):
                blocking.append((filename, "invalid_jsonld"))
        chemicals = [n for n in graphs if isinstance(n, dict) and "ChemicalSubstance" in (n.get("@type") if isinstance(n.get("@type"), list) else [n.get("@type")])]
        if len(chemicals) != 1:
            blocking.append((filename, "chemical_schema_count"))
            continue
        chemical = chemicals[0]
        identifiers = chemical.get("identifier") or []
        if isinstance(identifiers, dict):
            identifiers = [identifiers]
        for key, prop in (("cas", "CAS"), ("ec", "EC")):
            value = str(ident.get(key) or "").strip()
            if value and any(isinstance(i, dict) and i.get("propertyID") == prop and str(i.get("value", "")).strip() == value for i in identifiers):
                stats[key + "_schema"] += 1
            elif value:
                issues.append((filename, key + "_schema_missing_or_mismatch"))
        formula = str(ident.get("formula") or "").strip()
        if formula and norm(formula) in norm(json.dumps(chemical, ensure_ascii=False)):
            stats["formula_schema"] += 1
        elif formula:
            issues.append((filename, "formula_schema_missing"))

print(json.dumps({"stats": stats, "identity_gaps": len(issues), "blocking_errors": len(blocking), "first_gaps": issues[:100], "blocking": blocking[:100]}, ensure_ascii=False, indent=2))
# Do not publish ambiguous identity values solely to satisfy a search audit.
# Keep identity coverage as an explicit remediation backlog; fail on structural errors.
raise SystemExit(bool(blocking))
