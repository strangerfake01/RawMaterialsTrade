#!/usr/bin/env python3
"""Offline, fail-closed tests for the production release verifier.

The request fixture reads the current checked-out public pages; it never opens
the network, submits an enquiry or talks to a Search Console property.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

import verify_live_release as live

SHA = "f" * 40


def fixture_request(path: str, revision: str) -> bytes:
    if revision != SHA:
        raise AssertionError("Unexpected release revision in offline fixture")
    if path == "/release-manifest.json":
        return json.dumps({
            "repository": "strangerfake01/RawMaterialsTrade",
            "commit": SHA,
        }).encode("utf-8")
    file_path = live.ROOT / (path.lstrip("/") or "index.html")
    return file_path.read_bytes()


class LiveReleaseGateTests(unittest.TestCase):
    def test_matching_source_fixture_is_accepted_without_network(self):
        with patch.object(live, "request", side_effect=fixture_request):
            result = live.verify_once(SHA)
        self.assertEqual(result["manifestSha"], SHA)
        self.assertEqual(result["sitemapUrls"], len(live.parse_sitemap((live.ROOT / "sitemap.xml").read_bytes())))
        self.assertEqual(result["criticalHtmlPagesChecked"], len(live.CRITICAL_PAGES) + len(live.PRODUCT_PAGES))

    def test_wrong_manifest_sha_is_rejected(self):
        def wrong_sha(path, revision):
            if path == "/release-manifest.json":
                return json.dumps({
                    "repository": "strangerfake01/RawMaterialsTrade",
                    "commit": "0" * 40,
                }).encode("utf-8")
            return fixture_request(path, revision)
        with patch.object(live, "request", side_effect=wrong_sha):
            with self.assertRaisesRegex(RuntimeError, "revision mismatch"):
                live.verify_once(SHA)

    def test_duplicate_location_with_different_lastmod_is_rejected(self):
        parser = live.parse_sitemap
        def duplicate_loc(data):
            entries = parser(data)
            self.assertGreater(len(entries), 0)
            entries.append((entries[0][0], "2099-12-31"))
            return entries
        with patch.object(live, "request", side_effect=fixture_request):
            with patch.object(live, "parse_sitemap", side_effect=duplicate_loc):
                with self.assertRaisesRegex(RuntimeError, "duplicate loc URLs"):
                    live.verify_once(SHA)

    def test_changed_live_sitemap_is_rejected(self):
        def modified_sitemap(path, revision):
            if path == "/sitemap.xml":
                return b'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
            return fixture_request(path, revision)
        with patch.object(live, "request", side_effect=modified_sitemap):
            with self.assertRaisesRegex(RuntimeError, "Sitemap differs"):
                live.verify_once(SHA)


if __name__ == "__main__":
    unittest.main()
