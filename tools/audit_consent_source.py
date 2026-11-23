#!/usr/bin/env python3
"""Static GDPR analytics-consent UI regression gate; browser E2E remains required."""
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    "index.html": False, "hu.html": False, "de-at.html": False,
    "privacy-en.html": True, "privacy-hu.html": True, "privacy-de-at.html": True,
}
errors = []

class ScriptSources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.srcs = []
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.srcs.append(dict(attrs).get("src", ""))

for page, legal in PAGES.items():
    html = (ROOT / page).read_text(encoding="utf-8")
    required = ("id=\"cookieBanner\"", "data-analytics-accept", "data-analytics-reject",
                "/assets/js/analytics-consent.v20260713.js")
    for marker in required:
        if html.count(marker) != 1:
            errors.append(f"{page}: expected one {marker}; found {html.count(marker)}")
    if legal and html.count("data-cookie-settings") != 1:
        errors.append(f"{page}: settings cannot be reopened to withdraw consent")
    parser = ScriptSources()
    parser.feed(html)
    for src in parser.srcs:
        if src.startswith(("https://www.googletagmanager.com/", "https://www.google-analytics.com/")):
            errors.append(f"{page}: unconditional remote analytics script: {src}")

js = (ROOT / "assets/js/analytics-consent.v20260713.js").read_text(encoding="utf-8")
for marker in ("if (existing === 'accept') enable(); else disable();",
               "if (choice === 'accept') enable(); else disable();",
               "document.querySelectorAll('[data-cookie-settings]')",
               "function disable()", "wipeCookies();",
               "banner.classList.toggle('visible', !!show);"):
    if marker not in js:
        errors.append("consent controller missing safety contract: " + marker)

print(f"GDPR static consent regression: {len(PAGES)} pages, {len(errors)} errors")
for error in errors:
    print("ERROR:", error)
raise SystemExit(bool(errors))
