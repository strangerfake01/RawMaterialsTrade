#!/usr/bin/env python3
"""Fail if previously unverified chemical source matches leak into public claims."""
import csv
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
registry = json.loads((root / 'entity-registry.json').read_text(encoding='utf-8'))['entities']
status = {e['id']: e.get('sameAs_status') for e in registry}
errors = []
products = json.loads((root / 'products-multilingual.json').read_text(encoding='utf-8'))
expected_ids = {p['id'] for p in products}
registry_ids = [e['id'] for e in registry]
if len(registry_ids) != len(set(registry_ids)):
    errors.append('Duplicate registry product IDs')
if set(registry_ids) != expected_ids:
    errors.append('Entity registry must cover every catalogue product exactly: missing=' + str(sorted(expected_ids - set(registry_ids))) + ' extras=' + str(sorted(set(registry_ids) - expected_ids)))
for e in registry:
    if e['id'] == 'utszoro-zeolit-deicing' and e.get('wikidata_qid') == 'Q191323':
        errors.append('Unproven Zeolite A framework in entity registry')
    if e.get('sameAs_status') == 'verified':
        errors.append('Heuristic registry identity still marked verified without independent provenance: ' + e['id'])
    if not e.get('sameAs_status'):
        errors.append('Registry identity missing explicit review status: ' + e['id'])
    for field in ('cas','pubchem_cid'):
        value = e.get(field)
        if isinstance(value,str) and ('confirm' in value.lower() or 'specific' in value.lower()):
            errors.append('Unverified narrative stored as '+field+' identifier: '+e['id'])

for e in registry:
    if e.get('pubchem_status') == 'needs-independent-verification':
        if e.get('pubchem_cid') is not None or e.get('pubchem_formula') is not None:
            errors.append('Quarantined PubChem mapping exposed: ' + e['id'])
    elif e.get('pubchem_cid') is not None or e.get('pubchem_formula') is not None:
        errors.append('PubChem mapping lacking verified provenance: ' + e['id'])

with (root / 'HANDOFF/SOURCE-REGISTER.csv').open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
for row in rows:
    if row['source_type'].casefold() == 'pubchem' and row['evidence_status'] != 'needs-independent-verification':
        errors.append('Unreviewed PubChem source incorrectly marked verified: ' + row['product_id'])

pages = 0
for path in root.glob('*.html'):
    if not re.match(r'^(en|hu|de-at)-.*-(industrial|food|feed|deicing|futtermittel)\.html$', path.name):
        continue
    pages += 1
    source = path.read_text(encoding='utf-8')
    if re.search(r'PubChem (?:reports|formula check|:)', source):
        errors.append('Unverified PubChem comparison on page: ' + path.name)
    material_id = re.sub(r'^(en|hu|de-at)-', '', path.stem)
    if path.name in ('en-copper-oxide-feed.html', 'hu-rez-oxid-feed.html', 'de-at-kupferoxid-futtermittel.html'):
        if re.search(r'Zinc(?:%20|_|\s+)Chloride|Zinkchlorid|Cink-klorid|Q204714|Zinc salt used as flux|Erősen higroszkópos cinksó|Flussmittel beim Verzinken und Löten|Zn(?:-Gehalt|-tartalmat| assay)|battery electrolyte|Batterieelektrolyt|Zinkergänzung|feed zinc supplement|Forrasztási fluxok', source, re.I):
            errors.append('Unrelated zinc-chloride source copied into copper-oxide page: ' + path.name)
        if path.name.startswith('en-') and source.count('?product=Copper%28II%29%20oxide%20/%20') != 6:
            errors.append('Copper-oxide EN enquiry prefill not preserved on all six enquiry buttons')

    # Source quarantine must cover the actual rendered HTML and machine schema.
    if material_id in ('natronvizuveg-oldatok-industrial', 'utszoro-zeolit-deicing'):
        if re.search(r'external-identity-orientation|Na2O3Si|122\.063|23266|9942228|Q191323|Q72508125|Zeolite A', source, re.I):
            errors.append('Rejected exact identity appears on variable-family page: ' + path.name)
        if '<dl class="product-dl">' not in source:
            errors.append('Variable-family procurement detail missing on page: ' + path.name)
    if material_id == 'rez-klorid-dihidrat-industrial' and re.search(r'Cl2CuH2O|152\.46|16219111', source):
        errors.append('Rejected one-water copper chloride data on a dihydrate page: ' + path.name)
    if status.get(material_id) not in ('needs-confirmation', 'needs-independent-verification'):
        continue
    for script in re.findall(r'<script\b[^>]*type=["\x27]application/ld\+json["\x27][^>]*>(.*?)</script>', source, re.I | re.S):
        data = json.loads(script)
        def walk(o):
            if isinstance(o, dict):
                if (material_id in ('natronvizuveg-oldatok-industrial', 'utszoro-zeolit-deicing')
                        and o.get('@type') == 'ChemicalSubstance'
                        and any(k in o for k in ('identifier', 'chemicalComposition', 'molecularFormula', 'molecularWeight'))):
                    errors.append('Exact identifier or formula on variable-family schema: ' + path.name)
                if o.get('@type') == 'ChemicalSubstance' and o.get('sameAs'):
                    errors.append('Unapproved ChemicalSubstance sameAs: ' + path.name)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for item in o:
                    walk(item)
        walk(data)
if pages != 381:
    errors.append(f'Expected 381 product pages, found {pages}')
print(f'Chemical source integrity: {pages} pages, {len(registry)} entities, {len(rows)} evidence rows, errors={len(errors)}')
for error in errors[:50]:
    print('ERROR:', error)
raise SystemExit(bool(errors))
