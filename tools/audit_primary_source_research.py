#!/usr/bin/env python3
"""Fail closed on incorrect legacy PubChem candidates and inflated source evidence.

A documented general-substance PubChem match is not an approval of an RMT
supplier product, offered grade, batch or regulated application. Never promote
these scoped reference records to commercial ChemicalSubstance sameAs.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "entity-registry.json").read_text(encoding="utf-8"))
CATALOGUE = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
RESEARCH = json.loads((ROOT / "docs/primary-substance-research-2026-11-23.json").read_text(encoding="utf-8"))
with (ROOT / "HANDOFF/SOURCE-REGISTER.csv").open(encoding="utf-8", newline="") as f:
    ROWS = list(csv.DictReader(f))

EXPECTED = {
    "aszkorbinsav-food": (190531, 54670067, "50-81-7", "C6H8O6"),
    "ammonium-szulfat-industrial": (783, 6097028, "7783-20-2", "H8N2O4S"),
    "ammonium-klorid-industrial": (25423, 25517, "12125-02-9", "ClH4N"),
    "borax-dekahidrat-industrial": (159383, 16211214, "1303-96-4", "B4H20Na2O17"),
    "borax-pentahidrat-industrial": (57347062, 86341921, "12179-04-3", "B4H10Na2O12"),
    "ammonia-oldat-24-industrial": (222, 14923, "1336-21-6", "H5NO"),
    "copper-oxide-feed": (164827, 164827, "1317-38-0", "CuO"),
    "glicerin-99-5-food": (753, 753, "56-81-5", "C3H8O3"),
    "natrium-hidroxid-mikrogyongy-pikkelyes-industrial": (7303, 14798, "1310-73-2", "HNaO"),
    "natrium-hidroxid-oldat-4850-industrial": (7303, 14798, "1310-73-2", "HNaO"),
    "natrium-hidrogen-karbonat-industrial": (767, 516892, "144-55-8", "CHNaO3"),
    "natrium-hidrogen-karbonat-szodabikarbona-food": (767, 516892, "144-55-8", "CHNaO3"),
    "magnezium-szulfat-industrial": (1639, 24083, "7487-88-9", "MgO4S"),
}
errors: list[str] = []
if len(CATALOGUE) != 127 or len(REGISTRY.get("entities", [])) != 127:
    errors.append("Unexpected catalogue/registry size")
entries = {x["id"]: x for x in REGISTRY["entities"]}
evidence = {x["id"]: x for x in RESEARCH["entries"]}
if set(evidence) != set(EXPECTED):
    errors.append("General-source references have unreviewed or missing entries")
if RESEARCH.get("commercial_grade_verified") != 0:
    errors.append("Supplier grade was incorrectly approved by general references")
if RESEARCH.get("other_catalogue_families_not_yet_independently_verified") != 114:
    errors.append("Full catalogue research coverage misrepresented")
for pid, (rejected, cid, cas, formula) in EXPECTED.items():
    item = entries.get(pid, {})
    cited = evidence.get(pid, {})
    if (item.get("cas"), item.get("pubchem_candidate_cid"),
            item.get("pubchem_candidate_formula")) != (cas, cid, formula):
        errors.append(f"{pid}: wrong candidate CAS/CID/formula association")
    if cited.get("pubchem") != f"https://pubchem.ncbi.nlm.nih.gov/compound/{cas}":
        errors.append(f"{pid}: missing independently checked PubChem CAS URL")
    if (cited.get("cid"), cited.get("cas"), cited.get("formula")) != (cid, cas, formula):
        errors.append(f"{pid}: research evidence inconsistent with source record")
    scope = item.get("independent_general_substance_reference") or {}
    if scope.get("scope") != "general_substance_only_not_offered_grade":
        errors.append(f"{pid}: source has commercial-grade inflation")
    if scope.get("supplier_evidence_status") != "unverified":
        errors.append(f"{pid}: supplier incorrectly treated as verified")
    if item.get("sameAs_status") == "verified" or item.get("pubchem_cid") is not None:
        errors.append(f"{pid}: general reference promoted to approved material")
    if rejected != cid and item.get("pubchem_candidate_cid") == rejected:
        errors.append(f"{pid}: rejected legacy PubChem CID restored")
    pubchem = [r for r in ROWS if r["product_id"] == pid and r["source_type"] == "PubChem"]
    if len(pubchem) != 1:
        errors.append(f"{pid}: source register must have one PubChem reference")
    else:
        row = pubchem[0]
        if (row["source_url"] != f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}" or
                row["evidence_status"] != "needs-independent-verification"):
            errors.append(f"{pid}: source register is missing correct scoped reference")
for row in ROWS:
    if row["source_type"] == "Wikidata" and row["evidence_status"] == "verified":
        errors.append(f"{row['product_id']}: unchecked Wikidata matches labelled verified")
for pid in ("borax-dekahidrat-industrial", "borax-pentahidrat-industrial"):
    e = entries.get(pid, {})
    if e.get("wikidata_qid") or e.get("wikidata_label"):
        errors.append(f"{pid}: unapproved or mismatched hydrate Wikidata sameAs")
if len(ROWS) != 369:
    errors.append(f"Source register unexpected row count: {len(ROWS)}")
print(f"Primary substance research: {len(EXPECTED)} general concepts crosschecked, "
      f"{len(CATALOGUE)-len(EXPECTED)} unreviewed; "
      f"0 supplier grades approved; {len(errors)} source errors")
for error in errors[:35]:
    print("ERROR:", error)
raise SystemExit(bool(errors))
