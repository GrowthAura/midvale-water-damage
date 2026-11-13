#!/usr/bin/env python3
"""Targeted reuse net for opportunistic magna-ut-1 candidate Pexels 5587966.
Same fresh-disk corpus as opt1-hero-reuse.py (public/images + images, 34 sites).
Fast pass: md5 + aHash8 for all; aHash16 only for aHash8 <= 12 flags."""
import os, glob, hashlib, json
from PIL import Image
exec(open("qa/opt1-hero-reuse.py").read().split("corpus = []")[0].split("BASE = ")[0])  # reuse SITES list only
BASE = "/home/hatch/workspace"
def ahash(path, size=8):
    im = Image.open(path).convert("L").resize((size, size), Image.LANCZOS)
    px = list(im.getdata()); avg = sum(px)/len(px)
    return sum(1 << i for i, p in enumerate(px) if p >= avg)
def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()
def ham(a, b): return bin(a ^ b).count("1")
corpus = []
for site in SITES:
    root = os.path.join(BASE, site)
    if not os.path.isdir(root): continue
    for pat in ("public/images/**/*.*", "images/**/*.*"):
        for f in glob.glob(os.path.join(root, pat), recursive=True):
            if f.lower().endswith((".webp", ".jpg", ".jpeg", ".png")) and os.path.isfile(f):
                corpus.append(f)
corpus = sorted(set(corpus))
print("CORPUS", len(corpus), flush=True)
cand = "/tmp/cand-5587966.jpg"
cm, ca8 = md5(cand), ahash(cand, 8)
print("CAND md5", cm, "aHash8", ca8, flush=True)
md5hits, scored, flagged = [], [], []
for i, f in enumerate(corpus):
    try:
        m = md5(f); a8 = ahash(f, 8)
        if m == cm: md5hits.append(f)
        scored.append((ham(ca8, a8), f))
    except Exception as e:
        print("SKIP", f, e)
    if (i+1) % 500 == 0: print("HASHED", i+1, flush=True)
scored.sort()
closest = []
for h8, f in scored[:5]:
    a16 = ham(ahash(cand, 16), ahash(f, 16))
    closest.append({"aHash8": h8, "aHash16": a16, "file": f})
    if h8 <= 12: flagged.append(f)
print("md5hits:", md5hits, flush=True)
print("closest:", closest, flush=True)
json.dump({"corpus_size": len(corpus), "candidate": "pexels-5587966", "md5": cm,
           "md5_hits": md5hits, "closest": closest, "flagged_le12": flagged},
          open("/home/hatch/workspace/midvale-water-damage/qa/opt1-magna-reuse.json", "w"), indent=1)
print("WROTE qa/opt1-magna-reuse.json", flush=True)
