#!/usr/bin/env python3
"""Fail closed on cross-substance content and unverified supplier claims for CuO.

Copper(II) oxide general identity: EU 2018/1039 (3b404), PubChem CAS 1317-38-0.
Those public references do not verify any RMT supplier grade, batch or feed use.
No network, emails, private business data or certificate claims are involved.
"""
from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "en-copper-oxide-feed.html": {
        "lang": "en", "name": "Copper(II) oxide",
        "marker": "after contact",
        "wiki": "https://en.wikipedia.org/wiki/Copper(II)_oxide",
    },
    "hu-rez-oxid-feed.html": {
        "lang": "hu-HU", "name": "Réz(II)-oxid",
        "marker": "kapcsolatfelvétel után",
        "wiki": "https://hu.wikipedia.org/wiki/R%C3%A9z(II)-oxid",
    },
    "de-at-kupferoxid-futtermittel.html": {
        "lang": "de-AT", "name": "Kupfer(II)-oxid",
        "marker": "nach Kontaktaufnahme",
        "wiki": "https://de.wikipedia.org/wiki/Kupfer(II)-oxid",
    },
}
KNOWN_MIXUPS = re.compile(
    r"Zinc salt used as flux|Erősen higroszkópos cinksó|"
    r"Zinkergänzung in Futtermitteln|Cink-klorid(?!-)|"
    r"Zinkchlorid|Zinc%20Chloride|"
    r"Q204714|zinc chloride|"
    r"Zn assay|Zn-Gehalt|Zn-tartalm",
    re.I,
)
errors = []
for route, expected in PAGES.items():
    html = (ROOT / route).read_text(encoding="utf-8")
    if not re.search(r'<html[^>]*lang="' + re.escape(expected["lang"]) + '"', html, re.I):
        errors.append(f"{route}: HTML language mismatch")
    if KNOWN_MIXUPS.search(html):
        errors.append(f"{route}: cross-substance zinc chloride contamination")
    if expected["wiki"] not in html:
        errors.append(f"{route}: external article does not match CuO")
    if '<section class="product-alternative">' in html:
        errors.append(f"{route}: unsupported self-comparison still published")
    lead = re.search(r'<p class="lead">([^<]+)</p>', html)
    if not lead or expected["marker"].lower() not in unescape(lead.group(1)).lower():
        errors.append(f"{route}: unverified supplier grade not deferred after contact")
    schema_nodes = []
    for raw in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        obj = json.loads(raw)
        schema_nodes += obj.get("@graph", [obj])
    chemicals = [x for x in schema_nodes if isinstance(x, dict)
                 and x.get("@type") == "ChemicalSubstance"
                 and x.get("@id", "").endswith("#material")]
    if len(chemicals) != 1:
        errors.append(f"{route}: expected one exact ChemicalSubstance")
        continue
    chemical = chemicals[0]
    if chemical.get("chemicalComposition") != "CuO":
        errors.append(f"{route}: wrong formula")
    identifiers = chemical.get("identifier") or []
    if not any(x.get("propertyID") == "CAS" and x.get("value") == "1317-38-0"
               for x in identifiers if isinstance(x, dict)):
        errors.append(f"{route}: wrong general substance CAS")
    if chemical.get("alternateName"):
        errors.append(f"{route}: unverified alternateName was added")
    if KNOWN_MIXUPS.search(str(chemical.get("description", ""))):
        errors.append(f"{route}: wrong chemical description")
    if any(k in chemical for k in ("offers", "aggregateRating", "manufacturer")):
        errors.append(f"{route}: unsupported commercial claims in JSON-LD")

print(f"CuO evidence boundary: {len(PAGES)} language routes, {len(errors)} errors")
for error in errors:
    print("ERROR:", error)
raise SystemExit(bool(errors))
