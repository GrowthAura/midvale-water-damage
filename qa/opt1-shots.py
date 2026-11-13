#!/usr/bin/env python3
"""CYCLE 1 screenshot pass — Midvale UT. Fresh browser PER ROUTE (the shared
browser died twice mid-run, likely memory pressure from 27k-px full-page
captures). Desktop 1440 + mobile 390 full-page screenshots -> qa/opt1-uiux/.
Skips files that already exist and are non-trivial (>20KB). Retries once.
"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa", "opt1-uiux")
os.makedirs(OUT, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
BASE = "http://127.0.0.1:8351/midvale-water-damage"
ROUTES = [p["route"] for p in DATA["pages"]]

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def url(route):
    return BASE + "/" if route == "/" else BASE + route

def shoot(pw, route, label, w, h):
    path = os.path.join(OUT, f"{slug(route)}-{label}-full.png")
    if os.path.exists(path) and os.path.getsize(path) > 20000:
        return "exists"
    for attempt in (1, 2):
        try:
            b = pw.chromium.launch(args=["--disable-dev-shm-usage", "--disable-gpu", "--no-sandbox"])
            ctx = b.new_context(viewport={"width": w, "height": h})
            p = ctx.new_page()
            p.goto(url(route), wait_until="networkidle", timeout=30000)
            p.wait_for_timeout(300)
            p.evaluate("""async () => {
                const H = document.body.scrollHeight;
                for (let y = 0; y <= H; y += 800) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
                window.scrollTo(0, 0);
            }""")
            p.wait_for_timeout(300)
            p.screenshot(path=path, full_page=True, animations="disabled")
            b.close()
            return "ok"
        except Exception as e:
            print(f"  {route} {label} attempt {attempt} FAILED: {str(e)[:150]}")
            try: b.close()
            except Exception: pass
            if attempt == 2:
                return f"FAILED: {str(e)[:150]}"
    return "FAILED"

with sync_playwright() as pw:
    for route in ROUTES:
        for label, w, h in (("desktop", 1440, 900), ("m390", 390, 844)):
            r = shoot(pw, route, label, w, h)
            if r != "exists":
                print(route, label, r)
print("done")
print("files:", len(os.listdir(OUT)))
