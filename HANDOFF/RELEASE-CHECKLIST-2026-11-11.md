# PR #22 Technical Release Checklist

Date: 2026-11-11
Repository: strangerfake01/RawMaterialsTrade
Branch: integration/rmt-v4-20261108

## Completed technical gates

- [x] PR #20 certificate collision checked; identical public certificate blobs confirmed.
- [x] Public supplier-name removal from leadership schema.
- [x] Supplier disclosure and confidential-history audits.
- [x] EN/HU/DE page, canonical, hreflang, JSON-LD and catalogue parity checks.
- [x] AI-facing profile and `llms.txt` publication boundary.
- [x] Consent-first analytics code review; analytics is not loaded before consent in the verified desktop state.
- [x] Desktop production smoke review on EN, HU and DE routes.
- [x] CI: Static release contract, Product identity regression, Product catalogue parity and Confidential Git history audit.

## Release smoke sequence

1. Open `/`, `/hu.html` and `/de-at.html`.
2. Confirm title, language, canonical and hreflang links.
3. Confirm cookie banner is visible before analytics consent.
4. Choose essential-only consent and verify analytics remains disabled.
5. Choose analytics consent in a clean browser context and verify only the configured analytics request starts.
6. Open one catalogue page in each language and verify CAS/form/grade wording.
7. Open the certificate preview and confirm both public certificate assets load.
8. Check contact CTA, privacy, imprint and catalogue links.
9. Record desktop and mobile screenshots plus console/network errors.

## Rollback plan

- Stop the release if any smoke step fails or any confidential-data scan reports a hit.
- Preserve the failing commit SHA and deployment identifier.
- Revert the deployment to the previous known-good production commit.
- Re-run the four CI gates against the rollback target.
- Re-check EN/HU/DE homepages, cookie consent, certificate links and contact routes.
- Keep the form E2E test as a separate follow-up task.

