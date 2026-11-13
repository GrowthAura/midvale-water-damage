#!/usr/bin/env python3
"""Re-shoot full-page screenshots AFTER scrolling through the page so lazy
images are loaded (earlier fullPage captures were taken at scroll-0 and
Chromium rendered unloaded lazy images as absent + reflowed text — a capture
artifact, not the site). TEST ONLY.
"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUTDIR = os.path.join(ROOT, "qa", "10x-design")
BASE = "http://127.0.0.1:8325/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

SCROLL = """async () => {
  const H = document.documentElement.scrollHeight;
  for (let y = 0; y <= H; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
  window.scrollTo(0, 0);
}"""

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for route in ROUTES:
        url = BASE + "/" if route == "/" else BASE + route
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(300)
        page.evaluate(SCROLL)
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(OUTDIR, f"{slug(route)}-390-full-loaded.png"), full_page=True)
        ctx.close()
        if route in ("/", "/emergency-water-extraction", "/commercial-water-damage", "/about"):
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(300)
            page.evaluate(SCROLL)
            page.wait_for_timeout(800)
            page.screenshot(path=os.path.join(OUTDIR, f"{slug(route)}-1440-full-loaded.png"), full_page=True)
            ctx.close()
        print("done", route, flush=True)
    browser.close()
print("DONE reshoot")
