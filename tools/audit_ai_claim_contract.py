#!/usr/bin/env python3
"""Keep AI-facing sourcing claims aligned with unverified catalogue evidence."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
registry = json.loads((root / "entity-registry.json").read_text(encoding="utf-8"))["entities"]
products = json.loads((root / "products-multilingual.json").read_text(encoding="utf-8"))
llms = (root / "llms.txt").read_text(encoding="utf-8")
errors = []
profile = json.loads((root / "ai-company-profile.json").read_text(encoding="utf-8"))
boundary = profile.get("catalogueEvidenceBoundary", {})
if profile.get("machineReadableProductData", {}).get("productCount") != len(products):
    errors.append("AI profile product count differs from canonical catalogue")
if boundary.get("productFamilies") != len(products) or boundary.get("status") != "catalogue_enquiry_only":
    errors.append("Machine-readable company profile lacks an accurate catalogue evidence boundary")
if boundary.get("languageVariants") != ["en", "hu-HU", "de-AT"]:
    errors.append("Machine-readable evidence boundary does not preserve three-language parity")
for key in ("chemicalIdentity", "supplierDocumentation", "commercialTerms", "privacy"):
    if not boundary.get(key):
        errors.append("Machine-readable evidence boundary missing: " + key)

if len(products) != 126 or len(registry) != len(products):
    errors.append("Catalogue and registry family counts diverge")
if {p["id"] for p in products} != {e["id"] for e in registry}:
    errors.append("Catalogue and registry family identities diverge")
if "126 product families" not in llms or "126 termékcsalád" not in llms or "126 Produktfamilien" not in llms:
    errors.append("AI catalogue family counts missing or inconsistent across languages")
if "A catalogue listing is not evidence that these documents are already available or independently verified." not in llms:
    errors.append("AI-facing source disclosure absent")
for forbidden in (
    "documentation are confirmed per product, grade and supplier before every order",
    "supplied within verified documentation and applicable GMP+ scope",
    "Takarmányipari anyagok ellenőrzött dokumentációval",
    "Futtermittelbezogene Materialien mit geprüfter Dokumentation",
):
    if forbidden in llms:
        errors.append("Unsupported blanket documentation assertion in llms.txt")
if any(e.get("sameAs_status") == "verified" for e in registry):
    errors.append("Heuristic verified entity status leaked into registry")
print("AI trust claim contract:",len(products),"families; errors=",len(errors))
for e in errors:
    print("ERROR:",e)
raise SystemExit(bool(errors))
