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

    def test_path_digest_is_stable_and_does_not_expose_path(self):
        path = "private/supplier-identity.pdf"
        digest = module.opaque_path_id(path)
        self.assertEqual(len(digest), 16)
        self.assertNotIn("supplier", digest)
        self.assertEqual(digest, module.opaque_path_id(path))

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
