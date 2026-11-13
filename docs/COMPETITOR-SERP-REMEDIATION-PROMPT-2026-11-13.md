# Raw Materials Trade — magyar SERP-javító prompt

## Cél

A magyarországi ipari vegyianyag-keresésekben a Raw Materials Trade termékoldalai a döntéshez szükséges, bizonyítható információkat adják át gyorsan, három nyelven és ajánlatkérésig vezető úton.

## Kötelező ellenőrzés minden termékoldalon

- terméknév és magyar szakmai szinonimák;
- CAS, EC és képlet, ha az adott anyagnál hitelesen igazolt;
- koncentráció, minőség és fizikai forma;
- tipikus kiszerelés és szállítási régió, csak orientációként, ha a konkrét ajánlat eltérhet;
- alkalmazási területek és felhasználási korlátok;
- SDS/TDS/CoA útvonal;
- mennyiség, célország, csomagolás, határidő és dokumentumigény bekérése;
- MOQ, készlet, Incoterms, ár és tanúsítás csak aktuális, elsődleges bizonyíték alapján;
- helyettesítő termék csak szakmailag indokolt, dokumentum-alapú összevetéssel;
- magyar, angol és német tartalmi paritás;
- canonical, hreflang, JSON-LD, belső linkek és FAQ;
- 5 másodperces érthetőség és mobil olvashatóság.

## Biztonsági szabály

PubChem, Wikipedia, Wikidata vagy általános keresési találat nem igazol aktuális kereskedelmi minőséget, készletet, megfelelőséget vagy tételazonosságot. Ezek csak orientációs források lehetnek. A végleges adatot a kiválasztott beszállító aktuális SDS/TDS/CoA dokumentációja erősíti meg.

## Végrehajtás

1. Futtasd az evidence-depth, procurement-path, internal-link és chemical-search auditokat.
2. Javítsd a hiányzó, alacsony kockázatú döntéstámogató blokkokat mindhárom nyelven.
3. Ne találj ki árat, készletet, MOQ-t, Incoterms-et vagy tanúsítást.
4. Futtasd újra az automatizált ellenőrzéseket.
5. Külön ágon, PR-en és CI-n keresztül merge-eld.
6. A publikáció után ellenőrizd az élő URL-eket, sitemapet és release-manifestet.

## Aktuális végrehajtás

2026-11-13: a glicerin 99,5% EN/HU/DE-AT kiemelt oldalakon bekerült a beszerzési döntéstámogató blokk. A blokk azonosítást, alkalmazást, kereskedelmi adatokat, dokumentumokat és jóváhagyási pontot kezeli, ár- és készletígéret nélkül.
