#!/usr/bin/env python3
"""Safe one-shot injector for v2 product-specific FAQs + checkpoints.

Assumes pages already have product-dual-path from prior remediation.
Does not touch PR #13 reserved files.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Reuse FAQ builders from v2 module
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rmt_product_master_remediation_v2 import (  # noqa: E402
    RESERVED,
    DATE,
    JS_NEW,
    CSS_NEW,
    first_cas,
    faqs_for,
    faq_section,
    checkpoints_html,
    update_faq_jsonld,
    variant_flags,
    lang_of,
    product_id_from_filename,
    bump_assets,
)

ROOT = Path(__file__).resolve().parents[1]
WRITE = "--write" in sys.argv
QUAL = {
    "en": "how-we-qualify-a-raw-material.html",
    "hu": "hu-alapanyag-minosites.html",
    "de": "de-at-rohstoffqualifizierung.html",
}


def main() -> None:
    lookup = json.loads((ROOT / "audits/external-identity-lookup.json").read_text(encoding="utf-8"))
    wd_by_cas = lookup["wikidata_by_cas"]
    pc_by_cas = lookup["pubchem_by_cas"]
    products = {p["id"]: p for p in json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))}

    n = 0
    for path in sorted(ROOT.glob("*.html")):
        name = path.name
        if name in RESERVED:
            continue
        original = path.read_text(encoding="utf-8")
        html = bump_assets(original)

        is_product = bool(
            re.match(r"^(en|hu|de-at)-.+\.html$", name)
            and any(name.endswith(s) for s in ("-industrial.html", "-food.html", "-feed.html", "-deicing.html"))
        )
        if is_product:
            lang = lang_of(name)
            pid = product_id_from_filename(name)
            p = products.get(pid)
            if not p:
                continue
            ti = p.get("technical_identity") or {}
            cas = first_cas(str(ti.get("cas") or ""))
            flags = variant_flags(pid, ti)
            pc = pc_by_cas.get(cas or "") if cas else None
            wd = wd_by_cas.get(cas or "") if cas else None
            faqs = faqs_for(lang, p, flags, pc, wd)
            cp = checkpoints_html(lang, p, flags, pc, wd)
            faq = faq_section(lang, faqs, QUAL[lang])

            # drop prior generated blocks
            html = re.sub(r'<section class="product-faq"[\s\S]*?</section>\s*', "", html)
            html = re.sub(r'<section class="product-checkpoints"[\s\S]*?</section>\s*', "", html)

            if 'class="product-dual-path"' not in html:
                print("WARN missing dual-path", name)
                continue

            html = html.replace(
                '<section class="product-dual-path"',
                cp + '<section class="product-dual-path"',
                1,
            )
            # After dual-path closing section that contains dualPathHeading
            html = re.sub(
                r'(<section class="product-dual-path"[\s\S]*?</section>)',
                r"\1" + faq,
                html,
                count=1,
            )
            html = update_faq_jsonld(html, f"https://www.rawmaterialstrade.com/{name}", faqs)
            html = re.sub(r'("dateModified"\s*:\s*")[^"]+(")', rf"\g<1>{DATE}\2", html, count=1)
            n += 1

        if html != original and WRITE:
            path.write_text(html, encoding="utf-8")

    print(f"[{'WRITE' if WRITE else 'DRY'}] injected product pages={n}")


if __name__ == "__main__":
    main()
