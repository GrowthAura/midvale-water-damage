#!/usr/bin/env python3
"""F4 baseline (BEFORE) measurements — Midvale Cycle 1 UI/UX fix.
Serves the CURRENT out/ (pre-fix export) on port 8401.
Measures per-route hero crop at 390, Button 2 at 320/390, overflow,
console errors, logo + radio heights; takes before screenshots.
Usage: python3 qa/opt1-fix-baseline.py
"""
import json, math, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8401/midvale-water-damage"
ROUTES = [
    "/", "/about", "/contact", "/emergency-water-extraction",
    "/basement-flooding-cleanup", "/window-well-flooding",
    "/burst-pipe-water-damage", "/sewage-backup-cleanup",
    "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage",
    "/ceiling-water-damage", "/crawl-space-water-damage",
    "/hardwood-floor-cabinet-drying", "/condo-apartment-water-damage",
    "/commercial-water-damage", "/storm-flood-damage", "/mold-remediation",
    "/water-leak-detection", "/water-damage-repair",
    "/locations/cottonwood-heights-ut", "/locations/south-salt-lake-ut",
    "/locations/magna-ut", "/midvale-water-sewer-emergency-contacts",
    "/privacy-policy", "/terms-of-use", "/disclaimer",
    "/resources/frozen-pipes-midvale",
    "/resources/winterize-swamp-cooler-utah",
    "/resources/upstairs-unit-leak-who-pays-utah",
    "/resources/can-mold-grow-in-utah",
    "/resources/basement-flooding-spring-snowmelt-utah",
]
OUT = os.path.expanduser("~/workspace/midvale-water-damage/qa/opt1-fix-uiux/before")
os.makedirs(OUT, exist_ok=True)
WIDE = ["/", "/about", "/locations/cottonwood-heights-ut",
        "/locations/magna-ut", "/locations/south-salt-lake-ut"]

results = {"routes": {}, "logo": {}, "radio": {}, "button2": {}, "console_errors": []}

with sync_playwright() as pw:
    b = pw.chromium.launch()
    # --- 390px: hero crop + overflow + console ---
    pg = b.new_page(viewport={"width": 390, "height": 844})
    for r in ROUTES:
        errs = []
        pg.on("console", lambda m, e=errs: e.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e, errs=errs: errs.append(str(e)))
        pg.goto(BASE + ("" if r == "/" else r), wait_until="load")
        pg.wait_for_timeout(400)
        m = pg.evaluate("""() => {
          const img = document.querySelector('.hero-img');
          const r = img ? img.getBoundingClientRect() : null;
          const b2 = [...document.querySelectorAll('.hero-buttons .btn-help')][0];
          const b2r = b2 ? b2.getBoundingClientRect() : null;
          return {
            hero: r ? {w: r.width, h: r.height} : null,
            b2bottom390: b2r ? b2r.bottom : null,
            overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            imgW: img ? img.getAttribute('width') : null,
            imgH: img ? img.getAttribute('height') : null,
            hasBreadcrumbId: !!document.getElementById('breadcrumb'),
            hasHeroImgId: !!document.getElementById('hero-image'),
          };
        }""")
        if m["hero"]:
            scale = max(m["hero"]["w"] / 1600, m["hero"]["h"] / 1066)
            vis = m["hero"]["w"] / (1600 * scale)
            m["hero"]["scale"] = round(scale, 4)
            m["hero"]["visible_fraction"] = round(vis, 4)
            m["hero"]["visible_pct"] = round(vis * 100, 1)
        results["routes"][r] = m
        if errs:
            results["console_errors"].append({"route": r, "errors": errs})
        # hero viewport shot for wide scenes + homepage
        if r in WIDE:
            slug = "home" if r == "/" else r.strip("/").replace("/", "-")
            pg.screenshot(path=f"{OUT}/{slug}-m390-hero.png")
    pg.close()

    # --- 320px: Button 2 at scroll 0 ---
    pg = b.new_page(viewport={"width": 320, "height": 568})
    for r in ROUTES:
        pg.goto(BASE + ("" if r == "/" else r), wait_until="load")
        pg.wait_for_timeout(300)
        b2 = pg.evaluate("""() => {
          const b = [...document.querySelectorAll('.hero-buttons .btn-help')][0];
          return b ? b.getBoundingClientRect().bottom : null;
        }""")
        results["button2"][r] = b2
    pg.close()

    # --- 1440px: logo height, homepage cards, contact radios ---
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE, wait_until="load")
    pg.wait_for_timeout(400)
    results["logo"]["1440"] = pg.evaluate(
        "() => { const a=document.querySelector('a.brand'); const r=a.getBoundingClientRect(); return {w:r.width,h:r.height}; }")
    pg.screenshot(path=f"{OUT}/home-desktop-full.png", full_page=True)
    # card grid crop: first card row
    el = pg.query_selector(".card-grid")
    if el:
        el.screenshot(path=f"{OUT}/home-desktop-cards.png")
    pg.goto(BASE + "/contact", wait_until="load")
    pg.wait_for_timeout(400)
    results["radio"]["1440"] = pg.evaluate("""() => {
      return [...document.querySelectorAll('.radio-row label')].map(l => {
        const r = l.getBoundingClientRect(); return {text: l.textContent.trim(), w: Math.round(r.width), h: Math.round(r.height)};
      });
    }""")
    form = pg.query_selector(".contact-form")
    if form:
        form.screenshot(path=f"{OUT}/contact-desktop-form.png")
    # mobile logo height
    pg2 = b.new_page(viewport={"width": 390, "height": 844})
    pg2.goto(BASE, wait_until="load")
    pg2.wait_for_timeout(300)
    results["logo"]["390"] = pg2.evaluate(
        "() => { const a=document.querySelector('a.brand'); const r=a.getBoundingClientRect(); return {w:Math.round(r.width),h:Math.round(r.height)}; }")
    pg2.screenshot(path=f"{OUT}/home-m390-full.png", full_page=True)
    pg2.close()
    b.close()

json.dump(results, open(os.path.expanduser(
    "~/workspace/midvale-water-damage/qa/opt1-fix-baseline.json"), "w"), indent=2)

# summary
vis = [results["routes"][r]["hero"]["visible_pct"] for r in ROUTES if results["routes"][r].get("hero")]
print("hero visible fraction @390: min %.1f%%  max %.1f%%  mean %.1f%%" % (min(vis), max(vis), sum(vis)/len(vis)))
print("hero box heights @390: min %d  max %d" % (
    min(results["routes"][r]["hero"]["h"] for r in ROUTES),
    max(results["routes"][r]["hero"]["h"] for r in ROUTES)))
print("Button2 worst @320: %.1f (fold 568)  @390: %.1f (fold 844)" % (
    max(v for v in results["button2"].values() if v),
    max(results["routes"][r]["b2bottom390"] for r in ROUTES)))
print("overflow>0 routes:", [r for r in ROUTES if results["routes"][r]["overflow"] > 0])
print("console errors:", len(results["console_errors"]))
print("logo 1440:", results["logo"]["1440"], " 390:", results["logo"]["390"])
print("radio 1440:", results["radio"]["1440"])
print("hero img attrs:", set((results["routes"][r]["imgW"], results["routes"][r]["imgH"]) for r in ROUTES))
print("ids present: breadcrumb", sum(1 for r in ROUTES if results["routes"][r]["hasBreadcrumbId"]),
      "hero-image", sum(1 for r in ROUTES if results["routes"][r]["hasHeroImgId"]))
