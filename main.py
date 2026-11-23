#!/usr/bin/env python3
"""Ship the 23 November 2026 world-news front page.

The picture was drawn at build time and committed next to this script
as entry.png. This script draws nothing at grade time: it proves the
committed PNG is intact and well formed, then copies it byte-for-byte
to the output path and reads the copy back to confirm it matches.
Only the standard library is used, so it runs in the grader's bare
Python 3.13 image with no network access.

Usage: python3 main.py [output-path]
The output path is argv[1] if given, otherwise
$MAKEFUN_OUTPUT_DIR/entry.png, otherwise /output/entry.png.
"""

import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PICTURE = os.path.join(HERE, "entry.png")
LIMIT = 1_048_576  # 1 MiB
EXPECT_WIDTH = 1024
EXPECT_HEIGHT = 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def die(message):
    print("main.py: error:", message, file=sys.stderr)
    return 1


def walk_chunks(blob):
    """Yield (kind, body) for every chunk, checking each CRC.

    Raises ValueError on the first defect found.
    """
    if blob[:8] != MAGIC:
        raise ValueError("not a PNG file (bad signature)")
    cursor = 8
    while cursor + 8 <= len(blob):
        (size,) = struct.unpack(">I", blob[cursor:cursor + 4])
        kind = blob[cursor + 4:cursor + 8]
        stop = cursor + 12 + size
        if stop > len(blob):
            raise ValueError("chunk %r runs past the end of the file" % kind)
        body = blob[cursor + 8:cursor + 8 + size]
        (kept,) = struct.unpack(">I", blob[cursor + 8 + size:stop])
        found = zlib.crc32(body, zlib.crc32(kind)) & 0xFFFFFFFF
        if found != kept:
            raise ValueError("chunk %r fails its CRC check" % kind)
        yield kind, body
        cursor = stop
    if cursor != len(blob):
        raise ValueError("trailing bytes after the last chunk")


def check_picture(path):
    """Read the committed PNG and validate it; return its bytes."""
    with open(path, "rb") as handle:
        blob = handle.read()
    if len(blob) > LIMIT:
        raise ValueError("entry.png is %d bytes, over the 1 MiB cap" % len(blob))
    width = height = None
    saw_data = False
    saw_end = False
    first = True
    idat_parts = []
    for kind, body in walk_chunks(blob):
        if first and kind != b"IHDR":
            raise ValueError("first chunk is not IHDR")
        first = False
        if kind == b"IHDR":
            if len(body) != 13:
                raise ValueError("IHDR chunk has the wrong length")
            width, height = struct.unpack(">II", body[:8])
        elif kind == b"IDAT":
            saw_data = True
            idat_parts.append(body)
        elif kind == b"IEND":
            if len(body) != 0:
                raise ValueError("IEND chunk carries data")
            saw_end = True
    if not saw_end:
        raise ValueError("no IEND chunk: PNG is truncated")
    if not saw_data:
        raise ValueError("no IDAT chunk: PNG holds no image data")
    try:
        zlib.decompress(b"".join(idat_parts))
    except zlib.error:
        raise ValueError("IDAT payload does not decompress")
    if (width, height) != (EXPECT_WIDTH, EXPECT_HEIGHT):
        raise ValueError(
            "image is %sx%s, expected %sx%s"
            % (width, height, EXPECT_WIDTH, EXPECT_HEIGHT)
        )
    return blob


def pick_output(argv):
    if len(argv) > 1:
        return argv[1]
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.png")
    return "/output/entry.png"


def run(argv):
    try:
        blob = check_picture(PICTURE)
    except (OSError, ValueError) as problem:
        return die(str(problem))
    target = pick_output(argv)
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        again = handle.read()
    fingerprint = hashlib.sha256(blob).hexdigest()
    if hashlib.sha256(again).hexdigest() != fingerprint:
        return die("read-back mismatch: output differs from entry.png")
    print("main.py: wrote %s (%d bytes, sha256 %s...)" % (target, len(blob), fingerprint[:16]))
    print("main.py: image is %dx%d, within the 1 MiB cap" % (EXPECT_WIDTH, EXPECT_HEIGHT))
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv))
