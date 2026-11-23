#!/usr/bin/env python3
"""Read-only exact-live release verification for Raw Materials Trade GitHub Pages.

Run after a verified main commit is deployed. Checks live Pages revision, full
sitemap equivalence, and essential three-language route availability. Never
submits forms or Google Search Console requests. No private business inputs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://www.rawmaterialstrade.com"
SITEMAP_NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
CRITICAL_PAGES = {
    "/": "en",
    "/hu.html": "hu",
    "/de-at.html": "de",
    "/en-catalogue.html": "en",
    "/hu-termekkatalogus.html": "hu",
    "/de-at-produktkatalog.html": "de",
    "/sales-representation-distribution-partner-central-europe.html": "en",
    "/hu-ertekesitesi-kepviselet-disztribucios-partner.html": "hu",
    "/de-at-vertriebspartner-distribution-chemierohstoffe.html": "de",
    "/ai-trust-center.html": "en",
    "/hu-ai-bizalmi-kozpont.html": "hu",
    "/de-at-ai-vertrauenszentrum.html": "de",
}
PRODUCT_PAGES = (
    "/en-glicerin-99-5-food.html",
    "/hu-glicerin-99-5-food.html",
    "/de-at-glicerin-99-5-food.html",
)

class PageMeta(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.canonicals = []
        self.h1_count = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang") or ""
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a.get("href"))
        elif tag == "h1":
            self.h1_count += 1

def request(path: str, revision: str) -> bytes:
    if not path.startswith("/") or "//" in path[1:] or urlparse(path).scheme:
        raise ValueError("Unsafe request path")
    # Cache-busting query is not a new indexable URL; used only by release QA.
    url = ORIGIN + path + "?release_probe=" + revision[:12]
    req = Request(url, headers={
        "User-Agent": "RMT-Production-Release-QA/1.0",
        "Cache-Control": "no-cache",
        "Accept": "text/html,application/json,application/xml,text/plain",
    })
    with urlopen(req, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"{path} returned HTTP {response.status}")
        if urlparse(response.url).netloc != "www.rawmaterialstrade.com":
            raise RuntimeError(f"Unexpected redirect host: {response.url}")
        return response.read(4_000_001)

def parse_sitemap(data: bytes) -> list[tuple[str, str]]:
    root = ET.fromstring(data)
    values = []
    for node in root.findall("s:url", SITEMAP_NS):
        loc = node.findtext("s:loc", default="", namespaces=SITEMAP_NS)
        mod = node.findtext("s:lastmod", default="", namespaces=SITEMAP_NS)
        values.append((loc, mod))
    return values

def verify_once(sha: str) -> dict:
    manifest = json.loads(request("/release-manifest.json", sha))
    actual = manifest.get("commit")
    if actual != sha:
        raise RuntimeError(f"Pages revision mismatch: expected {sha}, got {actual!r}")
    if manifest.get("repository") != "strangerfake01/RawMaterialsTrade":
        raise RuntimeError("Manifest repository mismatch")
    expected_sitemap = parse_sitemap((ROOT / "sitemap.xml").read_bytes())
    actual_sitemap = parse_sitemap(request("/sitemap.xml", sha))
    if actual_sitemap != expected_sitemap:
        raise RuntimeError(f"Sitemap differs: source {len(expected_sitemap)} vs live {len(actual_sitemap)} URLs")
    if len(actual_sitemap) != len(set(actual_sitemap)):
        raise RuntimeError("Live sitemap contains duplicate loc/lastmod tuples")
    expected_count = len(json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8")))
    page_checks = 0
    for path, lang in CRITICAL_PAGES.items():
        html = request(path, sha).decode("utf-8")
        p = PageMeta()
        p.feed(html)
        canonical = ORIGIN + path if path != "/" else ORIGIN + "/"
        if p.canonicals != [canonical]:
            raise RuntimeError(f"{path} unexpected canonical: {p.canonicals}")
        if not p.lang.lower().startswith(lang):
            raise RuntimeError(f"{path} missing/mismatched HTML language: {p.lang!r}")
        if p.h1_count != 1:
            raise RuntimeError(f"{path} expected one semantic H1; got {p.h1_count}")
        if path in {"/", "/hu.html", "/de-at.html"}:
            if f'class="stat-number">{expected_count}</span>' not in html:
                raise RuntimeError(f"{path} does not display verified {expected_count} product families")
        page_checks += 1
    for path in PRODUCT_PAGES:
        html = request(path, sha).decode("utf-8")
        if 'application/ld+json' not in html or 'privacy-' not in html:
            raise RuntimeError(f"{path} product schema / privacy link absent")
        page_checks += 1
    for path in ("/robots.txt", "/ai.txt", "/llms.txt"):
        data = request(path, sha)
        if not data.strip():
            raise RuntimeError(f"{path} empty")
    return {
        "expectedSha": sha,
        "manifestSha": actual,
        "sitemapUrls": len(actual_sitemap),
        "criticalHtmlPagesChecked": page_checks,
        "publicRobotAndAIFilesChecked": 3,
        "status": "PRODUCTION-VERIFIED SOURCE/HTTP",
        "limitations": "Does not prove browser consent, Cloudflare/Turnstile form E2E or legal review."
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-sha", required=True, help="full 40-character main commit SHA")
    parser.add_argument("--attempts", type=int, default=1, help="retry attempts while Pages deploy completes")
    parser.add_argument("--delay", type=int, default=25, help="seconds between attempts")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-f0-9]{40}", args.expected_sha):
        parser.error("expected SHA must be exactly 40 lowercase hexadecimal characters")
    if not 1 <= args.attempts <= 20 or not 0 <= args.delay <= 120:
        parser.error("attempts must be 1..20; delay must be 0..120 seconds")
    for i in range(args.attempts):
        try:
            result = verify_once(args.expected_sha)
            print(json.dumps(result, indent=2))
            return 0
        except (OSError, HTTPError, URLError, ValueError, RuntimeError, ET.ParseError) as error:
            print(f"attempt {i+1}/{args.attempts}: {type(error).__name__}: {error}", file=sys.stderr)
            if i + 1 < args.attempts:
                time.sleep(args.delay)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
