#!/usr/bin/env python3
"""Check conditional alternative links and localized reciprocal product coverage."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PREFIXES = ("en-", "hu-", "de-at-")
PAIRS = (
    ("natrium-karbonat-konnyu-industrial", "natrium-karbonat-nehez-industrial"),
    ("vas-iii-klorid-40-oldat-industrial", "vas-iii-szulfat-40-oldat-industrial"),
    ("kalcium-klorid-dihidrat-7880-pikkelyes-deicing", "kalcium-klorid-2025-oldat-deicing"),
    ("borax-dekahidrat-industrial", "borax-pentahidrat-industrial"),
    ("natrium-hidrogen-karbonat-industrial", "natrium-hidrogen-karbonat-szodabikarbona-food"),
    ("aluminium-szulfat-03-mm-38-mm-industrial", "aluminium-szulfat-oldat-industrial"),
    ("kalium-hidroxid-pikkelyes-industrial", "kalium-hidroxid-oldat-21-45-4850-industrial"),
    ("glicerin-industrial", "glicerin-99-5-food"),
    ("magnezium-oxid-feed", "magnezium-oxid-nehez-industrial"),
    ("natrium-hidroxid-mikrogyongy-pikkelyes-industrial", "natrium-hidroxid-oldat-4850-industrial"),
    ("monoammonium-foszfat-industrial", "diammonium-hidrogenfoszfat-industrial"),
    ("kalcium-klorid-7780-food", "kalcium-klorid-dihidrat-7880-pikkelyes-deicing"),
    ("cink-szulfat-monohidrat-feed", "cink-szulfat-monohidrat-heptahidrat-industrial"),
    ("dinatrium-pirofoszfat-food", "dinatriumpirofoszfat-industrial"),
)
errors = []
checked = 0
for first, second in PAIRS:
    for prefix in PREFIXES:
        for src, dst in ((first, second), (second, first)):
            name = prefix + src + ".html"
            target = prefix + dst + ".html"
            path = ROOT / name
            if not path.is_file() or not (ROOT / target).is_file():
                errors.append(f"{name}: source or target missing")
                continue
            html = path.read_text(encoding="utf-8")
            sections = re.findall(r'<section class="product-alternative"[^>]*>(.*?)</section>', html, re.S)
            if not sections:
                errors.append(f"{name}: no conditional alternative section")
                continue
            matching = [section for section in sections if f'href="{target}"' in section]
            if not matching:
                errors.append(f"{name}: wrong localized alternative link")
                continue
            section = matching[0]
            if not re.search(r"<h2>.+?</h2>", section, re.S):
                errors.append(f"{name}: missing alternative heading")
            if not re.search(r"<p>.+?</p>", section, re.S):
                errors.append(f"{name}: missing technical explanation")
            checked += 1
print(f"Checked {checked} alternative sections across {len(PAIRS)} pairs x 3 languages")
for error in errors:
    print("ERROR:", error)
sys.exit(bool(errors))
