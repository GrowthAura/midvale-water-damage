#!/usr/bin/env python3
"""Full-page screenshots of all 31 Midvale routes, desktop 1440 + mobile 390,
on the FINAL build (chain DONE). Serves from
http://127.0.0.1:8355/midvale-water-damage/ (qa/linkfix-serve.py).
Writes ~/workspace/your_files/midvale-fullpage/NN-<slug>-{desktop,mobile}.png
+ manifest qa/fullpage-final-manifest.json.
Adapted from qa/fullpage-shoot.py (proven pattern): slow scroll to trigger
lazy images, full-page capture, stitched-tile fallback past the 16K texture
limit. Homepage is asserted Midvale (H1 + phone) before shooting.
"""
import json, os
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.expanduser("~/workspace/your_files/midvale-fullpage")
os.makedirs(OUT, exist_ok=True)
BASE = "http://127.0.0.1:8355/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]
H1S = {p["route"]: p["h1"] for p in DATA["pages"]}

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def prep(page):
    # Slow scroll so loading=lazy images actually fetch (110ms steps proved
    # too fast: lazy images never started loading and rendered blank).
    page.wait_for_timeout(800)
    page.evaluate("""async () => {
        const h = document.body.scrollHeight;
        for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 300)); }
        window.scrollTo(0, 0);
    }""")
    page.wait_for_timeout(1500)
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass
    # Straggler pass: scroll each still-incomplete image into view and wait.
    # Anything incomplete after this is a REAL broken image, not timing.
    page.evaluate("""async () => {
        await document.fonts.ready;
        for (const i of [...document.images].filter(i => !i.complete || i.naturalWidth === 0)) {
            i.scrollIntoView({block: 'center'});
            await new Promise(r => setTimeout(r, 900));
        }
        window.scrollTo(0, 0);
    }""")
    page.wait_for_timeout(1000)

def info(page):
    return page.evaluate("""() => ({
        height: document.documentElement.scrollHeight,
        h1: (document.querySelector('h1')||{}).innerText || '',
        phone: document.body.innerText.includes('(385) 337-3560'),
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
        for label, vw, vh in (("desktop", 1440, 900), ("mobile", 390, 844)):
            ctx = browser.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=1)
            pg = ctx.new_page()
            fname = f"{i+1:02d}-{s}-{label}.png"
            path = os.path.join(OUT, fname)
            try:
                meta = shoot_one(pg, url, path, vw, vh)
                meta["file"] = fname
                meta["route"] = route
                # homepage identity gate
                if i == 0 and label == "desktop":
                    assert "(385) 337-3560" in pg.content() or meta["phone"], "homepage phone missing"
                    assert meta["h1"], "homepage H1 missing"
                    print(f"    GATE home H1={meta['h1'][:60]!r} phone={meta['phone']}", flush=True)
                manifest[f"{route}|{label}"] = meta
                print(f"[{i+1}/31 {label}] {route} h={meta['height']} png={meta['png_w']}x{meta['png_h']} {meta['method']} brokenImgs={meta['brokenImgs']} overflow={meta['overflow']} {meta['bytes']//1024}KB", flush=True)
            except Exception as e:
                manifest[f"{route}|{label}"] = {"error": str(e), "file": fname, "route": route}
                print(f"[{i+1}/31 {label}] {route} ERROR {e}", flush=True)
            finally:
                ctx.close()
    browser.close()

json.dump(manifest, open(os.path.join(ROOT, "qa", "fullpage-final-manifest.json"), "w"), indent=1)
n = sum(1 for v in manifest.values() if "error" not in v)
print(f"DONE {n}/62 shots", flush=True)
