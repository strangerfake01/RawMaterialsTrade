# Supplier evidence request — product-grade comparison (internal template)

**Purpose:** gather verifiable evidence before assessing whether two catalogue entries with the same CAS number could be suitable for the *same explicitly defined application*. A shared CAS number is not an approval or a substitution claim.

## Request metadata
- Source catalogue ID:
- Candidate catalogue ID:
- Intended application, process, jurisdiction and customer specification:
- Supplier / manufacturer, product code and production site:
- Request owner / date:
- Response due date:

## Request the supplier's current, product-specific evidence
1. **Technical Data Sheet (TDS)**: trade name, CAS/EC, grade, assay/concentration and measurement basis, physical form, particle size/density where applicable, water/hydration and specification tolerances.
2. **Safety Data Sheet (SDS)**: current revision, classification, handling, storage and transport conditions for the offered material.
3. **Certificate of Analysis (CoA)**: representative batch, assay and relevant impurities with test methods, units and limits; clarify batch-to-batch variation.
4. **Regulatory / intended-use evidence**: only where applicable, confirm food, feed, pharmaceutical or other application-specific compliance with precise standards, scope and effective dates. Never infer this from purity or CAS alone.
5. **Commercial and logistics evidence**: origin, pack size, MOQ, available quantity, lead time, Incoterms, shelf life, sample availability and change-control notification.

## Internal comparison and decision
- Identify all material differences, including dilution/conversion factor, impurities, physical form, grade and safety conditions.
- Record which requirements are met, not met, or unknown, and the supplier documents that support each decision.
- Determine whether customer trials, regulatory review or a qualified technical sign-off are required.
- Record the final application-specific decision, evidence references, verification dates and reviewer in the governed substitution registry.
- **Do not publish a substitution recommendation while evidence or review is incomplete.**

## Handling
Keep confidential supplier documents and customer specifications in an access-controlled business system. The public GitHub repository must contain only non-confidential references and approved public claims; do not commit supplier CoAs, contracts, private emails or customer information.

### Reference convention

- Do not publish supplier-specific evidence IDs, even opaque IDs, unless independently reviewed as non-linkable. Prefer a public-facing generic verification statement; keep document identifiers and their mapping in a restricted internal evidence register. The existing public substitution registry must not contain supplier names, manufacturer codes, document IDs or other traceable sourcing metadata.
- Keep the evidence IDs, actual supplier files, document versions, batches, source identifiers and access permissions exclusively in the restricted evidence register.
- Never include supplier names, manufacturer names or product codes, personal email addresses, private cloud share links, credentials, confidential pricing, customer specifications, distinctive document numbers or sourcing-identifying metadata in public evidence references. Avoid combinations of apparently harmless details that could identify a supplier.
- Before approval, a qualified reviewer must open the restricted source document and verify that the exact grade, batch/specification, intended application and limitations match the substitution claim.
- The automated validator checks structure and chronology only; it cannot verify a document's authenticity, completeness or regulatory suitability.
