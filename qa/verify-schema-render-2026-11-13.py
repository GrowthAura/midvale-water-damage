#!/usr/bin/env python3
"""Render checks for schema verification — Midvale UT, 2026-11-13.
Serves from the already-running local server http://localhost:8321/midvale-water-damage
(all 31 routes @320/@390: Button 2 scroll-0, overflow, console errors;
4 pages @1440/390/320: screenshots + live speakable-selector matches).
Writes qa/verify-schema-render-2026-11-13.json. Read-only on site source.
"""
import json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "workspace" / "midvale-water-damage"
BASE = "http://localhost:8322/midvale-water-damage"
DATA = json.loads((ROOT / "lib" / "pages-data.json").read_text())
ROUTES = [p["route"] for p in DATA["pages"]]
SHOT_DIR = ROOT / "qa" / "render-schema"
SHOT_DIR.mkdir(exist_ok=True)
RENDER_PAGES = ["/", "/emergency-water-extraction", "/burst-pipe-water-damage",
                "/locations/cottonwood-heights-ut"]

out = {"widths": {}, "render_pages": {}, "speakable_live": {}, "console_errors": []}

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for width in (320, 390):
        per = {}
        for route in ROUTES:
            url = BASE + ("/" if route == "/" else route)
            errs = []
            page = browser.new_page(viewport={"width": width, "height": 844})
            page.on("console", lambda m, u=url: errs.append(f"{m.type}: {m.text}") if m.type == "error" else None)
            page.on("pageerror", lambda e, u=url: errs.append(f"pageerror: {e}"))
            page.on("response", lambda r: errs.append(f"HTTP {r.status}: {r.url}") if r.status >= 400 else None)
            try:
                page.goto(url, wait_until="load", timeout=30000)
                page.wait_for_timeout(400)
                m = page.evaluate("""() => {
                  const btns = [...document.querySelectorAll('.hero .hero-buttons a')];
                  const b2 = btns[1] ? btns[1].getBoundingClientRect() : null;
                  return {
                    scrollW: document.documentElement.scrollWidth,
                    innerW: window.innerWidth,
                    vh: window.innerHeight,
                    btn2: b2 ? {top: b2.top, bottom: b2.bottom, h: b2.height, w: b2.width,
                                text: btns[1].textContent.trim()} : null,
                    btnCount: btns.length,
                    h1: document.querySelectorAll('h1').length,
                    speakFaq: document.querySelectorAll('#faq .faq-item').length,
                    speakIntro: document.querySelectorAll('.hero .intro').length,
                  };
                }""")
                per[route] = {
                    "overflow_px": m["scrollW"] - m["innerW"],
                    "btn2_scroll0": bool(m["btn2"] and m["btn2"]["bottom"] <= m["vh"] + 1 and m["btn2"]["top"] >= 0),
                    "btn2": m["btn2"], "vh": m["vh"], "btnCount": m["btnCount"],
                    "h1": m["h1"], "speak_faq": m["speakFaq"],
                    "speak_intro": m["speakIntro"], "console_errors": errs,
                }
                if errs:
                    out["console_errors"].append({"route": route, "width": width, "errors": errs})
            except Exception as e:
                per[route] = {"error": str(e)}
            page.close()
        out["widths"][width] = per
    # render pages @1440/390/320 with screenshots
    for route in RENDER_PAGES:
        for width, height in ((1440, 900), (390, 844), (320, 844)):
            page = browser.new_page(viewport={"width": width, "height": height})
            errs = []
            page.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("response", lambda r: errs.append(f"HTTP {r.status}: {r.url}") if r.status >= 400 else None)
            url = BASE + ("/" if route == "/" else route)
            page.goto(url, wait_until="load", timeout=30000)
            page.wait_for_timeout(400)
            slug = "home" if route == "/" else route.strip("/").replace("/", "_")
            shot = SHOT_DIR / f"{slug}-{width}.png"
            page.screenshot(path=str(shot))
            m = page.evaluate("""() => ({
              scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth,
              h1: [...document.querySelectorAll('h1')].map(h => h.textContent.trim()),
              heroVisible: !!document.querySelector('.hero'),
              faqItems: document.querySelectorAll('#faq .faq-item').length,
              ols: [...document.querySelectorAll('main ol, .wrap ol')].length,
            })""")
            out["render_pages"].setdefault(route, {})[width] = {
                "screenshot": str(shot.relative_to(ROOT)), "overflow_px": m["scrollW"] - m["innerW"],
                "h1": m["h1"], "heroVisible": m["heroVisible"],
                "faqItems": m["faqItems"], "console_errors": errs}
            if errs:
                out["console_errors"].append({"route": route, "width": width, "errors": errs})
            page.close()
    browser.close()

(ROOT / "qa" / "verify-schema-render-2026-11-13.json").write_text(json.dumps(out, indent=1))
for width, per in out["widths"].items():
    bad_btn2 = [r for r, v in per.items() if not v.get("btn2_scroll0")]
    bad_over = {r: v["overflow_px"] for r, v in per.items() if v.get("overflow_px", 0) > 0}
    bad_h1 = {r: v.get("h1") for r, v in per.items() if v.get("h1") != 1}
    bad_err = {r: v.get("console_errors") for r, v in per.items() if v.get("console_errors")}
    print(f"@{width}: btn2 FAIL: {bad_btn2}")
    print(f"@{width}: overflow: {bad_over}")
    print(f"@{width}: h1!=1: {bad_h1}")
    print(f"@{width}: console errors: {bad_err}")
    print(f"@{width}: speakIntro==0: {[r for r,v in per.items() if v.get('speak_intro',1)==0]}")
print("RENDER PAGES:")
for r, w in out["render_pages"].items():
    print(" ", r, {k: (v["overflow_px"], v["h1"], v["faqItems"], v["console_errors"]) for k, v in w.items()})
print("TOTAL console error entries:", len(out["console_errors"]))
