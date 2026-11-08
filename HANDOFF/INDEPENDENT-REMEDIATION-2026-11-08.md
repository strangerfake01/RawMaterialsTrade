# Independent remediation 2026-11-08

- Verified that all 66 HTML files in the earlier ChemicalSubstance sameAs safety patch already match the supplied full repository byte-for-byte; no further sameAs file changes were required.
- Reconstituted asset paths from existing root/media files; originals retained.
- Added consent-first GA4 manager at the referenced path (G-13022PNK14). Analytics is disabled until opt-in. Settings can be reopened and rejection removes accessible _ga cookies.
- Updated GitHub Actions JS syntax target to V3 script; added consent JS syntax check.
- The existing audit is structural; it is not an external chemical specification or live browser endorsement.
- Form submission and Turnstile E2E were not executed.
- Production/live-device verification and Google Analytics behavior with actual browsers remain required.

- The `site.v20260709e.min.css` referenced by six pages was not present in any package; this candidate supplies the known `site.v20260709.min.css` as a fallback under that URL, pending browser comparison.
