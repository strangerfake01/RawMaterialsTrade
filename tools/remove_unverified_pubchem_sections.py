"""Remove unverified candidate PubChem sections from public product pages."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
section_re = re.compile(r'<section class="product-research-sources".*?</section>', re.S)
json_re = re.compile(r',"citation":\["https://pubchem\.ncbi\.nlm\.nih\.gov/compound/[^"]+"\],"additionalProperty":\[\{"@type":"PropertyValue","name":"PubChem molecular weight status","value":"source-reported; supplier SDS/TDS confirmation required"\}\]')
changed = 0
for path in ROOT.glob('*.html'):
    text = path.read_text(encoding='utf-8')
    new = section_re.sub('', text)
    new = json_re.sub('', new)
    if new != text:
        path.write_text(new, encoding='utf-8')
        changed += 1
print(f'Removed unverified PubChem sections from {changed} product pages')
