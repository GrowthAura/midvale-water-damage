#!/usr/bin/env python3
"""Real-browser verification of the Midvale rebuild on the local subpath mirror.
Playwright Chromium. For every route: desktop 1440 + mobile 390 + mobile 320
render checks (white screen, console errors, failed requests, overflow,
hero buttons equal + Button 2 visible at scroll-0), screenshots for the review pack.
Then real-click navigation tests (home->inner->home, inner->inner, mobile menu).
Reads only (serves the built export). Writes qa/render/*.png + qa/verify-render.json.
"""
import json, os, re
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa", "render")
os.makedirs(OUT, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
BASE = "http://localhost:8324/midvale-water-damage"
ROUTES = [p["route"] for p in DATA["pages"]]

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def url(route):
    return BASE + "/" if route == "/" else BASE + route

results = {}

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    # ---------- per-route render checks ----------
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
            body_text = page.evaluate("() => document.body.innerText.length")
            h1 = page.evaluate("""() => {
                const h = document.querySelector('main h1');
                if (!h) return null;
                const b = h.getBoundingClientRect();
                return {text: h.innerText, visible: b.height > 0 && b.width > 0};
            }""")
            overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            app_err = page.evaluate("() => document.body.innerText.includes('Application error')")
            chunk_err = any("ChunkLoadError" in e or "chunk" in e.lower() for e in errors)
            # hero buttons
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
            if btn1 and btn2:
                btn_equal = (abs(btn1["w"] - btn2["w"]) < 1.5 and abs(btn1["h"] - btn2["h"]) < 1.5)
                btn2_visible_scroll0 = (btn2["y"] + btn2["h"] <= h) and (btn2["y"] >= 0)
            shot = os.path.join(OUT, f"{slug(route)}-{label}.png")
            page.screenshot(path=shot)
            r[label] = {
                "body_text_len": body_text,
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
                "screenshot": shot,
            }
            ctx.close()
        results[route] = r
        d = r.get("desktop", {})
        m = r.get("m390", {})
        print(f"{route}: desktop body={d.get('body_text_len')} overflow={d.get('overflow_px')} errs={len(d.get('console_errors', []))} failed={len(d.get('failed_requests', []))} btnEq={d.get('buttons_equal')} btn2vis={d.get('btn2_visible_scroll0')} | m390 overflow={m.get('overflow_px')} btnEq={m.get('buttons_equal')} btn2vis={m.get('btn2_visible_scroll0')}")

    # ---------- real-click navigation ----------
    nav = {}
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    nav_errors = []
    page.on("pageerror", lambda e: nav_errors.append(str(e)))
    page.goto(url("/"), wait_until="networkidle")
    page.wait_for_timeout(300)
    # click first service card link (real click)
    try:
        link = page.locator("main section#services a[href*='emergency-water-extraction']").first
        link.click()
        page.wait_for_timeout(500)
        nav["home->emergency_click"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText"), "subpath_kept": "/midvale-water-damage/" in page.url}
    except Exception as e:
        nav["home->emergency_click"] = {"error": str(e)}
    # click logo -> home
    try:
        page.locator("header a[href='/midvale-water-damage']").first.click()
        page.wait_for_timeout(500)
        nav["logo->home"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")}
    except Exception as e:
        nav["logo->home"] = {"error": str(e)}
    # footer link -> another service
    try:
        page.locator("footer a[href*='mold-remediation']").first.click()
        page.wait_for_timeout(500)
        nav["footer->mold"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText"), "subpath_kept": "/midvale-water-damage/" in page.url}
    except Exception as e:
        nav["footer->mold"] = {"error": str(e)}
    # inner -> inner via header nav
    try:
        page.locator("header nav a[href*='sewage-backup-cleanup']").first.click()
        page.wait_for_timeout(500)
        nav["header->sewage"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText"), "subpath_kept": "/midvale-water-damage/" in page.url}
    except Exception as e:
        nav["header->sewage"] = {"error": str(e)}
    # breadcrumb link on inner page -> home
    try:
        page.locator("main nav.breadcrumb a").first.click()
        page.wait_for_timeout(500)
        nav["breadcrumb->home"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")}
    except Exception as e:
        nav["breadcrumb->home"] = {"error": str(e)}
    nav["desktop_click_errors"] = nav_errors
    ctx.close()

    # mobile menu: open, click, verify nav + menu closes
    mnav = {}
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    page = ctx.new_page()
    page.goto(url("/"), wait_until="networkidle")
    page.wait_for_timeout(300)
    try:
        btn = page.locator("header button[aria-expanded], header button.menu-toggle, header button").first
        btn.click()
        page.wait_for_timeout(400)
        menu_open = page.evaluate("() => { const n = document.querySelector('#main-nav'); return n ? getComputedStyle(n).display + '|' + (n.className||'') + '|aria:' + (document.querySelector('header button')?.getAttribute('aria-expanded')) : 'no-nav'; }")
        mnav["menu_open_state"] = menu_open
        # click a nav link inside the open menu
        page.locator("#main-nav a[href*='burst-pipe-water-damage']").first.click()
        page.wait_for_timeout(500)
        mnav["menu_click->burst"] = {"url": page.url, "h1": page.evaluate("() => document.querySelector('main h1')?.innerText"), "subpath_kept": "/midvale-water-damage/" in page.url}
        mnav["menu_state_after_click"] = page.evaluate("() => { const n = document.querySelector('#main-nav'); return n ? getComputedStyle(n).display + '|' + (n.className||'') : 'no-nav'; }")
    except Exception as e:
        mnav["error"] = str(e)
    # sticky bar: scroll down, check it appears (JS hydration proof)
    try:
        page.goto(url("/emergency-water-extraction"), wait_until="networkidle")
        page.wait_for_timeout(300)
        page.evaluate("window.scrollTo(0, 1200)")
        page.wait_for_timeout(400)
        mnav["sticky_bar_after_scroll"] = page.evaluate("() => { const b = document.querySelector('.sticky-bar'); if (!b) return 'no-bar'; const cs = getComputedStyle(b); return cs.position + '|' + cs.display + '|' + (b.className||''); }")
    except Exception as e:
        mnav["sticky_error"] = str(e)
    ctx.close()
    browser.close()

json.dump({"routes": results, "nav": nav, "mobile_nav": mnav}, open(os.path.join(ROOT, "qa", "verify-render.json"), "w"), indent=1)
print("---- NAV ----")
print(json.dumps(nav, indent=1)[:1500])
print("---- MOBILE NAV ----")
print(json.dumps(mnav, indent=1)[:1200])
print("---- SUMMARY ----")
bad = []
for route, r in results.items():
    for label in ("desktop", "m390", "m320"):
        d = r.get(label, {})
        if d.get("goto_error"):
            bad.append((route, label, "goto_error " + d["goto_error"]))
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
            bad.append((route, label, f"hero buttons unequal: {d.get('btn1')} vs {d.get('btn2')}"))
        if d.get("btn2_visible_scroll0") is False:
            bad.append((route, label, f"Button 2 NOT visible at scroll-0: {d.get('btn2')}"))
print("render problems:", len(bad))
for b in bad:
    print(" -", b)
