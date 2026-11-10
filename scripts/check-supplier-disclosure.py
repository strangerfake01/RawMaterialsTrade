#!/usr/bin/env python3
"""Conservative supplier-disclosure scan of tracked repository text files.

This is a review aid, not a guarantee that no supplier can be inferred.
No scanned content is printed to CI logs.
"""
import hashlib
import json
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
    "zip_office_archive": (bytes.fromhex("504b0304"), bytes.fromhex("504b0506"), bytes.fromhex("504b0708")),
    "legacy_office_archive": (bytes.fromhex("d0cf11e0a1b11ae1"),),
    "rar_archive": (bytes.fromhex("526172211a07"),),
    "7z_archive": (bytes.fromhex("377abcaf271c"),),
}

ALLOWLIST_PATH = ROOT / "config" / "public-certificate-allowlist.txt"
CERTIFICATE_PATH = "assets/documents/certificates/cert-gmp-plus-2020.pdf"

def load_allowlist():
    if not ALLOWLIST_PATH.is_file():
        return set()
    allowed = set()
    for raw in ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line != CERTIFICATE_PATH:
            raise SystemExit("ALLOWLIST ERROR: unexpected entry; only exact company certificate is permitted")
        allowed.add(line)
    return allowed

def allowlisted_certificate_hash_ok(rel):
    if rel != CERTIFICATE_PATH:
        return False
    pin = ROOT / "config" / "public-certificate-verification.json"
    if not pin.is_file():
        return False
    try:
        meta = json.loads(pin.read_text(encoding="utf-8"))
        expected = meta.get("sha256")
        target = ROOT / rel
        if (meta.get("path") != rel or meta.get("publication_allowlist_eligible") is not True
            or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected)
            or not target.is_file() or target.is_symlink()):
            return False
        return hashlib.sha256(target.read_bytes()).hexdigest() == expected
    except (OSError, ValueError, TypeError):
        return False

def restricted_magic(data):
    return next((kind for kind, signatures in RESTRICTED_MAGIC.items() if any(data.startswith(signature) for signature in signatures)), None)

def main():
    allowlist = load_allowlist()
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    hits = []
    checked = 0
    blocked = []
    allowlisted_restricted = []
    for rel in paths:
        if not rel:
            continue
        p = Path(rel)
        if p.suffix.lower() in RESTRICTED_EXT or p.name.lower() in RESTRICTED_FILENAMES:
            if rel in allowlist and allowlisted_certificate_hash_ok(rel):
                allowlisted_restricted.append(rel)
            else:
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
            if rel in allowlist and allowlisted_certificate_hash_ok(rel):
                allowlisted_restricted.append(rel)
            else:
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
        # Ignore only the three exact synthetic positive fixtures in the test
        # module; any additional text or newly inserted disclosure is still scanned.
        if rel == "scripts/test-supplier-disclosure.py":
            synthetic_lines = (
                '"private_share_link": "internal https://drive.google.com/file/d/SYNTHETIC123/view",',
                '''"embedded_credentials": 'access_token = "SYNTHETIC_SECRET_123456"',''',
                '"supplier_contact_email": "supplier contact: test.supplier@example.invalid",',
            )
            data = "\\n".join(line for line in data.splitlines()
                             if line.strip() not in synthetic_lines)
        for label, pattern in PATTERNS.items():
            if pattern.search(data):
                hits.append((rel, label))
    print(f"Supplier disclosure screening: {checked} tracked text files checked")
    if blocked:
        print(f"REVIEW REQUIRED: {len(blocked)} restricted file(s) detected; details withheld")
    if hits:
        print(f"REVIEW REQUIRED: {len(hits)} text or signature finding(s); details withheld")
    if blocked or hits:
        return 1
    print("PASS: no restricted document types or high-confidence disclosure patterns detected; manual and historical review still required")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
