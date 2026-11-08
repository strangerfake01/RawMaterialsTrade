#!/usr/bin/env python3
"""Final completion v3: integrate PR #13 pages + harden entity sameAs + quality audit helpers.

Run from repo root: python3 tools/rmt_final_completion_v3.py --write
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITE = "--write" in sys.argv
DATE = "2026-11-08"

PR13 = [
    "en-bentonit-industrial.html",
    "hu-bentonit-industrial.html",
    "de-at-bentonit-industrial.html",
    "en-borkosav-l-food.html",
    "hu-borkosav-l-food.html",
    "de-at-borkosav-l-food.html",
    "en-butil-glikol-industrial.html",
    "hu-butil-glikol-industrial.html",
    "de-at-butil-glikol-industrial.html",
]

QUAL = {
    "en": ("How do we qualify this material?", "how-we-qualify-a-raw-material.html", "See the qualification method"),
    "hu": ("Hogyan minősítjük ezt az alapanyagot?", "hu-alapanyag-minosites.html", "Tekintse meg a minősítési módszert"),
    "de": ("Wie qualifizieren wir diesen Rohstoff?", "de-at-rohstoffqualifizierung.html", "Zur Qualifizierungsmethode"),
}


def lang_of(name: str) -> str:
    if name.startswith("hu-"):
        return "hu"
    if name.startswith("de-at-"):
        return "de"
    return "en"


def pid_of(name: str) -> str:
    return re.sub(r"^(en|hu|de-at)-", "", name).removesuffix(".html")


def bump_assets(html: str) -> str:
    return (
        html.replace("/assets/js/site.v20260709d.js", "/assets/js/site.v20261108.js")
        .replace("/assets/css/a11y-fixes.v2.css", "/assets/css/a11y-fixes.v3.css")
        .replace("assets/js/site.v20260709d.js", "assets/js/site.v20261108.js")
        .replace("assets/css/a11y-fixes.v2.css", "assets/css/a11y-fixes.v3.css")
    )


def ensure_qualification_note(html: str, lang: str) -> str:
    if "qualification-note" in html:
        return html
    q, href, label = QUAL[lang]
    note = f'<p class="qualification-note">{q} <a href="{href}">{label}</a></p>'
    # insert after lead paragraph in hero
    html2, n = re.subn(
        r'(<p class="lead">[\s\S]*?</p>)',
        r"\1" + note,
        html,
        count=1,
    )
    return html2 if n else html + note


def dual_path(lang: str) -> str:
    if lang == "en":
        return '''<section class="product-dual-path" aria-labelledby="dualPathHeading">
<h2 id="dualPathHeading">Buyer and supplier pathways</h2>
<div class="dual-path-grid">
<div class="dual-path-card">
<h3>I need this material</h3>
<p>For an actionable quotation, send the target grade or concentration, intended use, quantity, packaging preference, delivery location and required documents. We confirm the selected offer against current supplier SDS/TDS/CoA.</p>
<p><a class="btn btn-primary" href="/#contact">Request a quotation</a></p>
</div>
<div class="dual-path-card">
<h3>I can supply this material</h3>
<p>Manufacturers and distributors may propose available inventory or recurring supply. Provide identity/CAS where known, grade, specification, current documents, available quantity, origin region and logistics parameters. Publication on this page does not imply purchase, exclusivity or a guaranteed sales channel.</p>
<p><a class="btn btn-outline" href="sales-representation-distribution-partner-central-europe.html">Propose a supply partnership</a></p>
</div>
</div>
</section>'''
    if lang == "hu":
        return '''<section class="product-dual-path" aria-labelledby="dualPathHeading">
<h2 id="dualPathHeading">Vevői és beszállítói útvonalak</h2>
<div class="dual-path-grid">
<div class="dual-path-card">
<h3>Ezt az alapanyagot keresem</h3>
<p>Érdemi ajánlatkéréshez adja meg a célminőséget vagy koncentrációt, a felhasználást, a mennyiséget, a kiszerelést, a szállítási helyet és a szükséges dokumentumokat. A kiválasztott ajánlatot az aktuális beszállítói SDS/TDS/CoA alapján erősítjük meg.</p>
<p><a class="btn btn-primary" href="/hu.html#contact">Ajánlatkérés</a></p>
</div>
<div class="dual-path-card">
<h3>Ezt az alapanyagot kínálom</h3>
<p>Gyártók és forgalmazók jelezhetik a rendelkezésre álló készletet vagy visszatérő szállítást. Adja meg az azonosságot/CAS-t, a minőséget, a specifikációt, az aktuális dokumentumokat, a mennyiséget, az eredetet és a logisztikai paramétereket. Az oldalon való megjelenés nem jelent felvásárlást, kizárólagosságot vagy garantált értékesítést.</p>
<p><a class="btn btn-outline" href="hu-ertekesitesi-kepviselet-disztribucios-partner.html">Beszállítói együttműködés jelzése</a></p>
</div>
</div>
</section>'''
    return '''<section class="product-dual-path" aria-labelledby="dualPathHeading">
<h2 id="dualPathHeading">Einkäufer- und Lieferantenwege</h2>
<div class="dual-path-grid">
<div class="dual-path-card">
<h3>Ich benötige diesen Rohstoff</h3>
<p>Für eine belastbare Anfrage bitte Zielqualität oder Konzentration, Verwendungszweck, Menge, Verpackung, Lieferort und benötigte Dokumente angeben. Das gewählte Angebot bestätigen wir anhand aktueller Lieferanten-SDS/TDS/CoA.</p>
<p><a class="btn btn-primary" href="/de-at.html#contact">Angebot anfragen</a></p>
</div>
<div class="dual-path-card">
<h3>Ich kann diesen Rohstoff liefern</h3>
<p>Hersteller und Händler können verfügbare Mengen oder wiederkehrende Lieferungen vorschlagen. Bitte Identität/CAS, Qualität, Spezifikation, aktuelle Dokumente, Menge, Herkunft und Logistikparameter angeben. Die Veröffentlichung auf dieser Seite bedeutet keinen Ankauf, keine Exklusivität und keinen garantierten Absatzkanal.</p>
<p><a class="btn btn-outline" href="de-at-vertriebspartner-distribution-chemierohstoffe.html">Lieferpartnerschaft vorschlagen</a></p>
</div>
</div>
</section>'''


def product_blocks(lang: str, pid: str, p: dict) -> tuple[str, str, list[tuple[str, str]]]:
    """Return checkpoints HTML, FAQ HTML parts, FAQ pairs — product-specific for PR13 trio."""
    ti = p.get("technical_identity") or {}
    cas = ti.get("cas") or ""
    name = {"en": p.get("name_en"), "hu": p.get("name_hu"), "de": p.get("name_de")}[lang]
    proc = p.get("procurement") or {}

    if pid.startswith("bentonit"):
        if lang == "en":
            cp_items = [
                f"<li><strong>Identity:</strong> bentonite is a clay mineral product family (CAS {cas} commonly cited). Confirm mineralogy and grade on supplier documents — Wikipedia/Wikidata are orientation only.</li>",
                "<li><strong>Performance drivers:</strong> swelling capacity, particle size, moisture and montmorillonite content vary by deposit; do not treat grades as interchangeable.</li>",
                "<li><strong>Documents:</strong> request SDS/TDS and any available mineral/assay data for the offered grade before process approval.</li>",
                "<li><strong>Regulatory:</strong> REACH/CLP classification and any food/feed suitability must come from the selected SDS and intended-use assessment — not from the catalogue page.</li>",
            ]
            faqs = [
                ("Which bentonite properties should I specify?", "State the process (e.g. foundry, sealing, clarification, drilling) and critical properties such as swelling, particle size, moisture and mineral composition. Source and grade differences can change performance."),
                ("Can I substitute one bentonite grade for another?", "Not automatically. Grades differ by deposit and processing. Approve substitution only against a representative specification and process trial where needed."),
                ("What documents are needed for a bentonite offer?", "Typically SDS/TDS and any available assay or mineralogical data for the offered grade, plus quantity, packaging and delivery location."),
            ]
        elif lang == "hu":
            cp_items = [
                f"<li><strong>Azonosság:</strong> a bentonit agyagásvány-család (gyakran hivatkozott CAS: {cas}). Az ásványi összetételt és minőséget a beszállítói dokumentumokon erősítse meg.</li>",
                "<li><strong>Teljesítmény:</strong> duzzadóképesség, szemcseméret, nedvesség és montmorillonit-tartalom lelőhelyenként változik; a minőségek nem csereszabatosak automatikusan.</li>",
                "<li><strong>Dokumentumok:</strong> kérjen SDS/TDS-t és elérhető ásványi/analízis adatokat a felajánlott minőséghez.</li>",
                "<li><strong>Szabályozás:</strong> REACH/CLP és bármely élelmiszer/takarmány alkalmasság az aktuális SDS és a tervezett felhasználás alapján vizsgálandó.</li>",
            ]
            faqs = [
                ("Milyen bentonit-tulajdonságokat adjak meg?", "Adja meg a folyamatot (pl. öntöde, szigetelés, derítés, fúrás) és a kritikus tulajdonságokat: duzzadás, szemcseméret, nedvesség, ásványi összetétel."),
                ("Helyettesíthető-e egy bentonitminőség egy másikkal?", "Nem automatikusan. A lelőhely és a feldolgozás miatt a teljesítmény eltérhet; helyettesítést csak specifikáció és szükség szerint próba alapján hagyjon jóvá."),
                ("Milyen dokumentum kell bentonit ajánlathoz?", "Általában SDS/TDS és elérhető analízis/ásványtani adat, valamint mennyiség, kiszerelés és szállítási hely."),
            ]
        else:
            cp_items = [
                f"<li><strong>Identität:</strong> Bentonit ist eine Tonmineral-Produktfamilie (häufig CAS {cas}). Mineralogie und Qualität in den Lieferantendokumenten bestätigen.</li>",
                "<li><strong>Leistungsparameter:</strong> Quellvermögen, Korngröße, Feuchte und Montmorillonitgehalt variieren je Lagerstätte; Qualitäten sind nicht automatisch austauschbar.</li>",
                "<li><strong>Dokumente:</strong> SDS/TDS und verfügbare Mineral-/Analysedaten der angebotenen Qualität anfordern.</li>",
                "<li><strong>Regulatorik:</strong> REACH/CLP sowie ggf. Lebensmittel-/Futtermitteleignung ergeben sich aus SDS und Verwendungsbewertung — nicht aus der Katalogseite.</li>",
            ]
            faqs = [
                ("Welche Bentonit-Eigenschaften soll ich angeben?", "Prozess nennen (z. B. Gießerei, Abdichtung, Klärung, Bohrung) sowie Quellvermögen, Korngröße, Feuchte und mineralische Zusammensetzung."),
                ("Kann ich Bentonit-Qualitäten austauschen?", "Nicht automatisch. Herkunft und Aufbereitung ändern die Performance; Austausch nur nach Spezifikation und ggf. Erprobung freigeben."),
                ("Welche Dokumente brauche ich für ein Bentonit-Angebot?", "Typischerweise SDS/TDS und verfügbare Analyse-/Mineraldaten sowie Menge, Verpackung und Lieferort."),
            ]
    elif pid.startswith("borkosav"):
        if lang == "en":
            cp_items = [
                f"<li><strong>Identity:</strong> confirm L(+)-tartaric acid (CAS {cas}) versus other isomers/forms on the offer documents.</li>",
                "<li><strong>Food use:</strong> food-grade status is not automatic from the chemical name; request the food specification, assay and impurity limits for the actual supplier/batch.</li>",
                "<li><strong>Documents:</strong> SDS always; food TDS/CoA or batch evidence where the application requires them.</li>",
                "<li><strong>Regulatory:</strong> suitability under food law must be established for the selected grade and intended use — catalogue text is orientation only.</li>",
            ]
            faqs = [
                ("Why does the L(+) form matter?", "Food and process recipes may require specifically L(+)-tartaric acid. Confirm the stereochemistry on the supplier specification before approving the offer."),
                ("When is tartaric acid suitable for food use?", "Only when the selected grade is evidenced as suitable for the intended food application via current supplier documentation. Do not infer food compliance from CAS alone."),
                ("What should an RFQ include?", "Intended food application, required L(+) confirmation, quantity, bagged packaging preference, destination, timing and needed CoA/TDS language."),
            ]
        elif lang == "hu":
            cp_items = [
                f"<li><strong>Azonosság:</strong> az ajánlat dokumentumain erősítse meg az L(+)-borkősavat (CAS {cas}) más izomerekkel/formákkal szemben.</li>",
                "<li><strong>Élelmiszer:</strong> az élelmiszeripari minőség nem következik a kémiai névből; kérje a specifikációt, tisztaságot és szennyező-határértékeket a konkrét beszállítóra/tételre.</li>",
                "<li><strong>Dokumentumok:</strong> mindig SDS; élelmiszeripari TDS/CoA ahol szükséges.</li>",
                "<li><strong>Szabályozás:</strong> az élelmiszerjogi alkalmasságot a kiválasztott minőségre és felhasználásra kell igazolni.</li>",
            ]
            faqs = [
                ("Miért számít az L(+) forma?", "Az élelmiszeripari és technológiai receptúrák gyakran kifejezetten L(+)-borkősavat írnak elő. Az ajánlat elfogadása előtt ellenőrizze a sztereokémiát a specifikáción."),
                ("Mikor alkalmas élelmiszeripari használatra?", "Csak akkor, ha a kiválasztott minőség aktuális beszállítói dokumentációja igazolja az adott felhasználást. A CAS önmagában nem élelmiszer-megfelelőség."),
                ("Mit tartalmazzon az ajánlatkérés?", "Felhasználás, L(+) megerősítés, mennyiség, zsákos kiszerelés, cím, időzítés és szükséges CoA/TDS nyelv."),
            ]
        else:
            cp_items = [
                f"<li><strong>Identität:</strong> L(+)-Weinsäure (CAS {cas}) gegenüber anderen Isomeren/Formen in den Angebotsdokumenten bestätigen.</li>",
                "<li><strong>Lebensmittel:</strong> Lebensmittelqualität folgt nicht aus dem Namen; Spezifikation, Gehalt und Verunreinigungsgrenzen für Lieferant/Charge anfordern.</li>",
                "<li><strong>Dokumente:</strong> stets SDS; Lebensmittel-TDS/CoA sofern erforderlich.</li>",
                "<li><strong>Regulatorik:</strong> lebensmittelrechtliche Eignung für die gewählte Qualität und Verwendung belegen.</li>",
            ]
            faqs = [
                ("Warum ist die L(+)-Form entscheidend?", "Rezepte können ausdrücklich L(+)-Weinsäure fordern. Stereochemie vor Freigabe in der Spezifikation prüfen."),
                ("Wann ist Weinsäure für Lebensmittel geeignet?", "Nur mit aktueller Lieferantendokumentation für die konkrete Anwendung. CAS allein belegt keine Lebensmittelkonformität."),
                ("Was gehört in die Anfrage?", "Anwendung, L(+)-Bestätigung, Menge, Sackware, Lieferort, Termin und benötigte CoA/TDS-Sprache."),
            ]
    else:  # butyl glycol / 2-butoxyethanol
        if lang == "en":
            cp_items = [
                f"<li><strong>Identity:</strong> confirm 2-butoxyethanol (butyl glycol) CAS {cas} on the selected SDS.</li>",
                "<li><strong>Hazard/handling:</strong> review current SDS for classification, PPE, storage and transport — do not infer from the product name.</li>",
                "<li><strong>Technical grade:</strong> purity, water content and impurity profile must match the process specification before substitution.</li>",
                "<li><strong>Documents:</strong> SDS/TDS and available batch analysis; packaging usually drums/IBC as confirmed in the offer.</li>",
            ]
            faqs = [
                ("What purity and water limits should I request?", "State the required purity and water content for the industrial process. Technical grades differ; approve only against the offered TDS/CoA."),
                ("What SDS points are critical for butyl glycol?", "Check classification, exposure controls, storage compatibility and transport details on the current SDS for the exact offered grade."),
                ("Which packaging is typical?", "Orientation packaging includes 200 L drums and IBC; confirm fill, availability and transport classification in the quotation."),
            ]
        elif lang == "hu":
            cp_items = [
                f"<li><strong>Azonosság:</strong> a kiválasztott SDS-en erősítse meg a 2-butoxietanol (butil-glikol) CAS {cas} adatot.</li>",
                "<li><strong>Veszély/kezelés:</strong> az aktuális SDS szerinti besorolás, védőeszköz, tárolás és szállítás irányadó — a névből nem következtethető.</li>",
                "<li><strong>Technikai minőség:</strong> tisztaság, víztartalom és szennyezőprofil egyezzen a folyamat specifikációjával.</li>",
                "<li><strong>Dokumentumok:</strong> SDS/TDS és elérhető tételanalízis; kiszerelés jellemzően hordó/IBC az ajánlat szerint.</li>",
            ]
            faqs = [
                ("Milyen tisztaságot és víztartalmat kérjek?", "Adja meg a folyamat által megkívánt tisztaságot és víztartalmat. A technikai minőségek eltérhetnek; csak a felajánlott TDS/CoA alapján hagyja jóvá."),
                ("Mely SDS pontok kritikusak butil-glikolnál?", "Ellenőrizze a besorolást, az expozíció szabályozását, a tárolási összeférhetőséget és a szállítási adatokat az aktuális SDS-en."),
                ("Mi a tipikus kiszerelés?", "Orientáció: 200 L hordó és IBC; a töltést, készletet és szállítási besorolást az ajánlatban erősítse meg."),
            ]
        else:
            cp_items = [
                f"<li><strong>Identität:</strong> 2-Butoxyethanol (Butylglycol) CAS {cas} im gewählten SDS bestätigen.</li>",
                "<li><strong>Gefahr/Handhabung:</strong> Einstufung, PSA, Lagerung und Transport dem aktuellen SDS entnehmen — nicht aus dem Namen ableiten.</li>",
                "<li><strong>Technische Qualität:</strong> Reinheit, Wassergehalt und Verunreinigungsprofil müssen zur Prozessspezifikation passen.</li>",
                "<li><strong>Dokumente:</strong> SDS/TDS und verfügbare Chargenanalyse; Verpackung typischerweise Fass/IBC laut Angebot.</li>",
            ]
            faqs = [
                ("Welche Reinheit und Wassergrenzen soll ich anfragen?", "Prozessbezogene Reinheit und Wassergehalt angeben. Technische Qualitäten unterscheiden sich; Freigabe nur anhand TDS/CoA."),
                ("Welche SDS-Punkte sind bei Butylglycol kritisch?", "Einstufung, Expositionskontrollen, Lagerverträglichkeit und Transportangaben im aktuellen SDS der angebotenen Qualität prüfen."),
                ("Welche Verpackung ist üblich?", "Orientierung: 200-Liter-Fässer und IBC; Füllung, Verfügbarkeit und Transporteinstufung im Angebot bestätigen."),
            ]

    # Prefer RFQ text from PR13 procurement if present
    rfq = proc.get(f"rfq_guidance_{lang}") or proc.get("rfq_guidance_en")
    if rfq and lang == "en":
        faqs.append(("What should I send for a quotation?", rfq))
    elif rfq and lang == "hu" and len(faqs) < 4:
        faqs.append(("Mit küldjek ajánlatkéréshez?", rfq))
    elif rfq and lang == "de" and len(faqs) < 4:
        faqs.append(("Welche Angaben brauche ich für eine Anfrage?", rfq))

    title = {
        "en": "Procurement checkpoints for this material",
        "hu": "Beszerzési ellenőrzőpontok ehhez az anyaghoz",
        "de": "Beschaffungs-Checkpunkte für diesen Stoff",
    }[lang]
    h2 = {
        "en": "Purchasing questions for this material",
        "hu": "Beszerzési kérdések ehhez az anyaghoz",
        "de": "Beschaffungsfragen zu diesem Stoff",
    }[lang]
    qlink = QUAL[lang]
    cp = f'<section class="product-checkpoints" aria-labelledby="checkpointsHeading"><h2 id="checkpointsHeading">{title}</h2><ul>{"".join(cp_items)}</ul></section>'
    body = "".join(f'<details class="sub-accordion rich-accordion"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs[:4])
    faq = f'<section class="product-faq" aria-labelledby="productFaqHeading"><h2 id="productFaqHeading">{h2}</h2>{body}<p class="microcopy"><a href="{qlink[1]}">{qlink[2]}</a></p></section>'
    return cp, faq, faqs[:4]


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


def strip_false_sameas(html: str) -> str:
    """Remove schema.org sameAs arrays that point only to Wikipedia for form-ambiguous pages."""
    # Keep Wikipedia links in visible content; only strip machine sameAs when present.
    def repl(m: re.Match) -> str:
        raw = m.group(1)
        try:
            data = json.loads(raw)
        except Exception:
            return m.group(0)

        def walk(o):
            if isinstance(o, dict):
                if "sameAs" in o:
                    # Drop sameAs entirely unless it is a Wikidata QID list already confirmed elsewhere.
                    # Conservative: remove Wikipedia-only sameAs.
                    sa = o["sameAs"]
                    if isinstance(sa, str) and "wikipedia.org" in sa:
                        del o["sameAs"]
                    elif isinstance(sa, list):
                        kept = [x for x in sa if isinstance(x, str) and "wikidata.org" in x]
                        if kept:
                            o["sameAs"] = kept
                        else:
                            del o["sameAs"]
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for i in o:
                    walk(i)

        walk(data)
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'

    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, html, flags=re.S)


def soften_echa_checkpoints(html: str) -> str:
    """Ensure checkpoint wording does not claim ECHA compliance."""
    replacements = [
        (
            "matched by CAS for disambiguation — not a commercial certification.",
            "matched by CAS for disambiguation only — not REACH/CLP compliance or commercial certification.",
        ),
        (
            "CAS alapján — nem kereskedelmi tanúsítás.",
            "CAS alapján, csak azonosításhoz — nem REACH/CLP megfelelőség és nem kereskedelmi tanúsítás.",
        ),
        (
            "per CAS — keine kommerzielle Zertifizierung.",
            "per CAS nur zur Disambiguierung — keine REACH/CLP-Konformität und keine kommerzielle Zertifizierung.",
        ),
    ]
    for a, b in replacements:
        html = html.replace(a, b)
    return html


def harden_entity_registry() -> dict:
    path = ROOT / "entity-registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    ents = data.get("entities") or []
    form_risk = re.compile(r"(oldat|solution|regeneralt|regenerated|vizmentes|anhydrous|hidrat|hydrate|kever|mixture|%)", re.I)
    changed = 0
    for e in ents:
        pid = e.get("id") or ""
        status = e.get("sameAs_status")
        # Solutions, regenerated grades, anhydrous/hydrate ambiguity: never auto-verified sameAs
        if form_risk.search(pid) and status == "verified":
            e["sameAs_status"] = "needs-confirmation"
            e["sameAs_reason"] = "CAS match exists but product form/grade may differ from the Wikipedia/Wikidata entity; sameAs withheld."
            changed += 1
        elif status == "verified":
            e["sameAs_reason"] = "CAS matched Wikidata label heuristically aligned with Wikipedia EN URL; still review before promoting machine sameAs."
        else:
            e["sameAs_reason"] = e.get("sameAs_reason") or "Needs human confirmation before sameAs use."
    data["schemaVersion"] = "3.0"
    data["generated"] = DATE
    data["sameAs_policy"] = "sameAs only when substance form is unambiguous and human-confirmed; CAS alone is insufficient for solutions, hydrates, mixtures and regenerated grades."
    if WRITE:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"entities": len(ents), "downgraded": changed}


def integrate_pr13(products: dict) -> int:
    n = 0
    for name in PR13:
        path = ROOT / name
        html = bump_assets(path.read_text(encoding="utf-8"))
        lang = lang_of(name)
        pid = pid_of(name)
        p = products[pid]
        html = ensure_qualification_note(html, lang)
        # strip prior injected blocks if re-run
        html = re.sub(r'<section class="product-faq"[\s\S]*?</section>\s*', "", html)
        html = re.sub(r'<section class="product-checkpoints"[\s\S]*?</section>\s*', "", html)
        html = re.sub(r'<section class="product-dual-path"[\s\S]*?</section>\s*', "", html)
        cp, faq, faqs = product_blocks(lang, pid, p)
        block = cp + dual_path(lang) + faq
        if 'class="related-section"' in html:
            html = html.replace('<section class="related-section">', block + '<section class="related-section">', 1)
        elif re.search(r"<h2[^>]*>\s*(Related materials|Kapcsolódó|Verwandte)", html, re.I):
            html = re.sub(
                r"(<h2[^>]*>\s*(?:Related materials|Kapcsolódó[^<]*|Verwandte[^<]*)\s*</h2>)",
                block + r"\1",
                html,
                count=1,
                flags=re.I,
            )
        else:
            html += block
        html = update_faq_jsonld(html, f"https://www.rawmaterialstrade.com/{name}", faqs)
        html = re.sub(r'("dateModified"\s*:\s*")[^"]+(")', rf"\g<1>{DATE}\2", html, count=1)
        if WRITE:
            path.write_text(html, encoding="utf-8")
        n += 1
    return n


def soften_all_checkpoints() -> int:
    n = 0
    for path in ROOT.glob("*.html"):
        if not any(path.name.endswith(s) for s in ("-industrial.html", "-food.html", "-feed.html", "-deicing.html")):
            continue
        text = path.read_text(encoding="utf-8")
        new = soften_echa_checkpoints(text)
        # strip Wikipedia-only sameAs in JSON-LD for form-ambiguous products
        if any(k in path.name for k in ("oldat", "regeneralt", "vizmentes", "hidrat", "solution")):
            new = strip_false_sameas(new)
        if new != text:
            n += 1
            if WRITE:
                path.write_text(new, encoding="utf-8")
    return n


def main() -> None:
    products = {p["id"]: p for p in json.loads((ROOT / "products-multilingual.json").read_text(encoding="utf-8"))}
    pr = integrate_pr13(products)
    ent = harden_entity_registry()
    soft = soften_all_checkpoints()
    print(f"[{'WRITE' if WRITE else 'DRY'}] pr13_pages={pr} entity={ent} softened_pages={soft}")


if __name__ == "__main__":
    main()
