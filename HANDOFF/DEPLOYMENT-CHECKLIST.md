# Deployment checklist (v3)

1. Start from `65d878ff84701e1e2847e645016e94cf8ad7eecb` (or rebase carefully if main moved).
2. Apply this ZIP.
3. Run `python3 tools/audit_release_contract.py` — must PASS with 378/126.
4. Confirm PR #13 pages still contain `product-procurement-guidance` plus new FAQ/checkpoints/dual-path (no duplicates).
5. After upload, hard-refresh production to load `site.v20261108.js` and `a11y-fixes.v3.css`.
6. Manually re-check FAB on iOS Safari + Android Chrome against footer + cookie banner states.
7. Do not merge/deploy without explicit approval.
