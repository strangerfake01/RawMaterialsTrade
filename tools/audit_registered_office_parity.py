#!/usr/bin/env python3
"""Fail closed on a wrong registered-office vs operational-site label.

The company details agree with the existing legal notice and privacy pages.
This audit prevents three-language visible-homepage/JSON-LD drift; it does not
substitute for an official live company-registry extract or legal sign-off.
"""
from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTERED = "Törökszentmiklós"
OPERATIONAL = "Ócsa"
PAGES = {
    "index.html": ("Registered office", "Operational & ISO-certified site"),
    "hu.html": ("Székhely", "Telephely és ISO-tanúsított helyszín"),
    "de-at.html": ("Firmensitz", "Betriebsstätte und ISO-9001-zertifizierter Standort"),
}
ORG_ID = "https://www.rawmaterialstrade.com/#org"
errors: list[str] = []

for name, (registered_label, operational_label) in PAGES.items():
    html = (ROOT / name).read_text(encoding="utf-8")
    card = re.search(r'<div[^>]*class="company-identity-card"[^>]*>.*?</dl>', html, re.S)
    if not card:
        errors.append(f"{name}: missing company identity card")
    else:
        excerpt = unescape(card.group(0))
        if not re.search(r'<dt>' + re.escape(registered_label) +
                         r'</dt><dd>[^<]*' + REGISTERED, excerpt):
            errors.append(f"{name}: wrong or missing visible registered office")
        if not re.search(r'<dt>' + re.escape(operational_label) +
                         r'</dt><dd>[^<]*' + OPERATIONAL, excerpt):
            errors.append(f"{name}: wrong or missing visible operational site")
        if re.search(r'<dt>' + re.escape(registered_label) +
                     r'</dt><dd>[^<]*' + OPERATIONAL, excerpt):
            errors.append(f"{name}: operational site mislabeled as registered office")
    # All languages must expose the official office via the customer contact area.
    if name == "hu.html":
        if '<strong>Bejegyzett székhely</strong><br/>5200 Törökszentmiklós' not in html:
            errors.append("HU contact details do not identify the registered office")
    elif name == "de-at.html":
        if '<strong>Firmensitz</strong><br/>5200 Törökszentmiklós' not in html:
            errors.append("DE contact details do not identify the registered office")
    else:
        if '<strong>Registered office</strong><br/>5200 Törökszentmiklós' not in html:
            errors.append("EN contact details do not identify the registered office")

    entities = []
    for raw in re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        try:
            schema = json.loads(raw)
        except ValueError:
            errors.append(f"{name}: invalid JSON-LD")
            continue
        entities += (schema.get("@graph", [schema]) if isinstance(schema, dict) else schema)
    orgs = [e for e in entities if isinstance(e, dict) and
            e.get("@id") == ORG_ID and e.get("@type") == "Organization"]
    if len(orgs) != 1:
        errors.append(f"{name}: expected one Organization entity, got {len(orgs)}")
    elif orgs[0].get("address", {}).get("addressLocality") != REGISTERED:
        errors.append(f"{name}: Organization addressLocality is not registered office")

impressum = (ROOT / "impressum.html").read_text(encoding="utf-8")
if not all(x in impressum for x in ("Sitz / Registered address:", REGISTERED, OPERATIONAL)):
    errors.append("Impressum company address baseline differs")
for lang in ("en", "hu", "de-at"):
    legal = (ROOT / f"privacy-{lang}.html").read_text(encoding="utf-8")
    if REGISTERED not in legal or OPERATIONAL not in legal:
        errors.append(f"privacy-{lang}: missing registered and operational addresses")

print(f"Legal identity parity: 3 homepages and 4 legal notices, errors={len(errors)}")
for error in errors:
    print("ERROR:", error)
raise SystemExit(bool(errors))
