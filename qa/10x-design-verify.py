#!/usr/bin/env python3
"""FRESH independent 10x design verification for Midvale (2026-11-13).
TEST ONLY — serves the built out/ locally, drives headless Chromium.
Writes qa/10x-design-render.json + screenshots under qa/10x-design/.
Does NOT modify any site source file. Does NOT push/deploy/touch GitHub.
"""
import json, os, re, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUTDIR = os.path.join(ROOT, "qa", "10x-design")
os.makedirs(OUTDIR, exist_ok=True)
BASE = "http://127.0.0.1:8325/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]
EXPECTED_H1 = {p["route"]: p["h1"] for p in DATA["pages"]}

JS_COLLECT = r"""
() => {
  const out = {};
  const cs = (el, prop) => getComputedStyle(el).getPropertyValue(prop);
  // H1
  const h1s = [...document.querySelectorAll('main h1')];
  out.h1_count = h1s.length;
  out.h1_text = h1s.length ? h1s[0].innerText.trim() : null;
  // overflow
  out.scrollW = document.documentElement.scrollWidth;
  out.clientW = document.documentElement.clientWidth;
  out.innerW = window.innerWidth;
  out.overflow_px = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  // hero Button 2 (.hero .btn-help)
  const b2 = document.querySelector('.hero .btn-help');
  if (b2) {
    const r = b2.getBoundingClientRect();
    out.btn2 = {top: r.top, bottom: r.bottom, left: r.left, right: r.right,
                width: r.width, height: r.height, vh: window.innerHeight,
                visible_scroll0: r.top >= 0 && r.bottom <= window.innerHeight,
                text: b2.innerText.trim()};
    const cx = r.left + r.width/2, cy = r.top + r.height/2;
    const hit = document.elementFromPoint(cx, cy);
    out.btn2.covered_by = hit ? (hit.closest('a,button') ? hit.closest('a,button').className : hit.tagName + '.' + hit.className) : null;
    out.btn2.hit_is_self = hit ? (b2.contains(hit) || hit === b2) : false;
  } else { out.btn2 = null; }
  // sticky bar state at scroll 0
  const bar = document.querySelector('.sticky-bar');
  if (bar) {
    const r = bar.getBoundingClientRect();
    out.sticky_bar = {cls: bar.className, top: r.top, bottom: r.bottom, height: r.height, visible: r.bottom > 0 && r.top < window.innerHeight};
  } else out.sticky_bar = null;
  // header / footer dashes
  const hdr = document.querySelector('header');
  const ftr = document.querySelector('footer');
  out.header_text = hdr ? hdr.innerText : '';
  out.footer_text = ftr ? ftr.innerText : '';
  out.header_em_dash = (out.header_text.match(/\u2014/g) || []).length;
  out.header_en_dash = (out.header_text.match(/\u2013/g) || []).length;
  out.footer_em_dash = (out.footer_text.match(/\u2014/g) || []).length;
  out.footer_en_dash = (out.footer_text.match(/\u2013/g) || []).length;
  // em/en dash anywhere in main visible text
  const main = document.querySelector('main');
  const mainText = main ? main.innerText : '';
  out.main_em_dash = (mainText.match(/\u2014/g) || []).length;
  out.main_en_dash = (mainText.match(/\u2013/g) || []).length;
  // underline violations on internal links
  out.underline_violations = [];
  document.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href') || '';
    const internal = href.startsWith('/midvale-water-damage/') || href === '/midvale-water-damage' || href.startsWith('#') === false && !href.startsWith('http') && !href.startsWith('tel:') && !href.startsWith('mailto:') && href.startsWith('/');
    if (!internal) return;
    const td = cs(a, 'text-decoration-line');
    const bb = cs(a, 'border-bottom-width');
    const isBtn = a.className && a.className.includes('btn');
    if (td && td.includes('underline')) {
      out.underline_violations.push({href, text: (a.innerText||'').trim().slice(0,60), cls: a.className, btn: isBtn, decoration: td});
    }
  });
  // body font sizes
  out.small_text = [];
  const sizes = [];
  document.querySelectorAll('main p, main li, main td, main th').forEach(el => {
    const fs = parseFloat(cs(el, 'font-size'));
    sizes.push(fs);
    if (fs < 18) out.small_text.push({tag: el.tagName, fs, text: (el.innerText||'').trim().slice(0,70)});
  });
  out.body_font_min = sizes.length ? Math.min(...sizes) : null;
  out.body_font_median = sizes.length ? sizes.slice().sort((a,b)=>a-b)[Math.floor(sizes.length/2)] : null;
  // H2/H3 contrast
  function lum(rgb) {
    const m = rgb.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const parts = m[1].split(',').map(Number);
    const [r,g,b] = parts.slice(0,3).map(v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
    return 0.2126*r + 0.7152*g + 0.0722*b;
  }
  function effBg(el) {
    let e = el;
    while (e) {
      const bg = getComputedStyle(e).backgroundColor;
      if (bg && !bg.startsWith('rgba(0, 0, 0, 0') && bg !== 'transparent') return bg;
      e = e.parentElement;
    }
    return 'rgb(255, 255, 255)';
  }
  out.headings = [];
  document.querySelectorAll('main h2, main h3').forEach(h => {
    const col = cs(h, 'color');
    const bg = effBg(h);
    const L1 = lum(col), L2 = lum(bg);
    const ratio = L1!==null && L2!==null ? (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05) : null;
    out.headings.push({tag: h.tagName, text: (h.innerText||'').trim().slice(0,60),
      color: col, bg, fs: parseFloat(cs(h,'font-size')), ratio: ratio ? +ratio.toFixed(2) : null});
  });
  out.worst_heading_ratio = out.headings.length ? Math.min(...out.headings.map(h=>h.ratio||99)) : null;
  // images
  out.images = [];
  document.querySelectorAll('img').forEach(im => {
    const r = im.getBoundingClientRect();
    const nw = im.naturalWidth, nh = im.naturalHeight;
    const dispA = r.width && r.height ? r.width/r.height : null;
    const natA = nw && nh ? nw/nh : null;
    let distort = null;
    if (dispA && natA) distort = Math.abs(dispA-natA)/natA;
    out.images.push({src: im.getAttribute('src'), alt: im.getAttribute('alt'),
      broken: !im.complete || nw === 0, nw, nh,
      dispW: Math.round(r.width), dispH: Math.round(r.height),
      distort: distort!==null ? +distort.toFixed(3) : null,
      top: Math.round(r.top + window.scrollY), cls: im.className});
  });
  // hero background image (if .hero-img is a div)
  const heroImg = document.querySelector('.hero-img');
  if (heroImg) {
    out.hero_img_el = {tag: heroImg.tagName, cls: heroImg.className,
      bg: heroImg.tagName !== 'IMG' ? cs(heroImg, 'background-image').slice(0,120) : null};
  }
  // section inventory
  out.sections = [...document.querySelectorAll('main section, main > div')].map(s => s.className).filter(Boolean);
  out.main_word_count = mainText.split(/\s+/).filter(Boolean).length;
  out.doc_title = document.title;
  return out;
}
"""

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

results = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for route in ROUTES:
        url = BASE + "/" if route == "/" else BASE + route
        pr = {"route": route, "url": url, "viewports": {}}
        for w, h, label in [(1440, 900, "1440"), (390, 844, "390"), (320, 568, "320")]:
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            page = ctx.new_page()
            errs, failed = [], []
            page.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error",) else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("requestfailed", lambda r: failed.append(f"{r.url} :: {r.failure}"))
            page.on("response", lambda r: failed.append(f"{r.url} :: HTTP {r.status}") if r.status >= 400 and "127.0.0.1" in r.url else None)
            try:
                resp = page.goto(url, wait_until="networkidle", timeout=30000)
                pr["viewports"][label] = {"http": resp.status if resp else None}
                page.wait_for_timeout(400)
                data = page.evaluate(JS_COLLECT)
                pr["viewports"][label].update(data)
                pr["viewports"][label]["console_errors"] = errs
                pr["viewports"][label]["failed_requests"] = failed
                s = slug(route)
                page.screenshot(path=os.path.join(OUTDIR, f"{s}-{label}-top.png"))
                if label == "390":
                    page.screenshot(path=os.path.join(OUTDIR, f"{s}-390-full.png"), full_page=True)
                if label == "1440" and route in ("/", "/emergency-water-extraction", "/commercial-water-damage", "/about"):
                    page.screenshot(path=os.path.join(OUTDIR, f"{s}-1440-full.png"), full_page=True)
            except Exception as e:
                pr["viewports"][label] = {"error": str(e)}
            ctx.close()
        # click-through test at 1440 on homepage + one service page
        results[route] = pr
        print(f"done {route}", flush=True)
    # ---- real-click navigation ----
    clicks = []
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(BASE + "/", wait_until="networkidle")
    page.wait_for_timeout(400)
    try:
        # click first service card link in main
        card = page.query_selector("main a[href*='/emergency-water-extraction']")
        if card:
            card.click()
            page.wait_for_load_state("networkidle")
            clicks.append({"action": "home card -> emergency", "url": page.url,
                           "subpath_kept": page.url.startswith(BASE),
                           "h1": page.query_selector("main h1").inner_text() if page.query_selector("main h1") else None,
                           "styled": page.evaluate("() => getComputedStyle(document.querySelector('main h1')).fontSize")})
        # click a body link on that page
        body_link = page.query_selector("main p a[href^='/midvale-water-damage/']")
        if body_link:
            href = body_link.get_attribute("href")
            body_link.click()
            page.wait_for_load_state("networkidle")
            clicks.append({"action": f"body link {href}", "url": page.url,
                           "subpath_kept": page.url.startswith(BASE),
                           "h1": page.query_selector("main h1").inner_text() if page.query_selector("main h1") else None})
        # footer link to a location
        page.goto(BASE + "/", wait_until="networkidle")
        fl = page.query_selector("footer a[href*='cottonwood']")
        if fl:
            fl.click()
            page.wait_for_load_state("networkidle")
            clicks.append({"action": "footer -> cottonwood", "url": page.url,
                           "subpath_kept": page.url.startswith(BASE),
                           "h1": page.query_selector("main h1").inner_text() if page.query_selector("main h1") else None})
        # header nav link to about
        page.goto(BASE + "/", wait_until="networkidle")
        nl = page.query_selector("header a[href*='/about']")
        if nl:
            nl.click()
            page.wait_for_load_state("networkidle")
            clicks.append({"action": "header nav -> about", "url": page.url,
                           "subpath_kept": page.url.startswith(BASE),
                           "h1": page.query_selector("main h1").inner_text() if page.query_selector("main h1") else None})
    except Exception as e:
        clicks.append({"action": "CLICK ERROR", "error": str(e)})
    clicks.append({"pageerrors": errs})
    ctx.close()
    browser.close()

json.dump({"routes": results, "clicks": clicks, "expected_h1": EXPECTED_H1},
          open(os.path.join(OUTDIR, "10x-design-render.json"), "w"), indent=1, default=str)
print("CLICKS:", json.dumps(clicks, indent=1))
print("DONE render pass")
