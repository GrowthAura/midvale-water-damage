#!/usr/bin/env python3
"""Adjudicate brokenImgs flags from the full-page shoot: for each affected
route/width, load the page, slow-scroll, wait long, and list images still
incomplete + any failed requests. Prints a verdict per route.
"""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8355/midvale-water-damage"
CASES = [
    ("/", "desktop", 1440, 900),
    ("/", "mobile", 390, 844),
    ("/basement-flooding-cleanup", "mobile", 390, 844),
    ("/commercial-water-damage", "desktop", 1440, 900),
    ("/locations/magna-ut", "mobile", 390, 844),
    ("/locations/cottonwood-heights-ut", "desktop", 1440, 900),
]

def probe(pg, url):
    failed = []
    pg.on("requestfailed", lambda r: failed.append(f"REQFAIL {r.url} {r.failure}"))
    pg.on("response", lambda r: failed.append(f"HTTP{r.status} {r.url}") if r.status >= 400 else None)
    pg.goto(url, wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(800)
    pg.evaluate("""async () => {
        const h = document.body.scrollHeight;
        for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 110)); }
        window.scrollTo(0, 0);
    }""")
    pg.wait_for_timeout(600)
    pg.evaluate("""async () => {
        await document.fonts.ready;
        const imgs = [...document.images];
        await Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = r; i.onerror = r; setTimeout(r, 5000); })));
    }""")
    pg.wait_for_timeout(400)
    first = pg.evaluate("""() => [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => ({
        src: (i.getAttribute('src') || '').split('/').slice(-2).join('/'),
        loading: i.getAttribute('loading'), y: Math.round(i.getBoundingClientRect().top + window.scrollY)
    }))""")
    # long second wait, re-check
    pg.wait_for_timeout(5000)
    second = pg.evaluate("""() => [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => ({
        src: (i.getAttribute('src') || '').split('/').slice(-2).join('/'),
        loading: i.getAttribute('loading')
    }))""")
    return first, second, failed

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox"])
    for route, label, vw, vh in CASES:
        ctx = browser.new_context(viewport={"width": vw, "height": vh})
        pg = ctx.new_page()
        try:
            first, second, failed = probe(pg, BASE + ("" if route == "/" else route))
            print(f"== {route} {label}: first-pass incomplete={len(first)} after-5s={len(second)} failed-requests={len(failed)}", flush=True)
            for i in first:
                print(f"   first: {i}", flush=True)
            for i in second:
                print(f"   STILL: {i}", flush=True)
            for f in failed[:10]:
                print(f"   {f}", flush=True)
        except Exception as e:
            print(f"== {route} {label}: ERROR {e}", flush=True)
        finally:
            ctx.close()
    browser.close()
print("ADJUDICATION DONE", flush=True)
