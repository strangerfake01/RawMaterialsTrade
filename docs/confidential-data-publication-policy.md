# Confidential and restricted data — publication policy

**Default: deny publication.** The public repository, GitHub Actions logs/artifacts, deployed pages, downloads, metadata, structured data, images and commit history are not authorized storage for restricted information.

## Never publish
- Supplier or manufacturer identities and any directly or indirectly identifying sourcing metadata.
- Purchase prices, margins, quotes, contracts, supplier/customer negotiations, internal sourcing terms, bank details or personal contact data.
- Supplier SDS/TDS/CoA originals, nonpublic certificates, batch traceability, customer-specific specifications and internal review records.
- Credentials, access tokens, private URLs, API keys, security configuration secrets and restricted exports.
- Information classified as confidential, restricted or otherwise subject to a nondisclosure obligation, regardless of file format.

## Publication gate
1. **Classify first**: absent explicit authorization, treat unknown business records as restricted.
2. **Minimize**: publish only product facts and approved general statements needed for the buyer; do not publish evidence IDs or source references.
3. **Verify**: a designated authorized reviewer checks both direct and inferential disclosure, legal permission, image/EXIF metadata, generated HTML/JSON-LD and download assets.
4. **Automated checks**: CI runs for every pull request and fails on high-confidence text findings, private records and restricted file formats. CI does not replace human approval.
5. **Release**: do not merge or deploy with open confidentiality blockers. Do not add broad exceptions to silence CI.

## Exposure response
If a secret or confidential record is committed or deployed, stop publication, preserve a restricted incident record, remove live access, assess prior downloads and Git history, revoke compromised credentials, and follow applicable contractual and legal notification duties. Deleting the latest file version does not erase public history.

The two existing GMP+ PDFs remain blocked pending authorized binary inspection and publication-rights verification.
