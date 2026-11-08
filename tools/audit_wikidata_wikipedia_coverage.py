#!/usr/bin/env python3
"""Audit recorded Wikidata/Wikipedia candidates without implying external verification.

A product SKU/grade/mixture is not necessarily identical to a substance concept.
Missing localized URLs in this registry do not imply that Wikipedia articles do not exist.
"""
import json
import re
from collections import Counter
from pathlib import Path

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
            if not value.startswith("https://" + domain + "/wiki/"):
                errors.append(f"{pid}: unexpected {lang} Wikipedia URL")
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
shared_concepts = {qid: product_ids for qid, product_ids in qid_to_products.items()
                   if len(product_ids) > 1}
print("Unique Wikidata candidates:", len(qid_to_products))
print("Shared Wikidata concepts:", len(shared_concepts),
      "covering", sum(len(product_ids) for product_ids in shared_concepts.values()),
      "product families")
for qid, product_ids in sorted(shared_concepts.items()):
    print("REVIEW shared substance concept:", qid, "|", ", ".join(product_ids))
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
