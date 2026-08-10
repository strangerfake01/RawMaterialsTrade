# PSI-javítás — 2026-08-10

A 2026-08-10 08:45 CEST mobil PageSpeed Insights audit alapján
(Teljesítmény 73 · Kisegítő lehetőségek 90 · Bevált módszerek 100 ·
Keresőoptimalizálás 100 · **Ügynöki böngészés 1/3**).

Minden változtatás a repo valós markupjára és színtokenjeire készült.
A `tools/rmt_psi_fix.py` idempotens: újrafuttatva 0 fájlt módosít.

---

## Ügynöki böngészés 1/3 → várhatóan 3/3

### `llms.txt` — teljes újraírás

**Hiba:** „Az llms.txt nem követi a javaslatokat — Úgy tűnik, hogy a fájl nem
tartalmaz linkeket."

**Ok:** a Lighthouse 13.3 óta markdown-dokumentumként parse-olja a fájlt.
A régi verzió `Kulcs: https://...` formában sorolta fel az URL-eket — a parser
ebből **nulla linket** ismert fel. Csak a `[szöveg](url)` szintaxis számít.

**Javítás:** H1 az első sorban, blockquote összefoglaló, majd 41 markdown-link
tematikus `##` szekciókban. A régi fájl minden tényadata megmaradt, csak a
formátum változott. Új: a három `ai-profile*.html`, a `sitemap.xml` és a
`robots.txt` is szerepel, valamint a nyelvenkénti kategóriaoldalak.

Ellenőrzött: H1 ✓ · blockquote ✓ · 41 markdown-link ✓ · 11 447 karakter ✓ ·
minden URL abszolút ✓

### ARIA — `aria-prohibited-attr`

**Hiba:** „Elemek tiltott ARIA-attribútumokat használnak", hibás elem:
`<div aria-label="Cloudflare security check" class="turnstile-container">`

**Ok:** a `role` nélküli `<div>` implicit `role="generic"`, ez pedig tiltja a
névadást, tehát az `aria-label` érvénytelen rajta.

**Javítás:** `role="group"` a turnstile konténerre mindhárom nyelvi verzión.
Emellett ugyanez a latens hiba javítva további 4 elemen (`lang-switcher`,
`hero-trust`, `company-identity-card`, `certificate-evidence`), amelyeket az
audit még nem jelzett, de ugyanabba a szabályba ütköznek.

---

## Kisegítő lehetőségek 90 → várhatóan 100

### Címsor-sorrend

**Hiba:** „A fejlécelemek nem egymást követő csökkenő sorrendben jelennek meg",
hibás elemek: `Enquiry` és `PRODUCTS`, mindkettő `<h4>`.

**Ok:** két helyen ugrott a szint `h2`-ről `h4`-re:

| Hely | Markup |
|---|---|
| Folyamatlépések | `<h2 id="processHeading">` … `<div class="step-num">1</div><h4>Enquiry</h4>` |
| Lábléc-oszlopok | `<h2>Request a B2B Quotation</h2>` … `<div class="footer-col"><h4>Products</h4>` |

**Javítás:** mindkét helyen `<h4>` → `<h3>`, 18 fájlban. A vezetői profilok
`h3 → h4` szerkezete **érintetlen**, az helyes volt.

A CSS a `.step h4` és `.footer-col h4` szelektorokhoz kötötte a stílust, ezért
az `a11y-fixes.v1.css` 6. blokkja pontosan ugyanazokat az értékeket adja meg
`h3`-ra. **A megjelenés nem változik**, csak a szemantikai szint.

Ellenőrzött: 0 fájlban maradt címsor-ugrás (411-ből).

### Kontraszt

**Hiba:** „Nem megfelelő a háttér- és előtérszínek közötti kontrasztarány."

A hibák forrása két színtoken volt: `--accent: #22d3ee` és `--grey-400: #94a3b8`.

| Elem | Régi | Arány | Új | Arány |
|---|---|---|---|---|
| `.section-label` | `#1e88e5` / fehér | 3,68:1 ✗ | `#14639e` | **6,35:1** ✓ |
| `.leader-kicker` | `#22d3ee` / fehér | 1,81:1 ✗ | `#14639e` | **6,35:1** ✓ |
| `.leader-link` | `#22d3ee` / fehér | 1,81:1 ✗ | `#0f5aa8` | **6,89:1** ✓ |
| `.form-notice` | `#94a3b8` / `#f8fafc` | 2,45:1 ✗ | `#4b5c70` | **6,55:1** ✓ |
| `.cert-valid-badge` | fehér / `#16a34a` | 3,30:1 ✗ | fehér / `#15702f` | **6,19:1** ✓ |

A sötét hátterű változatok (`.quality-section`, `.catalogue-page-hero`)
szándékosan **változatlanok**: ott a `#77d4e7` a navy alapon 10,23:1 — megfelelő.

A `.leader-kicker` 1,81:1 volt a legsúlyosabb: a `var(--accent, #1565c0)`
fallbackje sosem lépett életbe, mert az `--accent` definiálva van cyanként.

### Linkek felismerhetősége

**Hiba:** „A linkeket szín alapján lehet felismerni." (WCAG 1.4.1)

**Javítás:** a `.leader-link` (Email / LinkedIn) alapból aláhúzott lett, nem
csak hoverre. Ugyanígy a folyószövegben és a lábléc jogi sorában lévő linkek.
Gombok, navigáció, nyelvváltó és kártya-linkek **nem** kaptak aláhúzást.

Plusz: látható `:focus-visible` fókuszgyűrű és `prefers-reduced-motion` támogatás.

---

## Teljesítmény 73 → részben javítva

### Képtovábbítás (becsült megtakarítás 171 KiB)

A csapatfotók 800×800-ban töltődtek, miközben a CSS `max-width: 220px`-ben
jeleníti meg őket.

| Fájl | Előtte | Utána |
|---|---|---|
| `alexandra-sajban-frohner.webp` | 66 KB | 36 KB |
| `nikoletta-kadar.webp` | 45 KB | 23 KB |
| `alexandra-sajban-frohner-400.webp` | — | 13 KB (új) |
| `nikoletta-kadar-400.webp` | — | 8 KB (új) |

A markup `srcset` + `sizes` attribútumot kapott, így mobilon a 400-as változat
töltődik: **~90 KiB megtakarítás** a főoldalakon. Eredeti fájlok:
`.img-backup/`.

A logókat **szándékosan nem** tömörítettem tovább: a `logo-transpared.webp`
600×294-es, 256 fokozatú alfacsatornával, a q=50 is csak 89 → 75 KB-ot hoz,
láthatóan romló élekért cserébe. Ha kell a megtakarítás, a logót érdemes
SVG-ként újraexportálni — az néhány KB lenne.

### Gyorsítótár (becsült megtakarítás 299 KiB) — **kézi lépés**

A `_headers` fájl Netlify / Cloudflare Pages konvenció. **A GitHub Pages
figyelmen kívül hagyja**, saját rövid `Cache-Control`-t küld. Ezért jelzi a
PSI a hibát, hiába szerepel a fájlban az `immutable`.

Mivel az oldal Cloudflare mögött van (Turnstile + Worker), ott kell megoldani:

```
Cloudflare → Caching → Cache Rules → Create rule
  Ha:    URI Path starts with  /assets/
  Akkor: Eligible for cache
         Edge TTL     1 year
         Browser TTL  1 year
```

A fájlnevek már verziózottak (`site.v20260709.min.css`), így a hosszú TTL
biztonságos. Megjegyzés bekerült a `_headers` fájl végére is.

### Renderelést letiltó kérelmek (150 ms) — **nem javítva**

A `site.v20260709.min.css` 139 KB, egyetlen renderelést blokkoló kérés. A
kritikus CSS kiemelése valós nyereség lenne, de vizuális regressziót kockáztat
tesztelés nélkül, ezért ezt nem nyúltam hozzá. 150 ms a legkisebb tétel a
négy teljesítményhiba közül.

---

## Amit nem kellett javítani

Ellenőriztem, és ezek már rendben voltak:

- **hreflang:** 411 fájlból 406-on teljes (`en`, `hu-HU`, `de-AT`, `x-default`),
  kölcsönösen. Hiányzik: `en.html`, `privacy.html`,
  `de-at-alexandra-sajban-frohner.html`, `hu-sajban-frohner-alexandra.html`,
  `impressum.html` — az első négy átirányító csonk, ott nincs is rá szükség.
- **Hero LCP-markup:** már volt `preload` `imagesrcset`-tel, `fetchpriority="high"`,
  `width`/`height` és `<source>` srcset. Nem nyúltam hozzá.
- **JSON-LD:** mind a 406 blokk érvényes maradt a módosítások után.
- **Termékoldalak címsorai:** `h1` → `h2` szerkezet, nincs ugrás.

---

## Ellenőrzési lista publikálás után

```
1. PageSpeed Insights újrafuttatás — mobil és asztal
2. https://validator.schema.org/ — index.html, hu.html, de-at.html
3. Search Console → llms.txt lekérése (200, text/plain)
4. axe DevTools vagy WAVE — kontraszt 0 hiba
5. Vizuális ellenőrzés: lábléc-oszlopok és folyamatlépések címsorai
   (a h4 → h3 után azonosnak kell látszaniuk)
6. Cloudflare Cache Rule beállítása, majd újramérés
```

Megjegyzés: az Ügynöki böngészés kategória Chrome 150+ futtatót igényel. Ha a
PSI lábléce régebbi Chromiumot jelez, spec-helyes fájl mellett is előfordulhat
téves „Fetch failed" — ilyenkor 1–2 nap múlva érdemes újramérni.

---

## Ugyanez a hiba a másik oldalon

A 11. képernyőkép szerint a **goatprotective.com** is 2/3-on áll ugyanezzel az
`llms.txt` hibával. Ott ugyanez a formátumjavítás a megoldás.

---

## Domain-egységesítés — www.rawmaterialstrade.com a fő domain

### Ami már rendben volt

Végigellenőrizve a teljes repón:

| Ellenőrzés | Eredmény |
|---|---|
| `CNAME` | `www.rawmaterialstrade.com` |
| `rel="canonical"` | 411/411 fájl `https://www.rawmaterialstrade.com` |
| `sitemap.xml` `<loc>` | 399/399 `https://www.rawmaterialstrade.com` |
| Nem-www (`https://rawmaterialstrade.com/...`) hivatkozás | **0 db** |
| `github.io`, `netlify`, `pages.dev` maradvány | **0 db** |
| `llms.txt` saját URL-jei | 39/39 `https://www.` |

Itt tehát nem kellett javítani, és a PSI-javítócsomag sem rontott el semmit.

### Amit javítottam

A blog két különböző hosztnéven szerepelt ugyanazon az oldalon: a látható link
a saját aldomainre mutatott, a strukturált adat viszont a Blogger-hosztra.
Entitás-feloldásnál ez két külön blognak látszik, és a `sameAs` így nem
erősíti, hanem gyengíti a cég entitását.

Minden hivatkozás a fő domain családjára állítva — **12 előfordulás, 5 fájlban**:

| Fájl | Hol | Előtte | Utána |
|---|---|---|---|
| `index.html` | JSON-LD `Blog` `@id` + `url`, `Person.sameAs` | `rawmaterialstrade.blogspot.com` | `blog.rawmaterialstrade.com` |
| `hu.html` | ugyanaz | `rawmaterialstrade.blogspot.com` | `blog.rawmaterialstrade.com` |
| `de-at.html` | ugyanaz | `rawmaterialstrade.blogspot.com` | `blog.rawmaterialstrade.com` |
| `ai-company-profile.json` | `leadership.blog`, `professional_blog.url` | `rawmaterialstrade.blogspot.com` | `blog.rawmaterialstrade.com` |
| `llms.txt` | blog-hivatkozás | `rawmaterialstrade.blogspot.com` | `blog.rawmaterialstrade.com` |

Eredmény — az entitásgráf minden csomópontja a saját domainre horgonyzott:

```
Organization    https://www.rawmaterialstrade.com/#org
WebSite         https://www.rawmaterialstrade.com/#website
WebPage         https://www.rawmaterialstrade.com/#webpage
BreadcrumbList  https://www.rawmaterialstrade.com/#breadcrumb
Service         https://www.rawmaterialstrade.com/#b2b-sourcing-service
Service         https://www.rawmaterialstrade.com/#sales-partnership-service
Person          https://www.rawmaterialstrade.com/#alexandra-sajban-frohner
Person          https://www.rawmaterialstrade.com/#nikoletta-kadar
Blog            https://blog.rawmaterialstrade.com/#blog
```

Emellett javítva egy elgépelés: `ai-company-profile.json` →
`"Main Main Owner and Managing Director"` → `"Main Owner and Managing Director"`.

### Amit a repón kívül kell ellenőrizni

1. **Blogger custom domain.** A `blog.rawmaterialstrade.com` csak akkor
   működik, ha a Bloggerben be van állítva egyéni domainként
   (Beállítások → Közzététel → Egyéni domain), és a DNS-ben van rá `CNAME`
   rekord `ghs.google.com` célponttal. Ha nincs, a linkek 404-et adnak.
   A Blogger ilyenkor a `.blogspot.com` címről automatikusan átirányít az
   egyéni domainre, tehát a régi URL-ek nem vesznek el.
2. **Nem-www átirányítás.** A `rawmaterialstrade.com` (www nélkül) 301-gyel
   mutasson a `www.rawmaterialstrade.com`-ra. Cloudflare → Rules → Redirect
   Rules. Ez ma feltehetően működik, de érdemes ellenőrizni, mert a repóban
   nincs rá kényszerítés — a canonical önmagában csak jelzés, nem átirányítás.
3. **Search Console.** Ha a `blog.rawmaterialstrade.com` új aldomain, önálló
   propertyként érdemes felvenni.
