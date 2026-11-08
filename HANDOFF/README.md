# Raw Materials Trade — Product Master Remediation Handoff

**Package:** `RawMaterialsTrade_PRODUCT_MASTER_REMEDIATION_2026-11.zip`  
**Base commit (GitHub `main`):** `51fad6f121de388d22e87724432000b434b64903`  
**Generated:** 2026-11-08 (Europe/Vienna)  
**Operator action:** extract at repository root, review, open PR, do **not** merge/deploy without approval.

## What this package is

A static-site remediation for catalogue discoverability, buyer/supplier pathways, floating contact reliability, and multilingual evidence links. It is safe to extract over a clean checkout of `main` at the base SHA above.

## What this package is not

- Not a full ECHA/EUR-Lex first-principles rewrite of every substance monograph.
- Not a claim that every product is certified, in stock, or approved for every use.
- Not a Cloudflare / form-backend / Turnstile / DNS change.
- Not a merge of open **PR #13** (bentonite, L(+)-tartaric acid, butyl glycol). Those nine HTML files were intentionally left untouched.

## Import instructions

```bash
git clone https://github.com/strangerfake01/RawMaterialsTrade.git
cd RawMaterialsTrade
git checkout main
git checkout -b content/product-master-remediation-20261108
# optional integrity check
git rev-parse HEAD   # expect 51fad6f… or later main; re-diff if main moved
unzip -o /path/to/RawMaterialsTrade_PRODUCT_MASTER_REMEDIATION_2026-11.zip
python3 tools/audit_release_contract.py
# review HANDOFF/*, then commit + open PR
```

## Cloudflare configuration unchanged

Worker URL, CSP / `form-action`, Turnstile, and contact endpoint strings were not redesigned. Form submit logic remains the existing shared script.

## Completed product count

- Catalogue families in repo: **126**
- Language product pages: **378**
- Pages enriched in this package (dual path + FAQ + qualify note): **369**
- Reserved pending PR #13 (skipped): **9**
