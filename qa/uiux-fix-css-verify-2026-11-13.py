#!/usr/bin/env python3
"""Verify the 4 UI/UX CSS fixes for Midvale UT (Stage 1 round).
Serves out/ on http://127.0.0.1:8345/midvale-water-damage/ (linkfix-serve.py).
Measures, per route:
  - 320x568: H1/H2 font sizes, Button 2 bottom (must be <=568), overflow
  - 320x844 / 390x844: Button 2 scroll-0 visible, overflow
  - 1440x900: overflow, home card grid columns/rows/equal heights, H1 count
  - 390: Magna table fade ::after opacity at scroll 0 / max; narrow-table fade
  - contrast worst pairs (same method as uiux audit: leaf text vs bg, min+0.5)
  - H1 count per page, all widths
Output: qa/uiux-fix-css-verify-2026-11-13.json
"""
import json, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8345/midvale-water-damage"
ROUTES = [
 "/", "/about", "/contact", "/emergency-water-extraction", "/basement-flooding-cleanup",
 "/window-well-flooding", "/burst-pipe-water-damage", "/sewage-backup-cleanup",
 "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage", "/ceiling-water-damage",
 "/crawl-space-water-damage", "/hardwood-floor-cabinet-drying", "/condo-apartment-water-damage",
 "/commercial-water-damage", "/storm-flood-damage", "/mold-remediation",
 "/water-leak-detection", "/water-damage-repair", "/locations/cottonwood-heights-ut",
 "/locations/south-salt-lake-ut", "/locations/magna-ut",
 "/midvale-water-sewer-emergency-contacts", "/privacy-policy", "/terms-of-use",
 "/disclaimer", "/resources/frozen-pipes-midvale", "/resources/winterize-swamp-cooler-utah",
 "/resources/upstairs-unit-leak-who-pays-utah", "/resources/can-mold-grow-in-utah",
 "/resources/basement-flooding-spring-snowmelt-utah",
]
ARGS = ["--single-process", "--no-zygote", "--disable-gpu", "--disable-dev-shm-usage"]

JS_HERO = r"""
() => {
  const cs = el => getComputedStyle(el);
  const h1 = document.querySelector('h1');
  const h2 = document.querySelector('h2');
  const out = {
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    h1Count: document.querySelectorAll('h1').length,
    h1Size: h1 ? parseFloat(cs(h1).fontSize) : null,
    h1Lines: h1 ? Math.round(h1.getBoundingClientRect().height / parseFloat(cs(h1).lineHeight)) : null,
    h2Size: h2 ? parseFloat(cs(h2).fontSize) : null,
    h3Size: (() => { const h3 = document.querySelector('h3'); return h3 ? parseFloat(cs(h3).fontSize) : null; })(),
  };
  // Button 2 = the non-tel hero CTA ("Request Emergency Help") in .hero-buttons
  const btns = [...document.querySelectorAll('.hero-buttons .btn')];
  const b2 = btns.find(b => (b.textContent || '').includes('Request Emergency Help'))
        || btns[btns.length - 1];
  if (b2) {
    const r = b2.getBoundingClientRect();
    out.btn2 = {text: (b2.textContent || '').trim().slice(0, 40), top: +r.top.toFixed(1),
                bottom: +r.bottom.toFixed(1), h: +r.height.toFixed(1), w: +r.width.toFixed(1),
                visible: r.bottom <= window.innerHeight && r.top >= 0};
    const b1 = btns[0];
    if (b1) { const r1 = b1.getBoundingClientRect();
      out.btn1 = {bottom: +r1.bottom.toFixed(1), h: +r1.height.toFixed(1), w: +r1.width.toFixed(1)}; }
  }
  return out;
}
"""

JS_CONTRAST = r"""
() => {
  const cs = el => getComputedStyle(el);
  const vis = el => { const r = el.getBoundingClientRect(); const s = cs(el);
    return r.width>0 && r.height>0 && s.display!=='none' && s.visibility!=='hidden'; };
  function lum(rgb){ const m=rgb.match(/[\d.]+/g); if(!m) return null;
    const c=m.slice(0,3).map(v=>{v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4);});
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
  function bgOf(el){ let e=el; while(e){ const b=cs(e).backgroundColor;
      if(b && !b.startsWith('rgba(0, 0, 0, 0)') && b!=='transparent') return b; e=e.parentElement; }
    return 'rgb(255, 255, 255)'; }
  function ratio(fg,bg){ const L1=lum(fg),L2=lum(bg); if(L1==null||L2==null) return null;
    const hi=Math.max(L1,L2),lo=Math.min(L1,L2); return (hi+0.05)/(lo+0.05); }
  const txt = (el)=> (el.textContent||'').trim().replace(/\s+/g,' ').slice(0,50);
  let worst = [];
  document.querySelectorAll('body *').forEach(el=>{ if(!vis(el)) return;
    if(el.children.length>0) return; const t=(el.textContent||'').trim(); if(!t) return;
    const s=cs(el); const sz=parseFloat(s.fontSize); const r=ratio(s.color,bgOf(el));
    if(r==null) return; const large = sz>=24 || (sz>=18.66 && parseInt(s.fontWeight)>=700);
    const min = large?3:4.5;
    worst.push({text:txt(el), size:sz, ratio:+r.toFixed(2), min}); });
  worst.sort((a,b)=>a.ratio-b.ratio);
  return {worst5: worst.slice(0,5), belowAA: worst.filter(w=>w.ratio < w.min)};
}
"""

JS_CARDS = r"""
() => {
  const out = {};
  const grids = [...document.querySelectorAll('#services .card-grid, #areas .card-grid')];
  grids.forEach(g => {
    const cs = getComputedStyle(g);
    const cards = [...g.querySelectorAll('.card')];
    const rows = {};
    cards.forEach(c => {
      const r = c.getBoundingClientRect();
      const key = Math.round(r.top);
      rows[key] = rows[key] || [];
      rows[key].push({h: +r.height.toFixed(1), w: +r.width.toFixed(1),
                      imgH: (() => { const im = c.querySelector('img'); if (!im) return null;
                        const ir = im.getBoundingClientRect(); return +ir.height.toFixed(1); })()});
    });
    const id = g.closest('section') ? g.closest('section').id : '?';
    out[id] = {cols: cs.gridTemplateColumns.split(' ').length, nCards: cards.length,
               rows: Object.entries(rows).map(([top, cs2]) => ({top: +top, n: cs2.length,
                 heights: [...new Set(cs2.map(c => c.h))], widths: [...new Set(cs2.map(c => c.w))],
                 imgHeights: [...new Set(cs2.map(c => c.imgH))]}))};
  });
  return out;
}
"""

JS_TABLES = r"""
() => {
  const out = [];
  document.querySelectorAll('.table-wrap').forEach((w, i) => {
    const t = w.querySelector('table');
    const cs = getComputedStyle(w, '::after');
    out.push({i, scrollW: w.scrollWidth, clientW: w.clientWidth,
              maxScroll: w.scrollWidth - w.clientWidth,
              tableW: t ? +t.getBoundingClientRect().width.toFixed(1) : null,
              afterOpacity: cs.opacity, afterDisplay: cs.display,
              afterBg: cs.backgroundImage.slice(0, 60)});
  });
  return out;
}
"""

OUT_PATH = "/home/hatch/workspace/midvale-water-damage/qa/uiux-fix-css-verify-2026-11-13.json"

def save(results):
    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=1)

def measure_one(p, route, width, height, js):
    """One (route, viewport) in a FRESH browser (single-process mode is
    fragile: one renderer crash kills the whole browser — see render audit).
    Retries once after a relaunch."""
    last_err = None
    for attempt in range(2):
        b = None
        try:
            b = p.chromium.launch(args=ARGS)
            ctx = b.new_context(viewport={"width": width, "height": height},
                                device_scale_factor=1, is_mobile=width < 500)
            pg = ctx.new_page()
            pg.goto(BASE + route, wait_until="load", timeout=60000)
            pg.wait_for_timeout(400)
            d = pg.evaluate(js)
            ctx.close(); b.close()
            return d
        except Exception as e:
            last_err = str(e)[:200]
            try:
                if b: b.close()
            except Exception:
                pass
    return {"error": last_err}

def main():
    results = {}
    with sync_playwright() as p:
        # --- 320x568: Button 2 hard constraint + H1/H2 ---
        for route in ROUTES:
            results.setdefault(route, {})["320x568"] = measure_one(p, route, 320, 568, JS_HERO)
            save(results)
        # --- 320x844 + 390x844: Button 2 scroll-0 + overflow ---
        for (w, h) in ((320, 844), (390, 844)):
            for route in ROUTES:
                results.setdefault(route, {})[f"{w}x{h}"] = measure_one(p, route, w, h, JS_HERO)
                save(results)
        # --- 1440x900: overflow, cards, contrast, H1 ---
        for route in ROUTES:
            d = measure_one(p, route, 1440, 900, JS_HERO)
            if isinstance(d, dict) and "error" not in d:
                c = measure_one(p, route, 1440, 900, JS_CONTRAST)
                d["contrast"] = c
                if route == "/":
                    d["cards"] = measure_one(p, route, 1440, 900, JS_CARDS)
            results.setdefault(route, {})["1440"] = d
            save(results)
        # --- 390 tables: all-route inventory ---
        table_summary = {}
        for route in ROUTES:
            table_summary[route] = measure_one(p, route, 390, 844, JS_TABLES)
            results["_tables390"] = table_summary
            save(results)
        # --- Magna deep probe + screenshots (one browser, guarded) ---
        try:
            b = p.chromium.launch(args=ARGS)
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True)
            pg = ctx.new_page()
            pg.goto(BASE + "/locations/magna-ut", wait_until="load", timeout=60000)
            pg.wait_for_timeout(400)
            magna = pg.evaluate(r"""
            () => {
              const w = document.querySelector('.table-wrap');
              const cs = getComputedStyle(w, '::after');
              return {scrollW: w.scrollWidth, clientW: w.clientWidth, max: w.scrollWidth - w.clientWidth,
                      opacity0: cs.opacity};
            }""")
            pg.evaluate("document.querySelector('.table-wrap').scrollLeft = 100")
            pg.wait_for_timeout(600)
            magna["opacityMid"] = pg.evaluate("getComputedStyle(document.querySelector('.table-wrap'), '::after').opacity")
            pg.evaluate("document.querySelector('.table-wrap').scrollLeft = document.querySelector('.table-wrap').scrollWidth")
            pg.wait_for_timeout(600)
            magna["opacityMax"] = pg.evaluate("getComputedStyle(document.querySelector('.table-wrap'), '::after').opacity")
            magna["scrollLeftMax"] = pg.evaluate("document.querySelector('.table-wrap').scrollLeft")
            pg.evaluate("document.querySelector('.table-wrap').scrollLeft = 0")
            pg.wait_for_timeout(600)
            el = pg.query_selector(".table-wrap")
            el.screenshot(path="/home/hatch/workspace/midvale-water-damage/qa/uiux-fix-magna-table-390.png")
            results["_magnaFade"] = magna
            save(results)
            ctx.close()
            ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
            pg = ctx.new_page()
            pg.goto(BASE + "/", wait_until="load", timeout=60000)
            pg.wait_for_timeout(500)
            pg.evaluate("document.querySelector('#services').scrollIntoView()")
            pg.wait_for_timeout(400)
            pg.screenshot(path="/home/hatch/workspace/midvale-water-damage/qa/uiux-fix-home-cards-1440.png")
            ctx.close()
            ctx = b.new_context(viewport={"width": 320, "height": 568}, device_scale_factor=1, is_mobile=True)
            pg = ctx.new_page()
            pg.goto(BASE + "/condo-apartment-water-damage", wait_until="load", timeout=60000)
            pg.wait_for_timeout(400)
            pg.screenshot(path="/home/hatch/workspace/midvale-water-damage/qa/uiux-fix-hero-320-worst.png")
            ctx.close()
            b.close()
        except Exception as e:
            results["_screenshots"] = {"error": str(e)[:300]}
            save(results)
    save(results)
    # ---- console summary ----
    def b2bottom(route, key):
        d = results[route].get(key, {})
        return d.get("btn2", {}).get("bottom") if isinstance(d, dict) else None
    worst568 = max((b2bottom(r, "320x568") or 0) for r in ROUTES)
    worst568_route = [r for r in ROUTES if b2bottom(r, "320x568") == worst568]
    print("routes:", len(ROUTES))
    print("H1@320 all 30px:", all(results[r]["320x568"].get("h1Size") == 30 for r in ROUTES),
          "| H2@320 all 28px:", all(results[r]["320x568"].get("h2Size") == 28 for r in ROUTES))
    print("H1 count 1/page @320:", all(results[r]["320x568"].get("h1Count") == 1 for r in ROUTES),
          "| @1440:", all(results[r]["1440"].get("h1Count") == 1 for r in ROUTES))
    print("Button2 worst bottom @320x568:", worst568, "on", worst568_route, "(limit 568)")
    print("Button2 visible scroll-0 @320x844:", sum(1 for r in ROUTES if results[r]["320x844"].get("btn2", {}).get("visible")),
          "/31 | @390x844:", sum(1 for r in ROUTES if results[r]["390x844"].get("btn2", {}).get("visible")), "/31")
    print("overflow>0 @320x568:", sum(1 for r in ROUTES if (results[r]["320x568"].get("overflow") or 0) > 0),
          "| @320x844:", sum(1 for r in ROUTES if (results[r]["320x844"].get("overflow") or 0) > 0),
          "| @390x844:", sum(1 for r in ROUTES if (results[r]["390x844"].get("overflow") or 0) > 0),
          "| @1440:", sum(1 for r in ROUTES if (results[r]["1440"].get("overflow") or 0) > 0))
    below = [(r, w) for r in ROUTES for w in results[r]["1440"].get("contrast", {}).get("belowAA", [])]
    print("contrast below AA @1440:", len(below), below[:5])
    worst_ratio = min((w["ratio"] for r in ROUTES for w in results[r]["1440"].get("contrast", {}).get("worst5", [])), default=None)
    print("worst contrast ratio @1440:", worst_ratio)
    print("home cards @1440:", json.dumps(results["/"]["1440"].get("cards"), indent=1))
    print("Magna fade @390:", json.dumps(magna))
    n_overflow_tables = sum(1 for r in ROUTES for t in (table_summary.get(r) or []) if isinstance(t, dict) and t.get("maxScroll", 0) > 0)
    n_fade_on = sum(1 for r in ROUTES for t in (table_summary.get(r) or []) if isinstance(t, dict) and t.get("maxScroll", 0) > 0 and t.get("afterOpacity") == "1")
    n_fade_off_fit = sum(1 for r in ROUTES for t in (table_summary.get(r) or []) if isinstance(t, dict) and t.get("maxScroll", 0) == 0 and t.get("afterOpacity") == "0")
    print(f"tables @390: {n_overflow_tables} overflowing, fade ON at scroll-0 on {n_fade_on} of them; "
          f"fitting tables with fade OFF: {n_fade_off_fit}")

if __name__ == "__main__":
    main()
