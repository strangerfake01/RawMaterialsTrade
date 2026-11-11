#!/usr/bin/env python3
"""Read-only privacy inventory. No email messages, contacts or customer examples stored."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
text_suffixes = {".html", ".json", ".jsonld", ".js", ".css", ".md", ".txt", ".csv", ".xml", ".yml", ".yaml", ".py", ".svg"}
high_risk = {
    "email-derived handoff or policy": re.compile(r"ENQUIRY-FIRST-EMAIL-EVIDENCE-REMEDIATION|procurement-information-policy\.json|Reviewed real office@rawmaterialstrade\.com threads", re.I),
    "private email header": re.compile(r"(?m)^(?:From|To|Cc|Bcc|Feladó|Címzett|Másolatot kap):\s+[^\n]{0,180}@", re.I),
    "embedded email correspondence": re.compile(r"(?m)^[- ]{0,4}(?:Original Message|Forwarded message|Eredeti üzenet|Továbbított üzenet)\b", re.I),
    "credentials": re.compile(r"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\s*[:=]\s*['\"][A-Za-z0-9_./+=-]{18,}['\"]"),
}
email = re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.I)

public_domains = {"rawmaterialstrade.com"}
issues = []
emails = set()
review_paths = set()
for rel in filter(None, paths):
    path = ROOT / rel
    if path.suffix.lower() not in text_suffixes or not path.is_file():
        continue
    try:
        data = path.read_text(encoding="utf-8")
    except UnicodeError:
        continue
    for label, pattern in high_risk.items():
        if rel == "tools/audit_public_privacy.py":
            continue  # Avoid treating detection signatures as leaked content.
        if pattern.search(data):
            issues.append((rel, label))
    for found in email.findall(data):
        if found.lower().split("@")[-1] not in public_domains:
            emails.add(rel)
    if path.suffix.lower() in {".html", ".json", ".md", ".csv"} and re.search(r"(?i)(?:customer|client|supplier).{0,35}(?:quoted price|agreed price|confidential|private correspondence)", data):
        review_paths.add(rel)
print(f"Privacy inventory: {len(list(filter(None, paths)))} tracked paths; {len(emails)} files contain non-company email addresses; {len(review_paths)} files need commercial-context review.")
for rel, label in sorted(set(issues)):
    print(f"BLOCK {rel}: {label}")
for rel in sorted(emails):
    print(f"REVIEW non-company email: {rel}")
for rel in sorted(review_paths):
    print(f"REVIEW commercial context: {rel}")
if issues:
    sys.exit(1)
