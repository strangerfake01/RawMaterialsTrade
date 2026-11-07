#!/usr/bin/env python3
"""Read-only release audit for Raw Materials Trade static pages.

Run from repository root: python3 tools/audit_release_contract.py
No network access, no file mutations, no Cloudflare changes.
"""
from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.rawmaterialstrade.com"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "x": "http://www.w3.org/1999/xhtml"}
errors = []
warnings = []
sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
entries = sitemap.findall("s:url", NS)
locations = []
alternates = {}
for entry in entries:
    loc = entry.findtext("s:loc", default="", namespaces=NS)
    locations.append(loc)
    alts = {}
    for link in entry.findall("x:link", NS):
        lang = link.attrib.get("hreflang", "")
        href = link.attrib.get("href", "")
        if lang in alts:
            errors.append(f"Duplicate hreflang {lang}: {loc}")
        alts[lang] = href
    alternates[loc] = alts
if len(locations) != len(set(locations)):
    errors.append("Duplicate sitemap loc")
known = set(locations)
required = {"en", "hu-HU", "de-AT", "x-default"}
for loc in locations:
    if not loc.startswith(BASE + "/"):
        errors.append(f"Unexpected sitemap host: {loc}")
        continue
    alts = alternates[loc]
    if set(alts) != required:
        errors.append(f"Missing or unexpected hreflang: {loc}: {sorted(alts)}")
    for lang, href in alts.items():
        if href not in known:
            errors.append(f"Alternate not in sitemap: {loc} [{lang}] {href}")
    relative = unquote(urlparse(loc).path).lstrip("/")
    candidate = ROOT / (relative or "index.html")
    if relative.endswith("/"):
        candidate = ROOT / relative / "index.html"
    if not candidate.is_file():
        errors.append(f"Missing local page: {loc} => {candidate.relative_to(ROOT)}")
        continue
    source = candidate.read_text(encoding="utf-8")
    canonicals = re.findall(r'<link\\b(?=[^>]*rel=["\\\']canonical["\\\'])[^>]*href=["\\\']([^"\\\']+)', source, re.I)
    if len(canonicals) != 1 or canonicals[0] != loc:
        errors.append(f"Canonical mismatch: {loc}: {canonicals}")
    if len(re.findall(r'<h1\\b', source, re.I)) != 1:
        errors.append(f"H1 count mismatch: {loc}")
    scripts = re.findall(r'<script\\b[^>]*type=["\\\']application/ld\\+json["\\\'][^>]*>(.*?)</script>', source, re.I | re.S)
    for i, payload in enumerate(scripts):
        try:
            json.loads(payload)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON-LD: {loc} block {i}: {exc}")
    if not scripts:
        warnings.append(f"No JSON-LD: {loc}")
print(f"Audited {len(locations)} sitemap URLs; errors={len(errors)} warnings={len(warnings)}")
for issue in errors[:100]:
    print("ERROR:", issue)
for issue in warnings[:30]:
    print("WARN:", issue)
if len(errors) > 100:
    print(f"... {len(errors)-100} more errors")
sys.exit(1 if errors else 0)
