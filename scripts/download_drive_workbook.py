#!/usr/bin/env python3
"""Download a Google Drive file with a service-account JSON secret."""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


def b64(data: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def main() -> int:
    if len(sys.argv) != 4:
        print('usage: download_drive_workbook.py SERVICE_ACCOUNT_JSON FILE_ID OUTPUT', file=sys.stderr)
        return 2
    service = json.loads(sys.argv[1])
    now = int(time.time())
    header = b64(json.dumps({'alg': 'RS256', 'typ': 'JWT'}).encode())
    claim = b64(json.dumps({
        'iss': service['client_email'],
        'scope': 'https://www.googleapis.com/auth/drive.readonly',
        'aud': 'https://oauth2.googleapis.com/token',
        'iat': now,
        'exp': now + 3600,
    }).encode())
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
    except ImportError:
        print('cryptography is required', file=sys.stderr)
        return 1
    key = serialization.load_pem_private_key(service['private_key'].encode(), password=None)
    signature = key.sign(f'{header}.{claim}'.encode(), padding.PKCS1v15(), hashes.SHA256())
    assertion = f'{header}.{claim}.{b64(signature)}'
    token_req = urllib.request.Request(
        'https://oauth2.googleapis.com/token',
        data=urllib.parse.urlencode({'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': assertion}).encode(),
        method='POST',
    )
    with urllib.request.urlopen(token_req, timeout=30) as response:
        token = json.loads(response.read())['access_token']
    file_id = urllib.parse.quote(sys.argv[2], safe='')
    req = urllib.request.Request(
        f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media',
        headers={'Authorization': f'Bearer {token}'},
    )
    output = Path(sys.argv[3])
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=120) as response:
        output.write_bytes(response.read())
    print(f'downloaded {output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
