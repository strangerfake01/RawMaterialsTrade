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
# Second independently cross-checked PubChem CAS/name/formula batch, no seller approval.
EXPECTED.update({
    "aceton-technikai-regeneralt-industrial": (180, 180, "67-64-1", "C3H6O"),
    "etkezesi-so-food": (5234, 5234, "7647-14-5", "ClNa"),
    "sotabletta-industrial": (5234, 5234, "7647-14-5", "ClNa"),
    "utszoro-so-deicing": (5234, 5234, "7647-14-5", "ClNa"),
    "vakuum-so-industrial": (5234, 5234, "7647-14-5", "ClNa"),
    "metanol-technikai-regeneralt-industrial": (887, 887, "67-56-1", "CH4O"),
    "monoetilen-glikol-industrial": (174, 174, "107-21-1", "C2H6O2"),
    "monopropilenglikol-industrial": (1030, 1030, "57-55-6", "C3H8O2"),
    "izopropil-alkohol-technikai-regeneralt-industrial": (3776, 3776, "67-63-0", "C3H8O"),
    "hidrogen-peroxid-35-50-60-industrial": (784, 784, "7722-84-1", "H2O2"),
    "kensav-32-37-50-9597-industrial": (1118, 1118, "7664-93-9", "H2O4S"),
    "monoetanolamin-industrial": (700, 700, "141-43-5", "C2H7NO"),
    "glicin-industrial": (750, 750, "56-40-6", "C2H5NO2"),
    "butil-glikol-industrial": (8133, 8133, "111-76-2", "C6H14O2"),
    "ecetsavanhidrid-industrial": (7918, 7918, "108-24-7", "C4H6O3"),
    "ciklohexanon-industrial": (7966, 7967, "108-94-1", "C6H10O"),
    "karbamid-ipari-kezeletlen-industrial": (1176, 1176, "57-13-6", "CH4N2O"),
    "kalium-hidroxid-oldat-21-45-4850-industrial": (14797, 14797, "1310-58-3", "HKO"),
    "kalium-hidroxid-pikkelyes-industrial": (14797, 14797, "1310-58-3", "HKO"),
    "magnezium-oxid-feed": (14792, 14792, "1309-48-4", "MgO"),
    "magnezium-oxid-nehez-industrial": (14792, 14792, "1309-48-4", "MgO"),
    "cink-oxid-industrial": (14806, 14806, "1314-13-2", "OZn"),
    "cink-klorid-feed": (5727, 5727, "7646-85-7", "Cl2Zn"),
    "cink-klorid-vizmentes-industrial": (5727, 5727, "7646-85-7", "Cl2Zn"),
    "borsav-industrial": (7628, 7628, "10043-35-3", "BH3O3"),
    "ioncserelt-viz-industrial": (962, 962, "7732-18-5", "H2O"),
    "maleinsav-industrial": (723, 444266, "110-16-7", "C4H4O4"),
})

# Third independently cross-checked general CAS/name/formula batch; no seller approval.
EXPECTED.update({
    "aluminium-szulfat-03-mm-38-mm-industrial": (24850, 24850, "10043-01-3", "Al2O12S3"),
    "aluminium-szulfat-oldat-industrial": (24850, 24850, "10043-01-3", "Al2O12S3"),
    "ammonium-nitrat-industrial": (22985, 22985, "6484-52-2", "H4N2O3"),
    "borken-food": (28019, 28019, "16731-55-8", "K2O5S2"),
    "butil-diglikol-industrial": (8177, 8177, "112-34-5", "C8H18O3"),
    "dietilen-glikol-industrial": (8117, 8117, "111-46-6", "C4H10O3"),
    "natrium-karbonat-konnyu-industrial": (10340, 10340, "497-19-8", "CNa2O3"),
    "natrium-karbonat-nehez-industrial": (10340, 10340, "497-19-8", "CNa2O3"),
    "foszforsav-75-85-food": (1004, 1004, "7664-38-2", "H3O4P"),
    "foszforsav-75-industrial": (1004, 1004, "7664-38-2", "H3O4P"),
    "kalcium-karbonat-food": (10112, 10112, "471-34-1", "CCaO3"),
    "kalium-karbonat-industrial": (11430, 11430, "584-08-7", "CK2O3"),
    "etil-acetat-technikai-regeneralt-industrial": (8857, 8857, "141-78-6", "C4H8O2"),
    "natrium-szulfat-industrial": (24436, 24436, "7757-82-6", "Na2O4S"),
    "kalium-jodid-feed": (4875, 4875, "7681-11-0", "IK"),
    "propionsav-99-feed": (1032, 1032, "79-09-4", "C3H6O2"),
    "butanol-industrial": (263, 263, "71-36-3", "C4H10O"),
})

# Fourth source review: acid/anion and potassium-stoichiometry errors.
EXPECTED.update({
    "ecetsav-20-50-60-70-80-99-8-industrial": (175, 176, "64-19-7", "C2H4O2"),
    "ecetsav-20-50-60-70-80-99-8-jegecet-food": (175, 176, "64-19-7", "C2H4O2"),
    "hangyasav-85-industrial": (283, 284, "64-18-6", "CH2O2"),
    "kalium-ferrocianid-food": (26250, 9605257, "13943-58-3", "C6FeK4N6"),
})
VARIANT_SOURCES = json.loads((ROOT / "docs/variant-form-primary-sources-2026-11-23.json").read_text(encoding="utf-8"))

# Fifth source review: salt versus isolated anion and acid versus anion.
EXPECTED.update({
    "natrium-benzoat-gran-food": (242, 517055, "532-32-1", "C7H5NaO2"),
    "saletromsav-20-50-53-60-industrial": (943, 944, "7697-37-2", "HNO3"),
    "sosav-gyogyszerkonyvi-food": (312, 313, "7647-01-0", "ClH"),
    "sosav-technikai-regeneralt-industrial": (312, 313, "7647-01-0", "ClH"),
})
# Batch G: independently crosschecked PubChem CAS/name/formula concepts, not supplier material.
EXPECTED.update({
    "glicerin-industrial": (753, 753, "56-81-5", "C3H8O3"),
    "borkosav-l-food": (875, 444305, "87-69-4", "C4H6O6"),
    "trietilen-glikol-industrial": (8172, 8172, "112-27-6", "C6H14O4"),
    "tiokarbamid-industrial": (2723790, 2723790, "62-56-6", "CH4N2S"),
    "natrium-tripolifoszfat-industrial": (24455, 24455, "7758-29-4", "Na5O10P3"),
    "natrium-hipoklorit-150-g-l-90-g-l-industrial": (23665760, 23665760, "7681-52-9", "ClNaO"),
    "trinatrium-citrat-industrial": (6224, 6224, "68-04-2", "C6H5Na3O7"),
    "natrium-molibdat-feed": (61424, 61424, "7631-95-0", "MoNa2O4"),
    "natrium-metaszilikat-industrial": (23266, 23266, "6834-92-0", "Na2O3Si"),
    "kenpor-industrial": (402, 5362487, "7704-34-9", "S"),
    "natrium-metabiszulfit-natrium-piroszulfit-industrial": (24346, 656671, "7681-57-4", "Na2O5S2"),
})

# Batch H primary NIH/NLM sources; general chemicals only, not offered materials.
EXPECTED.update({
    "kalium-jodat-feed": (81757, 23665710, "7758-05-6", "IKO3"),
    "mangan-oxid-feed": (14940, 14940, "1344-43-0", "MnO"),
    "natrium-perszulfat-industrial": (62655, 62655, "7775-27-1", "Na2O8S2"),
    "diammonium-hidrogenfoszfat-industrial": (24540, 24540, "7783-28-0", "H9N2O4P"),
    "meszhidrat-industrial": (14777, 14777, "1305-62-0", "CaH2O2"),
    "meszhidrat-15-industrial": (14777, 14777, "1305-62-0", "CaH2O2"),
})

# Batch I primary PubChem salt/protonation evidence, never supplier approvals.
EXPECTED.update({
    "dikalium-hidrogen-foszfat-food": (24450, 24450, "7758-11-4", "HK2O4P"),
    "dinatrium-pirofoszfat-food": (24451, 24451, "7758-16-9", "H2Na2O7P2"),
    "dinatriumfoszfat-industrial": (24203, 24203, "7558-79-4", "HNa2O4P"),
    "dinatriumpirofoszfat-industrial": (24451, 24451, "7758-16-9", "H2Na2O7P2"),
    "monokalium-foszfat-industrial": (24506, 24506, "7778-77-0", "H2KO4P"),
    "mononatrium-foszfat-industrial": (24204, 24204, "7558-80-7", "H2NaO4P"),
    "mangan-karbonat-industrial": (11726, 11726, "598-62-9", "CMnO3"),
    "vas-iii-klorid-40-oldat-industrial": (24380, 24380, "7705-08-0", "Cl3Fe"),
})

errors: list[str] = []
if len(CATALOGUE) != 127 or len(REGISTRY.get("entities", [])) != 127:
    errors.append("Unexpected catalogue/registry size")
entries = {x["id"]: x for x in REGISTRY["entities"]}
evidence = {x["id"]: x for x in RESEARCH["entries"]}
if set(evidence) != set(EXPECTED):
    errors.append("General-source references have unreviewed or missing entries")
if RESEARCH.get("commercial_grade_verified") != 0:
    errors.append("Supplier grade was incorrectly approved by general references")
if RESEARCH.get("other_catalogue_families_not_yet_independently_verified") != 37:
    errors.append("Full catalogue research coverage misrepresented")
for pid, (rejected, cid, cas, formula) in EXPECTED.items():
    item = entries.get(pid, {})
    cited = evidence.get(pid, {})
    if (item.get("cas"), item.get("pubchem_candidate_cid"),
            item.get("pubchem_candidate_formula")) != (cas, cid, formula):
        errors.append(f"{pid}: wrong candidate CAS/CID/formula association")
    if cited.get("pubchem") not in (f"https://pubchem.ncbi.nlm.nih.gov/compound/{cas}", f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"):
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

QUARANTINE = set(RESEARCH.get("rejected_legacy_automatic_pubchem_product_ids", []))
if len(QUARANTINE) != 8 or RESEARCH.get("rejected_legacy_automatic_pubchem_match_count") != 8:
    errors.append("Unreviewed ion/hydrate/molecule quarantine is incomplete")
if QUARANTINE & set(EXPECTED):
    errors.append("Source-reviewed and quarantined identities must not overlap")
for pid in sorted(QUARANTINE):
    entry = entries.get(pid, {})
    if entry.get("pubchem_candidate_cid") is not None or entry.get("pubchem_candidate_formula") is not None:
        errors.append(f"{pid}: known wrong source candidate was reintroduced")
    if entry.get("pubchem_status") != "rejected-incorrect-substance-or-form":
        errors.append(f"{pid}: rejected source not marked as rejected")
    if entry.get("pubchem_cid") is not None or entry.get("sameAs_status") == "verified":
        errors.append(f"{pid}: rejected PubChem candidate promoted to public identity")
    source_rows = [r for r in ROWS if r["product_id"] == pid and
                   r["source_type"] == "RejectedCandidate"]
    if len(source_rows) != 1 or source_rows[0].get("source_url"):
        errors.append(f"{pid}: rejected source URL must be absent from source register")
for pid in ("borax-dekahidrat-industrial", "borax-pentahidrat-industrial"):
    e = entries.get(pid, {})
    if e.get("wikidata_qid") or e.get("wikidata_label"):
        errors.append(f"{pid}: unapproved or mismatched hydrate Wikidata sameAs")
if len(EXPECTED) != 90 or len({x["cid"] for x in RESEARCH["entries"]}) != 74:
    errors.append("General compound review must contain 90 families and 74 distinct CIDs")
# Multi-hydrate parent families deliberately remain outside approved single-CID
# references. Two sourced variants are not proof of one offered commercial product.
groups = VARIANT_SOURCES.get("groups") or {}
variant_ids = [pid for g in groups.values() for pid in g.get("family_ids", [])]
if len(groups) != 4 or len(variant_ids) != 8 or len(set(variant_ids)) != 8:
    errors.append("Expected 4 general chemical groups and 8 family routes with variant evidence")
if VARIANT_SOURCES.get("supplier_lots_verified") != 0 or VARIANT_SOURCES.get("commercial_sameas_approved") != 0:
    errors.append("Variant sources cannot assert commercial supplier or sameAs approval")
for group in groups.values():
    for form in group.get("variants", []):
        cas = form.get("cas")
        cid = form.get("cid")
        if not cas or not isinstance(cid, int) or form.get("source_url") not in (
                f"https://pubchem.ncbi.nlm.nih.gov/compound/{cas}",
                f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"):
            errors.append("Variant form source URL is invalid")
for pid in variant_ids:
    e = entries.get(pid, {})
    scope = e.get("form_specific_research_reference") or {}
    if scope.get("scope") != "form_specific_general_substances_not_offered_product" or scope.get("supplier_evidence_status") != "unverified":
        errors.append(f"{pid}: variant source evidence scope missing or inflated")
    if scope.get("commercial_product_identity_approved") is not False:
        errors.append(f"{pid}: commercial product identity was improperly approved")
    if e.get("independent_general_substance_reference") or e.get("pubchem_cid") is not None or e.get("sameAs_status") == "verified":
        errors.append(f"{pid}: multiple possible CAS/grades must not become single-CID product equivalence")
if set(variant_ids) & set(EXPECTED):
    errors.append("Multi-variant unresolved families must not be counted as approved single-substance identities")

if len(ROWS) != 369:
    errors.append(f"Source register unexpected row count: {len(ROWS)}")
print(f"Primary substance research: {len(EXPECTED)} general concepts crosschecked, "
      f"{len(CATALOGUE)-len(EXPECTED)} unreviewed; "
      f"0 supplier grades approved; {len(errors)} source errors")
for error in errors[:35]:
    print("ERROR:", error)
raise SystemExit(bool(errors))
