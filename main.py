#!/usr/bin/env python3
"""Entry point for the news-image-20261125 dense front page.

This script is intentionally standard-library only. The grader
environment installs nothing beyond the standard library, so this
module imports nothing but ``os``, ``shutil`` and ``sys``.

The finished front page is rendered at build time by ``gen.py``
(using Pillow) and committed to the repository as ``entry.png``.
At grade time this script only copies that pre-rendered image into
the output directory the grader provides.

Layout of the repository:

    entry.png   pre-rendered front page, 1024x640, under 1 MiB
    gen.py      build-time renderer (Pillow, not used by the grader)
    main.py     this file: stdlib-only copier, used by the grader
    README.md   entry notes with the three make.fun badges

Grader contract
---------------
The grader sets the ``MAKEFUN_OUTPUT_DIR`` environment variable to
an (initially empty) output directory and runs this script from an
arbitrary working directory, with the repository mounted read-only.
This script must therefore:

* resolve ``entry.png`` relative to its own file location, never
  relative to the current working directory;
* write only inside ``MAKEFUN_OUTPUT_DIR`` (defaulting to ``out``
  when the variable is absent, for local runs);
* exit 0 after copying the image byte-for-byte;
* print a short confirmation naming the destination path.

No network access, no third-party imports and no writes outside
the output directory are performed at grade time.
"""

import os
import shutil
import sys


OUTPUT_FILENAME = "entry.png"

# Fallback output directory used only when the grader does not set
# MAKEFUN_OUTPUT_DIR (for example during a local manual run).
DEFAULT_OUTPUT_DIR = "out"


def source_path():
    """Absolute path of the pre-rendered image next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, OUTPUT_FILENAME)


def output_dir():
    """Output directory chosen by the grader, or the local default."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return chosen
    return DEFAULT_OUTPUT_DIR


def destination_path():
    """Full destination path for the copied image."""
    return os.path.join(output_dir(), OUTPUT_FILENAME)


def copy_entry():
    """Copy the pre-rendered front page into the output directory.

    Returns the destination path on success. Raises ``SystemExit``
    with a non-zero code (and a message on stderr) when the source
    image is missing or the copy cannot be completed, so a broken
    entry fails loudly instead of silently producing no output.
    """
    src = source_path()
    dst = destination_path()

    if not os.path.isfile(src):
        print("error: source image not found: %s" % src, file=sys.stderr)
        raise SystemExit(1)

    # The grader hands us an empty directory, but create it anyway
    # so local runs without MAKEFUN_OUTPUT_DIR also work.
    os.makedirs(output_dir(), exist_ok=True)

    # copyfile preserves the bytes exactly; the grader compares the
    # output image against the committed one.
    shutil.copyfile(src, dst)

    return dst


def main():
    """Entry point: copy the image and confirm where it landed."""
    dst = copy_entry()
    size = os.path.getsize(dst)
    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
