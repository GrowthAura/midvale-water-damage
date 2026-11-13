#!/usr/bin/env python3
"""Build the final full-page review PDF: one page per shot (62 pages),
desktop full-page + mobile full-page per route, labelled header.
Reads ~/workspace/your_files/midvale-fullpage/*.png.
Writes ~/workspace/your_files/midvale-fullpage-review.pdf.
Images are downscaled for the PDF (desktop 1200w / mobile 520w, JPEG q80);
the PNGs in midvale-fullpage/ keep full resolution.
"""
import os, json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
SHOTS = os.path.expanduser("~/workspace/your_files/midvale-fullpage")
OUT_PDF = os.path.expanduser("~/workspace/your_files/midvale-fullpage-review.pdf")
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_title = ImageFont.truetype(FONT_B, 34) if os.path.exists(FONT_B) else ImageFont.load_default()
f_sub = ImageFont.truetype(FONT, 22) if os.path.exists(FONT) else ImageFont.load_default()

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

HEADER = 96
pages = []
missing = []
for i, p in enumerate(DATA["pages"]):
    route = p["route"]
    s = slug(route)
    for label, vw, target_w in (("desktop", "Desktop 1440", 1200), ("mobile", "Mobile 390", 520)):
        path = os.path.join(SHOTS, f"{i+1:02d}-{s}-{label}.png")
        if not os.path.exists(path):
            missing.append(path)
            continue
        im = Image.open(path).convert("RGB")
        w, h = im.size
        nw = target_w
        nh = max(1, int(h * nw / w))
        im = im.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new("RGB", (nw, HEADER + nh), "white")
        dr = ImageDraw.Draw(canvas)
        dr.rectangle([0, 0, nw, HEADER], fill=(15, 29, 46))
        dr.text((24, 12), f"{i+1:02d}  {route}  —  {vw}", font=f_title, fill="white")
        dr.text((24, 56), p["h1"][:110], font=f_sub, fill=(200, 210, 220))
        canvas.paste(im, (0, HEADER))
        pages.append(canvas)
        print(f"page {len(pages)} {i+1:02d}-{s}-{label} {w}x{h} -> {nw}x{nh}", flush=True)

if missing:
    print("MISSING:", *missing, sep="\n  ", flush=True)
    raise SystemExit(f"{len(missing)} shots missing, aborting PDF")
pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=150.0)
print(f"Wrote {OUT_PDF} ({len(pages)} pages, {os.path.getsize(OUT_PDF)/1e6:.1f} MB)", flush=True)
