# Raw Materials Trade – kontraszt- és tipográfiai javítás

Dátum: 2026. július 9.

## Audit hatóköre

A publikálható csomag 412 HTML-oldalát strukturális sablonok szerint vizsgáltam. A rendszer 10 eltérő oldaltípusból épül fel; a közös sablonokat, a sötét hátterű szakaszokat, a betűméreteket, sortávokat, szövegszélességeket, kártyaszövegeket, gombokat, asztali és mobil töréspontokat ellenőriztem.

A nagy főcímek méretét nem módosítottam.

## Feltárt hiba

Az `ai-profile-hero` sablonhoz nem tartozott önálló rácsszerkezet és kontrasztkezelés. Emiatt:

- a jobb oldali információs panel asztali nézetben a főszöveg alá került;
- a panel háttere átlátszó maradt;
- az alcím, a bevezető szöveg és a panel címe sötét színt örökölt a sötét háttéren;
- az outline gomb kék szövege túl gyenge kontrasztú volt;
- több kártya és magyarázó szöveg 13–14 px körüli mérete a prémium, könnyen olvasható megjelenéshez túl kicsi volt.

A hiba kizárólag hat oldalt érintett.

## Javított oldalak

1. `sales-representation-distribution-partner-central-europe.html`
2. `hu-ertekesitesi-kepviselet-disztribucios-partner.html`
3. `de-at-vertriebspartner-distribution-chemierohstoffe.html`
4. `ai-profile.html`
5. `ai-profile-hu.html`
6. `ai-profile-de-at.html`

## Beépített javítások

- kétoszlopos, kiegyensúlyozott desktop hero-rács;
- egyoszlopos, tiszta mobil elrendezés;
- világos, nagy kontrasztú szemöldökcím, lead és panelcím;
- áttetsző, finom keretes információs panel;
- 50 px minimális gombmagasság és következetes gombritmus;
- hosszabb szövegeknél lazább, 1.58–1.67 közötti sortáv;
- kártyaszövegek emelése kb. 15 px-re;
- 62 karakter körüli maximális bevezető szövegszélesség;
- nagyobb szakaszközök és kiegyensúlyozott vertikális ritmus;
- a főcímek meglévő méretének megtartása;
- új, cache-biztos stylesheet: `/assets/css/site.v20260709e.min.css`.

## Visszaellenőrzés

- módosított HTML-oldalak: 6
- új/módosított CSS-fájl: 1
- érintett `ai-profile-hero` oldalak lefedettsége: 6/6
- hiányzó belső asset vagy link: 0
- hibás JSON-LD blokk: 0
- CSS kapcsos zárójel eltérés: 0
- CSS parser hiba: 0
- desktop rács: 2 oszlop
- mobil rács: 1 oszlop
- hero lead kontrasztja: kb. 10.9:1
- panel törzsszöveg kontrasztja: kb. 9.3:1
- panel címszöveg kontrasztja: kb. 14.3:1
- eyebrow kontrasztja: kb. 11.5:1

A többi oldaltípuson nem találtam ugyanezt a kontraszt- és elrendezési hibát, ezért azok fájljait nem tettem a javítócsomagba.

## Feltöltés

A ZIP tartalmát a webhely gyökérkönyvtárába kell feltölteni a könyvtárstruktúra megtartásával. A hat HTML-fájlt felül kell írni, az új CSS-fájlt pedig az alábbi útvonalra kell feltölteni:

`/assets/css/site.v20260709e.min.css`

A Worker és a Google Apps Script nem változott.
