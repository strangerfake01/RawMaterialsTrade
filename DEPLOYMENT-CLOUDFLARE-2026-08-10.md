# Publikálás utáni Cloudflare ellenőrzés

A statikus weboldal kódszintű javítása elkészült. A PageSpeed cache-élettartam pontját azonban a kiszolgáló/CDN válaszfejlécei határozzák meg.

## Javasolt Cache Rule

Cloudflare → Caching → Cache Rules → Create rule

Feltétel: URI path starts with `/assets/`

Beállítási elv:

- Cache eligibility: eligible for cache
- Edge TTL: hosszú (pl. 1 hónap–1 év)
- Browser TTL: hosszú a verziózott asseteknél

A `site.v20260709.min.css` jellegű verziózott fájlnevek biztonságosan kaphatnak hosszú TTL-t. Nem verziózott képfájl cseréjénél célszerű új fájlnevet használni, ha a böngészőcache hosszú.

## Publikálás után újramérendő

1. PageSpeed Insights — mobil + asztal
2. Agentic Browsing / llms.txt
3. Accessibility / ARIA / contrast
4. LCP és image delivery
5. Cache lifetime
6. Render-blocking CSS
7. Google Rich Results / schema validáció reprezentatív főoldalon és termékoldalon

A végleges ZIP nem állít be Cloudflare-fiók oldali cache rule-t; ezt a hoszt/CDN oldalon kell megtenni.
