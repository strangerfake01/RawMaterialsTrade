#!/usr/bin/env python3
"""Ensure every localized product connects buyer and supplier to actionable paths."""
from pathlib import Path
import json
import re
import sys

root = Path(__file__).resolve().parents[1]
products = json.loads((root / "products-multilingual.json").read_text(encoding="utf-8"))
prefixes = {"en": "en-", "hu": "hu-", "de": "de-at-"}
expected_partnership = {
    "en": "sales-representation-distribution-partner-central-europe.html",
    "hu": "hu-ertekesitesi-kepviselet-disztribucios-partner.html",
    "de": "de-at-vertriebspartner-distribution-chemierohstoffe.html",
}
expected_home = {"en": "/#contact", "hu": "hu.html#contact", "de": "de-at.html#contact"}
errors = []
for product in products:
    slug = product["id"]
    for lang, prefix in prefixes.items():
        path = root / (prefix + slug + ".html")
        if not path.is_file():
            errors.append(f"{path.name}: missing")
            continue
        html = path.read_text(encoding="utf-8")
        match = re.search(r'<section class="product-dual-path"[^>]*>(.*?)</section>', html, re.S)
        if not match:
            errors.append(f"{path.name}: missing buyer/supplier section")
            continue
        section = match.group(1)
        cards = re.findall(r'<div class="dual-path-card">', section)
        if len(cards) != 2:
            errors.append(f"{path.name}: expected buyer and supplier cards, got {len(cards)}")
        if expected_home[lang] not in section:
            errors.append(f"{path.name}: missing buyer contact path")
        if expected_partnership[lang] not in section:
            errors.append(f"{path.name}: missing manufacturer partnership path")
        if not re.search(r'<details class="sub-accordion rich-accordion b2b-summary">', html):
            errors.append(f"{path.name}: missing material enquiry guidance")
        if not re.search(r'\b(?:SDS|TDS|CoA)\b', section):
            errors.append(f"{path.name}: missing document requirements")
print(f"Procurement pathways checked: {len(products)} families x {len(prefixes)} languages = {len(products)*len(prefixes)} pages")
for err in errors[:80]:
    print("ERROR:", err)
if len(errors) > 80:
    print(f"... plus {len(errors)-80} additional errors")
sys.exit(bool(errors))
