#!/usr/bin/env python3
"""Image verification for the Midvale rebuild.
1. md5 of all 50 site images; duplicates within site.
2. md5 vs ALL past-site image files under ~/workspace (excl. midvale, node_modules, .next, qa shots).
3. aHash 8x8 + 16x16 for the 10 NEW hero images vs past-site files; flag aHash8 <= 8.
4. Metadata scan (PIL info/exif + raw strings) on the 10 new heroes; AI/generator markers.
5. Dimensions + file sizes.
Reads only; writes qa/verify-images.json.
"""
import os, hashlib, json, re
from collections import defaultdict
from PIL import Image

WS = os.path.expanduser("~/workspace")
ROOT = os.path.join(WS, "midvale-water-damage")
IMG = os.path.join(ROOT, "public", "images")
NEW_HEROES = ["about", "contact", "privacy-policy", "terms-of-use", "disclaimer",
              "frozen-pipes-midvale", "winterize-swamp-cooler-utah",
              "upstairs-unit-leak-who-pays-utah", "can-mold-grow-in-utah",
              "basement-flooding-spring-snowmelt-utah"]
IMG_EXTS = (".webp", ".jpg", ".jpeg", ".png", ".avif", ".gif")
SKIP_DIRS = {"node_modules", ".next", ".git", "__pycache__", "qa", "screenshots",
             "screenshots-full", "screenshots-a-to-z", "blunder-hunt-screenshots",
             "blunder-hunt-screenshots-sections", "round3", "round4", "round5", "round6",
             "tmp-chrome", "doc-rematch", "final-a-z"}
SKIP_PATH_PARTS = ("midvale-water-damage", "node_modules", "/.next/", "/qa/",
                   "screenshots", "media_library", "your_files")

def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def ahash(path, size):
    try:
        im = Image.open(path).convert("L").resize((size, size), Image.LANCZOS)
    except Exception:
        return None
    px = list(im.getdata())
    avg = sum(px) / len(px)
    bits = 0
    for v in px:
        bits = (bits << 1) | (1 if v > avg else 0)
    return bits

def ham(a, b):
    return bin(a ^ b).count("1")

report = {"site_images": {}, "md5_matches_past": [], "ahash_flags": [],
          "metadata": {}, "ai_word_hits": [], "dims": {}}

# ---- 1. site images ----
site_md5 = defaultdict(list)
for dp, _, fns in os.walk(IMG):
    for fn in fns:
        fp = os.path.join(dp, fn)
        rel = os.path.relpath(fp, ROOT)
        m = md5_of(fp)
        site_md5[m].append(rel)
        try:
            im = Image.open(fp)
            report["dims"][rel] = {"size": im.size, "mode": im.mode,
                                    "bytes": os.path.getsize(fp)}
        except Exception as e:
            report["dims"][rel] = {"error": str(e)}
report["site_image_count"] = sum(len(v) for v in site_md5.values())
report["site_md5_dup_groups"] = {k: v for k, v in site_md5.items() if len(v) > 1}

# ---- 2. past-site files ----
past_files = []
for dp, dns, fns in os.walk(WS):
    dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
    if any(part in dp for part in SKIP_PATH_PARTS):
        continue
    for fn in fns:
        if fn.lower().endswith(IMG_EXTS):
            past_files.append(os.path.join(dp, fn))
print(f"past-site image files collected: {len(past_files)}")
past_md5 = {}
for fp in past_files:
    try:
        past_md5.setdefault(md5_of(fp), []).append(fp)
    except Exception:
        pass
for m, rels in site_md5.items():
    if m in past_md5:
        report["md5_matches_past"].append({"site": rels, "past": past_md5[m][:5],
                                           "past_count": len(past_md5[m])})
print(f"md5 matches vs past sites: {len(report['md5_matches_past'])}")

# ---- 3. aHash for the 10 new heroes vs past files ----
new_paths = [os.path.join(IMG, "heroes", n + ".webp") for n in NEW_HEROES]
past_ah8 = []
for fp in past_files:
    a8 = ahash(fp, 8)
    if a8 is not None:
        past_ah8.append((fp, a8))
print(f"past aHash8 computed: {len(past_ah8)}")
for np_ in new_paths:
    a8 = ahash(np_, 8)
    a16 = ahash(np_, 16)
    best = []
    for fp, pa8 in past_ah8:
        d8 = ham(a8, pa8)
        if d8 <= 8:
            pa16 = ahash(fp, 16)
            d16 = ham(a16, pa16) if pa16 is not None else None
            best.append({"past": fp, "ahash8": d8, "ahash16": d16})
    best.sort(key=lambda x: (x["ahash8"], x["ahash16"] if x["ahash16"] is not None else 999))
    report["ahash_flags"].append({"hero": os.path.basename(np_), "flags": best[:5]})
    print(f"{os.path.basename(np_)}: aHash8<=8 flags: {len(best)}")

# ---- 4. metadata + AI markers on the 10 new heroes ----
MARKERS = ["openai", "dall", "midjourney", "stable diffusion", "adobe firefly",
           "ai generated", "generated with ai", "imagen", "leonardo", "ideogram"]
for np_ in new_paths:
    name = os.path.basename(np_)
    raw = open(np_, "rb").read()
    info = {}
    try:
        im = Image.open(np_)
        info["pil_info_keys"] = list(im.info.keys())
        info["pil_info"] = {k: str(v)[:120] for k, v in im.info.items()}
        try:
            ex = im.getexif()
            info["exif"] = {str(k): str(v)[:120] for k, v in ex.items()} if ex else {}
        except Exception as e:
            info["exif_error"] = str(e)
    except Exception as e:
        info["error"] = str(e)
    low = raw.lower()
    hits = [m for m in MARKERS if m.encode() in low]
    # standalone AI word in raw bytes (word-ish)
    ai_word = bool(re.search(rb"(?i)(?<![a-z])ai(?![a-z])", raw[:20000]))
    info["generator_markers"] = hits
    info["ai_word_in_head"] = ai_word
    report["metadata"][name] = info

# ---- 5. AI word in filenames / alt text (built HTML) ----
for dp, _, fns in os.walk(IMG):
    for fn in fns:
        if re.search(r"(?i)(?<![a-z])ai(?![a-z])", fn):
            report["ai_word_hits"].append({"file": fn, "where": "filename"})
for dp, _, fns in os.walk(os.path.join(ROOT, "out")):
    for fn in fns:
        if fn.endswith(".html"):
            h = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
            for m in re.finditer(r'alt="([^"]*)"', h):
                if re.search(r"(?i)\bai\b", m.group(1)):
                    report["ai_word_hits"].append({"file": fn, "where": "alt", "alt": m.group(1)})

json.dump(report, open(os.path.join(ROOT, "qa", "verify-images.json"), "w"), indent=1)
print("site images:", report["site_image_count"], "dup groups:", len(report["site_md5_dup_groups"]))
print("md5 past matches:", len(report["md5_matches_past"]))
for m in report["md5_matches_past"]:
    print("  MATCH:", m)
print("ahash flags per hero:", {f["hero"]: len(f["flags"]) for f in report["ahash_flags"]})
print("metadata generator markers:", {k: v.get("generator_markers") for k, v in report["metadata"].items()})
print("ai word hits:", report["ai_word_hits"])
print("dims sample:", dict(list(report["dims"].items())[:3]))
