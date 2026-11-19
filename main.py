"""Make.fun bounty news-image-20261119: sum up 19 November 2026 world news in one image.
Simplest deterministic entry: copy the bundled image to /output/entry.png.
No network, same bytes on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "image.png")
OUT = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, OUT)
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
