#!/usr/bin/env python3
"""Focused body-image renderer test (DESIGN ROUND 2026-11-13).
Runs against the TEMP test manifest in lib/body-images.json (deleted
afterwards). Checks tag contract + layout + overflow + Button 2 on the
pages the manifest targets, and that invalid entries render nothing.
Test images do not exist as files, so their 404s are expected and
filtered here; the check is the TAG + layout, not the asset.
"""
import json, os, subprocess, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
BASE = "http://localhost:8332/midvale-water-damage"
EXPECTED_404 = "/images/body/"

def check(page, route, w, h):
    page.set_viewport_size({"width": w, "height": h})
    failed = []
    page.on("response", lambda r: failed.append(r.url) if r.status >= 400 and EXPECTED_404 not in r.url else None)
    page.goto(BASE + route, wait_until="domcontentloaded")
    page.wait_for_timeout(500)
    d = page.evaluate("""() => {
        const imgs = [...document.querySelectorAll('img.body-img')].map(im => {
            const fig = im.closest('figure');
            const grid = im.closest('.h2-section.with-image');
            const h2 = grid ? grid.querySelector('.h2-section-text h2') : null;
            const fr = fig ? fig.getBoundingClientRect() : null;
            const hr = h2 ? h2.getBoundingClientRect() : null;
            return {src: im.getAttribute('src'), alt: im.getAttribute('alt'),
                w: im.getAttribute('width'), h: im.getAttribute('height'),
                loading: im.getAttribute('loading'), decoding: im.getAttribute('decoding'),
                cls: im.className, figSticky: fig ? fig.classList.contains('sticky') : null,
                figPosition: fig ? getComputedStyle(fig).position : null,
                figTop: fr ? fr.top : null, h2Top: hr ? hr.top : null,
                imgW: im.getBoundingClientRect().width, imgH: im.getBoundingClientRect().height,
                sectionH2: h2 ? h2.innerText.trim().slice(0, 50) : null};
        });
        const hero = document.querySelector('main section.hero');
        const b2 = hero ? [...hero.querySelectorAll('a')].find(a => a.innerText.trim() === 'Request Emergency Help') : null;
        const b2r = b2 ? b2.getBoundingClientRect() : null;
        return {imgs, overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                btn2bottom: b2r ? b2r.bottom : null, vh: window.innerHeight,
                gridSections: document.querySelectorAll('.h2-section.with-image').length,
                failed: []};
    }""")
    d["failed_unexpected"] = failed
    return d

srv = subprocess.Popen([sys.executable, "/tmp/linkfix-serve.py", "8332"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
out = {}
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        for route in ("/emergency-water-extraction", "/locations/cottonwood-heights-ut",
                      "/ceiling-water-damage", "/about", "/burst-pipe-water-damage", "/"):
            out[route + "@1440"] = check(page, route, 1440, 900)
        out["/emergency-water-extraction@390"] = check(page, "/emergency-water-extraction", 390, 844)
        out["/emergency-water-extraction@320"] = check(page, "/emergency-water-extraction", 320, 568)
        out["/locations/cottonwood-heights-ut@390"] = check(page, "/locations/cottonwood-heights-ut", 390, 844)
        out["/locations/cottonwood-heights-ut@320"] = check(page, "/locations/cottonwood-heights-ut", 320, 568)
        page.screenshot(path=os.path.join(ROOT, "qa", "render-design", "bodyimg-emergency-desktop.png"))
        browser.close()
finally:
    srv.terminate()
print(json.dumps(out, indent=1))
