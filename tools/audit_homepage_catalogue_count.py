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
