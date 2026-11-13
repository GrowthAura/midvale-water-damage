#!/usr/bin/env python3
"""SEO FIX 1 baseline: measure hero intro font-size, Button 2 bottom,
footer tap targets, header phone, menu button, overflow — on the CURRENT
out/ build (pre-fix). Served on /midvale-water-damage/ via linkfix-serve.py.
Usage: python3 qa/seo-fix1-measure.py <port> <out.json>"""
import json, sys, subprocess, time, os, signal
from playwright.sync_api import sync_playwright

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8325
OUT = sys.argv[2] if len(sys.argv) > 2 else "qa/seo-fix1-baseline.json"
BASE = f"http://127.0.0.1:{PORT}/midvale-water-damage"

ROUTES = ["", "/about", "/contact", "/emergency-water-extraction",
"/basement-flooding-cleanup", "/window-well-flooding", "/burst-pipe-water-damage",
"/sewage-backup-cleanup", "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage",
"/ceiling-water-damage", "/crawl-space-water-damage", "/hardwood-floor-cabinet-drying",
"/condo-apartment-water-damage", "/commercial-water-damage", "/storm-flood-damage",
"/mold-remediation", "/water-leak-detection", "/water-damage-repair",
"/locations/cottonwood-heights-ut", "/locations/south-salt-lake-ut",
"/locations/magna-ut", "/midvale-water-sewer-emergency-contacts",
"/privacy-policy", "/terms-of-use", "/disclaimer",
"/resources/frozen-pipes-midvale", "/resources/winterize-swamp-cooler-utah",
"/resources/upstairs-unit-leak-who-pays-utah", "/resources/can-mold-grow-in-utah",
"/resources/basement-flooding-spring-snowmelt-utah"]

srv = subprocess.Popen(["python3", "qa/linkfix-serve.py", str(PORT)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
results = {}
try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height in [(320, 568), (390, 844)]:
            page = browser.new_page(viewport={"width": width, "height": height})
            for r in ROUTES:
                url = BASE + (r if r else "/")
                page.goto(url, wait_until="networkidle", timeout=30000)
                m = page.evaluate("""() => {
                  const q = s => document.querySelector(s);
                  const intro = q('p.intro');
                  const eyebrow = q('p.eyebrow');
                  const btns = [...document.querySelectorAll('.hero-buttons .btn')];
                  const b2 = btns[1];
                  const r2 = b2 ? b2.getBoundingClientRect() : null;
                  const footLinks = [...document.querySelectorAll('.site-footer a')];
                  const footH = footLinks.map(a => Math.round(a.getBoundingClientRect().height * 10) / 10);
                  const hp = q('.header-phone');
                  const hpR = hp ? hp.getBoundingClientRect() : null;
                  const mb = q('.menu-btn');
                  const mbR = mb && getComputedStyle(mb).display !== 'none' ? mb.getBoundingClientRect() : null;
                  const navLinks = [...document.querySelectorAll('.main-nav a')];
                  const navH = navLinks.map(a => Math.round(a.getBoundingClientRect().height * 10) / 10);
                  return {
                    introPx: intro ? parseFloat(getComputedStyle(intro).fontSize) : null,
                    eyebrowPx: eyebrow ? parseFloat(getComputedStyle(eyebrow).fontSize) : null,
                    btn2Bottom: r2 ? Math.round(r2.bottom * 10) / 10 : null,
                    btn2Top: r2 ? Math.round(r2.top * 10) / 10 : null,
                    footMin: footH.length ? Math.min(...footH) : null,
                    footMax: footH.length ? Math.max(...footH) : null,
                    footCount: footH.length,
                    headerPhoneH: hpR ? Math.round(hpR.height * 10) / 10 : null,
                    headerPhoneVisible: hp ? getComputedStyle(hp).display !== 'none' : null,
                    menuBtn: mbR ? [Math.round(mbR.width), Math.round(mbR.height)] : null,
                    navMin: navH.length ? Math.min(...navH) : null,
                    navCount: navH.length,
                    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                    h1: (q('h1') || {}).textContent || null,
                  };
                }""")
                results[f"{width}:{r or '/'}"] = m
            page.close()
        browser.close()
finally:
    srv.send_signal(signal.SIGTERM)

json.dump(results, open(OUT, "w"), indent=1)
# summary
for width in (320, 390):
    ks = [k for k in results if k.startswith(f"{width}:")]
    worst = max(results[k]["btn2Bottom"] for k in ks)
    worst_route = [k for k in ks if results[k]["btn2Bottom"] == worst][0]
    intro = sorted(set(results[k]["introPx"] for k in ks))
    eyebrow = sorted(set(results[k]["eyebrowPx"] for k in ks))
    footmin = min(results[k]["footMin"] for k in ks)
    hp = sorted(set(results[k]["headerPhoneH"] for k in ks if results[k]["headerPhoneH"] is not None))
    mb = sorted(set(tuple(results[k]["menuBtn"]) for k in ks if results[k]["menuBtn"]))
    navmin = min(results[k]["navMin"] for k in ks if results[k]["navMin"] is not None)
    ov = max(results[k]["overflow"] for k in ks)
    print(f"@{width}: intro={intro} eyebrow={eyebrow} btn2Worst={worst} ({worst_route}) "
          f"footMin={footmin} headerPhone={hp} menuBtn={mb} navMin={navmin} overflowMax={ov}")
print("wrote", OUT)
