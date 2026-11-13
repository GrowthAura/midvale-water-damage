#!/usr/bin/env python3
"""Fresh-disk reuse net for Midvale hero replacements.
Corpus: every image file under each site dir's image folders, read fresh from disk NOW.
Nets: (1) md5 exact; (2) 8x8 aHash hamming; (3) 16x16 aHash hamming.
Candidates: Pexels 40701216 (jpg) + 2 generated webp heroes.
Hash nets are supporting evidence only; any aHash8 <= 12 flag gets full-size visual adjudication."""
import os, glob, hashlib, json
from PIL import Image

SITES = ["acworth-water-damage","apopka-water-damage","belleville-water-damage",
 "biohazard-cleanup-oklahoma","biohazard-cleanup-oklahoma-site","boynton-beach-water-damage",
 "broken-arrow-water-damage","cape-coral-water-damage","chesterfield-water-damage",
 "elyria-water-damage","fort-myers-water-damage","high-desert-water-restoration",
 "lynnwood-water-damage-site","mcdonough-water-damage","midvale-water-damage",
 "naples-water-damage-site","owasso-water-damage","plano-blackland-restoration",
 "plano-water-damage","plano3-water-damage","pleasant-grove-water-damage",
 "san-bruno-water-damage","stockbridge-water-damage-site","texas-water-damage-build",
 "texas-water-damage-project","texas-water-damage-site","texas-water-damage-site-preview",
 "tukwila-water-damage-site","tukwila-water-damage-site-preview","tulsa-hardwood-restoration",
 "tulsa-water-damage-repair","tulsa-water-damage-site",
 "water-damage-restoration-lancaster-ca","water-damage-restoration-tulsa-ok-new"]
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
print("CORPUS", len(corpus))

cands = {
 "pexels-40701216": "/tmp/cand-40701216.jpg",
 "gen-disclaimer": "/home/hatch/workspace/midvale-water-damage/qa/gen/media-generation-midvale-hero-disclaimer-gen-0-e2aacd2f-2c2b-44f1-b3bd-6b96e82f8247.webp",
 "gen-upstairs": "/home/hatch/workspace/midvale-water-damage/qa/gen/media-generation-midvale-hero-upstairs-gen-0-24cf23d1-a513-4d89-8127-f1575efadbf6.webp",
}
out = {"corpus_size": len(corpus), "corpus_by_site": {}, "candidates": {}}
for f in corpus:
    site = f[len(BASE)+1:].split("/")[0]
    out["corpus_by_site"][site] = out["corpus_by_site"].get(site, 0) + 1

# precompute corpus hashes (skip unreadable)
ch = []
for f in corpus:
    try:
        ch.append((f, md5(f), ahash(f, 8), ahash(f, 16)))
    except Exception as e:
        print("SKIP", f, e)
    if len(ch) % 500 == 0:
        print("HASHED", len(ch), flush=True)
print("HASHED", len(ch))
for name, cp in cands.items():
    cm, ca8, ca16 = md5(cp), ahash(cp, 8), ahash(cp, 16)
    md5hits = [f for f, m, a8, a16 in ch if m == cm]
    scored = sorted(((ham(ca8, a8), ham(ca16, a16), f) for f, m, a8, a16 in ch))[:5]
    out["candidates"][name] = {"md5": cm, "md5_hits": md5hits,
        "closest": [{"aHash8": h8, "aHash16": h16, "file": f} for h8, h16, f in scored]}
    print(name, "md5hits:", md5hits, "closest:", scored)
json.dump(out, open("/home/hatch/workspace/midvale-water-damage/qa/opt1-hero-reuse.json", "w"), indent=1)
print("WROTE qa/opt1-hero-reuse.json")
