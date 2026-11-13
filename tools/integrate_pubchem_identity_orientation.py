#!/usr/bin/env python3
"""Add clearly labelled external identity orientation to pages lacking a catalogue formula.

The values are not promoted to the canonical supplier identity. They remain source-reported
orientation and explicitly require confirmation against the selected supplier SDS/TDS.
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
products = {p["id"]: p for p in json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))}
research = json.loads((ROOT / "audits/pubchem-cas-research-2026-11-13.json").read_text(encoding="utf-8"))

labels = {
    "en": ("External identity orientation", "Formula", "Molecular weight", "source-reported", "PubChem source-reported data; confirm the selected commercial grade against current supplier SDS/TDS."),
    "hu": ("Külső azonossági tájékoztató", "Képlet", "Molekulatömeg", "külső forrásadat", "PubChem-forrásadat; a kiválasztott kereskedelmi minőséget az aktuális beszállítói SDS/TDS alapján kell megerősíteni."),
    "de": ("Externe Identitätsorientierung", "Formel", "Molekulargewicht", "externe Quelldaten", "Von PubChem berichtete Orientierungsdaten; die gewählte Handelsqualität ist anhand des aktuellen Lieferanten-SDS/TDS zu bestätigen."),
}

def lang(path: Path) -> str:
    return "hu" if path.name.startswith("hu-") else "de" if path.name.startswith("de-at-") else "en"

def pid(path: Path) -> str:
    return re.sub(r"^(?:en|hu|de-at)-", "", path.stem)

changed = []
for path in sorted(ROOT.glob("*.html")):
    product_id = pid(path)
    if product_id not in products or "product-dl" not in path.read_text(encoding="utf-8"):
        continue
    html = path.read_text(encoding="utf-8")
    if "external-identity-orientation" in html:
        continue
    formula = str((products[product_id].get("technical_identity") or {}).get("formula") or "")
    if formula and not any(x in formula.lower() for x in ("confirm", "beszállít", "lieferant", "to be confirmed")):
        continue
    row = next((r for r in research if r.get("id") == product_id and r.get("formula") and r.get("molecular_weight")), None)
    if not row:
        continue
    l, f_label, mw_label, source_label, note = labels[lang(path)]
    block = (
        f'<div class="external-identity-orientation" aria-label="{l}">'
        f'<dt>{f_label} · {source_label}</dt><dd>{row["formula"]}</dd>'
        f'<dt>{mw_label} · {source_label}</dt><dd>{row["molecular_weight"]} g/mol</dd>'
        f'</div>'
    )
    # Add a single labelled block inside the existing decision summary.
    html, n = re.subn(r'(<dl class="product-dl">)', r'\1' + block, html, count=1)
    if not n:
        continue
    html = html.replace('</dl><p class="microcopy rich-note">', f'</dl><p class="microcopy rich-note">{note} ', 1)
    path.write_text(html, encoding="utf-8")
    changed.append(path.name)

print(f"Integrated external identity orientation on {len(changed)} pages")
for name in changed:
    print(name)
