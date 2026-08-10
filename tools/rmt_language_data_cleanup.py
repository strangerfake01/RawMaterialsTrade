#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-08-10'

SPECIAL_NAMES={
 'edta-na2-na4-industrial':{
   'en':'EDTA — disodium (Na₂) / tetrasodium (Na₄)',
   'hu':'EDTA — dinátrium (Na₂) / tetranátrium (Na₄)',
   'de-at':'EDTA — Dinatrium (Na₂) / Tetranatrium (Na₄)',
 },
 'kenpor-industrial':{'en':'Sulfur — powder','hu':'Kénpor','de-at':'Schwefel — Pulver'},
 'ioncserelt-viz-industrial':{'en':'Deionized water','hu':'Ioncserélt víz','de-at':'Deionisiertes Wasser'},
 'kalium-tripolifoszfat-food':{'en':'Potassium tripolyphosphate','hu':'Kálium-tripolifoszfát','de-at':'Kaliumtripolyphosphat'},
 'trinatrium-foszfat-dodekahidrat-vizmentes-industrial':{
   'en':'Trisodium phosphate — dodecahydrate, anhydrous',
   'hu':'Trinátrium-foszfát — dodekahidrát, vízmentes',
   'de-at':'Trinatriumphosphat — Dodecahydrat, wasserfrei',
 },
}
SPECIAL_GRADE={
 'edta-na2-na4-industrial':{
   'en':'disodium (Na₂) / tetrasodium (Na₄)',
   'hu':'dinátrium (Na₂) / tetranátrium (Na₄)',
   'de-at':'Dinatrium (Na₂) / Tetranatrium (Na₄)',
 },
 'natrium-szulfat-industrial':{
   'en':'anhydrous (salt-cake / industrial grade)',
   'hu':'vízmentes (salt-cake / ipari minőség)',
   'de-at':'wasserfrei (Salt-Cake / Industriequalität)',
 },
}

EN_REPL=[
 ('technikai','technical'),('regenerált','regenerated'),('monohidrát','monohydrate'),
 ('heptahidrát','heptahydrate'),('pentahidrát','pentahydrate'),('dekahidrát','decahydrate'),
 ('dodekahidrát','dodecahydrate'),('tetrahidrát','tetrahydrate'),('hexahidrát','hexahydrate'),
 ('dihidrát','dihydrate'),('anhidrát','anhydrous'),('vízmentes','anhydrous'),
 ('pikkelyes','flakes'),('nehéz','dense'),('könnyű','light'),('oldatok','solutions'),('oldat','solution'),
 ('ipari','industrial'),('kezeletlen','untreated'),('por','powder'),('jégecet','glacial acetic acid'),
 ('gyógyszerkönyvi','pharmacopoeial grade'),('nátrium-piroszulfit','sodium pyrosulfite'),
 ('szódabikarbóna','baking soda'),('99,5%','99.5%'),('99,8%','99.8%'),('3H2O','3H₂O'),
]

def clean_en_grade(v):
    if not v:return v
    out=v
    for a,b in EN_REPL: out=out.replace(a,b)
    # Humanise a few leftovers.
    out=out.replace('gran.','granular')
    return out

def clean_hu_grade(v):
    if not v:return v
    return v.replace('gran.','granulált')

def clean_de_grade(v):
    if not v:return v
    return v.replace('jégecet','Eisessig').replace('gran.','granuliert')

def load_lang(lang):
    fn={'en':'products-en.json','hu':'products-hu.json','de-at':'products-de-at.json'}[lang]
    path=ROOT/fn; d=json.load(open(path,encoding='utf8'))
    return path,d

# Load first so cross-language names can be rebuilt consistently.
lang_docs={}; by_lang={}
for lang in ('en','hu','de-at'):
    path,d=load_lang(lang); lang_docs[lang]=(path,d); by_lang[lang]={p['id']:p for p in d['products']}

# Correct names and commercial-grade localisation.
for lang,items in by_lang.items():
    for pid,p in items.items():
        if pid in SPECIAL_NAMES: p['name']=SPECIAL_NAMES[pid][lang]
        cc=p.setdefault('commercialContext',{})
        if pid in SPECIAL_GRADE:
            cc['gradeOrConcentration']=SPECIAL_GRADE[pid][lang]
        else:
            g=cc.get('gradeOrConcentration')
            if lang=='en': cc['gradeOrConcentration']=clean_en_grade(g)
            elif lang=='hu': cc['gradeOrConcentration']=clean_hu_grade(g)
            else: cc['gradeOrConcentration']=clean_de_grade(g)

# Rebuild alternateNames from authoritative localised names first, then retain useful prior aliases.
for pid in by_lang['en']:
    canon=[by_lang['en'][pid]['name'],by_lang['hu'][pid]['name'],by_lang['de-at'][pid]['name']]
    for lang in ('en','hu','de-at'):
        p=by_lang[lang][pid]
        old=p.get('alternateNames',[])
        names=[]
        own=p['name']
        for n in [own]+canon+old:
            if not n: continue
            # Drop known malformed/legacy aliases after canonical replacements.
            if pid=='edta-na2-na4-industrial' and ('— 2, Na4' in n or n=='EDTA Na2, Na4'): continue
            if pid=='kenpor-industrial' and ('— por' in n): continue
            if pid=='ecetsav-20-50-60-70-80-99-8-jegecet-food' and n.count('(')>n.count(')'): continue
            if n not in names: names.append(n)
        p['alternateNames']=names[:8]

# Write language datasets.
for lang,(path,d) in lang_docs.items():
    d['schemaVersion']=DATE
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

# Synchronise and enrich the multilingual list without breaking its existing list shape.
mp=ROOT/'products-multilingual.json'; multi=json.load(open(mp,encoding='utf8'))
for m in multi:
    pid=m['id']; en=by_lang['en'][pid]; hu=by_lang['hu'][pid]; de=by_lang['de-at'][pid]
    m['name_en']=en['name']; m['name_hu']=hu['name']; m['name_de']=de['name']
    m['sub_en']=en['name']; m['sub_hu']=hu['name']; m['sub_de']=de['name']
    ti=m.setdefault('technical_identity',{})
    ti['grade_en']=en.get('commercialContext',{}).get('gradeOrConcentration')
    ti['grade_hu']=hu.get('commercialContext',{}).get('gradeOrConcentration')
    ti['grade_de']=de.get('commercialContext',{}).get('gradeOrConcentration')
    ti['concentration_en']=ti['grade_en']; ti['concentration_hu']=ti['grade_hu']; ti['concentration_de']=ti['grade_de']
    ti['packaging_en']=en.get('commercialContext',{}).get('packaging')
    ti['packaging_hu']=hu.get('commercialContext',{}).get('packaging')
    ti['packaging_de']=de.get('commercialContext',{}).get('packaging')
    ti['synonyms_en']=en.get('alternateNames',[])[:8]
    ti['synonyms_hu']=hu.get('alternateNames',[])[:8]
    ti['synonyms_de']=de.get('alternateNames',[])[:8]
    pr=m.setdefault('procurement',{})
    pr['packaging_en']=en.get('commercialContext',{}).get('packaging')
    pr['packaging_hu']=hu.get('commercialContext',{}).get('packaging')
    pr['packaging_de']=de.get('commercialContext',{}).get('packaging')
    pr['delivery_region_en']=en.get('commercialContext',{}).get('deliveryRegion')
    pr['delivery_region_hu']=hu.get('commercialContext',{}).get('deliveryRegion')
    pr['delivery_region_de']=de.get('commercialContext',{}).get('deliveryRegion')
mp.write_text(json.dumps(multi,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('cleaned',sum(len(x) for x in by_lang.values()),'language product records and enriched multilingual dataset')
