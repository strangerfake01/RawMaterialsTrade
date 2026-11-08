#!/usr/bin/env python3
"""Withdraw unverified automated PubChem identity/formula assertions without inventing facts."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / 'entity-registry.json'
registry = json.loads(REG.read_text(encoding='utf-8'))
ids = {e['id'] for e in registry['entities']}
changed = 0
for ident in sorted(ids):
    for lang in ('en', 'hu', 'de-at'):
        page = ROOT / (lang + '-' + ident + '.html')
        if not page.exists():
            continue
        source = page.read_text(encoding='utf-8')
        new = re.sub(r'\s*\(PubChem(?: reports|:)\s*[^)]*\)', '', source)
        new = re.sub(r',\s*PubChem formula check [A-Za-z0-9+\-\u2212]+', '', new)
        if new != source:
            page.write_text(new, encoding='utf-8')
            changed += 1

quarantined = 0
for entity in registry['entities']:
    cid = entity.get('pubchem_cid')
    formula = entity.get('pubchem_formula')
    if cid is None and formula is None:
        continue
    entity['pubchem_candidate_cid'] = cid
    entity['pubchem_candidate_formula'] = formula
    entity['pubchem_cid'] = None
    entity['pubchem_formula'] = None
    entity['pubchem_status'] = 'needs-independent-verification'
    entity['pubchem_note'] = 'Automated identity/formula matching is unverified; supplier SDS and an independent primary-source CAS/CID check required.'
    quarantined += 1
REG.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

src = ROOT / 'HANDOFF' / 'SOURCE-REGISTER.csv'
with src.open(encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fields, rows = reader.fieldnames, list(reader)
source_changed = 0
for row in rows:
    if row.get('source_type', '').lower() == 'pubchem':
        row['evidence_status'] = 'needs-independent-verification'
        row['notes'] = 'Previous automated PubChem CID/formula match NOT independently validated; do not cite as verified identity or compliance evidence.'
        source_changed += 1
with src.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

report = ROOT / 'HANDOFF' / 'CHEMISTRY-SOURCE-REMEDIATION.md'
report.write_text(
    '# Chemical source integrity remediation\n\n'
    f'- Removed unverified PubChem formula comparisons from {changed} language product pages.\n'
    f'- Quarantined {quarantined} automatically matched CID/formula entries (candidate values preserved).\n'
    f'- Downgraded {source_changed} PubChem source-register entries for independent verification.\n'
    '- Existing product names, CAS/EC, grades, and supplier-document conditions were not rewritten.\n'
    '- No invented chemical values; no form, navigation, CSS or contact changes.\n'
    '- This is a **risk-containment fix**, not a claim that all 126 product identities were externally certified.\n'
    '- Follow-up: independently validate CAS/CID/identity, EC number, grade, hydrate, concentration and regulated-use evidence.\n',
    encoding='utf-8'
)
print(f'PAGES={changed} REGISTRY={quarantined} SOURCE_ROWS={source_changed}')
