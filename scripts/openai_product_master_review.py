#!/usr/bin/env python3
"""Fail-closed OpenAI review gate for a product-master change manifest."""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path


SYSTEM = """You are the release reviewer for a B2B raw-materials catalogue.
Return JSON only: {\"decision\": \"approve\"|\"block\", \"reasons\": [string], \"required_actions\": [string]}.
Approve only structural, source-backed, non-commercial changes. Block changes
that could publish unsupported CAS/EC/formula/form/grade/purity claims, sameAs,
substitution claims, prices, stock, MOQ, suppliers, Incoterms, personal data,
credentials, or invisible schema claims. If values are redacted or evidence is
not present, block. The default for sameAs is withheld and substitution is
not-assessed. Never infer chemistry from a hash or field name."""


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: openai_product_master_review.py MANIFEST", file=sys.stderr)
        return 2
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY is required; refusing to approve", file=sys.stderr)
        return 1
    manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    payload = {
        "model": os.environ.get("OPENAI_REVIEW_MODEL", "gpt-4o-mini"),
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(manifest, ensure_ascii=False)},
        ],
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            body = json.loads(response.read().decode("utf-8"))
        content = body["choices"][0]["message"]["content"]
        review = json.loads(content)
    except Exception as exc:
        print(f"OpenAI review failed; refusing approval: {exc}", file=sys.stderr)
        return 1
    if review.get("decision") not in {"approve", "block"}:
        print("invalid OpenAI decision; refusing approval", file=sys.stderr)
        return 1
    Path(sys.argv[1]).with_name("openai-review.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(review, ensure_ascii=False))
    return 0 if review["decision"] == "approve" else 1


if __name__ == "__main__":
    raise SystemExit(main())
