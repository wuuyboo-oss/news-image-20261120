#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120.

Copies the repository's entry.png byte-for-byte to /output/entry.png.
Standard library only, no network, fully deterministic: the output bytes
are always identical to the shipped image.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
