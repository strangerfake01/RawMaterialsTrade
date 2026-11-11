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
    if not re.match(r'^(en|hu|de-at)-.*-(industrial|food|feed|deicing)\.html$', path.name):
        continue
    pages += 1
    source = path.read_text(encoding='utf-8')
    if re.search(r'PubChem (?:reports|formula check|:)', source):
        errors.append('Unverified PubChem comparison on page: ' + path.name)
    material_id = re.sub(r'^(en|hu|de-at)-', '', path.stem)
    if status.get(material_id) not in ('needs-confirmation', 'needs-independent-verification'):
        continue
    for script in re.findall(r'<script\b[^>]*type=["\x27]application/ld\+json["\x27][^>]*>(.*?)</script>', source, re.I | re.S):
        data = json.loads(script)
        def walk(o):
            if isinstance(o, dict):
                if o.get('@type') == 'ChemicalSubstance' and o.get('sameAs'):
                    errors.append('Unapproved ChemicalSubstance sameAs: ' + path.name)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for item in o:
                    walk(item)
        walk(data)
if pages != 378:
    errors.append(f'Expected 378 product pages, found {pages}')
print(f'Chemical source integrity: {pages} pages, {len(registry)} entities, {len(rows)} evidence rows, errors={len(errors)}')
for error in errors[:50]:
    print('ERROR:', error)
raise SystemExit(bool(errors))
