#!/usr/bin/env python3
"""Guard the buyer-facing, multilingual procurement journey on all home pages."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "index.html": ("en", ["Define the material", "Set purchasing conditions", "Check sourcing and documentation", "Agree the quotation", "Confirm and fulfil"], ["CAS", "MOQ", "SDS", "TDS", "CoA", "FCA", "DAP", "DDP"]),
    "hu.html": ("hu-HU", ["Az anyag meghatározása", "Beszerzési feltételek", "Beszállítói és dokumentációs ellenőrzés", "Írásos ajánlat", "Megrendelés és teljesítés"], ["CAS", "SDS", "TDS", "CoA", "FCA", "DAP", "DDP"]),
    "de-at.html": ("de-AT", ["Material definieren", "Einkaufsbedingungen festlegen", "Lieferant und Unterlagen prüfen", "Schriftliches Angebot abstimmen", "Auftrag und Abwicklung"], ["CAS", "SDS", "TDS", "CoA", "FCA", "DAP", "DDP"]),
}

class JourneyParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts = []
        self.headings = []
        self.in_h3 = False
        self.h3_parts = []
        self.section_count = 0
        self.contact_cta = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("id") == "procurement-journey":
            self.section_count += 1
            self.depth = 1
            return
        if self.depth:
            if tag not in ("br", "hr", "img", "input", "meta", "link", "source", "wbr", "area"):
                self.depth += 1
            if tag == "h3":
                self.in_h3 = True
                self.h3_parts = []
            if tag == "a" and attrs.get("href") == "#contact":
                self.contact_cta = True

    def handle_endtag(self, tag):
        if not self.depth:
            return
        if tag == "h3" and self.in_h3:
            self.headings.append(" ".join("".join(self.h3_parts).split()))
            self.in_h3 = False
        self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)
            if self.in_h3:
                self.h3_parts.append(data)

errors = []
for filename, (lang, headings, terms) in PAGES.items():
    html = (ROOT / filename).read_text(encoding="utf-8")
    if not re.search(r'<html\s+lang="' + re.escape(lang) + r'"', html):
        errors.append(f"{filename}: unexpected HTML language")
    parser = JourneyParser()
    parser.feed(html)
    # Capture complete section, independent of parser nesting state.
    section = re.search(r'<section\b[^>]*id="procurement-journey"[^>]*>(.*?)</section>', html, re.S)
    content = re.sub(r"<[^>]+>", " ", section.group(1)) if section else ""
    content = " ".join(content.split())
    if parser.section_count != 1:
        errors.append(f"{filename}: expected one procurement journey, found {parser.section_count}")
    if parser.headings != headings:
        errors.append(f"{filename}: missing, translated incorrectly or reordered journey steps: {parser.headings!r}")
    if not parser.contact_cta:
        errors.append(f"{filename}: missing contact CTA")
    for term in terms:
        if term not in content:
            errors.append(f"{filename}: missing purchasing term {term}")
    if not any(term in content.casefold() for term in ("regular", "rendszeres", "regelmäßig")):
        errors.append(f"{filename}: recurring supply is not explained")
    print(f"{filename}: {len(parser.headings)} steps, contact CTA={parser.contact_cta}, procurement terms checked")

for error in errors:
    print("ERROR:", error)
raise SystemExit(bool(errors))
