# Changelog v3 — 2026-11-08

## PR #13 integration
- Merged bentonite / L(+) tartaric acid / butyl glycol EN/HU/DE pages and procurement JSON guidance.
- Added qualification note, dual-path, product-specific checkpoints/FAQs + FAQPage JSON-LD without duplicating PR13 guidance blocks.
- Bumped those pages to `site.v20261108.js` / `a11y-fixes.v3.css`.

## Evidence & entity policy
- SOURCE-REGISTER: ECHA rows marked identity-link-only (not REACH/CLP proof).
- Rejected false PubChem hit for bentonite mineral CAS.
- Downgraded form-ambiguous `sameAs_status=verified` entries (solutions/regenerated/anhydrous/hydrate) to needs-confirmation.
- Added bentonite, tartaric, butyl glycol to entity-registry.json.

## Audit
- Release audit now requires 378 pages / 126 families, FAQ uniqueness, FAQ schema↔visible parity, dual-path presence, and rejects unsafe verified sameAs for form-ambiguous IDs.

## Visual
- Local browser QA across 375/390/768/1024/1440 with screenshots in HANDOFF/visual/.
