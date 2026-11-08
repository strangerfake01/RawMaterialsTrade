#!/usr/bin/env python3
"""v2 remediation: product-specific FAQs, identity evidence, UX hardening.

Defaults to dry-run. Pass --write to apply.
Skips open PR #13 reserved pages. Does not invent commercial specs.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITE = "--write" in sys.argv
DATE = "2026-11-08"
BASE_SHA = "68d378ea18917742d91076d14e595c0968ec0406"
JS_NEW = "assets/js/site.v20261108.js"
CSS_NEW = "assets/css/a11y-fixes.v3.css"

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

GENERIC_FAQ_MARKERS = [
    "Is the CAS/EC identity enough to place an order?",
    "Elég a CAS/EK azonosító a rendeléshez?",
    "Reicht die CAS-/EG-Identität für eine Bestellung?",
    "Which documents are typically required?",
    "Milyen dokumentumok szoktak kelleni?",
    "Welche Dokumente werden typischerweise benötigt?",
    "Can an alternative grade be offered?",
    "Felajánlható alternatív minőség?",
    "Kann eine alternative Qualität angeboten werden?",
]


def lang_of(name: str) -> str:
    if name.startswith("hu-"):
        return "hu"
    if name.startswith("de-at-"):
        return "de"
    return "en"


def product_id_from_filename(name: str) -> str:
    return re.sub(r"^(en|hu|de-at)-", "", name).removesuffix(".html")


def first_cas(cas_field: str) -> str | None:
    m = re.search(r"\d{2,7}-\d{2}-\d", cas_field or "")
    return m.group(0) if m else None


def variant_flags(pid: str, ti: dict) -> dict:
    s = f"{pid} {ti.get('grade_en','')} {ti.get('concentration_en','')} {ti.get('form_en','')}".lower()
    return {
        "hydrate": any(x in s for x in ["hidrat", "hydrate", "pentahidrat", "dekahidrat", "tetrahidrat", "monohidrat", "hexahidrat", "dihidrat"]),
        "anhydrous": any(x in s for x in ["vizmentes", "anhydrous", "wasserfrei", "anhidrat"]),
        "solution": any(x in s for x in ["oldat", "solution", "lösung", "aq"]),
        "multi_conc": bool(re.search(r"\d+\s*%.*,.*\d+\s*%", str(ti.get("concentration_en") or ti.get("grade_en") or ""))),
        "food": pid.endswith("-food") or "food" in str(ti.get("grade_en") or "").lower(),
        "feed": pid.endswith("-feed"),
        "deicing": pid.endswith("-deicing"),
        "regenerated": "regeneralt" in pid or "regenerated" in s or "technisch" in s and "regener" in s,
        "pharmacopoeial": "pharmacopoe" in s or "gyogyszerkonyvi" in pid,
    }


def faqs_for(lang: str, p: dict, flags: dict, pc: dict | None, wd: dict | None) -> list[tuple[str, str]]:
    ti = p.get("technical_identity") or {}
    name = {"en": p.get("name_en"), "hu": p.get("name_hu"), "de": p.get("name_de")}[lang]
    cas = ti.get("cas") or ""
    ec = ti.get("ec") or ""
    formula = ti.get("formula") or ""
    grade = ti.get(f"grade_{lang}") or ti.get("grade_en") or ti.get("grade") or ""
    conc = ti.get(f"concentration_{lang}") or ti.get("concentration_en") or grade
    pack = ti.get(f"packaging_{lang}") or ti.get("packaging_en") or ti.get("packaging") or ""
    faqs: list[tuple[str, str]] = []

    if lang == "en":
        if flags["multi_conc"]:
            faqs.append((
                f"Which concentration of {name} should I request?",
                f"The catalogue lists these concentration options: {conc}. The suitable concentration depends on the intended process, handling limits and the exact supplier grade. State the target concentration or a reference product in the enquiry; we confirm against current SDS/TDS before offering.",
            ))
        if flags["hydrate"] or flags["anhydrous"]:
            faqs.append((
                f"Does hydrate form matter for {name}?",
                "Yes. Hydrated and anhydrous forms can differ in assay calculation, water contribution, dissolution and packaging. Confirm the required form (and CAS where form-specific) against the process recipe and supplier documentation.",
            ))
        if flags["solution"]:
            faqs.append((
                f"What must be confirmed for {name} as a solution?",
                "For solutions, confirm concentration, solvent/water basis, assay method, packaging (IBC/drum/tanker) and transport classification from the current SDS. Webpage concentration ranges are orientation only until the selected offer is documented.",
            ))
        if flags["food"] or flags["pharmacopoeial"]:
            faqs.append((
                f"When is {name} suitable for food or pharmacopoeial use?",
                "Food or pharmacopoeial suitability is not automatic from the chemical name. It depends on the selected grade, intended use and current supplier documentation (including any food-contact or pharmacopoeial evidence requested for that offer).",
            ))
        if flags["feed"]:
            faqs.append((
                f"What feed-specific checks apply to {name}?",
                "For feed use, confirm the exact composition/identity, intended feed application and current supplier documents. Where feed-additive authorisation or GMP+ scope is relevant, it must match the exact product and supplier — catalogue listing alone is not approval.",
            ))
        if flags["deicing"]:
            faqs.append((
                f"Which winter-service parameters matter for {name}?",
                "Clarify concentration or purity, physical form, packaging, delivery timing and any municipal/industrial specification referenced by the buyer. Suitability for road or process use is confirmed per enquiry against the selected grade documents.",
            ))
        if flags["regenerated"]:
            faqs.append((
                f"What is different about regenerated/technical {name}?",
                "Regenerated or technical grades may differ from virgin material in impurity profile and approved uses. Always compare the required specification and SDS before treating a regenerated grade as interchangeable.",
            ))
        # identity FAQ
        id_bits = []
        if cas:
            id_bits.append(f"CAS {cas}")
        if ec and re.match(r"\d{3}-\d{3}-\d", str(ec)):
            id_bits.append(f"EC {ec}")
        if formula and "confirm" not in str(formula).lower() and "beszállít" not in str(formula).lower():
            id_bits.append(f"formula {formula}")
        if pc and pc.get("formula"):
            id_bits.append(f"PubChem formula check {pc['formula']}")
        faqs.append((
            f"How is the chemical identity of {name} verified?",
            ("Identity is anchored on " + ", ".join(id_bits) + ". " if id_bits else "")
            + "Final commercial identity still requires the selected supplier SDS/TDS for the offered grade; Wikipedia/Wikidata links support disambiguation only.",
        ))
        pack_txt = f" Preferred packaging currently listed for orientation: {pack}." if pack and "confirm" not in pack.lower() else ""
        faqs.append((
            f"What should I send to request {name}?",
            "Send intended use, target grade/concentration or reference product, quantity and unit, packaging preference, delivery location, timing and required documents (SDS/TDS/CoA as needed)."
            + pack_txt
            + " If the grade is uncertain, describe the process so alternatives can be checked against documentation.",
        ))
    elif lang == "hu":
        if flags["multi_conc"]:
            faqs.append((
                f"Melyik {name} koncentrációt érdemes kérni?",
                f"A katalógusban szereplő koncentráció-opciók: {conc}. A megfelelő érték a folyamattól, a kezelési korlátoktól és a pontos beszállítói minőségről függ. Az ajánlatkérésben adja meg a célkoncentrációt vagy referencia terméket; megerősítés SDS/TDS alapján történik.",
            ))
        if flags["hydrate"] or flags["anhydrous"]:
            faqs.append((
                f"Számít a hidrátforma a(z) {name} esetén?",
                "Igen. A hidratált és vízmentes forma különbözhet a hatóanyag-számításban, a vízbevitelben, az oldódásban és a kiszerelésben. A kívánt formát (és ahol formafüggő, a CAS-t) a receptúra és a beszállítói dokumentáció alapján erősítsük meg.",
            ))
        if flags["solution"]:
            faqs.append((
                f"Mit kell tisztázni a(z) {name} oldatnál?",
                "Oldatoknál a koncentrációt, az oldószer/vízbázist, az analitikai módszert, a kiszerelést (IBC/hordó/tartályautó) és a szállítási besorolást az aktuális SDS alapján kell megerősíteni.",
            ))
        if flags["food"] or flags["pharmacopoeial"]:
            faqs.append((
                f"Mikor alkalmas a(z) {name} élelmiszeripari vagy gyógyszerkönyvi használatra?",
                "Az alkalmasság nem következik automatikusan a kémiai névből. A kiválasztott minőségen, a tervezett felhasználáson és az aktuális beszállítói dokumentáción múlik.",
            ))
        if flags["feed"]:
            faqs.append((
                f"Milyen takarmányipari ellenőrzés kell a(z) {name} esetén?",
                "Igazolni kell a pontos összetételt/azonosságot, a takarmánycélú felhasználást és az aktuális beszállítói dokumentumokat. Ahol engedélyezés vagy GMP+ hatókör releváns, az a konkrét termékre és beszállítóra vonatkozik.",
            ))
        if flags["deicing"]:
            faqs.append((
                f"Milyen téli útüzemeltetési paraméterek számítanak a(z) {name} esetén?",
                "Tisztázni kell a koncentrációt/tisztaságot, a fizikai formát, a kiszerelést, a szállítási időzítést és a vevő által hivatkozott specifikációt.",
            ))
        if flags["regenerated"]:
            faqs.append((
                f"Miben más a regenerált/technikai {name}?",
                "A regenerált vagy technikai minőség szennyezőprofilban és engedélyezett felhasználásban eltérhet a virgin anyagtól. Csere előtt mindig hasonlítsa össze a specifikációt és az SDS-t.",
            ))
        id_bits = []
        if cas:
            id_bits.append(f"CAS {cas}")
        if ec and re.match(r"\d{3}-\d{3}-\d", str(ec)):
            id_bits.append(f"EK {ec}")
        if formula and "confirm" not in str(formula).lower() and "beszállít" not in str(formula).lower() and "dokument" not in str(formula).lower():
            id_bits.append(f"képlet {formula}")
        faqs.append((
            f"Hogyan azonosítjuk a(z) {name} kémiai azonosságát?",
            ("Az azonosság kiindulópontja: " + ", ".join(id_bits) + ". " if id_bits else "")
            + "A végleges kereskedelmi azonosságot a kiválasztott beszállító SDS/TDS dokumentumaival erősítjük meg.",
        ))
        pack_txt = f" Orientációs kiszerelés a katalógusban: {pack}." if pack and "confirm" not in pack.lower() and "egyedileg" not in pack.lower() and "Beszállítói" not in pack else ""
        faqs.append((
            f"Mit küldjek a(z) {name} ajánlatkéréséhez?",
            "Adja meg a tervezett felhasználást, a célminőséget/koncentrációt vagy referencia terméket, a mennyiséget, a kiszerelést, a szállítási helyet, az időzítést és a szükséges dokumentumokat."
            + pack_txt,
        ))
    else:  # de
        if flags["multi_conc"]:
            faqs.append((
                f"Welche Konzentration von {name} soll ich anfragen?",
                f"Im Katalog genannte Konzentrationsoptionen: {conc}. Die geeignete Konzentration hängt vom Prozess, von Handhabungsgrenzen und der genauen Lieferantenqualität ab. Bitte Zielkonzentration oder Referenzprodukt angeben; Bestätigung erfolgt anhand aktueller SDS/TDS.",
            ))
        if flags["hydrate"] or flags["anhydrous"]:
            faqs.append((
                f"Ist die Hydratform bei {name} entscheidend?",
                "Ja. Hydratisierte und wasserfreie Formen können sich in Gehaltsberechnung, Wasseranteil, Löslichkeit und Verpackung unterscheiden. Die geforderte Form (und ggf. formspezifische CAS) ist gegen Rezeptur und Lieferantendokumentation zu bestätigen.",
            ))
        if flags["solution"]:
            faqs.append((
                f"Was ist bei {name} als Lösung zu klären?",
                "Bei Lösungen sind Konzentration, Lösemittel-/Wasserbasis, Analysenmethode, Verpackung (IBC/Fass/Tankwagen) und Transportklassifikation anhand der aktuellen SDS zu bestätigen.",
            ))
        if flags["food"] or flags["pharmacopoeial"]:
            faqs.append((
                f"Wann ist {name} für Lebensmittel- oder Arzneibuchanwendungen geeignet?",
                "Die Eignung folgt nicht automatisch aus dem chemischen Namen. Maßgeblich sind gewählte Qualität, Verwendungszweck und aktuelle Lieferantendokumentation.",
            ))
        if flags["feed"]:
            faqs.append((
                f"Welche futtermittelbezogenen Prüfungen gelten für {name}?",
                "Zu bestätigen sind genaue Zusammensetzung/Identität, Verwendungszweck und aktuelle Lieferantendokumente. Zulassung oder GMP+-Geltung muss zum konkreten Produkt und Lieferanten passen.",
            ))
        if flags["deicing"]:
            faqs.append((
                f"Welche Winterdienst-Parameter sind für {name} relevant?",
                "Konzentration/Reinheit, physikalische Form, Verpackung, Liefertermin und die vom Käufer referenzierte Spezifikation sind je Anfrage zu klären.",
            ))
        if flags["regenerated"]:
            faqs.append((
                f"Was unterscheidet regeneriertes/technisches {name}?",
                "Regenerierte oder technische Qualitäten können im Verunreinigungsprofil und in zulässigen Verwendungen von Virgin-Ware abweichen. Vor Austausch Spezifikation und SDS vergleichen.",
            ))
        id_bits = []
        if cas:
            id_bits.append(f"CAS {cas}")
        if ec and re.match(r"\d{3}-\d{3}-\d", str(ec)):
            id_bits.append(f"EG {ec}")
        if formula and "confirm" not in str(formula).lower() and "Basis" not in str(formula) and "dokument" not in str(formula).lower():
            id_bits.append(f"Formel {formula}")
        faqs.append((
            f"Wie wird die chemische Identität von {name} abgesichert?",
            ("Ausgangspunkt: " + ", ".join(id_bits) + ". " if id_bits else "")
            + "Die endgültige kommerzielle Identität wird mit SDS/TDS der gewählten Lieferantenqualität bestätigt.",
        ))
        pack_txt = f" Orientierende Verpackung laut Katalog: {pack}." if pack and "confirm" not in pack.lower() and "individuell" not in pack.lower() and "Anfrage" not in pack else ""
        faqs.append((
            f"Welche Angaben brauche ich für eine Anfrage zu {name}?",
            "Bitte Verwendungszweck, Zielqualität/Konzentration oder Referenzprodukt, Menge, Verpackung, Lieferort, Termin und benötigte Dokumente senden."
            + pack_txt,
        ))

    # Deduplicate / cap at 4 most specific
    seen = set()
    out = []
    for q, a in faqs:
        if q in seen:
            continue
        seen.add(q)
        out.append((q, a))
    return out[:4]


def checkpoints_html(lang: str, p: dict, flags: dict, pc: dict | None, wd: dict | None) -> str:
    ti = p.get("technical_identity") or {}
    cas = ti.get("cas") or ""
    ec = ti.get("ec") or ""
    formula = ti.get("formula") or ""
    items = []
    if lang == "en":
        title = "Procurement checkpoints for this material"
        if cas:
            items.append(f"<li><strong>Identity:</strong> confirm CAS {cas}" + (f" / EC {ec}" if re.match(r'\d{3}-\d{3}-\d', str(ec or '')) else "") + " on the selected supplier documents.</li>")
        if formula and "confirm" not in str(formula).lower() and "dokument" not in str(formula).lower():
            items.append(f"<li><strong>Formula orientation:</strong> {formula}" + (f" (PubChem reports {pc['formula']})" if pc and pc.get('formula') else "") + ". Batch assay remains supplier-document based.</li>")
        if flags["hydrate"] or flags["anhydrous"]:
            items.append("<li><strong>Form:</strong> hydrate vs anhydrous / solid vs solution must match the process recipe.</li>")
        if flags["multi_conc"]:
            items.append(f"<li><strong>Concentration:</strong> choose among listed options ({ti.get('concentration_en') or ti.get('grade_en')}) and confirm assay method.</li>")
        if flags["food"] or flags["feed"] or flags["pharmacopoeial"]:
            items.append("<li><strong>Regulated use:</strong> request the exact grade evidence for food/feed/pharmacopoeial suitability; do not infer from the chemical name alone.</li>")
        items.append("<li><strong>Documents:</strong> SDS always; TDS/CoA where the application requires them.</li>")
        if wd:
            items.append(f"<li><strong>Entity check:</strong> Wikidata {wd.get('qid')} ({wd.get('label')}) matched by CAS for disambiguation — not a commercial certification.</li>")
    elif lang == "hu":
        title = "Beszerzési ellenőrzőpontok ehhez az anyaghoz"
        if cas:
            items.append(f"<li><strong>Azonosság:</strong> a kiválasztott beszállítói dokumentumokon ellenőrizze a CAS {cas}" + (f" / EK {ec}" if re.match(r'\d{3}-\d{3}-\d', str(ec or '')) else "") + " adatot.</li>")
        if formula and "confirm" not in str(formula).lower() and "beszállít" not in str(formula).lower() and "dokument" not in str(formula).lower():
            items.append(f"<li><strong>Képlet (orientáció):</strong> {formula}" + (f" (PubChem: {pc['formula']})" if pc and pc.get('formula') else "") + ". A tételes analízis beszállítói dokumentum alapján történik.</li>")
        if flags["hydrate"] or flags["anhydrous"]:
            items.append("<li><strong>Forma:</strong> hidrát vs vízmentes / szilárd vs oldat egyezzen a receptúrával.</li>")
        if flags["multi_conc"]:
            items.append(f"<li><strong>Koncentráció:</strong> a listázott opciók közül ({ti.get('concentration_hu') or ti.get('concentration_en') or ti.get('grade_hu')}) válasszon, és erősítse meg az analitikai módszert.</li>")
        if flags["food"] or flags["feed"] or flags["pharmacopoeial"]:
            items.append("<li><strong>Szabályozott használat:</strong> élelmiszer/takarmány/gyógyszerkönyvi alkalmassághoz a pontos minőség bizonyítékát kérje; a kémiai név önmagában nem elég.</li>")
        items.append("<li><strong>Dokumentumok:</strong> mindig SDS; TDS/CoA ahol az alkalmazás megkívánja.</li>")
        if wd:
            items.append(f"<li><strong>Entitásellenőrzés:</strong> Wikidata {wd.get('qid')} ({wd.get('label')}) CAS alapján — nem kereskedelmi tanúsítás.</li>")
    else:
        title = "Beschaffungs-Checkpunkte für diesen Stoff"
        if cas:
            items.append(f"<li><strong>Identität:</strong> CAS {cas}" + (f" / EG {ec}" if re.match(r'\d{3}-\d{3}-\d', str(ec or '')) else "") + " in den gewählten Lieferantendokumenten bestätigen.</li>")
        if formula and "confirm" not in str(formula).lower() and "Basis" not in str(formula) and "dokument" not in str(formula).lower():
            items.append(f"<li><strong>Formel (Orientierung):</strong> {formula}" + (f" (PubChem: {pc['formula']})" if pc and pc.get('formula') else "") + ". Chargenanalyse bleibt dokumentenbasiert.</li>")
        if flags["hydrate"] or flags["anhydrous"]:
            items.append("<li><strong>Form:</strong> Hydrat vs. wasserfrei / fest vs. Lösung muss zur Rezeptur passen.</li>")
        if flags["multi_conc"]:
            items.append(f"<li><strong>Konzentration:</strong> unter den gelisteten Optionen ({ti.get('concentration_de') or ti.get('concentration_en') or ti.get('grade_de')}) wählen und Analysenmethode bestätigen.</li>")
        if flags["food"] or flags["feed"] or flags["pharmacopoeial"]:
            items.append("<li><strong>Regulierte Verwendung:</strong> Lebensmittel-/Futtermittel-/Arzneibucheignung nur mit passender Qualitätsdokumentation — nicht allein aus dem Namen ableiten.</li>")
        items.append("<li><strong>Dokumente:</strong> stets SDS; TDS/CoA sofern die Anwendung es erfordert.</li>")
        if wd:
            items.append(f"<li><strong>Entity-Check:</strong> Wikidata {wd.get('qid')} ({wd.get('label')}) per CAS — keine kommerzielle Zertifizierung.</li>")
    return f'<section class="product-checkpoints" aria-labelledby="checkpointsHeading"><h2 id="checkpointsHeading">{title}</h2><ul>{"".join(items)}</ul></section>'


def faq_section(lang: str, faqs: list[tuple[str, str]], qualify_href: str) -> str:
    label = {"en": "See the qualification method", "hu": "Tekintse meg a minősítési módszert", "de": "Zur Qualifizierungsmethode"}[lang]
    h2 = {"en": "Purchasing questions for this material", "hu": "Beszerzési kérdések ehhez az anyaghoz", "de": "Beschaffungsfragen zu diesem Stoff"}[lang]
    body = "".join(f'<details class="sub-accordion rich-accordion"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    return f'<section class="product-faq" aria-labelledby="productFaqHeading"><h2 id="productFaqHeading">{h2}</h2>{body}<p class="microcopy"><a href="{qualify_href}">{label}</a></p></section>'


def replace_faq_and_checkpoints(html: str, lang: str, section_faq: str, section_cp: str) -> str:
    html = re.sub(r'<section class="product-faq"[\s\S]*?</section>\s*', "", html)
    html = re.sub(r'<section class="product-checkpoints"[\s\S]*?</section>\s*', "", html)
    # insert checkpoints before dual-path if present, else before faq insertion point
    if 'class="product-dual-path"' in html or 'aria-labelledby="dualPathHeading"' in html:
        # Repair accidentally truncated dual-path open tags from earlier runs.
        html = re.sub(
            r'</section>\s*aria-labelledby="dualPathHeading">',
            '</section><section class="product-dual-path" aria-labelledby="dualPathHeading">',
            html,
        )
        if 'class="product-checkpoints"' not in html:
            html = html.replace(
                '<section class="product-dual-path"',
                section_cp + '<section class="product-dual-path"',
                1,
            )
        else:
            # refresh checkpoints: drop old then insert before dual-path
            html = re.sub(r'<section class="product-checkpoints"[\s\S]*?</section>\s*', '', html)
            html = html.replace(
                '<section class="product-dual-path"',
                section_cp + '<section class="product-dual-path"',
                1,
            )
        html = re.sub(
            r'(<section class="product-dual-path"[\s\S]*?</section>)',
            r'\1' + section_faq,
            html,
            count=1,
        )
    elif re.search(r"<h2[^>]*>\s*(Related materials|Kapcsolódó|Verwandte)", html, re.I):
        html = re.sub(
            r"(<h2[^>]*>\s*(?:Related materials|Kapcsolódó[^<]*|Verwandte[^<]*)\s*</h2>)",
            section_cp + section_faq + r"\1",
            html,
            count=1,
            flags=re.I,
        )
    elif "</article>" in html:
        html = html.replace("</article>", section_cp + section_faq + "</article>", 1)
    else:
        html += section_cp + section_faq
    return html


def update_faq_jsonld(html: str, page_url: str, faqs: list[tuple[str, str]]) -> str:
    node = {
        "@type": "FAQPage",
        "@id": f"{page_url}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }

    def repl(m: re.Match) -> str:
        raw = m.group(1)
        try:
            data = json.loads(raw)
        except Exception:
            return m.group(0)
        if isinstance(data, dict) and isinstance(data.get("@graph"), list):
            data["@graph"] = [x for x in data["@graph"] if not (isinstance(x, dict) and x.get("@type") == "FAQPage")]
            data["@graph"].append(node)
            return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'
        if isinstance(data, list):
            data = [x for x in data if not (isinstance(x, dict) and x.get("@type") == "FAQPage")]
            data.append(node)
            return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'
        return m.group(0)

    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, html, count=1, flags=re.S)


def bump_assets(html: str) -> str:
    html = html.replace("/assets/js/site.v20260709d.js", "/" + JS_NEW)
    html = html.replace("/assets/css/a11y-fixes.v2.css", "/" + CSS_NEW)
    html = html.replace("assets/js/site.v20260709d.js", JS_NEW)
    html = html.replace("assets/css/a11y-fixes.v2.css", CSS_NEW)
    return html


def harden_js(src: str) -> str:
    # Remove any hide-on-footer logic if present; keep permanent visibility.
    src = re.sub(
        r"\n\s*const footer=document\.querySelector\('footer'\);[\s\S]*?updateVisibility\(\);\n",
        "\n  // Permanent visibility: do not hide on footer or cookie banner.\n",
        src,
    )
    if "Permanent visibility" not in src:
        src = src.replace(
            "document.body.appendChild(root);",
            "document.body.appendChild(root);\n  root.hidden=false;\n  // Permanent visibility: do not hide on footer or cookie banner.",
            1,
        )
    # Ensure hidden attribute cannot stick
    if "root.hidden=false" not in src:
        src = src.replace("document.body.appendChild(root);", "document.body.appendChild(root);\n  root.hidden=false;", 1)
    return src


def build_css(old: str) -> str:
    # strip old fab blocks and append v3 token system
    css = re.sub(
        r"/\* Persistent multilingual contact control[\s\S]*?@media print\{\.rmt-contact-fab\{display:none!important\}\}",
        "",
        old,
    )
    css = re.sub(
        r"/\* Shared floating control tokens[\s\S]*?@media print\{\.rmt-contact-fab,\.cookie-settings-toggle\{display:none!important\}\}\n?",
        "",
        css,
    )
    css = re.sub(r"\.rmt-contact-fab\{position:fixed;[\s\S]*?@media print\{\.rmt-contact-fab\{display:none!important\}\}", "", css)
    addon = """
/* Shared floating controls + product intelligence surfaces (v3) */
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
}
.cookie-settings-toggle{position:fixed;left:max(1rem,env(safe-area-inset-left));bottom:max(1rem,env(safe-area-inset-bottom));background:#1f2937;color:#fff;z-index:var(--rmt-float-z);cursor:pointer}
.rmt-contact-fab{position:fixed;right:max(1rem,env(safe-area-inset-right));bottom:max(1rem,env(safe-area-inset-bottom));z-index:var(--rmt-float-z);display:flex!important;flex-direction:column;align-items:flex-end;gap:8px;visibility:visible!important;opacity:1!important}
.rmt-contact-options[hidden]{display:none!important}
.rmt-contact-trigger{order:2;background:#142b3e;color:#fff;cursor:pointer}
.rmt-contact-options{order:1;max-width:min(300px,calc(100vw - 32px));padding:8px;border:1px solid #c5ccd3;border-radius:12px;background:#fff;box-shadow:0 8px 28px rgba(0,0,0,.18)}
.rmt-contact-options a{display:block;min-height:44px;padding:12px;color:#142b3e;text-decoration:none;border-radius:6px}
.rmt-contact-options a:hover,.rmt-contact-options a:focus-visible{background:#edf2f6;text-decoration:underline}
.rmt-contact-trigger:focus-visible,.rmt-contact-options a:focus-visible,.cookie-settings-toggle:focus-visible{outline:3px solid #f3b84a;outline-offset:3px}
.product-dual-path,.product-checkpoints,.product-faq{margin:1.25rem 0}
.dual-path-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem}
.dual-path-card{padding:1rem 1.1rem;border:1px solid rgba(20,43,62,.14);border-radius:12px;background:#fff}
.dual-path-card h3,.product-checkpoints h2,.product-faq h2{color:#142b3e}
.product-checkpoints ul{margin:.4rem 0 0;padding-left:1.1rem}
.product-checkpoints li{margin:.35rem 0;line-height:1.45;color:#1f2937}
.qualification-note,.catalogue-trust-note{margin:.55rem 0 .85rem;max-width:46rem;line-height:1.45;font-size:.95rem}
.product-hero-detail .qualification-note,.product-hero-detail .catalogue-trust-note{color:#e8eef7}
.product-hero-detail .qualification-note a,.product-hero-detail .catalogue-trust-note a{color:#9bdcf0;text-decoration:underline;text-underline-offset:.18em}
.product-hero-detail .product-hero-copy .lead,.product-hero-detail .product-hero-copy p{color:#e8eef7}
.product-dl dt{color:#334155}
.product-dl dd{color:#0f172a}
.sub-accordion>summary{color:#142b3e}
@media(max-width:600px){
  .cookie-settings-toggle,.rmt-contact-fab{bottom:max(12px,env(safe-area-inset-bottom))}
  .cookie-settings-toggle{left:max(12px,env(safe-area-inset-left))}
  .rmt-contact-fab{right:max(12px,env(safe-area-inset-right))}
  .product-dl, table{display:block;max-width:100%;overflow-x:auto}
}
@media print{.rmt-contact-fab,.cookie-settings-toggle{display:none!important}}
"""
    return css.rstrip() + "\n" + addon + "\n"


def main() -> None:
    lookup = json.loads((ROOT / "audits/external-identity-lookup.json").read_text(encoding="utf-8"))
    wd_by_cas = lookup["wikidata_by_cas"]
    pc_by_cas = lookup["pubchem_by_cas"]
    products = {p["id"]: p for p in json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))}

    # assets
    js_src = (ROOT / "assets/js/site.v20260709d.js").read_text(encoding="utf-8")
    js_new = harden_js(js_src)
    css_src = (ROOT / "assets/css/a11y-fixes.v2.css").read_text(encoding="utf-8")
    css_new = build_css(css_src)
    if WRITE:
        (ROOT / JS_NEW).write_text(js_new, encoding="utf-8")
        (ROOT / CSS_NEW).write_text(css_new, encoding="utf-8")

    changed = {JS_NEW, CSS_NEW, "tools/rmt_product_master_remediation_v2.py"}
    source_rows = []
    entity_rows = []
    n_faq = 0

    qualify = {
        "en": "how-we-qualify-a-raw-material.html",
        "hu": "hu-alapanyag-minosites.html",
        "de": "de-at-rohstoffqualifizierung.html",
    }

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
            html = replace_faq_and_checkpoints(
                html,
                lang,
                faq_section(lang, faqs, qualify[lang]),
                checkpoints_html(lang, p, flags, pc, wd),
            )
            html = update_faq_jsonld(html, f"https://www.rawmaterialstrade.com/{name}", faqs)
            html = re.sub(r'("dateModified"\s*:\s*")[^"]+(")', rf"\g<1>{DATE}\2", html, count=1)
            n_faq += 1

            if lang == "en" and cas:
                source_rows.append({
                    "product_id": pid,
                    "claim": f"CAS {cas} chemical identity",
                    "source_type": "PubChem",
                    "source_url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{pc['cid']}" if pc and pc.get("cid") else f"https://pubchem.ncbi.nlm.nih.gov/#query={cas}",
                    "accessed": DATE,
                    "evidence_status": "verified" if pc and pc.get("formula") else "needs-confirmation",
                    "notes": f"PubChem formula={pc.get('formula') if pc else 'n/a'}; catalogue formula={ti.get('formula')}",
                })
                if wd:
                    source_rows.append({
                        "product_id": pid,
                        "claim": f"Wikidata entity for CAS {cas}",
                        "source_type": "Wikidata",
                        "source_url": f"https://www.wikidata.org/wiki/{wd['qid']}",
                        "accessed": DATE,
                        "evidence_status": "verified",
                        "notes": f"label={wd.get('label')}; sameAs only after human review of hydrate/solution context",
                    })
                source_rows.append({
                    "product_id": pid,
                    "claim": "ECHA substance information entry point",
                    "source_type": "ECHA",
                    "source_url": f"https://echa.europa.eu/search-for-chemicals?p_p_id=echarevsubstance_WAR_echarevsubstanceportlet&_echarevsubstance_WAR_echarevsubstanceportlet_searchKeyword={cas}",
                    "accessed": DATE,
                    "evidence_status": "editorial-link",
                    "notes": "Search entry by CAS; CLP/REACH details confirmed per selected SDS",
                })
                wiki = (p.get("wikipedia") or {}).get("en")
                match = "needs-confirmation"
                if wd and wiki:
                    label = (wd.get("label") or "").lower().replace(" ", "_")
                    match = "verified" if label and label.split("(")[0].strip("_") in wiki.lower().replace("%28", "(").replace("%29", ")") else "needs-confirmation"
                entity_rows.append({
                    "id": pid,
                    "cas": cas,
                    "wikidata_qid": wd.get("qid") if wd else None,
                    "wikidata_label": wd.get("label") if wd else None,
                    "wikipedia_en": wiki,
                    "sameAs_status": match if match == "verified" else "needs-confirmation",
                    "pubchem_cid": pc.get("cid") if pc else None,
                    "pubchem_formula": pc.get("formula") if pc else None,
                })

        if html != original:
            if WRITE:
                path.write_text(html, encoding="utf-8")
            changed.add(name)

    # entity registry + source register outputs prepared later in HANDOFF writer
    if WRITE:
        (ROOT / "entity-registry.json").write_text(
            json.dumps({"schemaVersion": "2.0", "baseCommit": BASE_SHA, "generated": DATE, "entities": entity_rows}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        changed.add("entity-registry.json")
        (ROOT / "audits/source-register-generated.json").write_text(json.dumps(source_rows, ensure_ascii=False, indent=2), encoding="utf-8")
        changed.add("audits/source-register-generated.json")
        changed.add("audits/external-identity-lookup.json")

    print(f"[{'WRITE' if WRITE else 'DRY'}] faq pages={n_faq} files~={len(changed)} entity_rows={len(entity_rows)} source_rows={len(source_rows)}")


if __name__ == "__main__":
    main()
