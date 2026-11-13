#!/usr/bin/env python3
"""Definitive all-routes image check (Stage 1 verifier, 2026-11-13).
The first render script's scroll was defeated by `html { scroll-behavior:
smooth; }` — its 60ms-step scrollTo loop never reached the bottom of long
pages, so lazy images there never loaded (48 false 'broken' flags, 0 failed
requests). This re-check scrolls in passes until scrollHeight is stable,
waits 2s, then verifies every <main> img decodes (naturalWidth > 0).
Also records failed requests per page.
Writes qa/uiux-images-all-2026-11-13.json
"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
BASE = "http://127.0.0.1:8341/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]

def url(route):
    return BASE + "/" if route == "/" else BASE + route

out = {"pages": {}, "problems": [], "site": {"total_imgs": 0, "total_broken": 0, "failed_requests": 0}}
with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--disable-gpu", "--no-sandbox"])
    for route in ROUTES:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        failed = []
        page.on("response", lambda resp: failed.append(f"{resp.status} {resp.url}") if resp.status >= 400 else None)
        page.goto(url(route), wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(300)
        page.evaluate("""async () => {
            for (let pass = 0; pass < 6; pass++) {
                const before = document.body.scrollHeight;
                for (let y = window.scrollY; y <= document.body.scrollHeight; y += 400) {
                    window.scrollTo(0, y);
                    await new Promise(r => setTimeout(r, 120));
                }
                window.scrollTo(0, document.body.scrollHeight);
                await new Promise(r => setTimeout(r, 800));
                if (document.body.scrollHeight === before) break;
            }
        }""")
        page.wait_for_timeout(2000)
        imgs = page.evaluate("""() => [...document.querySelectorAll('main img')].map(im => ({
            src: im.getAttribute('src'), ok: im.complete && im.naturalWidth > 0,
            w: im.naturalWidth, h: im.naturalHeight
        }))""")
        bad = [i for i in imgs if not i["ok"]]
        out["pages"][route] = {"imgs": len(imgs), "broken": [i["src"] for i in bad], "failed_requests": failed}
        out["site"]["total_imgs"] += len(imgs)
        out["site"]["total_broken"] += len(bad)
        out["site"]["failed_requests"] += len(failed)
        if bad:
            out["problems"].append({"sev": "P1", "route": route, "what": "broken images after proper scroll", "detail": [i["src"] for i in bad]})
        if failed:
            out["problems"].append({"sev": "P2", "route": route, "what": "failed requests", "detail": failed[:5]})
        ctx.close()
    browser.close()

json.dump(out, open(os.path.join(ROOT, "qa/uiux-images-all-2026-11-13.json"), "w"), indent=1)
print("routes:", len(ROUTES), "| total imgs in main:", out["site"]["total_imgs"],
      "| broken:", out["site"]["total_broken"], "| failed requests:", out["site"]["failed_requests"])
print("PROBLEMS:", len(out["problems"]))
for pb in out["problems"]:
    print(" -", pb["sev"], pb["route"], pb["what"], str(pb.get("detail", ""))[:200])
