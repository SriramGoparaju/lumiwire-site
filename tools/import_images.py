#!/usr/bin/env python3
"""Copies the site's pictures out of the Lumiwire app repo into images/.

usage: python tools/import_images.py [path/to/lumiwire]   (default: ../lumiwire)

The screenshots are the app's own emulator captures (docs/emulator/phase-*/shots,
git-ignored in the app repo), so re-run this after a phase changes the look.
Screens lose the Android status bar and gesture bar; obstacle pictures are the
board alone (the emulator fixtures carry developer titles above the board).
"""
import os, sys
from PIL import Image

APP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "lumiwire")
SHOTS = os.path.join(APP, "docs", "emulator")
OUT = os.path.join(os.path.dirname(__file__), "..", "images")

# (output name, source shot): whole screens for the home page.
SCREENS = [
    ("screen-home", "phase-6/shots/phase6-07-home.png"),
    ("screen-journey", "phase-6/shots/phase6-04-map.png"),
    ("screen-blitz", "phase-7/shots/phase7-05-blitz-round.png"),
]
# Board crops for How to play: the first board and one per obstacle.
BOARDS = [
    ("board-basics", "phase-6/shots/phase6-02-level1.png"),
    ("obstacle-dead", "phase-5/shots/phase5-j-0051.png"),
    ("obstacle-cut", "phase-4/shots/phase4-cut-3-pair3.png"),
    ("obstacle-fuse", "phase-4/shots/phase4-fuse-0-start.png"),
    ("obstacle-relay", "phase-4/shots/phase4-relay-3-pair3.png"),
    ("obstacle-solder", "phase-4/shots/phase4-solder-0-start.png"),
    ("obstacle-bridge", "phase-8/shots/phase8-bridge-6-pair6.png"),
    ("obstacle-via", "phase-8/shots/phase8-via-3-pair3.png"),
    ("obstacle-wrap", "phase-8/shots/phase8-wrap-6-pair6.png"),
]
STATUS_BAR, GESTURE_BAR = 140, 70   # pixels at 1080 × 2340
BOARD_BAND = (520, 1840)            # the rows that hold the board on every fixture screen


def trim(im, pad=28, tol=10):
    """Crops to what differs from the corner (ground) colour, plus padding."""
    px = im.load()
    ground = px[4, 4]
    w, h = im.size
    def differs(p):
        return any(abs(a - b) > tol for a, b in zip(p, ground))
    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if differs(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        return im
    box = (max(min(xs) - pad, 0), max(min(ys) - pad, 0), min(max(xs) + pad, w), min(max(ys) + pad, h))
    return im.crop(box)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, rel in SCREENS:
        im = Image.open(os.path.join(SHOTS, rel)).convert("RGB")
        im = im.crop((0, STATUS_BAR, im.width, im.height - GESTURE_BAR))
        im.save(os.path.join(OUT, name + ".png"), optimize=True)
        print("screen", name, im.size)
    for name, rel in BOARDS:
        im = Image.open(os.path.join(SHOTS, rel)).convert("RGB")
        im = trim(im.crop((0, BOARD_BAND[0], im.width, BOARD_BAND[1])))
        im.save(os.path.join(OUT, name + ".png"), optimize=True)
        print("board", name, im.size)
    Image.open(os.path.join(APP, "assets", "icon.png")).convert("RGB").save(os.path.join(OUT, "icon.png"), optimize=True)
    print("icon")


if __name__ == "__main__":
    main()
