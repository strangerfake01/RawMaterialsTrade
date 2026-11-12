from pathlib import Path
from xml.etree import ElementTree as ET
import json
from datetime import date
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'blog-knowledge-index.json'
OUT.parent.mkdir(exist_ok=True)
feed_url = 'https://blog.rawmaterialstrade.com/feeds/posts/default?alt=atom&max-results=500'
data = urlopen(Request(feed_url, headers={'User-Agent': 'RawMaterialsTrade-knowledge-index/1.0'}), timeout=30).read()
root = ET.fromstring(data)
ns = {'a': 'http://www.w3.org/2005/Atom'}
items = []
for entry in root.findall('a:entry', ns):
    title = entry.findtext('a:title', '', ns)
    published = entry.findtext('a:published', '', ns)
    updated = entry.findtext('a:updated', '', ns)
    author = entry.findtext('a:author/a:name', '', ns)
    link = next((x.attrib.get('href') for x in entry.findall('a:link', ns) if x.attrib.get('rel') == 'alternate'), '')
    labels = [x.attrib.get('term') for x in entry.findall('a:category', ns) if x.attrib.get('term')]
    languages = []
    if 'magyar' in labels: languages.append('hu-HU')
    if 'english' in labels: languages.append('en')
    items.append({'title': title, 'url': link, 'published': published, 'updated': updated, 'author': author, 'labels': labels, 'languages': languages})
items.sort(key=lambda x: x.get('published', ''), reverse=True)
payload = {
    'schemaVersion': '1.0',
    'generatedAt': date.today().isoformat(),
    'source': {'type': 'Blogger Atom feed', 'url': feed_url, 'canonicalHost': 'https://blog.rawmaterialstrade.com'},
    'policy': 'Index and link to original articles; do not republish or treat editorial content as product, SDS, CoA or regulatory evidence.',
    'counts': {'articles': len(items), 'hungarian': sum('hu-HU' in x['languages'] for x in items), 'english': sum('en' in x['languages'] for x in items), 'german': 0},
    'articles': items,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Indexed {len(items)} blog articles -> {OUT}')
