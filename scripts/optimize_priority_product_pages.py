from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

TEXT = {
    "en": {
        "heading": "Decision guide for procurement",
        "intro": "Before requesting an offer, confirm the points below. The catalogue is an orientation; the selected supplier grade, batch and current documentation determine the final suitability.",
        "items": [
            ("Identity", "Use the CAS number and, where relevant, hydrate/form and concentration to avoid comparing different commercial forms."),
            ("Application", "State the intended process and end use. Food, feed, cosmetic, water-treatment and industrial uses can require different grades and evidence."),
            ("Commercial details", "Include quantity, unit, packaging, delivery country/site and requested delivery date. Availability, MOQ, Incoterms and lead time are confirmed in the written offer."),
            ("Documents", "Request the current SDS as a minimum; request TDS/specification and lot-specific CoA when the application or quality system requires them."),
            ("Approval checkpoint", "Do not infer regulatory suitability, certification or batch conformity from the catalogue name, PubChem, Wikipedia or Wikidata. Confirm it against the offered supplier documents."),
        ],
        "cta": "If the required grade or form is uncertain, describe the process and target result in the enquiry so suitable alternatives can be checked.",
    },
    "hu": {
        "heading": "Beszerzési döntéstámogató útmutató",
        "intro": "Ajánlatkérés előtt ellenőrizze az alábbi pontokat. A katalógus tájékoztató jellegű; a végső megfelelőséget a kiválasztott beszállítói minőség, tétel és aktuális dokumentáció határozza meg.",
        "items": [
            ("Azonosítás", "A különböző kereskedelmi formák elkerüléséhez adja meg a CAS-számot, valamint ha releváns, a hidrát-/formát és a koncentrációt."),
            ("Felhasználás", "Írja le a tervezett folyamatot és végfelhasználást. Élelmiszer-, takarmány-, kozmetikai-, vízkezelési és ipari alkalmazás eltérő minőséget és igazolást igényelhet."),
            ("Kereskedelmi adatok", "Adja meg a mennyiséget, mértékegységet, csomagolást, szállítási országot/helyszínt és a kívánt határidőt. Az elérhetőséget, MOQ-t, Incoterms-paritást és átfutási időt írásos ajánlatban erősítjük meg."),
            ("Dokumentumok", "Minimum az aktuális SDS-t kérje; az alkalmazástól vagy minőségirányítási rendszertől függően TDS/specifikáció és tételszintű CoA is szükséges lehet."),
            ("Jóváhagyási pont", "A szabályozási megfelelőséget, tanúsítást vagy tételmegfelelőséget ne vezesse le a katalógusnévből, PubChem-, Wikipedia- vagy Wikidata-adatból. Ezt a konkrét ajánlat beszállítói dokumentumaival kell igazolni."),
        ],
        "cta": "Ha a szükséges minőség vagy forma bizonytalan, írja le a folyamatot és a kívánt eredményt az érdeklődésben, hogy dokumentumok alapján alternatívákat is ellenőrizhessünk.",
    },
    "de": {
        "heading": "Entscheidungshilfe für den Einkauf",
        "intro": "Vor einer Anfrage sollten Sie die folgenden Punkte bestätigen. Der Katalog dient der Orientierung; die endgültige Eignung bestimmen die ausgewählte Lieferantenqualität, Charge und aktuelle Dokumentation.",
        "items": [
            ("Identität", "Geben Sie die CAS-Nummer und, sofern relevant, Hydrat-/Formvariante und Konzentration an, damit unterschiedliche Handelsformen nicht vermischt werden."),
            ("Anwendung", "Beschreiben Sie Prozess und Endanwendung. Für Lebensmittel, Futtermittel, Kosmetik, Wasseraufbereitung und industrielle Anwendungen können unterschiedliche Qualitäten und Nachweise erforderlich sein."),
            ("Kaufdaten", "Nennen Sie Menge, Einheit, Verpackung, Lieferland/-ort und gewünschten Termin. Verfügbarkeit, MOQ, Incoterms und Lieferzeit werden im schriftlichen Angebot bestätigt."),
            ("Dokumente", "Fordern Sie mindestens das aktuelle SDS an; je nach Anwendung oder Qualitätsmanagement können TDS/Spezifikation und chargenbezogenes CoA erforderlich sein."),
            ("Freigabepunkt", "Regulatorische Eignung, Zertifizierung oder Chargenkonformität dürfen nicht aus dem Katalognamen, PubChem, Wikipedia oder Wikidata abgeleitet werden. Sie müssen anhand der Lieferantendokumente des konkreten Angebots bestätigt werden."),
        ],
        "cta": "Wenn Qualität oder Form noch unklar sind, beschreiben Sie Prozess und gewünschtes Ergebnis in der Anfrage, damit dokumentenbasierte Alternativen geprüft werden können.",
    },
}

PATTERNS = [
    "*natrium-karbonat*.html", "*natrium-hidrogen-karbonat*.html", "*kalcium-klorid*.html",
    "*foszforsav*.html", "*karbamid*.html", "*citromsav*.html", "*glicerin*.html",
    "*natrium-hidroxid*.html", "*rez-klorid*.html", "*rez-szulfat*.html", "*cink-*.html",
    "*propionsav*.html", "*etil-acetat*.html", "*natrium-perszulfat*.html", "*ammonium-szulfat*.html",
]

def lang_for(path: Path) -> str:
    if path.name.startswith("hu-"): return "hu"
    if path.name.startswith("de-at-"): return "de"
    return "en"

def section(lang: str) -> str:
    t = TEXT[lang]
    lis = "".join(f"<li><strong>{label}:</strong> {body}</li>" for label, body in t["items"])
    return (f'<section class="product-decision-guide" aria-labelledby="decisionGuideHeading">'
            f'<h2 id="decisionGuideHeading">{t["heading"]}</h2><p>{t["intro"]}</p>'
            f'<ul>{lis}</ul><p class="microcopy">{t["cta"]}</p></section>')

changed = []
paths = sorted({p for pattern in PATTERNS for p in ROOT.glob(pattern)})
for path in paths:
    html = path.read_text(encoding="utf-8")
    if "product-decision-guide" not in html or 'dateModified":"2026-11-12"' not in html:
        if "product-decision-guide" not in html:
            marker = '<section class="product-faq"'
            if marker not in html:
                raise SystemExit(f"Missing FAQ insertion point: {path}")
            html = html.replace(marker, section(lang_for(path)) + marker, 1)
        html = html.replace('"dateModified":"2026-11-08"', '"dateModified":"2026-11-12"')
        path.write_text(html, encoding="utf-8")
        changed.append(path.name)

print(f"Updated {len(changed)} pages")
for name in changed:
    print(name)
