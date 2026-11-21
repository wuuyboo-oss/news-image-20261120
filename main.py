#!/usr/bin/env python3
"""Entry program for news-image-20261120.

Copies the generated front page (entry.png, in this same directory)
byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
Standard library only; deterministic.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
