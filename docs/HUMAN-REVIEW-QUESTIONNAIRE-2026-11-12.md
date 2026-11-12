# Raw Materials Trade — emberi felülvizsgálati kérdőív

**Dátum:** 2026-11-12  
**Cél:** a nyitott kémiai, üzleti, adatvédelmi, SEO/schema és release-döntések lezárása.

## Kitöltési szabály

Minden választ termékcsaládonként vagy kifejezetten megjelölt termékcsoportra kell megadni. Bizonyíték nélküli adatot nem szabad tényként jóváhagyni. Minden jóváhagyáshoz tartozzon felelős, dátum és forrásdokumentum.

## 1. Felelősség és jóváhagyás

1. Ki jogosult a kémiai termékadatok végleges jóváhagyására?
2. Ki hagyhatja jóvá a Wikidata- és `sameAs`-kapcsolatokat?
3. Ki hagyhat jóvá helyettesíthetőségi állítást?
4. Ki ellenőrzi az SDS/TDS/CoA és megfelelőségi dokumentumokat?
5. Ki hagyhatja jóvá a publikus kereskedelmi állításokat?
6. Ki végzi a GDPR- és adatvédelmi végső ellenőrzést?
7. Milyen dokumentum tekinthető hiteles jóváhagyási bizonyítéknak?
8. Kötelező-e a jóváhagyó neve, dátuma és forráslinkje?
9. Mennyi ideig érvényes egy jóváhagyás?
10. Ki indít újraellenőrzést beszállító- vagy specifikációváltozáskor?

## 2. Termékazonosítás

Minden termékhez válaszolandó:

1. Mi a hivatalos szabványos terméknév és mely szinonimák publikálhatók?
2. Mi a helyes CAS- és EC-szám, és ugyanarra a formára vonatkoznak-e?
3. Mi a helyes kémiai képlet és molekulatömeg?
4. Mi a fizikai forma: por, pehely, granulátum, folyadék, oldat vagy keverék?
5. Van-e hidratációs állapot: vízmentes, mono-, di-, penta- vagy más hidrát?
6. Tiszta anyag vagy keverék a termék?
7. Ha keverék, jogszerű-e egyetlen CAS-t és képletet megadni?
8. A terméknévben szereplő forma és koncentráció bizonyított adat-e?
9. Mely mezők biztosak, feltételesek vagy hiányzóak?
10. Mely SDS, TDS, CoA vagy hivatalos adatlap támasztja alá az értéket?
11. Publikálható-e az adat HTML-ben és JSON-LD-ben?

## 3. Wikidata és `sameAs`

Minden Wikidata-jelöltnél:

1. Ugyanazt az anyagot, hidratációs állapotot, koncentrációt és fizikai formát jelöli-e az entitás?
2. Ugyanazt az oldatot vagy keveréket jelöli-e?
3. Van-e CAS-egyezésen kívüli független bizonyíték?
4. A Wikidata címkéje, leírása és a Wikipedia-link megfelel-e a terméknek?
5. Használható-e a kapcsolat gépi `sameAs` értékként, vagy csak látható külső forráslinkként?
6. Ha nem hagyható jóvá, maradjon-e `needs-confirmation`?
7. Ki, mikor és milyen forrás alapján hagyta jóvá?
8. Jóváhagyható-e egy QID több, eltérő formájú termékhez, és milyen korlátozással?

CAS-egyezés önmagában nem elegendő `sameAs` jóváhagyásához.

## 4. Hiányzó kémiai adatok

1. Pótolható-e a molekulatömeg, tisztaság, EC-szám, képlet és anyagforma hivatalos forrásból?
2. Termékszintű vagy csak tételszintű adat-e a tisztaság?
3. Van-e adat, amely csak beszállítói visszaigazolással adható meg?
4. Mi legyen a publikus szöveg hiányzó adat esetén?
5. Használható-e az „egyeztetés alapján” megfogalmazás?
6. A JSON-LD-ben `null`, üres mező vagy teljes elhagyás legyen?
7. Mely adatok minősülnek kereskedelmi titoknak vagy tételspecifikus adatnak?

## 5. Koncentráció, minőség és forma

Minden jelenlegi `concentration` értéknél döntendő:

1. Valódi koncentrációról van-e szó, és mi az egysége?
2. A `Technical`, `Food grade`, `Feed grade` vagy `pharmaceutical grade` minőség-e?
3. A `monohydrate`, `anhydrous` vagy `heptahydrate` hidratációs állapot-e?
4. A `solution`, `flakes`, `powder`, `light` vagy `dense` fizikai forma-e?
5. A `regenerated` technológiai vagy minőségi megjegyzés-e?
6. A `0–3 mm`, `3–8 mm` vagy mesh szemcseméret-e?
7. Szükséges-e `grade`, `concentration`, `physical_form`, `hydrate_state`, `particle_size`, `process_note`, `purity` vagy `molecular_weight` mező?
8. Mely adat jelenjen meg title-ben, H1-ben, meta descriptionben és JSON-LD-ben?
9. Minden nyelven azonos jelentésű-e a mezőszerkezet?

## 6. Dokumentumok és megfelelőség

1. Mely termékekhez létezik aktuális SDS, TDS és CoA?
2. A CoA mindig tétel- és gyártófüggő-e?
3. Publikálható-e dokumentumletöltési link?
4. Ha nincs publikus dokumentum, milyen feltételes szöveg jelenjen meg?
5. Mikor szükséges SDS, TDS, CoA vagy egyéb megfelelőségi dokumentum?
6. Mely állítások csak „kérésre” vagy „egyeztetés alapján” használhatók?
7. Szerepelhet-e ADR-információ publikus oldalon?
8. Ki ellenőrzi a dokumentum aktuális verzióját és mikor kell újraellenőrizni?
9. Tilos-e a „compliant”, „certified” vagy „approved” állítás bizonyíték nélkül?

## 7. Csomagolás és logisztika

1. Milyen csomagolás ténylegesen elérhető: zsák, BigBag, IBC, hordó, raklap vagy ömlesztett forma?
2. Mi kötelező és mi csak lehetséges opció?
3. Megadható-e standard csomagolási méret?
4. Változik-e a csomagolás beszállító vagy régió szerint?
5. Megadható-e MOQ, készlet vagy szállítási idő?
6. Megadható-e FCA, DAP, DDP vagy más Incoterm?
7. Mely országokba és régiókba szállítható?
8. Milyen ADR- vagy vámkorlátozást kell feltüntetni?
9. Milyen adatokat kell bekérni ajánlatkéréskor?

## 8. Helyettesíthetőség és alternatívák

Minden jelölt párnál:

1. Ugyanarra az alkalmazásra használható-e, vagy csak kémiailag hasonló?
2. Azonos koncentráció, tisztaság és fizikai forma mellett használható-e?
3. Van-e jogi, biztonsági vagy technológiai korlát?
4. Szükséges-e próba, validáció vagy vevői jóváhagyás?
5. Szükséges-e új SDS, TDS vagy CoA?
6. Ki hagyja jóvá az alternatívát?
7. „Related product” vagy tényleges alternatíva legyen-e a publikus besorolás?
8. Használható-e a „drop-in replacement” kifejezés?

Ha a bizonyíték nem elegendő, a publikus szöveg legyen:

> Lehetséges alternatíva csak az alkalmazás, minőségi követelmény és dokumentáció ellenőrzése után.

## 9. Vevői ajánlatkérés

1. Kötelező-e az anyag, CAS, felhasználás, iparág, minőség, koncentráció, tisztaság, forma, mennyiség, csomagolás, szállítási hely és kívánt időpont?
2. Megadható-e egyszeri vagy rendszeres igény?
3. Megadható-e SDS/TDS/CoA-igény?
4. Elfogadható-e alternatív anyag?
5. Milyen adatot nem szabad bekérni vagy megjeleníteni?
6. Mennyi ideig őrzik meg az ajánlatkérési adatokat, mi a jogalap és milyen nyelven válaszolnak?

## 10. GDPR, privacy és nyilvános adatok

1. Mely kapcsolattartói adatok és személynevek publikálhatók?
2. Mely beszállítói és partneri nevek tilosak?
3. Mely e-mail-címek és telefonszámok publikus céges adatok?
4. Mely adatok tilosak `llms.txt`-ben, JSON-LD-ben, sitemapben vagy HTML-ben?
5. A privacy audit találatai közül melyek céges adatok, belső adatok, bizalmas adatok vagy hamis pozitívok?
6. Szükséges-e bármely adat Git-historyból való eltávolítása, és van-e ehhez jóváhagyás?
7. Mely cookie-k és analitikai kódok töltődnek be hozzájárulás előtt?
8. Újranyitható-e a cookie-beállítás, mely harmadik felek kapnak adatot, és van-e mindhárom nyelven tájékoztató?

## 11. SEO, schema és LLM

1. Mely terméknevek és szinonimák legyenek elsődleges keresési kifejezések?
2. Minden FAQ-válasz ténylegesen látható-e az oldalon?
3. Használható-e `FAQPage` schema?
4. Mely oldalaknál indokolt `ChemicalSubstance`, `DefinedTerm` vagy `TechArticle`?
5. Mely műszaki adatok szerepelhetnek JSON-LD-ben bizonyítékkal?
6. Használható-e külső forráslink `sameAs` nélkül?
7. Mely Organization- és személyi adatok publikálhatók?
8. A három nyelvi oldal title-je, meta descriptionje, H1-je és schema-ja paritásos-e?
9. Mely német oldalak igényelnek anyanyelvi lektorálást?

## 12. Release és működtetés

1. Ki hagyja jóvá a végleges release-t?
2. Mely CI-kapuk kötelezőek?
3. Kell-e külön szakmai, kereskedelmi és privacy sign-off?
4. Ki ellenőrzi a live oldalt deploy után?
5. Milyen URL-eket kell smoke-tesztelni?
6. Mi bizonyítja a live és repository verzió azonosságát?
7. Van-e automatikus Cloudflare deploy és ki tud rollbackelni?
8. Mi az előző ismert jó commit?
9. Mikor fut újra a teljes 378 oldalas audit, sitemap/indexelési ellenőrzés?
10. Mikor végezhető el külön az űrlap/Turnstile E2E?

## Kötelező döntési kimenet minden termékhez

```text
identity_status: verified | needs-confirmation | incomplete
sameAs_status: approved | withheld
chemical_data_status: complete | partial | supplier-confirmation-required
form_status: verified | unconfirmed
grade_status: verified | unconfirmed
documentation_status: available | conditional | unavailable
packaging_status: verified | conditional | unavailable
substitution_status: approved | related-only | not-assessed
publication_status: publish | publish-with-caveat | withhold
reviewed_by:
reviewed_on:
source_documents:
follow_up_owner:
follow_up_deadline:
```
