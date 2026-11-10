# Same-CAS substitution review priorities — 2026-11-10

**Scope:** 23 candidate pairs across 18 CAS groups. These are screening priorities, not verified substitutions. Do not interpret a higher priority as evidence of technical compatibility.

## P0 — regulated-grade or high-consequence differences

Review first where the catalogue mixes food, feed, pharmaceutical and technical grades under one CAS:
- Zinc chloride: feed vs anhydrous industrial (CAS 7646-85-7).
- Disodium pyrophosphate: food vs technical (CAS 7758-16-9).
- Acetic acid: food vs industrial (CAS 64-19-7).
- Sodium chloride: food salt vs road salt / tablet salt / vacuum salt (CAS 7647-14-5); assess each pair separately.
- Phosphoric acid: food vs industrial (CAS 7664-38-2).
- Glycerine: 99.5% food vs industrial/multiple grades (CAS 56-81-5).
- Magnesium chloride: food vs industrial hexahydrate (CAS 7791-18-6).
- Magnesium oxide: feed vs dense industrial (CAS 1309-48-4).
- Manganese sulfate monohydrate: feed vs industrial (CAS 10034-96-5).
- Sodium bicarbonate: food vs industrial (CAS 144-55-8).
- Copper sulfate: feed vs industrial pentahydrate (CAS 7758-99-8).
- Hydrochloric acid: pharmacopoeial vs technical/regenerated (CAS 7647-01-0).
- Iron(II) sulfate: feed monohydrate vs industrial mono-/heptahydrate (CAS 7720-78-7).

**Gate:** obtain exact intended-use regulatory status and supplier-specific grade/impurity evidence. The source's regulatory grade must not be presumed transferable to the candidate.

## P1 — concentration, hydration, form or dosing differences

- Aluminium sulfate: solid vs solution (CAS 10043-01-3).
- Potassium hydroxide: solution vs flakes (CAS 1310-58-3).
- Calcium hydroxide: solid vs 15% form (CAS 1305-62-0).
- Sodium hydroxide: flakes vs 48–50% solution (CAS 1310-73-2).
- Sodium carbonate: light vs dense (CAS 497-19-8).

**Gate:** confirm assay and measurement basis, dilution/stoichiometry, physical performance, handling, equipment suitability and process validation. Differences in density or physical form can be material even for identical chemical identity.

## Operational sequence

1. Use `reports/same-cas-review-queue.csv` as the authoritative *unassessed candidate list*, not as an approval ledger.
2. Assign one technical reviewer and a sales/procurement owner per pair, recording confidential correspondence outside the public repo.
3. Request current SDS/TDS, representative CoA, grade and intended-use evidence using `docs/supplier-substitution-evidence-request.md`.
4. Resolve the application-specific comparison, safety and regulatory gates.
5. Only after qualified approval, add a traceable relationship to `product-substitutions.json`; the CI validator will reject missing evidence or review metadata.
6. Do not create public-facing substitution language for unassessed or incomplete pairs.

**Current state:** all 23 candidate pairs remain unassessed; no supplier-specific evidence or customer validation has been independently verified.
