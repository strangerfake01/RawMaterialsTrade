#!/usr/bin/env python3
"""Conservative supplier-disclosure scan of tracked repository text files.

This is a review aid, not a guarantee that no supplier can be inferred.
No scanned content is printed to CI logs.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = {".html", ".json", ".jsonld", ".csv", ".md", ".txt", ".xml", ".yml", ".yaml"}
PATTERNS = {
    "private_share_link": re.compile(r"https?://[^\s\"'<>]*(?:drive\.google\.com/file/d/|dropbox\.com/s/|sharepoint\.com/:|onedrive\.live\.com/)", re.I),
    "embedded_credentials": re.compile(r"(?i)(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']"),
    "supplier_contact_email": re.compile(r"(?i)(?:supplier|manufacturer|vendor|besz[aá]ll[ií]t[oó]|gy[aá]rt[oó])[^\n]{0,70}[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}"),
}
EXCLUDE = {".git", "node_modules", "dist"}
def main():
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    hits = []
    checked = 0
    for rel in paths:
        if not rel:
            continue
        p = Path(rel)
        if p.suffix.lower() not in EXT or any(part in EXCLUDE for part in p.parts):
            continue
        try:
            data = (ROOT / p).read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        checked += 1
        for label, pattern in PATTERNS.items():
            if pattern.search(data):
                hits.append((rel, label))
    print(f"Supplier disclosure screening: {checked} tracked text files checked")
    if hits:
        for rel, label in hits:
            print(f"REVIEW REQUIRED: {rel}: {label} (matching content suppressed)")
        return 1
    print("PASS: no high-confidence disclosure patterns detected; manual and historical review still required")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
