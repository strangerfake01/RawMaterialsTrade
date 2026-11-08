#!/usr/bin/env python3
"""Validate local static asset references on every root HTML page."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        key = {'link': 'href', 'script': 'src', 'img': 'src',
               'source': 'src', 'video': 'poster'}.get(tag)
        if key and values.get(key):
            self.urls.append(values[key])

missing = Counter()
documents = list(ROOT.glob('*.html'))
for doc in documents:
    parser = Assets()
    parser.feed(doc.read_text(encoding='utf-8'))
    for ref in parser.urls:
        if ref.startswith(('https:', 'http:', '//', 'data:', 'mailto:', 'tel:', '#')):
            continue
        rel = unquote(urlparse(ref).path)
        target = ROOT / rel.lstrip('/') if rel.startswith('/') else doc.parent / rel
        if not target.is_file():
            missing[rel] += 1

print(f'Checked {len(documents)} HTML pages; missing same-origin assets={len(missing)}')
for path, count in missing.most_common():
    print(f'MISSING {count} references: {path}')
raise SystemExit(1 if missing else 0)
