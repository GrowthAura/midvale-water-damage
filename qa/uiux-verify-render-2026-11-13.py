#!/usr/bin/env python3
"""INDEPENDENT VERIFIER — Midvale UT Stage 1 UI/UX round (2026-11-13).
Fresh render checks on the new export, served on /midvale-water-damage/
(port 8341, already running). Playwright Chromium.
Per route x 3 viewports: console errors, failed requests, overflow, H1
visible + computed size, hero buttons (equal size, Button 2 visible at
scroll-0), images rendered after slow scroll, body font-size spot check.
Homepage @1440: 4-col service card grid. Tables @390: scroll-cue ::after
opacity (1 at scroll 0 when overflowing, 0 at max scroll, 0 when fitting).
Contact form fields + submit text. Real-click nav (card, body link, logo,
footer, mobile menu @390). Screenshots desktop + m390 per route to
qa/uiux-render/ for the review pack.
Writes qa/uiux-verify-render-2026-11-13.json
"""
import json, os, re, time
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa", "uiux-render")
os.makedirs(OUT, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
BASE = "http://127.0.0.1:8341/midvale-water-damage"
ROUTES = [p["route"] for p in DATA["pages"]]
PHONE = "(385) 337-3560"
BTN2 = "Request Emergency Help"

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def url(route):
    return BASE + "/" if route == "/" else BASE + route

results = {"pages": {}, "problems": [], "site": {}}
all_failed_local = []
all_failed_maps = []
all_console = []

with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--disable-gpu", "--no-sandbox"])
    for route in ROUTES:
        r = {"route": route}
        for label, w, h in (("desktop", 1440, 900), ("m390", 390, 844), ("m320", 320, 568)):
            ctx = browser.new_context(viewport={"width": w, "height": h})
            page = ctx.new_page()
            errors, failed = [], []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
            page.on("response", lambda resp: failed.append(f"{resp.status} {resp.url}") if resp.status >= 400 else None)
            d = {}
            try:
                page.goto(url(route), wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(300)
            except Exception as e:
                d["goto_error"] = str(e)
                r[label] = d
                ctx.close()
                continue
            # identity
            h1 = page.evaluate("""() => {
                const el = document.querySelector('main h1');
                if (!el) return null;
                const b = el.getBoundingClientRect();
                const cs = getComputedStyle(el);
                return {text: el.innerText.trim(), visible: b.height > 0 && b.width > 0,
                        fontSize: parseFloat(cs.fontSize)};
            }""")
            d["h1"] = h1
            d["overflow"] = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            # hero buttons at scroll-0 (before any scrolling)
            btns = page.evaluate("""() => {
                const hero = document.querySelector('main section.hero');
                if (!hero) return null;
                return [...hero.querySelectorAll('a')].filter(a => !a.closest('nav')).map(a => {
                    const b = a.getBoundingClientRect();
                    return {text: a.innerText.trim(), x: Math.round(b.x), y: Math.round(b.y),
                            w: Math.round(b.width), h: Math.round(b.height),
                            bottom: Math.round(b.bottom)};
                });
            }""")
            d["hero_buttons"] = btns
            b1 = next((b for b in (btns or []) if b["text"] == PHONE), None)
            b2 = next((b for b in (btns or []) if b["text"] == BTN2), None)
            d["btn_equal"] = bool(b1 and b2 and b1["w"] == b2["w"] and b1["h"] == b2["h"])
            d["btn2_bottom"] = b2["bottom"] if b2 else None
            d["btn2_visible_scroll0"] = bool(b2 and b2["bottom"] <= h and b2["y"] >= 0)
            # body font-size spot check (first 3 p/li in main)
            d["body_font_px"] = page.evaluate("""() => {
                const els = [...document.querySelectorAll('main p, main li')].slice(0, 12);
                return els.map(e => parseFloat(getComputedStyle(e).fontSize));
            }""")
            # slow scroll to trigger lazy images, then check all imgs
            page.evaluate("""async () => {
                const H = document.body.scrollHeight;
                for (let y = 0; y <= H; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
                window.scrollTo(0, 0);
            }""")
            page.wait_for_timeout(400)
            imgs = page.evaluate("""() => [...document.querySelectorAll('main img')].map(im => ({
                src: im.getAttribute('src'), alt: im.getAttribute('alt') || '',
                ok: im.complete && im.naturalWidth > 0, w: im.naturalWidth, h: im.naturalHeight,
                loading: im.getAttribute('loading') || ''
            }))""")
            d["imgs_total"] = len(imgs)
            d["imgs_broken"] = [i for i in imgs if not i["ok"]]
            d["imgs_no_alt"] = [i["src"] for i in imgs if not i["alt"].strip()]
            # table scroll cue @390 only
            if label == "m390":
                d["tables"] = page.evaluate("""() => [...document.querySelectorAll('.table-wrap')].map(w => {
                    const over = w.scrollWidth > w.clientWidth;
                    const op0 = parseFloat(getComputedStyle(w, '::after').opacity);
                    w.scrollLeft = w.scrollWidth; // max scroll
                    const opMax = parseFloat(getComputedStyle(w, '::after').opacity);
                    w.scrollLeft = 0;
                    return {overflowing: over, cue_at_scroll0: op0, cue_at_max: opMax};
                })""")
            # screenshots desktop + m390
            if label in ("desktop", "m390"):
                page.screenshot(path=os.path.join(OUT, f"{slug(route)}-{label}.png"))
            # console/failed classification
            for f in failed:
                if "google.com" in f or "maps.googleapis" in f:
                    all_failed_maps.append({"route": route, "vp": label, "url": f})
                else:
                    all_failed_local.append({"route": route, "vp": label, "url": f})
            for e in errors:
                all_console.append({"route": route, "vp": label, "err": e})
            d["console_errors"] = errors
            d["failed_requests"] = failed
            r[label] = d
            ctx.close()
        results["pages"][route] = r
    # ---- homepage card grid @1440 ----
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(url("/"), wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(300)
    grid = page.evaluate("""() => {
        const g = document.querySelector('#services .card-grid');
        if (!g) return null;
        const cards = [...g.querySelectorAll(':scope > a, :scope > article, :scope > div')];
        const rects = cards.map(c => { const b = c.getBoundingClientRect(); return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; });
        const cols = new Set(rects.map(r => r.x)).size;
        const rows = {};
        rects.forEach(r => { rows[r.y] = (rows[r.y] || 0) + 1; });
        const cs = getComputedStyle(g);
        return {cards: rects.length, cols: cols, rowSizes: Object.values(rows),
                gridTemplate: cs.gridTemplateColumns, cardWidths: [...new Set(rects.map(r => r.w))],
                imgHeights: [...new Set([...g.querySelectorAll('img')].map(i => Math.round(i.getBoundingClientRect().height)))]};
    }""")
    results["site"]["home_card_grid_1440"] = grid
    # ---- contact form ----
    page.goto(url("/contact"), wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(300)
    form = page.evaluate("""() => {
        const f = document.querySelector('form');
        if (!f) return null;
        const fields = [...f.querySelectorAll('input, select, textarea')].map(e => ({
            tag: e.tagName.toLowerCase(), type: e.getAttribute('type') || '',
            name: e.getAttribute('name') || '', label: (e.closest('label')?.innerText || '').trim(),
            required: e.required }));
        const submit = f.querySelector('button[type=submit], input[type=submit]');
        return {fields, submitText: submit ? submit.innerText.trim() : null,
                notice: (document.querySelector('.contact-form')?.innerText || '').slice(0, 400)};
    }""")
    results["site"]["contact_form"] = form
    # ---- real clicks ----
    clicks = {}
    page.goto(url("/"), wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(300)
    # card link click (first service card)
    try:
        with page.expect_navigation(timeout=10000):
            page.click("#services .card-grid a >> nth=0")
        clicks["card_click"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText.trim()")}
    except Exception as e:
        clicks["card_click"] = {"error": str(e)[:200], "url": page.url}
    # body link click (first .body-link on a service page)
    page.goto(url("/emergency-water-extraction"), wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(300)
    try:
        href = page.evaluate("() => document.querySelector('main a.body-link')?.getAttribute('href')")
        with page.expect_navigation(timeout=10000):
            page.click("main a.body-link >> nth=0")
        clicks["body_click"] = {"from_href": href, "url": page.url,
                                "h1": page.evaluate("() => document.querySelector('main h1')?.innerText.trim()")}
    except Exception as e:
        clicks["body_click"] = {"error": str(e)[:200], "url": page.url}
    # logo click -> home
    try:
        with page.expect_navigation(timeout=10000):
            page.click("header a[href*='midvale-water-damage'] >> nth=0")
        clicks["logo_click"] = {"url": page.url}
    except Exception as e:
        clicks["logo_click"] = {"error": str(e)[:200], "url": page.url}
    # footer link click
    page.goto(url("/"), wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(300)
    try:
        with page.expect_navigation(timeout=10000):
            page.click("footer a[href*='about'] >> nth=0")
        clicks["footer_click"] = {"url": page.url,
                                  "h1": page.evaluate("() => document.querySelector('main h1')?.innerText.trim()")}
    except Exception as e:
        clicks["footer_click"] = {"error": str(e)[:200], "url": page.url}
    # mobile menu @390
    ctx2 = browser.new_context(viewport={"width": 390, "height": 844})
    mp = ctx2.new_page()
    mp.goto(url("/"), wait_until="networkidle", timeout=30000)
    mp.wait_for_timeout(300)
    try:
        mp.click("button[aria-label*='menu' i], header button >> nth=0")
        mp.wait_for_timeout(400)
        vis = mp.evaluate("() => { const n = document.querySelector('#main-nav, nav'); return n ? getComputedStyle(n).display + '|' + n.innerText.slice(0,120) : 'no-nav'; }")
        clicks["mobile_menu"] = {"after_click_nav": vis}
        # click a nav link inside the opened menu
        with mp.expect_navigation(timeout=10000):
            mp.click("#main-nav a >> nth=0")
        clicks["mobile_menu_click"] = {"url": mp.url,
                                       "h1": mp.evaluate("() => document.querySelector('main h1')?.innerText.trim()")}
    except Exception as e:
        clicks["mobile_menu"] = {"error": str(e)[:200], "url": mp.url}
    ctx2.close()
    results["site"]["real_clicks"] = clicks
    browser.close()

# ---- adjudication ----
probs = results["problems"]
for route, r in results["pages"].items():
    for label, w, h in (("desktop", 1440, 900), ("m390", 390, 844), ("m320", 320, 568)):
        d = r.get(label, {})
        if "goto_error" in d:
            probs.append({"sev": "P1", "route": route, "vp": label, "what": "goto failed", "detail": d["goto_error"][:200]})
            continue
        if d.get("overflow", 0) != 0:
            probs.append({"sev": "P2", "route": route, "vp": label, "what": "horizontal overflow", "px": d["overflow"]})
        h1 = d.get("h1") or {}
        if not h1.get("visible"):
            probs.append({"sev": "P1", "route": route, "vp": label, "what": "H1 not visible"})
        if label == "m320" and h1.get("fontSize") is not None and h1["fontSize"] < 28:
            probs.append({"sev": "P2", "route": route, "vp": label, "what": "H1 < H2 size @320", "h1_px": h1["fontSize"]})
        if not d.get("btn_equal"):
            probs.append({"sev": "P2", "route": route, "vp": label, "what": "hero buttons not equal size", "buttons": d.get("hero_buttons")})
        if not d.get("btn2_visible_scroll0"):
            probs.append({"sev": "P1", "route": route, "vp": label, "what": "Button 2 NOT visible at scroll-0",
                          "btn2_bottom": d.get("btn2_bottom"), "viewport_h": h})
        if d.get("imgs_broken"):
            probs.append({"sev": "P1", "route": route, "vp": label, "what": "broken images in rendered DOM",
                          "detail": [i["src"] for i in d["imgs_broken"]][:6]})
        if d.get("imgs_no_alt"):
            probs.append({"sev": "P3", "route": route, "vp": label, "what": "imgs missing alt", "detail": d["imgs_no_alt"][:6]})
        if d.get("body_font_px") and min(d["body_font_px"]) < 19:
            probs.append({"sev": "P3", "route": route, "vp": label, "what": "body text < 19px sampled",
                          "px": d["body_font_px"]})
        if label == "m390":
            for ti, t in enumerate(d.get("tables", [])):
                if t["overflowing"] and t["cue_at_scroll0"] != 1:
                    probs.append({"sev": "P2", "route": route, "vp": label, "what": "table scroll cue OFF at scroll-0 on overflowing table", "table": ti})
                if t["overflowing"] and t["cue_at_max"] != 0:
                    probs.append({"sev": "P2", "route": route, "vp": label, "what": "table scroll cue still ON at max scroll", "table": ti})
                if not t["overflowing"] and t["cue_at_scroll0"] != 0:
                    probs.append({"sev": "P3", "route": route, "vp": label, "what": "table scroll cue ON on fitting table", "table": ti})
        if d.get("console_errors"):
            probs.append({"sev": "P2", "route": route, "vp": label, "what": "console errors", "detail": d["console_errors"][:3]})
        if d.get("failed_requests"):
            local_f = [f for f in d["failed_requests"] if "google.com" not in f and "maps.googleapis" not in f]
            if local_f:
                probs.append({"sev": "P2", "route": route, "vp": label, "what": "failed local requests", "detail": local_f[:5]})

grid = results["site"].get("home_card_grid_1440") or {}
if grid.get("cols") != 4 or grid.get("cards") != 16:
    probs.append({"sev": "P2", "route": "/", "what": "service card grid not 4-col x 16", "grid": grid})
form = results["site"].get("contact_form") or {}
if not form:
    probs.append({"sev": "P1", "route": "/contact", "what": "no form found"})
else:
    if len(form.get("fields", [])) != 6:
        probs.append({"sev": "P2", "route": "/contact", "what": "contact form field count != 6", "fields": form["fields"]})
    if form.get("submitText") != "[Send My Request]":
        probs.append({"sev": "P2", "route": "/contact", "what": "submit text != verbatim", "submit": form.get("submitText")})
clicks = results["site"].get("real_clicks", {})
for k, c in clicks.items():
    if isinstance(c, dict) and "error" in c:
        probs.append({"sev": "P2", "route": "*", "what": f"real-click {k} failed", "detail": c["error"][:200]})
    elif isinstance(c, dict) and c.get("url") and "/midvale-water-damage" not in c["url"]:
        probs.append({"sev": "P1", "route": "*", "what": f"real-click {k} lost subpath", "url": c["url"]})

results["site"]["failed_local_requests"] = all_failed_local
results["site"]["failed_maps_requests"] = all_failed_maps
results["site"]["console_errors_all"] = all_console
results["site"]["problems_count"] = len(probs)

# Button 2 worst-case summary
worst320 = max((results["pages"][rt]["m320"].get("btn2_bottom") or 0) for rt in ROUTES)
worst390 = max((results["pages"][rt]["m390"].get("btn2_bottom") or 0) for rt in ROUTES)
results["site"]["btn2_worst_bottom_320"] = worst320
results["site"]["btn2_worst_bottom_390"] = worst390
results["site"]["btn2_worst_route_320"] = max(ROUTES, key=lambda rt: results["pages"][rt]["m320"].get("btn2_bottom") or 0)

json.dump(results, open(os.path.join(ROOT, "qa/uiux-verify-render-2026-11-13.json"), "w"), indent=1)
print("routes:", len(ROUTES))
print("btn2 worst bottom @320:", worst320, "| @390:", worst390, "| worst route @320:", results["site"]["btn2_worst_route_320"])
print("card grid 1440:", grid)
print("contact form fields:", len(form.get("fields", [])) if form else 0, "| submit:", form.get("submitText") if form else None)
print("real clicks:", json.dumps(clicks)[:600])
print("failed local:", len(all_failed_local), "| failed maps (env):", len(all_failed_maps), "| console errors:", len(all_console))
print("PROBLEMS:", len(probs))
for pb in probs:
    print(" -", pb["sev"], pb["route"], pb.get("vp", ""), pb["what"], str(pb.get("detail", pb.get("px", pb.get("btn2_bottom", ""))))[:180])
