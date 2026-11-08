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
    for lang, href in alts.items():
        if href in alternates and alternates[href] != alts:
            errors.append(f"Non-reciprocal hreflang cluster: {loc} -> {href}")
    relative = unquote(urlparse(loc).path).lstrip("/")
    candidate = ROOT / (relative or "index.html")
    if relative.endswith("/"):
        candidate = ROOT / relative / "index.html"
    if not candidate.is_file():
        errors.append(f"Missing local page: {loc} => {candidate.relative_to(ROOT)}")
        continue
    source = candidate.read_text(encoding="utf-8")
    canonical_tags = re.findall(r'<link\b[^>]*>', source, re.I)
    canonicals = []
    for tag in canonical_tags:
        rel = re.search(r'\brel=["\x27]([^"\x27]+)', tag, re.I)
        href = re.search(r'\bhref=["\x27]([^"\x27]+)', tag, re.I)
        if rel and "canonical" in rel.group(1).lower().split():
            canonicals.append(href.group(1) if href else "")
    if len(canonicals) != 1 or canonicals[0] != loc:
        errors.append(f"Canonical mismatch: {loc}: {canonicals}")
    if len(re.findall(r'<h1[ >]', source, re.I)) != 1:
        errors.append(f"H1 count mismatch: {loc}")
    scripts = re.findall(r'<script\b[^>]*type=["\x27]application/ld\+json["\x27][^>]*>(.*?)</script>', source, re.I | re.S)
    for i, payload in enumerate(scripts):
        try:
            json.loads(payload)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON-LD: {loc} block {i}: {exc}")
    if not scripts:
        warnings.append(f"No JSON-LD: {loc}")
# Static inquiry-form contract: no external requests or test submissions.
expected_endpoint = "https://muddy-voice-db90.6ymnrwgnv9.workers.dev/api/contact"
for homepage in ("index.html", "hu.html", "de-at.html"):
    page = (ROOT / homepage).read_text(encoding="utf-8")
    forms = re.findall(r'<form\b[^>]*class="[^"]*inquiry-form[^"]*"[^>]*>', page, re.I)
    if len(forms) != 1 or f'action="{expected_endpoint}"' not in forms[0]:
        errors.append(f"Inquiry form endpoint mismatch: {homepage}")
    if 'id="turnstileContainer"' not in page:
        errors.append(f"Missing Turnstile container: {homepage}")
    if '/assets/js/site.v20261108.js' not in page:
        errors.append(f"Missing shared inquiry script: {homepage}")
script = (ROOT / "assets/js/site.v20261108.js").read_text(encoding="utf-8")
for required_fragment in (expected_endpoint, "/config", "turnstile.render", "turnstileReady"):
    if required_fragment not in script:
        errors.append(f"Inquiry script contract missing: {required_fragment}")
if "footerVisible" in script:
    errors.append("Contact FAB still contains footerVisible hide logic")

# v2 product intelligence checks
reserved = {
    "en-bentonit-industrial.html", "hu-bentonit-industrial.html", "de-at-bentonit-industrial.html",
    "en-borkosav-l-food.html", "hu-borkosav-l-food.html", "de-at-borkosav-l-food.html",
    "en-butil-glikol-industrial.html", "hu-butil-glikol-industrial.html", "de-at-butil-glikol-industrial.html",
}
product_pages = missing_faq = generic_hit = missing_checkpoints = 0
for path in sorted(ROOT.glob("*.html")):
    name = path.name
    if name in reserved:
        continue
    if not (name.startswith(("en-", "hu-", "de-at-")) and name.endswith(("-industrial.html", "-food.html", "-feed.html", "-deicing.html"))):
        continue
    product_pages += 1
    text = path.read_text(encoding="utf-8")
    if 'class="product-faq"' not in text:
        missing_faq += 1
    if 'class="product-checkpoints"' not in text:
        missing_checkpoints += 1
    if (
        "Is the CAS/EC identity enough to place an order?" in text
        or "Elég a CAS/EK azonosító" in text
        or "Reicht die CAS-/EG-Identität" in text
    ):
        generic_hit += 1
if product_pages < 360:
    errors.append(f"Unexpected enriched product page count: {product_pages}")
if missing_faq:
    errors.append(f"Missing product-faq section on {missing_faq} pages")
if missing_checkpoints:
    errors.append(f"Missing product-checkpoints section on {missing_checkpoints} pages")
if generic_hit:
    errors.append(f"Generic FAQ boilerplate still present on {generic_hit} pages")
print(f"Product intelligence: pages={product_pages} missing_faq={missing_faq} missing_checkpoints={missing_checkpoints} generic_faq={generic_hit}")

print(f"Audited {len(locations)} sitemap URLs; errors={len(errors)} warnings={len(warnings)}")
for issue in errors[:100]:
    print("ERROR:", issue)
for issue in warnings[:30]:
    print("WARN:", issue)
if len(errors) > 100:
    print(f"... {len(errors)-100} more errors")
sys.exit(1 if errors else 0)
