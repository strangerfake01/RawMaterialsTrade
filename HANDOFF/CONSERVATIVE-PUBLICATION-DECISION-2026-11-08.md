# V4 conservative product publication decision — 2026-11-08

Decision: use **conservative B2B publication**, not a claim of supplier-grade chemical or regulatory verification. This decision does not waive independent acceptance, privacy, mobile QA, or deployment checks.

## Mandatory publication semantics (all 126 families / EN, HU, DE-AT)

1. Product pages are **indicative B2B enquiry material**, not binding offers or certified specifications.
2. Identify chemical form and CAS only as catalogue orientation unless independently supported. Do not infer suitability, purity, grade, certification, regulatory classification, or REACH/CLP status from a catalogue field.
3. SDS, TDS, CoA and other documents are **requested for the exact offered supplier material**; never imply a downloadable or already-verified supplier document when no direct evidence exists.
4. Packaging, MOQ, stock, origin, delivery regions, lead times, Incoterms, price and availability are **subject to written confirmation** for the selected offer.
5. Food, feed, pharmaceutical and other regulated uses require separate supplier evidence and applicable compliance review; a purity percentage alone does not certify a grade.
6. Keep EN/HU/DE-AT product identities, route relationships and procurement guidance aligned with the catalogue; do not change an unrelated product family through global text replacement.
7. Do not expose customer emails, private commercial terms, or unsupported supplier names.
8. Preserve search discoverability: indexable product pages, canonical/hreflang, accurate structured data, and honest document status.

## Current evidence boundary

The V4 evidence matrix covers 126 families and 378 localized product routes. It reports **zero direct supplier SDS/TDS/CoA links** and **126 identity records needing confirmation**. Structural presence is not external scientific verification.

## Release gate

- CI: static release contract and catalogue parity must both pass on the exact final head SHA.
- Re-run internal-link, public-claim, privacy, chemical-source, technical-semantics, and evidence-depth audits against that SHA.
- Review unqualified supplier/document/grade claims in rendered visible text and JSON-LD; remove or qualify every confirmed instance.
- Validate actual mobile/desktop UX, hreflang, sitemap, certificate scopes, and live deployment independently.
- Form submission E2E remains explicitly deferred and must be disclosed; do not mark it tested.
- Keep the PR in draft and unmerged until acceptance evidence is recorded. Do not claim all products chemically verified.

This policy authorizes a cautious public presentation; it does **not** authorize inventing evidence or silently passing unverified claims.
