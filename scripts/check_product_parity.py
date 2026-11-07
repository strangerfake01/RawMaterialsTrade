#!/usr/bin/env python3
"""Fail when published product pages drift from catalogue and SEO data.

Run from repository root: python3 scripts/check_product_parity.py
No third-party dependencies. Checks all product routes and detailed guidance.
"""
import html
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
LANGS = {"en": "en", "hu": "hu", "de-at": "de"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text_parts = []
        self.schema_parts = []
        self.in_schema = False
        self.hidden_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style", "template", "noscript"):
            self.hidden_depth += 1
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_schema = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_schema = False
        if tag in ("script", "style", "template", "noscript"):
            self.hidden_depth = max(0, self.hidden_depth - 1)

    def handle_data(self, data):
        if self.in_schema:
            self.schema_parts.append(data)
        elif self.hidden_depth == 0:
            self.text_parts.append(data)


def norm(value):
    return " ".join(html.unescape(str(value)).split())


def main():
    products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    failures = []
    checked = 0
    seen_ids = set()
    for product in products:
        product_id = product.get("id")
        if not isinstance(product_id, str) or not product_id:
            failures.append("catalogue: product without valid id")
            continue
        if product_id in seen_ids:
            failures.append(f"catalogue: duplicate id {product_id}")
        seen_ids.add(product_id)
        for prefix in LANGS:
            route = ROOT / f"{prefix}-{product_id}.html"
            if not route.is_file():
                failures.append(f"{route.name}: missing catalogue product route")
                continue
            page = route.read_text(encoding="utf-8")
            expected_lang = {"en": "en", "hu": "hu-HU", "de-at": "de-AT"}[prefix]
            if not re.search(r'<html\s+lang=[\x22\x27]' + re.escape(expected_lang) + r'[\x22\x27]', page, re.I):
                failures.append(f"{route.name}: wrong html lang")
            expected_url = f"https://www.rawmaterialstrade.com/{route.name}"
            if not re.search(r'<link\b(?=[^>]*\brel=[\x22\x27]canonical[\x22\x27])(?=[^>]*\bhref=[\x22\x27]' + re.escape(expected_url) + r'[\x22\x27])[^>]*>', page, re.I):
                failures.append(f"{route.name}: missing or wrong canonical")
            for sibling, hreflang in (("en", "en"), ("hu", "hu-HU"), ("de-at", "de-AT"), ("en", "x-default")):
                sibling_url = f"https://www.rawmaterialstrade.com/{sibling}-{product_id}.html"
                if not re.search(r'<link\b(?=[^>]*\brel=[\x22\x27]alternate[\x22\x27])(?=[^>]*\bhreflang=[\x22\x27]' + re.escape(hreflang) + r'[\x22\x27])(?=[^>]*\bhref=[\x22\x27]' + re.escape(sibling_url) + r'[\x22\x27])[^>]*>', page, re.I):
                    failures.append(f"{route.name}: missing {hreflang} alternate")
    # Validate machine-readable product identity for every language route.
    for product in products:
        product_id = product.get("id")
        if not isinstance(product_id, str) or not product_id:
            continue
        for prefix in LANGS:
            route = ROOT / f"{prefix}-{product_id}.html"
            if not route.is_file():
                continue
            parser = PageParser()
            parser.feed(route.read_text(encoding="utf-8"))
            expected_url = f"https://www.rawmaterialstrade.com/{route.name}"
            entities = []
            for raw in parser.schema_parts:
                try:
                    graph = json.loads(raw)
                    if isinstance(graph, dict):
                        nodes = graph.get("@graph", [graph])
                        if isinstance(nodes, list):
                            entities.extend(node for node in nodes if isinstance(node, dict))
                except (ValueError, TypeError):
                    failures.append(f"{route.name}: invalid JSON-LD")
            for entity_type, suffix in (("WebPage", "#webpage"), ("material", "#material")):
                if not any(
                    (entity.get("@type") in ("ChemicalSubstance", "DefinedTerm") if entity_type == "material" else entity.get("@type") == entity_type)
                    and entity.get("@id") == expected_url + suffix
                    for entity in entities
                ):
                    failures.append(f"{route.name}: missing or mismatched {entity_type} identity")
    for product in products:
        procurement = product.get("procurement") or {}
        if not procurement.get("buyer_guidance_en"):
            continue
        for prefix, lang in LANGS.items():
            path = ROOT / (prefix + "-" + product["id"] + ".html")
            if not path.is_file():
                failures.append(f"{path.name}: missing HTML")
                continue
            source = path.read_text(encoding="utf-8")
            parser = PageParser()
            parser.feed(source)
            visible = norm(" ".join(parser.text_parts))
            for key in ("buyer_guidance_", "rfq_guidance_", "packaging_"):
                expected = procurement.get(key + lang)
                if not expected:
                    failures.append(f"{path.name}: missing catalogue {key + lang}")
                elif norm(expected) not in visible:
                    failures.append(f"{path.name}: visible {key + lang} differs from catalogue")
            if "product-procurement-guidance" not in source:
                failures.append(f"{path.name}: missing procurement accordion")
            try:
                graphs = [json.loads(item) for item in parser.schema_parts]
                entities = []
                for graph in graphs:
                    entities.extend(graph.get("@graph", [graph]))
                chemicals = [e for e in entities if e.get("@type") == "ChemicalSubstance"]
                services = [e for e in entities if e.get("@type") == "Service"]
                if not chemicals or not services:
                    failures.append(f"{path.name}: missing ChemicalSubstance or Service")
                elif not any(
                    service.get("about", {}).get("@id") == chemical.get("@id")
                    for service in services for chemical in chemicals
                ):
                    failures.append(f"{path.name}: disconnected Service / ChemicalSubstance")
            except (ValueError, TypeError, AttributeError) as exc:
                failures.append(f"{path.name}: invalid JSON-LD ({exc})")
            checked += 1
    print(f"Checked {len(seen_ids)} catalogue product IDs for three-language route coverage.")
    print(f"Checked {checked} language pages with detailed procurement guidance.")
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        raise SystemExit(1)
    print("PASS: catalogue, visible copy, accordion and entity relationships agree.")


if __name__ == "__main__":
    main()
