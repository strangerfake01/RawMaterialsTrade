from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TODAY = '2026-11-12'
source_index = {
    'policy': 'Market context is a monitoring signal, not a demand forecast or product-specific availability claim.',
    'sources': [
        {'publisher': 'Reuters', 'title': "Europe's chemical makers catch a break as Iran war hits Asian rivals", 'url': 'https://news.google.com/rss/articles/CBMitAFBVV95cUxNdVhiVXEwaEFKdlMwaFdMdVNXSUhQNzVUMHJDY2JVdl9Ta2twSDdON29NYUV0ZjBkRkxweTZJSDY1LU5ra2VxSkF6RXloU2oxWUZuYUQzcFNBMEY1MEVwSXpMSUhFN2p', 'themes': ['European chemical production', 'geopolitical supply risk']},
        {'publisher': 'Chemistry World', 'title': 'Gulf chemicals supply disruption will continue for months to years', 'url': 'https://news.google.com/rss/articles/CBMiugFBVV95cUxNWnNNYjFDd3ZBMlJMUUJDUGp4aU5FTmdTTVdWdHlLVnpSaXM3a1FfcFhRcEl0WnNKbG9NbVZqY20xZDM3a2tvOW4xQW9mdlZHX0paREtUdUI1UUdFRXRIV1VlTlRGaHl', 'themes': ['chemical supply chains', 'Gulf logistics']},
        {'publisher': 'ICIS', 'title': 'Five Forecasts for Global Chemical Markets in 2026', 'url': 'https://news.google.com/rss/articles/CBMiqgFBVV95cUxPNmkzc3dIZm5VMmRRNkFPWVJJaTMzMmVaRzZxVmFXZ2tZbWI0eXVuRjZWYkFuWlFXSXlkUnRMbGtzUE9NSkVsOGdpZUhYQktJMmVZT0xwb3U0MUNyMU1rdEU0UkNwZ09', 'themes': ['chemical market outlook']},
        {'publisher': 'Bruegel', 'title': 'Competing for inputs: how the European Union can improve critical raw materials supply security', 'url': 'https://news.google.com/rss/articles/CBMiwAFBVV95cUxPMGdPWVNpNDBQVHNlSi05WDlwUzJ3aUpBeVhKRlhPZnRydzZoTzZweTVmQ2JrZmFYazNlelVQaHdPX2ZjRjhqQ0FLRDlvNWNDOExBU3U5SjBQVXdkdjFodERxb0pUZmI', 'themes': ['EU supply security', 'critical inputs']},
        {'publisher': 'McKinsey & Company', 'title': 'Chemicals 2025: A new reality for the global chemical industry', 'url': 'https://news.google.com/rss/articles/CBMilAFBVV95cUxNaTFGd1ZZemNHTG1LMktsUm5IU2dOM3JUYkw0clNSVjNSZlF2LXhwZ2RaRnpaLTNUdm5fVkJiQTRONXp1ejdETFhFRFRVci1Rel9iYVdGSTZBaEZGWDNuWkkxejNZbzQ', 'themes': ['chemical industry outlook', 'regional competitiveness']},
    ],
}
(ROOT / 'data' / 'market-outlook-sources.json').write_text(json.dumps({'schemaVersion':'1.0','generatedAt':TODAY,**source_index},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

targets = {
    'karbamid': ('Fertiliser and chemical supply monitoring', 'Műtrágya- és vegyipari ellátás figyelése', 'Beobachtung der Düngemittel- und Chemieversorgung'),
    'ammonium-szulfat': ('Fertiliser and chemical supply monitoring', 'Műtrágya- és vegyipari ellátás figyelése', 'Beobachtung der Düngemittel- und Chemieversorgung'),
    'ammonium-nitrat': ('Fertiliser and chemical supply monitoring', 'Műtrágya- és vegyipari ellátás figyelése', 'Beobachtung der Düngemittel- und Chemieversorgung'),
    'foszforsav': ('Acid and chemical supply monitoring', 'Sav- és vegyipari ellátás figyelése', 'Beobachtung der Säure- und Chemieversorgung'),
    'saletromsav': ('Acid and chemical supply monitoring', 'Sav- és vegyipari ellátás figyelése', 'Beobachtung der Säure- und Chemieversorgung'),
    'kensav': ('Acid and chemical supply monitoring', 'Sav- és vegyipari ellátás figyelése', 'Beobachtung der Säure- und Chemieversorgung'),
    'natrium-hidroxid': ('Chlor-alkali and chemical supply monitoring', 'Klóralkáli- és vegyipari ellátás figyelése', 'Beobachtung der Chloralkali- und Chemieversorgung'),
    'hidrogen-peroxid': ('Chemical supply monitoring', 'Vegyipari ellátás figyelése', 'Beobachtung der Chemieversorgung'),
    'glicerin': ('Chemical and logistics monitoring', 'Vegyipari és logisztikai figyelés', 'Beobachtung von Chemie und Logistik'),
    'monopropilenglikol': ('Chemical and logistics monitoring', 'Vegyipari és logisztikai figyelés', 'Beobachtung von Chemie und Logistik'),
}
texts = {
 'en': ('Market monitoring context', 'International chemical-industry and supply-chain reporting currently highlights regional production, energy, logistics and critical-input risks. This is a monitoring signal only, not a forecast of demand, price, stock or availability for this product. Confirm the selected grade, supplier, documents and commercial terms before purchase.', 'Market-outlook source register'),
 'hu': ('Piaci figyelési háttér', 'A nemzetközi vegyipari és ellátásilánc-jelentések jelenleg regionális termelési, energia-, logisztikai és kritikusinput-kockázatokat emelnek ki. Ez csak piaci figyelési jelzés, nem az adott termék keresletére, árára, készletére vagy elérhetőségére vonatkozó előrejelzés. Vásárlás előtt a kiválasztott minőséget, beszállítót, dokumentumokat és kereskedelmi feltételeket meg kell erősíteni.', 'Piaci outlook forrásjegyzék'),
 'de': ('Marktbeobachtung', 'Internationale Berichte zur Chemieindustrie und zu Lieferketten weisen derzeit auf regionale Produktions-, Energie-, Logistik- und Risiken bei kritischen Vorprodukten hin. Dies ist nur ein Beobachtungssignal und keine Prognose für Nachfrage, Preis, Bestand oder Verfügbarkeit dieses Produkts. Vor dem Kauf sind Qualität, Lieferant, Dokumente und kaufmännische Bedingungen zu bestätigen.', 'Quellenregister Marktbeobachtung'),
}
changed=0
for path in ROOT.glob('*.html'):
    if 'product-page-rich' not in path.read_text(encoding='utf-8') or 'product-market-watch' in path.name:
        continue
    key=next((k for k in targets if k in path.name),None)
    if not key: continue
    text=path.read_text(encoding='utf-8')
    if 'product-market-watch' in text: continue
    lang='hu' if path.name.startswith('hu-') else 'de' if path.name.startswith('de-at-') else 'en'
    heading, body, link_text=texts[lang]
    section=f'<section class="product-market-watch" aria-labelledby="marketWatchHeading"><h2 id="marketWatchHeading">{heading}</h2><p>{body}</p><p class="microcopy"><a href="/data/market-outlook-sources.json">{link_text}</a></p></section>'
    if '<section class="product-faq"' in text:
        text=text.replace('<section class="product-faq"',section+'<section class="product-faq"',1)
        path.write_text(text,encoding='utf-8'); changed+=1
print(f'Added market-watch context to {changed} pages')
