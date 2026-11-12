#!/usr/bin/env python3
"""Scoped image verification (fast): md5 + aHash for the 10 NEW heroes vs
past-site images from KNOWN site image dirs only. Reads only.
Writes qa/verify-images.json. Run with python3 -u for live progress."""
import os, hashlib, json, re, sys
from collections import defaultdict
from PIL import Image

WS = os.path.expanduser("~/workspace")
ROOT = os.path.join(WS, "midvale-water-damage")
IMG = os.path.join(ROOT, "public", "images")
NEW_HEROES = ["about", "contact", "privacy-policy", "terms-of-use", "disclaimer",
              "frozen-pipes-midvale", "winterize-swamp-cooler-utah",
              "upstairs-unit-leak-who-pays-utah", "can-mold-grow-in-utah",
              "basement-flooding-spring-snowmelt-utah"]
IMG_EXTS = (".webp", ".jpg", ".jpeg", ".png", ".avif")
# known site image roots (source dirs only, not out/ exports, not qa shots)
SITE_DIRS = []
for name in sorted(os.listdir(WS)):
    p = os.path.join(WS, name)
    if not os.path.isdir(p):
        continue
    if name.startswith("midvale") or name in ("backups", "_build", "media_library",
            "your_files", "agents", "custom-skills", "custom-connectors", "cron.d",
            "goals", "user", "memory"):
        continue
    for sub in ("public/images", "assets/img", "images", "public/images/heroes",
                "public/images/cards", "assets/images"):
        q = os.path.join(p, sub)
        if os.path.isdir(q):
            SITE_DIRS.append(q)
print(f"site image dirs: {len(SITE_DIRS)}", flush=True)

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
          "metadata": {}, "ai_word_hits": [], "dims": {}, "past_file_count": 0}

# site images
site_md5 = defaultdict(list)
for dp, _, fns in os.walk(IMG):
    for fn in fns:
        fp = os.path.join(dp, fn)
        rel = os.path.relpath(fp, ROOT)
        site_md5[md5_of(fp)].append(rel)
        try:
            im = Image.open(fp)
            report["dims"][rel] = {"size": im.size, "bytes": os.path.getsize(fp)}
        except Exception as e:
            report["dims"][rel] = {"error": str(e)}
report["site_image_count"] = sum(len(v) for v in site_md5.values())
report["site_md5_dup_groups"] = {k: v for k, v in site_md5.items() if len(v) > 1}
print(f"site images: {report['site_image_count']}, dup groups: {len(report['site_md5_dup_groups'])}", flush=True)

# past files
past_files = []
for d in SITE_DIRS:
    for dp, _, fns in os.walk(d):
        for fn in fns:
            if fn.lower().endswith(IMG_EXTS):
                past_files.append(os.path.join(dp, fn))
past_files = sorted(set(past_files))
report["past_file_count"] = len(past_files)
print(f"past-site image files: {len(past_files)}", flush=True)
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
print(f"md5 matches vs past sites: {len(report['md5_matches_past'])}", flush=True)

# aHash for the 10 new heroes
past_ah8 = []
for i, fp in enumerate(past_files):
    a8 = ahash(fp, 8)
    if a8 is not None:
        past_ah8.append((fp, a8))
    if (i + 1) % 500 == 0:
        print(f"  ahash progress {i+1}/{len(past_files)}", flush=True)
print(f"past aHash8 computed: {len(past_ah8)}", flush=True)
for n in NEW_HEROES:
    np_ = os.path.join(IMG, "heroes", n + ".webp")
    a8, a16 = ahash(np_, 8), ahash(np_, 16)
    flags = []
    for fp, pa8 in past_ah8:
        d8 = ham(a8, pa8)
        if d8 <= 8:
            pa16 = ahash(fp, 16)
            d16 = ham(a16, pa16) if pa16 is not None else None
            flags.append({"past": fp, "ahash8": d8, "ahash16": d16})
    flags.sort(key=lambda x: (x["ahash8"], x["ahash16"] if x["ahash16"] is not None else 999))
    report["ahash_flags"].append({"hero": n + ".webp", "flags": flags[:5]})
    print(f"{n}.webp: aHash8<=8 flags: {len(flags)}", flush=True)

# metadata + AI markers on the 10 new heroes
MARKERS = ["openai", "dall", "midjourney", "stable diffusion", "adobe firefly",
           "ai generated", "generated with ai", "imagen", "leonardo", "ideogram"]
for n in NEW_HEROES:
    np_ = os.path.join(IMG, "heroes", n + ".webp")
    raw = open(np_, "rb").read()
    info = {}
    try:
        im = Image.open(np_)
        info["pil_info"] = {k: str(v)[:120] for k, v in im.info.items()}
        try:
            ex = im.getexif()
            info["exif"] = {str(k): str(v)[:120] for k, v in ex.items()} if ex else {}
        except Exception as e:
            info["exif_error"] = str(e)
    except Exception as e:
        info["error"] = str(e)
    low = raw.lower()
    info["generator_markers"] = [m for m in MARKERS if m.encode() in low]
    info["ai_word_in_head"] = bool(re.search(rb"(?i)(?<![a-z])ai(?![a-z])", raw[:20000]))
    report["metadata"][n + ".webp"] = info

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
print("md5 past matches:", report["md5_matches_past"], flush=True)
print("ahash flags:", {f["hero"]: len(f["flags"]) for f in report["ahash_flags"]}, flush=True)
print("metadata markers:", {k: v.get("generator_markers") for k, v in report["metadata"].items()}, flush=True)
print("ai word hits:", report["ai_word_hits"], flush=True)
print("DONE", flush=True)
