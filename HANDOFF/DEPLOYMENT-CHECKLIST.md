# Deployment checklist

1. Extract ZIP onto clean checkout at base SHA 68d378e (or rebase carefully if main moved).
2. Ensure PR #13 files were not overwritten.
3. Run python3 tools/audit_release_contract.py — must PASS.
4. Hard-refresh live preview to load site.v20261108.js / a11y-fixes.v3.css.
5. Manually verify FAB on iPhone Safari + Android Chrome after deploy.
6. Merge only after CI + human review; deploy only with approval.
