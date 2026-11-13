#!/usr/bin/env python3
"""Full-page screenshots of all 31 Midvale routes, desktop 1440 + mobile 390.
Serves from http://127.0.0.1:8324/midvale-water-damage/ (qa/linkfix-serve.py).
Writes qa/fullpage/<slug>-{desktop,m390}-full.png + manifest.json.
Full-page first; if the PNG height does not match scrollHeight (Chromium
16384px texture limit), falls back to stitched viewport tiles.
"""
import json, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa", "fullpage")
os.makedirs(OUT, exist_ok=True)
BASE = "http://127.0.0.1:8324/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]
MAX_TEX = 16000

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def prep(page):
    page.wait_for_timeout(800)
    page.evaluate("""async () => {
        const h = document.body.scrollHeight;
        for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 110)); }
        window.scrollTo(0, 0);
    }""")
    page.wait_for_timeout(600)
    page.evaluate("""async () => {
        await document.fonts.ready;
        const imgs = [...document.images];
        await Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = r; i.onerror = r; setTimeout(r, 5000); })));
    }""")
    page.wait_for_timeout(400)

def info(page):
    return page.evaluate("""() => ({
        height: document.documentElement.scrollHeight,
        h1: (document.querySelector('h1')||{}).innerText || '',
        brokenImgs: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).length,
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth
    })""")

def sticky_header_h(page):
    return page.evaluate("""() => {
        const els = [...document.querySelectorAll('header, nav')];
        for (const el of els) {
            const cs = getComputedStyle(el);
            if ((cs.position === 'sticky' || cs.position === 'fixed') && el.getBoundingClientRect().top <= 1) {
                return Math.round(el.getBoundingClientRect().height);
            }
        }
        return 0;
    }""")

def stitch(page, path, vw, vh, total_h):
    """Capture viewport tiles and stitch. Tiles after the first have the
    sticky header at their top; crop it off. Returns True on success."""
    hdr = sticky_header_h(page)
    step = vh - hdr if hdr else vh
    tiles = []
    y = 0
    while y < total_h:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(350)
        tile = os.path.join(OUT, "_tile.png")
        page.screenshot(path=tile)
        im = Image.open(tile).convert("RGB")
        if y > 0 and hdr:
            im = im.crop((0, hdr, vw, vh))
        tiles.append((y, im))
        y += step
    # assemble
    canvas = Image.new("RGB", (vw, total_h), "white")
    for y, im in tiles:
        canvas.paste(im, (0, y))
    canvas.save(path)
    return True

def shoot_one(page, url, path, vw, vh):
    page.goto(url, wait_until="networkidle", timeout=60000)
    prep(page)
    meta = info(page)
    total_h = meta["height"]
    ok = False
    method = "fullpage"
    try:
        page.screenshot(path=path, full_page=True)
        with Image.open(path) as im:
            if abs(im.size[1] - total_h) <= 2:
                ok = True
            else:
                print(f"    fullpage height {im.size[1]} != scrollHeight {total_h} -> stitching", flush=True)
    except Exception as e:
        print(f"    fullpage failed ({e}) -> stitching", flush=True)
    if not ok:
        method = "stitched"
        stitch(page, path, vw, vh, total_h)
        with Image.open(path) as im:
            if abs(im.size[1] - total_h) > 2:
                raise RuntimeError(f"stitched height {im.size[1]} != {total_h}")
    meta["method"] = method
    meta["bytes"] = os.path.getsize(path)
    with Image.open(path) as im:
        meta["png_w"], meta["png_h"] = im.size
    return meta

manifest = {}
with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox"])
    for i, route in enumerate(ROUTES):
        s = slug(route)
        url = BASE + ("" if route == "/" else route)
        for label, vw, vh in (("desktop", 1440, 900), ("m390", 390, 844)):
            ctx = browser.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=1)
            pg = ctx.new_page()
            fname = f"{s}-{label}-full.png"
            path = os.path.join(OUT, fname)
            try:
                meta = shoot_one(pg, url, path, vw, vh)
                meta["file"] = fname
                manifest[f"{route}|{label}"] = meta
                print(f"[{i+1}/31 {label}] {route} h={meta['height']} png={meta['png_w']}x{meta['png_h']} {meta['method']} brokenImgs={meta['brokenImgs']} overflow={meta['overflow']} {meta['bytes']//1024}KB", flush=True)
            except Exception as e:
                manifest[f"{route}|{label}"] = {"error": str(e), "file": fname}
                print(f"[{i+1}/31 {label}] {route} ERROR {e}", flush=True)
            finally:
                ctx.close()
    browser.close()

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
n = sum(1 for v in manifest.values() if "error" not in v)
print(f"DONE {n}/62 shots", flush=True)
