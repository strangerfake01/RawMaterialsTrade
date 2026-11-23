# RMT primary-source chemical identity audit — 23 November 2026

**Status: limited, evidence-scoped source research; NOT supplier-material, regulatory, legal or live-production approval.**

## Scope, method and distinction

- Reviewed the 127-family canonical catalogue, `entity-registry.json` and the public 369-entry `HANDOFF/SOURCE-REGISTER.csv`. Cross-checked selected identity claims directly against original NLM/PubChem substance pages, ECHA regulatory references and EUR-Lex legal text.
- **57/127 catalogue family entries** now have an independently checked **general chemical-substance reference** (46 distinct general PubChem concepts). The other **70 are still pending source-by-source verification**. No product batch, supplier, offered grade, purity, storage, delivery, SDS/TDS/CoA document or food/feed use is confirmed by this audit.
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

The reviewed concepts are machine-readable at `docs/primary-substance-research-2026-11-23.json`. Supplier and offered-grade verification status remains **unverified** for all 57; `pubchem_cid` (approved commercial identity) and `sameAs_status=verified` remain unavailable.

## Second and third source-review batches — 44 additional catalogue families

The following entries were inspected against the cited **NIH/NLM PubChem general compound records**, using their CAS, compound name and molecular formula. A parent chemical formula does not verify a particular solution strength, salt density, regenerated source, bulk purity, available grade, feed/food authorization or manufacturer. **No commercial grade was approved.**

| Catalogue family (public request ID) | General substance CAS | PubChem CID | Source |
|---|---|---:|---|
| `aceton-technikai-regeneralt-industrial` | 67-64-1 | 180 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/67-64-1) |
| `etkezesi-so-food` | 7647-14-5 | 5234 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7647-14-5) |
| `sotabletta-industrial` | 7647-14-5 | 5234 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7647-14-5) |
| `utszoro-so-deicing` | 7647-14-5 | 5234 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7647-14-5) |
| `vakuum-so-industrial` | 7647-14-5 | 5234 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7647-14-5) |
| `metanol-technikai-regeneralt-industrial` | 67-56-1 | 887 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/67-56-1) |
| `monoetilen-glikol-industrial` | 107-21-1 | 174 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/107-21-1) |
| `monopropilenglikol-industrial` | 57-55-6 | 1030 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/57-55-6) |
| `izopropil-alkohol-technikai-regeneralt-industrial` | 67-63-0 | 3776 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/67-63-0) |
| `hidrogen-peroxid-35-50-60-industrial` | 7722-84-1 | 784 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7722-84-1) |
| `kensav-32-37-50-9597-industrial` | 7664-93-9 | 1118 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7664-93-9) |
| `monoetanolamin-industrial` | 141-43-5 | 700 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/141-43-5) |
| `glicin-industrial` | 56-40-6 | 750 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/56-40-6) |
| `butil-glikol-industrial` | 111-76-2 | 8133 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/111-76-2) |
| `ecetsavanhidrid-industrial` | 108-24-7 | 7918 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/108-24-7) |
| `ciklohexanon-industrial` | 108-94-1 | 7967 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/108-94-1) |
| `karbamid-ipari-kezeletlen-industrial` | 57-13-6 | 1176 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/57-13-6) |
| `kalium-hidroxid-oldat-21-45-4850-industrial` | 1310-58-3 | 14797 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1310-58-3) |
| `kalium-hidroxid-pikkelyes-industrial` | 1310-58-3 | 14797 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1310-58-3) |
| `magnezium-oxid-feed` | 1309-48-4 | 14792 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1309-48-4) |
| `magnezium-oxid-nehez-industrial` | 1309-48-4 | 14792 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1309-48-4) |
| `cink-oxid-industrial` | 1314-13-2 | 14806 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/1314-13-2) |
| `cink-klorid-feed` | 7646-85-7 | 5727 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7646-85-7) |
| `cink-klorid-vizmentes-industrial` | 7646-85-7 | 5727 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7646-85-7) |
| `borsav-industrial` | 10043-35-3 | 7628 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/10043-35-3) |
| `ioncserelt-viz-industrial` | 7732-18-5 | 962 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7732-18-5) |
| `maleinsav-industrial` | 110-16-7 | 444266 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/110-16-7) |
| `aluminium-szulfat-03-mm-38-mm-industrial` | 10043-01-3 | 24850 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/10043-01-3) |
| `aluminium-szulfat-oldat-industrial` | 10043-01-3 | 24850 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/10043-01-3) |
| `ammonium-nitrat-industrial` | 6484-52-2 | 22985 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/6484-52-2) |
| `borken-food` | 16731-55-8 | 28019 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/16731-55-8) |
| `butil-diglikol-industrial` | 112-34-5 | 8177 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/112-34-5) |
| `dietilen-glikol-industrial` | 111-46-6 | 8117 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/111-46-6) |
| `natrium-karbonat-konnyu-industrial` | 497-19-8 | 10340 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/497-19-8) |
| `natrium-karbonat-nehez-industrial` | 497-19-8 | 10340 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/497-19-8) |
| `foszforsav-75-85-food` | 7664-38-2 | 1004 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7664-38-2) |
| `foszforsav-75-industrial` | 7664-38-2 | 1004 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7664-38-2) |
| `kalcium-karbonat-food` | 471-34-1 | 10112 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/471-34-1) |
| `kalium-karbonat-industrial` | 584-08-7 | 11430 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/584-08-7) |
| `etil-acetat-technikai-regeneralt-industrial` | 141-78-6 | 8857 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/141-78-6) |
| `natrium-szulfat-industrial` | 7757-82-6 | 24436 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7757-82-6) |
| `kalium-jodid-feed` | 7681-11-0 | 4875 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/7681-11-0) |
| `propionsav-99-feed` | 79-09-4 | 1032 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/79-09-4) |
| `butanol-industrial` | 71-36-3 | 263 | [NIH PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/71-36-3) |

Two wrong automatic candidate links were replaced by verified general references in this batch: `ciklohexanon-industrial` **7966 → 7967** (cyclohexanol vs. cyclohexanone), and `maleinsav-industrial` **723 → 444266** (maleic acid). Links remain general-substance evidence and are **not** approved `sameAs` identifiers for a commercial offered variant.

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

The 57 reviewed registry entries now use independently checked **general reference candidates only**. Rejected CID mappings have not been retained as public truth. The current source-register state is intentionally not `verified` for a supplier's product.

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

## Rejected candidate quarantine — 14 additional catalogue family records

The further formula/species screen detected and **removed** 14 unsafe legacy PubChem candidate links from the public research register and from the unapproved `entity-registry.json` candidate fields. No replacement molecule or supplier material was asserted. The rejected groups were: calcium chloride (3), magnesium chloride (2), sodium benzoate (1), nitric acid (1), hydrochloric acid (2), zinc sulfate with hydrate variants (2), copper chloride dihydrate (1), potassium iodate (1), and elemental sulfur (1).

For these records the old candidate IDs often represented free Ca²⁺/Mg²⁺/Cl⁻/NO₃⁻/benzoate ions, an anhydrous salt without hydration, or an unrelated organic molecule. The `pubchem_candidate_cid` and `pubchem_candidate_formula` fields are now `null`, and their old source-register rows have `RejectedCandidate`, no misleading URL and explicit non-approval status. This is **not** proof of the correct alternative or of offered material; each remains among the 70 pending family entries. Source examples: [CaCl2](https://pubchem.ncbi.nlm.nih.gov/compound/10043-52-4) versus [CaCl2·2H2O](https://pubchem.ncbi.nlm.nih.gov/compound/6093260); [MgCl2·6H2O](https://pubchem.ncbi.nlm.nih.gov/compound/24644); [sodium benzoate](https://pubchem.ncbi.nlm.nih.gov/compound/532-32-1); [nitric acid](https://pubchem.ncbi.nlm.nih.gov/compound/7697-37-2); [hydrochloric acid](https://pubchem.ncbi.nlm.nih.gov/compound/7647-01-0). No solution strength or grade has been approved.

The permanent `tools/audit_primary_source_research.py` CI gate now checks the quarantined candidate entries, the absent wrong source URLs, the 57 independently source-reviewed general concepts and their retained `supplier_evidence_status=unverified`.

## Important primary-source conflict: copper(II) chloride dihydrate

Even *two PubChem records associated with CAS 10125-13-0* are not interchangeable. [CID 16219111](https://pubchem.ncbi.nlm.nih.gov/compound/16219111) is labelled "Copper Chloride Dihydrate", but displays a single-water-unit computed formula `Cl2CuH2O` and molecular mass **152.46 g/mol**, inconsistent with **dihydrate**. Another [PubChem record, CID 61482](https://pubchem.ncbi.nlm.nih.gov/compound/61482), explicitly identifies `CuCl2·2H2O` as **170.48 g/mol**, and [ECHA CAS 10125-13-0](https://poisoncentres.echa.europa.eu/el/web/guest/substance-information/-/substanceinfo/100.129.663?_disssubsinfo_WAR_disssubsinfoportlet_substanceId=100.129.663) states "copper(2+) chloride hydrate (1:2:2)". This means the familiar CAS and compound-page title **alone** do not justify promoting one CID to a reviewed product `sameAs`.

**Decision: keep `rez-klorid-dihidrat-industrial` quarantined, do not publish a PubChem CID as a product-equivalent identifier, and request exact hydrate/form plus supplier SDS/TDS/CoA when an enquiry arrives.** This is a concrete example why automated CAS lookups, PubChem synonyms and formula mismatches require source-level adjudication.

## Publication boundary and acceptance

Public source references can support **general chemical education and product-request identification** only. They cannot establish current RMT supplier details, grade, SDS/TDS/CoA availability, restricted-use compliance or shipment conditions. The default rule is **withhold until reliable proof**, confirm privately after contact and maintain the protected RFQ process. The remaining 70 catalogue families require independent concept-by-concept verification before any reference can be called independently cross-checked; **0/127 supplier offers have been authenticated** in this audit.

The #52 PR remains DRAFT and NOT LIVE until independent real Worker/Turnstile/inbox E2E, legal and chemistry review where applicable, production exact SHA readback and post-release GSC acceptance are complete.
