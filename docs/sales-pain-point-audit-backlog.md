# P0 — Sales pain-point audit: Nikoletta Kádár

Status: IN PROGRESS. Scope: sales correspondence in the connected Raw Materials Trade mailbox, mapped to EN/HU/DE-AT website content and buyer journey. Do not publish customer names, correspondence, negotiated prices, contact details, confidential delivery data, or individual terms.

## First evidence-based sample (2026-11-03 to 2026-11-06)

Six detailed emails reviewed (non-exhaustive). Sales workflow observed:
1. Compare supplier/grade variants of the same chemical with different pallet quantities and packaging. Website: grade/alternative pathways exist; supplier-variant decision support not fully verified.
2. Communicate actual availability, collection windows, Incoterms and payment terms. Website: generic procurement fields exist, but no verified real-time stock or fixed terms. Do not imply guaranteed stock or prices.
3. Source urgent quantities and communicate uncertain arrival/collection dates. Website: generic lead-time fields exist; dedicated urgent RFQ pathway needs assessment.
4. Obtain and forward batch-specific CoA for sodium percarbonate. Website: CoA mentioned; clear document request/availability workflow needs verification.
5. Search for non-catalogue chemicals or unavailable items. Website: general sourcing route exists; explicit non-catalogue sourcing request should be evaluated.
6. Prevent lost deals caused by slow supplier response or uncertain delivery. Website: verify expectation-setting, response process, and non-binding ETA language.

## Required audit matrix for every meaningful sales conversation
- Date/time window; anonymized conversation reference (internal only)
- Buyer/supplier type and request category
- Pain point and precise question asked
- Sales solution actually offered (not hypothetical)
- Product/CAS/grade/concentration/packaging/quantity/logistics/documentation attributes
- Website destination: exact EN/HU/DE-AT URLs and existing relevant text
- Status: implemented / partial / absent / requires business decision
- Proposed change, owner, priority, evidence, and QA result

## Work plan
- [ ] Audit representative inbound and outbound conversations across time periods, not only recent sent mail; deduplicate threads.
- [ ] Classify recurring buyer pain points: specification, alternative grade/supplier, MOQ, packaging, availability, urgency, Incoterms, freight, CoA/SDS/TDS, payment, non-catalogue sourcing, claim handling.
- [ ] Classify supplier pain points and procurement responses separately.
- [ ] Compare each verified sales solution to homepage, sourcing pages, all 126 product families × 3 languages, and RFQ pathway.
- [ ] Implement missing generic process explanations and safe decision aids without exposing individual customer information or commercial secrets.
- [ ] Avoid publishing unsupported stock, delivery promises, prices, supplier names or fixed payment terms.
- [ ] Validate translations, internal links, schema claims, mobile UX and release CI; check production only after approved merge.
- [ ] Maintain evidence-based gap register and completion report with exact URLs and commit references.

## Initial implementation assessment
EN sample product pages checked: sodium carbonate light, sodium percarbonate, trisodium phosphate. These include buyer/supplier pathways and CoA/Incoterms/MOQ/lead-time terminology. Presence of terms is NOT evidence that real-world sales solutions are fully implemented. Current finding: PARTIAL; deeper full-site and full-mailbox audit pending.

## Implementation batch — 2026-11-09

Expanded correspondence sample: October 16–November 6, including detailed packaging negotiation, specification-led MPG sourcing, urgent trisodium phosphate sourcing, and supplier quality/compliance document request. This remains a sample, not a full-mailbox audit.

- [x] Ion-exchanged water EN/HU/DE-AT: dedicated packaging/consumption/storage request guidance. No universal shelf-life claim; supplier-specific evidence required.
- [x] Monopropylene glycol EN/HU/DE-AT: detailed specification comparison request, TDS and batch CoA verification.
- [x] Trisodium phosphate EN/HU/DE-AT: urgent sourcing intake and hydrate-form clarification; no stock or delivery promise.
- [ ] Extend conditional supplier documentation checklist to food/feed applications; do not imply all parameters apply to every chemical.
- [ ] Review all remaining correspondence and compare homepage, sourcing pages, contact flow and 126 families.
- [ ] Verify visual accessibility and mobile presentation of the new product-sales-guidance sections.

Privacy: no customer names, negotiated prices or specific correspondence are included in public product pages.

## Implementation batch — batch-specific CoA (2026-11-09)

Additional October correspondence reviewed: specific lot/batch CoA requests, sodium bicarbonate for animal feed, and supplier distinction between generic SDS/TDS and order-specific CoA. Supplier certificates may be expired or pending renewal; never imply certification without current evidence.

- [x] Sodium bicarbonate (food-labelled catalogue page), EN/HU/DE-AT: explain lot number, intended use, actual grade and batch-specific CoA; do not infer feed approval from food catalogue category.
- [x] Sodium percarbonate EN/HU/DE-AT: explain CoA requests for delivered batches, test parameters and deadlines.
- [ ] Extend evidence-based documentation workflow to other food/feed product families where correspondence supports the need.
- [ ] Verify actual RFQ form captures batch number, document type and intended use where relevant (form testing remains deferred per project decision).
- [ ] Complete visual QA and CI for this batch.

## Implementation batch — industrial salt and bulk sodium bicarbonate (2026-11-09)

Further sales evidence reviewed: industrial salt-tablet RFQ for water softening with quality certificate and FCA/DAP comparison; bulk sodium bicarbonate delivery planning with unloading slot and order/transport references; food-grade calcium sulfate procurement with delivered terms, batch CoA and remaining shelf-life constraints.

- [x] Salt tablets industrial EN/HU/DE-AT: intended application, specification, tonnage, packaging, FCA/DAP and certificate checklist.
- [x] Sodium bicarbonate industrial EN/HU/DE-AT: bulk/big-bag delivery, Incoterms, time-slot and unloading requirements.
- [ ] Locate the exact calcium sulfate catalogue family and grade before changing it; do not invent a product slug or equate industrial grade with food grade.
- [ ] For food-grade orders, assess conditional remaining shelf-life at delivery and batch documentation. Do not state a universal two-thirds requirement: it was a customer-specific contractual requirement.
- [ ] Verify latest CI and responsive rendering for all newly inserted guidance sections.

## Implementation batch — food receiving and shelf-life (2026-11-09)

Catalogue checked: 126 product families, 34 food/feed-labelled families. The calcium sulfate food-grade item mentioned in sales correspondence is NOT present as a matching product family in the current products-multilingual.json; flag as catalogue gap, do not silently substitute calcium carbonate.

- [x] Citric acid monohydrate/anhydrous food EN/HU/DE-AT: conditional remaining shelf-life at delivery, form, batch CoA and storage verification.
- [x] Calcium carbonate food EN/HU/DE-AT: receiving specification, contaminant limits, food-use evidence and customer-defined shelf-life.
- [ ] Catalogue decision: whether to add calcium sulfate food grade as a new, documented family (requires verified supplier grade, CAS, regulatory evidence and technical sheet).
- [ ] Check remaining 32 food/feed families for relevant sales documentation needs and language parity.
- [ ] CI and visual QA for new guidance; do not merge until verified.

## Implementation batch — feed-grade trace element (2026-11-09)

- [x] Zinc sulfate monohydrate feed EN/HU/DE-AT: specify species/intended use, Zn assay, monohydrate form, impurity limits, lot CoA and applicable feed regulatory evidence. Industrial-grade equivalence explicitly disclaimed.
- [ ] Verify applicability of this pattern to remaining feed-labelled families one by one; do not mechanically copy product-specific regulatory language.
- [ ] Complete responsive visual QA and review branch CI before merge.

## Feed-labelled catalogue verification — 2026-11-09

Catalogue source has 126 families; 21 carry a feed category (some also industrial/food). This is a classification, not proof of regulatory approval. Prior guidance for zinc sulfate monohydrate remains in place.

- [x] Sodium selenite EN/HU/DE-AT: target species, selenium assay, chemical form, market authorization, use levels, labeling, supplier CoA.
- [x] Copper sulfate EN/HU/DE-AT: copper assay, exact hydrate, impurity limits, feed authorization/restrictions, lot CoA.
- [ ] Review remaining feed-labelled families, including vitamin mixtures, for product-specific authorization, specifications and naming accuracy; do not imply universal feed eligibility.
- [ ] Obtain current supplier technical evidence before asserting approvals or exact numerical limits.
- [ ] Responsive visual QA and latest CI checks pending; merge/deployment not authorized by this documentation update.

## Feed portfolio refinement — vitamins and iodine (2026-11-09)

- [x] Grouped vitamin portfolio EN/HU/DE-AT: distinguish individual vitamins and chemical forms, potency units, carrier/formulation, species, supplier lot CoA, stability and market-specific feed authorization. Do not imply a standard blend.
- [x] Calcium iodate EN/HU/DE-AT: iodine assay, exact grade/hydrate, species, impurity limits, lot CoA and applicable feed authorization/labeling.
- [ ] Remaining feed categories require product-by-product review; verify authoritative supplier evidence before numeric specification or regulatory claims.
- [ ] Validate responsive layout and CI for this batch before merging.

## Feed-labelled catalogue verification — vitamins and iodine (2026-11-09)

- [x] Vitamin portfolio (A, B1, B12, B5, B6, C, D3, E, H, K3) EN/HU/DE-AT: explicitly a sourcing grouping, not a single standardized product or interchangeable formulation; require exact vitamin, chemical form, activity units, carrier, species, batch CoA and product-specific regulatory evidence.
- [x] Calcium iodate feed EN/HU/DE-AT: iodine assay, hydration state, species, impurity limits, batch CoA and applicable feed authorization.
- [ ] Evaluate whether the vitamin portfolio should be split into distinct product families with verified supplier evidence; avoid creating unsupported CAS, grades or regulatory claims.
- [ ] Review remaining feed-labelled families for chemical identity and feed-specific regulatory distinctions.
- [ ] Re-run CI and mobile/desktop visual QA before considering merge.

## Feed iodine sources — 2026-11-09

- [x] Potassium iodate EN/HU/DE-AT: distinguish from iodide; specify iodine assay, target species, impurity limits, lot CoA and market-specific authorization.
- [x] Potassium iodide EN/HU/DE-AT: distinguish from iodate; verify supplier grade, permitted use, labeling and authorization rather than assuming interchangeability.
- [ ] Review remaining feed-labelled families with distinct chemical forms or species-specific limits.
- [ ] Verify responsive rendering and final CI before merge; no publication implied.

## Feed trace-element continuation — 2026-11-09

- [x] Manganese sulfate monohydrate EN/HU/DE-AT: manganese assay, hydrate form, impurity limits, batch CoA and feed-use evidence.
- [x] Iron(II) sulfate monohydrate EN/HU/DE-AT: elemental iron assay, chemical/hydration identity, relevant impurity and oxidation criteria, batch CoA and feed-use evidence.
- [ ] Continue product-specific review of remaining feed-labelled families, prioritizing substances with narrow use conditions.
- [ ] Confirm responsive rendering and latest CI before merging or publishing.

## Feed continuation — cobalt, molybdate, magnesium oxide (2026-11-10)

- [x] Cobalt(II) carbonate EN/HU/DE-AT: no automatic feed eligibility; verify market-specific authorization, species, permitted use, labeling and batch CoA before any claim.
- [x] Sodium molybdate EN/HU/DE-AT: exact form, molybdenum assay, market-specific authorization and documentation verification.
- [x] Magnesium oxide feed EN/HU/DE-AT: MgO/Mg assay, particle size or reactivity where applicable, impurities, batch CoA and feed-use evidence.
- [ ] Review remaining feed catalogue entries and identify which need evidence-based edits rather than generic copy.
- [ ] Confirm current branch CI and mobile/desktop visual rendering; no merge/deployment has been verified.
