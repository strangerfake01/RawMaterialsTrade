#!/usr/bin/env python3
"""Regression tests: substitution validator must reject unverified claims."""
import contextlib
import io
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
import importlib.util

SCRIPT = Path(__file__).with_name("check-product-substitutions.py")
spec = importlib.util.spec_from_file_location("substitution_check", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def check(registry):
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        (root / "schemas").mkdir()
        (root / "schemas/product-substitution.schema.json").write_text((SCRIPT.parent.parent / "schemas/product-substitution.schema.json").read_text(encoding="utf-8"), encoding="utf-8")
        (root / "products-multilingual.json").write_text(json.dumps([{"id": "a"}, {"id": "b"}]), encoding="utf-8")
        (root / "product-substitutions.json").write_text(json.dumps(registry), encoding="utf-8")
        with patch.object(module, "ROOT", root), contextlib.redirect_stdout(io.StringIO()):
            return module.main()

def main():
    assert check([]) == 0, "Empty unverified registry must be permitted"
    base = {
        "source_product_id": "a",
        "candidate_product_id": "b",
        "application": "Test application",
        "status": "requires_validation",
        "technical_basis": "Different technical properties require testing",
        "limitations": "No automatic substitution permitted",
        "evidence": [{"document_type": "TDS", "reference": "internal-test-document", "verification_date": "2026-11-10"}],
    }
    assert check([base]) == 0, "Well-formed research record must pass"
    assert check([{**base, "candidate_product_id": "missing"}]) != 0, "Unknown target must fail"
    assert check([{**base, "status": "approved"}]) != 0, "Unreviewed approval must fail"
    assert check([{**base, "evidence": []}]) != 0, "Missing evidence must fail"
    assert check([{**base, "candidate_product_id": "a"}]) != 0, "Self-substitution must fail"
    assert check([{**base, "invented_claim": "approved"}]) != 0, "Unknown schema fields must fail"
    assert check([{**base, "evidence": [{**base["evidence"][0], "unverified": True}]}]) != 0, "Unknown evidence fields must fail"
    assert check([{**base, "evidence": [{**base["evidence"][0], "verification_date": "2999-01-01"}]}]) != 0, "Future evidence verification must fail"
    assert check([{**base, "status": "approved", "reviewer": "Test reviewer", "review_date": "2999-01-01"}]) != 0, "Future approval must fail"
    print("PASS: substitution registry positive and negative regression fixtures")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
