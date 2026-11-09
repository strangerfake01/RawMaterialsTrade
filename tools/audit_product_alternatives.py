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
            section = re.search(r'<section class="product-alternative"[^>]*>(.*?)</section>', html, re.S)
            if not section:
                errors.append(f"{name}: no conditional alternative section")
                continue
            if f'href="{target}"' not in section.group(1):
                errors.append(f"{name}: wrong localized alternative link")
            if not re.search(r"<h2>.+?</h2>", section.group(1), re.S):
                errors.append(f"{name}: missing alternative heading")
            if not re.search(r"<p>.+?</p>", section.group(1), re.S):
                errors.append(f"{name}: missing technical explanation")
            checked += 1
print(f"Checked {checked} alternative sections across {len(PAIRS)} pairs x 3 languages")
for error in errors:
    print("ERROR:", error)
sys.exit(bool(errors))
