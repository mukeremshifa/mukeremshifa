"""Turn the profile photo into the ASCII portrait used by the hero.

    python tools/make_portrait.py

Two things matter here and are easy to get wrong.

1. The studio backdrop overlaps the face in luminance (the backdrop sits around
   95-133, mid-face around 123), so no threshold separates them. Instead the
   backdrop is modelled as a quadratic surface fitted to the border pixels, and
   anything departing from that model is subject. Enclosed regions are then
   filled, which recovers the face and shirt because both are ringed by hair,
   collar and jacket.

2. Polarity, which pulls in two directions. Dense glyphs on the dark parts give
   a solid silhouette, but on a dark ground more ink also reads as brighter,
   which inverts the tone. So density and colour are split: dark areas get the
   dense glyphs (silhouette) and the dim bronze (tone), highlights get sparse
   glyphs in bright gold. Two files come out, the characters and a tone band
   per cell, and the hero builder colours runs from the second.
"""

from __future__ import annotations

import pathlib
from collections import deque

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTO = ROOT / "assets" / "photo.png"
OUT = ROOT / "assets" / "portrait.txt"
OUT_TONE = ROOT / "assets" / "portrait-tone.txt"

COLS = 76
ASPECT = 0.47          # a monospace cell is roughly twice as tall as it is wide
RAMP = " .,:;irsXA253hMHGS#9B&@"
BANDS = 6


def subject_mask(gray: Image.Image) -> np.ndarray:
    W, H = gray.size
    img = np.asarray(gray.filter(ImageFilter.GaussianBlur(1.5)), dtype=float)

    ys, xs = np.mgrid[0:H, 0:W]
    band = 18
    border = np.zeros((H, W), bool)
    border[:band, :] = border[-band:, :] = True
    border[:, :band] = border[:, -band:] = True

    bx, by, bv = xs[border] / W, ys[border] / H, img[border]
    A = np.column_stack([np.ones_like(bx), bx, by, bx * bx, bx * by, by * by])
    coef, *_ = np.linalg.lstsq(A, bv, rcond=None)
    fx, fy = (xs / W).ravel(), (ys / H).ravel()
    model = (np.column_stack([np.ones(W * H), fx, fy, fx * fx, fx * fy, fy * fy])
             @ coef).reshape(H, W)

    subject = np.abs(model - img) > 22
    m = Image.fromarray((subject * 255).astype(np.uint8))
    subject = np.asarray(m.filter(ImageFilter.MaxFilter(7))
                          .filter(ImageFilter.MinFilter(7))) > 127

    # flood the exterior, so every enclosed hole counts as subject
    ext = np.zeros((H, W), bool)
    q: deque = deque()
    for x in range(W):
        for y in (0, H - 1):
            if not subject[y, x] and not ext[y, x]:
                ext[y, x] = True; q.append((x, y))
    for y in range(H):
        for x in (0, W - 1):
            if not subject[y, x] and not ext[y, x]:
                ext[y, x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= nx < W and 0 <= ny < H and not subject[ny, nx] and not ext[ny, nx]:
                ext[ny, nx] = True; q.append((nx, ny))
    mask = ~ext

    # keep the largest component only, dropping specks at the frame edge
    seen = np.zeros_like(mask); best, best_n = None, 0
    for sy in range(0, H, 4):
        for sx in range(0, W, 4):
            if mask[sy, sx] and not seen[sy, sx]:
                comp = []; q = deque([(sx, sy)]); seen[sy, sx] = True
                while q:
                    x, y = q.popleft(); comp.append((x, y))
                    for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                        if 0 <= nx < W and 0 <= ny < H and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; q.append((nx, ny))
                if len(comp) > best_n:
                    best_n, best = len(comp), comp
    clean = np.zeros_like(mask)
    for x, y in best:
        clean[y, x] = True
    return clean


def main() -> None:
    gray = Image.open(PHOTO).convert("L")
    mask = subject_mask(gray)

    sharp = ImageEnhance.Contrast(gray).enhance(1.3)
    sharp = sharp.filter(ImageFilter.UnsharpMask(radius=2, percent=130, threshold=3))
    arr = np.asarray(sharp, dtype=float)

    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    y1 = y0 + int((y1 - y0) * 0.82)      # trim the lower jacket; this is a portrait
    sub, sm = arr[y0:y1+1, x0:x1+1], mask[y0:y1+1, x0:x1+1]

    lo, hi = np.percentile(sub[sm], 3), np.percentile(sub[sm], 97)
    norm = np.clip((sub - lo) / (hi - lo), 0, 1)

    h, w = sub.shape
    rows = int(COLS * (h / w) * ASPECT)
    grid, tone = [], []
    for r in range(rows):
        ya, yb = int(r*h/rows), max(int((r+1)*h/rows), int(r*h/rows)+1)
        line, tline = [], []
        for c in range(COLS):
            xa, xb = int(c*w/COLS), max(int((c+1)*w/COLS), int(c*w/COLS)+1)
            cell = sm[ya:yb, xa:xb]
            if cell.mean() < 0.45:
                line.append(" "); tline.append(" ")
                continue
            v = norm[ya:yb, xa:xb][cell].mean()
            line.append(RAMP[int((1.0 - v) * (len(RAMP)-1) + 0.5)])   # dark -> dense
            tline.append(str(min(BANDS - 1, int(v * BANDS))))         # dark -> band 0
        grid.append(line); tone.append(tline)

    # drop near-isolated glyphs left by the mask edge
    for _ in range(2):
        rm = [(y, x) for y in range(rows) for x in range(COLS)
              if grid[y][x] != " " and sum(
                  1 for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                  if (dx or dy) and 0 <= y+dy < rows and 0 <= x+dx < COLS
                  and grid[y+dy][x+dx] != " ") <= 2]
        for y, x in rm:
            grid[y][x] = " "; tone[y][x] = " "

    keep = [i for i, r in enumerate(grid) if any(c != " " for c in r)]
    lo_r, hi_r = keep[0], keep[-1]
    chars = "\n".join("".join(r).rstrip() for r in grid[lo_r:hi_r+1])
    bands = "\n".join("".join(r).rstrip() for r in tone[lo_r:hi_r+1])
    OUT.write_text(chars, encoding="utf-8")
    OUT_TONE.write_text(bands, encoding="utf-8")
    print(chars)
    print(f"\nwrote {OUT.name} and {OUT_TONE.name}  "
          f"{COLS} cols x {len(chars.splitlines())} rows")


if __name__ == "__main__":
    main()
