# Release blocker: GMP+ PDF provenance and supplier confidentiality

Status: **SECURITY GATE PASSED (2026-11-10) — broader release review remains open.**

The Product identity regression run for commit `59a8694c` failed on the restricted-document check. The following tracked files triggered it:

- `assets/documents/certificates/cert-gmp-plus-2020.pdf`
- `cert-gmp-plus-2020.pdf`

The filename alone does **not** establish the certificate holder, authenticity, validity or whether publication is permitted. Binary PDF inspection via the connected GitHub text endpoint failed; no conclusion about document contents has been made.

## Required review before any exception or removal

1. Obtain the PDF files via an authorized binary-capable channel; compare SHA-256 hashes to determine whether they are duplicates.
2. Identify the certificate holder, issuer, scope, validity, names, addresses, signatures, contact details and any traceable supplier or manufacturer information **in a restricted review environment**.
3. Determine whether the certificate belongs to Raw Materials Trade, is authorized for public redistribution, and is still valid. Do not assume a GMP+ certificate is current because of its filename.
4. Inspect references in HTML, JSON-LD, metadata, navigation and downloadable links before proposing removal or replacement.
5. If supplier-identifying or unauthorized, remove from public delivery and review Git history and existing published copies. Deleting from the current tree does not erase historical exposure.
6. Only if explicitly verified safe, document the review outcome and design a narrowly scoped exception with regression coverage; do not weaken the blanket check without evidence.

Do not place PDF contents, certificate holder names, document IDs, internal source URLs or reviewer contact details in this public issue record. The restricted audit log must hold those details.

## Acceptance criteria

- Both flagged files dispositioned with documented authorization and supplier-confidentiality review.
- Public HTML, JSON-LD and asset references checked for broken links or source disclosure.
- CI green without broadening supplier exposure.
- PR #22 remains draft and unmerged until the review is complete.


## 2026-11-10 — scoped publication approval and integration

The company owner confirmed permission to publish the company GMP+ certificate. A single exact-path SHA-256 pin is now configured for `assets/documents/certificates/cert-gmp-plus-2020.pdf`; the verification metadata originated from Cursor's local review. The CI must verify that the repository PDF bytes match the pinned hash before the document can pass. No other PDF or supplier document is authorized.

**Still required before release:** remove the duplicate root-level `cert-gmp-plus-2020.pdf` from the current branch, confirm any references are updated, and verify all required CI checks pass. The historical audit and any Git history rewrite are separate actions; history rewriting has not been authorized. The 23 same-CAS candidates remain `not_assessed`.


## 2026-11-10 — verified resolution

- Duplicate root-level GMP+ PDF removed from the integration branch.
- Supplier-disclosure scanner and synthetic regression tests pass without blanket exceptions.
- Confidential Git history audit passes: 1,287 reachable commits, two known company-certificate paths, zero other restricted paths, one distinct historical certificate blob matching the approved SHA-256.
- Product identity regression, product catalogue parity, static release contract, and history audit all passed on commit `696f0de252b794cff1b0f7700733c512799e1eca`.
- The historical paths remain in Git history; no rewrite has been performed or authorized.
- PR #22 is ready for review, not merged or deployed. PR #20 overlaps certificate assets and must be reconciled before merge.
- Passing integrity checks does not independently certify the GMP+ certificate's scope, validity, or regulatory claims. The owner approved publication of the company certificate; issuer and validity review remains a distinct factual check.
