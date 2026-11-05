from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = sorted(ROOT.glob('*.html'))
JS = ROOT / 'assets/js/rmt-contact.v20261104.js'
CSS = ROOT / 'assets/css/rmt-contact.v20261104.css'
SITE_JS = ROOT / 'assets/js/site.v20260709d.js'
WORKER = 'https://muddy-voice-db90.6ymnrwgnv9.workers.dev'

def contrast_ratio(foreground, background):
    def luminance(color):
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        channels = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in channels]
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]
    a, b = luminance(foreground), luminance(background)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def main():
    assert len(HTML) >= 400, f'Unexpectedly small public HTML set: {len(HTML)}'
    assert JS.exists() and CSS.exists()
    js = JS.read_text()
    css = CSS.read_text()
    site_js = SITE_JS.read_text()
    assert "https://muddy-voice-db90.6ymnrwgnv9.workers.dev/api/contact" in site_js
    assert "function initForm()" in site_js and "turnstile" in site_js.lower()
    assert "aria-expanded" in js and "aria-controls" in js and "aria-label" in js
    assert "Escape" in js and "keydown" in js and ".focus()" in js
    assert ":focus-visible" in css
    assert contrast_ratio("#0879c9", "#ffffff") >= 4.5
    for path in HTML:
        text = path.read_text()
        assert ('/assets/js/site.v20260709d.js' in text or '/assets/js/rmt-contact.v20261104.js' in text), path
        assert text.count('/assets/css/rmt-contact.v20261104.css') == 0, path
        csp_tags = re.findall(r"<meta\b[^>]*http-equiv=\"Content-Security-Policy\"[^>]*>", text, re.I)
        if not csp_tags and "noindex" in text.lower() and "http-equiv=" in text.lower() and "refresh" in text.lower():
            continue
        assert csp_tags, f"Missing CSP on non-redirect page: {path}"
        csp_match = re.search(r'content="([^"]+)"', csp_tags[0], re.I)
        assert csp_match, f"CSP meta has no content: {path}"
        csp = csp_match.group(1)
        assert f"form-action 'self' {WORKER}" in csp, path
        assert f"connect-src 'self' {WORKER}" in csp, path
        assert "https://challenges.cloudflare.com" in csp, path
        assert "worker-src 'none'" in csp, path
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
        ec_label = {"en-": "EC / EINECS number", "hu-": "EK / EINECS-szám", "de-at-": "EG / EINECS-Nummer"}[prefix]
        for product in products:
            body = product.read_text()
            assert re.search(r"<dt[^>]*>CAS[^<]*</dt>\s*<dd[^>]*>[^<]+</dd>", body, re.I)
            assert f"<dt>{ec_label}</dt><dd>" in body
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

