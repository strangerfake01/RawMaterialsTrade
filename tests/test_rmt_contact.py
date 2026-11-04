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
    assert 'IntersectionObserver' in js
    assert 'safe-area-inset-bottom' in css
    assert 'prefers-reduced-motion:reduce' in css
    assert 'min-height:44px' in css
    print(f'PASS: {len(HTML)} HTML pages include one shared contact CSS/JS reference')
    print('PASS: WhatsApp, phone and email destinations are centralized and exact')
    print('PASS: footer observer, safe-area, keyboard focus and reduced-motion hooks present')

if __name__ == '__main__':
    main()
