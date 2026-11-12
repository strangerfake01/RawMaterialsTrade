# Raw Materials Trade – magyarországi pozicionálási audit és háromnyelvű változáscsomag

Dátum: 2026-11-12  
Bizonyossági jelölés: **A** = elsődleges, közvetlenül ellenőrzött forrás; **B** = másodlagos vagy keresési kivonat; **H** = hipotézis, publikálás előtt igazolandó.

## 1. Döntés

**Ajánlott pozicionálás:** dokumentált, többnyelvű B2B vegyipari beszerzési koordinátor közép-európai ipari és ingredient-vevők számára.

Ez nem állít gyártói státuszt, készletet, kizárólagosságot vagy jogi megfelelést. A bizonyítható előny a következő szolgáltatásígéret lehet: a vevő egy specifikációból gyors, dokumentált és többnyelvű ajánlatkérési folyamatot kap, amelyben tisztázott a termékazonosság, grade, koncentráció, csomagolás, célország és szükséges dokumentáció.

### Miért ez a legjobb irány?

- A nagyobb szereplők széles portfóliót és technikai/szolgáltatási infrastruktúrát kommunikálnak: Brenntag iparágakat, értéknövelt supply-chain szolgáltatásokat és digitális dokumentációt; Univar iparági portfóliót és e-commerce funkciókat; IMCD szakosított üzleti csoportokat és technikai kompetenciát; Azelis specialty chemicals/food ingredients fókuszt és technikai-logisztikai szolgáltatást mutat be. [Brenntag Hungary](https://brenntag-pwa-hungary-nuxt3.e-spirit.cloud/en-hu/), [Univar industries](https://www.univarsolutions.com/industries), [IMCD Hungary](https://www.imcd.hu/), [Azelis Hungary](https://www.azelis.com/en/regions-and-locations/emea/hungary) — **A/B**.
- A Raw Materials Trade GSC-adatai alapján jelenleg a főoldal, a HU oldal és egy kénsavoldal adja a mérhető láthatóság magját; a katalógus- és termékoldalakban van bővítési lehetőség — **A**, GSC 2026-10-13–2026-11-09.
- A „trade in raw materials” query 44 megjelenéssel és 11,36-os pozícióval közeli opportunity — **A**, GSC Wizard opportunity scoring; a kattintási upside becslés, nem garancia.

## 2. Pozicionálási alternatívák

| Alternatíva | Célvevő / probléma | Bizonyítható előny | Különbség | Kockázat | Döntés |
|---|---|---|---|---|---|
| Dokumentált B2B beszerzési koordinátor | KKV beszerző, aki specifikációt, dokumentumot és ajánlatot akar gyorsan összeállítani | RMT többnyelvű, dokumentum-orientált RFQ-folyamatot kommunikálhat, ha a tényleges dokumentumkezelés igazolható | szűkebb és érthetőbb, mint a „vegyipari kereskedő” | bizonyíték nélkül csak ígéret | **Ajánlott** |
| Rugalmas közép-európai alapanyag-partner | EU/HU/AT/DE vevő, akinek kisebb vagy változó mennyiség kell | régiós nyelvi és koordinációs előny csak tényleges szállítási/e-mail adatokkal | nem versenyez közvetlenül a globális portfólióval | szállítási régió/MOQ igazolása kell | Másodlagos |
| Többnyelvű speciális vegyianyag-trader | olyan vevő, aki ritkább vagy több grade-ben elérhető terméket keres | a 13 termékből kialakítható termékkönyvtár | termék- és grade-specifikus keresletre épít | trader státuszt és forrásláncot tisztázni kell | Kísérleti |

## 3. Vevői problémák és versenyhézagok

| Probléma | Megfigyelés | RMT-válasz | Bizonyosság |
|---|---|---|---|
| Nem világos, milyen grade kell | A SERP-ekben a grade/concentration/form rendszeresen szerepel | „Küldje el az alkalmazást, mennyiséget, csomagolást és célországot” intake blokk | B + H |
| Nehezen elérhető dokumentum | Versenytársi oldalak gyakran SDS/TDS/CoA CTA-t használnak | dokumentumlista és request gomb; publikus fájl csak ténylegesen aktuális dokumentummal | A/B |
| Lassú ajánlatkérés | A bulk oldalak RFQ-t használnak, de a vevői bemenet sokszor nem részletezett | 6 mezős RFQ-form: termék, grade, mennyiség, pack, destination, deadline | H – mérni kell e-mailben |
| Nyelvi bizonytalanság | HU és DE/AT eltérő terminológiát használ | natív HU/EN/AT-DE oldalazonos tartalommal | B |
| KKV-k kiszolgálása | nagy disztribútorok széles portfóliót kommunikálnak | koordinációs és döntéstámogató folyamat, nem „legnagyobb” claim | H |

## 4. Háromnyelvű üzenetarchitektúra

### Hero

**HU H1:** Dokumentált ipari és élelmiszeripari alapanyag-beszerzés egyértelmű ajánlatkérési folyamattal  
**HU lead:** Adja meg a terméket, minőséget, mennyiséget, csomagolást és célországot. Ellenőrizhető specifikáció alapján egyeztetjük a beszállítói ajánlatot és a szükséges dokumentumokat.

**EN H1:** Documented sourcing for industrial chemicals and ingredients  
**EN lead:** Share the product, grade, quantity, packaging and destination. We coordinate a supplier quotation around the specification and documents required for your purchase decision.

**DE-AT H1:** Dokumentierte Beschaffung von Industriechemikalien und Rohstoffen  
**DE-AT lead:** Teilen Sie Produkt, Qualität, Menge, Verpackung und Lieferort mit. Wir koordinieren ein Lieferantenangebot auf Basis Ihrer Spezifikation und der benötigten Unterlagen.

### CTA

HU: **Ajánlatot kérek specifikáció alapján**  
EN: **Request a specification-based quote**  
DE-AT: **Angebot auf Basis Ihrer Spezifikation anfragen**

### Kötelező döntéstámogató blokk minden termékoldalon

1. Termék és synonymek.
2. CAS / EC / formula, ha ellenőrzött.
3. Grade és koncentráció/purity.
4. Forma és csomagolás.
5. Elérhető dokumentumok: SDS, TDS/spec, CoA — státuszonként.
6. Tipikus alkalmazások, kizárólag ellenőrzött forrásból.
7. Ajánlatkéréshez szükséges adatok.
8. Frissítés dátuma és cégazonosság.

## 5. Kulcsszó- és URL-architektúra

| Klaszter | HU példa | EN példa | DE-AT példa | Oldaltípus |
|---|---|---|---|---|
| általános beszerzés | ipari vegyianyag beszállító | industrial chemical supplier | Industriechemikalien Lieferant | főoldal/kategória |
| dokumentáció | SDS TDS CoA beszállító | chemical supplier SDS TDS CoA | Sicherheitsdatenblatt TDS CoA Lieferant | trust/resource oldal |
| grade | glicerin 99,5 ipari/food | glycerine 99.5 food/industrial | Glycerin 99,5 Lebensmittelqualität | termék/grade |
| koncentráció | kénsav 32 37 50 95 97 | sulfuric acid 32 37 50 95 98 | Schwefelsäure 96 98 | termékvariáns |
| forma/csomagolás | IBC, hordó, ömlesztett | IBC, drums, bulk | IBC, Fass, Tankzug | termék/RFQ |
| régió | beszállító Magyarország | supplier Hungary / EU | Lieferant Österreich | lokalizált landing |

## 6. Implementációs változáslista

### Főoldal

- Hero a fenti három nyelvi változatra.
- 13 termékből indexelhető termékkönyvtár.
- Külön blokkok: industrial chemicals, food/feed ingredients, documentation, sourcing process.
- Rövid „hogyan működik” folyamat: specifikáció → beszállítói egyeztetés → dokumentumellenőrzés → ajánlat.
- Bizonyítható cégadatok és kapcsolat; nem publikálható „global network”, „certified”, „stock available” vagy „manufacturer” állítás ellenőrzés nélkül.

### Termékoldalak

- Egységes chemical identity panel.
- Grade/concentration/form/packaging táblázat.
- SDS/TDS/CoA státuszok.
- 4–6 kérdéses FAQ, amely csak az oldal tényeire hivatkozik.
- RFQ-form és célország-mező.
- Kapcsolódó termékek és iparági oldalak.

### Schema és gépi olvashatóság

- Organization: csak ellenőrzött cégnév, URL, logo, kapcsolat.
- WebPage + BreadcrumbList minden indexelhető oldalon.
- Product csak tényleges termékoldalon; `offers` és `price` csak aktuális, igazolt adatokkal.
- ChemicalSubstance csak akkor, ha a schema-környezet és a site implementáció ténylegesen támogatja.
- FAQPage csak látható, egyező FAQ-tartalommal.
- `llms.txt` és gépi cégprofil: csak dokumentált tényekkel, forráshivatkozással és frissítési dátummal.

### Belső linkelés

- Főoldal → termékkategória → termék → dokumentum/RFQ.
- Blogcikk → pontosan illeszkedő termékoldal, nem általános katalógus.
- Termékoldal → kapcsolódó grade, alkalmazás és beszerzési útmutató.

## 7. Mérés

| Cél | Mérőszám | Forrás | Gyakoriság |
|---|---|---|---|
| organikus láthatóság | impressions, clicks, CTR, position query/page/country szerint | GSC | heti/havi |
| RFQ minőség | qualified RFQ, missing-field rate, response time | form/CRM/e-mail | heti |
| üzleti hatás | quote-to-opportunity, product, destination, grade | CRM | havi |
| tartalom | assisted conversions, product-page engagement | GA4 | havi |
| AI láthatóság | AI referral sessions, cited pages, branded query change | GA4/GSC/LLM log | havi |
| bizalom | dokumentumkérés, visszatérő vevő, consent rate | CRM/form analytics | havi |

## 8. Kockázati és ellenőrzési lista

- Ne publikáljunk készletet, árat vagy MOQ-t élő ellenőrzés nélkül.
- Ne állítsunk megfelelést, tanúsítványt, REACH/ADR/food/feed státuszt dokumentum nélkül.
- A három nyelvi oldal tényállítása legyen azonos; eltérhet a terminológia és a példázás, nem térhet el a termék- vagy szolgáltatásállítás.
- A cégazonosságot, jogi nevet, címet, kapcsolattartót és adatkezelési tájékoztatót elsődleges forrásból kell validálni.
- E-mailes érdeklődési adatok jelenleg nem voltak elérhetők ebben a környezetben; ezért átfedést vagy e-mailes mintát nem állítok.
- Repository, release-audit és deploy nem végezhető el, mert a munkakönyvtárban nincs alkalmazásforrás vagy Git-repository.

## 9. Forrás- és bizonyítéktábla

| Forrás | Téma | Dátum | Szint |
|---|---|---|---|
| [Brenntag Hungary](https://brenntag-pwa-hungary-nuxt3.e-spirit.cloud/en-hu/) | ipari/specialty portfólió, szolgáltatások, magyar jelenlét | 2026-11-12 lekérdezés | A/B |
| [Brenntag corporate](https://corporate.brenntag.com/en/about/) | komplex supply chain, technikai és értéknövelt szolgáltatások | 2026-11-12 lekérdezés | A |
| [Univar industries](https://www.univarsolutions.com/industries) | iparági fókusz és portfólió | 2026-11-12 lekérdezés | A |
| [IMCD Hungary](https://www.imcd.hu/) | specialty chemicals, local knowledge, technical expertise | 2026-11-12 lekérdezés | A |
| [IMCD products](https://www.imcd.hu/our-products) | üzleti csoportok és iparágak | 2026-11-12 lekérdezés | A |
| [Azelis Hungary](https://www.azelis.com/en/regions-and-locations/emea/hungary) | magyar jelenlét, logistics, technical support | 2026-11-12 lekérdezés | A |
| [Raw Materials Trade GSC report](./raw-materials-trade-serp-audit-2026-11-12.md) | saját teljesítmény, oldalak, opportunity, cannibalization | 2026-11-12 | A |

## 10. Implementációs státusz

**Elkészült:** audit, pozicionálási döntés, három alternatíva, háromnyelvű üzenetarchitektúra, kulcsszó- és URL-architektúra, változáslista, mérési terv, kockázati lista.

**Nem hajtható végre jelenleg:** repository-módosítás, release-auditok futtatása, commit, push, deploy és éles URL-ellenőrzés. Ennek oka, hogy a megadott munkakönyvtárban nincs weboldalforrás vagy Git-repository.
