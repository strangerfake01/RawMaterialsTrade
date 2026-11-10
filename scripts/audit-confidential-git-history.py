#!/usr/bin/env python3
"""Report potentially sensitive files across reachable Git history.

Print only aggregate counts and opaque path digests, never paths or blob content. This is a review gate:
historical exposure cannot be undone by removing the current file.
"""
import subprocess
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
    findings = {}
    for commit in commits:
        paths = git("ls-tree", "-r", "-z", "--name-only", commit).decode("utf-8", "replace").split("\0")
        for rel in paths:
            if not rel:
                continue
            p = Path(rel)
            if p.suffix.lower() in BLOCKED or p.name.lower() in NAMES:
                findings.setdefault(rel, commit)
    print(f"History inventory: {len(commits)} commits inspected; {len(findings)} restricted paths found")
    if findings:
        print("HISTORY REVIEW REQUIRED: restricted paths exist; names, identifiers and content withheld")
    if findings:
        print("Review all flagged paths in a restricted environment; do not interpret this as confirmed disclosure.")
        return 1
    print("PASS: no restricted paths found in fetched Git history; content-level historical audit still required")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
