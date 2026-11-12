# Blog tudásintegráció – audit és alapréteg

## Forrás

Nyilvános Blogger Atom-feed: `https://blog.rawmaterialstrade.com/feeds/posts/default?alt=atom&max-results=500`

Az ellenőrzött feed 14 cikket tartalmazott:

- 6 magyar nyelvű címkézett cikk;
- 6 angol nyelvű címkézett cikk;
- 2 cikk nyelvi címke nélkül, ezért kézi felülvizsgálatra vár.

Német nyelvű, külön címkézett cikket a feed nem tartalmazott. A `?lang=de` paraméter az auditkor nem hozott létre külön német canonical oldalt; ugyanarra az angol címke-archívumra canonicalizált.

## Implementált alapréteg

Létrejött a `data/blog-knowledge-index.json` gépi tudásindex. Tartalmazza a cikk eredeti URL-jét, címét, szerzőjét, publikálási és frissítési dátumát, Blogger-címkéit és nyelvi státuszát.

A `llms.txt` most egyértelműen meghatározza a blog szerepét: szerkesztőségi háttér- és tudásforrás, nem SDS, TDS, CoA, laborjelentés, szabályozási jóváhagyás vagy beszállítói kereskedelmi bizonyíték.

## Következő Blogger-oldali javítások

- valós HU/EN/DE-AT nyelvi oldalstruktúra és canonical/hreflang;
- egyedi meta description és Open Graph leírás címke- és cikkoldalakon;
- BlogPosting JSON-LD szerzővel, dátummal, képpel és canonical URL-lel;
- nyelvi címkék pótlása a két jelenleg címke nélküli bejegyzésnél;
- magyar/angol párok és esetleges német fordítások explicit összekapcsolása;
- termékoldali kapcsolódó cikkek csak eredeti canonical linkkel, másolás nélkül.

Ezekhez Blogger-sablon- vagy adminisztrációs hozzáférés szükséges; a statikus repositoryból önmagában nem élesíthetők.
