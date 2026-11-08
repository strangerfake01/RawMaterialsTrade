# QA results (actually executed)

| Check | Result | Notes |
|---|---|---|
| python3 tools/audit_release_contract.py | PASS | 405 sitemap URLs; product intelligence 369/0/0 |
| JSON-LD parse on enriched samples | PASS | FAQPage questions match visible FAQs on samples |
| Generic FAQ boilerplate remaining | PASS | 0 pages |
| PR #13 reserved files untouched | PASS | git clean for those 9 HTML files |
| Contrast calculations (selected pairs) | PASS | qualification/link/contact pairs ≥ 4.5:1 |
| Local browser FAB permanent visibility | PASS | computerUse on 127.0.0.1:8765; remains visible at footer on home + product; Escape closes panel |
| Live production FAB | NOT RUN | requires deploy + hard refresh of v20261108 assets |
| Form Turnstile E2E | NOT RUN | deferred |
