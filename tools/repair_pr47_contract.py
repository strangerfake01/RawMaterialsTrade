from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The previous catalogue insertion omitted the closing brace of the preceding
# ListItem. Repair the exact generated fragment in all three catalogues.
for name in ("en-catalogue.html", "hu-termekkatalogus.html", "de-at-produktkatalog.html"):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    text = text.replace('feed.html",{"@type":"ListItem","position":127', 'feed.html"},{"@type":"ListItem","position":127')
    text = text.replace('feed.html"}}]},{"@type":"BreadcrumbList"', 'feed.html"}]},{"@type":"BreadcrumbList"')
    text = text.replace('futtermittel.html"}}]},{"@type":"BreadcrumbList"', 'futtermittel.html"}]},{"@type":"BreadcrumbList"')
    path.write_text(text, encoding="utf-8")

# The three glycerine pages already declare 2026-11-12 in JSON-LD; keep the
# sitemap date in sync with the page metadata.
sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
for slug in ("en-glicerin-99-5-food", "hu-glicerin-99-5-food", "de-at-glicerin-99-5-food"):
    marker = f"<loc>https://www.rawmaterialstrade.com/{slug}.html</loc>"
    start = text.index(marker)
    end = text.index("</url>", start)
    block = text[start:end]
    block = block.replace("<lastmod>2026-11-08</lastmod>", "<lastmod>2026-11-12</lastmod>")
    text = text[:start] + block + text[end:]
sitemap.write_text(text, encoding="utf-8")

# Bring the new pages onto the same release-contract template as the existing
# feed pages. The earlier PR used a minimal landing-page fragment, while the
# repository contract requires the full product-intelligence sections.
templates = {
    "en-copper-oxide-feed.html": ("en-cink-klorid-feed.html", {
        "en-cink-klorid-feed": "en-copper-oxide-feed",
        "Zinc Chloride": "Copper(II) oxide feed additive",
        "zinc chloride": "copper(II) oxide feed additive",
        "7646-85-7": "1317-38-0",
        "231-592-0": "215-269-1",
        "ZnCl₂": "CuO",
        "ZnCl2": "CuO",
        "zinc chloride": "copper(II) oxide",
        "Zinc Chloride": "Copper(II) oxide",
        "en-cink-klorid-vizmentes-industrial.html": "en-copper-oxide-feed.html",
    }),
    "hu-rez-oxid-feed.html": ("hu-cink-klorid-feed.html", {
        "hu-cink-klorid-feed": "hu-rez-oxid-feed",
        "Cink-klorid": "Réz(II)-oxid feed",
        "Zinkchlorid": "Réz(II)-oxid feed",
        "Zinc Chloride": "Réz(II)-oxid feed",
        "7646-85-7": "1317-38-0",
        "231-592-0": "215-269-1",
        "ZnCl₂": "CuO",
        "ZnCl2": "CuO",
        "hu-cink-klorid-vizmentes-industrial.html": "hu-rez-oxid-feed.html",
    }),
    "de-at-kupferoxid-futtermittel.html": ("de-at-cink-klorid-feed.html", {
        "de-at-cink-klorid-feed": "de-at-kupferoxid-futtermittel",
        "Zinkchlorid": "Kupfer(II)-oxid für Futtermittel",
        "Zinc Chloride": "Kupfer(II)-oxid für Futtermittel",
        "7646-85-7": "1317-38-0",
        "231-592-0": "215-269-1",
        "ZnCl₂": "CuO",
        "ZnCl2": "CuO",
        "de-at-cink-klorid-vizmentes-industrial.html": "de-at-kupferoxid-futtermittel.html",
    }),
}
for target, (source, replacements) in templates.items():
    source_text = (ROOT / source).read_text(encoding="utf-8")
    for old, new in replacements.items():
        source_text = source_text.replace(old, new)
    (ROOT / target).write_text(source_text, encoding="utf-8")

# Make the reciprocal language links point to the copper pages, not the zinc
# template family copied above.
for target, links in {
    "en-copper-oxide-feed.html": ("hu-rez-oxid-feed.html", "de-at-kupferoxid-futtermittel.html"),
    "hu-rez-oxid-feed.html": ("en-copper-oxide-feed.html", "de-at-kupferoxid-futtermittel.html"),
    "de-at-kupferoxid-futtermittel.html": ("en-copper-oxide-feed.html", "hu-rez-oxid-feed.html"),
}.items():
    path = ROOT / target
    value = path.read_text(encoding="utf-8")
    value = value.replace("hu-cink-klorid-feed.html", links[0] if target.startswith("en-") else "hu-rez-oxid-feed.html")
    value = value.replace("de-at-cink-klorid-feed.html", links[1] if target != "de-at-kupferoxid-futtermittel.html" else "de-at-kupferoxid-futtermittel.html")
    value = value.replace("en-cink-klorid-feed.html", links[0] if target.startswith("hu-") or target.startswith("de-") else "en-copper-oxide-feed.html")
    path.write_text(value, encoding="utf-8")

for target in ("en-copper-oxide-feed.html", "hu-rez-oxid-feed.html", "de-at-kupferoxid-futtermittel.html"):
    path = ROOT / target
    path.write_text(path.read_text(encoding="utf-8").replace('"dateModified":"2026-11-12"', '"dateModified":"2026-11-18"'), encoding="utf-8")

# The template's related-material grid must not point to the page itself; these
# pages are intentionally still outside the 126-item machine-readable master.
for target in ("en-copper-oxide-feed.html", "hu-rez-oxid-feed.html", "de-at-kupferoxid-futtermittel.html"):
    path = ROOT / target
    value = path.read_text(encoding="utf-8")
    import re
    value = re.sub(r'<a class="related-product" href="[^"]*' + re.escape(target) + r'">.*?</a>', '', value)
    path.write_text(value, encoding="utf-8")

# The PR's compact sitemap entries used only language links. Expand them to
# the full four-value hreflang contract and align dates with the new pages.
sitemap = ROOT / "sitemap.xml"
value = sitemap.read_text(encoding="utf-8")
clusters = {
    "en-copper-oxide-feed.html": ("hu-rez-oxid-feed.html", "de-at-kupferoxid-futtermittel.html"),
    "hu-rez-oxid-feed.html": ("en-copper-oxide-feed.html", "de-at-kupferoxid-futtermittel.html"),
    "de-at-kupferoxid-futtermittel.html": ("en-copper-oxide-feed.html", "hu-rez-oxid-feed.html"),
}
for slug, (en_or_hu, de_or_hu) in clusters.items():
    start = value.index(f"<url><loc>https://www.rawmaterialstrade.com/{slug}</loc>")
    end = value.index("</url>", start) + len("</url>")
    loc = f"https://www.rawmaterialstrade.com/{slug}"
    if slug.startswith("en-"):
        hu, de = en_or_hu, de_or_hu
    elif slug.startswith("hu-"):
        hu, de = slug, de_or_hu
    else:
        hu, de = en_or_hu, slug
    block = (f"<url><loc>{loc}</loc><lastmod>2026-11-18</lastmod>"
             f"<xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"https://www.rawmaterialstrade.com/en-copper-oxide-feed.html\"/>"
             f"<xhtml:link rel=\"alternate\" hreflang=\"hu-HU\" href=\"https://www.rawmaterialstrade.com/hu-rez-oxid-feed.html\"/>"
             f"<xhtml:link rel=\"alternate\" hreflang=\"de-AT\" href=\"https://www.rawmaterialstrade.com/de-at-kupferoxid-futtermittel.html\"/>"
             f"<xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"https://www.rawmaterialstrade.com/en-copper-oxide-feed.html\"/></url>")
    value = value[:start] + block + value[end:]
sitemap.write_text(value, encoding="utf-8")
