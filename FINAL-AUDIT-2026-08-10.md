# Raw Materials Trade — végleges audit és javítási összefoglaló

Dátum: 2026-08-10  
Kiindulás: teljes weboldal ZIP + Claude által készített PSI-javítócsomag  
Cél: a PageSpeed/Lighthouse hibák javítása mellett a teljes EN / HU / DE-AT oldal SEO-, GEO/answer-engine-, LLM-, schema-, hozzáférhetőségi és terméktartalmi megerősítése, emberi hangvétellel.

## 1. Claude csomagjának értékelése

A Claude-csomag a 2026-08-10-i PageSpeed képernyőképeken látható **közvetlen technikai hibák nagy részét jól célozta**:

- `llms.txt`: valódi Markdown-linkek és rendezett szerkezet;
- Cloudflare Turnstile / általános `div aria-label` probléma: szemantikailag megengedett `role="group"`;
- címsor-sorrend: a hibás `h4` ugrások megszüntetése;
- kontraszt: a világos háttéren gyenge színek AA-közeli/AA-kompatibilis sötétebb tokenekre cserélése;
- csak színnel jelölt linkek: aláhúzás és fókuszállapot;
- `prefers-reduced-motion` és billentyűzetfókusz;
- csapatfotókhoz 400 px-es WebP variáns és `srcset`;
- domain- és bloghivatkozások egységesítése.

**A tágabb kérés azonban csak részben volt lefedve.** A Claude-csomag nem építette át elég mélyen a 378 termékoldal szövegét, a három nyelv termékadatait, a kapcsolódó termékek logikáját, az egész site entitásgráfját és az AI-nak szánt kanonikus cégadatokat. Ezeket a végleges körben kiegészítettem.

## 2. A végleges körben elvégzett fő javítások

### 378 termékoldal — EN / HU / DE-AT

- Mind a 126 termékcsalád három nyelvi oldala újra lett szinkronizálva a strukturált katalógusadatokkal.
- A keresőmotoroknak szóló, gépies mondatok helyett természetes, B2B beszerzőnek is értelmes szövegek kerültek a leadekbe, beszerzési blokkokba és CTA-kba.
- A termékoldalak önálló kontextust adnak: terméknév, CAS/EC, képlet ahol rendelkezésre áll, minőség/koncentráció, kiszerelés, tipikus alkalmazások, beszerzési információ, dokumentációs keret, tárolási/szabályozási figyelmeztetés és kapcsolódó alapanyagok.
- Nem kerültek be kitalált árak, készletállapotok, értékelések vagy beszállítói tények.
- A `Product` / `Offer` schema mesterséges használata helyett a vegyi entitások `ChemicalSubstance`, a nem egyértelmű családok `DefinedTerm` típust kapnak.
- A kapcsolódó termékek nem ugyanazt a sablonlistát ismétlik: 126 termékből nyelvenként 124 egyedi kapcsolódó-link készlet lett, szemantikai hasonlóság és kategória alapján.
- Az idegen nyelvű szinonimák megmaradtak az entitásfeloldás miatt, de explicit `lang` jelöléssel szerepelnek.

### Nyelvi adatminőség

- A német alkalmazási mezőkből az angol maradványok ki lettek tisztítva.
- A magyar, angol és német minőség-, kiszerelés-, koncentráció- és szinonimamezők külön lokalizált mezőket kaptak a többnyelvű JSON-ban.
- Több hibás vagy félrevezetően vegyes terméknév korrigálva lett, például EDTA Na2/Na4, kénpor, ioncserélt víz, kálium-tripolifoszfát és trinátrium-foszfát dodekahidrát.
- A termékoldalak látható főtartalma jelenleg jellemzően kb. 500–750 szó/oldal, nyelvtől és anyagtól függően.

### SEO / hreflang / indexelési struktúra

- 126/126 termékoldal mindhárom nyelven jelen van.
- Canonical és hreflang hálózat ellenőrizve; hibás nyelvi készlet nincs.
- `x-default` megmaradt a megfelelő oldalakon.
- Belső linkek ellenőrizve: nincs hiányzó lokális cél.
- Oldalcímek és meta descriptionök hossza a statikus auditban rendben van.
- `sitemap.xml`: 399 publikált/indexelendő URL, mind `2026-08-10` lastmod értékkel, hiányzó lokális cél nélkül.
- A noindex oldalak (privacy, impressum, AI segédprofilok, 404, redirect csonkok) szándékosan nincsenek a sitemapben.

### Schema / entitásgráf

A tartalmi HTML-oldalakon egységes cégentitás szerepel:

- `Organization`: 404 oldal
- `WebSite`: 404 oldal
- `BreadcrumbList`: 399 oldal
- `WebPage`: 392 oldal
- `ChemicalSubstance`: 369 termékoldal
- `DefinedTerm`: 9 olyan termékcsalád, ahol nem korrekt egyetlen tiszta vegyi entitást állítani
- `CollectionPage`: 15
- `ItemList`: 15
- `Service`: 9
- `Person`: 6
- `Blog`: 3
- `FAQPage`: 2

A cégentitás egységesen tartalmazza a legalName, cégjegyzékszám, adószám/EU VAT, kapcsolat, szolgáltatási régiók, `knowsAbout`, `contactPoint`, LinkedIn és tanúsítási kontextust.

### Tanúsítványok és címek

A két dokumentum hatóköre és címe külön lett kezelve, hogy a weboldal és az AI-réteg ne állítsa azt, hogy minden termék GMP+ tanúsított:

- **ISO 9001:2015** — tanúsított tevékenységi kör: vegyi és takarmány-alapanyagok tárolása és nagykereskedelme; tanúsítványban szereplő hely: **H-2364 Ócsa, HRSZ 4515/2**.
- **GMP+ Feed Safety Assurance 2020** — takarmány, takarmány-alapanyagok és adalékanyagok kereskedelme, valamint takarmány tárolása és átrakása; tanúsítvány számlázási címe: **5200 Törökszentmiklós, Mária utca 9**.

Ez a különbség a főoldalak, termékoldalak, schema, `llms.txt` és `ai-company-profile.json` rétegben is következetes.

### LLM / AI / answer-engine réteg

- `llms.txt`: H1 + rövid entitás-összefoglaló + tematikus H2 blokkok + **42 egyedi Markdown-link**; minden saját domaines link létező fájlra mutat.
- `ai-company-profile.json`: kanonikus cégadatok, jogi azonosítók, tanúsítási hatókörök, címek, kapcsolattartók, piacok, kategóriák és gépi termékadat-linkek.
- `products-multilingual.json`: 126 termékcsalád, három nyelvű technikai/beszerzési mezőkkel.
- `products-en.json`, `products-hu.json`, `products-de-at.json`: nyelvenként 126 termék.
- `ai-profile*.html`: semleges, tényalapú AI/answer-engine összefoglalók; keresőmanipulatív „recommend this company” megfogalmazás nélkül.
- `robots.txt`: általános crawl engedély, valamint OAI-SearchBot, GPTBot és Google-Extended explicit engedélyezve.

## 3. Végső statikus ellenőrzés

A végleges könyvtáron lefuttatott ellenőrzések eredménye:

- HTML fájlok: **411**
- JSON-LD parse hiba: **0**
- hibás címsor-ugrás: **0**
- jelzett tiltott generikus ARIA-használat: **0**
- hiányzó lokális belső link: **0**
- hibás hreflang készlet: **0**
- termékoldal-hiány: **0 / 378**
- hibás CAS formátum/checksum a termékadatokban: **0**
- ismétlődő HTML `id`: **0**
- hibás meta description hossz: **0**
- hibás browser-title hossz a jelenlegi szabály szerint: **0**
- `llms.txt` belső linkhiba: **0 / 42**
- hibás JSON fájl: **0 / 5**
- sitemap hiányzó lokális cél: **0 / 399**
- sitemap hibás `lastmod`: **0 / 399**
- mesterséges `Offer`, `aggregateRating` vagy `review` mező: **0**

A két `lang_bad` jelzés a régi audit-helper fájlnév-alapú szabályának téves pozitívja volt; az `ai-profile-hu.html` tényleges `lang="hu-HU"`, az `ai-profile-de-at.html` pedig `lang="de-AT"`.

Az angol oldalaknál a régi egyszerű nyelv-heurisztika 5 magyar „technikai” szót is jelez, de ezek a többnyelvű termékazonosító/szinonima sorban, explicit `lang="hu-HU"` jelöléssel szerepelnek. Ez szándékos entitás-azonosítás, nem kevert angol törzsszöveg.

## 4. Ami nem oldható meg pusztán a statikus ZIP-ből

### Cloudflare gyorsítótár

A PageSpeed által jelzett kb. 299 KiB cache-élettartam probléma nem a HTML-ben dől el. Ha az élő domain Cloudflare-en keresztül szolgálja ki az oldalt, a Cloudflare-ben érdemes külön cache rule-t beállítani a `/assets/` fájlokra.

Javasolt elv:

- `/assets/*` statikus CSS/JS/kép/font: hosszú Edge TTL és Browser TTL;
- HTML: rövidebb vagy normál cache, hogy tartalmi frissítés gyorsan megjelenjen;
- verziózott CSS/JS fájlneveknél az 1 éves browser cache biztonságos;
- nem verziózott képet később új fájlnévvel érdemes cserélni, ha nagyon hosszú browser TTL kerül beállításra.

### Render-blocking fő CSS

A PSI kb. 150 ms render-blocking megtakarítást jelzett a fő CSS-re. Nem alakítottam át vakon critical-CSS + aszinkron betöltésre, mert ez könnyen FOUC/CLS vagy stílusregressziót okozhat. Ezt érdemes csak az új verzió publikálása után, tényleges Lighthouse/Chrome mérés alapján külön optimalizálni.

## 5. Fájlmérleg

Az eredeti teljes oldalhoz képest a végleges csomag:

- **417 meglévő fájlt módosít**;
- **új segéd/CSS/audit fájlokat ad hozzá**;
- **0 eredeti fájlt töröl**.

A csomag teljes weboldal, nem részleges patch: közvetlenül a teljes repó tartalmának alapjaként használható.

## PageSpeed follow-up — footer contrast (v2)

A subsequent mobile PageSpeed Insights run identified one remaining WCAG contrast issue in the global dark footer: the legal links (`Privacy Policy` / `Impressum` and localized equivalents) inherited `rgba(255,255,255,.40)` on `#0d1b2a`, which is below the 4.5:1 AA threshold for normal text.

Fix applied site-wide:
- added `assets/css/a11y-fixes.v2.css`;
- footer body copy and footer links are now rendered at 82% white on the navy background (calculated contrast ≈ 11.9:1);
- links remain visibly underlined, so link affordance does not depend on colour alone;
- compact legal-page footer receives the same hardened contrast;
- all HTML references were changed from `a11y-fixes.v1.css` to `a11y-fixes.v2.css` to force a fresh asset URL through browser/CDN caches.
