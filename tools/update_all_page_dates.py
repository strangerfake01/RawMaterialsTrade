from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TODAY = '2026-11-12'
changed = 0
for path in ROOT.glob('*.html'):
    text = path.read_text(encoding='utf-8')
    new = re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"', f'"dateModified":"{TODAY}"', text)
    # Privacy pages have WebPage JSON-LD but did not previously expose a modification date.
    if path.name in {'privacy.html', 'privacy-en.html', 'privacy-hu.html', 'privacy-de-at.html'} and '"dateModified"' not in new:
        new = new.replace('"name":"', f'"dateModified":"{TODAY}","name":"', 1)
    if new != text:
        path.write_text(new, encoding='utf-8')
        changed += 1
print(f'Updated dateModified on {changed} HTML pages')
