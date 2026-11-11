#!/usr/bin/env python3
"""Reproducible source-state inventory, not fabricated product-quality scores.

The report describes visible page content and available first-party evidence.
It does not certify CAS, formula, EC, supplier documentation, or compliance.
"""
import argparse
import csv
import io
import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "HANDOFF" / "PRODUCT-DEPTH-SCORES-v4.csv"
LANGS = ("en", "hu", "de-at")
SECTION_RE = re.compile(r'<section\b[^>]*class=["\x27][^"\x27]*\b%s\b[^"\x27]*["\x27][^>]*>(.*?)</section>', re.I | re.S)
TAG_RE = re.compile(r"<[^>]*>")
TEXT_RE = lambda v: unescape(TAG_RE.sub(" ", v)).replace("\xa0", " ").strip()
FIELDS = (
    "product_id", "language_pages", "identity_cas_present", "ec_identification_present",
    "formula_orientation_present", "visible_product_checkpoints", "visible_buyer_supplier_path",
    "visible_document_status", "visible_rfq_checklist", "specific_faq_questions_en",
    "sameas_review_status", "pubchem_review_status", "supplier_sds_link_present",
    "supplier_tds_link_present", "supplier_coa_link_present",
    "technical_specs_independently_verified", "commercial_terms_supplier_confirmed",
    "external_evidence_review", "editorial_review_priority"
)

def match_section(html, klass):
    match = re.search(SECTION_RE.pattern % re.escape(klass), html, re.I | re.S)
    return match.group(1) if match else ""

def visible_cas(html, expected):
    chunk = re.search(r'<section\b[^>]*class=["\x27][^"\x27]*\bproduct-checkpoints\b.*?</section>', html, re.S | re.I)
    return bool(expected and chunk and expected in TEXT_RE(chunk.group(0)))

def supplier_doc(html, needle):
    """Link to an identifiable actual document; not merely an SDS/TDS/CoA mention."""
    links = re.findall(r'<a\b[^>]*href=["\x27]([^"\x27]+)["\x27][^>]*>(.*?)</a>', html, re.I | re.S)
    return any(needle in (href + " " + TEXT_RE(label)).lower() and
               re.search(r'\.(pdf|docx?|xlsx?)(?:\?|$)', href, re.I)
               for href, label in links)

def build():
    registry = json.loads((ROOT / "entity-registry.json").read_text(encoding="utf-8"))
    registered = {e["id"]: e for e in registry["entities"]}
    products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    rows = []
    for product in sorted(products, key=lambda x: x["id"]):
        ident = product["id"]
        e = registered.get(ident) or {
            "id": ident,
            "cas": product.get("technical_identity", {}).get("cas"),
            "sameAs_status": "missing_registry_entry",
            "pubchem_status": "missing_registry_entry",
        }
        pages = {l: ROOT / (l+"-"+ident+".html") for l in LANGS}
        htmls = {l: p.read_text(encoding="utf-8") if p.exists() else "" for l, p in pages.items()}
        en = htmls["en"]
        counts = {l: bool(htmls[l]) for l in LANGS}
        doc_status = {l: bool(match_section(htmls[l], "product-doc-status")) for l in LANGS}
        rfq = {l: bool(match_section(htmls[l], "product-rfq-checklist")) for l in LANGS}
        checkpoints = {l: bool(match_section(htmls[l], "product-checkpoints")) for l in LANGS}
        dual = {l: bool(match_section(htmls[l], "product-dual-path")) for l in LANGS}
        details = match_section(en, "product-faq")
        questions = [TEXT_RE(x) for x in re.findall(r"<summary\b[^>]*>(.*?)</summary>", details, re.I | re.S)]
        has_ec = bool(re.search(r'\bEC\s*\d{3}-\d{3}-\d\b', TEXT_RE(match_section(en, "product-checkpoints"))))
        has_formula = bool(re.search(r'Formula orientation:|chemicalComposition', en, re.I))
        cas = e.get("cas")
        complete = all(counts.values())
        sameas = e.get("sameAs_status", "unknown")
        if sameas == "verified":
            sameas = "registry_verified_label_external_review_required"
        pubchem = e.get("pubchem_status", "unknown")
        actual_documents = [supplier_doc(en, x) for x in ("sds", "tds", "coa")]
        # No supplier file accessible in this repository was independently authenticated.
        external = "not_independently_verified"
        # Prioritize actual missing on-page elements before any unsupported numeric rating.
        missing = sum(not all(v.values()) for v in (counts, doc_status, rfq, checkpoints, dual))
        missing += int(not questions or len(questions) < 2)
        missing += int(not visible_cas(en, cas))
        rows.append({
            "product_id":ident,
            "language_pages":"/".join("present" if counts[l] else "missing" for l in LANGS),
            "identity_cas_present":"yes" if visible_cas(en,cas) else "no",
            "ec_identification_present":"yes" if has_ec else "no",
            "formula_orientation_present":"yes" if has_formula else "no",
            "visible_product_checkpoints":"all_languages" if all(checkpoints.values()) else "missing_some",
            "visible_buyer_supplier_path":"all_languages" if all(dual.values()) else "missing_some",
            "visible_document_status":"all_languages" if all(doc_status.values()) else "missing_some",
            "visible_rfq_checklist":"all_languages" if all(rfq.values()) else "missing_some",
            "specific_faq_questions_en":str(len(questions)),
            "sameas_review_status":sameas,
            "pubchem_review_status":pubchem,
            "supplier_sds_link_present":"yes" if actual_documents[0] else "no",
            "supplier_tds_link_present":"yes" if actual_documents[1] else "no",
            "supplier_coa_link_present":"yes" if actual_documents[2] else "no",
            "technical_specs_independently_verified":"not_verified_in_this_audit",
            "commercial_terms_supplier_confirmed":"not_verified_in_this_audit",
            "external_evidence_review":external,
            "editorial_review_priority":"P1_structural_gap" if missing else "P1_external_evidence_required"
        })
    out=io.StringIO(newline="")
    w=csv.DictWriter(out,fieldnames=FIELDS,lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    assert len(rows)==126, "Expected 126 family identities, found %d" % len(rows)
    return out.getvalue(),rows

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    content,rows=build()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8")!=content:
            print("Product evidence report is stale; run: python3 tools/audit_product_evidence_depth.py")
            sys.exit(1)
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(content,encoding="utf-8")
    print("Evidence matrix:",len(rows),"families; all verification labels explicitly unverified unless first-party evidence is present")
    print("Structural gaps:",sum(x["editorial_review_priority"]=="P1_structural_gap" for x in rows))
