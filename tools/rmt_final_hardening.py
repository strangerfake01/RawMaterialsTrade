#!/usr/bin/env python3
"""Final SEO/GEO/LLM/schema + human-language hardening for Raw Materials Trade.

Designed to be idempotent. It applies the 2026-08-10 post-PSI improvements:
- removes English leakage from German product applications,
- humanises product-page lead/procurement copy in EN/HU/DE without inventing facts,
- exposes multilingual alternative names visibly,
- improves topical internal linking with semantic related-product selection,
- strengthens self-contained entity/schema context on every product page,
- clarifies the GMP+ certificate as feed-scope specific,
- humanises homepage entity descriptions and certification wording,
- updates machine-readable catalog versions and sitemap lastmod.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json, re, html
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-10"

DE_APP_TRANSLATIONS = {
    "air disinfection/sterilisation": "Luftdesinfektion und Sterilisation",
    "aluminium production": "Aluminiumherstellung",
    "analytical reagent": "analytisches Reagenz",
    "animal feed additive": "Futtermittelzusatzstoff",
    "animal feed component": "Futtermittelkomponente",
    "animal feed energy source": "Energiequelle in Futtermitteln",
    "animal feed non-protein nitrogen source": "Nichtprotein-Stickstoffquelle in Futtermitteln",
    "antifreeze base": "Basis für Frostschutzmittel",
    "antifreeze ingredient": "Bestandteil von Frostschutzmitteln",
    "beverage fortification": "Anreicherung von Getränken",
    "catalyst": "Katalysator",
    "ceramic and glass production": "Keramik- und Glasherstellung",
    "ceramic binder": "Bindemittel in der Keramik",
    "cleaning and descaling": "Reinigung und Entkalkung",
    "concrete accelerator": "Erhärtungsbeschleuniger für Beton",
    "corrosion inhibitor": "Korrosionsinhibitor",
    "cosmetic formulations": "kosmetische Formulierungen",
    "cosmetic moisturiser (high-concentration)": "Feuchthaltemittel in kosmetischen Formulierungen (höhere Konzentrationen)",
    "cosmetic solvent": "Lösungsmittel in kosmetischen Formulierungen",
    "de-icing agent": "Enteisungsmittel",
    "desiccant": "Trockenmittel",
    "environmental remediation": "Umweltsanierung",
    "feed additive": "Futtermittelzusatzstoff",
    "feed mineral supplement": "mineralische Ergänzung in Futtermitteln",
    "food additive (E518)": "Lebensmittelzusatzstoff (E518)",
    "food equipment sanitation": "Reinigung und Desinfektion von Lebensmittelanlagen",
    "food grade (vacuum salt)": "Lebensmittelqualität (Vakuumsalz)",
    "food processing (E525)": "Lebensmittelverarbeitung (E525)",
    "formaldehyde production": "Formaldehydherstellung",
    "galvanic plating": "galvanische Beschichtung",
    "gold ore processing": "Goldaufbereitung",
    "industrial lubricant additive": "Additiv für industrielle Schmierstoffe",
    "industrial solvent": "industrielles Lösungsmittel",
    "laboratory solvent": "Laborlösungsmittel",
    "nail varnish remover": "Nagellackentferner",
    "paper and textile industry": "Papier- und Textilindustrie",
    "paper pulping": "Zellstoffaufschluss",
    "pharmaceutical": "pharmazeutische Anwendungen",
    "pharmaceutical (laxative)": "pharmazeutische Anwendung (Abführmittel)",
    "pharmaceutical buffering": "pharmazeutische Pufferung",
    "pharmaceutical extraction": "pharmazeutische Extraktion",
    "pharmaceutical topical formulations": "topische pharmazeutische Formulierungen",
    "plasticiser intermediate": "Zwischenprodukt für Weichmacher",
    "protein precipitation in biotechnology": "Proteinfällung in der Biotechnologie",
    "resin production": "Harzherstellung",
    "rubber coagulant": "Koagulierung in der Gummiherstellung",
    "stain removal": "Fleckenentfernung",
    "surface treatment": "Oberflächenbehandlung",
    "swimming pool water treatment": "Schwimmbadwasseraufbereitung",
    "textile dyeing": "Textilfärbung",
    "tofu coagulant": "Gerinnungsmittel bei der Tofuherstellung",
    "wastewater and drinking water treatment (coagulant)": "Abwasser- und Trinkwasseraufbereitung (Koagulans)",
    "wastewater pH correction": "pH-Korrektur im Abwasser",
    "water treatment": "Wasseraufbereitung",
}

LANG = {
    "en": {
        "file": "products-en.json", "html_lang": "en",
        "lead_extra": "For a quotation, we confirm the requested grade or concentration, packaging, current availability and the supplier documents relevant to the selected offer.",
        "formula": "Formula",
        "decision_label": "What buyers should know",
        "decision_h2": "Typical applications and procurement details",
        "summary": "How to request this material",
        "summary_text": "Raw Materials Trade Kft. handles this material on a quotation basis for professional buyers in Hungary, Austria, the DACH region and wider Europe. Send the target specification, quantity, packaging and delivery location; we will confirm current availability and the documentation supplied with the selected grade.",
        "related": "Related materials",
        "cert_iso": "ISO 9001:2015 — certified quality-management scope",
        "cert_gmp": "GMP+ FSA 2020 — certified feed scope",
        "cert_link": "View certificates",
        "synonyms": "Synonyms",
    },
    "hu": {
        "file": "products-hu.json", "html_lang": "hu-HU",
        "lead_extra": "Ajánlatkérésnél a kívánt minőséget vagy koncentrációt, a kiszerelést, az aktuális elérhetőséget és a kiválasztott ajánlathoz tartozó beszállítói dokumentációt egyedileg erősítjük meg.",
        "formula": "Képlet",
        "decision_label": "Amit érdemes tudni",
        "decision_h2": "Tipikus felhasználás és beszerzési szempontok",
        "summary": "Ajánlatkérés ehhez az alapanyaghoz",
        "summary_text": "A Raw Materials Trade Kft. ezt az alapanyagot ajánlatkérés alapján, professzionális B2B vevők számára szerzi be Magyarországon, Ausztriában, a DACH-régióban és más európai piacokon. Add meg a kívánt specifikációt, mennyiséget, kiszerelést és szállítási helyet; ezek alapján tudjuk megerősíteni az aktuális elérhetőséget és a kiválasztott minőség dokumentációját.",
        "related": "Kapcsolódó alapanyagok",
        "cert_iso": "ISO 9001:2015 – tanúsított minőségirányítási tevékenységi kör",
        "cert_gmp": "GMP+ FSA 2020 – tanúsított takarmányipari tevékenységi kör",
        "cert_link": "Tanúsítványok megtekintése",
        "synonyms": "Szinonimák",
    },
    "de-at": {
        "file": "products-de-at.json", "html_lang": "de-AT",
        "lead_extra": "Für ein Angebot bestätigen wir die gewünschte Qualität bzw. Konzentration, Verpackung, aktuelle Verfügbarkeit und die zum ausgewählten Angebot gehörende Lieferantendokumentation individuell.",
        "formula": "Formel",
        "decision_label": "Was für die Beschaffung wichtig ist",
        "decision_h2": "Typische Anwendungen und Beschaffungshinweise",
        "summary": "Anfrage für dieses Material",
        "summary_text": "Raw Materials Trade Kft. beschafft dieses Material auf Angebotsbasis für professionelle B2B-Kunden in Ungarn, Österreich, der DACH-Region und weiteren europäischen Märkten. Nennen Sie gewünschte Spezifikation, Menge, Verpackung und Lieferort; anschließend bestätigen wir die aktuelle Verfügbarkeit und die Dokumentation der ausgewählten Qualität.",
        "related": "Verwandte Rohstoffe",
        "cert_iso": "ISO 9001:2015 – zertifizierter Qualitätsmanagement-Geltungsbereich",
        "cert_gmp": "GMP+ FSA 2020 – zertifizierter Futtermittel-Geltungsbereich",
        "cert_link": "Zertifikate ansehen",
        "synonyms": "Synonyme",
    },
}

ORG_DESC = {
    "en": "Raw Materials Trade Kft. is a Hungarian B2B raw-material trading and sourcing company serving industrial buyers, procurement teams, distributors and manufacturers across Hungary, Austria, the DACH region and wider Europe. The company supplies and sources industrial chemicals, food and feed raw materials, cosmetic and home-care ingredients, water-treatment materials, de-icing products and specialty chemicals on a quotation basis. ISO 9001:2015 covers its certified quality-management scope; GMP+ Feed Safety Assurance 2020 applies to the certified feed-trading, storage and transshipment scope.",
    "hu": "A Raw Materials Trade Kft. magyar B2B alapanyag-kereskedelmi és beszerzési vállalat, amely ipari vevőket, beszerzési csapatokat, disztribútorokat és gyártókat szolgál ki Magyarországon, Ausztriában, a DACH-régióban és más európai piacokon. Portfóliója ipari vegyi anyagokat, élelmiszer- és takarmányipari alapanyagokat, kozmetikai és háztartás-vegyipari összetevőket, vízkezelési és síkosságmentesítő anyagokat, valamint speciális vegyipari alapanyagokat foglal magában. Az ISO 9001:2015 a tanúsított minőségirányítási tevékenységi körre, a GMP+ Feed Safety Assurance 2020 pedig a tanúsított takarmányipari kereskedelmi, tárolási és átrakási tevékenységi körre vonatkozik.",
    "de-at": "Raw Materials Trade Kft. ist ein ungarisches B2B-Unternehmen für Rohstoffhandel und Beschaffung und betreut industrielle Einkäufer, Beschaffungsteams, Distributoren und Hersteller in Ungarn, Österreich, der DACH-Region und weiteren europäischen Märkten. Das Portfolio umfasst Industriechemikalien, Lebensmittel- und Futtermittelrohstoffe, Inhaltsstoffe für Kosmetik und Haushaltspflege, Wasseraufbereitungs- und Enteisungsmaterialien sowie Spezialchemikalien. ISO 9001:2015 gilt für den zertifizierten Qualitätsmanagement-Geltungsbereich; GMP+ Feed Safety Assurance 2020 für den zertifizierten Bereich Handel, Lagerung und Umschlag von Futtermitteln.",
}

KNOWS_ABOUT = [
    "B2B chemical raw material trading",
    "chemical raw material sourcing and procurement",
    "industrial chemicals",
    "food industry raw materials",
    "feed materials and feed additives",
    "cosmetic and personal-care ingredients",
    "home-care raw materials",
    "water-treatment chemicals",
    "de-icing and winter-service materials",
    "specialty chemicals",
    "SDS, TDS and CoA documentation",
    "REACH and CLP documentation context",
    "international supplier-network development",
    "sales representation and distribution partnerships",
    "Hungary, Austria, DACH and European B2B markets",
]

HOME_META = {
    "index.html": "B2B chemical raw material sourcing for European industrial, food, feed, cosmetic and home-care partners. ISO 9001:2015 certified; GMP+ FSA applies to the certified feed scope.",
    "hu.html": "B2B vegyipari alapanyag-kereskedelem ipari, élelmiszer-, takarmány-, kozmetikai és háztartás-vegyipari partnereknek. ISO 9001:2015; GMP+ tanúsított takarmányipari kör.",
    "de-at.html": "B2B-Rohstoffhandel und Beschaffung für Industrie, Lebensmittel, Futtermittel, Kosmetik und Haushaltspflege. ISO 9001:2015; GMP+ FSA für den zertifizierten Futtermittelbereich.",
}
HOME_HERO = {
    "index.html": "B2B raw-material sourcing for industrial, feed, food, cosmetic and home-care applications. ISO 9001:2015 supports our quality-management scope; GMP+ FSA covers the certified feed activities. Hungarian expertise — European reach.",
    "hu.html": "B2B alapanyag-kereskedelem és beszerzés ipari, takarmányipari, élelmiszeripari, kozmetikai és háztartás-vegyipari felhasználásra. ISO 9001:2015 a minőségirányítási, GMP+ FSA a tanúsított takarmányipari tevékenységi körre. Magyar szakértelem — európai piac.",
    "de-at.html": "B2B-Rohstoffhandel und Beschaffung für Industrie, Futtermittel, Lebensmittel, Kosmetik und Haushaltspflege. ISO 9001:2015 für das Qualitätsmanagement, GMP+ FSA für den zertifizierten Futtermittelbereich. Kompetenz aus Ungarn — europäische Reichweite.",
}
HOME_CERT = {
    "index.html": {
        "contact": "ISO 9001:2015 covers our quality-management scope; GMP+ Feed Safety Assurance 2020 covers the certified feed-trading, storage and transshipment activities.",
        "service": "ISO 9001:2015-certified quality management, with GMP+ Feed Safety Assurance 2020 for the certified feed scope. Product-specific documentation and certificates are confirmed per enquiry.",
        "footer": "B2B chemical raw material trading and sourcing. ISO 9001:2015 certified; GMP+ Feed Safety Assurance 2020 for the certified feed scope. Hungary — serving Europe.",
    },
    "hu.html": {
        "contact": "Az ISO 9001:2015 a minőségirányítási tevékenységi körre, a GMP+ Feed Safety Assurance 2020 pedig a tanúsított takarmányipari kereskedelmi, tárolási és átrakási tevékenységre vonatkozik.",
        "service": "ISO 9001:2015 szerinti minőségirányítás, valamint GMP+ Feed Safety Assurance 2020 a tanúsított takarmányipari tevékenységi körre. A termékspecifikus dokumentációt ajánlatkérésenként erősítjük meg.",
        "footer": "B2B vegyipari alapanyag-kereskedelem és beszerzés. ISO 9001:2015 tanúsítással; GMP+ Feed Safety Assurance 2020 a tanúsított takarmányipari körre. Magyarország — Európa.",
    },
    "de-at.html": {
        "contact": "ISO 9001:2015 gilt für den Qualitätsmanagement-Geltungsbereich; GMP+ Feed Safety Assurance 2020 für den zertifizierten Handel, die Lagerung und den Umschlag von Futtermitteln.",
        "service": "ISO 9001:2015-zertifiziertes Qualitätsmanagement sowie GMP+ Feed Safety Assurance 2020 für den zertifizierten Futtermittelbereich. Produktspezifische Dokumentation wird je Anfrage bestätigt.",
        "footer": "B2B-Rohstoffhandel und Beschaffung. ISO 9001:2015 zertifiziert; GMP+ Feed Safety Assurance 2020 für den zertifizierten Futtermittelbereich. Ungarn — europaweit tätig.",
    },
}

CATEGORY_CONTEXT = {
    "industrial": {
        "en": ("Industrial procurement", "For industrial use, the requested technical grade, concentration, process context and documentation should be specified before the material is approved for a production route."),
        "hu": ("Ipari beszerzés", "Ipari felhasználásnál a kívánt műszaki minőséget, koncentrációt, technológiai környezetet és dokumentációt még a beszerzés előtt pontosítani kell."),
        "de-at": ("Industrielle Beschaffung", "Für industrielle Anwendungen sollten technische Qualität, Konzentration, Prozesskontext und benötigte Dokumentation vor der Beschaffung eindeutig festgelegt werden."),
    },
    "food": {
        "en": ("Food-industry procurement", "Food use is grade- and application-specific. State the intended use and required food-grade or compliance documentation so suitability can be confirmed for the selected offer."),
        "hu": ("Élelmiszeripari beszerzés", "Élelmiszeripari felhasználásnál a kívánt minőség és az alkalmazás a döntő. Az ajánlatkérésben add meg a felhasználási célt és a szükséges élelmiszeripari vagy megfelelőségi dokumentációt."),
        "de-at": ("Beschaffung für die Lebensmittelindustrie", "Die Eignung für Lebensmittelanwendungen hängt von Qualität und Einsatzbereich ab. Nennen Sie den Verwendungszweck und die benötigte Lebensmittel- bzw. Konformitätsdokumentation."),
    },
    "feed": {
        "en": ("Feed-industry procurement", "Feed use requires the appropriate feed-grade specification and the documentation applicable to the selected product and supply route. The GMP+ certificate relates to the company's certified feed scope, not automatically to every material or grade."),
        "hu": ("Takarmányipari beszerzés", "Takarmányipari felhasználásnál a megfelelő takarmányipari minőséget és az adott termékhez, illetve ellátási útvonalhoz tartozó dokumentációt kell igazolni. A GMP+ tanúsítás a vállalat tanúsított takarmányipari tevékenységi körére vonatkozik, nem automatikusan minden anyagra vagy minőségre."),
        "de-at": ("Beschaffung für die Futtermittelindustrie", "Für Futtermittelanwendungen müssen die geeignete Futtermittelqualität und die für Produkt und Lieferweg geltende Dokumentation bestätigt werden. Das GMP+-Zertifikat bezieht sich auf den zertifizierten Futtermittel-Geltungsbereich des Unternehmens, nicht automatisch auf jedes Material oder jede Qualität."),
    },
    "deicing": {
        "en": ("Winter-service procurement", "For de-icing and winter-service use, specify form or concentration, required volume, packaging or bulk delivery and destination so the appropriate supply option can be checked."),
        "hu": ("Téli útüzemeltetési beszerzés", "Síkosságmentesítésnél add meg a kívánt formát vagy koncentrációt, mennyiséget, kiszerelést vagy ömlesztett szállítási igényt és a célállomást, hogy a megfelelő ellátási lehetőséget lehessen ellenőrizni."),
        "de-at": ("Beschaffung für Winterdienst", "Für Enteisung und Winterdienst sollten Form bzw. Konzentration, benötigte Menge, Verpackung oder lose Lieferung und Zielort angegeben werden, damit die passende Lieferoption geprüft werden kann."),
    },
}


def clean_sentence(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def without_terminal(s: str) -> str:
    return clean_sentence(s).rstrip(" .;:")


def join_list(vals, lang):
    vals=[without_terminal(v) for v in vals if clean_sentence(v)]
    if not vals: return ""
    if len(vals)==1: return vals[0]
    conj={"en":"and","hu":"és","de-at":"und"}[lang]
    if len(vals)==2: return f"{vals[0]} {conj} {vals[1]}"
    return ", ".join(vals[:-1]) + f" {conj} " + vals[-1]


def update_german_datasets():
    p=ROOT/'products-de-at.json'
    d=json.loads(p.read_text(encoding='utf-8'))
    changed=0
    for item in d['products']:
        new=[]
        for a in item.get('applications',[]):
            b=DE_APP_TRANSLATIONS.get(a, a)
            changed += b != a
            new.append(b)
        item['applications']=new
    d['schemaVersion']=DATE
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')

    mp=ROOT/'products-multilingual.json'
    md=json.loads(mp.read_text(encoding='utf-8'))
    for item in md:
        item['applications_de']=[DE_APP_TRANSLATIONS.get(a,a) for a in item.get('applications_de',[])]
    mp.write_text(json.dumps(md,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')
    return changed


def load_products():
    out={}
    for lang,cfg in LANG.items():
        p=ROOT/cfg['file']
        d=json.loads(p.read_text(encoding='utf-8'))
        d['schemaVersion']=DATE
        # localize the business model instead of keeping English in HU/DE machine datasets
        if lang=='hu': d['publisher']['businessModel']='Ajánlatkérés-alapú B2B vegyipari alapanyag-beszerzés és gyártói/disztribúciós partnerség'
        elif lang=='de-at': d['publisher']['businessModel']='Angebotsbasierte B2B-Rohstoffbeschaffung sowie Hersteller- und Vertriebspartnerschaften'
        p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')
        out[lang]={x['id']:x for x in d['products']}
    return out


def load_multilingual_primary():
    d=json.loads((ROOT/'products-multilingual.json').read_text(encoding='utf-8'))
    return {x['id']:x.get('primary_category','industrial') for x in d}


def semantic_related(products_en, primary):
    ids=list(products_en)
    docs=[]
    for pid in ids:
        p=products_en[pid]
        docs.append(' '.join([
            p.get('name',''), p.get('description',''),
            ' '.join(p.get('alternateNames',[])),
            ' '.join(p.get('applications',[])),
            ' '.join(p.get('categories',[])),
            (p.get('commercialContext',{}).get('gradeOrConcentration') or '')
        ]))
    vec=TfidfVectorizer(lowercase=True, ngram_range=(1,2), stop_words='english', min_df=1).fit_transform(docs)
    sim=cosine_similarity(vec)
    pos={pid:i for i,pid in enumerate(ids)}
    out={}
    for pid in ids:
        i=pos[pid]
        p=products_en[pid]
        cas=set(p.get('identity',{}).get('CAS') or [])
        scored=[]
        for j,qid in enumerate(ids):
            if qid==pid: continue
            q=products_en[qid]
            score=float(sim[i,j])
            if primary.get(qid)==primary.get(pid): score += 0.18
            qcas=set(q.get('identity',{}).get('CAS') or [])
            if cas and qcas and cas&qcas: score += 2.0
            # exact/near chemical family tokens get a small boost
            a=set(re.findall(r'[a-z]{4,}',p.get('name','').lower()))
            b=set(re.findall(r'[a-z]{4,}',q.get('name','').lower()))
            score += 0.06*len(a&b)
            scored.append((score,qid))
        scored.sort(reverse=True)
        out[pid]=[qid for _,qid in scored[:4]]
    return out


def natural_lead(p, lang):
    cfg=LANG[lang]
    desc=clean_sentence(p.get('description',''))
    # Avoid duplicating the generic procurement line already present in many HU/DE descriptions.
    has_procurement = (
        ('B2B ajánlatkérés' in desc) if lang=='hu' else
        ('im Rahmen der Anfrage' in desc or 'B2B-Anfrage' in desc) if lang=='de-at' else
        False
    )
    parts=[desc]
    if not has_procurement: parts.append(cfg['lead_extra'])
    formula=p.get('identity',{}).get('formula')
    if formula and formula not in desc:
        parts.append(f"{cfg['formula']}: {formula}.")
    return ' '.join(x for x in parts if x)


def natural_decision(p, lang):
    apps=join_list(p.get('applications',[])[:5],lang)
    grade=clean_sentence((p.get('commercialContext',{}).get('gradeOrConcentration') or ''))
    packaging=clean_sentence(p.get('commercialContext',{}).get('packaging',''))
    if lang=='en':
        first=f"Typical applications include {apps}." if apps else "The intended application should be stated in the enquiry."
        details=[]
        if grade: details.append(f"grade or concentration ({grade})")
        details += ["expected quantity"]
        if packaging: details.append(f"packaging ({packaging})")
        details.append("delivery location")
        return f"{first} For a useful quotation, specify {join_list(details,'en')}. We then confirm current availability and the supplier documentation for the selected offer."
    if lang=='hu':
        first=f"Tipikus felhasználási területei: {apps}." if apps else "Az ajánlatkérésben érdemes megadni a tervezett felhasználást."
        details=[]
        if grade: details.append(f"a kívánt minőséget vagy koncentrációt ({grade})")
        details += ["a várható mennyiséget"]
        if packaging: details.append(f"a kiszerelést ({packaging})")
        details.append("a szállítási helyet")
        return f"{first} Ajánlatkéréskor add meg {join_list(details,'hu')}. Ez alapján tudjuk megerősíteni az aktuális elérhetőséget és a kiválasztott ajánlathoz tartozó beszállítói dokumentációt."
    first=f"Typische Anwendungen sind {apps}." if apps else "Der vorgesehene Einsatz sollte in der Anfrage angegeben werden."
    details=[]
    if grade: details.append(f"gewünschte Qualität bzw. Konzentration ({grade})")
    details += ["voraussichtliche Menge"]
    if packaging: details.append(f"Verpackung ({packaging})")
    details.append("Lieferort")
    return f"{first} Für eine belastbare Anfrage nennen Sie {join_list(details,'de-at')}. Auf dieser Basis bestätigen wir die aktuelle Verfügbarkeit und die Lieferantendokumentation des ausgewählten Angebots."


def localized_disambiguation(lang):
    return {
        'en': 'B2B raw-material identity page for quotation-based procurement. The exact grade, concentration, packaging, availability and regulatory suitability are confirmed from the current supplier documentation for the selected offer.',
        'hu': 'B2B alapanyag-azonosító és beszerzési oldal ajánlatkéréses beszerzéshez. A pontos minőséget, koncentrációt, kiszerelést, elérhetőséget és szabályozási alkalmasságot a kiválasztott ajánlat aktuális beszállítói dokumentációja alapján kell megerősíteni.',
        'de-at': 'B2B-Rohstoffseite für angebotsbasierte Beschaffung. Qualität, Konzentration, Verpackung, Verfügbarkeit und regulatorische Eignung werden anhand der aktuellen Lieferantendokumentation des ausgewählten Angebots bestätigt.'
    }[lang]


def update_schema(soup, p, lang, lead, all_products):
    cfg=LANG[lang]
    for sc in soup.find_all('script',attrs={'type':'application/ld+json'}):
        try: d=json.loads(sc.string or sc.get_text())
        except Exception: continue
        graph=d.get('@graph') if isinstance(d,dict) else None
        if not isinstance(graph,list): continue
        # Add WebSite node to make each product page self-contained.
        if not any(isinstance(n,dict) and n.get('@id')=='https://www.rawmaterialstrade.com/#website' for n in graph):
            graph.insert(1,{
                '@type':'WebSite','@id':'https://www.rawmaterialstrade.com/#website',
                'url':'https://www.rawmaterialstrade.com','name':'Raw Materials Trade Kft.',
                'publisher':{'@id':'https://www.rawmaterialstrade.com/#org'},
                'inLanguage':['en','hu-HU','de-AT']
            })
        for n in graph:
            if not isinstance(n,dict): continue
            ty=n.get('@type')
            if ty=='Organization' and n.get('@id')=='https://www.rawmaterialstrade.com/#org':
                n.update({
                    'alternateName':'RMT Kft.',
                    'legalName':'RAW MATERIALS TRADE Korlátolt Felelősségű Társaság',
                    'description':ORG_DESC[lang],
                    'logo':{'@type':'ImageObject','url':'https://www.rawmaterialstrade.com/assets/images/brand/logo-schema.png'},
                    'email':'office@rawmaterialstrade.com','telephone':'+36 30 160 1960',
                    'vatID':'HU29224933','taxID':'29224933-2-16',
                    'identifier':[
                        {'@type':'PropertyValue','name':'Company registration number','value':'16-09-020248'},
                        {'@type':'PropertyValue','name':'EU VAT ID','value':'HU29224933'}],
                    'areaServed':['Hungary','Austria','DACH','Europe'],
                    'sameAs':['https://www.linkedin.com/company/raw-materials-trade-kft'],
                    'knowsAbout':KNOWS_ABOUT,
                })
            elif ty=='WebPage':
                n['name']=f"{p.get('name','')} | Raw Materials Trade Kft."
                n['isPartOf']={'@id':'https://www.rawmaterialstrade.com/#website'}
                n['publisher']={'@id':'https://www.rawmaterialstrade.com/#org'}
                n['dateModified']=DATE
            elif ty in ('ChemicalSubstance','DefinedTerm') and n.get('@id','').endswith('#material'):
                # Use the unique, readable catalogue description plus the current procurement boundary.
                n['name']=p.get('name','')
                alts=[]
                for code in ('en','hu','de-at'):
                    nm=clean_sentence(all_products[code][p['id']].get('name',''))
                    if nm and nm!=p.get('name','') and nm not in alts: alts.append(nm)
                if alts: n['alternateName']=alts
                n['description']=lead
                n['disambiguatingDescription']=localized_disambiguation(lang)
            elif ty=='BreadcrumbList':
                items=n.get('itemListElement') or []
                if items and isinstance(items[-1],dict): items[-1]['name']=p.get('name','')
        sc.string=json.dumps(d,ensure_ascii=False,separators=(',',':'))
        break


def sync_product_detail_fields(soup, p, lang):
    """Synchronise every repeated visible technical/procurement value with the localised dataset."""
    cc=p.get('commercialContext',{}) or {}
    ident=p.get('identity',{}) or {}
    docs=p.get('documentation',{}) or {}
    labels={
        'en':{
            'grade':['grade / concentration'], 'packaging':['packaging'], 'region':['delivery region'],
            'availability':['availability note'], 'syn':['synonyms / names','synonyms'],
            'sds':['sds status'], 'tds':['tds status'], 'coa':['coa status'],
        },
        'hu':{
            'grade':['minőség / koncentráció'], 'packaging':['kiszerelés'], 'region':['szállítási régió'],
            'availability':['elérhetőségi megjegyzés'], 'syn':['szinonimák / elnevezések','szinonimák'],
            'sds':['sds-státusz','sds státusz'], 'tds':['tds-státusz','tds státusz'], 'coa':['coa-státusz','coa státusz'],
        },
        'de-at':{
            'grade':['qualität / konzentration'], 'packaging':['verpackung'], 'region':['lieferregion'],
            'availability':['verfügbarkeitshinweis'], 'syn':['synonyme / bezeichnungen','synonyme'],
            'sds':['sds-status'], 'tds':['tds-status'], 'coa':['coa-status'],
        }
    }[lang]
    names=[]
    for n in [p.get('name','')]+list(p.get('alternateNames',[])):
        n=clean_sentence(n)
        if n and n not in names: names.append(n)
    values={
        'grade':cc.get('gradeOrConcentration',''), 'packaging':cc.get('packaging',''),
        'region':cc.get('deliveryRegion',''), 'availability':cc.get('availabilityNote',''),
        'syn':', '.join(names[:8]), 'sds':docs.get('SDS',''), 'tds':docs.get('TDS',''), 'coa':docs.get('CoA','')
    }
    for dt in soup.find_all('dt'):
        lab=clean_sentence(dt.get_text()).lower()
        dd=dt.find_next_sibling('dd')
        if not dd: continue
        for key,opts in labels.items():
            if any(lab==o or o in lab for o in opts):
                val=clean_sentence(values.get(key,''))
                if val: dd.string=val
                break

def browser_title(p, lang):
    name=clean_sentence(p.get('name',''))
    # One catalogue name is intentionally long; keep the browser title concise without changing the H1/entity name.
    if p.get('id')=='ecetsav-20-50-60-70-80-99-8-jegecet-food' and lang=='en':
        return 'Acetic Acid 20–99.8% (glacial) | RMT Kft.'
    title=f"{name} | RMT Kft."
    if len(title)<20:
        cat=(p.get('categories') or ['B2B raw material'])[0]
        title=f"{name} — {cat} | RMT Kft."
    return title

def update_product_page(path, p, lang, primary, related_ids, all_products):
    txt=path.read_text(encoding='utf-8')
    soup=BeautifulSoup(txt,'html.parser')
    cfg=LANG[lang]
    # Keep the human-readable product identity consistent with the structured catalogue.
    if soup.title:
        soup.title.string=browser_title(p,lang)
    h1=soup.find('h1')
    if h1: h1.string=p.get('name','')
    for tag in soup.find_all('meta'):
        if tag.get('property')=='og:title' or tag.get('name')=='twitter:title':
            tag['content']=browser_title(p,lang)
    # Update the visible current breadcrumb item without altering URLs.
    bc=soup.select_one('.breadcrumb, .breadcrumbs')
    if bc:
        parts=bc.find_all(['a','span'])
        if parts:
            parts[-1].string=p.get('name','')
    lead=natural_lead(p,lang)
    lead_tag=soup.select_one('p.lead')
    if lead_tag: lead_tag.string=lead
    sync_product_detail_fields(soup,p,lang)

    decision=soup.select_one('.decision-card')
    if decision:
        label=decision.select_one('.section-label')
        h2=decision.find('h2')
        para=decision.find('p')
        if label: label.string=cfg['decision_label']
        if h2: h2.string=cfg['decision_h2']
        if para: para.string=natural_decision(p,lang)
        ctx=decision.select_one('.category-context')
        cat=primary.get(p['id'],'industrial')
        strong_text, span_text=CATEGORY_CONTEXT.get(cat,CATEGORY_CONTEXT['industrial'])[lang]
        if ctx:
            strong=ctx.find('strong'); span=ctx.find('span')
            if strong: strong.string=strong_text
            if span: span.string=span_text

    # Technical identity: expose the three canonical language names with explicit lang attributes.
    for dt in soup.find_all('dt'):
        label=clean_sentence(dt.get_text()).lower()
        if any(k in label for k in ('synonym','szinonim','synonyme')):
            dd=dt.find_next_sibling('dd')
            if dd:
                dd.clear()
                order=[lang]+[x for x in ('en','hu','de-at') if x!=lang]
                seen=set()
                for code in order:
                    n=clean_sentence(all_products[code][p['id']].get('name',''))
                    if not n or n in seen: continue
                    if seen: dd.append(' · ')
                    sp=soup.new_tag('span'); sp['lang']=LANG[code]['html_lang']; sp.string=n; dd.append(sp); seen.add(n)
            break

    # Applications: regenerate visible bullets from the localized machine dataset.
    appbox=soup.select_one('.rich-application .industry-use ul')
    if appbox:
        appbox.clear()
        for a in p.get('applications',[]):
            li=soup.new_tag('li'); li.string=clean_sentence(a); appbox.append(li)

    summary=soup.select_one('.b2b-summary')
    if summary:
        sm=summary.find('summary'); para=summary.find('p')
        if sm: sm.string=cfg['summary']
        if para: para.string=cfg['summary_text']

    # Better semantic internal linking, same product-family graph in all languages.
    relsec=soup.select_one('.related-section')
    if relsec:
        h2=relsec.find('h2')
        if h2: h2.string=cfg['related']
        grid=relsec.select_one('.related-grid')
        if grid:
            grid.clear()
            for rid in related_ids:
                rp=all_products[lang][rid]
                a=soup.new_tag('a',href=urlparse(rp['pageUrl']).path.lstrip('/'))
                a['class']=['related-product']
                sp=soup.new_tag('span'); sp.string=rp['name']; a.append(sp)
                sm=soup.new_tag('small'); sm.string=' · '.join(rp.get('categories',[])); a.append(sm)
                grid.append(a)

    # Certification wording: GMP+ applies to feed scope, not automatically every product.
    trust=soup.select_one('.side-trust')
    if trust:
        spans=trust.find_all('span',recursive=False)
        for sp in spans:
            t=clean_sentence(sp.get_text())
            if t.startswith('ISO 9001:2015'): sp.string=cfg['cert_iso']
            elif t.startswith('GMP+ FSA 2020'): sp.string=cfg['cert_gmp']
        link=trust.select_one('.cert-link')
        if link: link.string=cfg['cert_link']

    # Product quick-view note also gets human phrasing rather than SEO language.
    note=soup.select_one('.product-summary-panel .rich-note')
    if note:
        note.string={
            'en':'Quotation-based B2B supply. Exact specification and availability are confirmed for each enquiry.',
            'hu':'Ajánlatkérés-alapú B2B beszerzés. A pontos specifikációt és elérhetőséget megkeresésenként erősítjük meg.',
            'de-at':'Angebotsbasierte B2B-Beschaffung. Spezifikation und Verfügbarkeit werden je Anfrage bestätigt.'
        }[lang]

    update_schema(soup,p,lang,lead,all_products)
    path.write_text(str(soup),encoding='utf-8')


def update_homepages():
    for fn in ('index.html','hu.html','de-at.html'):
        path=ROOT/fn
        soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
        lang='en' if fn=='index.html' else ('hu' if fn=='hu.html' else 'de-at')
        desc=HOME_META[fn]
        for key,attr in [('description','name'),('og:description','property'),('twitter:description','name')]:
            tag=soup.find('meta',attrs={attr:key})
            if tag: tag['content']=desc
        hero=soup.select_one('.hero-lead')
        if hero: hero.string=HOME_HERO[fn]
        # contact certification line
        for row in soup.select('.contact-row-spaced'):
            if 'GMP+' in row.get_text(' ',strip=True):
                strong=row.find('strong')
                if strong:
                    # Keep the label and replace the following textual content cleanly.
                    label=strong.get_text(' ',strip=True)
                    for child in list(row.contents):
                        if getattr(child,'name',None)=='svg': continue
                    # Replace span text if structure uses a span.
                    span=row.find('span')
                    if span:
                        span.clear()
                        st=soup.new_tag('strong'); st.string=label
                        span.append(st); span.append(' '+HOME_CERT[fn]['contact'])
                break
        # quality/compliance service card
        for card in soup.select('.service-card'):
            if 'GMP+' in card.get_text(' ',strip=True):
                h3=card.find('h3')
                if h3 and any(x in h3.get_text() for x in ('Quality','Minőség','Qualität')):
                    p=card.find('p')
                    if p: p.string=HOME_CERT[fn]['service']
                    break
        fp=soup.select_one('footer p')
        if fp: fp.string=HOME_CERT[fn]['footer']

        # Main Organization schema: concise, human and unambiguous.
        for sc in soup.find_all('script',attrs={'type':'application/ld+json'}):
            try:d=json.loads(sc.string or sc.get_text())
            except Exception: continue
            graph=d.get('@graph') if isinstance(d,dict) else None
            if not isinstance(graph,list): continue
            for n in graph:
                if not isinstance(n,dict): continue
                if n.get('@type')=='Organization' and n.get('@id')=='https://www.rawmaterialstrade.com/#org':
                    n['description']=ORG_DESC[lang]
                    n['knowsAbout']=KNOWS_ABOUT
                    n['disambiguatingDescription']={
                        'en':'Hungarian B2B chemical raw-material trading and sourcing company. Quotation-based professional supply; not a consumer webshop.',
                        'hu':'Magyar B2B vegyipari alapanyag-kereskedelmi és beszerzési vállalat. Professzionális, ajánlatkérés-alapú ellátás; nem lakossági webshop.',
                        'de-at':'Ungarisches B2B-Unternehmen für Chemierohstoffhandel und Beschaffung. Professionelle, angebotsbasierte Versorgung; kein Endkunden-Webshop.'
                    }[lang]
                elif n.get('@type')=='WebPage' and n.get('@id','').endswith('#webpage'):
                    n['description']=desc
                    n['dateModified']=DATE
            sc.string=json.dumps(d,ensure_ascii=False,separators=(',',':'))
            # First schema block contains organization/webpage.
            break
        path.write_text(str(soup),encoding='utf-8')


def update_sitemap():
    p=ROOT/'sitemap.xml'
    txt=p.read_text(encoding='utf-8')
    txt=re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>',f'<lastmod>{DATE}</lastmod>',txt)
    p.write_text(txt,encoding='utf-8')


def main():
    translated=update_german_datasets()
    products=load_products()
    primary=load_multilingual_primary()
    rel=semantic_related(products['en'],primary)
    n=0
    for lang,items in products.items():
        for pid,p in items.items():
            fn=urlparse(p['pageUrl']).path.lstrip('/')
            path=ROOT/fn
            if not path.exists(): raise FileNotFoundError(path)
            update_product_page(path,p,lang,primary,rel[pid],products)
            n+=1
    update_homepages()
    update_sitemap()
    print(f'updated product pages: {n}')
    print(f'translated German application values: {translated}')

if __name__=='__main__': main()
