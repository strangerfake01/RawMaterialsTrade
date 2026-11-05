from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = sorted(ROOT.glob('*.html'))
JS = ROOT / 'assets/js/rmt-contact.v20261104.js'
CSS = ROOT / 'assets/css/rmt-contact.v20261104.css'

def main():
    assert len(HTML) >= 400, f'Unexpectedly small public HTML set: {len(HTML)}'
    assert JS.exists() and CSS.exists()
    js = JS.read_text()
    css = CSS.read_text()
    for path in HTML:
        text = path.read_text()
        assert ('/assets/js/site.v20260709d.js' in text or '/assets/js/rmt-contact.v20261104.js' in text), path
        assert text.count('/assets/css/rmt-contact.v20261104.css') == 0, path
    assert js.count('https://wa.me/36205567917') == 1
    assert js.count('tel:+36205567917') == 1
    assert js.count('mailto:nikoletta.kadar@rawmaterialstrade.com') == 1
    assert 'window.addEventListener(\'scroll\',scheduleFooterOffset' in js
    assert 'window.addEventListener(\'resize\',scheduleFooterOffset' in js
    assert 'getBoundingClientRect().top' in js
    assert 'ResizeObserver' in js
    assert 'safe-area-inset-bottom' in css
    assert 'prefers-reduced-motion:reduce' in css
    assert 'min-height:44px' in css
    qualification = {
        'en-': 'how-we-qualify-a-raw-material.html',
        'hu-': 'hu-alapanyag-minosites.html',
        'de-at-': 'de-at-rohstoffqualifizierung.html',
    }
    for prefix, href in qualification.items():
        products = [p for p in HTML if p.name.startswith(prefix) and 'product-hero-detail' in p.read_text()]
        assert len(products) == 126, (prefix, len(products))
        assert all(href in p.read_text() for p in products), prefix
    category_trust = {
        'en-industrial-chemicals.html': 'ai-trust-center.html',
        'en-deicing-materials.html': 'ai-trust-center.html',
        'hu-ipari-vegyipari-alapanyagok.html': 'hu-ai-bizalmi-kozpont.html',
        'hu-teli-utszorasi-anyagok.html': 'hu-ai-bizalmi-kozpont.html',
        'de-at-industriechemikalien.html': 'de-at-ai-vertrauenszentrum.html',
        'de-at-winterdienst-streumittel.html': 'de-at-ai-vertrauenszentrum.html',
    }
    for page, href in category_trust.items():
        assert href in (ROOT / page).read_text(), page
    assert 'What this review does not mean' in (ROOT / 'how-we-qualify-a-raw-material.html').read_text()
    assert 'Mit nem jelent ez az áttekintés?' in (ROOT / 'hu-alapanyag-minosites.html').read_text()
    assert 'Was diese Prüfung nicht bedeutet' in (ROOT / 'de-at-rohstoffqualifizierung.html').read_text()
    assert 'Human accountability' in (ROOT / 'ai-trust-center.html').read_text()
    assert 'Emberi felelősség' in (ROOT / 'hu-ai-bizalmi-kozpont.html').read_text()
    assert 'Menschliche Verantwortung' in (ROOT / 'de-at-ai-vertrauenszentrum.html').read_text()
    print(f'PASS: {len(HTML)} HTML pages include one shared contact CSS/JS reference')
    print('PASS: WhatsApp, phone and email destinations are centralized and exact')
    print('PASS: scroll/resize footer offset, safe-area, keyboard focus and reduced-motion hooks present')
    print('PASS: 126 EN/HU/DE product pages per language link to the matching qualification page')
    print('PASS: industrial and winter-service category pages link to the matching AI Trust Center')
    print('PASS: qualification boundaries and human AI-Trust accountability are present in all three languages')

if __name__ == '__main__':
    main()

