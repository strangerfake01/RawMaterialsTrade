#!/usr/bin/env python3
"""Check that every same-CAS group is assigned exactly one review priority."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
queue = ROOT / "reports" / "same-cas-review-queue.csv"
plan = ROOT / "docs" / "same-cas-review-priorities-2026-11-10.md"
rows = list(csv.DictReader(queue.open(encoding="utf-8", newline="")))
expected = {r["cas"] for r in rows}
content = plan.read_text(encoding="utf-8")
p0 = content.split("## P0", 1)[1].split("## P1", 1)[0]
p1 = content.split("## P1", 1)[1].split("## Operational sequence", 1)[0]
pattern = r"CAS\s+(\d{2,7}-\d{2}-\d)"
found0 = set(re.findall(pattern, p0))
found1 = set(re.findall(pattern, p1))
missing = expected - found0 - found1
extra = (found0 | found1) - expected
overlap = found0 & found1
if missing or extra or overlap:
    raise SystemExit(f"Priority coverage failed: missing={sorted(missing)}, extra={sorted(extra)}, duplicate={sorted(overlap)}")
print(f"PASS: {len(rows)} candidate pairs in {len(expected)} groups; P0={len(found0)}, P1={len(found1)}; all covered")
