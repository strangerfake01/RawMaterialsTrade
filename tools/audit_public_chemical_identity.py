#!/usr/bin/env python3
"""Fail if unreviewed product chemical identities leak into public JSON-LD.

Checks all three catalogue language variants, not merely one sample page.
Does not claim scientific validation of CAS, EC, formula or supplier documents.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
REGISTRY = {e["id"]: e for e in json.loads((ROOT / "entity-registry.json").read_text(encoding="utf-8"))["entities"]}
LANGUAGES = ("en", "hu", "de-at")
LD = re.compile(r'<script\b[^>]*type=["\x27]application/ld\+json["\x27][^>]*>(.*?)</script>', re.I | re.S)
errors = []
checked = 0

def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)

for product in PRODUCTS:
    pid = product["id"]
    registry = REGISTRY.get(pid)
    if registry is None:
        errors.append(f"{pid}: missing entity-registry entry")
        continue
    if registry.get("sameAs_status") == "verified":
        evidence = registry.get("identity_verification_evidence") or {}
        required = ("primary_source_url", "supplier_document_reference", "verified_cas", "verified_material_form", "reviewed_by", "reviewed_on")
        missing = [field for field in required if not isinstance(evidence.get(field), str) or not evidence[field].strip()]
        if missing:
            errors.append(f"{pid}: verified identity lacks human/primary/supplier provenance: {', '.join(missing)}")
        if evidence.get("verified_cas") != registry.get("cas"):
            errors.append(f"{pid}: verified identity CAS does not match registry")
        if evidence.get("primary_source_url") and not str(evidence["primary_source_url"]).startswith("https://"):
            errors.append(f"{pid}: primary source must be an HTTPS reference")
    for lang in LANGUAGES:
        path = ROOT / f"{lang}-{pid}.html"
        if not path.is_file():
            errors.append(f"{path.name}: missing catalogue page")
            continue
        html = path.read_text(encoding="utf-8")
        scripts = LD.findall(html)
        if not scripts:
            errors.append(f"{path.name}: missing JSON-LD")
        checked += 1
        for idx, raw in enumerate(scripts):
            try:
                graph = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}: invalid JSON-LD script {idx}: {exc}")
                continue
            for node in walk(graph):
                types = node.get("@type", [])
                if isinstance(types, str):
                    types = [types]
                if "ChemicalSubstance" not in types:
                    continue
                if registry.get("sameAs_status") != "verified" and node.get("sameAs"):
                    errors.append(f"{path.name}: unverified ChemicalSubstance sameAs")
                if node.get("identifier") and registry.get("sameAs_status") != "verified":
                    # The identifier may be legitimate catalogue text, but cannot be
                    # accepted as independently verified without source review.
                    identifiers = node["identifier"]
                    if isinstance(identifiers, dict):
                        identifiers = [identifiers]
                    for ident in identifiers if isinstance(identifiers, list) else []:
                        if isinstance(ident, dict) and ident.get("verificationStatus") == "verified":
                            errors.append(f"{path.name}: unverified identifier marked verified")
assert len(PRODUCTS) == 126, "Unexpected product catalogue size"
if checked != 378:
    errors.append(f"Expected 378 language pages, checked {checked}")
print(f"Product JSON-LD identity disclosure: {checked} pages, {len(errors)} errors")
for error in errors[:60]:
    print("ERROR:", error)
raise SystemExit(bool(errors))
