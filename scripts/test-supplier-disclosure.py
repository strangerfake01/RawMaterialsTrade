#!/usr/bin/env python3
"""Regression tests for supplier disclosure pattern detection; no real supplier data."""
import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).with_name("check-supplier-disclosure.py")
spec = importlib.util.spec_from_file_location("supplier_disclosure", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SupplierDisclosureTests(unittest.TestCase):
    def test_detects_sensitive_synthetic_examples(self):
        examples = {
            "private_share_link": "internal https://drive.google.com/file/d/SYNTHETIC123/view",
            "embedded_credentials": 'access_token = "SYNTHETIC_SECRET_123456"',
            "supplier_contact_email": "supplier contact: test.supplier@example.invalid",
        }
        for kind, sample in examples.items():
            with self.subTest(kind=kind):
                self.assertIsNotNone(module.PATTERNS[kind].search(sample))

    def test_restricted_formats(self):
        for filename in ("secret.pdf", "quote.xlsx", "archive.zip", ".env", ".npmrc", "id_rsa"):
            with self.subTest(filename=filename):
                p = pathlib.Path(filename)
                self.assertTrue(p.suffix.lower() in module.RESTRICTED_EXT or p.name.lower() in module.RESTRICTED_FILENAMES)

    def test_certificate_hash_pin_fails_closed(self):
        import hashlib
        import json
        import tempfile
        from unittest import mock
        rel = module.CERTIFICATE_PATH
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            target = root / rel
            target.parent.mkdir(parents=True)
            target.write_bytes(b"synthetic company certificate")
            pin = root / "config" / "public-certificate-verification.json"
            pin.parent.mkdir()
            meta = {"path": rel, "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "publication_allowlist_eligible": True}
            with mock.patch.object(module, "ROOT", root):
                self.assertFalse(module.allowlisted_certificate_hash_ok(rel))
                pin.write_text(json.dumps(meta), encoding="utf-8")
                self.assertTrue(module.allowlisted_certificate_hash_ok(rel))
                self.assertFalse(module.allowlisted_certificate_hash_ok("other.pdf"))
                target.write_bytes(b"tampered")
                self.assertFalse(module.allowlisted_certificate_hash_ok(rel))
                pin.write_text("{broken", encoding="utf-8")
                self.assertFalse(module.allowlisted_certificate_hash_ok(rel))

    def test_disguised_binary_files_are_detected(self):
        examples = {
            "pdf": b"%PDF-1.7",
            "zip_office_archive": bytes.fromhex("504b0304") + b"test",
            "legacy_office_archive": bytes.fromhex("d0cf11e0a1b11ae1"),
            "rar_archive": bytes.fromhex("526172211a07"),
            "7z_archive": bytes.fromhex("377abcaf271c"),
        }
        for expected, data in examples.items():
            with self.subTest(expected=expected):
                self.assertEqual(module.restricted_magic(data), expected)
        self.assertIsNone(module.restricted_magic(b"ordinary text"))

    def test_public_ordinary_files_not_blocked_by_extension(self):
        for filename in ("index.html", "styles.css", "catalog.json", "product.js"):
            p = pathlib.Path(filename)
            self.assertNotIn(p.suffix.lower(), module.RESTRICTED_EXT)
            self.assertIn(p.suffix.lower(), module.EXT)

if __name__ == "__main__":
    unittest.main()
