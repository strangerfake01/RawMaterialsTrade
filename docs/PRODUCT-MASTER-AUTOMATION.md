# Product master automation

The scheduled workflow `.github/workflows/product-master-sync.yml` downloads the
Drive workbook, creates a redacted change manifest and sends that manifest to
the OpenAI review gate.

## Required GitHub configuration

Environment: `product-master-release`

Secrets:

- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `GOOGLE_DRIVE_FILE_ID`
- `OPENAI_API_KEY`

The service account must have read access to the workbook. The OpenAI key is
used only in GitHub Actions and must never be committed.

## Fail-closed publication rule

The workflow currently refuses to publish spreadsheet values because the
repository does not yet contain an approved deterministic mapping from workbook
columns to catalogue fields and HTML/schema templates. This is intentional:
the OpenAI reviewer may classify a change, but it must not invent or infer
chemical identity, compliance, substitution or commercial data.

Before enabling automatic `main` publication, add and review a mapping that
defines, for every writable column:

- target JSON path;
- allowed source status;
- required evidence fields;
- public/private classification;
- affected language pages;
- regeneration method;
- regression tests;
- rollback behavior.

High-risk fields must remain human-approved: CAS, EC, formula, molecular weight,
purity, physical form, hydrate state, `sameAs`, substitutions, compliance,
prices, stock, MOQ, suppliers and Incoterms.

Until that mapping exists, the workflow is an audit/review gate and does not
change `main` or production.
