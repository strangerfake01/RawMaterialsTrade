#!/usr/bin/env python3
"""Measure misleading concentration/form fields without fabricating specifications.

Non-numeric values are candidates for manual review, not automatically false:
'anhydrous', 'solution', or 'technical' may be meaningful grade descriptors.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
assert len(products) == 126
review = []
placeholders = []
for product in products:
    ident = product.get("technical_identity") or {}
    concentration = str(ident.get("concentration_en") or ident.get("concentration") or "").strip()
    grade = str(ident.get("grade_en") or ident.get("grade") or "").strip()
    form = str(ident.get("form_en") or "").strip()
    # A grade or particle size is not, by itself, a measured chemical concentration.
    looks_quantitative = bool(re.search(r"\d+(?:[.,]\d+)?\s*(?:%|wt%|w/w|g/l|mg/l|mol/l|ppm|ppb)(?![A-Za-z])", concentration, re.I))
    if concentration and not looks_quantitative:
        review.append((product["id"], concentration, grade))
        if ident.get("concentration_semantics") != "grade_or_form_descriptor_not_numeric" or ident.get("concentration_value_verified") is not False:
            raise SystemExit(f"{product['id']}: nonnumeric concentration must be explicitly marked as a grade/form descriptor")
    cas = str(ident.get("cas") or "")
    if " / " in cas:
        if ident.get("cas_identifier_status") != "multiple_candidates_unverified" or ident.get("cas_candidate_identifiers") != cas.split(" / "):
            raise SystemExit(f"{product['id']}: multiple CAS candidates must be separately recorded as unverified")
    elif not re.fullmatch(r"\d{2,7}-\d{2}-\d", cas):
        if ident.get("cas_identifier_status") != "supplier_identity_required" or ident.get("cas_candidate_identifiers") != []:
            raise SystemExit(f"{product['id']}: CAS placeholder must not be interpreted as an identifier")
    if "supplier documentation" in form.lower() or "to be confirmed" in form.lower():
        placeholders.append(product["id"])
print("Technical-field semantics: %d families" % len(products))
print("Concentration fields without quantitative concentration units (manual review):", len(review))
print("Form fields with supplier-confirmation placeholders:", len(placeholders))
for pid, value, grade in review[:25]:
    print("REVIEW concentration:", pid, "| value:", value[:100], "| grade:", grade[:100])
if len({p["id"] for p in products}) != len(products):
    raise SystemExit("Duplicate product IDs")
if not review:
    print("No semantic concentration candidates found; no data changes needed")
# A review inventory is deliberately non-blocking; it cannot establish actual specifications.
