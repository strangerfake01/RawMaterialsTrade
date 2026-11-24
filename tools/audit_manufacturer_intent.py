#!/usr/bin/env python3
"""Verify the three supplier-partnership pages have distinct and truthful manufacturer intent."""
from pathlib import Path
from html.parser import HTMLParser
import re

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    "sales-representation-distribution-partner-central-europe.html": ("Process", "For manufacturers and qualified distributors", "Industrial buyers contact us", "does not promise orders"),
    "hu-ertekesitesi-kepviselet-disztribucios-partner.html": ("Folyamat", "Gyártók és minősített nagykereskedők", "Az ipari vevők jellemzően", "nem jelent megrendelési"),
    "de-at-vertriebspartner-distribution-chemierohstoffe.html": ("Ablauf", "Bei Herstellern und qualifizierten Großhändlern", "Industrielle Einkäufer nennen", "keine Zusage für Aufträge"),
}
issues = []
for file, (section_label, intro1, intro2, caveat) in PAGES.items():
    html = (ROOT / file).read_text(encoding="utf-8")
    sections = {}
    for marker in ("strategic-section", "dach-section"):
        match = re.search(r'<section class="' + marker + r'"[^>]*>(.*?)</section>', html, re.S)
        sections[marker] = match.group(1) if match else ""
        if not match:
            issues.append(f"{file}: missing {marker}")
    if f'<span class="section-label">{section_label}</span>' not in sections["strategic-section"]:
        issues.append(f"{file}: locale-specific process label missing")
    for marker, phrase in (("strategic-section", intro1), ("dach-section", intro2)):
        if phrase not in sections[marker]:
            issues.append(f"{file}: {marker} lacks manufacturer-specific decision guidance")
    if caveat not in sections["strategic-section"]:
        issues.append(f"{file}: missing no-guarantee qualification")
    p1 = re.search(r'<p class="lead">(.*?)</p>', sections["strategic-section"], re.S)
    p2 = re.search(r'<p class="lead">(.*?)</p>', sections["dach-section"], re.S)
    if not p1 or not p2 or p1.group(1) == p2.group(1):
        issues.append(f"{file}: duplicated or missing lead paragraphs")
    if html.count("dateModified") < 1:
        issues.append(f"{file}: dateModified missing")
    for marker in ('id="mfrIntakeHeading"', 'id="supplier-contact"', 'hreflang="x-default"'):
        if marker not in html:
            issues.append(f"{file}: missing {marker}")
for issue in issues:
    print("ERROR:", issue)
print(f"Manufacturer partnership intent: {len(PAGES)} localized pages; errors={len(issues)}")
raise SystemExit(bool(issues))
