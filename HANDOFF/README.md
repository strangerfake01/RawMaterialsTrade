# Raw Materials Trade — Product Master Remediation v2

**Package:** `RawMaterialsTrade_PRODUCT_MASTER_REMEDIATION_v2.zip`  
**Base commit audited:** `68d378ea18917742d91076d14e595c0968ec0406` (`main`)  
**Generated:** 2026-11-08 (Europe/Vienna)

## What changed in v2 vs prior package
- Replaced generic FAQ boilerplate with **product-specific** FAQs (hydrate/concentration/food/feed/solution/regenerated where relevant).
- Added **procurement checkpoints** per product using catalogue identity + PubChem/Wikidata evidence where available.
- Built **product-level SOURCE-REGISTER.csv** (PubChem, Wikidata, ECHA entry points) with access dates.
- Validated Wikidata QIDs by CAS; `sameAs` remains needs-confirmation unless Wikipedia URL heuristically matches label.
- Cache-busted floating contact assets: `site.v20261108.js` + `a11y-fixes.v3.css` (permanent FAB visibility; matched cookie/contact tokens).
- Restored/extended `tools/audit_release_contract.py` on this package (missing from audited main tree before this ZIP).

## Counts
- Families: 126
- Language product pages: 378
- Enriched in v2 (FAQ+checkpoints): 369
- Reserved for open PR #13: 9

## Cloudflare configuration unchanged
Worker / form-action / Turnstile / contact endpoint not redesigned.

## Import
```bash
git checkout 68d378ea18917742d91076d14e595c0968ec0406
git checkout -b content/product-master-remediation-v2-20261108
unzip -o RawMaterialsTrade_PRODUCT_MASTER_REMEDIATION_v2.zip
python3 tools/audit_release_contract.py
```
Do not merge/deploy without separate approval. Resolve PR #13 before touching those nine pages.
