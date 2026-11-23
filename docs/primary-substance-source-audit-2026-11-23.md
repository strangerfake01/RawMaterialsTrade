# RMT primary-source chemical identity audit — 23 November 2026

**Status: limited, evidence-scoped source research; NOT supplier-material, regulatory, legal or live-production approval.**

## Scope, method and distinction

- Reviewed the 127-family canonical catalogue, `entity-registry.json` and the public 369-entry `HANDOFF/SOURCE-REGISTER.csv`. Cross-checked selected identity claims directly against original NLM/PubChem substance pages, ECHA regulatory references and EUR-Lex legal text.
- **13/127 catalogue family entries** now have an independently checked **general chemical-substance reference** (11 distinct substance concepts). The other **114 are still pending source-by-source verification**. No product batch, supplier, offered grade, purity, storage, delivery, SDS/TDS/CoA document or food/feed use is confirmed by this audit.
- The old source register misleadingly showed **120 Wikidata source rows with `verified` status** without human independent evidence: 118 were downgraded, two borax hydrate candidate links were removed; the generic Borax Wikipedia links were also withheld because they do not identify the exact hydrate. **No `ChemicalSubstance.sameAs` approvals** were introduced.
- The PubChem source may describe a molecule, parent salt, ion, hydrate, solution or standardization convention. CAS/EC/name/form/formula must agree *at the same specificity*. Automated `CAS → first CID` matching is unsafe; never promote it into a verified offered material or publish an approximate commercial specification.

## Independently cross-checked general chemical identities

| Canonical family record | General CAS | Correct general PubChem CID | Official source |
|---|---|---:|---|
| L-ascorbic acid | 50-81-7 | 54670067 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/50-81-7) |
| Ammonium sulfate | 7783-20-2 | 6097028 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7783-20-2) |
| Ammonium chloride | 12125-02-9 | 25517 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/12125-02-9) |
| Disodium tetraborate decahydrate | 1303-96-4 | 16211214 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1303-96-4), [ECHA](https://echa.europa.eu/substance-information/-/substanceinfo/100.129.152) |
| Disodium tetraborate pentahydrate | 12179-04-3 | 86341921 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/12179-04-3), [ECHA primary support document](https://chem.echa.europa.eu/api-obligation-list/v1/candidateList/documents?name=db0ecbd7123c0151e83a694bb86e6a9b_svhc_supdoc_disodium_tetraborate_anhydrous_publication_en.pdf) |
| Aqueous ammonia/ammonium hydroxide *general record only* | 1336-21-6 | 14923 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1336-21-6), [ECHA](https://echa.europa.eu/substance-information/-/substanceinfo/100.014.225) |
| Copper(II) oxide, CuO | 1317-38-0 | 164827 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1317-38-0), [EU 2018/1039](https://eur-lex.europa.eu/eli/reg_impl/2018/1039/oj/eng) |
| Glycerol *general record only* | 56-81-5 | 753 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/56-81-5) |
| Sodium hydroxide, flakes inquiry designation | 1310-73-2 | 14798 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1310-73-2) |
| Sodium hydroxide, solution inquiry designation | 1310-73-2 | 14798 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1310-73-2) |
| Sodium bicarbonate, industrial inquiry designation | 144-55-8 | 516892 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/144-55-8) |
| Sodium bicarbonate, food-sector inquiry designation | 144-55-8 | 516892 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/144-55-8) |
| Magnesium sulfate, anhydrous substance concept | 7487-88-9 | 24083 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7487-88-9) |

The reviewed concepts are machine-readable at `docs/primary-substance-research-2026-11-23.json`. Supplier and offered-grade verification status remains **unverified** for all 13; `pubchem_cid` (approved commercial identity) and `sameAs_status=verified` remain unavailable.

## Definite legacy source-link errors removed

The **source register and candidate mapping**, not the supplier's actual batch, contained misassigned compounds:

- Ascorbic acid was mapped to `190531`, a triazine-based organic compound, not vitamin C.
- Ammonium sulfate was mapped to `783`, the hydrogen molecule, not the sulfate salt.
- Ammonium chloride was mapped to `25423` instead of `25517`.
- Borax decahydrate was mapped to `159383`, *trisodium borate*, instead of the decahydrate.
- Borax pentahydrate was mapped to `57347062`, an incompatible decasodium complex, instead of disodium tetraborate pentahydrate.
- Aqueous ammonia was mapped to `222` (ammonia), not an aqueous ammonium-hydroxide reference. **CID 14923 does not authenticate a 24% offer**.
- Sodium hydroxide was mapped to `7303` (an incompatible organic composition) on two product families.
- Sodium bicarbonate was mapped to `767`, a parent carbonic acid concept, on two families.
- Magnesium sulfate was mapped to `1639`, a different organic formula.

The 13 reviewed registry entries now use independently checked **general reference candidates only**. Rejected CID mappings have not been retained as public truth. The current source-register state is intentionally not `verified` for a supplier's product.

## Regulatory source and safety caveats

- [EU 2018/1039](https://eur-lex.europa.eu/eli/reg_impl/2018/1039/oj/eng) includes **3b404 Copper(II) oxide** as a feed additive **subject to conditions**. It does not mean any offered copper oxide grade can be marketed as approved for feed. Check the current [EU Feed Additives Register](https://food.ec.europa.eu/food-safety/animal-feed/feed-additives_en), specific product composition, manufacturer documentation and all applicable requirements before making an offer.
- [ECHA's original disodium tetraborate SVHC supporting evidence](https://chem.echa.europa.eu/api-obligation-list/v1/candidateList/documents?name=db0ecbd7123c0151e83a694bb86e6a9b_svhc_supdoc_disodium_tetraborate_anhydrous_publication_en.pdf) distinguishes CAS `12179-04-3` (pentahydrate), `1303-96-4` (decahydrate), and `1330-43-4` (anhydrous), and sets out serious reproductive-toxicity concerns. This historic primary document is not a substituted 2026 SDS, CLP evaluation or current regulatory-status certificate.
- NaOH `1310-73-2` substantiates the **parent substance only**, not an advertised 48–50% solution; glycerol `56-81-5` does not substantiate 99.5% purity, food grade, pharmacopoeial grade or a particular batch.

## High-priority next verification cases — still UNAPPROVED

The source-formula versus automated candidate comparison raised other substantial mismatches. These are **investigation candidates**, not an asserted total error count:

1. **Calcium chloride**: multiple catalogue forms include anhydrous `10043-52-4` and dihydrate `10035-04-8`; legacy CID `271` denotes a calcium ion, **not CaCl2 or CaCl2·2H2O**. Separate [anhydrous PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/10043-52-4) and [dihydrate PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/6093260) concepts exist. Supplier composition and exact hydrate must be checked before selecting one.
2. **Magnesium chloride hexahydrate**: legacy CID `888` is a magnesium ion, not the hydrate; PubChem [CID 24644](https://pubchem.ncbi.nlm.nih.gov/compound/24644) includes CAS `7791-18-6`, while some depositor records associate a related hydrated concept with a separate CID. Do not choose an offer-specific identity from a single automated hit.
3. **Sodium benzoate**: the salt must not be confused with an isolated benzoate ion; [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/532-32-1) identifies the general sodium salt `517055`.
4. **Nitric acid and hydrochloric acid**: historical candidates point to constituent anions (`943` nitrate, `312` chloride), not the full acids. See [nitric acid CID 944](https://pubchem.ncbi.nlm.nih.gov/compound/7697-37-2) and [hydrochloric acid CID 313](https://pubchem.ncbi.nlm.nih.gov/compound/7647-01-0). No promise of 20/50/60% mixtures, pharmacopoeial grades or batch composition follows from those records.
5. **Mixed hydrate/solution forms** (citric acid, zinc sulfate, copper sulfate, magnesium chloride, EDTA Na2/Na4): multiple hydrated or ionic species may share a parent concept; review form-specific CAS and the supplier's SDS/TDS before publication of a `sameAs` or a purity/grade assertion.

## Publication boundary and acceptance

Public source references can support **general chemical education and product-request identification** only. They cannot establish current RMT supplier details, grade, SDS/TDS/CoA availability, restricted-use compliance or shipment conditions. The default rule is **withhold until reliable proof**, confirm privately after contact and maintain the protected RFQ process. The remaining 114 catalogue families require independent concept-by-concept verification before any reference can be called independently cross-checked; **0/127 supplier offers have been authenticated** in this audit.

The #52 PR remains DRAFT and NOT LIVE until independent real Worker/Turnstile/inbox E2E, legal and chemistry review where applicable, production exact SHA readback and post-release GSC acceptance are complete.
