#!/usr/bin/env python3
"""Fail closed if public homepages advertise a stale product-family count."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOGUES = ("products-multilingual.json", "products-en.json", "products-hu.json", "products-de-at.json")
HOMEPAGES = {"index.html": "listed B2B raw materials",
             "hu.html": "katalogizált B2B alapanyag",
             "de-at.html": "katalogisierte B2B-Rohstoffe"}

def main() -> int:
    counts = {}
    for filename in CATALOGUES:
        data = json.loads((ROOT / filename).read_text(encoding="utf-8"))
        products = data if isinstance(data, list) else data["products"]
        counts[filename] = len(products)
    if len(set(counts.values())) != 1:
        print(f"FAIL: multilingual catalogue counts disagree: {counts}")
        return 1
    expected = next(iter(counts.values()))
    errors = []
    for filename, label in HOMEPAGES.items():
        html = (ROOT / filename).read_text(encoding="utf-8")
        pattern = (r'<span class="stat-number">(\d+)</span>\s*'
                   r'<span class="stat-label">' + re.escape(label) + r'</span>')
        values = re.findall(pattern, html)
        if values != [str(expected)]:
            errors.append(f"{filename}: expected one {expected} count for {label}; got {values}")
    localised_overview = {"index.html": f"The full {expected}-product portfolio",
                          "hu.html": f"A {expected} termékből álló teljes portfólió",
                          "de-at.html": f"Das vollständige Portfolio mit {expected} Produkten"}
    for filename, phrase in localised_overview.items():
        html = (ROOT / filename).read_text(encoding="utf-8")
        if phrase not in html:
            errors.append(f"{filename}: catalogue overview paragraph count does not match {expected}")
        if re.search(r'(?<![0-9])126(?![0-9])', html):
            errors.append(f"{filename}: a stale legacy product count remains")
    for filename in ("en-catalogue.html", "hu-termekkatalogus.html", "de-at-produktkatalog.html"):
        html = (ROOT / filename).read_text(encoding="utf-8")
        results = re.findall(r'<span id="resultCount">(\d+)</span>', html)
        if results != [str(expected)]:
            errors.append(f"{filename}: visible catalogue count mismatch: {results}; expected {expected}")
        narrative = re.sub(r'"position":126', '', html)
        if re.search(r'\b126\b', narrative):
            errors.append(f"{filename}: stale legacy family count remains outside item list position")
    de_html = (ROOT / "de-at.html").read_text(encoding="utf-8")
    if "prüfen wir Wir koordinieren" in de_html:
        errors.append("de-at.html: duplicated German buyer hero clause")
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print(f"PASS: catalogue count={expected} in JSON and EN/HU/DE-AT homepage statistics")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
