#!/usr/bin/env python3
"""Inventory unverified commercial assertions on public product pages.

Read-only. This report does not infer supplier availability or chemical validity.
No private correspondence is read or used.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
LANGS = {"en": "en-", "hu": "hu-", "de": "de-at-"}
CHECKS = {
    "blanket_sds": re.compile(r"(?i)(?:SDS always|SDS stets|mindig SDS|stets SDS|immer SDS)"),
    "fixed_packaging_orientation": re.compile(r"(?i)(?:preferred packaging currently listed|orientierende verpackung laut katalog|orientációs kiszerelés a katalógusban|packaging preference [(]catalogue orientation:)"),
    "grade_as_concentration": re.compile(r"(?i)(?:target concentration or purity where relevant: currently listed orientation|célkoncentráció vagy tisztaság, ha releváns: katalógus-orientáció|zielkonzentration oder reinheit, falls relevant: katalogorientierung)"),
    "unqualified_document_promise": re.compile(r"(?i)(?:SDS, TDS, certificates of analysis and compliance documents available on request|SDS, TDS, analízis-tanúsítványok és megfelelőségi dokumentumok kérésre rendelkezésre állnak)"),
    "supplier_documents_assumed": re.compile(r"(?i)(?:supplier (?:SDS|TDS|CoA) (?:is|are) (?:available|verified)|beszállítói (?:SDS|TDS|CoA) (?:rendelkezésre áll|igazolt)|Lieferanten-(?:SDS|TDS|CoA) (?:ist|sind) (?:verfügbar|bestätigt))"),
}
counts = {k: 0 for k in CHECKS}
examples = {k: [] for k in CHECKS}
missing = []
for product in products:
    for lang, prefix in LANGS.items():
        page = ROOT / (prefix + product["id"] + ".html")
        if not page.exists():
            missing.append(page.name)
            continue
        html = page.read_text(encoding="utf-8")
        for label, pattern in CHECKS.items():
            if pattern.search(html):
                counts[label] += 1
                if len(examples[label]) < 6:
                    examples[label].append(page.name)
print("Public product claim inventory:", len(products), "families;", sum(1 for p in products for lang in LANGS if (ROOT / (LANGS[lang] + p["id"] + ".html")).exists()), "language pages")
for label, count in counts.items():
    print("REVIEW", label, count, "pages; examples:", ", ".join(examples[label]))
if missing:
    print("ERROR missing product pages:", ", ".join(missing[:10]))
    sys.exit(1)
print("NOTE: claim matches are review candidates, not independent evidence of falsehood or compliance.")
# Report-only until each product's provenance is established; do not silently invent replacement values.
