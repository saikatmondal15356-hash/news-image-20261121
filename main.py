#!/usr/bin/env python3
"""Write the 21 November 2026 front page to /output/entry.png.

The picture itself lives in this repository as entry.png.b64: the exact
PNG bytes, base64-encoded, one line, no wrapping. This script only
unpacks those bytes and puts them where the judge looks. It talks to
nothing, reads nothing else, and always produces the same file, so a
second run is indistinguishable from the first.

Run it from anywhere; the payload is located relative to this file,
not to the working directory.
"""

import base64
import sys
from pathlib import Path

PAYLOAD_FILENAME = "entry.png.b64"
OUTPUT_DIRECTORY = Path("/output")
OUTPUT_FILENAME = "entry.png"


def _payload_path() -> Path:
    """Where the encoded picture sits: beside this script."""
    return Path(__file__).resolve().parent / PAYLOAD_FILENAME


def _load_picture_bytes() -> bytes:
    """Decode the bundled payload, rejecting anything malformed."""
    try:
        encoded = _payload_path().read_text(encoding="ascii").strip()
    except FileNotFoundError:
        raise SystemExit("entry.png.b64 is missing beside this script.")
    if not encoded:
        raise SystemExit("entry.png.b64 is empty; there is no picture to write.")
    try:
        return base64.b64decode(encoded, validate=True)
    except ValueError:
        raise SystemExit("entry.png.b64 is not valid base64; refusing to guess.")


def _write_picture(data: bytes) -> Path:
    """Place the decoded bytes at /output/entry.png, creating the folder."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_DIRECTORY / OUTPUT_FILENAME
    target.write_bytes(data)
    return target


def main() -> int:
    picture = _load_picture_bytes()
    target = _write_picture(picture)
    print(f"wrote {target} ({len(picture)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
