#!/usr/bin/env python3
"""Protect batch-specific CoA disclosure on every EN/HU/DE catalogue page.

A static text check is not supplier-document verification.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
LANGUAGE_CLAIMS = {
    "en": ("CoA / batch evidence",
           "No independently verified batch CoA is linked on this catalogue page.",
           "Request a lot-specific CoA from the proposed supplier"),
    "hu": ("CoA / tételigazolás",
           "Az adatlapon nincs függetlenül ellenőrzött, letölthető tételigazolás.",
           "A kiválasztott beszállítótól az ajánlott gyártási tételre szóló CoA-t"),
    "de-at": ("CoA / Chargennachweis",
              "Auf dieser Katalogseite ist kein unabhängig geprüfter Chargennachweis verlinkt.",
              "Ein chargenbezogenes CoA beim vorgesehenen Lieferanten anfordern"),
}
UNSUPPORTED = (
    "Available when supplied by the producer for the offered lot",
    "Ha a gyártó az ajánlott tételhez biztosítja",
    "Wenn der Hersteller sie für die angebotene Charge bereitstellt",
)
errors = []
checked = 0
for product in PRODUCTS:
    for lang, claims in LANGUAGE_CLAIMS.items():
        page = ROOT / f"{lang}-{product['id']}.html"
        if not page.is_file():
            errors.append(f"{page.name}: missing page")
            continue
        html = page.read_text(encoding="utf-8")
        matches = re.findall(r'<dt>CoA / [^<]+</dt><dd>(.*?)</dd>', html, re.S | re.I)
        if len(matches) != 1:
            errors.append(f"{page.name}: expected one CoA status, found {len(matches)}")
            continue
        for claim in claims:
            if claim not in html:
                errors.append(f"{page.name}: missing CoA caveat or request instruction: {claim}")
        if any(phrase in html for phrase in UNSUPPORTED):
            errors.append(f"{page.name}: superseded blanket CoA availability text")
        checked += 1

if checked != 378:
    errors.append(f"Expected 378 CoA status blocks; checked {checked}")
print(f"Supplier CoA status parity: {checked} product pages; errors={len(errors)}")
for error in errors[:50]:
    print("ERROR:", error)
raise SystemExit(bool(errors))
