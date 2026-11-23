#!/usr/bin/env python3
"""Deliver the 23 November 2026 world-news front page.

The picture itself was rendered at build time and is committed beside
this program as entry.png. This program never draws anything: it checks
that the committed PNG is whole and well formed (PNG signature, every
chunk walked with its CRC checked, at least one IDAT chunk, ending in
IEND, 1024x1024, at most 1 MiB) and copies it byte-for-byte to the
output path, then reads the copy back and compares it with the source.
Standard library only, so
it runs in the grader's bare Python 3.13 image with no network.

Usage: python3 main.py [output-path]
Output path order: argv[1], $MAKEFUN_OUTPUT_DIR/entry.png,
/output/entry.png
"""

import hashlib
import os
import struct
import sys
import zlib

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1_048_576
WANT_W = 1024
WANT_H = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"main.py: error: {msg}", file=sys.stderr)
    return 1


def read_png(path):
    """Read and fully validate the committed PNG; return (data, error)."""
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        return None, f"entry.png is {len(data)} bytes, over the 1 MiB cap"
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        return None, "entry.png is not a PNG file"
    pos = 8
    width = height = None
    seen_iend = False
    seen_idat = False
    first = True
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            return None, f"chunk {ctype!r} overruns the file"
        body = data[pos + 8:pos + 8 + length]
        (stored_crc,) = struct.unpack(">I", data[pos + 8 + length:end])
        actual_crc = zlib.crc32(ctype)
        actual_crc = zlib.crc32(body, actual_crc) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            return None, f"chunk {ctype!r} fails its CRC check"
        if first and ctype != b"IHDR":
            return None, "first chunk is not IHDR"
        first = False
        if ctype == b"IHDR":
            if length != 13:
                return None, "IHDR chunk has the wrong length"
            width, height = struct.unpack(">II", body[:8])
        if ctype == b"IDAT":
            seen_idat = True
        if ctype == b"IEND":
            if length != 0:
                return None, "IEND chunk carries data"
            if end != len(data):
                return None, "trailing bytes after IEND"
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        return None, "no IEND chunk: PNG is truncated"
    if not seen_idat:
        return None, "no IDAT chunk: PNG holds no image data"
    if width != WANT_W or height != WANT_H:
        return None, f"image is {width}x{height}, expected {WANT_W}x{WANT_H}"
    return data, None


def main(argv):
    data, err = read_png(SOURCE)
    if err is not None:
        return fail(err)
    if len(argv) > 1:
        out = argv[1]
    elif os.environ.get("MAKEFUN_OUTPUT_DIR"):
        out = os.path.join(os.environ["MAKEFUN_OUTPUT_DIR"], "entry.png")
    else:
        out = "/output/entry.png"
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "wb") as fh:
        fh.write(data)
    with open(out, "rb") as fh:
        written = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if hashlib.sha256(written).hexdigest() != digest:
        return fail("read-back mismatch: output differs from entry.png")
    print(f"main.py: wrote {out} ({len(data)} bytes, sha256 {digest[:16]}...)")
    print(f"main.py: image is {WANT_W}x{WANT_H}, within the 1 MiB cap")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
