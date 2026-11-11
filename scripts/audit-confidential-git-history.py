#!/usr/bin/env python3
"""Report potentially sensitive files across reachable Git history.

Print aggregate counts only, never paths, identifiers or blob content. This is a review gate:
historical exposure cannot be undone by removing the current file.
"""
import subprocess
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKED = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".7z", ".rar", ".eml", ".msg", ".pem", ".key", ".p12", ".pfx"}
NAMES = {".env", ".env.local", ".env.production", ".npmrc", ".pypirc", "id_rsa", "id_ed25519"}

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL)

def main():
    # All fetched refs are scanned. GitHub Actions checkout is shallow by default,
    # so a dedicated history-audit job must fetch-depth: 0.
    if git("rev-parse", "--is-shallow-repository").decode().strip() != "false":
        print("FAIL: Git history is shallow; full history review is not possible")
        return 1
    commits = git("rev-list", "--all").decode().splitlines()
    if not commits:
        print("FAIL: no reachable commits available for history review")
        return 1
    # Include all changed paths from fetched refs, including deleted and renamed files.
    # NUL delimiters preserve filenames containing whitespace or newlines.
    changed = git("log", "--all", "--pretty=format:", "--name-only", "-z").decode("utf-8", "replace").split("\0")
    findings = set()
    for rel in changed:
        rel = rel.strip("\n")
        if not rel:
            continue
        p = Path(rel)
        if p.suffix.lower() in BLOCKED or p.name.lower() in NAMES:
            findings.add(rel)
    known_company_certificate_paths = {
        "cert-gmp-plus-2020.pdf",
        "assets/documents/certificates/cert-gmp-plus-2020.pdf",
    }
    known = findings & known_company_certificate_paths
    unknown = findings - known_company_certificate_paths
    print(f"History inventory: {len(commits)} reachable commits; {len(findings)} restricted path(s) found")
    print(f"Historical path classification: {len(known)} known company certificate path(s), {len(unknown)} other restricted path(s)")
    # A historical path match is not proof of a safe blob. Every reachable
    # revision of the two explicitly approved paths must match the pinned PDF.
    if unknown:
        print("HISTORY REVIEW REQUIRED: unknown restricted historical path(s)")
        return 1
    if known:
        try:
            pin = json.loads((ROOT / "config" / "public-certificate-verification.json").read_text(encoding="utf-8"))
            expected = pin["sha256"]
            if (pin.get("publication_allowlist_eligible") is not True
                    or pin.get("path") != "assets/documents/certificates/cert-gmp-plus-2020.pdf"
                    or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected)):
                raise ValueError("invalid pin")
            checked = set()
            for path in sorted(known):
                revisions = git("rev-list", "--objects", "--all", "--", path).decode("utf-8", "replace").splitlines()
                if not revisions:
                    raise ValueError("historical path has no objects")
                for entry in revisions:
                    oid = entry.split(" ", 1)[0]
                    if oid in checked:
                        continue
                    if git("cat-file", "-t", oid).strip() != b"blob":
                        continue
                    checked.add(oid)
                    if hashlib.sha256(git("cat-file", "blob", oid)).hexdigest() != expected:
                        print("HISTORY REVIEW REQUIRED: historical certificate content differs from approved SHA-256")
                        return 1
            print(f"Historical certificate verification: {len(checked)} distinct object(s) checked against approved SHA-256")
        except (OSError, KeyError, ValueError, subprocess.CalledProcessError):
            print("HISTORY REVIEW REQUIRED: unable to verify all historical certificate objects")
            return 1
        print("PASS: only approved company certificate paths and pinned certificate bytes found in reachable history")
        return 0
    if findings:
        print("HISTORY REVIEW REQUIRED: restricted paths exist; names, identifiers and content withheld")
    if findings:
        print("Review all flagged paths in a restricted environment; do not interpret this as confirmed disclosure.")
        return 1
    print("PASS: no restricted extensions or names in fetched reachable Git history; unreferenced objects, other clones, and blob contents are not covered")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
