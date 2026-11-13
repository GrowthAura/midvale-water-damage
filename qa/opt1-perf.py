#!/usr/bin/env python3
"""CYCLE 1 OPT — perf + mobile audit (LCP/CLS/overflow/tap-targets/body-19px/Button-2),
Midvale UT. AUDIT ONLY — Playwright headless Chromium, local loopback server on 8325.
Fresh context per page load (cold cache). LAB numbers only — never field data.
Writes qa/opt1-perf.json."""
import json, statistics
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "workspace/midvale-water-damage"
BASE = "http://127.0.0.1:8325/midvale-water-damage"
ROUTES = [
    "/", "/about", "/contact", "/emergency-water-extraction", "/basement-flooding-cleanup",
    "/window-well-flooding", "/burst-pipe-water-damage", "/sewage-backup-cleanup",
    "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage", "/ceiling-water-damage",
    "/crawl-space-water-damage", "/hardwood-floor-cabinet-drying",
    "/condo-apartment-water-damage", "/commercial-water-damage", "/storm-flood-damage",
    "/mold-remediation", "/water-leak-detection", "/water-damage-repair",
    "/locations/cottonwood-heights-ut", "/locations/south-salt-lake-ut", "/locations/magna-ut",
    "/midvale-water-sewer-emergency-contacts", "/privacy-policy", "/terms-of-use", "/disclaimer",
    "/resources/frozen-pipes-midvale", "/resources/winterize-swamp-cooler-utah",
    "/resources/upstairs-unit-leak-who-pays-utah", "/resources/can-mold-grow-in-utah",
    "/resources/basement-flooding-spring-snowmelt-utah",
]
VIEWPORTS = [(320, 568), (390, 844), (1440, 900)]

INIT = """
window.__perf = {lcp: [], fcp: null, cls: 0};
try {
  new PerformanceObserver((list) => {
    for (const e of list.getEntries()) {
      if (e.entryType === 'largest-contentful-paint') {
        const el = e.element;
        window.__perf.lcp.push({startTime: e.startTime, size: e.size,
          tag: el ? el.tagName : null,
          cls: el ? (el.className && el.className.baseVal !== undefined ? el.className.baseVal : String(el.className)) : null,
          id: el ? el.id : null, src: el ? (el.currentSrc || el.src || null) : null});
      }
      if (e.entryType === 'paint' && e.name === 'first-contentful-paint') window.__perf.fcp = e.startTime;
      if (e.entryType === 'layout-shift' && !e.hadRecentInput) window.__perf.cls += e.value;
    }
  }).observe({type: 'largest-contentful-paint', buffered: true});
  new PerformanceObserver((list) => {
    for (const e of list.getEntries()) {
      if (e.entryType === 'paint' && e.name === 'first-contentful-paint') window.__perf.fcp = e.startTime;
    }
  }).observe({type: 'paint', buffered: true});
  new PerformanceObserver((list) => {
    for (const e of list.getEntries()) {
      if (e.entryType === 'layout-shift' && !e.hadRecentInput) window.__perf.cls += e.value;
    }
  }).observe({type: 'layout-shift', buffered: true});
} catch (err) { window.__perf.error = String(err); }
"""

MEASURE = """() => {
  const r = {};
  r.innerWidth = window.innerWidth; r.innerHeight = window.innerHeight;
  r.docScrollWidth = document.documentElement.scrollWidth;
  r.bodyScrollWidth = document.body.scrollWidth;
  r.overflowPx = Math.max(0, document.documentElement.scrollWidth - window.innerWidth);
  r.scrollX = window.scrollX; r.scrollY = window.scrollY;
  // body copy font: .page-body p if present, else main p excluding .eyebrow
  const bodyPs = document.querySelectorAll('.page-body p');
  const probe = bodyPs.length ? [...bodyPs] : [...document.querySelectorAll('main p')].filter(p => !p.classList.contains('eyebrow'));
  r.bodyFontSizes = [...new Set(probe.map(p => parseFloat(getComputedStyle(p).fontSize)))];
  r.bodyPCount = probe.length;
  const intro = document.querySelector('p.intro');
  r.introFontSize = intro ? parseFloat(getComputedStyle(intro).fontSize) : null;
  const eyebrow = document.querySelector('p.eyebrow');
  r.eyebrowFontSize = eyebrow ? parseFloat(getComputedStyle(eyebrow).fontSize) : null;
  // Button 2 = second button in .hero-buttons (.btn-help, 'Request Emergency Help')
  const btns = [...document.querySelectorAll('.hero-buttons a, .hero-buttons button')];
  r.heroButtons = btns.map(b => ({text: b.textContent.trim().slice(0, 60), cls: b.className,
    rect: (() => { const x = b.getBoundingClientRect(); return {top: x.top, bottom: x.bottom, left: x.left, right: x.right, h: x.height, w: x.width}; })()}));
  const b2 = btns[1] || null;
  if (b2) { const x = b2.getBoundingClientRect(); r.button2 = {text: b2.textContent.trim(), bottom: x.bottom, top: x.top, height: x.height, fold: window.innerHeight, visibleAtScroll0: x.bottom <= window.innerHeight}; }
  else r.button2 = null;
  // footer links
  const fl = [...document.querySelectorAll('footer a')].filter(a => { const x = a.getBoundingClientRect(); const cs = getComputedStyle(a); return x.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden'; });
  r.footerLinks = fl.map(a => ({text: a.textContent.trim().slice(0, 50), h: Math.round(a.getBoundingClientRect().height * 10) / 10}));
  r.footerMinVisible = fl.length ? Math.min(...fl.map(a => a.getBoundingClientRect().height)) : null;
  // header nav links (menu closed state first)
  const nav = [...document.querySelectorAll('header nav a, .main-nav a')].filter(a => { const x = a.getBoundingClientRect(); return x.height > 0; });
  r.navLinksClosed = nav.map(a => ({text: a.textContent.trim().slice(0, 40), h: Math.round(a.getBoundingClientRect().height * 10) / 10}));
  // menu button + header phone
  const menuBtn = document.querySelector('button[aria-label*="menu" i], .menu-button, header button');
  r.menuButton = null;
  if (menuBtn) { const x = menuBtn.getBoundingClientRect(); const cs = getComputedStyle(menuBtn); r.menuButton = {visible: cs.display !== 'none' && x.height > 0, w: x.width, h: x.height, ariaLabel: menuBtn.getAttribute('aria-label')}; }
  const hp = document.querySelector('header a[href^="tel:"]');
  r.headerPhone = null;
  if (hp) { const x = hp.getBoundingClientRect(); const cs = getComputedStyle(hp); r.headerPhone = {visible: cs.display !== 'none' && x.height > 0, w: x.width, h: x.height, text: hp.textContent.trim()}; }
  // hero img present?
  const hero = document.querySelector('img.hero-img');
  r.heroImgPresent = !!hero;
  r.perf = window.__perf;
  return r;
}"""

MENU_OPEN_MEASURE = """() => {
  const nav = [...document.querySelectorAll('header nav a, .main-nav a')].filter(a => { const x = a.getBoundingClientRect(); return x.height > 0; });
  return nav.map(a => ({text: a.textContent.trim().slice(0, 40), h: Math.round(a.getBoundingClientRect().height * 10) / 10}));
}"""

pages = []
problems = []
def add(sev, check, page, detail):
    problems.append({"severity": sev, "check": check, "page": page, "detail": detail})

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for rt in ROUTES:
        url = BASE + "/" if rt == "/" else BASE + rt
        rec = {"route": rt, "url": url, "viewports": {}}
        for (w, h) in VIEWPORTS:
            ctx = browser.new_context(viewport={"width": w, "height": h})
            page = ctx.new_page()
            console_errors = []
            failed_reqs = []
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
            page.on("requestfailed", lambda r: failed_reqs.append({"url": r.url, "failure": r.failure}))
            page.on("response", lambda r: failed_reqs.append({"url": r.url, "status": r.status}) if r.status >= 400 else None)
            page.add_init_script(INIT)
            try:
                page.goto(url, wait_until="load", timeout=30000)
            except Exception as e:
                rec["viewports"][f"{w}x{h}"] = {"goto_error": str(e)}
                add("P1", "perf-load", rt, f"viewport {w}x{h}: page.goto failed: {e}")
                ctx.close()
                continue
            page.wait_for_timeout(2500)
            m = page.evaluate(MEASURE)
            # mobile: open the menu and re-measure nav links
            if w in (320, 390):
                try:
                    btn = page.query_selector('button[aria-label*="menu" i], .menu-button, header button')
                    if btn:
                        btn.click()
                        page.wait_for_timeout(400)
                        m["navLinksMenuOpen"] = page.evaluate(MENU_OPEN_MEASURE)
                except Exception as e:
                    m["menuOpenError"] = str(e)
            perf = m.pop("perf")
            lcp_entries = perf.get("lcp", [])
            final_lcp = lcp_entries[-1] if lcp_entries else None
            vp = {
                "innerWidth": m["innerWidth"], "innerHeight": m["innerHeight"],
                "docScrollWidth": m["docScrollWidth"], "bodyScrollWidth": m["bodyScrollWidth"],
                "overflowPx": m["overflowPx"],
                "fcpMs": round(perf["fcp"], 1) if perf.get("fcp") is not None else None,
                "lcpMs": round(final_lcp["startTime"], 1) if final_lcp else None,
                "lcpElement": ({k: final_lcp[k] for k in ("tag", "cls", "id", "src", "size")} if final_lcp else None),
                "lcpEntriesCount": len(lcp_entries),
                "cls": round(perf.get("cls", 0), 4),
                "bodyFontSizes": m["bodyFontSizes"], "bodyPCount": m["bodyPCount"],
                "introFontSize": m["introFontSize"], "eyebrowFontSize": m["eyebrowFontSize"],
                "button2": m["button2"],
                "heroButtonsCount": len(m["heroButtons"]),
                "footerMinVisible": m["footerMinVisible"], "footerCount": len(m["footerLinks"]),
                "footerLinks": m["footerLinks"],
                "navLinksClosed": m["navLinksClosed"],
                "navLinksMenuOpen": m.get("navLinksMenuOpen"),
                "menuButton": m["menuButton"], "headerPhone": m["headerPhone"],
                "heroImgPresent": m["heroImgPresent"],
                "consoleErrors": console_errors,
                "failedRequests": [f for f in failed_reqs if "google.com" not in f["url"]],
                "mapsFailedRequests": [f for f in failed_reqs if "google.com" in f["url"]],
            }
            rec["viewports"][f"{w}x{h}"] = vp
            # per-load flags
            if m["overflowPx"] != 0:
                add("P1", "mobile-overflow", rt, f"viewport {w}x{h}: horizontal overflow {m['overflowPx']}px (scrollWidth {m['docScrollWidth']} vs {w})")
            if m["bodyFontSizes"] != [19.0] and m["bodyFontSizes"] != [19]:
                add("P2", "body-19px", rt, f"viewport {w}x{h}: body font sizes {m['bodyFontSizes']} (expected [19])")
            if m["introFontSize"] != 19:
                add("P2", "intro-19px", rt, f"viewport {w}x{h}: p.intro {m['introFontSize']}px (expected 19)")
            b2 = m["button2"]
            if not b2:
                add("P1", "button2", rt, f"viewport {w}x{h}: no second hero button found")
            elif not b2["visibleAtScroll0"]:
                add("P2", "button2", rt, f"viewport {w}x{h}: Button 2 bottom {b2['bottom']:.1f}px below fold {b2['fold']}px")
            if vp["footerMinVisible"] is not None and vp["footerMinVisible"] < 48:
                add("P2", "tap-target-footer", rt, f"viewport {w}x{h}: footer min visible {vp['footerMinVisible']}px < 48px")
            if console_errors:
                add("P2", "console-errors", rt, f"viewport {w}x{h}: {console_errors}")
            if vp["failedRequests"]:
                add("P2", "failed-requests", rt, f"viewport {w}x{h}: non-maps failed requests: {vp['failedRequests']}")
            if vp["cls"] and vp["cls"] > 0.1:
                add("P2", "cls", rt, f"viewport {w}x{h}: CLS {vp['cls']} > 0.1")
            ctx.close()
        pages.append(rec)
    browser.close()

def med(vals):
    vals = [v for v in vals if v is not None]
    return round(statistics.median(vals), 1) if vals else None

summary = {}
for key in ["320x568", "390x844", "1440x900"]:
    fcp = [p["viewports"][key].get("fcpMs") for p in pages if "fcpMs" in p["viewports"][key]]
    lcp = [p["viewports"][key].get("lcpMs") for p in pages if "lcpMs" in p["viewports"][key]]
    cls = [p["viewports"][key].get("cls") for p in pages if "cls" in p["viewports"][key]]
    ovf = [p["viewports"][key].get("overflowPx") for p in pages if "overflowPx" in p["viewports"][key]]
    summary[key] = {"fcpMedianMs": med(fcp), "fcpMaxMs": max(fcp) if fcp else None,
                    "lcpMedianMs": med(lcp), "lcpMaxMs": max(lcp) if lcp else None,
                    "lcpMinMs": min(lcp) if lcp else None,
                    "clsMedian": med(cls), "clsMax": max(cls) if cls else None,
                    "overflowMaxPx": max(ovf) if ovf else None, "n": len(pages)}
    # LCP element identity tally
    els = {}
    for p in pages:
        e = p["viewports"][key].get("lcpElement")
        k = f"{e['tag']}.{e['cls']}" if e else "none"
        els[k] = els.get(k, 0) + 1
    summary[key]["lcpElementTally"] = els
    # worst LCP pages
    worst = sorted(((p["viewports"][key].get("lcpMs"), p["route"]) for p in pages
                    if p["viewports"][key].get("lcpMs") is not None), reverse=True)[:5]
    summary[key]["lcpWorst5"] = [{"route": r, "lcpMs": v} for v, r in worst]
    # Button 2 worst
    b2s = sorted(((p["viewports"][key].get("button2") or {}).get("bottom"), p["route"]) for p in pages
                 if (p["viewports"][key].get("button2") or {}).get("bottom") is not None)
    summary[key]["button2WorstBottom"] = {"route": b2s[-1][1], "bottomPx": round(b2s[-1][0], 1),
                                          "foldPx": pages[0]["viewports"][key]["innerHeight"]} if b2s else None
    summary[key]["button2VisibleAtScroll0"] = sum(
        1 for p in pages if (p["viewports"][key].get("button2") or {}).get("visibleAtScroll0"))

report = {
    "audit": "CYCLE 1 OPT — perf + mobile audit (lab numbers only)",
    "site": "Midvale UT water damage",
    "date": "2026-11-13",
    "meta": {
        "base": BASE,
        "viewports": [{"w": w, "h": h} for w, h in VIEWPORTS],
        "conditions": "local loopback http://127.0.0.1:8325, unthrottled, cold cache (fresh browser context per page load), headless Chromium via Playwright (python). LAB numbers, NOT field data.",
        "routes": 31,
        "note": "google.com maps embed egress blocked in this sandbox (environmental); maps failures listed separately, never counted as site defects. Button 2 = second button in .hero-buttons ('Request Emergency Help', .btn-help); visible at scroll-0 means its bottom edge is above the viewport fold.",
    },
    "pages": pages,
    "summary": summary,
    "problems": problems,
    "problem_counts": {
        "P1": sum(1 for p in problems if p["severity"] == "P1"),
        "P2": sum(1 for p in problems if p["severity"] == "P2"),
        "P3": sum(1 for p in problems if p["severity"] == "P3"),
        "total": len(problems),
    },
}
(ROOT / "qa/opt1-perf.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
print("PROBLEMS:", report["problem_counts"])
for p in problems:
    print(p["severity"], "|", p["check"], "|", p["page"], "|", p["detail"][:300])
print(json.dumps(summary, indent=1))
