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
import html as html_lib
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
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
        self.img_count = 0
        self.img_missing_alt = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        if tag == "img":
            self.img_count += 1
            if "alt" not in a:
                self.img_missing_alt += 1
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


def definition_values(source: str, label_pattern: str):
    values = []
    for label, value in re.findall(r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>", source, re.I | re.S):
        clean_label = html_lib.unescape(re.sub(r"<[^>]+>", " ", label))
        clean_value = html_lib.unescape(re.sub(r"<[^>]+>", " ", value)).strip()
        if re.search(label_pattern, clean_label, re.I) and clean_value:
            values.append(clean_value)
    return sorted(set(values))


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


def expected_language(path: Path) -> str:
    name = path.name.lower()
    if name.startswith("de-at-") or name in ("de-at.html", "privacy-de-at.html", "ai-profile-de-at.html"):
        return "de-at"
    if name.startswith("hu-") or name in ("hu.html", "privacy-hu.html", "ai-profile-hu.html"):
        return "hu-hu"
    return "en"


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
    catalogue_rows = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    catalogue = {item["id"]: item for item in catalogue_rows}
    html_files = sorted(ROOT.glob("*.html"))
    duplicate_locs = len(sitemap) != sum(1 for node in ET.parse(sitemap_path).getroot().iter() if local_name(node.tag) == "url")
    if duplicate_locs:
        raise SystemExit("FAIL: duplicate or empty sitemap URL entries")
    missing_targets = []
    for loc in sitemap:
        url_path = urlparse(loc).path
        if url_path in ("", "/"):
            target = ROOT / "index.html"
        elif url_path.endswith("/"):
            target = ROOT / url_path.strip("/") / "index.html"
        else:
            target = ROOT / url_path.lstrip("/")
        if not target.is_file():
            missing_targets.append(loc)
    if missing_targets:
        raise SystemExit(f"FAIL: sitemap URLs do not map to repository files: {missing_targets}")
    invalid_lastmods = [loc for loc, entry in sitemap.items() if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", entry["lastmod"])]
    if invalid_lastmods:
        raise SystemExit(f"FAIL: sitemap entries without ISO lastmod: {invalid_lastmods}")

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

        is_product = category_for(path) == "product"
        source_html = path.read_text(encoding="utf-8")
        data_language = "en" if path.name.startswith("en-") else "hu" if path.name.startswith("hu-") else "de"
        product_id = re.sub(r"^(?:en-|hu-|de-at-)", "", path.stem) if is_product else ""
        product_record = catalogue.get(product_id) if is_product else None
        identity = product_record.get("technical_identity", {}) if product_record else {}
        procurement = product_record.get("procurement", {}) if product_record else {}
        document_claims = product_record.get("documentation", {}) if product_record else {}
        cas = definition_values(source_html, r"\bCAS\b") if is_product else []
        ec = definition_values(source_html, r"\b(?:EC|EG|EINECS|EK)\b") if is_product else []
        docs = sorted(set(DOC_RE.findall(page.text)), key=str.lower) if is_product else []
        doc_file_links = re.findall(r"""href=["']([^"']+\.(?:pdf|docx|xlsx)(?:\?[^"']*)?)["']""", source_html, re.I)
        cas_catalogue_match = bool(identity.get("cas") and identity.get("cas") in cas)
        ec_catalogue_match = bool(identity.get("ec") and identity.get("ec") in ec)
        current_language = page.lang.lower()
        self_hreflang = alternate.get(current_language) == canonical
        schema_types = []
        for block in parsed_json:
            objects = block if isinstance(block, list) else [block]
            for obj in objects:
                if isinstance(obj, dict):
                    typ = obj.get("@type", [])
                    schema_types.extend(typ if isinstance(typ, list) else [typ])

        noindex = "noindex" in page._meta_robots.lower()
        date_modified_values = []
        def collect_date_modified(value):
            if isinstance(value, dict):
                if value.get("dateModified"):
                    date_modified_values.append(str(value["dateModified"]))
                for child in value.values():
                    collect_date_modified(child)
            elif isinstance(value, list):
                for child in value:
                    collect_date_modified(child)
        for block in parsed_json:
            collect_date_modified(block)
        sitemap_lastmod = sitemap_entry.get("lastmod", "")
        date_sync_status = "verified" if not sitemap_entry and noindex else "verified" if sitemap_lastmod and date_modified_values and all(x == sitemap_lastmod for x in date_modified_values) else "needs-confirmation" if sitemap_entry else "missing"

        source_url = "https://www.rawmaterialstrade.com/" if path.name == "index.html" else f"https://www.rawmaterialstrade.com/{path.name}"
        source_in_sitemap = source_url in sitemap
        excluded_by_policy = noindex and not source_in_sitemap
        checks = {
            "language_status": "verified" if page.lang.lower() == expected_language(path) else "needs-confirmation",
            "title_status": "verified" if page.title or noindex else "missing",
            "description_status": "verified" if page.description or noindex else "missing",
            "h1_status": "verified" if noindex or (page.h1_count == 1 and page.h1) else "needs-confirmation" if page.h1_count > 1 else "missing",
            "canonical_status": "verified" if canonical and (noindex or canonical == source_url) else "missing",
            "sitemap_status": "verified" if (source_in_sitemap and canonical in sitemap and not noindex) or excluded_by_policy else "needs-confirmation" if noindex and source_in_sitemap else "missing",
            "hreflang_status": "verified" if (noindex and not alternate and excluded_by_policy) or (alternate and "x-default" in alternate and self_hreflang and reciprocal) else "needs-confirmation" if alternate else "missing",
            "jsonld_status": "verified" if noindex or (page.jsonld and len(parsed_json) == len(page.jsonld)) else "missing" if not page.jsonld else "needs-confirmation",
            "date_sync_status": date_sync_status,
            "image_alt_status": "needs-confirmation" if page.img_missing_alt and not noindex else "verified",
            "cas_status": ("needs-confirmation" if cas else "missing") if is_product else "verified",
            "ec_status": ("needs-confirmation" if ec else "missing") if is_product else "verified",
            "cas_source_status": "needs-confirmation" if is_product and identity.get("cas") else "missing" if is_product else "verified",
            "ec_source_status": "needs-confirmation" if is_product and identity.get("ec") else "missing" if is_product else "verified",
            "identity_catalogue_match_status": "verified" if is_product and cas_catalogue_match and ec_catalogue_match else "needs-confirmation" if is_product and product_record else "missing" if is_product else "verified",
            "supplier_document_status": "needs-confirmation" if is_product and document_claims else "missing" if is_product else "verified",
            "sds_tds_coa_status": ("needs-confirmation" if docs else "missing") if is_product else "verified",
            "formula_status": "needs-confirmation" if is_product and identity.get("formula") else "missing" if is_product else "verified",
            "grade_status": "needs-confirmation" if is_product and identity.get(f"grade_{data_language}") else "missing" if is_product else "verified",
            "intended_use_status": "needs-confirmation" if is_product and product_record and product_record.get(f"applications_{data_language}") else "missing" if is_product else "verified",
            "packaging_status": "needs-confirmation" if is_product and procurement.get(f"packaging_{data_language}") else "missing" if is_product else "verified",
            "delivery_status": "needs-confirmation" if is_product and procurement.get(f"delivery_region_{data_language}") else "missing" if is_product else "verified",
            "moq_status": "needs-confirmation" if is_product and procurement.get("moq") else "missing" if is_product else "verified",
            "lead_time_status": "needs-confirmation" if is_product and procurement.get("lead_time") else "missing" if is_product else "verified",
        }
        for key, value in checks.items():
            if value != "verified":
                missing[key] += 1

        records.append({
            "url": canonical,
            "source_url": source_url,
            "file": path.name,
            "language": page.lang,
            "category": category_for(path),
            "h1": page.h1,
            "title": page.title,
            "description": page.description,
            "canonical": canonical,
            "sitemap_lastmod": sitemap_lastmod,
            "date_modified_values": "|".join(sorted(set(date_modified_values))),
            "hreflang_count": len(alternate),
            "jsonld_types": "|".join(sorted(set(t for t in schema_types if t))),
            "cas": "|".join(cas),
            "ec": "|".join(ec),
            "cas_catalogue": identity.get("cas", ""),
            "ec_catalogue": identity.get("ec", ""),
            "cas_catalogue_match": cas_catalogue_match if is_product else "",
            "ec_catalogue_match": ec_catalogue_match if is_product else "",
            "identity_source_status": "needs-confirmation" if is_product else "",
            "background_reference_urls": "|".join((product_record.get("wikipedia", {}) or {}).values()) if product_record else "",
            "product_name": product_record.get(f"name_{data_language}", "") if product_record else "",
            "product_formula": identity.get("formula", ""),
            "grade": identity.get(f"grade_{data_language}", identity.get("grade", "")) if product_record else "",
            "intended_use": " | ".join(product_record.get(f"applications_{data_language}", [])) if product_record and isinstance(product_record.get(f"applications_{data_language}", []), list) else (product_record.get(f"applications_{data_language}", "") if product_record else ""),
            "packaging": procurement.get(f"packaging_{data_language}", ""),
            "delivery_region": procurement.get(f"delivery_region_{data_language}", ""),
            "availability_note": procurement.get(f"availability_note_{data_language}", ""),
            "sds_claim": document_claims.get(f"sds_status_{data_language}", ""),
            "tds_claim": document_claims.get(f"tds_status_{data_language}", ""),
            "coa_claim": document_claims.get(f"coa_status_{data_language}", ""),
            "document_file_link_count": len(doc_file_links),
            "documentation_mentions": "|".join(docs),
            "image_count": page.img_count,
            "images_missing_alt": page.img_missing_alt,
            "robots": page._meta_robots,
            "indexing_policy": "noindex-excluded" if excluded_by_policy else "indexable" if not noindex else "noindex-in-sitemap-review",
            **checks,
        })

    output.mkdir(parents=True, exist_ok=True)
    fields = list(records[0]) if records else []
    with (output / "site-inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    review_keys = ("language_status", "title_status", "description_status", "h1_status", "canonical_status", "sitemap_status", "hreflang_status", "jsonld_status", "date_sync_status", "image_alt_status")
    review_pages = {
        key: [row["file"] for row in records if row[key] != "verified"]
        for key in review_keys
        if any(row[key] != "verified" for row in records)
    }
    summary = {
        "scope": "repository source only; not a live-site verification",
        "html_pages": len(html_files),
        "sitemap_urls": len(sitemap),
        "sitemap_targets_missing": len(missing_targets),
        "product_pages": sum(1 for path in html_files if category_for(path) == "product"),
        "product_pages_missing_cas": [row["file"] for row in records if row["category"] == "product" and row["cas_status"] == "missing"],
        "product_pages_missing_ec": [row["file"] for row in records if row["category"] == "product" and row["ec_status"] == "missing"],
        "product_pages_without_catalogue_entry": [row["file"] for row in records if row["category"] == "product" and row["identity_catalogue_match_status"] == "missing"],
        "product_pages_needing_authoritative_CAS_EC_sources": sum(1 for row in records if row["category"] == "product" and row["identity_source_status"] == "needs-confirmation"),
        "product_pages_needing_supplier_document_confirmation": sum(1 for row in records if row["category"] == "product" and row["supplier_document_status"] == "needs-confirmation"),
        "product_pages_without_attached_document_links": sum(1 for row in records if row["category"] == "product" and row["document_file_link_count"] == 0),
        "indexable_pages_with_date_sync_review": [row["file"] for row in records if row["indexing_policy"] == "indexable" and row["date_sync_status"] != "verified"],
        "pages_with_images_missing_alt": [row["file"] for row in records if row["images_missing_alt"] > 0],
        "intentionally_excluded_noindex_pages": sum(1 for row in records if row["indexing_policy"] == "noindex-excluded"),
        "duplicate_or_empty_sitemap_entries": False,
        "invalid_jsonld_blocks": invalid_jsonld,
        "non_verified_counts": dict(sorted(missing.items())),
        "review_pages": review_pages,
        "status_legend": {
            "verified": "present and structurally verified in repository source",
            "supplier-provided": "reserved for explicitly identifiable supplier documents",
            "editorial": "editorial claim or explanation",
            "missing": "not found in inspected page source",
            "needs-confirmation": "present but source, accuracy, or applicability needs confirmation; chemical identifiers need an authoritative source and supplier documents need exact-product confirmation",
            "non-product identity fields": "chemical identity and supplier-document status are not applicable outside product pages",
            "noindex-excluded": "page intentionally excluded from the sitemap by a noindex policy; index-only metadata checks do not apply",
        },
    }
    (output / "site-inventory-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if invalid_jsonld:
        raise SystemExit(f"FAIL: {len(invalid_jsonld)} invalid JSON-LD block(s); see audit output")
    print(f"Inventory: {len(html_files)} HTML pages; {len(sitemap)} sitemap URLs; {summary['product_pages']} product pages")
    print(f"Non-verified fields: {dict(missing)}")
    print(f"Language attribute review: {review_pages.get('language_status', [])}")
    print(f"Product pages missing CAS: {summary['product_pages_missing_cas']}")
    print(f"Product pages missing EC: {summary['product_pages_missing_ec']}")
    print(f"Intentionally excluded noindex pages: {summary['intentionally_excluded_noindex_pages']}")
    print(f"Pages with image alt review: {len(summary['pages_with_images_missing_alt'])}")
    print(f"Product records missing: {len(summary['product_pages_without_catalogue_entry'])}")
    print(f"Product pages needing authoritative identifier sources: {summary['product_pages_needing_authoritative_CAS_EC_sources']}")
    print(f"Product pages needing supplier document confirmation: {summary['product_pages_needing_supplier_document_confirmation']}")
    print(f"Product pages without attached document links: {summary['product_pages_without_attached_document_links']}")
    print(f"Indexable date sync review: {summary['indexable_pages_with_date_sync_review']}")
    for key, files in review_pages.items():
        print(f"Review {key}: {', '.join(files)}")
    print(f"Written: {output / 'site-inventory.csv'} and site-inventory-summary.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "audit-output")
    args = parser.parse_args()
    inventory(args.output if args.output.is_absolute() else ROOT / args.output)


if __name__ == "__main__":
    main()
