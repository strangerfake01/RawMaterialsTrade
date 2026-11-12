#!/usr/bin/env python3
"""Create a redacted, deterministic change manifest from the Drive workbook.

This script deliberately does not edit product pages or catalogue data. It is
the safe input stage for the OpenAI review gate in GitHub Actions.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

from openpyxl import load_workbook


ALLOWED_SHEETS = {"Product master", "Products"}
BLOCKED_TERMS = ("price", "stock", "supplier", "customer", "email", "phone", "password", "secret", "token")
SENSITIVE_FIELDS = {"price", "stock", "supplier", "customer", "email", "phone", "password", "secret", "token", "incoterm", "moq"}


def norm(value: object) -> str:
    return " ".join(str(value or "").split())


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: product_master_change_manifest.py WORKBOOK OUTPUT_JSON", file=sys.stderr)
        return 2
    workbook_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    if not workbook_path.is_file():
        print(f"missing workbook: {workbook_path}", file=sys.stderr)
        return 2

    wb = load_workbook(workbook_path, read_only=True, data_only=True)
    sheet_name = next((name for name in wb.sheetnames if name in ALLOWED_SHEETS), None)
    if not sheet_name:
        print(f"missing allowed product sheet; found={wb.sheetnames}", file=sys.stderr)
        return 1
    ws = wb[sheet_name]
    rows = ws.iter_rows(values_only=True)
    headers = [norm(x) for x in next(rows)]
    if "id" not in headers:
        print("product sheet must have an id column", file=sys.stderr)
        return 1
    id_index = headers.index("id")
    changes = []
    blocked = []
    product_ids = set()
    for row_number, values in enumerate(rows, start=2):
        row = {headers[i]: norm(values[i]) if i < len(values) else "" for i in range(len(headers))}
        product_id = row.get("id", "")
        if not product_id:
            continue
        if product_id in product_ids:
            print(f"duplicate product id at row {row_number}: {product_id}", file=sys.stderr)
            return 1
        product_ids.add(product_id)
        for field, value in row.items():
            if field in ("id", "missing_information") or not value:
                continue
            field_lower = field.lower()
            if any(term in field_lower for term in BLOCKED_TERMS) or field_lower in SENSITIVE_FIELDS:
                blocked.append({"row": row_number, "product_id": product_id, "field": field, "reason": "commercial_or_sensitive_field"})
                continue
            changes.append({
                "product_id": product_id,
                "field": field,
                "value_sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
                "value_present": True,
                "row": row_number,
            })

    manifest = {
        "schema_version": "1.0",
        "source_file": workbook_path.name,
        "source_sha256": hashlib.sha256(workbook_path.read_bytes()).hexdigest(),
        "sheet": sheet_name,
        "product_count": len(product_ids),
        "change_count": len(changes),
        "blocked_count": len(blocked),
        "changes": changes,
        "blocked_fields": blocked,
        "policy": {
            "status": "review_required",
            "sameAs_default": "withheld",
            "substitution_default": "not-assessed",
            "commercial_fields": "never_public",
            "values_redacted": True,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"manifest={output_path} products={len(product_ids)} changes={len(changes)} blocked={len(blocked)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
