#!/usr/bin/env python3
"""Conservatively remove unsupported supplier-specific guarantees, in three languages.

This is a one-shot, fail-closed, PUBLIC content-only migration. It does not
validate chemistry, expose a supplier, change any secret, send requests, or
alter Cloudflare/Turnstile/form code. It preserves general chemical identities,
product names and catalogue lookup; offered specifications remain unconfirmed.
The source master and localized machine-readable feeds are updated together.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "products-multilingual.json"
OVERRIDE = {"copper-oxide-feed": {
    "en": "en-copper-oxide-feed.html",
    "hu": "hu-rez-oxid-feed.html",
    "de-at": "de-at-kupferoxid-futtermittel.html",
}}
CFG = {
    "en": {
        "pack_label": "Packaging",
        "sds_label": "SDS status", "tds_label": "TDS status", "coa_label": "CoA status",
        "pack": "Packaging is confirmed with the selected supplier after enquiry.",
        "sds": "Availability of the supplier SDS is checked after enquiry.",
        "tds": "Availability of the supplier TDS is checked after enquiry.",
        "coa": "Lot-specific CoA availability is checked after enquiry.",
        "faq_marker": "Preferred packaging currently listed for orientation:",
        "faq": "Specify preferred packaging in your enquiry; actual formats and documents are confirmed with the supplier after contact.",
        "badge_old": "SDS/TDS/CoA on request",
        "badge_new": "Document status checked after enquiry",
    },
    "hu": {
        "pack_label": "Kiszerelés",
        "sds_label": "SDS státusz", "tds_label": "TDS státusz", "coa_label": "CoA státusz",
        "pack": "A kiszerelést kapcsolatfelvétel után, a kiválasztott beszállítóval egyeztetjük.",
        "sds": "Az SDS elérhetőségét kapcsolatfelvétel után ellenőrizzük.",
        "tds": "A TDS elérhetőségét kapcsolatfelvétel után ellenőrizzük.",
        "coa": "A tételszintű CoA elérhetőségét kapcsolatfelvétel után ellenőrizzük.",
        "faq_marker": "Orientációs kiszerelés a katalógusban:",
        "faq": "A kívánt kiszerelést jelezze az ajánlatkérésben; a tényleges lehetőségeket és dokumentumokat kapcsolatfelvétel után ellenőrizzük.",
        "badge_old": "SDS/TDS/CoA kérésre",
        "badge_new": "Dokumentumok egyeztetése ajánlatkérés után",
    },
    "de-at": {
        "pack_label": "Verpackung",
        "sds_label": "SDS-Status", "tds_label": "TDS-Status", "coa_label": "CoA-Status",
        "pack": "Die Verpackung wird nach Kontaktaufnahme mit dem ausgewählten Lieferanten bestätigt.",
        "sds": "Die Verfügbarkeit des Lieferanten-SDS wird nach der Anfrage geprüft.",
        "tds": "Die Verfügbarkeit des Lieferanten-TDS wird nach der Anfrage geprüft.",
        "coa": "Die Verfügbarkeit eines chargenbezogenen CoA wird nach der Anfrage geprüft.",
        "faq_marker": "Orientierende Verpackung laut Katalog:",
        "faq": "Bitte gewünschte Verpackung bei der Anfrage nennen; lieferbare Gebinde und Dokumente werden nach Kontaktaufnahme geprüft.",
        "badge_old": "SDS/TDS/CoA auf Anfrage",
        "badge_new": "Dokumentationsstatus nach Anfrage",
    },
}
DOC_FIELDS = {"sds_status_en": "sds", "sds_status_hu": "sds", "sds_status_de": "sds",
              "tds_status_en": "tds", "tds_status_hu": "tds", "tds_status_de": "tds",
              "coa_status_en": "coa", "coa_status_hu": "coa", "coa_status_de": "coa"}
LANG_KEY = {"en": "en", "hu": "hu", "de-at": "de"}
FAQ_SCRIPT = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S)
FORBIDDEN_PACKAGING = tuple(x["faq_marker"] for x in CFG.values())


def replace_doc_dd(html: str, label: str, replacement: str, route: str) -> str:
    pattern = re.compile(r'(<dt>' + re.escape(label) + r'</dt><dd>)(.*?)(</dd>)', re.S)
    matches = list(pattern.finditer(html))
    # Existing pages use either a generic "CoA status" field or the more
    # specific, already verified request-only "CoA / batch evidence" block.
    # Do not add or replace the latter; it is guarded by a separate CI test.
    if len(matches) == 0 and label in ("CoA status", "CoA státusz", "CoA-Status"):
        return html
    if len(matches) != 1:
        raise ValueError(f"{route}: expected one {label} in product detail, found {len(matches)}")
    return pattern.sub(lambda m: m.group(1) + replacement + m.group(3), html, count=1)


def clean_packaging_faq(html: str, cfg: dict, route: str) -> str:
    if cfg["faq_marker"] not in html:
        return html
    section_start = html.find('<section class="product-faq"')
    if section_start < 0:
        raise ValueError(f"{route}: missing visible FAQ section")
    # The marker may also exist in JSON-LD before the HTML. Only alter the
    # specific visible FAQ answer, then the corresponding JSON-LD answer.
    index = html.find(cfg["faq_marker"], section_start)
    if index < 0:
        raise ValueError(f"{route}: FAQ packaging marker only appears in schema")
    paragraph_start = html.rfind("<p>", section_start, index)
    paragraph_end = html.find("</p>", index)
    if paragraph_start < 0 or paragraph_end < 0:
        raise ValueError(f"{route}: cannot delimit visible packaging answer")
    html = html[:paragraph_start + 3] + cfg["faq"] + html[paragraph_end:]
    def change_json(match):
        graph = json.loads(match.group(2))
        for entity in graph.get("@graph", [graph]):
            if entity.get("@type") != "FAQPage":
                continue
            for faq in entity.get("mainEntity", []):
                answer = faq.get("acceptedAnswer", {})
                if cfg["faq_marker"] in str(answer.get("text", "")):
                    answer["text"] = cfg["faq"]
        return match.group(1) + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + match.group(3)
    html = FAQ_SCRIPT.sub(change_json, html)
    if cfg["faq_marker"] in html:
        raise ValueError(f"{route}: unverified packaging phrase still published")
    return html


def rewrite_html(html: str, lang: str, route: str) -> str:
    cfg = CFG[lang]
    expected_lang = {"en": "en", "hu": "hu-HU", "de-at": "de-AT"}[lang]
    if not re.search(r'<html\s+lang=["\']' + re.escape(expected_lang) + r'["\']', html, re.I):
        raise ValueError(f"{route}: wrong HTML language")
    package = re.compile(r'(<dt>' + re.escape(cfg["pack_label"]) + r'</dt><dd>)(.*?)(</dd>)', re.S)
    matches = len(package.findall(html))
    if matches < 3:
        raise ValueError(f"{route}: fewer than 3 packaging disclosures; got {matches}")
    html = package.sub(lambda m: m.group(1) + cfg["pack"] + m.group(3), html)
    for label, key in ((cfg["sds_label"], "sds"), (cfg["tds_label"], "tds"), (cfg["coa_label"], "coa")):
        html = replace_doc_dd(html, label, cfg[key], route)
    html = html.replace(cfg["badge_old"], cfg["badge_new"])
    html = clean_packaging_faq(html, cfg, route)
    # No catalogue packaging example may masquerade as a currently offered
    # form within a generic procurement introduction.
    if lang == "en":
        html = re.sub(r'packaging \([^<]*\) and delivery location',
                      'preferred packaging and delivery location', html)
    elif lang == "hu":
        html = re.sub(r'a kiszerelést \([^<]*\) és a szállítási helyet',
                      'a kívánt kiszerelést és a szállítási helyet', html)
    else:
        html = re.sub(r'Verpackung \([^<]*\) und Lieferort',
                      'gewünschte Verpackung und Lieferort', html)
    for term in FORBIDDEN_PACKAGING:
        if term in html:
            raise ValueError(f"{route}: product-specific unverified packaging FAQ still present")
    return html


def encode(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def build() -> dict[Path, str]:
    products = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    if len(products) != 127 or len({p["id"] for p in products}) != 127:
        raise ValueError("Unexpected catalogue family count or duplicated IDs")
    replacements: dict[Path, str] = {}
    routes = set()
    for product in products:
        for lang, cfg in CFG.items():
            path = ROOT / OVERRIDE.get(product["id"], {}).get(lang, f"{lang}-{product['id']}.html")
            if path.name in routes or not path.is_file():
                raise ValueError(f"Missing or duplicated product route: {path}")
            routes.add(path.name)
            original = path.read_text(encoding="utf-8")
            updated = rewrite_html(original, lang, path.name)
            # Include unchanged pages too, so --check audits all 381 routes.
            replacements[path] = updated
        # A publicly downloadable master must not contradict HTML.
        ident = product.setdefault("technical_identity", {})
        procurement = product.setdefault("procurement", {})
        for lang, cfg in CFG.items():
            short = LANG_KEY[lang]
            ident[f"packaging_{short}"] = cfg["pack"]
            procurement[f"packaging_{short}"] = cfg["pack"]
            doc = product.setdefault("documentation", {})
            for field in ("sds", "tds", "coa"):
                doc[f"{field}_status_{short}"] = cfg[field]
        ident["packaging"] = CFG["en"]["pack"]
        procurement["packaging"] = CFG["en"]["pack"]
    if len(routes) != 381:
        raise ValueError(f"Expected 381 routes, got {len(routes)}")
    replacements[CATALOGUE] = encode(products)
    # The three language feeds are also public; strip any unapproved sameAs
    # equivalence, which is a stronger assertion than a labelled Wikipedia
    # research link. No registry entry has a human-approved identity status.
    registry = {x["id"]: x for x in json.loads((ROOT / "entity-registry.json").read_text(encoding="utf-8"))["entities"]}
    for lang, cfg in CFG.items():
        path = ROOT / f"products-{lang}.json"
        feed = json.loads(path.read_text(encoding="utf-8"))
        if len(feed.get("products", [])) != 127:
            raise ValueError(f"{path.name}: wrong product count")
        for item in feed["products"]:
            if item["id"] not in registry:
                raise ValueError(f"{path.name}: unknown ID {item['id']}")
            item["commercialContext"]["packaging"] = cfg["pack"]
            item["documentation"] = {"SDS": cfg["sds"], "TDS": cfg["tds"], "CoA": cfg["coa"]}
            if registry[item["id"]].get("sameAs_status") != "verified":
                item["sameAs"] = []
        replacements[path] = encode(feed)
    return replacements


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write only reviewed public content fields")
    args = parser.parse_args()
    changes = build()
    missing = [p for p, value in changes.items()
               if p.read_text(encoding="utf-8") != value]
    if args.apply:
        for path in missing:
            path.write_text(changes[path], encoding="utf-8")
        print(f"Applied supplier-evidence deferral on {len(missing)} public HTML/JSON files")
        return 0
    print(f"Supplier-evidence content parity: {len(changes)} files checked; divergent={len(missing)}")
    for path in missing[:12]:
        print("DIFF:", path.relative_to(ROOT))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
