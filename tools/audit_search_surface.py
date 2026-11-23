#!/usr/bin/env python3
"""Verify machine and human search metadata across every indexed sitemap route.

Read-only. Audit-only; never mutate product identity, supplier data or security.
"""
from __future__ import annotations
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "x": "http://www.w3.org/1999/xhtml"}


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.in_title = False
        self.title = []
        self.meta = defaultdict(list)
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.html_lang = attrs.get("lang") or ""
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.meta[key.casefold()].append(attrs.get("content") or "")
        elif tag == "link":
            self.links.append(attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def main():
    root = ET.parse(ROOT / "sitemap.xml").getroot()
    errors = []
    notes = []
    seen = 0
    titles = defaultdict(list)
    descriptions = defaultdict(list)
    for entry in root.findall("s:url", NS):
        loc = entry.findtext("s:loc", default="", namespaces=NS)
        url = urlparse(loc)
        if url.netloc != "www.rawmaterialstrade.com":
            errors.append((loc, "unexpected host"))
            continue
        rel = unquote(url.path).lstrip("/") or "index.html"
        path = ROOT / rel
        if not path.is_file():
            errors.append((rel, "missing indexed HTML"))
            continue
        parser = Metadata()
        parser.feed(path.read_text(encoding="utf-8"))
        seen += 1
        title = " ".join("".join(parser.title).split())
        descs = parser.meta.get("description", [])
        if len(title) < 12:
            errors.append((rel, "missing/too short HTML title"))
        else:
            titles[title.casefold()].append(rel)
        if len(descs) != 1 or not descs[0].strip():
            errors.append((rel, "missing or duplicated meta description"))
        else:
            descriptions[descs[0].strip().casefold()].append(rel)
            if len(descs[0].strip()) < 65:
                notes.append((rel, "short meta description"))
        expected_lang = ("hu" if rel.startswith("hu-") or rel == "hu.html" else
                         "de" if rel.startswith("de-at-") or rel == "de-at.html" else "en")
        if not parser.html_lang.lower().startswith(expected_lang):
            errors.append((rel, "HTML lang incorrect or missing: " + parser.html_lang))
        if "viewport" not in parser.meta:
            errors.append((rel, "missing responsive viewport"))
        if "noindex" in ",".join(parser.meta.get("robots", [])).lower():
            errors.append((rel, "sitemap entry marked noindex"))
        exp_alts = {a.attrib.get("hreflang"): a.attrib.get("href")
                    for a in entry.findall("x:link", NS)}
        actual_alts = {}
        for link in parser.links:
            if "alternate" in link.get("rel", "").lower().split() and link.get("hreflang"):
                key = link["hreflang"]
                if key in actual_alts:
                    errors.append((rel, "duplicate HTML hreflang: " + key))
                actual_alts[key] = link.get("href")
        if actual_alts != exp_alts:
            errors.append((rel, "HTML/sitemap hreflang differs: " + str(sorted(actual_alts))))
        og = parser.meta.get("og:url", [])
        if len(og) != 1 or og[0] != loc:
            notes.append((rel, "missing or mismatched og:url"))
    for title, routes in titles.items():
        if len(routes) > 1:
            notes.append((", ".join(routes[:3]), f"duplicate title ({len(routes)} pages)"))
    for description, routes in descriptions.items():
        if len(routes) > 1:
            notes.append((", ".join(routes[:3]), f"duplicate description ({len(routes)} pages)"))
    print(f"SEO/AEO metadata: {seen} sitemap routes, {len(errors)} blocking errors, {len(notes)} enhancement candidates")
    print("BLOCKING:", json.dumps(errors[:100], ensure_ascii=False))
    print("REVIEW:", json.dumps(notes[:60], ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
