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
lastmods = {}
for entry in entries:
    loc = entry.findtext("s:loc", default="", namespaces=NS)
    locations.append(loc)
    lastmods[loc] = entry.findtext("s:lastmod", default="", namespaces=NS)
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
    lastmod = lastmods.get(loc, "")
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
    page_dates = set()
    for i, payload in enumerate(scripts):
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON-LD: {loc} block {i}: {exc}")
            continue

        def collect_page_dates(value):
            if isinstance(value, dict):
                types = value.get("@type") or []
                if isinstance(types, str):
                    types = [types]
                if set(types) & {"WebPage", "CollectionPage", "TechArticle"} and value.get("dateModified"):
                    page_dates.add(value["dateModified"])
                for child in value.values():
                    collect_page_dates(child)
            elif isinstance(value, list):
                for child in value:
                    collect_page_dates(child)

        collect_page_dates(data)
    if len(page_dates) != 1:
        errors.append(f"Expected one primary-page dateModified value: {loc}: {sorted(page_dates)}")
    elif lastmod != next(iter(page_dates)):
        errors.append(f"Sitemap lastmod/page dateModified mismatch: {loc}: {lastmod} != {next(iter(page_dates))}")
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

# v3 product intelligence + content-quality checks (all 378 language product pages)
product_pages = missing_faq = generic_hit = missing_checkpoints = missing_dual = 0
faq_schema_mismatch = 0
faq_blocks = []
checkpoint_blocks = []
families = set()
for path in sorted(ROOT.glob("*.html")):
    name = path.name
    if not (name.startswith(("en-", "hu-", "de-at-")) and name.endswith(("-industrial.html", "-food.html", "-feed.html", "-deicing.html"))):
        continue
    product_pages += 1
    families.add(re.sub(r"^(en|hu|de-at)-", "", name).removesuffix(".html"))
    text = path.read_text(encoding="utf-8")
    if 'class="product-faq"' not in text:
        missing_faq += 1
    if 'class="product-checkpoints"' not in text:
        missing_checkpoints += 1
    if 'class="product-dual-path"' not in text:
        missing_dual += 1
    if (
        "Is the CAS/EC identity enough to place an order?" in text
        or "Elég a CAS/EK azonosító" in text
        or "Reicht die CAS-/EG-Identität" in text
    ):
        generic_hit += 1
    faq_html = re.search(r'<section class="product-faq"[\s\S]*?</section>', text)
    cp_html = re.search(r'<section class="product-checkpoints"[\s\S]*?</section>', text)
    if faq_html:
        faq_blocks.append(faq_html.group(0))
        visible_q = re.findall(r"<summary>(.*?)</summary>", faq_html.group(0))
        schema_q = []
        for payload in re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S):
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                continue

            def walk(o, acc):
                if isinstance(o, dict):
                    if o.get("@type") == "FAQPage":
                        for q in o.get("mainEntity") or []:
                            if isinstance(q, dict) and q.get("name"):
                                acc.append(q["name"])
                    for v in o.values():
                        walk(v, acc)
                elif isinstance(o, list):
                    for i in o:
                        walk(i, acc)
                return acc

            schema_q.extend(walk(data, []))
        if visible_q and schema_q and visible_q != schema_q:
            faq_schema_mismatch += 1
            if faq_schema_mismatch <= 5:
                errors.append(f"FAQ schema/visible mismatch: {name}")
    if cp_html:
        checkpoint_blocks.append(cp_html.group(0))
    # Reject false Product/Offer commercial claims
    if re.search(r'"@type"\s*:\s*"Offer"', text) or re.search(r'"@type"\s*:\s*"AggregateRating"', text):
        errors.append(f"Forbidden commercial schema on product page: {name}")

if product_pages != 378:
    errors.append(f"Expected 378 product language pages, found {product_pages}")
if len(families) != 126:
    errors.append(f"Expected 126 product families, found {len(families)}")
if missing_faq:
    errors.append(f"Missing product-faq section on {missing_faq} pages")
if missing_checkpoints:
    errors.append(f"Missing product-checkpoints section on {missing_checkpoints} pages")
if missing_dual:
    errors.append(f"Missing product-dual-path section on {missing_dual} pages")
if generic_hit:
    errors.append(f"Generic FAQ boilerplate still present on {generic_hit} pages")
identical_faq = len(faq_blocks) - len(set(faq_blocks))
if identical_faq:
    errors.append(f"Identical FAQ blocks found across {identical_faq} page comparisons")
# Soft uniqueness: EN first FAQ question should not all be identical
en_first = []
for path in sorted(ROOT.glob("en-*-*.html")):
    if not path.name.endswith(("-industrial.html", "-food.html", "-feed.html", "-deicing.html")):
        continue
    m = re.search(r'<section class="product-faq"[\s\S]*?<summary>(.*?)</summary>', path.read_text(encoding="utf-8"))
    if m:
        en_first.append(m.group(1))
unique_ratio = (len(set(en_first)) / len(en_first)) if en_first else 0
if unique_ratio < 0.7:
    errors.append(f"EN first-FAQ uniqueness too low: {unique_ratio:.2%} ({len(set(en_first))}/{len(en_first)})")

# Entity registry sameAs policy sanity
entity_path = ROOT / "entity-registry.json"
if entity_path.is_file():
    entities = json.loads(entity_path.read_text(encoding="utf-8")).get("entities") or []
    if len(entities) < 120:
        warnings.append(f"entity-registry has only {len(entities)} entities")
    for ent in entities:
        pid = ent.get("id") or ""
        if ent.get("sameAs_status") == "verified" and re.search(r"(oldat|regeneralt|vizmentes|solution|mixture)", pid):
            errors.append(f"Unsafe verified sameAs for form-ambiguous product: {pid}")

print(
    "Product intelligence: "
    f"pages={product_pages} families={len(families)} "
    f"missing_faq={missing_faq} missing_checkpoints={missing_checkpoints} missing_dual={missing_dual} "
    f"generic_faq={generic_hit} faq_schema_mismatch={faq_schema_mismatch} "
    f"identical_faq_blocks={identical_faq} en_first_faq_unique={len(set(en_first))}/{len(en_first)}"
)

print(f"Audited {len(locations)} sitemap URLs; errors={len(errors)} warnings={len(warnings)}")
for issue in errors[:100]:
    print("ERROR:", issue)
for issue in warnings[:30]:
    print("WARN:", issue)
if len(errors) > 100:
    print(f"... {len(errors)-100} more errors")
sys.exit(1 if errors else 0)
