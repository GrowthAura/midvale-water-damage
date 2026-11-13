#!/usr/bin/env python3
"""Independent reuse net for Midvale Cycle 1 new images (fresh disk reads).
Candidates: 3 new heroes + 1 body swap, as INSTALLED in public/images/.
Corpus: every image under public/images + images in all site dirs in ~/workspace.
Nets: md5 exact, 8x8 aHash, 16x16 aHash. Writes qa/reverify-reuse.json."""
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
 "heroes/disclaimer.webp": "/home/hatch/workspace/midvale-water-damage/public/images/heroes/disclaimer.webp",
 "heroes/upstairs-unit-leak-who-pays-utah.webp": "/home/hatch/workspace/midvale-water-damage/public/images/heroes/upstairs-unit-leak-who-pays-utah.webp",
 "heroes/water-damage-repair.webp": "/home/hatch/workspace/midvale-water-damage/public/images/heroes/water-damage-repair.webp",
 "body/magna-ut-1.webp": "/home/hatch/workspace/midvale-water-damage/public/images/body/magna-ut-1.webp",
}
ch = []
for f in corpus:
    try: ch.append((f, md5(f), ahash(f, 8), ahash(f, 16)))
    except Exception: pass
print("HASHED", len(ch))
out = {"corpus_size": len(corpus), "hashed": len(ch), "candidates": {}}
for name, cf in cands.items():
    cm, ca8, ca16 = md5(cf), ahash(cf, 8), ahash(cf, 16)
    md5hits = [f for f, m, a8, a16 in ch if m == cm and os.path.abspath(f) != os.path.abspath(cf)]
    scored = sorted(((ham(ca8, a8), ham(ca16, a16), f) for f, m, a8, a16 in ch if os.path.abspath(f) != os.path.abspath(cf)))[:6]
    out["candidates"][name] = {"md5": cm[:12], "md5_hits_other_sites": md5hits,
        "closest": [{"aHash8": a, "aHash16": b, "file": f} for a, b, f in scored]}
    print(name, "md5hits:", len(md5hits), "closest a8:", [(a, b, os.path.basename(f)) for a, b, f in scored[:3]])
json.dump(out, open("/home/hatch/workspace/midvale-water-damage/qa/reverify-reuse.json", "w"), indent=1)
