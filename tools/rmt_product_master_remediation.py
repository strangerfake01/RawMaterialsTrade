#!/usr/bin/env python3
"""Product catalogue intelligence + UX remediation for ZIP handoff.

Defaults to dry-run. Pass --write to apply.

Does NOT invent CAS/EC/specs/stock/prices/certifications.
Does NOT modify Cloudflare Worker/CSP/Turnstile/form endpoint.
Does NOT touch PR #13 reserved product pages.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITE = "--write" in sys.argv
DATE = "2026-11-08"
BASE_SHA = "51fad6f121de388d22e87724432000b434b64903"

RESERVED = {
    "en-bentonit-industrial.html",
    "hu-bentonit-industrial.html",
    "de-at-bentonit-industrial.html",
    "en-borkosav-l-food.html",
    "hu-borkosav-l-food.html",
    "de-at-borkosav-l-food.html",
    "en-butil-glikol-industrial.html",
    "hu-butil-glikol-industrial.html",
    "de-at-butil-glikol-industrial.html",
}

QUAL = {
    "en": "how-we-qualify-a-raw-material.html",
    "hu": "hu-alapanyag-minosites.html",
    "de": "de-at-rohstoffqualifizierung.html",
}
TRUST = {
    "en": "ai-trust-center.html",
    "hu": "hu-ai-bizalmi-kozpont.html",
    "de": "de-at-ai-vertrauenszentrum.html",
}
PARTNER = {
    "en": "sales-representation-distribution-partner-central-europe.html",
    "hu": "hu-ertekesitesi-kepviselet-disztribucios-partner.html",
    "de": "de-at-vertriebspartner-distribution-chemierohstoffe.html",
}
HOME = {"en": "/", "hu": "hu.html", "de": "de-at.html"}

COPY = {
    "en": {
        "qual_note": 'How do we qualify this material? <a href="{q}">See the qualification method</a>',
        "qual_feed": 'How do we qualify this feed material? <a href="{q}">See the qualification method</a>',
        "dual_h2": "Buyer and supplier pathways",
        "buyer_h3": "I need this material",
        "buyer_p": "For an actionable quotation, send the intended use, target grade or concentration, quantity and unit, preferred packaging, delivery country/city, timing, and required SDS/TDS/CoA or other documents. If the grade is uncertain, describe the process and we will help assess suitable options against current supplier documentation.",
        "buyer_cta": "Request a buyer quotation",
        "supplier_h3": "I can supply this material",
        "supplier_p": "Manufacturers and distributors may propose available inventory or recurring supply. Provide identity/CAS where known, grade, specification, current documents, available quantity, origin region and logistics parameters. Publication on this page does not imply purchase, exclusivity or a guaranteed sales channel.",
        "supplier_cta": "Propose a supply partnership",
        "faq_h2": "Purchasing questions",
        "faq1_q": "Is the CAS/EC identity enough to place an order?",
        "faq1_a": "No. Identity is the starting point. Grade, concentration, physical form, documentation and intended use must still be confirmed for the selected commercial offer.",
        "faq2_q": "Which documents are typically required?",
        "faq2_a": "Buyers commonly request SDS, and where relevant TDS and CoA, for the exact grade and supplier. Food or feed suitability depends on the selected product and current documentation, not on the webpage alone.",
        "faq3_q": "Can an alternative grade be offered?",
        "faq3_a": "Possible alternatives are compared on identity, composition, specification and application fit using current supplier documents. An unverified substitute is not presented as equivalent.",
        "cat_note": 'Need identity, grade or documentation checks? <a href="{q}">How we qualify a raw material</a> · <a href="{t}">AI Trust Center</a>',
        "cat_food": 'Food-grade documentation and qualification questions? <a href="{q}">Qualification method</a> · <a href="{t}">AI Trust Center</a>',
        "cat_feed": 'Feed-material documentation and qualification questions? <a href="{q}">Qualification method</a> · <a href="{t}">AI Trust Center</a>',
        "cat_deice": 'Winter-service grade or documentation questions? <a href="{q}">Qualification method</a> · <a href="{t}">AI Trust Center</a>',
        "cat_catalogue": 'Need help validating identity, grade, documents or supplier continuity? <a href="{q}">Qualification method</a> · <a href="{t}">AI Trust Center</a>',
    },
    "hu": {
        "qual_note": 'Hogyan minősítjük ezt az alapanyagot? <a href="{q}">Tekintse meg a minősítési módszert</a>',
        "qual_feed": 'Hogyan minősítjük ezt a takarmányipari alapanyagot? <a href="{q}">Tekintse meg a minősítési módszert</a>',
        "dual_h2": "Vevői és beszállítói útvonal",
        "buyer_h3": "Erre az alapanyagra van szükségem",
        "buyer_p": "Használható ajánlathoz adja meg a tervezett felhasználást, a célminőséget vagy koncentrációt, a mennyiséget és mértékegységet, a kívánt kiszerelést, a szállítási országot/várost, az időzítést, valamint a szükséges SDS/TDS/CoA vagy egyéb dokumentumokat. Ha a minőség bizonytalan, írja le a folyamatot; a lehetséges változatokat az aktuális beszállítói dokumentáció alapján értékeljük.",
        "buyer_cta": "Vevői ajánlatkérés",
        "supplier_h3": "Ezt az alapanyagot tudom szállítani",
        "supplier_p": "Gyártók és disztribútorok jelezhetnek elérhető készletet vagy rendszeres szállítást. Adja meg az azonosságot/CAS-t ha ismert, a minőséget, specifikációt, aktuális dokumentumokat, elérhető mennyiséget, származási régiót és logisztikai paramétereket. Az oldalon való megjelenés nem jelent vételi kötelezettséget, kizárólagosságot vagy garantált értékesítési csatornát.",
        "supplier_cta": "Beszállítói együttműködés jelzése",
        "faq_h2": "Beszerzési kérdések",
        "faq1_q": "Elég a CAS/EK azonosító a rendeléshez?",
        "faq1_a": "Nem. Az azonosság a kiindulópont. A minőséget, koncentrációt, fizikai formát, dokumentációt és a tervezett felhasználást a kiválasztott kereskedelmi ajánlatra külön meg kell erősíteni.",
        "faq2_q": "Milyen dokumentumok szoktak kelleni?",
        "faq2_a": "A vevők jellemzően SDS-t, és ahol releváns, TDS-t és CoA-t kérnek a pontos minőséghez és beszállítóhoz. Az élelmiszer- vagy takarmányalkalmasság a kiválasztott terméktől és az aktuális dokumentációtól függ, nem önmagában a weboldaltól.",
        "faq3_q": "Felajánlható alternatív minőség?",
        "faq3_a": "A lehetséges alternatívákat azonosság, összetétel, specifikáció és alkalmazási illeszkedés alapján vetjük össze az aktuális beszállítói dokumentumokkal. Nem igazolt helyettesítőt nem állítunk egyenértékűnek.",
        "cat_note": 'Azonosítás, minőség vagy dokumentáció kérdés? <a href="{q}">Így minősítünk egy alapanyagot</a> · <a href="{t}">AI Bizalmi Központ</a>',
        "cat_food": 'Élelmiszeripari dokumentációs és minősítési kérdés? <a href="{q}">Minősítési módszer</a> · <a href="{t}">AI Bizalmi Központ</a>',
        "cat_feed": 'Takarmányipari dokumentációs és minősítési kérdés? <a href="{q}">Minősítési módszer</a> · <a href="{t}">AI Bizalmi Központ</a>',
        "cat_deice": 'Téli útüzemeltetési minőség vagy dokumentáció kérdés? <a href="{q}">Minősítési módszer</a> · <a href="{t}">AI Bizalmi Központ</a>',
        "cat_catalogue": 'Segítség az azonosítás, minőség, dokumentumok vagy beszállítói folytonosság ellenőrzéséhez? <a href="{q}">Minősítési módszer</a> · <a href="{t}">AI Bizalmi Központ</a>',
    },
    "de": {
        "qual_note": 'Wie qualifizieren wir diesen Rohstoff? <a href="{q}">Zur Qualifizierungsmethode</a>',
        "qual_feed": 'Wie qualifizieren wir diesen Futtermittelrohstoff? <a href="{q}">Zur Qualifizierungsmethode</a>',
        "dual_h2": "Wege für Einkäufer und Lieferanten",
        "buyer_h3": "Ich benötige diesen Rohstoff",
        "buyer_p": "Für ein belastbares Angebot senden Sie Verwendungszweck, Zielqualität oder Konzentration, Menge und Einheit, bevorzugte Verpackung, Lieferland/-ort, Termin sowie erforderliche SDS/TDS/CoA oder andere Dokumente. Ist die Qualität unklar, beschreiben Sie den Prozess; mögliche Varianten prüfen wir anhand aktueller Lieferantendokumentation.",
        "buyer_cta": "Einkäuferangebot anfragen",
        "supplier_h3": "Ich kann diesen Rohstoff liefern",
        "supplier_p": "Hersteller und Distributoren können verfügbare Mengen oder wiederkehrende Lieferung vorschlagen. Bitte Identität/CAS falls bekannt, Qualität, Spezifikation, aktuelle Dokumente, verfügbare Menge, Herkunftsregion und Logistikparameter angeben. Die Veröffentlichung auf dieser Seite bedeutet keinen Kauf, keine Exklusivität und keinen garantierten Absatzkanal.",
        "supplier_cta": "Lieferpartnerschaft vorschlagen",
        "faq_h2": "Fragen zur Beschaffung",
        "faq1_q": "Reicht die CAS-/EG-Identität für eine Bestellung?",
        "faq1_a": "Nein. Die Identität ist der Ausgangspunkt. Qualität, Konzentration, physikalische Form, Dokumentation und Verwendungszweck müssen für das konkrete Angebot weiterhin bestätigt werden.",
        "faq2_q": "Welche Dokumente werden typischerweise benötigt?",
        "faq2_a": "Einkäufer fordern üblicherweise SDS und, soweit relevant, TDS sowie CoA für die genaue Qualität und den Lieferanten an. Lebensmittel- oder Futtermittelgeeignetheit hängt vom gewählten Produkt und der aktuellen Dokumentation ab — nicht allein von der Webseite.",
        "faq3_q": "Kann eine alternative Qualität angeboten werden?",
        "faq3_a": "Mögliche Alternativen werden anhand von Identität, Zusammensetzung, Spezifikation und Anwendungsfit mit aktuellen Lieferantendokumenten verglichen. Ein nicht verifizierter Ersatz wird nicht als gleichwertig dargestellt.",
        "cat_note": 'Fragen zu Identität, Qualität oder Dokumentation? <a href="{q}">Zur Rohstoffqualifizierung</a> · <a href="{t}">AI-Vertrauenszentrum</a>',
        "cat_food": 'Fragen zu lebensmittelbezogenen Dokumenten und Qualifizierung? <a href="{q}">Qualifizierungsmethode</a> · <a href="{t}">AI-Vertrauenszentrum</a>',
        "cat_feed": 'Fragen zu Futtermittel-Dokumenten und Qualifizierung? <a href="{q}">Qualifizierungsmethode</a> · <a href="{t}">AI-Vertrauenszentrum</a>',
        "cat_deice": 'Fragen zu Winterdienst-Qualität oder Dokumentation? <a href="{q}">Qualifizierungsmethode</a> · <a href="{t}">AI-Vertrauenszentrum</a>',
        "cat_catalogue": 'Unterstützung bei Identität, Qualität, Dokumenten oder Lieferkontinuität? <a href="{q}">Qualifizierungsmethode</a> · <a href="{t}">AI-Vertrauenszentrum</a>',
    },
}

CATEGORY_FILES = {
    "en-industrial-chemicals.html": ("en", "cat_note"),
    "hu-ipari-vegyipari-alapanyagok.html": ("hu", "cat_note"),
    "de-at-industriechemikalien.html": ("de", "cat_note"),
    "en-food-raw-materials.html": ("en", "cat_food"),
    "hu-elelmiszeripari-alapanyagok.html": ("hu", "cat_food"),
    "de-at-lebensmittelrohstoffe.html": ("de", "cat_food"),
    "en-feed-raw-materials.html": ("en", "cat_feed"),
    "hu-takarmanyipari-alapanyagok.html": ("hu", "cat_feed"),
    "de-at-futtermittelrohstoffe.html": ("de", "cat_feed"),
    "en-deicing-materials.html": ("en", "cat_deice"),
    "hu-teli-utszorasi-anyagok.html": ("hu", "cat_deice"),
    "de-at-winterdienst-streumittel.html": ("de", "cat_deice"),
    "en-catalogue.html": ("en", "cat_catalogue"),
    "hu-termekkatalogus.html": ("hu", "cat_catalogue"),
    "de-at-produktkatalog.html": ("de", "cat_catalogue"),
}


def lang_of(name: str) -> str:
    if name.startswith("hu-") or name == "hu.html":
        return "hu"
    if name.startswith("de-at-") or name == "de-at.html":
        return "de"
    return "en"


def is_product(name: str) -> bool:
    return bool(
        re.match(r"^(en|hu|de-at)-.+\.html$", name)
        and any(name.endswith(s) for s in ("-industrial.html", "-food.html", "-feed.html", "-deicing.html"))
    )


def bump_date(html: str) -> str:
    return re.sub(r'("dateModified"\s*:\s*")[^"]+(")', rf"\g<1>{DATE}\2", html, count=1)


def inject_after_h1(html: str, note_html: str) -> str:
    html = re.sub(
        r"\s*<p class=\"(?:qualification-note|catalogue-trust-note)\">.*?</p>",
        "",
        html,
        flags=re.I | re.S,
    )
    note = f'<p class="qualification-note">{note_html}</p>'
    return re.sub(r"(</h1>)", r"\1" + note, html, count=1, flags=re.I)


def strip_internal_arrows(html: str) -> str:
    internal = set(QUAL.values()) | set(TRUST.values()) | set(PARTNER.values())

    def repl(m: re.Match) -> str:
        tag, inner = m.group(1), m.group(2)
        href_m = re.search(r'href=["\']([^"\']+)["\']', tag, re.I)
        if not href_m:
            return m.group(0)
        path = href_m.group(1).split("#", 1)[0].split("?", 1)[0].rsplit("/", 1)[-1]
        if path in internal and "↗" in inner:
            return f"<a{tag}>{inner.replace(' ↗', '').replace('↗', '')}</a>"
        return m.group(0)

    return re.sub(r"<a([^>]+)>(.*?)</a>", repl, html, flags=re.I | re.S)


def dual_and_faq_block(lang: str, product_href_home: str) -> str:
    c = COPY[lang]
    q = QUAL[lang]
    partner = PARTNER[lang]
    home = HOME[lang]
    buyer_href = f"{home}#contact" if home != "/" else "/#contact"
    qual_link_label = {
        "en": "See the qualification method",
        "hu": "Tekintse meg a minősítési módszert",
        "de": "Zur Qualifizierungsmethode",
    }[lang]
    return f'''<section class="product-dual-path" aria-labelledby="dualPathHeading">
<h2 id="dualPathHeading">{c["dual_h2"]}</h2>
<div class="dual-path-grid">
<div class="dual-path-card">
<h3>{c["buyer_h3"]}</h3>
<p>{c["buyer_p"]}</p>
<p><a class="btn btn-primary" href="{buyer_href}">{c["buyer_cta"]}</a></p>
</div>
<div class="dual-path-card">
<h3>{c["supplier_h3"]}</h3>
<p>{c["supplier_p"]}</p>
<p><a class="btn btn-outline" href="{partner}">{c["supplier_cta"]}</a></p>
</div>
</div>
</section>
<section class="product-faq" aria-labelledby="productFaqHeading">
<h2 id="productFaqHeading">{c["faq_h2"]}</h2>
<details class="sub-accordion rich-accordion"><summary>{c["faq1_q"]}</summary><p>{c["faq1_a"]}</p></details>
<details class="sub-accordion rich-accordion"><summary>{c["faq2_q"]}</summary><p>{c["faq2_a"]}</p></details>
<details class="sub-accordion rich-accordion"><summary>{c["faq3_q"]}</summary><p>{c["faq3_a"]}</p></details>
<p class="microcopy"><a href="{q}">{qual_link_label}</a></p>
</section>'''


def faq_schema(lang: str, page_url: str) -> dict:
    c = COPY[lang]
    return {
        "@type": "FAQPage",
        "@id": f"{page_url}#faq",
        "mainEntity": [
            {"@type": "Question", "name": c["faq1_q"], "acceptedAnswer": {"@type": "Answer", "text": c["faq1_a"]}},
            {"@type": "Question", "name": c["faq2_q"], "acceptedAnswer": {"@type": "Answer", "text": c["faq2_a"]}},
            {"@type": "Question", "name": c["faq3_q"], "acceptedAnswer": {"@type": "Answer", "text": c["faq3_a"]}},
        ],
    }


def inject_blocks(html: str, lang: str, name: str) -> str:
    # remove previous generated blocks for idempotency
    html = re.sub(r'<section class="product-dual-path"[\s\S]*?</section>\s*', "", html)
    html = re.sub(r'<section class="product-faq"[\s\S]*?</section>\s*', "", html)
    block = dual_and_faq_block(lang, name)
    # insert before related materials h2 if present, else before closing article
    if re.search(r"<h2[^>]*>\s*Related materials", html, re.I) or re.search(
        r"<h2[^>]*>\s*(Kapcsolódó|Verwandte)", html, re.I
    ):
        html = re.sub(
            r"(<h2[^>]*>\s*(?:Related materials|Kapcsolódó[^<]*|Verwandte[^<]*)\s*</h2>)",
            block + r"\1",
            html,
            count=1,
            flags=re.I,
        )
    elif "</article>" in html:
        html = html.replace("</article>", block + "</article>", 1)
    else:
        html += block

    # FAQ schema: append into first JSON-LD @graph if present and FAQPage not already there
    if "FAQPage" not in html:
        page_url = f"https://www.rawmaterialstrade.com/{name}"
        faq = json.dumps(faq_schema(lang, page_url), ensure_ascii=False)
        def add_graph(m: re.Match) -> str:
            raw = m.group(1)
            try:
                data = json.loads(raw)
            except Exception:
                return m.group(0)
            node = json.loads(faq)
            if isinstance(data, dict) and isinstance(data.get("@graph"), list):
                data["@graph"].append(node)
                return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'
            if isinstance(data, list):
                data.append(node)
                return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'
            return m.group(0)

        html = re.sub(
            r'<script type="application/ld\+json">(.*?)</script>',
            add_graph,
            html,
            count=1,
            flags=re.S,
        )
    return html


def fix_floating_css(css: str) -> str:
    """Shared control tokens: cookie (left) and contact (right) matched."""
    block = """
/* Shared floating control tokens — cookie left, contact right */
:root{
  --rmt-float-pad-y:.5rem;
  --rmt-float-pad-x:.8rem;
  --rmt-float-font:.74rem;
  --rmt-float-radius:999px;
  --rmt-float-min-h:44px;
  --rmt-float-z:1000;
  --rmt-float-shadow:0 8px 22px rgba(0,0,0,.18);
}
.cookie-settings-toggle,
.rmt-contact-trigger{
  min-height:var(--rmt-float-min-h);
  min-width:var(--rmt-float-min-h);
  padding:var(--rmt-float-pad-y) var(--rmt-float-pad-x);
  font-size:var(--rmt-float-font);
  line-height:1.2;
  font-weight:600;
  border-radius:var(--rmt-float-radius);
  border:1px solid rgba(255,255,255,.28);
  box-shadow:var(--rmt-float-shadow);
  z-index:var(--rmt-float-z);
}
.cookie-settings-toggle{position:fixed;left:max(1rem,env(safe-area-inset-left));bottom:max(1rem,env(safe-area-inset-bottom));background:#1f2937;color:#fff;z-index:var(--rmt-float-z)}
.rmt-contact-fab{position:fixed;right:max(1rem,env(safe-area-inset-right));bottom:max(1rem,env(safe-area-inset-bottom));z-index:var(--rmt-float-z);display:flex;flex-direction:column;align-items:flex-end;gap:8px}
.rmt-contact-options[hidden]{display:none!important}
.rmt-contact-trigger{order:2;background:#142b3e;color:#fff;cursor:pointer}
.rmt-contact-options{order:1;max-width:min(300px,calc(100vw - 32px));padding:8px;border:1px solid #c5ccd3;border-radius:12px;background:#fff;box-shadow:0 8px 28px rgba(0,0,0,.18)}
.rmt-contact-options a{display:block;min-height:44px;padding:12px;color:#142b3e;text-decoration:none;border-radius:6px}
.rmt-contact-options a:hover,.rmt-contact-options a:focus-visible{background:#edf2f6;text-decoration:underline}
.rmt-contact-trigger:focus-visible,.rmt-contact-options a:focus-visible,.cookie-settings-toggle:focus-visible{outline:3px solid #f3b84a;outline-offset:3px}
.product-dual-path{margin:1.5rem 0 1.25rem}
.dual-path-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem}
.dual-path-card{padding:1rem 1.1rem;border:1px solid rgba(20,43,62,.14);border-radius:12px;background:#fff}
.dual-path-card h3{margin:.2rem 0 .55rem;font-size:1.05rem;color:#142b3e}
.product-faq{margin:1rem 0 1.5rem}
.qualification-note,.catalogue-trust-note{margin:.55rem 0 .85rem;max-width:46rem;line-height:1.45;font-size:.95rem}
.product-hero-detail .qualification-note,.product-hero-detail .catalogue-trust-note{color:#e8eef7}
.product-hero-detail .qualification-note a,.product-hero-detail .catalogue-trust-note a{color:#9bdcf0;text-decoration:underline;text-underline-offset:.18em}
.catalogue-page-hero .qualification-note a,.catalogue-page-hero .catalogue-trust-note a{color:#9bdcf0;text-decoration:underline;text-underline-offset:.18em}
@media(max-width:600px){
  .cookie-settings-toggle,.rmt-contact-fab{bottom:max(12px,env(safe-area-inset-bottom))}
  .cookie-settings-toggle{left:max(12px,env(safe-area-inset-left))}
  .rmt-contact-fab{right:max(12px,env(safe-area-inset-right))}
}
@media print{.rmt-contact-fab,.cookie-settings-toggle{display:none!important}}
"""
    # replace previous generated blocks / old fab rules
    css = re.sub(
        r"/\* Shared floating control tokens[\s\S]*?@media print\{\.rmt-contact-fab,\.cookie-settings-toggle\{display:none!important\}\}\n?",
        "",
        css,
    )
    css = re.sub(
        r"\.rmt-contact-fab\{position:fixed;[\s\S]*?@media print\{\.rmt-contact-fab\{display:none!important\}\}",
        "",
        css,
    )
    return css.rstrip() + "\n" + block + "\n"


def ensure_js_never_hides(js: str) -> str:
    # Remove footer/cookie hide logic if any remnant remains
    js = re.sub(
        r"\n\s*const footer=document\.querySelector\('footer'\);[\s\S]*?updateVisibility\(\);\n",
        "\n  // Contact FAB remains permanently visible; panel still closes on outside click or Escape.\n",
        js,
    )
    if "permanently visible" not in js and "Contact FAB remains" not in js:
        js = js.replace(
            "document.body.appendChild(root);",
            "document.body.appendChild(root);\n  // Contact FAB remains permanently visible while scrolling, at the footer and during consent.",
            1,
        )
    return js


def build_entity_registry(products: list) -> list:
    rows = []
    for p in products:
        ti = p.get("technical_identity") or {}
        wiki = p.get("wikipedia") or {}
        rows.append(
            {
                "id": p.get("id"),
                "name_en": p.get("name_en"),
                "cas": ti.get("cas") or None,
                "ec": ti.get("ec") or None,
                "formula": ti.get("formula") or None,
                "wikipedia": wiki if isinstance(wiki, dict) else {"url": wiki} if wiki else None,
                "wiki_check": p.get("wiki_check"),
                "sameAs_status": "needs-confirmation",
                "provenance": "repository-catalogue",
                "accessed": DATE,
            }
        )
    return rows


def main() -> None:
    changed: set[str] = set()
    products = json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))
    if isinstance(products, dict):
        products = products.get("products", [])

    # CSS + JS UX fixes
    css_path = ROOT / "assets/css/a11y-fixes.v2.css"
    css = fix_floating_css(css_path.read_text(encoding="utf-8"))
    if WRITE:
        css_path.write_text(css, encoding="utf-8")
    changed.add(css_path.relative_to(ROOT).as_posix())

    js_path = ROOT / "assets/js/site.v20260709d.js"
    js_orig = js_path.read_text(encoding="utf-8")
    js = ensure_js_never_hides(js_orig)
    if js != js_orig:
        if WRITE:
            js_path.write_text(js, encoding="utf-8")
        changed.add(js_path.relative_to(ROOT).as_posix())

    # products
    touched_products = 0
    for path in sorted(ROOT.glob("*.html")):
        name = path.name
        if name in RESERVED:
            continue
        original = path.read_text(encoding="utf-8")
        html = strip_internal_arrows(original)
        lang = lang_of(name)

        if is_product(name):
            c = COPY[lang]
            note = (c["qual_feed"] if name.endswith("-feed.html") else c["qual_note"]).format(q=QUAL[lang])
            html = inject_after_h1(html, note)
            html = inject_blocks(html, lang, name)
            html = bump_date(html)
            touched_products += 1

        if name in CATEGORY_FILES:
            lg, key = CATEGORY_FILES[name]
            note = COPY[lg][key].format(q=QUAL[lg], t=TRUST[lg])
            # catalogue uses catalogue-trust-note class preference
            html = re.sub(
                r"\s*<p class=\"(?:qualification-note|catalogue-trust-note)\">.*?</p>",
                "",
                html,
                flags=re.I | re.S,
            )
            cls = "catalogue-trust-note" if "catalogue" in name or "katalog" in name or "termekkatalogus" in name or "produktkatalog" in name else "qualification-note"
            html = re.sub(r"(</h1>)", rf'\1<p class="{cls}">{note}</p>', html, count=1, flags=re.I)
            html = bump_date(html)

        if html != original:
            if WRITE:
                path.write_text(html, encoding="utf-8")
            changed.add(name)

    # entity registry
    registry = {
        "schemaVersion": "1.0",
        "baseCommit": BASE_SHA,
        "generated": DATE,
        "note": "Identifiers come from the repository catalogue. Wikipedia/Wikidata links require human confirmation before sameAs use.",
        "entities": build_entity_registry(products),
    }
    reg_path = ROOT / "entity-registry.json"
    if WRITE:
        reg_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    changed.add("entity-registry.json")

    # sitemap lastmod for changed html
    if WRITE and changed:
        sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for name in sorted(changed):
            if not name.endswith(".html"):
                continue
            loc = f"https://www.rawmaterialstrade.com/{name}"
            sm, _ = re.subn(
                rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]+(</lastmod>)",
                rf"\g<1>{DATE}\2",
                sm,
                count=1,
            )
        (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")
        changed.add("sitemap.xml")

    mode = "WRITE" if WRITE else "DRY-RUN"
    print(f"[{mode}] product pages targeted={touched_products} reserved_skipped={len(RESERVED)}")
    print(f"[{mode}] files changed={len(changed)}")
    for n in sorted(changed)[:25]:
        print(" ", n)
    if len(changed) > 25:
        print(f"  ... +{len(changed)-25} more")


if __name__ == "__main__":
    main()
