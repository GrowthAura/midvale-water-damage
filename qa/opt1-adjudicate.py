#!/usr/bin/env python3
"""CYCLE 1 adjudication — re-probe every raw flag with a corrected method.
1. Images: slow scroll (200ms/step) + settle waits + per-image load wait.
2. Table cue: real scroll + wait before reading ::after opacity.
3. Fonts: exclude .eyebrow (kicker) and .breadcrumbs (nav) from body-text rule.
4. Taps: radio LABEL boxes (the real tap target), brand box, footer links, tel bar.
Writes qa/opt1-adjudicate.json
"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
BASE = "http://127.0.0.1:8351/midvale-water-damage"
ROUTES = [p["route"] for p in DATA["pages"]]
RAW = json.load(open(os.path.join(ROOT, "qa", "opt1-uiux.json")))

def url(route):
    return BASE + "/" if route == "/" else BASE + route

out = {"images": {}, "tables": {}, "fonts": {}, "taps": {}, "tel_bar": {}}

with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--disable-dev-shm-usage", "--disable-gpu", "--no-sandbox"])
    # ---- 1. images: every route flagged broken at any viewport, m390 (worst) + desktop ----
    flagged = [rt for rt in ROUTES if any(RAW["pages"][rt][vp].get("imgs_broken") for vp in ("desktop", "m390", "m320"))]
    print("routes to re-probe for images:", len(flagged))
    for route in flagged:
        for label, w, h in (("m390", 390, 844), ("desktop", 1440, 900)):
            ctx = b.new_context(viewport={"width": w, "height": h})
            p = ctx.new_page()
            errs = []
            p.on("pageerror", lambda e: errs.append(str(e)))
            p.goto(url(route), wait_until="networkidle", timeout=30000)
            p.wait_for_timeout(300)
            p.evaluate("""async () => {
                const H = document.body.scrollHeight;
                for (let y = 0; y <= H; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 200)); }
                window.scrollTo(0, 0);
            }""")
            p.wait_for_timeout(1500)
            imgs = p.evaluate("""() => [...document.querySelectorAll('main img')].map(im => ({
                src: im.getAttribute('src'), ok: im.complete && im.naturalWidth > 0,
                loading: im.getAttribute('loading') || ''}))""")
            still = [i["src"] for i in imgs if not i["ok"]]
            # per-image rescue: scroll each failing img into view and wait for load
            rescued = []
            for src in still:
                try:
                    el = p.query_selector(f'main img[src="{src}"]')
                    if el:
                        el.scroll_into_view()
                        p.wait_for_timeout(800)
                        ok = p.evaluate("(s) => { const im = document.querySelector(`main img[src=\"${s}\"]`); return im && im.complete && im.naturalWidth > 0; }", src)
                        if ok:
                            rescued.append(src)
                except Exception as e:
                    pass
            final_bad = [s for s in still if s not in rescued]
            out["images"].setdefault(route, {})[label] = {
                "total": len(imgs), "initial_bad": still, "rescued": rescued,
                "final_bad": final_bad, "pageerrors": errs}
            ctx.close()
    # ---- 2. tables: re-probe cue with real scroll + wait ----
    for route in ROUTES:
        n = len(RAW["pages"][route]["m390"].get("tables", []))
        if not n:
            continue
        ctx = b.new_context(viewport={"width": 390, "height": 844})
        p = ctx.new_page()
        p.goto(url(route), wait_until="networkidle", timeout=30000)
        p.wait_for_timeout(300)
        tabs = p.evaluate("""async () => {
            const res = [];
            for (const w of document.querySelectorAll('.table-wrap')) {
                const over = w.scrollWidth > w.clientWidth;
                const op0 = parseFloat(getComputedStyle(w, '::after').opacity);
                w.scrollTo({left: w.scrollWidth, behavior: 'instant'});
                w.dispatchEvent(new Event('scroll'));
                await new Promise(r => setTimeout(r, 400));
                const opMax = parseFloat(getComputedStyle(w, '::after').opacity);
                w.scrollTo({left: 0, behavior: 'instant'});
                await new Promise(r => setTimeout(r, 200));
                const opBack = parseFloat(getComputedStyle(w, '::after').opacity);
                res.push({overflowing: over, cue_at_scroll0: op0, cue_at_max: opMax, cue_back_at_0: opBack});
            }
            return res;
        }""")
        out["tables"][route] = tabs
        ctx.close()
    # ---- 3. fonts corrected + 4. taps detail, desktop + m390 ----
    for route in ROUTES:
        for label, w, h in (("desktop", 1440, 900), ("m390", 390, 844)):
            ctx = b.new_context(viewport={"width": w, "height": h})
            p = ctx.new_page()
            p.goto(url(route), wait_until="networkidle", timeout=30000)
            p.wait_for_timeout(300)
            fonts = p.evaluate("""() => {
                const bad = [];
                const els = [...document.querySelectorAll('main p:not(.eyebrow), main li')].filter(e => !e.closest('.breadcrumbs'));
                els.forEach(e => { const fs = parseFloat(getComputedStyle(e).fontSize);
                    if (fs < 19) bad.push({tag: e.tagName, px: fs, text: (e.innerText||'').trim().slice(0,60)}); });
                return {total: els.length, badCount: bad.length, bad: bad.slice(0,6)};
            }""")
            taps = p.evaluate("""() => {
                const out = {};
                const brand = document.querySelector('header a.brand');
                if (brand) { const r = brand.getBoundingClientRect(); out.brand = {w: Math.round(r.width), h: Math.round(r.height)}; }
                out.radios = [...document.querySelectorAll('form input[type=radio]')].map(inp => {
                    const lab = inp.closest('label');
                    const lr = lab ? lab.getBoundingClientRect() : null;
                    return {labelText: lab ? lab.innerText.trim() : '', labelW: lr ? Math.round(lr.width) : null,
                            labelH: lr ? Math.round(lr.height) : null, inputH: Math.round(inp.getBoundingClientRect().height)};
                });
                out.footerLinks = [...document.querySelectorAll('footer a')].filter(a => { const r = a.getBoundingClientRect(); return r.width > 0 && r.height > 0; }).map(a => ({text: a.innerText.trim().slice(0,30), w: Math.round(a.getBoundingClientRect().width), h: Math.round(a.getBoundingClientRect().height)})).filter(x => x.h < 48).slice(0,8);
                out.footerSmallCount = [...document.querySelectorAll('footer a')].filter(a => { const r = a.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.height < 48; }).length;
                out.telBar = [...document.querySelectorAll('a[href^="tel:"]')].map(a => ({text: a.innerText.trim().slice(0,30), fixed: getComputedStyle(a).position === 'fixed', h: Math.round(a.getBoundingClientRect().height)})).slice(0,4);
                return out;
            }""")
            out["fonts"].setdefault(route, {})[label] = fonts
            out["taps"].setdefault(route, {})[label] = taps
            ctx.close()
    # ---- 5. tel bar sticky check @390 after scroll (homepage) ----
    ctx = b.new_context(viewport={"width": 390, "height": 844})
    p = ctx.new_page()
    p.goto(url("/"), wait_until="networkidle", timeout=30000)
    p.wait_for_timeout(300)
    p.evaluate("window.scrollTo(0, 1500)")
    p.wait_for_timeout(300)
    out["tel_bar"] = p.evaluate("""() => {
        const cands = [...document.querySelectorAll('a[href^="tel:"]')].map(a => {
            let n = a, fixed = false;
            while (n) { if (getComputedStyle(n).position === 'fixed') { fixed = true; break; } n = n.parentElement; }
            const r = a.getBoundingClientRect();
            return {text: a.innerText.trim().slice(0,40), fixed, y: Math.round(r.y), h: Math.round(r.height), visible: r.height > 0 && r.y >= 0 && r.y < innerHeight};
        });
        return cands;
    }""")
    ctx.close()
    b.close()

json.dump(out, open(os.path.join(ROOT, "qa", "opt1-adjudicate.json"), "w"), indent=1)

# summary
img_bad = {r: v for r, v in out["images"].items() if any(vp["final_bad"] for vp in v.values())}
print("IMAGE re-probe: routes with FINAL bad images:", len(img_bad))
for r, v in img_bad.items():
    print("  ", r, v)
tab_bad = {}
for r, tabs in out["tables"].items():
    for i, t in enumerate(tabs):
        if t["overflowing"] and t["cue_at_max"] != 0:
            tab_bad.setdefault(r, []).append((i, t))
print("TABLE cue still ON at max after real scroll+wait:", len(tab_bad))
for r, v in list(tab_bad.items())[:10]:
    print("  ", r, v)
font_bad = {r: v for r, v in out["fonts"].items() if any(vp["badCount"] for vp in v.values())}
print("FONTS corrected-selector bad routes:", len(font_bad), font_bad)
print("TEL BAR @390 scrolled:", json.dumps(out["tel_bar"]))
print("BRAND sizes:", sorted({(r, v["desktop"]["brand"]["h"]) for r, v in out["taps"].items() if v["desktop"].get("brand")}))
print("RADIO label heights sample:", out["taps"].get("/contact", {}).get("desktop", {}).get("radios"))
print("FOOTER small links (desktop, /):", out["taps"].get("/", {}).get("desktop", {}).get("footerSmallCount"))
