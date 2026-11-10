#!/usr/bin/env python3
"""Regression gate: MnO linked-product labels must not identify MnO as MnO2.

Run from the repository root: python3 scripts/check-related-product-identity.py
This checks generated HTML, not feed-additive authorisation or SDS accuracy.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "en": "Manganese(II) oxide",
    "hu": "Mangán(II)-oxid",
    "de-at": "Mangan(II)-oxid",
}

class RelatedLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.target = None
        self.in_span = False
        self.labels = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "related-product" in a.get("class", "").split():
            self.target = a.get("href", "").split("?", 1)[0].split("#", 1)[0]
        elif tag == "span" and self.target:
            self.in_span = True
            self.parts = []

    def handle_data(self, data):
        if self.in_span:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "span" and self.in_span:
            self.labels.append((self.target, "".join(self.parts).strip()))
            self.in_span = False
        elif tag == "a":
            self.target = None
            self.in_span = False

def main():
    catalogue = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    mno = next((item for item in catalogue if item.get("id") == "mangan-oxid-feed"), None)
    if mno is None:
        print("ERROR: MnO record missing from catalogue")
        return 1
    if mno.get("technical_identity", {}).get("formula") != "MnO":
        print("ERROR: MnO formula mismatch in catalogue")
        return 1
    failures = []
    checked = 0
    related_links = 0
    pages = 0
    for lang, name in EXPECTED.items():
        if mno.get("name_" + ("de" if lang == "de-at" else lang)) != name:
            failures.append(f"Catalogue name mismatch for {lang}")
        for page in ROOT.glob(f"{lang}-*.html"):
            pages += 1
            parser = RelatedLinkParser()
            parser.feed(page.read_text(encoding="utf-8"))
            for href, label in parser.labels:
                related_links += 1
                if not href.startswith(f"{lang}-") or not href.endswith(".html"):
                    failures.append(f"{page.name}: related link crosses language or is not a local HTML product: {href!r}")
                elif not (ROOT / href).is_file():
                    failures.append(f"{page.name}: related product target missing: {href!r}")
                if not label:
                    failures.append(f"{page.name}: empty related-product label for {href!r}")
                if href == f"{lang}-mangan-oxid-feed.html":
                    checked += 1
                    if name.casefold() not in label.casefold():
                        failures.append(f"{page.name}: MnO link labelled {label!r}; expected {name!r}")
    if pages == 0:
        failures.append("No localized HTML files found")
    if checked == 0:
        failures.append("No MnO related-product links found; check generator output and link parsing")
    print(f"Related-product integrity: {related_links} links across {pages} localized HTML files; MnO identity: {checked} links")
    for failure in failures:
        print("ERROR:", failure)
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
