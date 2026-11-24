# Raw Materials Trade — public-claims evidence and post-contact confirmation policy

Effective editorial instruction: 2026-11-23. Applies to every public EN/HU/DE-AT HTML route, catalogue JSON, JSON-LD, AI/LLM files, FAQs, metadata, downloads and editorial publication.

## Release rule (default deny)

**If a product-, supplier-, batch- or offer-specific assertion cannot be supported by a current source, do not publish the assertion.** Do not camouflage it with an uncertain numerical guess, a "likely", an automatic external-identifier match, an unauthenticated supplier PDF, or a machine-only Schema.org claim.

Use a short, non-promissory customer action instead: **"Specify your requirement in the enquiry; the exact variant, availability, documents and conditions are checked with the selected supplier after contact."** Translate naturally into HU and DE-AT. Confirm only what the actual evidence supports. An enquiry is not a guarantee that a document or supply is available.

### Must be withheld pending offer-specific evidence

- Price, stock, MOQ, delivery region/route, lead time, available packaging, freight/Incoterms, sample availability, exclusive supplier or guaranteed volume.
- Exact offered grade, concentration, assay/purity, hydrate/solution/form, batch identity, substitution, source and suitability for the stated process.
- Actual availability and contents of SDS, TDS, CoA, test reports, certificates, food/feed approvals, REACH/CLP classification and authorisation for the particular product and use.
- Any unverified ChemicalSubstance `sameAs`, ambiguous CAS/EC/formula/variant mapping, manufacturer affiliation, customer, supplier, qualification or scientific authority claim.

**Do not suppress legally required safety communication**; instead provide only verified public safety information and obtain the relevant current supplier SDS and compliance review before a consequential offer. A catalogue description is not a substitute for SDS, technical or legal advice.

### May remain public with provenance and correct scope

- Legally verified company identity, registered-office and operational-site distinction, public contact methods.
- Company-level certifications only with authentic certificate, correct holder, valid date and documented scope, never converted into product/batch certification.
- Verified general chemical identity or public reference material, carefully separated from a promise about an RMT supplier product. Cross-substance references must be removed immediately.

### Approval after contact — private, controlled process

1. Receive B2B intended use, target grade/form, quantity, required documentation, destination and timing through the existing protected contact route.
2. Ask the selected supplier to provide current SDS/TDS, where relevant batch-specific CoA, applicable conformity/authorisation evidence and current offer details.
3. Have an appropriate human specialist check CAS/EC/form, product and batch applicability, intended use, legal/safety requirements and validity. Record review provenance securely; *never put customer/supplier files, secrets, contract terms or PII into GitHub*.
4. Provide only evidence-supported offer-specific details privately to the customer. Publishing a durable site-wide fact requires separate public evidence classification, a reviewed field-mapping/manifest, natural EN/HU/DE-AT parity and the normal PR/CI/deploy gates.
5. If no evidence arrives or the expert cannot resolve a conflict, **keep the fact absent from public pages and offers**. Do not auto-fill, equate, recommend substitutes or assert certificates.

## Engineering regressions

- `tools/defer_unverified_supplier_claims.py` is a read-only release guard by default. It checks 381 HTML products plus 4 public product JSON files for the currently approved generic packaging and supplier-document status text. `--apply` was used exactly once on the isolated review branch and is not a normal CI step.
- `tools/audit_copper_oxide_evidence_boundary.py` rejects known zinc-chloride/CuO contamination and unsupported supplier-specific claims for the three affected copper oxide routes.
- Existing product identity, supplier CoA, confidential history, AI claim, SEO, link, browser and responsive tests remain mandatory; none validates all 127 supplier grades or legal adequacy.
- The public master catalogue still contains reference/target chemical information that may require source-level specialist validation. It is *not* an approved offered-material specification. Do not describe all remaining chemistry as independently proven; resolve any high-risk mismatch by removing the public claim or withholding it until verified.
- Do not bypass Cloudflare Worker, Turnstile, CSP, protected form endpoint or the fail-closed product-master write-back to force release.

This policy changes only what RMT publicly asserts; it does **not** establish any customer order, supplier availability, current certification, legal compliance or production deployment.
