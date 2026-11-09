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
