#!/usr/bin/env python3
"""Make each published multilingual product footer link to its privacy notice.

Static HTML, independent of JavaScript and the consent banner. The operation
never touches products, chemistry, schemas, dates, commercial data or forms.
Default mode is read-only verification; --apply is restricted to product routes.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE_OVERRIDES = {
    "copper-oxide-feed": {
        "en": "en-copper-oxide-feed.html",
        "hu": "hu-rez-oxid-feed.html",
        "de-at": "de-at-kupferoxid-futtermittel.html",
    }
}
NOTICES = {
    "en": ("privacy-en.html", "Privacy Policy", "en"),
    "hu": ("privacy-hu.html", "Adatvédelmi tájékoztató", "hu-HU"),
    "de-at": ("privacy-de-at.html", "Datenschutzerklärung", "de-AT"),
}
FOOTER = '<footer class="site-footer">'
TAIL = '</p></div></footer>'


def inspect() -> tuple[list[tuple[Path, str]], list[str]]:
    products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    changes: list[tuple[Path, str]] = []
    if len(products) != 127:
        errors.append(f"Unexpected product master size {len(products)}, expected reviewed 127")
    found: set[str] = set()
    for product in products:
        pid = product.get("id")
        if not isinstance(pid, str) or not pid:
            errors.append("Invalid product id; refusing edits")
            continue
        for prefix, (href, label, language) in NOTICES.items():
            name = ROUTE_OVERRIDES.get(pid, {}).get(prefix, f"{prefix}-{pid}.html")
            if name in found:
                errors.append(f"{name}: duplicate route")
                continue
            found.add(name)
            path = ROOT / name
            if not path.is_file():
                errors.append(f"{name}: missing product page")
                continue
            source = path.read_text(encoding="utf-8")
            if not re.search(r'<html\\s+lang=["\']' + re.escape(language) + r'["\']', source, re.I):
                errors.append(f"{name}: unexpected HTML language")
                continue
            if source.count(FOOTER) != 1:
                errors.append(f"{name}: missing or duplicated static footer")
                continue
            before, footer = source.split(FOOTER, 1)
            if footer.count(TAIL) != 1:
                errors.append(f"{name}: unexpected footer structure")
                continue
            expected = f'<a href="{href}">{label}</a>'
            if expected not in footer.split(TAIL, 1)[0]:
                replacement = f' · {expected}' + TAIL
                revised = before + FOOTER + footer.replace(TAIL, replacement, 1)
                changes.append((path, revised))
    if len(found) != 381:
        errors.append(f"Expected 381 distinct localized routes, found {len(found)}")
    return changes, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Write exactly the verified static privacy footer links")
    args = parser.parse_args()
    changes, errors = inspect()
    if errors:
        for error in errors[:30]:
            print("ERROR:", error)
        return 1
    if args.apply:
        for path, source in changes:
            path.write_text(source, encoding="utf-8")
        print(f"Applied privacy footer links on {len(changes)} of 381 product pages")
        return 0
    print(f"Product privacy footer links: 381 inspected; missing={len(changes)}")
    for path, _ in changes[:15]:
        print("MISSING:", path.name)
    return 1 if changes else 0


if __name__ == "__main__":
    raise SystemExit(main())
