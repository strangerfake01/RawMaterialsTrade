#!/usr/bin/env python3
"""Apply gate for product-master updates.

The current repository has no deterministic spreadsheet-to-catalogue mapping
for high-risk chemical fields. Until that mapping is explicitly approved, an
OpenAI approval cannot mutate product pages. This guard prevents a future
workflow change from silently publishing redacted or inferred values.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print('usage: apply_approved_product_master_changes.py WORKBOOK REVIEW_JSON', file=sys.stderr)
        return 2
    review = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    if review.get('decision') != 'approve':
        print('OpenAI review blocked the release; no files changed.')
        return 1
    print('OpenAI approved, but no approved field mapping exists; refusing to publish inferred product data.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
