#!/usr/bin/env python3
"""Default-deny offered-grade claims until supplier-specific evidence is reviewed.

Keep product names and requested-variant categories as B2B search/inquiry
designations, NOT as evidence of available commercial grade, purity or form.
The exact offered grade/concentration/form is unknown until supplier contact.

Update 381 static product HTML pages + multilingual canonical master + the
three localized public product feeds together. No private data, offer claims,
chemical identifier mutations, form submissions, Worker/Turnstile/CSP edits.
Read-only by default; --apply performs an audited, scope-limited migration.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "products-multilingual.json"
OVERRIDES = {
    "copper-oxide-feed": {
        "en": "en-copper-oxide-feed.html",
        "hu": "hu-rez-oxid-feed.html",
        "de-at": "de-at-kupferoxid-futtermittel.html",
    },
}
CFG = {
    "en": {
        "status": "Offered grade, purity, concentration and form are confirmed after contact from the selected supplier's current documents.",
        "requested": "State the required grade, purity or concentration and form, if relevant; the offered specification is checked with the selected supplier after enquiry.",
        "field": "Offered specification",
    },
    "hu": {
        "status": "A kínálható minőség, tisztaság, koncentráció és forma a kiválasztott beszállító aktuális dokumentációja alapján, kapcsolatfelvétel után igazolható.",
        "requested": "Az ajánlatkérésben adja meg a kívánt minőséget, tisztaságot, koncentrációt vagy formát; a tényleges specifikációt kapcsolatfelvétel után ellenőrizzük.",
        "field": "Ajánlott minőség és specifikáció",
    },
    "de-at": {
        "status": "Angebotene Qualität, Reinheit, Konzentration und Form werden nach Kontaktaufnahme anhand der aktuellen Unterlagen des ausgewählten Lieferanten bestätigt.",
        "requested": "Bitte geforderte Qualität, Reinheit, Konzentration oder Form nennen; die lieferbare Spezifikation wird nach Kontaktaufnahme beim Lieferanten geprüft.",
        "field": "Angebotene Qualität und Spezifikation",
    },
}
GRADE_LABELS = {
    "en": ("Grade / concentration", "Grade / form", "Grade / product designation"),
    "hu": ("Minőség / koncentráció", "Minőség / forma", "Minőség / termékmegnevezés"),
    "de-at": ("Qualität / Konzentration", "Qualität / Form", "Qualität / Produktbezeichnung"),
}
SOURCE_LANG = {"en": "en", "hu": "hu", "de-at": "de"}
SOURCE_KEYS = ("grade", "concentration")


def check_and_rewrite_html(source: str, lang: str, route: str) -> str:
    config = CFG[lang]
    wanted = "|".join(re.escape(label) for label in GRADE_LABELS[lang])
    label_dd = re.compile(
        r'(<dt>(?:' + wanted + r')</dt><dd>)(.*?)(</dd>)', re.S
    )
    matches = label_dd.findall(source)
    if len(matches) != 2:
        raise ValueError(f"{route}: expected 2 grade/form disclosures, got {len(matches)}")
    result = label_dd.sub(lambda m: m.group(1) + config["status"] + m.group(3), source)
    # Remove the catalogue's former example as if it were the concentration
    # or purity that RMT can now supply; this is a requested-variant inquiry.
    markers = {
        "en": r'Target concentration or purity where relevant: currently listed orientation — [^<]*',
        "hu": r'Célkoncentráció vagy tisztaság, ha releváns: katalógus-orientáció — [^<]*',
        "de-at": r'Zielkonzentration oder Reinheit, falls relevant: Katalogorientierung — [^<]*',
    }
    result = re.sub(
        r'(<li>)' + markers[lang] + r'(</li>)',
        lambda m: m.group(1) + config["requested"] + m.group(2),
        result,
    )
    if any(re.search(s, result) for s in markers.values()):
        raise ValueError(f"{route}: unverified target grade promoted as offered concentration")
    return result


def encode(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def build() -> dict[Path, str]:
    products = json.loads(SOURCE.read_text(encoding="utf-8"))
    if len(products) != 127 or len({p["id"] for p in products}) != 127:
        raise ValueError("Catalogue identity count invalid")
    replacement: dict[Path, str] = {}
    seen: set[str] = set()
    for product in products:
        technical = product.get("technical_identity")
        if not isinstance(technical, dict):
            raise ValueError(f"{product['id']}: technical identity missing")
        for lang, cfg in CFG.items():
            route = OVERRIDES.get(product["id"], {}).get(lang, f"{lang}-{product['id']}.html")
            if route in seen:
                raise ValueError(f"Duplicated route: {route}")
            seen.add(route)
            path = ROOT / route
            if not path.is_file():
                raise ValueError(f"Missing product HTML: {route}")
            html = path.read_text(encoding="utf-8")
            expected_lang = {"en": "en", "hu": "hu-HU", "de-at": "de-AT"}[lang]
            if not re.search(r'<html\\s+lang="' + re.escape(expected_lang) + '"', html, re.I):
                raise ValueError(f"{route}: incorrect language")
            replacement[path] = check_and_rewrite_html(html, lang, route)
            suffix = SOURCE_LANG[lang]
            for key in SOURCE_KEYS:
                technical[f"{key}_{suffix}"] = cfg["status"]
        for key in SOURCE_KEYS:
            technical[key] = CFG["en"]["status"]
        # Both statuses are open until the exact selected lot and supplier
        # documents are independently qualified by an authorized human.
        technical["concentration_value_verified"] = False
    if len(seen) != 381:
        raise ValueError(f"Expected 381 localized product routes, got {len(seen)}")
    replacement[SOURCE] = encode(products)
    for lang, cfg in CFG.items():
        path = ROOT / f"products-{lang}.json"
        public = json.loads(path.read_text(encoding="utf-8"))
        if len(public.get("products", [])) != 127:
            raise ValueError(f"Expected 127 product records in {path.name}")
        if {p["id"] for p in public["products"]} != {p["id"] for p in products}:
            raise ValueError(f"{path.name}: product identity drift")
        for item in public["products"]:
            if "gradeOrConcentration" not in item.get("commercialContext", {}):
                raise ValueError(f"{path.name}: grade field missing for {item['id']}")
            item["commercialContext"]["gradeOrConcentration"] = cfg["status"]
        replacement[path] = encode(public)
    if len(replacement) != 385:
        raise ValueError(f"Unexpected changed-file scope {len(replacement)}")
    return replacement


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write only public offered-grade claim fields")
    args = parser.parse_args()
    outputs = build()
    different = [p for p, content in outputs.items() if p.read_text(encoding="utf-8") != content]
    print(f"Unverified grade evidence boundary: 381 HTML products + 4 public JSON sources; divergent={len(different)}")
    if args.apply:
        for path in different:
            path.write_text(outputs[path], encoding="utf-8")
        print(f"Updated {len(different)} public files only")
        return 0
    for path in different[:12]:
        print("UNVERIFIED OFFERED GRADE:", path.name)
    return 1 if different else 0


if __name__ == "__main__":
    raise SystemExit(main())
