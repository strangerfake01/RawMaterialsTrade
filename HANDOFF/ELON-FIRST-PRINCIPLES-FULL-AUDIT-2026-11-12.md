# Raw Materials Trade – első alapelvekre épülő teljes audit

## Auditértelmezés

Az „Elon Musk szempontjai” itt nem személyes jóváhagyást jelent, hanem az alábbi működési elveket: első alapelvek, igazolható állítások, kevés fölösleges réteg, gyors megértés, nagy információsűrűség, automatizálható folyamat és mérhető release-kapu.

## Eredmény

### AUDITED / FIXED / CI-VERIFIED

- 378 lokalizált termékoldal, 126 termékcsalád.
- EN/HU/DE-AT route-, canonical-, hreflang- és JSON-LD-paritás.
- ChemicalSubstance identitásréteg CAS/EC/formula státuszkorlátokkal.
- FAQ és látható tartalom egyezése.
- Beszerzési útvonal, dokumentum- és ajánlatkérési út minden termékcsaládnál.
- Organization, WebSite, WebPage, ChemicalSubstance és BreadcrumbList gépi kapcsolatok.
- AI Trust állítási szerződés: 0 hiba.
- Nyilvános adatvédelmi ellenőrzés: 0 idegen e-mail-cím.
- Bizalmas git-történeti ellenőrzés: PASS.
- Release contract: 405 sitemap URL, 0 hiba, 0 figyelmeztetés.

### Javított kritikus hitelességi kockázat

A korábban közzétett, automatikus PubChem-jelölt adatok nem voltak minden oldalon form- és képletazonosság szinten függetlenül hitelesítve. A 366 érintett lokalizált oldalról eltávolítottuk a nyilvános PubChem-képlet/molekulatömeg blokkot és a hozzá tartozó JSON-LD hivatkozást. A képlet, CAS, EC, forma, minőség és szabályozási alkalmasság csak dokumentumalapú megerősítéssel tehető vissza.

Ez tudatos információcsökkentés: a hiányzó, de nem bizonyított adat jobb üresen vagy „megerősítendő” státuszban, mint gazdag, de félrevezető állításként.

### 5 másodperces érthetőség

Strukturális ellenőrzés alapján a termékoldal első rétege egyértelműen mutatja:

1. mi az anyag;
2. milyen B2B beszerzési célra szolgál;
3. mely azonosítóval kell ellenőrizni;
4. milyen dokumentum szükséges;
5. mit kell elküldeni ajánlatkéréshez.

A teljes 5 másodperces vizuális tesztet valódi böngészőben, minden viewporton külön kell mérni; statikus audit önmagában nem bizonyít vizuális 100%-ot.

## Nyitott, nem automatikusan lezárható tételek

- 70 koncentráció/grade mező szemantikai felülvizsgálata szükséges, mert a grade, hidrát, részecskeméret vagy fizikai forma nem mindig koncentráció.
- 126 form-/beszállítói megerősítés továbbra is dokumentumfüggő.
- 21 megosztott Wikidata-koncepció 45 form/grade családnál emberi form-ellenőrzést igényel.
- Nyilvános Wikipédiából nem következik termékazonosság vagy szabályozási megfelelőség.
- Aktuális készlet, ár, MOQ, Incoterms, szállítási idő, SDS/TDS/CoA és tanúsítás csak konkrét ajánlatból igazolható.
- Jogszabályi teljes megfelelőség nem állítható kizárólag technikai audit alapján; szükség esetén szakértői jogi felülvizsgálat kell.

## Release-határok

Nem kerülhet vissza nyilvános oldalra olyan adat, amely csak automatikus jelölt, nem ellenőrzött vagy formaütközéses külső forrásból származik. A kiadási folyamatnak a beszállítói dokumentumot, forrást, ellenőrzőt és dátumot kell rögzítenie.
