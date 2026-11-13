#!/usr/bin/env python3
"""SEO FIX 1 P3-8 trial: re-encode the 10 largest webp images at q75 with PIL
and report size + perceptual diff. Writes candidates to qa/img-opt/ for
side-by-side viewing; does NOT touch public/ — the coordinator decides
which (if any) to adopt after viewing them full-size.
Usage: python3 qa/img-opt-trial.py"""
import os, math
from PIL import Image

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa/img-opt")
os.makedirs(OUT, exist_ok=True)

# 10 largest webp under public/images
cands = []
for dp, _, fns in os.walk(os.path.join(ROOT, "public/images")):
    for f in fns:
        if f.endswith(".webp"):
            p = os.path.join(dp, f)
            cands.append((os.path.getsize(p), p))
cands.sort(reverse=True)
top = cands[:10]

def rms_diff(a: Image.Image, b: Image.Image) -> float:
    a2 = a.convert("RGB").resize((200, 112))
    b2 = b.convert("RGB").resize((200, 112))
    pa, pb = list(a2.getdata()), list(b2.getdata())
    s = 0.0
    for x, y in zip(pa, pb):
        s += sum((i - j) ** 2 for i, j in zip(x, y))
    return math.sqrt(s / (len(pa) * 3))

print(f"{'file':55s} {'orig':>8s} {'q75':>8s} {'save%':>6s} {'rms':>6s}")
for size, path in top:
    rel = os.path.relpath(path, os.path.join(ROOT, "public/images"))
    im = Image.open(path)
    dst = os.path.join(OUT, rel.replace("/", "__"))
    im.save(dst, "WEBP", quality=75, method=6)
    new = os.path.getsize(dst)
    im2 = Image.open(dst)
    print(f"{rel:55s} {size:8d} {new:8d} {100*(size-new)/size:5.1f}% {rms_diff(im, im2):6.2f}")
print("candidates in", OUT)
