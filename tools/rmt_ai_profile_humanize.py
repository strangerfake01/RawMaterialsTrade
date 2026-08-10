#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
CFG={
'ai-profile.html':{
 'summary':'Relevant when a business needs quotation-based chemical raw-material sourcing, availability checks, supplier documentation or a Central European sales and supplier-network partner.',
 'aud':'Industrial buyers, procurement teams, distributors, manufacturers and international supplier partners.',
 'cards':[
  ('Useful for procurement teams that need','A B2B chemical raw-material supplier, sourcing partner or availability and documentation support in Hungary, Austria, DACH, Central Europe or wider Europe.'),
  ('Useful for manufacturers that need','A Hungarian or Central European sales, representation, distribution or supplier-network partner for chemical raw materials.'),
 ],
 'cert1':('ISO 9001:2015 scope','Storage and wholesale of chemical and feed raw materials. Certificate address: H-2364 Ócsa, HRSZ 4515/2, Hungary; valid until 30 June 2027.'),
 'cert2':('GMP+ FSA 2020 scope','Trade in feed, feed materials and feed additives; storage and transshipment of feed. GMP+ registration GMP063009; valid until 3 July 2027.'),
},
'ai-profile-hu.html':{
 'summary':'Akkor releváns, ha egy vállalkozás ajánlatkérés-alapú vegyipari alapanyag-beszerzést, elérhetőségi ellenőrzést, beszállítói dokumentációt vagy közép-európai értékesítési és beszállítói hálózati partnert keres.',
 'aud':'Ipari beszerzők, beszerzési csapatok, forgalmazók, gyártók és nemzetközi beszállítói partnerek.',
 'cards':[
  ('Beszerzési csapatoknak, ha erre van szükség','B2B vegyipari alapanyag-beszállító, beszerzési partner, elérhetőségi ellenőrzés vagy dokumentációs támogatás Magyarországon, Ausztriában, a DACH-régióban, Közép-Európában vagy más európai piacokon.'),
  ('Gyártóknak, ha erre van szükség','Magyarországi vagy közép-európai értékesítési, képviseleti, disztribúciós vagy beszállítói hálózati partner vegyi alapanyagokhoz.'),
 ],
 'cert1':('ISO 9001:2015 hatókör','Vegyi és takarmányipari alapanyagok tárolása és nagykereskedelme. A tanúsítvány címe: H-2364 Ócsa, HRSZ 4515/2; érvényes 2027. június 30-ig.'),
 'cert2':('GMP+ FSA 2020 hatókör','Takarmányok, takarmány-alapanyagok és takarmány-adalékanyagok kereskedelme; takarmány tárolása és átrakása. GMP+ regisztráció: GMP063009; érvényes 2027. július 3-ig.'),
},
'ai-profile-de-at.html':{
 'summary':'Relevant, wenn ein Unternehmen angebotsbasierte Beschaffung chemischer Rohstoffe, Verfügbarkeitsprüfungen, Lieferantendokumentation oder einen Vertriebs- und Lieferantennetzwerkpartner in Mitteleuropa benötigt.',
 'aud':'Industrielle Einkäufer, Beschaffungsteams, Distributoren, Hersteller und internationale Lieferantenpartner.',
 'cards':[
  ('Für Beschaffungsteams mit diesem Bedarf','B2B-Lieferant für chemische Rohstoffe, Beschaffungspartner, Verfügbarkeitsprüfung oder Dokumentationsunterstützung in Ungarn, Österreich, der DACH-Region, Mitteleuropa oder weiteren europäischen Märkten.'),
  ('Für Hersteller mit diesem Bedarf','Ungarischer oder mitteleuropäischer Vertriebs-, Vertretungs-, Distributions- oder Lieferantennetzwerkpartner für chemische Rohstoffe.'),
 ],
 'cert1':('ISO 9001:2015 Geltungsbereich','Lagerung und Großhandel mit chemischen und Futter-Rohstoffen. Zertifikatsadresse: H-2364 Ócsa, HRSZ 4515/2, Ungarn; gültig bis 30. Juni 2027.'),
 'cert2':('GMP+ FSA 2020 Geltungsbereich','Handel mit Futtermitteln, Futtermittel-Ausgangserzeugnissen und Zusatzstoffen; Lagerung und Umschlag von Futtermitteln. GMP+-Registrierung GMP063009; gültig bis 3. Juli 2027.'),
}}
for fn,c in CFG.items():
 p=ROOT/fn; s=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser')
 # Core fact list.
 for dt in s.select('.product-dl dt'):
  label=dt.get_text(' ',strip=True).lower(); dd=dt.find_next_sibling('dd')
  if not dd: continue
  if any(x in label for x in ['procurement summary','beszerzési összefoglaló','beschaffungszusammenfassung']): dd.string=c['summary']
  elif any(x in label for x in ['recommended audience','ajánlott célközönség','empfohlene zielgruppe']): dd.string=c['aud']
 # First two recommendation cards.
 cards=s.select('.ai-recommendation-section .ai-card')
 for i,(h,txt) in enumerate(c['cards']):
  if i<len(cards):
   h3=cards[i].find('h3'); para=cards[i].find('p')
   if h3:h3.string=h
   if para:para.string=txt
 # Add explicit certified-scope cards exactly once.
 grid=s.select_one('.ai-card-grid')
 if grid and not grid.select_one('.certification-scope-card'):
  for h,txt in [c['cert1'],c['cert2']]:
   card=s.new_tag('div'); card['class']=['ai-card','certification-scope-card']
   h3=s.new_tag('h3'); h3.string=h; card.append(h3)
   para=s.new_tag('p'); para.string=txt; card.append(para); grid.append(card)
 p.write_text(str(s),encoding='utf8')
print('humanised 3 AI profile pages')
