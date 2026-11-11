# RMT — full catalogue identity and semantics screening (2026-11-08)

**Scope:** all 126 records in `products-multilingual.json`; multilingual site has 378 product routes. This is a deterministic **catalogue-field screening**, not an external SDS/REACH/PubChem verification or full human review of all translated prose.

## Results

- 126/126 catalogue entries inspected.
- 70/126 English `technical_identity.concentration_en` values lack a numerical concentration unit; many represent grade, hydrate, particle size or physical form. **Requires semantic field repair**, not invented percentage.
- 13/126 CAS fields contain multiple CAS values or explanatory placeholders. The catalogue must distinguish a multi-form material from an unknown identifier. **Do not publish such fields as one certified CAS.**
- 3/126 CAS fields are explicitly descriptive placeholders rather than identifiers: `kalium-tripolifoszfat-food`, `trilon-industrial`, `vitamin-a-b1-b12-b5-b6-c-d3-e-h-k3-feed`.
- `citromsav-monohidrat-anhidrat-food` combines anhydrous and monohydrate forms; source catalogue formula currently lists only `C₆H₈O₇`, although the hydrated form is `C₆H₈O₇·H₂O`. Public localized pages were corrected previously; source catalogue still requires synchronization.
- Existing GitHub Actions static release and catalogue parity gates passed on commit `bfaea94bfd80e91ab89c3c27c476c6831245f332`, but these **do not establish chemical truth**.
- Independent supplier-grade evidence (SDS/TDS/CoA) remains unavailable in the current product-depth report; no chemical grade or regulatory claim can be certified from these fields alone.

## Nonquantitative concentration candidates (70)

- `aceton-technikai-regeneralt-industrial`
- `aluminium-szulfat-03-mm-38-mm-industrial`
- `aluminium-szulfat-oldat-industrial`
- `ammonium-klorid-industrial`
- `ammonium-szulfat-industrial`
- `aszkorbinsav-food`
- `borax-dekahidrat-industrial`
- `borax-pentahidrat-industrial`
- `borkosav-l-food`
- `borsav-industrial`
- `butil-glikol-industrial`
- `ciklohexanon-industrial`
- `cink-klorid-feed`
- `cink-klorid-vizmentes-industrial`
- `cink-oxid-industrial`
- `cink-szulfat-monohidrat-feed`
- `cink-szulfat-monohidrat-heptahidrat-industrial`
- `citromsav-monohidrat-anhidrat-food`
- `dietilen-glikol-industrial`
- `ecetsavanhidrid-industrial`
- `edta-na2-na4-industrial`
- `etil-acetat-technikai-regeneralt-industrial`
- `etkezesi-so-food`
- `glicin-industrial`
- `izopropil-alkohol-technikai-regeneralt-industrial`
- `kalium-ferrocianid-food`
- `kalium-hidroxid-pikkelyes-industrial`
- `karbamid-ipari-kezeletlen-industrial`
- `kenpor-industrial`
- `magnezium-karbonat-konnyu-nehez-industrial`
- `magnezium-klorid-hexahidrat-industrial`
- `magnezium-oxid-feed`
- `magnezium-oxid-nehez-industrial`
- `magnezium-szulfat-industrial`
- `maleinsav-industrial`
- `mangan-ii-szulfat-monohidrat-industrial`
- `mangan-klorid-monohidrat-tetrahidrat-industrial`
- `mangan-szulfat-monohidrat-feed`
- `metanol-technikai-regeneralt-industrial`
- `monoetanolamin-industrial`
- `monoetilen-glikol-industrial`
- `monopropilenglikol-industrial`
- `natrium-acetat-vizmentes-3h2o-industrial`
- `natrium-benzoat-gran-food`
- `natrium-hidrogen-karbonat-industrial`
- `natrium-hidrogen-karbonat-szodabikarbona-food`
- `natrium-hidroxid-mikrogyongy-pikkelyes-industrial`
- `natrium-karbonat-konnyu-industrial`
- `natrium-karbonat-nehez-industrial`
- `natrium-metabiszulfit-natrium-piroszulfit-industrial`
- `natrium-metaszilikat-industrial`
- `natrium-molibdat-feed`
- `natrium-perkarbonat-industrial`
- `natrium-szulfat-industrial`
- `natrium-tripolifoszfat-industrial`
- `natronvizuveg-oldatok-industrial`
- `rez-klorid-dihidrat-industrial`
- `rez-szulfat-pentahidrat-industrial`
- `sosav-gyogyszerkonyvi-food`
- `sosav-technikai-regeneralt-industrial`
- `sotabletta-industrial`
- `tiokarbamid-industrial`
- `trietilen-glikol-industrial`
- `trinatrium-citrat-industrial`
- `trinatrium-foszfat-dodekahidrat-vizmentes-industrial`
- `utszoro-so-deicing`
- `vakuum-so-industrial`
- `vas-ii-szulfat-monohidrat-feed`
- `vas-ii-szulfat-monohidrat-heptahidrat-industrial`
- `vitamin-a-b1-b12-b5-b6-c-d3-e-h-k3-feed`

## Multi-value or non-CAS identifier fields (13)

- `cink-szulfat-monohidrat-feed`: `7446-19-7 / 7446-20-0`
- `cink-szulfat-monohidrat-heptahidrat-industrial`: `7446-19-7 / 7446-20-0`
- `citromsav-monohidrat-anhidrat-food`: `77-92-9 / 5949-29-1`
- `edta-na2-na4-industrial`: `6381-92-6 / 64-02-8`
- `kalcium-klorid-2025-oldat-deicing`: `10043-52-4 / 10035-04-8`
- `kalcium-klorid-7780-food`: `10043-52-4 / 10035-04-8`
- `kalcium-klorid-dihidrat-7880-pikkelyes-deicing`: `10043-52-4 / 10035-04-8`
- `kalium-tripolifoszfat-food`: `Product-specific — confirm exact CAS/component identity from SDS/TDS`
- `mangan-klorid-monohidrat-tetrahidrat-industrial`: `7773-01-5 / 13446-34-9`
- `mangan-klorid-tetrahidrat-feed`: `7773-01-5 / 13446-34-9`
- `natrium-acetat-vizmentes-3h2o-industrial`: `127-09-3 / 6131-90-4`
- `trilon-industrial`: `Product type-specific — confirm exact CAS/component identity from SDS/TDS`
- `vitamin-a-b1-b12-b5-b6-c-d3-e-h-k3-feed`: `Composition-dependent — confirm exact CAS/component identity from SDS/TDS`

## Acceptance boundary

Each of 378 localized pages requires: canonical identity and exact grade/form; verified or explicitly provisional CAS/EC/formula; EN/HU/DE semantic parity; no unsupported SDS/TDS/CoA, food/feed/pharma, packaging, stock, price or certification promises. Unverified fields remain orientation only. This inventory **does not claim that all 378 pages have been individually fact-checked**.
