#!/usr/bin/env python3
from pathlib import Path
import sys
from bs4 import BeautifulSoup
import json,re
ROOT=Path(__file__).resolve().parents[1]
WRITE='--write' in sys.argv
DATE='2026-08-10'
WEBSITE_ID='https://www.rawmaterialstrade.com/#website'
ORG_ID='https://www.rawmaterialstrade.com/#org'
ORG_DESC={
'en':'Raw Materials Trade Kft. is a Hungarian B2B raw-material trading and sourcing company serving industrial buyers, procurement teams, distributors and manufacturers across Hungary, Austria, the DACH region and wider Europe. The portfolio covers industrial chemicals, food and feed raw materials, cosmetic and home-care ingredients, water-treatment materials, de-icing products and specialty chemicals on a quotation basis. ISO 9001:2015 covers the certified quality-management scope; GMP+ Feed Safety Assurance 2020 applies to the certified trade, storage and transshipment of feed, feed materials and feed additives.',
'hu':'A Raw Materials Trade Kft. magyar B2B alapanyag-kereskedelmi és beszerzési vállalat, amely ipari vevőket, beszerzési csapatokat, disztribútorokat és gyártókat szolgál ki Magyarországon, Ausztriában, a DACH-régióban és más európai piacokon. A portfólió ipari vegyi anyagokat, élelmiszer- és takarmányipari alapanyagokat, kozmetikai és háztartás-vegyipari összetevőket, vízkezelési és síkosságmentesítő anyagokat, valamint speciális vegyipari alapanyagokat foglal magában. Az ISO 9001:2015 a tanúsított minőségirányítási körre, a GMP+ Feed Safety Assurance 2020 pedig a takarmányok, takarmány-alapanyagok és takarmány-adalékanyagok tanúsított kereskedelmi, tárolási és átrakási körére vonatkozik.',
'de-at':'Raw Materials Trade Kft. ist ein ungarisches B2B-Unternehmen für Rohstoffhandel und Beschaffung und betreut industrielle Einkäufer, Beschaffungsteams, Distributoren und Hersteller in Ungarn, Österreich, der DACH-Region und weiteren europäischen Märkten. Das Portfolio umfasst Industriechemikalien, Lebensmittel- und Futtermittelrohstoffe, Inhaltsstoffe für Kosmetik und Haushaltspflege, Wasseraufbereitungs- und Enteisungsmaterialien sowie Spezialchemikalien auf Angebotsbasis. ISO 9001:2015 gilt für den zertifizierten Qualitätsmanagement-Geltungsbereich; GMP+ Feed Safety Assurance 2020 für den zertifizierten Handel, die Lagerung und den Umschlag von Futtermitteln, Futtermittel-Ausgangserzeugnissen und Zusatzstoffen.'}
KNOWS=[
'B2B chemical raw material trading','chemical raw material sourcing and procurement','industrial chemicals',
'food industry raw materials','feed materials and feed additives','cosmetic and personal-care ingredients',
'home-care raw materials','water-treatment chemicals','de-icing and winter-service materials','specialty chemicals',
'SDS, TDS and CoA documentation','REACH and CLP documentation context','international supplier-network development',
'sales representation and distribution partnerships','Hungary, Austria, DACH and European B2B markets']

def lang_of(soup,path):
    l=(soup.html.get('lang','') if soup.html else '').lower()
    if l.startswith('hu'): return 'hu'
    if l.startswith('de'): return 'de-at'
    return 'en'

def enrich_org(n,lang):
    n.update({
      'alternateName':'RMT Kft.','legalName':'RAW MATERIALS TRADE Korlátolt Felelősségű Társaság',
      'description':ORG_DESC[lang],
      'logo':{'@type':'ImageObject','url':'https://www.rawmaterialstrade.com/assets/images/brand/logo-schema.png'},
      'email':'office@rawmaterialstrade.com','telephone':'+36 30 160 1960',
      'vatID':'HU29224933','taxID':'29224933-2-16',
      'identifier':[{'@type':'PropertyValue','name':'Company registration number','value':'16-09-020248'},
                    {'@type':'PropertyValue','name':'EU VAT ID','value':'HU29224933'}],
      'areaServed':['Hungary','Austria','Germany','Switzerland','DACH','European Union'],
      'sameAs':['https://www.linkedin.com/company/raw-materials-trade-kft'],
      'knowsAbout':KNOWS,
      'contactPoint':{'@type':'ContactPoint','contactType':'B2B sales and procurement','email':'office@rawmaterialstrade.com','telephone':'+36 30 160 1960','availableLanguage':['English','Hungarian','German']},
    })
    # Keep the two public locations explicit and certification-address wording accurate.
    n['address']={'@type':'PostalAddress','streetAddress':'Mária utca 9','addressLocality':'Törökszentmiklós','postalCode':'5200','addressCountry':'HU'}
    n['location']=[
      {'@type':'Place','name':'Registered office and GMP+ certificate invoicing address','address':{'@type':'PostalAddress','streetAddress':'Mária utca 9','addressLocality':'Törökszentmiklós','postalCode':'5200','addressCountry':'HU'}},
      {'@type':'Place','name':'Operational site and ISO 9001 certificate address','address':{'@type':'PostalAddress','streetAddress':'HRSZ 4515/2','addressLocality':'Ócsa','postalCode':'2364','addressCountry':'HU'}}]
    n['additionalProperty']=[
      {'@type':'PropertyValue','name':'Registered office and GMP+ certificate invoicing address','value':'Mária utca 9, 5200 Törökszentmiklós, Hungary'},
      {'@type':'PropertyValue','name':'Operational site and ISO 9001 certificate address','value':'H-2364 Ócsa, HRSZ 4515/2, Hungary'},
      {'@type':'PropertyValue','name':'ISO 9001:2015 certified scope','value':'Storage and wholesale of chemical and feed raw materials'},
      {'@type':'PropertyValue','name':'GMP+ FSA 2020 certified scope','value':'Trade in feed, feed materials and feed additives; storage and transshipment of feed'}]

def website_node():
    return {'@type':'WebSite','@id':WEBSITE_ID,'url':'https://www.rawmaterialstrade.com/','name':'Raw Materials Trade Kft.','publisher':{'@id':ORG_ID},'inLanguage':['en','hu-HU','de-AT']}

changed=0; blocks=0
for path in ROOT.glob('*.html'):
    soup=BeautifulSoup(path.read_text(encoding='utf8',errors='replace'),'html.parser')
    if soup.find('meta',attrs={'http-equiv':re.compile('refresh',re.I)}):
        # Redirect stubs stay minimal.
        continue
    lang=lang_of(soup,path)
    touched=False
    for sc in soup.find_all('script',attrs={'type':'application/ld+json'}):
        try:d=json.loads(sc.string or sc.get_text())
        except Exception: continue
        graph=d.get('@graph') if isinstance(d,dict) else None
        if not isinstance(graph,list): continue
        has_org=False
        for n in graph:
            if not isinstance(n,dict): continue
            ty=n.get('@type')
            if ty=='Organization' and (n.get('@id')==ORG_ID or n.get('name')=='Raw Materials Trade Kft.'):
                n['@id']=ORG_ID; enrich_org(n,lang); has_org=True; touched=True
            if ty=='WebSite' and n.get('@id')==WEBSITE_ID:
                n.update(website_node()); touched=True
            if ty in ('WebPage','CollectionPage','FAQPage','Blog','ProfilePage'):
                n['isPartOf']={'@id':WEBSITE_ID}; n['publisher']={'@id':ORG_ID}; n['dateModified']=DATE; touched=True
        if has_org and not any(isinstance(n,dict) and n.get('@id')==WEBSITE_ID for n in graph):
            # Place WebSite after Organization when possible.
            idx=next((i for i,n in enumerate(graph) if isinstance(n,dict) and n.get('@id')==ORG_ID),0)
            graph.insert(idx+1,website_node()); touched=True
        if touched:
            sc.string=json.dumps(d,ensure_ascii=False,separators=(',',':')); blocks+=1
        # The site consistently uses one primary graph block.
        break
    if touched:
        path.write_text(str(soup),encoding='utf8'); changed+=1
print('schema-synchronised HTML:',changed,'JSON-LD blocks:',blocks,'mode:', 'write' if WRITE else 'dry-run (use --write to modify files)')
