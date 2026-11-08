# Deployment checklist (operator)

1. Extract ZIP on clean `main` (or rebased main).
2. Confirm base SHA and resolve conflicts with any newer commits / PR #13.
3. Run `python3 tools/audit_release_contract.py`.
4. Spot-check reserved PR #13 files were not overwritten.
5. Open PR — do not merge until CI green and human review.
6. After merge: wait for Pages deploy; verify exact-live FAB + one product page per language.
7. Submit sitemap only after live verification.
8. Record production SHA.
