#!/usr/bin/env python3
"""Identify same-CAS catalogue records for manual grade review.

Same CAS does not prove substitutability. This report never approves substitutes.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    by_cas = defaultdict(list)
    for product in products:
        identity = product.get("technical_identity") or {}
        cas = str(identity.get("cas") or "").strip()
        if cas and "/" not in cas and "confirm" not in cas.lower():
            by_cas[cas].append(product)
    groups = 0
    for cas, items in sorted(by_cas.items()):
        if len(items) < 2:
            continue
        groups += 1
        print(f"CAS {cas}: {len(items)} catalogue entries; REVIEW ONLY, not approved substitutes")
        for item in items:
            identity = item.get("technical_identity") or {}
            print(f"  {item['id']}: {item.get('name_en', '')} | grade={identity.get('grade', 'unspecified')}")
    print(f"Same-CAS groups requiring application/grade review: {groups}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
