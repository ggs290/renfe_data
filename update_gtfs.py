import hashlib
import os
import sys
from pathlib import Path

import requests

GTFS_CERCANIAS_URL = "https://ssl.renfe.com/ftransit/Fichero_CER_FOMENTO/fomento_transit.zip"
OUTPUT_PATH = Path("data/fomento_transit.zip")
TIMEOUT = 60


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download_file() -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GTFS-Updater/1.0)"
    }
    r = requests.get(GTFS_CERCANIAS_URL, headers=headers, timeout=TIMEOUT)
    r.raise_for_status()
    return r.content


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    old_hash = sha256_file(OUTPUT_PATH)
    content = download_file()
    new_hash = sha256_bytes(content)

    if old_hash == new_hash:
        print("No changes detected")
        return 0

    with OUTPUT_PATH.open("wb") as f:
        f.write(content)

    print(f"Updated {OUTPUT_PATH} ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
