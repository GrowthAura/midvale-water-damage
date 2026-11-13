#!/usr/bin/env python3
"""Adjudication probe for the 3 flagged categories from
qa/uiux-verify-render-2026-11-13.py (2026-11-13 Stage 1 verifier).
1) body text < 19px: identify WHICH elements are 18px / 14px (selector path + text).
2) broken images: slow scroll + network tracking — was each flagged src ever
   requested, with what status, and does it decode after a proper wait?
3) table scroll cue: re-probe with a real wait after max-scroll (container
   queries update asynchronously).
Writes qa/uiux-adjudicate-2026-11-13.json
"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
BASE = "http://127.0.0.1:8341/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]

def url(route):
    return BASE + "/" if route == "/" else BASE + route

out = {"body_text": {}, "images": {}, "cue": {}}

with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--disable-gpu", "--no-sandbox"])

    # ---- (1) body text: first 12 main p/li with identity ----
    for label, w, h in (("desktop", 1440, 900), ("m320", 320, 568)):
        ctx = browser.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        page.goto(url("/"), wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(300)
        els = page.evaluate("""() => [...document.querySelectorAll('main p, main li')].slice(0, 12).map(e => {
            let path = [];
            let n = e;
            while (n && n !== document.body) {
                let s = n.tagName.toLowerCase();
                if (n.className && typeof n.className === 'string') s += '.' + n.className.trim().split(/\\s+/).slice(0,2).join('.');
                path.unshift(s);
                n = n.parentElement;
            }
            return {path: path.slice(-4).join(' > '), px: parseFloat(getComputedStyle(e).fontSize),
                    text: e.innerText.slice(0, 60)};
        })""")
        out["body_text"][label] = els
        # same probe on a service page
        page.goto(url("/water-damage-repair"), wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(300)
        els2 = page.evaluate("""() => [...document.querySelectorAll('main p, main li')].slice(0, 12).map(e => {
            let path = [];
            let n = e;
            while (n && n !== document.body) {
                let s = n.tagName.toLowerCase();
                if (n.className && typeof n.className === 'string') s += '.' + n.className.trim().split(/\\s+/).slice(0,2).join('.');
                path.unshift(s);
                n = n.parentElement;
            }
            return {path: path.slice(-4).join(' > '), px: parseFloat(getComputedStyle(e).fontSize),
                    text: e.innerText.slice(0, 60)};
        })""")
        out["body_text"][label + "_service"] = els2
        ctx.close()

    # ---- (2) images: slow scroll + request tracking on flagged pages ----
    flagged = ["/water-damage-repair", "/locations/magna-ut", "/locations/cottonwood-heights-ut",
               "/basement-flooding-cleanup", "/"]
    for route in flagged:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        reqs = {}
        page.on("request", lambda r: reqs.__setitem__(r.url, reqs.get(r.url, 0) + 1))
        page.on("response", lambda resp: reqs.__setitem__(resp.url + "|status", resp.status))
        page.goto(url(route), wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(300)
        h0 = page.evaluate("() => document.body.scrollHeight")
        page.evaluate("""async () => {
            let prev = -1;
            for (let i = 0; i < 40; i++) {
                const H = document.body.scrollHeight;
                if (H === prev) break;
                prev = H;
                for (let y = window.scrollY; y <= H; y += 400) {
                    window.scrollTo(0, y);
                    await new Promise(r => setTimeout(r, 120));
                }
            }
            window.scrollTo(0, document.body.scrollHeight);
        }""")
        page.wait_for_timeout(2000)
        h1 = page.evaluate("() => document.body.scrollHeight")
        imgs = page.evaluate("""() => [...document.querySelectorAll('main img')].map(im => ({
            src: im.getAttribute('src'), loading: im.getAttribute('loading') || '',
            complete: im.complete, ok: im.complete && im.naturalWidth > 0,
            w: im.naturalWidth, h: im.naturalHeight,
            top: Math.round(im.getBoundingClientRect().top + window.scrollY)
        }))""")
        out["images"][route] = {
            "scrollHeight_before": h0, "scrollHeight_after": h1,
            "imgs": imgs,
            "requested": {u: s for u, s in reqs.items() if "images/" in u},
        }
        ctx.close()

    # ---- (3) table cue with wait ----
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    page = ctx.new_page()
    page.goto(url("/locations/magna-ut"), wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(300)
    cue = page.evaluate("""async () => {
        const res = [];
        for (const w of document.querySelectorAll('.table-wrap')) {
            const over = w.scrollWidth > w.clientWidth;
            const op0 = parseFloat(getComputedStyle(w, '::after').opacity);
            w.scrollLeft = w.scrollWidth;
            await new Promise(r => setTimeout(r, 500));
            await new Promise(r => requestAnimationFrame(r));
            const opMax = parseFloat(getComputedStyle(w, '::after').opacity);
            w.scrollLeft = 0;
            await new Promise(r => setTimeout(r, 300));
            const opBack = parseFloat(getComputedStyle(w, '::after').opacity);
            res.push({overflowing: over, cue_at_scroll0: op0, cue_at_max_waited: opMax, cue_back_at_0: opBack});
        }
        return res;
    }""")
    out["cue"]["/locations/magna-ut"] = cue
    ctx.close()
    browser.close()

json.dump(out, open(os.path.join(ROOT, "qa/uiux-adjudicate-2026-11-13.json"), "w"), indent=1)
print("== BODY TEXT (home desktop) ==")
for e in out["body_text"]["desktop"]:
    print(f"  {e['px']}px  {e['path']}  | {e['text'][:50]}")
print("== BODY TEXT (home m320) ==")
for e in out["body_text"]["m320"]:
    print(f"  {e['px']}px  {e['path']}  | {e['text'][:50]}")
print("== BODY TEXT (service desktop) ==")
for e in out["body_text"]["desktop_service"]:
    print(f"  {e['px']}px  {e['path']}  | {e['text'][:50]}")
print("== IMAGES ==")
for route, d in out["images"].items():
    bad = [i for i in d["imgs"] if not i["ok"]]
    print(f"  {route}: scrollHeight {d['scrollHeight_before']} -> {d['scrollHeight_after']}, imgs {len(d['imgs'])}, broken-after-proper-scroll: {len(bad)}")
    for i in bad:
        print(f"    STILL BROKEN: {i['src']} loading={i['loading']} complete={i['complete']} top={i['top']}")
    for i in d["imgs"]:
        if not i["ok"]:
            pass
print("== CUE (magna @390) ==")
print(" ", json.dumps(out["cue"]["/locations/magna-ut"]))
