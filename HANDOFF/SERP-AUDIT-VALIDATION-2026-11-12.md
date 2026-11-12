# SERP-audit validálás és végrehajtási döntés

**Dátum:** 2026-11-12  
**Hatókör:** a csatolt `raw-materials-trade-serp-audit-2026-11-12.md`, GSC 2026-08-01–2026-11-10, valamint a 90 napos üzleti e-mail keresletjelzések.

## Rövid döntés

A csatolt SERP-audit használható versenytársi szerkezeti hipotézisekhez, de nem használható stabil országos rangsor vagy piaci részesedés bizonyítékaként. A jelentés ezt helyesen jelzi: a legtöbb találati pozícióhoz nincs reprodukálható ország-, eszköz-, idő- és teljes SERP-export.

A weboldalon ezért csak az alábbi, egymással összhangban álló jeleket kezeljük prioritásként:

- **GSC:** salétromsav, kénsav, foszforsav, hidrogén-peroxid, nátrium-hidroxid, glicerin, propionsav, nátrium-perszulfát és síkosságmentesítő oldalak adnak mérhető láthatóságot;
- **e-mailek:** nátrium-karbonát, nátrium-hidrogén-karbonát, kalcium-klorid, foszforsav, karbamid, citromsav, réz/cink és nátrium-hidroxid mutatnak üzleti érdeklődést;
- **SERP-minta:** CAS/képlet, minőség vagy koncentráció, forma, csomagolás, SDS/TDS/CoA, alkalmazási kontextus és ajánlatkérési út a visszatérő beszerzői információs minta.

## Bizonyíték- és eltérésvizsgálat

| Állítás vagy jel | Ellenőrzés | Döntés |
|---|---|---|
| A SERP-ben a dokumentum- és specifikációs mezők erősek | Több terméknél ismétlődő szerkezeti megfigyelés; nem minden sorhoz teljes SERP-export | Elfogadható szerkezeti input |
| Stabil országos top-rangsorok | A jelentés több helyen `nem igazolt` státuszt ad | Nem publikálható tényként |
| HU kénsav top10-közeli oldal | GSC-ben megerősített, de a különböző időablakok miatt az értékeket mindig időszakkal együtt kell idézni | Monitorozandó opportunity |
| EN glicerin 99,5% romló pozíciója | GSC-ben láthatóság van, de a teljesítmény időablak- és lekérdezésfüggő | Prioritásos frissítés, rangsorígéret nélkül |
| Email és GSC azonos termékprioritása | Foszforsav és nátrium-hidroxid közös jel; a többi adatforrás eltérő szándékot mér | Keresztforrásos prioritás csak az átfedésnél |
| Versenytársi kereskedelmi állítások | Más oldalak készlet-, MOQ-, ár-, gyártó- vagy megfelelőségi állításai nem RMT-bizonyítékok | Nem másolható át |

## Implementált állapot

A jelenlegi termékoldal-sablon már tartalmazza a SERP-ben megfigyelt és RMT által hitelesen vállalható információs elemeket: azonosítás, CAS/EK/képlet ahol ismert, minőség/koncentráció, kiszerelés-orientáció, alkalmazási kontextus, SDS/TDS/CoA státusz, ajánlatkérési checklist, döntéstámogató blokk, FAQ és dokumentum-alapú megfelelőségi figyelmeztetés.

A GSC- és piaci-monitoringgal összhangban a 14 kiemelt termékcsalád három nyelvű oldalain már szerepel a bizonyíték-korlátozott `Piaci figyelési háttér` blokk. Ez nem állít keresletet, árat, készletet vagy elérhetőséget, ezért nem alakít át piaci hírt ellenőrizetlen termékállítássá.

Új, nem ellenőrzött készlet-, MOQ-, ár-, szállítási, gyártói vagy szabályozási állítást nem vezetünk be. A blog külső Blogger-rendszerben marad; a repo-oldali tudásindex és a belső termékoldali kapcsolatok kezelik a gépi feldolgozhatóságot, a Blogger admin-oldali canonical/schema/language módosítás külön külső kiadási feladat.

## Következő mérési kapuk

1. A frissítés dátumától legalább 28 napig külön mérjük a három nyelvű URL-eket és a termék-/dokumentum-/beszerzési lekérdezéseket.
2. A GSC-ben oldalszintű kattintás, megjelenés, CTR és pozíció alapján döntünk; 1–2 megjelenéses mintából nem általánosítunk.
3. Az e-mail termékcsoportoknál az ismétlődő, egyedi érdeklődéseket különítjük el a levélszál- és kifejezésátfedésektől.
4. Új nyilvános állítás csak elsődleges vagy beszállítói dokumentummal, URL-lel, dátummal és termékazonosítóval kerülhet a termékoldalra.

## Release-ellenőrzés

Ezt a döntési dokumentumot a release-kapu részeként kell megőrizni. A kiadás feltételei: `audit_release_contract`, termékparitás, kémiai forrásintegritás, publikus kémiai identitás, AI-claim, procurement path, belső link, statikus asset és sitemap audit hibamentes futása.
