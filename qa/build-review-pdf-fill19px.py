#!/usr/bin/env python3
"""Review pack PDF for the Midvale fill + 19px verification round (2026-11-13).
Reads qa/render-fill19px/<slug>-{desktop,m390}.png (fresh viewport shots from
qa/verify-fill-19px-render.py, THIS build). Writes
~/workspace/your_files/midvale-design-review.pdf — one page per route (31),
desktop 1440 + mobile 390 side by side, labelled header.
"""
import os, json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
RENDER = os.path.join(ROOT, "qa", "render-fill19px")
OUT_PDF = os.path.expanduser("~/workspace/your_files/midvale-design-review.pdf")
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_title = ImageFont.truetype(FONT_B, 34) if os.path.exists(FONT_B) else ImageFont.load_default()
f_sub = ImageFont.truetype(FONT, 22) if os.path.exists(FONT) else ImageFont.load_default()
f_cap = ImageFont.truetype(FONT_B, 20) if os.path.exists(FONT) else ImageFont.load_default()

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
    assert os.path.exists(d_path), f"missing {d_path}"
    assert os.path.exists(m_path), f"missing {m_path}"
    canvas = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(canvas)
    dr.rectangle([0, 0, W, HEADER], fill=(15, 29, 46))
    dr.text((28, 14), f"{i+1:02d}  {route}", font=f_title, fill="white")
    dr.text((28, 58), f"{p['h1']}", font=f_sub, fill=(200, 210, 220))
    y = HEADER + 16
    d = Image.open(d_path).convert("RGB")
    dw, dh = 1200, 750
    d = d.resize((dw, dh), Image.LANCZOS)
    canvas.paste(d, (28, y))
    dr.text((28, y + dh + 8), "Desktop 1440", font=f_cap, fill=(15, 29, 46))
    m = Image.open(m_path).convert("RGB")
    mw, mh = 348, 753
    m = m.resize((mw, mh), Image.LANCZOS)
    canvas.paste(m, (28 + dw + 28, y))
    dr.text((28 + dw + 28, y + mh + 8), "Mobile 390", font=f_cap, fill=(15, 29, 46))
    pages.append(canvas)
    print(f"page {i+1}/31 {route}", flush=True)

pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=150.0)
print(f"Wrote {OUT_PDF} ({len(pages)} pages, {os.path.getsize(OUT_PDF)/1e6:.1f} MB)", flush=True)
