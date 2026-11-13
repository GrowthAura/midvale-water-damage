#!/usr/bin/env python3
"""INDEPENDENT link-fix render verification (2026-11-13).
Playwright Chromium on the local subpath mirror (port 8324).
Per route x 3 viewports: rendered-DOM paren gate (innerText), white
screen, console errors, failed requests, overflow, hero buttons equal +
Button 2 visible at scroll-0, screenshots to qa/render/.
Plus: computed text-decoration of .body-link / .card-wrap-link, homepage
card geometry (equal heights, image aspect ratios), real-click nav
(card link, body link, logo, footer, breadcrumb, mobile menu).
Reads only the built export (serves it). Writes qa/render/*.png +
qa/verify-linkfix-render.json. Does NOT modify site sources.
"""
import json, os, re, subprocess, sys, time, signal
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa", "render")
os.makedirs(OUT, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
BASE = "http://localhost:8324/midvale-water-damage"
ROUTES = [p["route"] for p in DATA["pages"]]
PAREN_RE = re.compile(r"\(/[^)]+/\)")

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def url(route):
    return BASE + "/" if route == "/" else BASE + route

results = {}

srv = subprocess.Popen([sys.executable, "/tmp/linkfix-serve.py", "8324"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for route in ROUTES:
            r = {"route": route}
            for label, w, h in (("desktop", 1440, 900), ("m390", 390, 844), ("m320", 320, 568)):
                ctx = browser.new_context(viewport={"width": w, "height": h})
                page = ctx.new_page()
                errors, failed = [], []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
                page.on("response", lambda resp: failed.append(f"{resp.status} {resp.url}") if resp.status >= 400 else None)
                try:
                    page.goto(url(route), wait_until="networkidle", timeout=30000)
                    page.wait_for_timeout(400)
                except Exception as e:
                    r[label] = {"goto_error": str(e)}
                    ctx.close()
                    continue
                body_text = page.evaluate("() => document.body.innerText")
                main_text = page.evaluate("() => document.querySelector('main')?.innerText || ''")
                h1 = page.evaluate("""() => {
                    const h = document.querySelector('main h1');
                    if (!h) return null;
                    const b = h.getBoundingClientRect();
                    return {text: h.innerText, visible: b.height > 0 && b.width > 0};
                }""")
                overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                app_err = "Application error" in body_text
                chunk_err = any("ChunkLoadError" in e or "chunk" in e.lower() for e in errors)
                btns = page.evaluate("""() => {
                    const hero = document.querySelector('main section.hero');
                    if (!hero) return null;
                    const links = [...hero.querySelectorAll('a')].filter(a => !a.closest('nav'));
                    return links.map(a => {
                        const b = a.getBoundingClientRect();
                        return {text: a.innerText.trim(), href: a.getAttribute('href'),
                                x: b.x, y: b.y, w: b.width, h: b.height};
                    });
                }""")
                btn1 = next((b for b in (btns or []) if b["text"] == "(385) 337-3560"), None)
                btn2 = next((b for b in (btns or []) if b["text"] == "Request Emergency Help"), None)
                btn_equal = None
                btn2_visible_scroll0 = None
                btn2_bottom = None
                if btn1 and btn2:
                    btn_equal = (abs(btn1["w"] - btn2["w"]) < 1.5 and abs(btn1["h"] - btn2["h"]) < 1.5)
                    btn2_visible_scroll0 = (btn2["y"] + btn2["h"] <= h) and (btn2["y"] >= 0)
                    btn2_bottom = round(btn2["y"] + btn2["h"], 1)
                # link decoration computed styles (sampled on every page)
                deco = page.evaluate("""() => {
                    const out = {};
                    const bl = document.querySelector('a.body-link');
                    if (bl) { const cs = getComputedStyle(bl); out.body_link = {decoration: cs.textDecorationLine, color: cs.color}; }
                    const cw = document.querySelector('a.card-wrap-link');
                    if (cw) { const cs = getComputedStyle(cw); out.card_wrap_link = {decoration: cs.textDecorationLine, color: cs.color}; }
                    return out;
                }""")
                shot = os.path.join(OUT, f"{slug(route)}-{label}.png")
                page.screenshot(path=shot)
                r[label] = {
                    "body_text_len": len(body_text),
                    "paren_in_body_innerText": len(PAREN_RE.findall(body_text)),
                    "paren_in_main_innerText": len(PAREN_RE.findall(main_text)),
                    "paren_samples": PAREN_RE.findall(body_text)[:3],
                    "h1": h1,
                    "overflow_px": overflow,
                    "application_error_text": app_err,
                    "chunk_error": chunk_err,
                    "console_errors": errors,
                    "failed_requests": failed,
                    "hero_buttons": btns,
                    "btn1": btn1, "btn2": btn2,
                    "buttons_equal": btn_equal,
                    "btn2_visible_scroll0": btn2_visible_scroll0,
                    "btn2_bottom_px": btn2_bottom,
                    "viewport_h": h,
                    "link_decoration": deco,
                    "screenshot": shot,
                }
                ctx.close()
            results[route] = r
            d, m3, m2 = r.get("desktop", {}), r.get("m390", {}), r.get("m320", {})
            print(f"{route}: paren body/main={d.get('paren_in_body_innerText')}/{d.get('paren_in_main_innerText')} "
                  f"overflow d/m390/m320={d.get('overflow_px')}/{m3.get('overflow_px')}/{m2.get('overflow_px')} "
                  f"errs={len(d.get('console_errors', []))} failed={len(d.get('failed_requests', []))} "
                  f"btn2vis d/m390/m320={d.get('btn2_visible_scroll0')}/{m3.get('btn2_visible_scroll0')}/{m2.get('btn2_visible_scroll0')} "
                  f"btn2bottom m320={m2.get('btn2_bottom_px')}", flush=True)

        # ---------- homepage card geometry (desktop) ----------
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(url("/"), wait_until="networkidle")
        page.wait_for_timeout(400)
        card_geo = page.evaluate("""() => {
            const cards = [...document.querySelectorAll('article.card')];
            return cards.map((c, i) => {
                const b = c.getBoundingClientRect();
                const a = c.querySelector('a.card-wrap-link');
                const ab = a ? a.getBoundingClientRect() : null;
                const img = c.querySelector('img');
                const ib = img ? img.getBoundingClientRect() : null;
                const cs = a ? getComputedStyle(a) : null;
                return {i, x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
                        href: a ? a.getAttribute('href') : null,
                        link_w: ab ? Math.round(ab.width) : null, link_h: ab ? Math.round(ab.height) : null,
                        img_w: ib ? Math.round(ib.width) : null, img_h: ib ? Math.round(ib.height) : null,
                        img_ratio: ib ? +(ib.width / ib.height).toFixed(3) : null,
                        deco: cs ? cs.textDecorationLine : null, nested_a: c.querySelectorAll('a').length};
            });
        }""")
        # scroll to the card grid so images are loaded, re-measure img boxes
        page.evaluate("document.querySelector('#services').scrollIntoView()")
        page.wait_for_timeout(600)
        card_geo2 = page.evaluate("""() => {
            const cards = [...document.querySelectorAll('article.card')];
            return cards.map((c, i) => {
                const img = c.querySelector('img');
                const ib = img ? img.getBoundingClientRect() : null;
                return {i, img_w: ib ? Math.round(ib.width) : null, img_h: ib ? Math.round(ib.height) : null,
                        img_ratio: ib ? +(ib.width / ib.height).toFixed(3) : null,
                        natural: img ? [img.naturalWidth, img.naturalHeight] : null};
            });
        }""")
        ctx.close()

        # ---------- real-click navigation ----------
        nav = {}
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        nav_errors = []
        page.on("pageerror", lambda e: nav_errors.append(str(e)))
        page.goto(url("/"), wait_until="networkidle")
        page.wait_for_timeout(300)
        def click_state(key, locator_expr):
            try:
                page.locator(locator_expr).first.click()
                page.wait_for_timeout(600)
                nav[key] = {"url": page.url,
                            "h1": page.evaluate("() => document.querySelector('main h1')?.innerText"),
                            "subpath_kept": "/midvale-water-damage/" in page.url}
            except Exception as e:
                nav[key] = {"error": str(e)}
        click_state("card->emergency_click", "article.card a.card-wrap-link[href*='emergency-water-extraction']")
        click_state("logo->home", "header a[href='/midvale-water-damage']")
        # body link on homepage: #18 emergency-contacts link in the First-30 section
        try:
            page.locator("main a.body-link[href*='midvale-water-sewer-emergency-contacts']").first.click()
            page.wait_for_timeout(600)
            nav["bodylink->emergency_contacts"] = {"url": page.url,
                "h1": page.evaluate("() => document.querySelector('main h1')?.innerText"),
                "subpath_kept": "/midvale-water-damage/" in page.url}
        except Exception as e:
            nav["bodylink->emergency_contacts"] = {"error": str(e)}
        # inner body link: emergency page -> hardwood body link
        try:
            page.goto(url("/emergency-water-extraction"), wait_until="networkidle")
            page.wait_for_timeout(300)
            page.locator("main a.body-link[href*='hardwood-floor-cabinet-drying']").first.click()
            page.wait_for_timeout(600)
            nav["inner_bodylink->hardwood"] = {"url": page.url,
                "h1": page.evaluate("() => document.querySelector('main h1')?.innerText"),
                "subpath_kept": "/midvale-water-damage/" in page.url}
        except Exception as e:
            nav["inner_bodylink->hardwood"] = {"error": str(e)}
        click_state("footer->mold", "footer a[href*='mold-remediation']")
        click_state("header->sewage", "header nav a[href*='sewage-backup-cleanup']")
        click_state("breadcrumb->home", "main nav.breadcrumb a")
        nav["desktop_click_errors"] = nav_errors
        ctx.close()

        # mobile menu
        mnav = {}
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto(url("/"), wait_until="networkidle")
        page.wait_for_timeout(300)
        try:
            page.locator("header button[aria-expanded], header button.menu-btn, header button").first.click()
            page.wait_for_timeout(400)
            mnav["menu_open_state"] = page.evaluate("() => { const n = document.querySelector('#main-nav'); return n ? getComputedStyle(n).display + '|' + (n.className||'') + '|aria:' + (document.querySelector('header button')?.getAttribute('aria-expanded')) : 'no-nav'; }")
            mnav["menu_scroll_lock"] = page.evaluate("() => getComputedStyle(document.body).overflow + '|' + document.body.style.position")
            page.locator("#main-nav a[href*='burst-pipe-water-damage']").first.click()
            page.wait_for_timeout(500)
            mnav["menu_click->burst"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText"), "subpath_kept": "/midvale-water-damage/" in page.url}
            mnav["menu_state_after_click"] = page.evaluate("() => { const n = document.querySelector('#main-nav'); return n ? getComputedStyle(n).display + '|' + (n.className||'') : 'no-nav'; }")
        except Exception as e:
            mnav["error"] = str(e)
        ctx.close()
        browser.close()

    json.dump({"routes": results, "card_geometry": card_geo, "card_geometry_scrolled": card_geo2,
               "nav": nav, "mobile_nav": mnav},
              open(os.path.join(ROOT, "qa", "verify-linkfix-render.json"), "w"), indent=1)
    print("---- CARD GEOMETRY (desktop, scroll-0) ----")
    for c in card_geo:
        print(c)
    print("---- CARD GEOMETRY (scrolled to #services) ----")
    for c in card_geo2:
        print(c)
    print("---- NAV ----")
    print(json.dumps(nav, indent=1))
    print("---- MOBILE NAV ----")
    print(json.dumps(mnav, indent=1))
    print("---- SUMMARY ----")
    bad = []
    for route, r in results.items():
        for label in ("desktop", "m390", "m320"):
            d = r.get(label, {})
            if d.get("goto_error"):
                bad.append((route, label, "goto_error " + d["goto_error"]))
            if d.get("paren_in_body_innerText"):
                bad.append((route, label, f"paren in rendered body innerText: {d.get('paren_samples')}"))
            if d.get("application_error_text"):
                bad.append((route, label, "APPLICATION ERROR TEXT"))
            if d.get("chunk_error"):
                bad.append((route, label, "ChunkLoadError"))
            if d.get("body_text_len", 0) < 500:
                bad.append((route, label, f"body text only {d.get('body_text_len')}"))
            if (d.get("overflow_px") or 0) > 0:
                bad.append((route, label, f"overflow {d['overflow_px']}px"))
            if d.get("console_errors"):
                bad.append((route, label, f"console errors: {d['console_errors'][:2]}"))
            if d.get("failed_requests"):
                bad.append((route, label, f"failed requests: {d['failed_requests'][:2]}"))
            if d.get("buttons_equal") is False:
                bad.append((route, label, "hero buttons unequal"))
            if d.get("btn2_visible_scroll0") is False:
                bad.append((route, label, f"Button 2 NOT visible at scroll-0 (bottom {d.get('btn2_bottom_px')} vs viewport {d.get('viewport_h')})"))
            dl = (d.get("link_decoration") or {})
            if dl.get("body_link") and dl["body_link"]["decoration"] != "none":
                bad.append((route, label, f"body-link text-decoration={dl['body_link']['decoration']}"))
            if dl.get("card_wrap_link") and dl["card_wrap_link"]["decoration"] != "none":
                bad.append((route, label, f"card-wrap-link text-decoration={dl['card_wrap_link']['decoration']}"))
    print("render problems:", len(bad))
    for b in bad:
        print(" -", b)
finally:
    srv.send_signal(signal.SIGTERM)
