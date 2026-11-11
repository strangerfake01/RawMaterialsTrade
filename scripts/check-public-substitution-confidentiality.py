#!/usr/bin/env python3
"""Fail closed: the public repository must not store private substitution evidence.

The internal evidence register belongs in a separate access-controlled system.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
registry = ROOT / "product-substitutions.json"

def main():
    try:
        records = json.loads(registry.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL: public substitution registry unreadable: {exc}")
        return 1
    if records != []:
        print("FAIL: public product-substitutions.json must remain empty; never commit supplier evidence, reviewer identity, document references or internal approval records.")
        return 1
    print("PASS: public substitution registry contains no internal evidence records")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
