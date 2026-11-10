#!/usr/bin/env python3
"""Validate reviewed substitution records before any customer-facing publication.

The registry is deliberately empty until application-specific evidence is verified.
No third-party dependencies are required.
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID = {"research", "requires_validation", "approved", "rejected"}
TYPES = {"SDS", "TDS", "CoA", "regulatory", "manufacturer", "other"}

def main():
    catalogue = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    ids = {p["id"] for p in catalogue}
    records = json.loads((ROOT / "product-substitutions.json").read_text(encoding="utf-8"))
    errors = []
    if not isinstance(records, list):
        print("ERROR: substitution registry must be a list")
        return 1
    seen = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record {index}: expected object")
            continue
        src, dst = record.get("source_product_id"), record.get("candidate_product_id")
        key = (src, dst, record.get("application"))
        if key in seen:
            errors.append(f"record {index}: duplicate substitution/application relationship")
        seen.add(key)
        if src not in ids or dst not in ids or src == dst:
            errors.append(f"record {index}: invalid source/candidate product IDs")
        if record.get("status") not in VALID:
            errors.append(f"record {index}: invalid review status")
        for field in ("application", "technical_basis", "limitations"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"record {index}: missing {field}")
        evidence = record.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"record {index}: missing evidence")
            continue
        for item in evidence:
            if not isinstance(item, dict) or item.get("document_type") not in TYPES or not isinstance(item.get("reference"), str) or not item["reference"].strip():
                errors.append(f"record {index}: invalid evidence item")
                continue
            try:
                date.fromisoformat(item["verification_date"])
            except (KeyError, TypeError, ValueError):
                errors.append(f"record {index}: invalid evidence verification date")
        if record.get("status") == "approved":
            if not isinstance(record.get("reviewer"), str) or not record["reviewer"].strip():
                errors.append(f"record {index}: approved without reviewer")
            try:
                date.fromisoformat(record["review_date"])
            except (KeyError, TypeError, ValueError):
                errors.append(f"record {index}: approved without valid review date")
    print(f"Substitution registry: {len(records)} records, {sum(r.get('status') == 'approved' for r in records if isinstance(r, dict))} approved")
    for error in errors:
        print("ERROR:", error)
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
