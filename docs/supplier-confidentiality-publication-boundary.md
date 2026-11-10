# Supplier confidentiality — publication boundary

**Policy:** Supplier identities, manufacturer identities, contact details, source-specific product codes, procurement terms, document references and identifying combinations of metadata are confidential. Do not publish them in source control, public webpages, schema.org markup, downloadable assets, generated reports or build artifacts.

## Public repository
- `product-substitutions.json` must remain an empty list until a separately designed, privacy-reviewed public recommendation format exists.
- `scripts/check-public-substitution-confidentiality.py` fails CI when any internal substitution record is added to that file.
- `reports/same-cas-review-queue.csv` is a **catalogue-only screening queue**, not a supplier evidence register.
- Public product pages may describe chemical identity, specifications and the Raw Materials Trade service, but must not disclose the source of supply.

## Restricted internal system (not this repository)
Store supplier identity, documents, access-controlled evidence IDs, reviewer identity, customer specifications, traceable approval and audit logs. Restrict access by role and retention policy. This repository must not contain exports or backups of that system.

## Release controls
Before merging, review HTML, JSON-LD, metadata, static assets, CSV reports, commit diffs and generated artifacts for supplier disclosure. A green CI check for an empty registry does **not** certify that other files or historical commits are free of supplier information. A repository-wide disclosure audit remains mandatory.

**Important:** Public GitHub commit history is not a secure storage system. If a supplier secret is ever committed, deleting the file in a later commit is insufficient; follow an incident process, revoke any exposed credentials and assess repository-history remediation.
