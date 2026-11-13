#!/usr/bin/env python3
"""Targeted render re-verification for the final-5 fix (2 hero-crop card swaps).
Fresh run: homepage + 2 location pages x 1440/390/320. Checks H1, Button 2
bottom, overflow, console, failed local requests; element-screenshots the two
new cards in the rendered homepage.
"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa", "final5-fix")
os.makedirs(OUT, exist_ok=True)
BASE = "http://127.0.0.1:8350/midvale-water-damage"
PAGES = ["/", "/locations/south-salt-lake-ut", "/locations/magna-ut"]
VIEWPORTS = [(1440, 900), (390, 844), (320, 568)]
CARD_ALTS = [
    "Apartment blocks and warehouse buildings in South Salt Lake, Utah",
    "Older brick homes and storefronts on historic Main Street in Magna, Utah",
]

results = {"pages": {}, "cards": {}}
with sync_playwright() as p:
    b = p.chromium.launch()
    for route in PAGES:
        url = BASE + ("/" if route == "/" else route)
        results["pages"][route] = {}
        for w, h in VIEWPORTS:
            pg = b.new_page(viewport={"width": w, "height": h})
            console_errs, failed = [], []
            pg.on("console", lambda m: console_errs.append(m.text) if m.type == "error" else None)
            pg.on("requestfailed", lambda r: failed.append(r.url) if "google.com" not in r.url else None)
            pg.on("response", lambda r: failed.append(r.url) if r.status >= 400 and "google.com" not in r.url else None)
            pg.goto(url, wait_until="networkidle", timeout=60000)
            pg.wait_for_timeout(800)
            data = pg.evaluate("""() => {
              const btns = [...document.querySelectorAll('a,button')].filter(e => /Request Emergency Help/i.test(e.textContent||''));
              const b2 = btns[btns.length-1];
              const r = b2 ? b2.getBoundingClientRect() : null;
              const h1 = document.querySelector('h1');
              return {
                h1: h1 ? h1.textContent.trim().slice(0,80) : null,
                h1_count: document.querySelectorAll('h1').length,
                btn2_bottom: r ? Math.round(r.bottom) : null,
                btn2_visible: r ? (r.bottom <= innerHeight && r.top >= 0) : false,
                overflow: document.documentElement.scrollWidth - innerWidth,
                title: document.title.slice(0,60),
              };
            }""")
            data["console_errors"] = console_errs
            data["failed_local"] = failed
            slug = "home" if route == "/" else route.strip("/").replace("/", "-")
            shot = os.path.join(OUT, f"{slug}-{w}.png")
            pg.screenshot(path=shot, full_page=False)
            data["screenshot"] = shot
            results["pages"][route][f"{w}x{h}"] = data
            pg.close()
    # Cards on the rendered homepage @1440: element screenshots + src/alt/natural size
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(800)
    for alt in CARD_ALTS:
        info = pg.evaluate("""(alt) => {
          const img = [...document.querySelectorAll('img')].find(i => i.alt === alt);
          if (!img) return null;
          const r = img.getBoundingClientRect();
          img.scrollIntoView({block: 'center'});
          return {src: img.getAttribute('src'), cur: img.currentSrc, nw: img.naturalWidth, nh: img.naturalHeight,
                  x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
        }""", alt)
        key = "ssl" if "South Salt Lake" in alt else "magna"
        if info:
            pg.wait_for_timeout(400)
            el = pg.locator(f'img[alt="{alt}"]').first
            shot = os.path.join(OUT, f"card-rendered-{key}.png")
            el.screenshot(path=shot)
            info["element_screenshot"] = shot
        results["cards"][key] = info
    pg.close()
    b.close()

json.dump(results, open(os.path.join(OUT, "final5-fix-render.json"), "w"), indent=1)
for route, vps in results["pages"].items():
    for vp, d in vps.items():
        print(f"{route} @{vp}: h1={d['h1_count']} btn2_bottom={d['btn2_bottom']} overflow={d['overflow']} console={len(d['console_errors'])} failed={len(d['failed_local'])}")
for k, v in results["cards"].items():
    print(f"card {k}: {v}")
