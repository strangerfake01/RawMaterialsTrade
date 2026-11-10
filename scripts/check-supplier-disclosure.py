#!/usr/bin/env python3
"""Conservative supplier-disclosure scan of tracked repository text files.

This is a review aid, not a guarantee that no supplier can be inferred.
No scanned content is printed to CI logs.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = {".html", ".htm", ".json", ".jsonld", ".csv", ".md", ".txt", ".xml", ".yml", ".yaml", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".css", ".svg", ".py", ".sh", ".env", ".toml", ".ini", ".properties"}
PATTERNS = {
    "private_share_link": re.compile(r"https?://[^\s\"'<>]*(?:drive\.google\.com/file/d/|dropbox\.com/s/|sharepoint\.com/:|onedrive\.live\.com/)", re.I),
    "embedded_credentials": re.compile(r"(?i)(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']"),
    "supplier_contact_email": re.compile(r"(?i)(?:supplier|manufacturer|vendor|besz[aá]ll[ií]t[oó]|gy[aá]rt[oó])[^\n]{0,70}[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}"),
}
EXCLUDE = {".git", "node_modules", "dist"}
RESTRICTED_EXT = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".7z", ".rar", ".eml", ".msg", ".p12", ".pfx", ".pem", ".key", ".p7b", ".p7m", ".p7s", ".pkcs12"}
RESTRICTED_FILENAMES = {".env", ".env.local", ".env.production", ".npmrc", ".pypirc", "id_rsa", "id_ed25519"}
RESTRICTED_MAGIC = {
    "pdf": (b"%PDF-",),
    "zip_office_archive": (b"PK\\x03\\x04", b"PK\\x05\\x06", b"PK\\x07\\x08"),
    "legacy_office_archive": (bytes.fromhex("d0cf11e0a1b11ae1"),),
    "rar_archive": (b"Rar!\\x1a\\x07",),
    "7z_archive": (bytes.fromhex("377abcaf271c"),),
}

def restricted_magic(data):
    return next((kind for kind, signatures in RESTRICTED_MAGIC.items() if any(data.startswith(signature) for signature in signatures)), None)

def main():
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    hits = []
    checked = 0
    blocked = []
    for rel in paths:
        if not rel:
            continue
        p = Path(rel)
        if p.suffix.lower() in RESTRICTED_EXT or p.name.lower() in RESTRICTED_FILENAMES:
            blocked.append(rel)
            continue
        try:
            with (ROOT / p).open("rb") as handle:
                header = handle.read(16)
        except OSError:
            hits.append((rel, "unreadable_tracked_file"))
            continue
        signature = restricted_magic(header)
        if signature:
            hits.append((rel, f"restricted_binary_signature_{signature}"))
            continue
        if p.suffix.lower() not in EXT or any(part in EXCLUDE for part in p.parts):
            continue
        try:
            data = (ROOT / p).read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            hits.append((rel, "unreadable_text_file"))
            continue
        checked += 1
        for label, pattern in PATTERNS.items():
            if pattern.search(data):
                hits.append((rel, label))
    print(f"Supplier disclosure screening: {checked} tracked text files checked")
    if blocked:
        for rel in blocked:
            print(f"REVIEW REQUIRED: restricted file type in public repository: {rel}")
    if hits:
        for rel, label in hits:
            print(f"REVIEW REQUIRED: {rel}: {label} (matching content suppressed)")
    if blocked or hits:
        return 1
    print("PASS: no restricted document types or high-confidence disclosure patterns detected; manual and historical review still required")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
