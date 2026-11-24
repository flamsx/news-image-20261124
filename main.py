"""Entry point for the news-image-20261124 submission.

The entry image is drawn by draw.py (Pillow) and committed to this
repository as entry.png. This program is intentionally small and uses only
the Python standard library, so it runs in the grading sandbox with no
network and nothing installed: it copies the committed image to the
output directory. The copy is byte-identical on every run.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(src, os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
