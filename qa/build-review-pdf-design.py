#!/usr/bin/env python3
"""Build the rebuild review pack PDF: one page per route (31 pages),
desktop screenshot + mobile-390 screenshot side by side, labelled header.
Reads qa/render/*.png. Writes ~/workspace/your_files/midvale-design-review.pdf.
"""
import os, json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
RENDER = os.path.join(ROOT, "qa", "render")
OUT_PDF = os.path.expanduser("~/workspace/your_files/midvale-design-review.pdf")
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_title = ImageFont.truetype(FONT_B, 34) if os.path.exists(FONT_B) else ImageFont.load_default()
f_sub = ImageFont.truetype(FONT, 22) if os.path.exists(FONT) else ImageFont.load_default()
f_cap = ImageFont.truetype(FONT_B, 20) if os.path.exists(FONT_B) else ImageFont.load_default()

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

W, H = 1700, 1250
HEADER = 96
pages = []
for i, p in enumerate(DATA["pages"]):
    route = p["route"]
    s = slug(route)
    d_path = os.path.join(RENDER, f"{s}-desktop.png")
    m_path = os.path.join(RENDER, f"{s}-m390.png")
    canvas = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(canvas)
    # header bar
    dr.rectangle([0, 0, W, HEADER], fill=(15, 29, 46))
    dr.text((28, 14), f"{i+1:02d}  {route}", font=f_title, fill="white")
    dr.text((28, 58), f"{p['h1']}", font=f_sub, fill=(200, 210, 220))
    y = HEADER + 16
    # desktop left
    d = Image.open(d_path).convert("RGB")
    dw, dh = 1200, 750
    d = d.resize((dw, dh), Image.LANCZOS)
    canvas.paste(d, (28, y))
    dr.text((28, y + dh + 8), "Desktop 1440", font=f_cap, fill=(15, 29, 46))
    # mobile right
    m = Image.open(m_path).convert("RGB")
    mw, mh = 348, 753
    m = m.resize((mw, mh), Image.LANCZOS)
    canvas.paste(m, (28 + dw + 28, y))
    dr.text((28 + dw + 28, y + mh + 8), "Mobile 390", font=f_cap, fill=(15, 29, 46))
    pages.append(canvas)
    print(f"page {i+1}/31 {route}", flush=True)

pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=150.0)
print(f"Wrote {OUT_PDF} ({len(pages)} pages, {os.path.getsize(OUT_PDF)/1e6:.1f} MB)", flush=True)
