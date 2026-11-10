#!/usr/bin/env python3
"""Create a reproducible, non-approval review queue for same-CAS product variants.

This report is a screening aid, not evidence of substitution. It does not modify
the governed substitution registry or any public product page.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "same-cas-review-queue.csv"
FIELDS = [
    "cas", "source_product_id", "candidate_product_id", "source_name_en",
    "candidate_name_en", "source_grade", "candidate_grade", "review_status",
    "application_to_verify", "supplier_tds", "supplier_sds", "batch_coa",
    "regulatory_grade_evidence", "process_validation", "qualified_reviewer",
]

def main():
    catalogue = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    grouped = defaultdict(list)
    for p in catalogue:
        cas = str((p.get("technical_identity") or {}).get("cas") or "").strip()
        if cas and "/" not in cas and "confirm" not in cas.lower():
            grouped[cas].append(p)
    rows = []
    for cas, products in sorted(grouped.items()):
        if len(products) < 2:
            continue
        for i, a in enumerate(products):
            for b in products[i + 1:]:
                rows.append({
                    "cas": cas,
                    "source_product_id": a["id"],
                    "candidate_product_id": b["id"],
                    "source_name_en": a.get("name_en", ""),
                    "candidate_name_en": b.get("name_en", ""),
                    "source_grade": (a.get("technical_identity") or {}).get("grade", ""),
                    "candidate_grade": (b.get("technical_identity") or {}).get("grade", ""),
                    "review_status": "not_assessed",
                    "application_to_verify": "",
                    "supplier_tds": "required",
                    "supplier_sds": "required",
                    "batch_coa": "required",
                    "regulatory_grade_evidence": "required_if_applicable",
                    "process_validation": "required",
                    "qualified_reviewer": "",
                })
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created {OUT.relative_to(ROOT)}: {len(rows)} candidate pairs, all not_assessed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
