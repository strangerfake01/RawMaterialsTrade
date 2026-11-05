#!/usr/bin/env python3
"""Build a machine-readable source audit of the static Raw Materials Trade site.

This describes repository evidence only. It does not claim that product data,
supplier documents, certificates, or live HTTP responses were independently verified.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CAS_RE = re.compile(r"\bCAS\s*(?:No\.?|number)?\s*[:#]?\s*(\d{2,7}-\d{2}-\d)\b", re.I)
EC_RE = re.compile(r"\bEC\s*(?:No\.?|number)?\s*[:#]?\s*(\d{3}-\d{3}-\d)\b", re.I)
DOC_RE = re.compile(r"\b(SDS|TDS|CoA|certificate of analysis|safety data sheet|technical data sheet)\b", re.I)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.h1_parts = []
        self.h1_count = 0
        self.description = ""
        self.lang = ""
        self.canonical = ""
        self.hreflang = {}
        self.jsonld = []
        self._capture = None
        self._script_type = ""
        self._script_parts = []
        self._text_parts = []
        self._meta_robots = ""

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self._capture = "title"
        elif tag == "h1":
            self.h1_count += 1
            self._capture = "h1"
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.description = a.get("content", "")
            elif name == "robots":
                self._meta_robots = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonical = a.get("href", "")
            if "alternate" in rel and a.get("hreflang"):
                self.hreflang[a["hreflang"].lower()] = a.get("href", "")
        elif tag == "script":
            self._script_type = a.get("type", "").lower()
            if self._script_type == "application/ld+json":
                self._script_parts = []
                self._capture = "jsonld"
        elif tag not in ("br", "img", "input", "meta", "link", "hr", "source"):
            self._text_parts.append(" ")

    def handle_data(self, data):
        if self._capture == "title":
            self.title_parts.append(data)
        elif self._capture == "h1":
            self.h1_parts.append(data)
        elif self._capture == "jsonld":
            self._script_parts.append(data)
        self._text_parts.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title" and self._capture == "title":
            self._capture = None
        elif tag == "h1" and self._capture == "h1":
            self._capture = None
        elif tag == "script" and self._capture == "jsonld":
            raw = "".join(self._script_parts).strip()
            if raw:
                self.jsonld.append(raw)
            self._capture = None
            self._script_type = ""
            self._script_parts = []

    @property
    def text(self):
        return " ".join("".join(self._text_parts).split())

    @property
    def title(self):
        return " ".join("".join(self.title_parts).split())

    @property
    def h1(self):
        return " ".join("".join(self.h1_parts).split())


def category_for(path: Path) -> str:
    name = path.name.lower()
    if name in ("en.html", "hu.html", "de-at.html"):
        return "home"
    if name.startswith("privacy") or name.startswith("impressum") or name.startswith("legal"):
        return "legal"
    if "trust" in name or "vertrauenszentrum" in name or "bizalmi-kozpont" in name:
        return "ai-trust"
    if "qualif" in name or "minosites" in name:
        return "qualification"
    if name.endswith(("-industrial.html", "-food.html", "-feed.html", "-deicing.html")):
        return "product"
    if any(x in name for x in ("industrial-chemicals", "deicing-materials", "ipari-vegyipari", "teli-utszorasi", "industriechemikalien", "winterdienst")):
        return "category"
    return "other"


def read_sitemap(path: Path):
    root = ET.parse(path).getroot()
    entries = {}
    for url_node in root.iter():
        if local_name(url_node.tag) != "url":
            continue
        loc = ""
        alternates = {}
        lastmod = ""
        for child in url_node:
            kind = local_name(child.tag)
            if kind == "loc":
                loc = (child.text or "").strip()
            elif kind == "lastmod":
                lastmod = (child.text or "").strip()
            elif kind == "link" and child.attrib.get("hreflang"):
                alternates[child.attrib["hreflang"].lower()] = child.attrib.get("href", "")
        if loc:
            entries[loc] = {"lastmod": lastmod, "alternates": alternates}
    return entries


def inventory(output: Path):
    sitemap_path = ROOT / "sitemap.xml"
    sitemap = read_sitemap(sitemap_path)
    html_files = sorted(ROOT.glob("*.html"))
    duplicate_locs = len(sitemap) != sum(1 for node in ET.parse(sitemap_path).getroot().iter() if local_name(node.tag) == "url")
    if duplicate_locs:
        raise SystemExit("FAIL: duplicate or empty sitemap URL entries")

    records = []
    invalid_jsonld = []
    missing = Counter()
    for path in html_files:
        page = PageParser()
        page.feed(path.read_text(encoding="utf-8"))
        page.close()
        parsed_json = []
        for i, raw in enumerate(page.jsonld, 1):
            try:
                parsed_json.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                invalid_jsonld.append({"file": path.name, "block": i, "error": str(exc)})

        canonical = page.canonical.strip()
        sitemap_entry = sitemap.get(canonical, {})
        alternate = sitemap_entry.get("alternates", {})
        reciprocal = True
        for lang, href in alternate.items():
            if lang == "x-default":
                continue
            if href not in sitemap:
                reciprocal = False
                break
            peer_alternates = sitemap[href].get("alternates", {})
            if not any(v == canonical for k, v in peer_alternates.items() if k != "x-default"):
                reciprocal = False
                break

        cas = sorted(set(CAS_RE.findall(page.text)))
        ec = sorted(set(EC_RE.findall(page.text)))
        docs = sorted(set(DOC_RE.findall(page.text)), key=str.lower)
        schema_types = []
        for block in parsed_json:
            objects = block if isinstance(block, list) else [block]
            for obj in objects:
                if isinstance(obj, dict):
                    typ = obj.get("@type", [])
                    schema_types.extend(typ if isinstance(typ, list) else [typ])

        checks = {
            "title_status": "verified" if page.title else "missing",
            "description_status": "verified" if page.description else "missing",
            "h1_status": "verified" if page.h1_count == 1 and page.h1 else "needs-confirmation" if page.h1_count > 1 else "missing",
            "canonical_status": "verified" if canonical and canonical == sitemap.get(canonical, {}).get("canonical", canonical) else "missing",
            "sitemap_status": "verified" if canonical in sitemap else "missing",
            "hreflang_status": "verified" if alternate and "x-default" in alternate and reciprocal else "needs-confirmation" if alternate else "missing",
            "jsonld_status": "verified" if page.jsonld and len(parsed_json) == len(page.jsonld) else "missing" if not page.jsonld else "needs-confirmation",
            "cas_status": "needs-confirmation" if cas else "missing",
            "ec_status": "needs-confirmation" if ec else "missing",
            "sds_tds_coa_status": "needs-confirmation" if docs else "missing",
        }
        for key, value in checks.items():
            if value != "verified":
                missing[key] += 1

        records.append({
            "url": canonical,
            "file": path.name,
            "language": page.lang,
            "category": category_for(path),
            "h1": page.h1,
            "title": page.title,
            "description": page.description,
            "canonical": canonical,
            "sitemap_lastmod": sitemap_entry.get("lastmod", ""),
            "hreflang_count": len(alternate),
            "jsonld_types": "|".join(sorted(set(t for t in schema_types if t))),
            "cas": "|".join(cas),
            "ec": "|".join(ec),
            "documentation_mentions": "|".join(docs),
            "robots": page._meta_robots,
            **checks,
        })

    output.mkdir(parents=True, exist_ok=True)
    fields = list(records[0]) if records else []
    with (output / "site-inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    summary = {
        "scope": "repository source only; not a live-site verification",
        "html_pages": len(html_files),
        "sitemap_urls": len(sitemap),
        "duplicate_or_empty_sitemap_entries": False,
        "invalid_jsonld_blocks": invalid_jsonld,
        "non_verified_counts": dict(sorted(missing.items())),
        "status_legend": {
            "verified": "present and structurally verified in repository source",
            "supplier-provided": "reserved for explicitly identifiable supplier documents",
            "editorial": "editorial claim or explanation",
            "missing": "not found in inspected page source",
            "needs-confirmation": "present but source, accuracy, or applicability needs confirmation",
        },
    }
    (output / "site-inventory-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if invalid_jsonld:
        raise SystemExit(f"FAIL: {len(invalid_jsonld)} invalid JSON-LD block(s); see audit output")
    print(f"Inventory: {len(html_files)} HTML pages; {len(sitemap)} sitemap URLs")
    print(f"Non-verified fields: {dict(missing)}")
    print(f"Written: {output / 'site-inventory.csv'} and site-inventory-summary.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "audit-output")
    args = parser.parse_args()
    inventory(args.output if args.output.is_absolute() else ROOT / args.output)


if __name__ == "__main__":
    main()
