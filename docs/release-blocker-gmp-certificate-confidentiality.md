# Release blocker: GMP+ PDF provenance and supplier confidentiality

Status: **OPEN — do not bypass the supplier-disclosure CI gate.**

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
