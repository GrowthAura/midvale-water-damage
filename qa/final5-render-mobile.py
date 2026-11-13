#!/usr/bin/env python3
"""W3 — Midvale UT final friendly check, Stage 5: mobile render checks.
Renders all 31 sitemap routes at 390x844 and 320x568 in real Chromium
(Playwright), verifies by viewed render + DOM measurements.
Read-only on site source; writes only qa/final5-* files and screenshots
under qa/render-final5/.
"""
import json, os, re, sys, time, xml.etree.ElementTree as ET
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.expanduser("~/workspace/midvale-water-damage")
BASE_URL = "http://127.0.0.1:8350/midvale-water-damage"
QA_DIR = os.path.join(BASE_DIR, "qa")
SHOT_390 = os.path.join(QA_DIR, "render-final5", "mobile390")
SHOT_320 = os.path.join(QA_DIR, "render-final5", "mobile320")
os.makedirs(SHOT_390, exist_ok=True)
os.makedirs(SHOT_320, exist_ok=True)

FULL_PAGE_SLUGS = {"home", "emergency-water-extraction", "mold-remediation"}
MENU_TEST_SLUGS = ["home", "emergency-water-extraction", "mold-remediation"]
PROGRESS_PATH = os.path.join(QA_DIR, "final5-render-mobile.progress.json")

def launch_browser(p):
    # Full Chromium build (channel="chromium"), NOT the headless-shell build:
    # headless_shell-1243 crashed with SIGILL/CFI (signal 4) after route 1.
    return p.chromium.launch(channel="chromium", args=["--disable-dev-shm-usage"])
MENU_TEST_SLUGS = ["home", "emergency-water-extraction", "mold-remediation"]

def slug_for(path: str) -> str:
    p = path.strip("/")
    if not p:
        return "home"
    return p.replace("/", "-")

def routes():
    t = ET.parse(os.path.join(BASE_DIR, "out", "sitemap.xml"))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    out = []
    for e in t.getroot().findall(".//s:loc", ns):
        u = urlparse(e.text)
        out.append(u.path.replace("/midvale-water-damage", "") or "/")
    return out

MEASURE_JS = r"""
() => {
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const q = (s) => document.querySelector(s);
  const qa = (s) => Array.from(document.querySelectorAll(s));
  const rect = (el) => { const r = el.getBoundingClientRect(); return {top: r.top, bottom: r.bottom, left: r.left, right: r.right, width: r.width, height: r.height}; };
  const visible = (el) => { if (!el) return false; const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 && r.height > 0; };

  // H1
  const h1s = qa('h1');
  const h1 = h1s[0] || null;

  // Hero buttons
  const b1 = q('.hero-buttons a.btn-call');
  const b2 = q('.hero-buttons a.btn-help');
  const headerPhone = q('.header-phone');
  const menuBtn = q('.menu-btn');

  // Images
  const imgs = qa('img');
  const imgBroken = imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => (i.getAttribute('src') || '').slice(0, 120));

  // Body copy font size: first 5 <p> inside <main>
  const mainPs = qa('main p').slice(0, 5).map(p => getComputedStyle(p).fontSize);
  const bodyFs = getComputedStyle(document.body).fontSize;

  // Tap targets: footer links, header phone, menu button
  const footLinks = qa('footer a').map(a => { const r = a.getBoundingClientRect(); return {text: (a.textContent || '').trim().slice(0, 40), h: Math.round(r.height), w: Math.round(r.width)}; });
  const smallFoot = footLinks.filter(x => x.h < 48);

  // Overflow / clipped elements
  const docSW = document.documentElement.scrollWidth;
  const bodySW = document.body.scrollWidth;
  const overflowing = [];
  qa('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0) return;
    if (r.right > vw + 1 || r.left < -1) {
      if (el.closest('.table-wrap')) return; // intentional horizontal scroll inside table wrap
      const cs = getComputedStyle(el);
      if (cs.position === 'fixed') return;
      overflowing.push(el.tagName + '.' + (el.className && typeof el.className === 'string' ? el.className.split(' ')[0] : '') + ' right=' + Math.round(r.right));
    }
  });

  // Tables
  const tables = qa('.table-wrap').map(w => {
    const cue = getComputedStyle(w, '::after');
    return {
      wrapperClientW: w.clientWidth,
      wrapperScrollW: w.scrollWidth,
      overflows: w.scrollWidth > w.clientWidth + 1,
      cueOpacity: cue.opacity,
      cueVisible: cue.opacity !== '0' && cue.display !== 'none',
      tableW: w.querySelector('table') ? Math.round(w.querySelector('table').getBoundingClientRect().width) : null,
    };
  });

  // Styled render check: body background / hero image rendered
  const heroImg = q('.hero-img');
  const styled = {
    bodyBg: getComputedStyle(document.body).backgroundColor,
    heroImgNaturalW: heroImg ? heroImg.naturalWidth : null,
    h1FontSize: h1 ? getComputedStyle(h1).fontSize : null,
  };

  return {
    vw, vh, scrollY: window.scrollY,
    h1Count: h1s.length,
    h1Visible: h1 ? visible(h1) : false,
    h1Text: h1 ? h1.textContent.trim().slice(0, 80) : null,
    h1Rect: h1 ? rect(h1) : null,
    b1: b1 ? {text: b1.textContent.trim(), visible: visible(b1), rect: rect(b1), href: b1.getAttribute('href')} : null,
    b2: b2 ? {text: b2.textContent.trim(), visible: visible(b2), rect: rect(b2), href: b2.getAttribute('href')} : null,
    headerPhone: headerPhone ? {text: headerPhone.textContent.trim(), visible: visible(headerPhone), rect: rect(headerPhone)} : null,
    menuBtn: menuBtn ? {visible: visible(menuBtn), rect: rect(menuBtn), ariaExpanded: menuBtn.getAttribute('aria-expanded')} : null,
    imgCount: imgs.length,
    imgBroken,
    mainPFontSizes: mainPs,
    bodyFontSize: bodyFs,
    footLinkCount: footLinks.length,
    footLinkMinH: footLinks.length ? Math.min(...footLinks.map(x => x.h)) : null,
    smallFootTargets: smallFoot.slice(0, 10),
    docScrollWidth: docSW,
    bodyScrollWidth: bodySW,
    overflowPx: docSW - vw,
    overflowingEls: overflowing.slice(0, 10),
    tables,
    styled,
  };
}
"""

SWIPE_JS = r"""
() => {
  const out = [];
  document.querySelectorAll('.table-wrap').forEach(w => {
    if (w.scrollWidth > w.clientWidth + 1) {
      const before = w.scrollLeft;
      w.scrollLeft = 60;
      const moved = w.scrollLeft > before;
      w.scrollLeft = 0;
      out.push({moved, afterReset: w.scrollLeft});
    }
  });
  return out;
}
"""

def menu_test(page, slug, url):
    """Menu open/close/scroll-lock test at 390px. Returns dict."""
    res = {"slug": slug, "url": url, "steps": {}, "pass": True}
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, 600)")
        page.wait_for_timeout(400)
        y0 = page.evaluate("window.scrollY")
        res["steps"]["scrollBefore"] = y0
        btn = page.locator(".menu-btn")
        btn.click()
        page.wait_for_timeout(500)
        nav = page.locator("#main-nav")
        res["steps"]["ariaExpandedAfterOpen"] = btn.get_attribute("aria-expanded")
        res["steps"]["navOpenClass"] = page.evaluate("document.getElementById('main-nav').className")
        nav_box = nav.bounding_box()
        res["steps"]["navBox"] = nav_box
        links = page.evaluate("""() => {
          const nav = document.getElementById('main-nav');
          return Array.from(nav.querySelectorAll('a')).map(a => { const r = a.getBoundingClientRect(); return {t: a.textContent.trim(), vis: r.width > 0 && r.height > 0 && r.top >= 0 && r.bottom <= window.innerHeight}; });
        }""")
        res["steps"]["navLinks"] = links
        res["steps"]["linksVisibleCount"] = sum(1 for l in links if l["vis"])
        res["steps"]["linksTotal"] = len(links)
        # scroll lock: body position fixed + top offset
        lock = page.evaluate("""() => {
          const b = document.body;
          const cs = getComputedStyle(b);
          return {position: cs.position, top: cs.top, overflow: cs.overflow};
        }""")
        res["steps"]["bodyLockStyle"] = lock
        # try to scroll while open
        page.evaluate(f"window.scrollTo(0, {y0 + 800})")
        page.wait_for_timeout(300)
        y_while_open = page.evaluate("window.scrollY")
        res["steps"]["scrollYWhileOpenAfterAttempt"] = y_while_open
        res["steps"]["scrollLocked"] = (y_while_open == y0)
        # close via menu button
        btn.click()
        page.wait_for_timeout(500)
        res["steps"]["ariaExpandedAfterClose"] = btn.get_attribute("aria-expanded")
        res["steps"]["navOpenClassAfterClose"] = page.evaluate("document.getElementById('main-nav').className")
        y_after = page.evaluate("window.scrollY")
        res["steps"]["scrollYAfterClose"] = y_after
        res["steps"]["scrollRestored"] = (y_after == y0)
        res["pass"] = (
            res["steps"]["ariaExpandedAfterOpen"] == "true"
            and "open" in res["steps"]["navOpenClass"]
            and res["steps"]["linksVisibleCount"] == res["steps"]["linksTotal"]
            and res["steps"]["linksTotal"] > 0
            and res["steps"]["scrollLocked"]
            and res["steps"]["ariaExpandedAfterClose"] == "false"
            and "open" not in res["steps"]["navOpenClassAfterClose"]
            and res["steps"]["scrollRestored"]
        )
    except Exception as e:
        res["pass"] = False
        res["error"] = str(e)
    return res

def check_route(browser, path, slug, url, widths):
    entry = {"slug": slug, "path": path, "url": url, "checks": {}}
    for (w, h, shotdir) in widths:
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
        page = ctx.new_page()
        console_errors, failed_reqs, google_fails = [], [], []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errors.append(f"pageerror: {e}"))
        def on_resp(resp):
            if resp.status >= 400:
                rec = {"url": resp.url, "status": resp.status}
                if "google.com" in resp.url or "gstatic.com" in resp.url or "maps.googleapis" in resp.url:
                    google_fails.append(rec)
                else:
                    failed_reqs.append(rec)
        page.on("response", on_resp)
        page.on("requestfailed", lambda r: (google_fails if ("google.com" in r.url or "gstatic.com" in r.url) else failed_reqs).append({"url": r.url, "failure": r.failure or "failed"}))
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            try:
                page.wait_for_selector("h1", timeout=10000)
            except Exception:
                pass
            page.wait_for_timeout(500)
            m = page.evaluate(MEASURE_JS)
            swipe = page.evaluate(SWIPE_JS)
            for i, s in enumerate(swipe):
                if i < len(m["tables"]):
                    m["tables"][i]["swipeMoved"] = s["moved"]
            shot = os.path.join(shotdir, f"{slug}.png")
            page.screenshot(path=shot)
            if slug in FULL_PAGE_SLUGS:
                page.screenshot(path=os.path.join(shotdir, f"{slug}-full.png"), full_page=True)
            entry["checks"][str(w)] = {
                "http_ok": True,
                "screenshot": f"qa/render-final5/mobile{w}/{slug}.png",
                "console_errors": console_errors,
                "failed_requests": failed_reqs,
                "google_env_fails": google_fails,
                **m,
            }
        except Exception as e:
            entry["checks"][str(w)] = {"http_ok": False, "error": str(e)}
            raise
        finally:
            try:
                ctx.close()
            except Exception:
                pass
    return entry

def main():
    all_routes = routes()
    print(f"routes: {len(all_routes)}")
    results = {"generated": time.strftime("%Y-%m-%d %H:%M %Z"), "base_url": BASE_URL,
               "widths": [390, 320], "routes": [], "menu_tests": [], "totals": {}}
    # resume from progress file if a previous run crashed
    done_slugs = set()
    if os.path.exists(PROGRESS_PATH):
        try:
            prev = json.load(open(PROGRESS_PATH))
            results["routes"] = prev.get("routes", [])
            done_slugs = {r["slug"] for r in results["routes"]}
            print(f"resumed: {len(done_slugs)} routes already done")
        except Exception as e:
            print(f"progress file unreadable, starting fresh: {e}")
    widths = [(390, 844, SHOT_390), (320, 568, SHOT_320)]
    with sync_playwright() as p:
        browser = launch_browser(p)
        for path in all_routes:
            slug = slug_for(path)
            if slug in done_slugs:
                continue
            url = BASE_URL + ("" if path == "/" else path)
            for attempt in range(3):
                try:
                    entry = check_route(browser, path, slug, url, widths)
                    break
                except Exception as e:
                    print(f"  !! {slug} attempt {attempt+1} failed: {str(e)[:200]}")
                    try:
                        browser.close()
                    except Exception:
                        pass
                    if attempt == 2:
                        entry = {"slug": slug, "path": path, "url": url,
                                 "checks": {"390": {"http_ok": False, "error": f"browser crash after 3 attempts: {e}"},
                                            "320": {"http_ok": False, "error": f"browser crash after 3 attempts: {e}"}}}
                    else:
                        time.sleep(2)
                        browser = launch_browser(p)
                        continue
            results["routes"].append(entry)
            done_slugs.add(slug)
            with open(PROGRESS_PATH, "w") as f:
                json.dump(results, f, indent=2)
            c390 = entry["checks"].get("390", {})
            c320 = entry["checks"].get("320", {})
            print(f"done {slug}: 390 b2bottom={(c390.get('b2') or {}).get('rect', {}).get('bottom')} 320 b2bottom={(c320.get('b2') or {}).get('rect', {}).get('bottom')} overflow390={c390.get('overflowPx')} overflow320={c320.get('overflowPx')}")
        # menu tests at 390 on homepage + 2 service pages
        for slug in MENU_TEST_SLUGS:
            path = "/" if slug == "home" else f"/{slug}"
            url = BASE_URL + ("" if path == "/" else path)
            for attempt in range(3):
                try:
                    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1)
                    page = ctx.new_page()
                    res = menu_test(page, slug, url)
                    ctx.close()
                    break
                except Exception as e:
                    print(f"  !! menu {slug} attempt {attempt+1} failed: {str(e)[:200]}")
                    try:
                        browser.close()
                    except Exception:
                        pass
                    if attempt == 2:
                        res = {"slug": slug, "url": url, "steps": {}, "pass": False, "error": str(e)}
                    else:
                        time.sleep(2)
                        browser = launch_browser(p)
                        continue
            results["menu_tests"].append(res)
            print(f"menu {slug}: pass={res['pass']} {res['steps']}")
            with open(PROGRESS_PATH, "w") as f:
                json.dump(results, f, indent=2)
        browser.close()

    # totals
    t = {"routes": len(results["routes"]), "h1_fail": 0, "b2_not_visible_scroll0": 0,
         "b2_bottom_over_fold_390": 0, "b2_bottom_over_fold_320": 0,
         "overflow_390": 0, "overflow_320": 0, "console_error_routes": 0,
         "failed_req_routes": 0, "img_broken_total": 0, "img_total": 0,
         "tap_target_lt48_390": 0, "tap_target_lt48_320": 0,
         "table_routes": 0, "table_overflowing": 0, "table_cue_missing": 0,
         "table_not_swipeable": 0, "body_font_not19": 0, "menu_tests_pass": 0}
    for r in results["routes"]:
        for w, fold in (("390", 844), ("320", 568)):
            c = r["checks"].get(w, {})
            if not c.get("http_ok"):
                t["h1_fail"] += 1
                continue
            if c.get("h1Count") != 1 or not c.get("h1Visible"):
                t["h1_fail"] += 1
            b2 = c.get("b2") or {}
            if not b2.get("visible"):
                t["b2_not_visible_scroll0"] += 1
            elif b2.get("rect", {}).get("bottom", 9999) > fold:
                t[f"b2_bottom_over_fold_{w}"] += 1
            if (c.get("overflowPx") or 0) > 0:
                t[f"overflow_{w}"] += 1
            if c.get("console_errors"):
                t["console_error_routes"] += 1
            if c.get("failed_requests"):
                t["failed_req_routes"] += 1
            t["img_broken_total"] += len(c.get("imgBroken") or [])
            t["img_total"] += c.get("imgCount") or 0
            small = (c.get("smallFootTargets") or [])
            hp = c.get("headerPhone") or {}
            mb = c.get("menuBtn") or {}
            n_small = len(small)
            if hp.get("rect", {}).get("height", 999) < 48 and hp.get("visible"):
                n_small += 1
            if mb.get("rect", {}).get("height", 999) < 48 and mb.get("visible"):
                n_small += 1
            t[f"tap_target_lt48_{w}"] += n_small
            if c.get("tables"):
                t["table_routes"] += 1
                for tb in c["tables"]:
                    if tb.get("overflows"):
                        t["table_overflowing"] += 1
                        if not tb.get("cueVisible"):
                            t["table_cue_missing"] += 1
                        if tb.get("swipeMoved") is False:
                            t["table_not_swipeable"] += 1
            fs = c.get("mainPFontSizes") or []
            if fs and not all(f == "19px" for f in fs):
                t["body_font_not19"] += 1
    t["menu_tests_pass"] = sum(1 for m in results["menu_tests"] if m.get("pass"))
    t["menu_tests_total"] = len(results["menu_tests"])
    results["totals"] = t
    out_path = os.path.join(QA_DIR, "final5-render-mobile.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(t, indent=2))
    print("wrote", out_path)

if __name__ == "__main__":
    main()
