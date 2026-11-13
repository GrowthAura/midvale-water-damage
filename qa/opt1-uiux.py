#!/usr/bin/env python3
"""CYCLE 1 (Batch 2) UI/UX AUDITOR — Midvale UT, A-to-Z, audit-only.
Fresh render checks on the existing out/ export, served on
/midvale-water-damage/ port 8351. Playwright Chromium.
Per route x 3 viewports (1440/390/320): console errors, failed requests,
overflow, H1 visible+size, hero buttons (equal, Button 2 at scroll-0),
ALL body font sizes in main, images after slow scroll, tap targets
(nav/actionable, inline body links counted separately), WCAG AA contrast
worst-case, per-section presence/heights, sticky tel bar, tables @390,
contact form, mobile menu + scroll lock, real clicks.
Full-page screenshots desktop + m390 -> qa/opt1-uiux/.
Writes qa/opt1-uiux.json
"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa", "opt1-uiux")
os.makedirs(OUT, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
BASE = "http://127.0.0.1:8351/midvale-water-damage"
ROUTES = [p["route"] for p in DATA["pages"]]
PHONE = "(385) 337-3560"
BTN2 = "Request Emergency Help"
SUBMIT = "[Send My Request]"

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def url(route):
    return BASE + "/" if route == "/" else BASE + route

results = {"pages": {}, "problems": [], "site": {}, "observations": []}
_PARTIAL = os.path.join(ROOT, "qa", "opt1-uiux-partial.json")
if os.path.exists(_PARTIAL):
    try:
        _p = json.load(open(_PARTIAL))
        results["pages"] = _p.get("pages", {})
        print("resumed from partial:", len(results["pages"]), "routes")
    except Exception as e:
        print("partial load failed:", e)
all_failed_local, all_failed_maps, all_console = [], [], []

JS_IDENTITY = """() => {
  const h1 = document.querySelector('main h1');
  const b = h1 ? h1.getBoundingClientRect() : null;
  const cs = h1 ? getComputedStyle(h1) : null;
  const body = getComputedStyle(document.body);
  return {
    h1: h1 ? {text: h1.innerText.trim(), visible: b.height > 0 && b.width > 0,
              fontSize: parseFloat(cs.fontSize), top: Math.round(b.top)} : null,
    bodyFont: body.fontFamily.slice(0, 60), bodyBg: body.backgroundColor,
    stylesheets: document.styleSheets.length,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    title: document.title
  };
}"""

JS_BUTTONS = """() => {
  const hero = document.querySelector('main section.hero, main .hero, main section:first-of-type');
  if (!hero) return null;
  return [...hero.querySelectorAll('a')].filter(a => !a.closest('nav')).map(a => {
    const b = a.getBoundingClientRect();
    return {text: a.innerText.trim(), x: Math.round(b.x), y: Math.round(b.y),
            w: Math.round(b.width), h: Math.round(b.height), bottom: Math.round(b.bottom)};
  });
}"""

JS_FONTS = """() => {
  const bad = [];
  const els = document.querySelectorAll('main p, main li, main td, main dd, main figcaption');
  els.forEach(e => {
    const fs = parseFloat(getComputedStyle(e).fontSize);
    if (fs < 19) bad.push({tag: e.tagName, cls: (e.className||'').toString().slice(0,40),
      px: fs, text: (e.innerText||'').trim().slice(0,60)});
  });
  return {total: els.length, bad: bad.slice(0, 12), badCount: bad.length};
}"""

JS_IMGS = """() => [...document.querySelectorAll('main img')].map(im => ({
  src: im.getAttribute('src'), alt: im.getAttribute('alt') || '',
  ok: im.complete && im.naturalWidth > 0, w: im.naturalWidth, h: im.naturalHeight,
  dispW: Math.round(im.getBoundingClientRect().width), dispH: Math.round(im.getBoundingClientRect().height)
}))"""

JS_TAPS = """() => {
  const bad = [], inlineSmall = [];
  const els = [...document.querySelectorAll('header a, header button, nav a, nav button, footer a, footer button, main button, main .card-grid a, main a.btn, main a[class*="btn"], form input, form select, form textarea, form button, [class*="tel-bar"] a, [class*="sticky"] a, summary')];
  els.forEach(e => {
    const b = e.getBoundingClientRect();
    const cs = getComputedStyle(e);
    if (b.width === 0 || b.height === 0 || cs.visibility === 'hidden' || cs.display === 'none') return;
    if (b.height < 48 || b.width < 48) bad.push({tag: e.tagName, text: (e.innerText||e.getAttribute('aria-label')||e.getAttribute('type')||'').trim().slice(0,50), w: Math.round(b.width), h: Math.round(b.height), cls: (e.className||'').toString().slice(0,40)});
  });
  const inl = [...document.querySelectorAll('main p a, main li a')];
  inl.forEach(e => {
    const b = e.getBoundingClientRect();
    if (b.height > 0 && b.height < 24) inlineSmall.push({text: e.innerText.trim().slice(0,40), h: Math.round(b.height)});
  });
  return {bad: bad.slice(0, 15), badCount: bad.length, inlineSmallCount: inl.length, inlineSmall: inlineSmall.slice(0,5)};
}"""

JS_CONTRAST = """() => {
  function lum(r, g, b) {
    const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  }
  function parse(c) { const m = c.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)(?:,\\s*([\\d.]+))?\\)/); return m ? [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]] : null; }
  function bgOf(el) {
    let n = el;
    while (n && n !== document.documentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return {image: true};
      const p = parse(cs.backgroundColor);
      if (p && p[3] > 0) return {color: p.slice(0, 3)};
      n = n.parentElement;
    }
    return {color: [255, 255, 255]};
  }
  const rows = [];
  document.querySelectorAll('main *, header *, footer *').forEach(el => {
    if (el.children.length) return;
    const t = (el.textContent || '').trim();
    if (!t) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    const b = el.getBoundingClientRect();
    if (b.width === 0 || b.height === 0) return;
    const fg = parse(cs.color);
    if (!fg) return;
    const bg = bgOf(el);
    if (bg.image) { rows.push({text: t.slice(0, 50), overImage: true, px: parseFloat(cs.fontSize)}); return; }
    const L1 = lum(...fg.slice(0, 3)), L2 = lum(...bg.color);
    const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const fs = parseFloat(cs.fontSize), fw = parseInt(cs.fontWeight) || 400;
    const large = fs >= 24 || (fs >= 18.66 && fw >= 700);
    const need = large ? 3 : 4.5;
    rows.push({text: t.slice(0, 60), ratio: Math.round(ratio * 100) / 100, px: fs, fw, large,
               pass: ratio >= need, cls: (el.className || '').toString().slice(0, 30),
               tag: el.tagName});
  });
  const fails = rows.filter(r => !r.pass && !r.overImage).sort((a, b) => a.ratio - b.ratio);
  const overImg = rows.filter(r => r.overImage);
  const worst = [...rows].filter(r => !r.overImage).sort((a, b) => a.ratio - b.ratio).slice(0, 5);
  return {checked: rows.length, fails: fails.slice(0, 15), failCount: fails.length,
          overImageCount: overImg.length, overImage: overImg.slice(0, 8), worst};
}"""

JS_SECTIONS = """() => {
  const secs = [...document.querySelectorAll('main > section, main > div')].map(s => {
    const b = s.getBoundingClientRect();
    return {id: s.id || '', cls: (s.className || '').toString().slice(0, 50),
            h: Math.round(b.height), top: Math.round(b.top + window.scrollY),
            heading: (s.querySelector('h1,h2,h3')?.innerText || '').trim().slice(0, 60)};
  }).filter(s => s.h > 0 || s.id || s.heading);
  const faq = document.querySelectorAll('main details, main [class*="faq"] details, main .faq-item').length;
  const trust = document.querySelector('[class*="trust"]');
  const cta = document.querySelector('[class*="cta"], [class*="final"]');
  return {sections: secs, faqItems: faq,
          trustBar: trust ? {h: Math.round(trust.getBoundingClientRect().height), text: trust.innerText.trim().slice(0, 120)} : null,
          finalCta: cta ? {h: Math.round(cta.getBoundingClientRect().height), text: cta.innerText.trim().slice(0, 120)} : null};
}"""

JS_TELBAR = """() => {
  const els = [...document.querySelectorAll('a[href^="tel:"], [class*="tel"], [class*="sticky"]')];
  const fixed = els.filter(e => getComputedStyle(e).position === 'fixed' || getComputedStyle(e.closest('div') || e).position === 'fixed');
  return els.map(e => { const b = e.getBoundingClientRect(); return {text: (e.innerText||'').trim().slice(0,40), fixed: getComputedStyle(e).position === 'fixed' || (e.closest('div') && getComputedStyle(e.closest('div')).position === 'fixed'), y: Math.round(b.y), h: Math.round(b.height), visible: b.height > 0}; }).slice(0, 8);
}"""

def new_browser(pw):
    return pw.chromium.launch(args=["--disable-dev-shm-usage", "--disable-gpu", "--no-sandbox"])

with sync_playwright() as pw:
    browser = new_browser(pw)
    for route in ROUTES:
        for label, w, h in (("desktop", 1440, 900), ("m390", 390, 844), ("m320", 320, 568)):
            if label in results["pages"].get(route, {}) and "goto_error" not in results["pages"][route][label]:
                continue
            try:
                ctx = browser.new_context(viewport={"width": w, "height": h})
            except Exception:
                browser = new_browser(pw)
                ctx = browser.new_context(viewport={"width": w, "height": h})
            r = results["pages"].setdefault(route, {"route": route})
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
                try: ctx.close()
                except Exception: pass
                json.dump(results, open(os.path.join(ROOT, "qa", "opt1-uiux-partial.json"), "w"), indent=1)
                continue
            d["identity"] = page.evaluate(JS_IDENTITY)
            d["overflow"] = d["identity"]["overflow"]
            btns = page.evaluate(JS_BUTTONS)
            d["hero_buttons"] = btns
            b1 = next((b for b in (btns or []) if b["text"] == PHONE), None)
            b2 = next((b for b in (btns or []) if b["text"] == BTN2), None)
            d["btn_equal"] = bool(b1 and b2 and b1["w"] == b2["w"] and b1["h"] == b2["h"])
            d["btn2_bottom"] = b2["bottom"] if b2 else None
            d["btn2_visible_scroll0"] = bool(b2 and b2["bottom"] <= h and b2["y"] >= 0)
            d["btn1"] = b1
            # slow scroll to trigger lazy images
            page.evaluate("""async () => {
                const H = document.body.scrollHeight;
                for (let y = 0; y <= H; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); }
                window.scrollTo(0, 0);
            }""")
            page.wait_for_timeout(400)
            imgs = page.evaluate(JS_IMGS)
            d["imgs_total"] = len(imgs)
            d["imgs_broken"] = [i for i in imgs if not i["ok"]]
            d["imgs_no_alt"] = [i["src"] for i in imgs if not i["alt"].strip()]
            d["imgs_zero_display"] = [i["src"] for i in imgs if i["ok"] and (i["dispW"] == 0 or i["dispH"] == 0)]
            d["fonts"] = page.evaluate(JS_FONTS)
            d["taps"] = page.evaluate(JS_TAPS)
            d["contrast"] = page.evaluate(JS_CONTRAST)
            d["sections"] = page.evaluate(JS_SECTIONS)
            if label == "m390":
                d["tables"] = page.evaluate("""() => [...document.querySelectorAll('.table-wrap')].map(w => {
                    const over = w.scrollWidth > w.clientWidth;
                    const op0 = parseFloat(getComputedStyle(w, '::after').opacity);
                    w.scrollLeft = w.scrollWidth;
                    const opMax = parseFloat(getComputedStyle(w, '::after').opacity);
                    w.scrollLeft = 0;
                    return {overflowing: over, cue_at_scroll0: op0, cue_at_max: opMax};
                })""")
                # sticky tel bar after scroll
                page.evaluate("window.scrollTo(0, 1200)")
                page.wait_for_timeout(200)
                d["tel_bar_scrolled"] = page.evaluate(JS_TELBAR)
                page.evaluate("window.scrollTo(0, 0)")
            # full-page screenshots desktop + m390 (skipped in measurement-only mode)
            if label in ("desktop", "m390") and not os.environ.get("OPT1_NO_SHOTS"):
                try:
                    page.screenshot(path=os.path.join(OUT, f"{slug(route)}-{label}-full.png"), full_page=True, animations="disabled")
                except Exception as e:
                    d["screenshot_error"] = str(e)[:200]
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
            try: ctx.close()
            except Exception:
                try: browser.close()
                except Exception: pass
                browser = new_browser(pw)
            json.dump(results, open(os.path.join(ROOT, "qa", "opt1-uiux-partial.json"), "w"), indent=1)

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
        return {cards: rects.length, cols, rowSizes: Object.values(rows),
                gridTemplate: cs.gridTemplateColumns, cardWidths: [...new Set(rects.map(r => r.w))],
                imgHeights: [...new Set([...g.querySelectorAll('img')].map(i => Math.round(i.getBoundingClientRect().height)))],
                cardHeights: [...new Set(rects.map(r => r.h))].sort((a,b)=>a-b)};
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
        return {fields, submitText: submit ? submit.innerText.trim() : null};
    }""")
    results["site"]["contact_form"] = form
    # ---- real clicks ----
    clicks = {}
    page.goto(url("/"), wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(300)
    try:
        with page.expect_navigation(timeout=10000):
            page.click("#services .card-grid a >> nth=0")
        clicks["card_click"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText.trim()")}
    except Exception as e:
        clicks["card_click"] = {"error": str(e)[:200], "url": page.url}
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
    try:
        with page.expect_navigation(timeout=10000):
            page.click("header a[href*='midvale-water-damage'] >> nth=0")
        clicks["logo_click"] = {"url": page.url}
    except Exception as e:
        clicks["logo_click"] = {"error": str(e)[:200], "url": page.url}
    page.goto(url("/"), wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(300)
    try:
        with page.expect_navigation(timeout=10000):
            page.click("footer a[href*='about'] >> nth=0")
        clicks["footer_click"] = {"url": page.url,
                                  "h1": page.evaluate("() => document.querySelector('main h1')?.innerText.trim()")}
    except Exception as e:
        clicks["footer_click"] = {"error": str(e)[:200], "url": page.url}
    # mobile menu @390 + scroll lock
    ctx2 = browser.new_context(viewport={"width": 390, "height": 844})
    mp = ctx2.new_page()
    mp.goto(url("/"), wait_until="networkidle", timeout=30000)
    mp.wait_for_timeout(300)
    try:
        mp.click("button[aria-label*='menu' i], header button >> nth=0")
        mp.wait_for_timeout(400)
        vis = mp.evaluate("""() => {
            const n = document.querySelector('#main-nav, nav');
            const bodyLocked = getComputedStyle(document.body).overflow === 'hidden' || document.documentElement.style.overflow === 'hidden' || document.body.classList.contains('menu-open') || document.body.classList.contains('nav-open');
            const before = window.scrollY;
            window.scrollTo(0, 500);
            const after = window.scrollY;
            window.scrollTo(0, 0);
            return {navDisplay: n ? getComputedStyle(n).display : 'no-nav',
                    navText: n ? n.innerText.slice(0, 150) : '',
                    bodyOverflow: getComputedStyle(document.body).overflow,
                    bodyClass: document.body.className,
                    scrollLocked: before === after};
        }""")
        clicks["mobile_menu"] = vis
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
        h1 = (d.get("identity") or {}).get("h1") or {}
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
        if d.get("imgs_zero_display"):
            probs.append({"sev": "P2", "route": route, "vp": label, "what": "loaded imgs rendering 0px",
                          "detail": d["imgs_zero_display"][:6]})
        fonts = d.get("fonts") or {}
        if fonts.get("badCount"):
            probs.append({"sev": "P2", "route": route, "vp": label, "what": "body text < 19px",
                          "count": fonts["badCount"], "examples": fonts.get("bad", [])[:4]})
        taps = d.get("taps") or {}
        if taps.get("badCount"):
            probs.append({"sev": "P2", "route": route, "vp": label, "what": "tap targets < 48px (nav/actionable)",
                          "count": taps["badCount"], "examples": taps.get("bad", [])[:6]})
        con = d.get("contrast") or {}
        if con.get("failCount"):
            probs.append({"sev": "P2", "route": route, "vp": label, "what": "WCAG AA contrast failures",
                          "count": con["failCount"], "worst": con.get("fails", [])[:5]})
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
        local_f = [f for f in d.get("failed_requests", []) if "google.com" not in f and "maps.googleapis" not in f]
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
    if form.get("submitText") != SUBMIT:
        probs.append({"sev": "P2", "route": "/contact", "what": "submit text != verbatim", "submit": form.get("submitText")})
clicks = results["site"].get("real_clicks", {})
for k, c in clicks.items():
    if isinstance(c, dict) and "error" in c:
        probs.append({"sev": "P2", "route": "*", "what": f"real-click {k} failed", "detail": c["error"][:200]})
    elif isinstance(c, dict) and c.get("url") and "/midvale-water-damage" not in c["url"]:
        probs.append({"sev": "P1", "route": "*", "what": f"real-click {k} lost subpath", "url": c["url"]})
mm = clicks.get("mobile_menu", {})
if isinstance(mm, dict) and "error" not in mm:
    if mm.get("navDisplay") == "none":
        probs.append({"sev": "P1", "route": "/", "what": "mobile menu does not open (nav display none after hamburger click)"})
    if not mm.get("scrollLocked"):
        results["observations"].append({"route": "/", "what": "mobile menu open but page still scrolls (no scroll lock)", "detail": mm})

results["site"]["failed_local_requests"] = all_failed_local
results["site"]["failed_maps_requests"] = all_failed_maps
results["site"]["console_errors_all"] = all_console
results["site"]["problems_count"] = len(probs)

worst320 = max((results["pages"][rt]["m320"].get("btn2_bottom") or 0) for rt in ROUTES)
worst390 = max((results["pages"][rt]["m390"].get("btn2_bottom") or 0) for rt in ROUTES)
results["site"]["btn2_worst_bottom_320"] = worst320
results["site"]["btn2_worst_bottom_390"] = worst390
results["site"]["btn2_worst_route_320"] = max(ROUTES, key=lambda rt: results["pages"][rt]["m320"].get("btn2_bottom") or 0)
results["site"]["btn2_worst_route_390"] = max(ROUTES, key=lambda rt: results["pages"][rt]["m390"].get("btn2_bottom") or 0)

json.dump(results, open(os.path.join(ROOT, "qa", "opt1-uiux.json"), "w"), indent=1)
print("routes:", len(ROUTES))
print("btn2 worst bottom @320:", worst320, "| @390:", worst390, "| worst route @320:", results["site"]["btn2_worst_route_320"])
print("card grid 1440:", grid)
print("contact form fields:", len(form.get("fields", [])) if form else 0, "| submit:", form.get("submitText") if form else None)
print("real clicks:", json.dumps(clicks)[:800])
print("failed local:", len(all_failed_local), "| failed maps (env):", len(all_failed_maps), "| console errors:", len(all_console))
print("PROBLEMS:", len(probs))
for pb in probs:
    print(" -", pb["sev"], pb["route"], pb.get("vp", ""), pb["what"], str(pb.get("detail", pb.get("count", pb.get("px", pb.get("btn2_bottom", "")))))[:200])
