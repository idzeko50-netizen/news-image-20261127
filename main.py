#!/usr/bin/env python3
"""Copy entry/entry.png to MAKEFUN_OUTPUT_DIR/entry.png and verify it.

Standard library only, no network. Run: python3 main.py
"""
import hashlib
import os
import shutil
import struct
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "entry", "entry.png")
MAX_BYTES = 1048576
MAX_DIM = 1024


def fail(message):
    print("main.py: error: %s" % message, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")
    try:
        with open(SOURCE, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read %s: %s" % (SOURCE, exc))
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png does not start with the PNG magic bytes")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk where one is expected")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        fail("entry.png is %dx%d, over the 1024x1024 limit"
             % (width, height))
    source_sha = hashlib.sha256(data).hexdigest()
    os.makedirs(out_dir, exist_ok=True)
    try:
        shutil.copyfile(SOURCE, dest)
    except OSError as exc:
        fail("cannot write %s: %s" % (dest, exc))
    try:
        with open(dest, "rb") as handle:
            copied = handle.read()
    except OSError as exc:
        fail("cannot read back %s: %s" % (dest, exc))
    if hashlib.sha256(copied).hexdigest() != source_sha:
        fail("copied entry.png does not match the source SHA-256")
    if copied[:8] != b"\x89PNG\r\n\x1a\n" or copied[12:16] != b"IHDR":
        fail("copied entry.png lost its PNG magic or IHDR chunk")
    if len(copied) != len(data):
        fail("copied entry.png is %d bytes, source is %d"
             % (len(copied), len(data)))
    os.chmod(dest, 0o644)
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dest, width, height, len(data), source_sha))


if __name__ == "__main__":
    main()
