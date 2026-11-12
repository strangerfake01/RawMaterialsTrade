# Prioritásos termékoldalak – döntéstámogató audit

## Hatókör

Az e-mailes érdeklődések és a GSC látható keresési jelei alapján kiválasztott termékcsaládok:

- nátrium-karbonát és nátrium-hidrogén-karbonát;
- kalcium-klorid;
- foszforsav;
- karbamid;
- citromsav;
- glicerin;
- nátrium-hidroxid;
- réz- és cinkvegyületek;
- propionsav;
- etil-acetát;
- nátrium-perszulfát;
- ammónium-szulfát.

Az audit 84 lokalizált oldalt érintett EN/HU/DE-AT nyelven.

## Implementált javítás

Minden érintett oldalon létrejött a `product-decision-guide` blokk, amely mindhárom nyelven közérthetően összeköti:

1. a CAS-számot, hidrát-/formaváltozatot és koncentrációt;
2. a tényleges felhasználási célt és az eltérő minőségi követelményeket;
3. a mennyiséget, csomagolást, szállítási helyet és határidőt;
4. az SDS, TDS/specifikáció és tételszintű CoA szerepét;
5. a szabályozási megfelelőség és tanúsítás dokumentumalapú igazolását;
6. az alternatívák dokumentumok alapján történő vizsgálatát.

Ez a réteg nem állít készletet, árat, MOQ-t, Incoterms-paritást, tanúsítást vagy jogszabályi megfelelőséget dokumentum nélkül.

## Ellenőrzési eredmény

- Release contract: PASS, 378 oldal / 126 család.
- Háromnyelvű katalógusparitás: PASS.
- FAQ–látható tartalom egyezés: PASS.
- Termékoldali döntési ellenőrzőpontok: PASS.
- Bizalmas git-történeti ellenőrzés: PASS.

## Még szükséges emberi / beszállítói hitelesítés

Az oldalstruktúra döntéstámogató, de az alábbi termékszintű tényeket nem szabad automatikusan véglegesnek tekinteni:

- az adott kereskedelmi forma és a CAS/EC/formula pontos megfelelése;
- a tényleges minőség, koncentráció, részecskeméret és hidratáltsági forma;
- az aktuális SDS, TDS/specifikáció és tételszintű CoA;
- REACH/CLP, élelmiszer-, takarmány-, kozmetikai vagy egyéb szabályozási alkalmasság;
- aktuális elérhetőség, MOQ, Incoterms és szállítási idő.

Ezeket a kiválasztott beszállítói ajánlat és dokumentáció alapján kell kitölteni vagy megerősíteni. A PubChem/Wikipedia/Wikidata hivatkozások azonosítási és tájékozódási segítséget adnak, de nem helyettesítik a beszállítói dokumentumokat.
