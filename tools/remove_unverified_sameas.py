#!/usr/bin/env python3
"""Remove ChemicalSubstance.sameAs on products whose identity is not approved."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
registry = json.loads((root / 'entity-registry.json').read_text(encoding='utf-8'))['entities']
unapproved = {e['id'] for e in registry if e.get('sameAs_status') == 'needs-confirmation'}
pattern = re.compile(r'(<script\b[^>]*type=["\x27]application/ld\+json["\x27][^>]*>)(.*?)(</script>)', re.I | re.S)
changes = 0
for pid in sorted(unapproved):
    for lang in ('en', 'hu', 'de-at'):
        page = root / (lang + '-' + pid + '.html')
        if not page.exists():
            continue
        original = page.read_text(encoding='utf-8')
        removed = [0]
        def replace(match):
            data = json.loads(match.group(2))
            def visit(node):
                if isinstance(node, dict):
                    if node.get('@type') == 'ChemicalSubstance' and node.pop('sameAs', None) is not None:
                        removed[0] += 1
                    for value in node.values():
                        visit(value)
                elif isinstance(node, list):
                    for value in node:
                        visit(value)
            visit(data)
            if not removed[0]:
                return match.group(0)
            return match.group(1) + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + match.group(3)
        updated = pattern.sub(replace, original)
        if updated != original:
            page.write_text(updated, encoding='utf-8')
            changes += 1

(root / 'HANDOFF' / 'SAMEAS-REMEDIATION.md').write_text(
    '# Unapproved ChemicalSubstance sameAs remediation\n\n'
    f'- Removed unapproved ChemicalSubstance.sameAs from {changes} HU/EN/DE product pages.\n'
    '- Other JSON-LD entities, including Organization and WebPage, were preserved.\n'
    '- This does not determine which candidate mappings are chemically correct.\n'
    '- Promote public sameAs only after documented independent substance/form identity review.\n',
    encoding='utf-8'
)
print(f'UNAPPROVED_SAMEAS_REMOVED_FROM_PAGES={changes}')
