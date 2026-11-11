#!/usr/bin/env python3
"""Audit recorded Wikidata/Wikipedia candidates without implying external verification.

A product SKU/grade/mixture is not necessarily identical to a substance concept.
Missing localized URLs in this registry do not imply that Wikipedia articles do not exist.
"""
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
entities = json.loads((ROOT / "entity-registry.json").read_text(encoding="utf-8"))["entities"]
ids = [p["id"] for p in products]
registered = [e["id"] for e in entities]
assert len(ids) == len(set(ids)) == 126, "Expected 126 unique products"
assert len(registered) == len(set(registered)) == 126, "Expected 126 unique registry entries"
assert set(ids) == set(registered), "Product and entity registry IDs differ"
qid_pattern = re.compile(r"Q[1-9][0-9]*\Z")
language_domains = {"en": "en.wikipedia.org", "hu": "hu.wikipedia.org", "de": "de.wikipedia.org"}
errors = []
counts = Counter()
missing = []
for e in entities:
    pid = e["id"]
    qid = e.get("wikidata_qid")
    if qid:
        counts["wikidata_candidate"] += 1
        if not qid_pattern.fullmatch(qid):
            errors.append(f"{pid}: invalid Wikidata QID syntax")
    else:
        missing.append(pid)
    for lang, domain in language_domains.items():
        value = e.get("wikipedia_" + lang)
        if value:
            counts["wikipedia_" + lang + "_recorded"] += 1
            parsed = urlsplit(value)
            if (parsed.scheme != "https" or parsed.netloc != domain
                    or not parsed.path.startswith("/wiki/")
                    or not unquote(parsed.path[len("/wiki/"):]).strip()
                    or parsed.query or parsed.fragment or parsed.username or parsed.password):
                errors.append(f"{pid}: malformed or noncanonical {lang} Wikipedia article URL")
    # Automated PubChem CID/formula candidates are not verified product identities.
    # Never allow them to become approved registry data without provenance.
    if e.get("pubchem_status") != "verified":
        if e.get("pubchem_cid") is not None or e.get("pubchem_formula") is not None:
            errors.append(f"{pid}: unverified PubChem candidate promoted to approved field")
    else:
        evidence = e.get("pubchem_verification_evidence") or {}
        required_pubchem = ("primary_source_url", "verified_cas",
                            "verified_material_form", "reviewed_by", "reviewed_on")
        if any(not str(evidence.get(k) or "").strip() for k in required_pubchem):
            errors.append(f"{pid}: verified PubChem identity lacks provenance")
    if e.get("sameAs_status") == "verified":
        counts["identity_approved"] += 1
        evidence = e.get("identity_verification_evidence") or {}
        required = ("primary_source_url", "supplier_document_reference", "verified_cas",
                    "verified_material_form", "reviewed_by", "reviewed_on")
        if any(not str(evidence.get(k) or "").strip() for k in required):
            errors.append(f"{pid}: identity approval lacks provenance")
# Shared substance concepts are candidates, not evidence that distinct commercial grades are identical.
qid_to_products = {}
for entity in entities:
    qid = entity.get("wikidata_qid")
    if qid:
        qid_to_products.setdefault(qid, []).append(entity["id"])
# Registry integrity: one candidate QID must not point to contradictory EN articles.
qid_to_english_urls = {}
for entity in entities:
    qid = entity.get("wikidata_qid")
    english_url = entity.get("wikipedia_en")
    if bool(qid) != bool(english_url):
        errors.append(f"{entity['id']}: Wikidata and EN Wikipedia candidate presence differs")
    if qid and english_url:
        qid_to_english_urls.setdefault(qid, set()).add(english_url)
for qid, urls in qid_to_english_urls.items():
    if len(urls) != 1:
        errors.append(f"{qid}: conflicting EN Wikipedia URLs for shared Wikidata concept")
shared_concepts = {qid: product_ids for qid, product_ids in qid_to_products.items()
                   if len(product_ids) > 1}
print("Unique Wikidata candidates:", len(qid_to_products))
print("Shared Wikidata concepts:", len(shared_concepts),
      "covering", sum(len(product_ids) for product_ids in shared_concepts.values()),
      "product families")
for qid, product_ids in sorted(shared_concepts.items()):
    print("REVIEW shared substance concept:", qid, "|", ", ".join(product_ids))
# Candidate coverage is report-only: do not infer chemical correctness from populated fields.
candidate_cids = {}
for entity in entities:
    cid = entity.get("pubchem_candidate_cid")
    formula = entity.get("pubchem_candidate_formula")
    if cid is not None:
        if type(cid) is not int or cid <= 0:
            errors.append(f"{entity['id']}: invalid PubChem candidate CID")
        else:
            candidate_cids.setdefault(cid, []).append(entity["id"])
    if formula is not None and (not isinstance(formula, str) or not formula.strip()):
        errors.append(f"{entity['id']}: invalid PubChem candidate formula")
print("PubChem candidate CIDs:", sum(bool(e.get("pubchem_candidate_cid")) for e in entities))
print("Unique PubChem candidate CIDs:", len(candidate_cids))
print("PubChem candidate formulas:", sum(bool(e.get("pubchem_candidate_formula")) for e in entities))
print("NOTE: candidate CID/formula presence is not independent identity verification.")
print("Entity registry coverage:", len(entities), "families")
print("Wikidata candidates:", counts["wikidata_candidate"])
for lang in language_domains:
    print(f"Wikipedia {lang} URLs recorded:", counts["wikipedia_" + lang + "_recorded"])
print("Identity-approved relationships:", counts["identity_approved"])
print("No QID candidate:", ", ".join(missing) if missing else "none")
print("NOTE: recorded URL coverage is not Wikipedia language availability or live link verification.")
print("NOTE: unapproved candidates must not become public ChemicalSubstance sameAs.")
for err in errors:
    print("ERROR:", err)
raise SystemExit(bool(errors))
