#!/usr/bin/env python3
"""Measure misleading concentration/form fields without fabricating specifications.

Non-numeric values are candidates for manual review, not automatically false:
'anhydrous', 'solution', or 'technical' may be meaningful grade descriptors.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
assert len(products) == 126
review = []
placeholders = []
cas_checked = 0

def valid_cas_checksum(value):
    match = re.fullmatch(r"(\d{2,7})-(\d{2})-(\d)", value)
    if not match:
        return False
    digits = match.group(1) + match.group(2)
    return sum((index + 1) * int(digit) for index, digit in enumerate(reversed(digits))) % 10 == int(match.group(3))
for product in products:
    ident = product.get("technical_identity") or {}
    concentration = str(ident.get("concentration_en") or ident.get("concentration") or "").strip()
    grade = str(ident.get("grade_en") or ident.get("grade") or "").strip()
    form = str(ident.get("form_en") or "").strip()
    # A grade or particle size is not, by itself, a measured chemical concentration.
    looks_quantitative = bool(re.search(r"\d+(?:[.,]\d+)?\s*(?:%|wt%|w/w|g/l|mg/l|mol/l|ppm|ppb)(?![A-Za-z])", concentration, re.I))
    is_supplier_placeholder = concentration.casefold() in {"confirmed upon supplier documentation", "to be confirmed"}
    if concentration and not looks_quantitative and not is_supplier_placeholder:
        review.append((product["id"], concentration, grade))
        if ident.get("concentration_semantics") != "grade_or_form_descriptor_not_numeric" or ident.get("concentration_value_verified") is not False:
            raise SystemExit(f"{product['id']}: nonnumeric concentration must be explicitly marked as a grade/form descriptor")
    cas = str(ident.get("cas") or "")
    cas_candidates = ident.get("cas_candidate_identifiers") or []
    for candidate in (cas_candidates if cas_candidates else ([cas] if re.fullmatch(r"\d{2,7}-\d{2}-\d", cas) else [])):
        cas_checked += 1
        if not valid_cas_checksum(candidate):
            raise SystemExit(f"{product['id']}: CAS checksum or format invalid: {candidate}")
    if " / " in cas:
        if ident.get("cas_identifier_status") != "multiple_candidates_unverified" or ident.get("cas_candidate_identifiers") != cas.split(" / "):
            raise SystemExit(f"{product['id']}: multiple CAS candidates must be separately recorded as unverified")
    elif not re.fullmatch(r"\d{2,7}-\d{2}-\d", cas):
        if ident.get("cas_identifier_status") != "supplier_identity_required" or ident.get("cas_candidate_identifiers") != []:
            raise SystemExit(f"{product['id']}: CAS placeholder must not be interpreted as an identifier")
    if ident.get("cas_identifier_status") and not (" / " in cas or not re.fullmatch(r"\d{2,7}-\d{2}-\d", cas)):
        raise SystemExit(f"{product['id']}: stale CAS uncertainty flag on a single numeric identifier")
    if is_supplier_placeholder or "supplier documentation" in form.lower() or "to be confirmed" in form.lower():
        placeholders.append(product["id"])
print("Technical-field semantics: %d families; CAS checksums verified: %d" % (len(products), cas_checked))
print("Concentration fields without quantitative concentration units (manual review):", len(review))
print("Form fields with supplier-confirmation placeholders:", len(placeholders))
for pid, value, grade in review[:25]:
    print("REVIEW concentration:", pid, "| value:", value[:100], "| grade:", grade[:100])
if len({p["id"] for p in products}) != len(products):
    raise SystemExit("Duplicate product IDs")
if not review:
    print("No semantic concentration candidates found; no data changes needed")
# A review inventory is deliberately non-blocking; it cannot establish actual specifications.

# Regression guard for verified hydrate formula corrections and nonnumeric form labels.
hydrate_formulas = {
    "cink-szulfat-monohidrat-feed": "ZnSO₄·H₂O",
    "cink-szulfat-monohidrat-heptahidrat-industrial": "ZnSO₄·H₂O; heptahydrate: ZnSO₄·7H₂O",
    "kalcium-klorid-dihidrat-7880-pikkelyes-deicing": "CaCl₂·2H₂O",
}
form_only_families = {
    "cink-szulfat-monohidrat-feed",
    "cink-szulfat-monohidrat-heptahidrat-industrial",
    "citromsav-monohidrat-anhidrat-food",
    "borax-dekahidrat-industrial",
    "magnezium-klorid-hexahidrat-industrial",
    "rez-szulfat-pentahidrat-industrial",
    "aceton-technikai-regeneralt-industrial",
    "aluminium-szulfat-03-mm-38-mm-industrial",
    "etil-acetat-technikai-regeneralt-industrial",
    "magnezium-oxid-feed",
    "magnezium-oxid-nehez-industrial",
    "metanol-technikai-regeneralt-industrial",
    "natrium-benzoat-gran-food",
    "natrium-hidroxid-mikrogyongy-pikkelyes-industrial",
    "natrium-karbonat-konnyu-industrial",
    "natrium-karbonat-nehez-industrial",
    "natrium-acetat-vizmentes-3h2o-industrial",
    "mangan-klorid-monohidrat-tetrahidrat-industrial",
    "natrium-metaszilikat-industrial",
    "natrium-szulfat-industrial",
    "natronvizuveg-oldatok-industrial",
    "sotabletta-industrial",
    "rez-klorid-dihidrat-industrial",
    "trinatrium-foszfat-dodekahidrat-vizmentes-industrial",
    "vas-ii-szulfat-monohidrat-heptahidrat-industrial",
    "vas-ii-szulfat-monohidrat-feed",
    "trinatrium-citrat-industrial",
    "natrium-molibdat-feed",
    "natrium-perkarbonat-industrial",
    "sosav-technikai-regeneralt-industrial",
    "natrium-tripolifoszfat-industrial",
    "sosav-gyogyszerkonyvi-food",
    "utszoro-so-deicing",
}
old_form_labels = {
    "en": "<dt>Grade / concentration</dt>",
    "hu": "<dt>Minőség / koncentráció</dt>",
    "de-at": "<dt>Qualität / Konzentration</dt>",
}
by_id = {product["id"]: product for product in products}
for pid, expected in hydrate_formulas.items():
    actual = str(by_id[pid]["technical_identity"].get("formula", ""))
    if expected not in actual:
        raise SystemExit(f"{pid}: corrected hydrate formula missing from catalogue")
for pid in set(hydrate_formulas) | form_only_families:
    for lang in ("en", "hu", "de-at"):
        html = (ROOT / f"{lang}-{pid}.html").read_text(encoding="utf-8")
        if pid in hydrate_formulas:
            if lang == "hu" and pid == "cink-szulfat-monohidrat-heptahidrat-industrial":
                expected = "ZnSO₄·H₂O; heptahidrát: ZnSO₄·7H₂O"
            elif lang == "de-at" and pid == "cink-szulfat-monohidrat-heptahidrat-industrial":
                expected = "ZnSO₄·H₂O; Heptahydrat: ZnSO₄·7H₂O"
            else:
                expected = hydrate_formulas[pid]
            if expected not in html:
                raise SystemExit(f"{lang}-{pid}: corrected hydrate formula missing from HTML")
        if pid in form_only_families and old_form_labels[lang] in html:
            raise SystemExit(f"{lang}-{pid}: hydrate form still mislabeled as concentration")
print("Hydrate formula and form-label regression checks: passed")
