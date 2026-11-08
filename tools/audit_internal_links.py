#!/usr/bin/env python3
"""Validate every same-origin anchor link across public HTML, including PDF certificates.

Unlike audits restricted to <link>, <script> and <img>, this tests <a href>.
Fragment targets and external domains are intentionally out of scope.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT=Path(__file__).resolve().parents[1]
HOSTS={"www.rawmaterialstrade.com","rawmaterialstrade.com"}
FAILURES={}
TOTAL=0

class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs=[]
    def handle_starttag(self, tag, attrs):
        if tag=="a":
            v=dict(attrs).get("href")
            if v is not None: self.hrefs.append(v.strip())

for html in ROOT.glob("*.html"):
    parser=Anchors()
    parser.feed(html.read_text(encoding="utf-8"))
    for href in parser.hrefs:
        if not href or href.startswith("#"):
            continue
        url=urlsplit(href)
        if url.scheme and url.scheme not in ("https","http"):
            if url.scheme in ("mailto","tel","sms","whatsapp"):
                continue
            FAILURES.setdefault((html.name,href),"unsupported link scheme")
            continue
        if url.netloc and url.netloc.lower() not in HOSTS:
            continue
        path=unquote(url.path)
        if not path:
            continue
        if re.search(r'[\x00-\x1f]',path) or ".." in Path(path).parts:
            FAILURES.setdefault((html.name,href),"invalid same-origin path")
            continue
        relative=path.lstrip("/") if path.startswith("/") else path
        if not relative or relative.endswith("/"):
            relative+="index.html"
        target=ROOT/relative
        TOTAL+=1
        if not target.is_file():
            FAILURES.setdefault((html.name,href),"missing local target")

print(f"Internal anchor links: {TOTAL} checked across {len(list(ROOT.glob('*.html')))} HTML documents; missing/unsafe={len(FAILURES)}")
for (page,href),msg in list(FAILURES.items())[:60]:
    print("ERROR:",page,repr(href),msg)
raise SystemExit(bool(FAILURES))
