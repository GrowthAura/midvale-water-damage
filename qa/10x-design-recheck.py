#!/usr/bin/env python3
"""Image re-check for Midvale 10x design round: scrolls each page fully so
lazy-loaded images actually load, then re-measures broken/distortion with
object-fit awareness. Also re-runs real-click navigation with proper waits.
TEST ONLY. Writes qa/10x-design/10x-design-images.json.
"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUTDIR = os.path.join(ROOT, "qa", "10x-design")
BASE = "http://127.0.0.1:8325/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]

JS_IMGS = r"""
() => {
  const out = [];
  document.querySelectorAll('img').forEach(im => {
    const r = im.getBoundingClientRect();
    const cs = getComputedStyle(im);
    const nw = im.naturalWidth, nh = im.naturalHeight;
    const dispA = r.width && r.height ? r.width/r.height : null;
    const natA = nw && nh ? nw/nh : null;
    out.push({src: im.getAttribute('src'), alt: (im.getAttribute('alt')||'').slice(0,60),
      broken: !im.complete || nw === 0, nw, nh,
      dispW: Math.round(r.width), dispH: Math.round(r.height),
      objectFit: cs.objectFit, distort: (dispA && natA) ? +((Math.abs(dispA-natA)/natA).toFixed(3)) : null,
      loading: im.getAttribute('loading')});
  });
  return out;
}
"""

results = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for route in ROUTES:
        url = BASE + "/" if route == "/" else BASE + route
        pr = {}
        for w, h, label in [(1440, 900, "1440"), (390, 844, "390")]:
            ctx = browser.new_context(viewport={"width": w, "height": h})
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(300)
            # scroll through in steps to trigger lazy loads
            page.evaluate("""async () => {
              const H = document.documentElement.scrollHeight;
              for (let y = 0; y <= H; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
              window.scrollTo(0, 0);
            }""")
            page.wait_for_timeout(800)
            pr[label] = page.evaluate(JS_IMGS)
            ctx.close()
        results[route] = pr
        print("done", route, flush=True)

    # ---- click test with proper waits ----
    clicks = []
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(BASE + "/", wait_until="networkidle")
    page.wait_for_timeout(400)
    try:
        card = page.query_selector("main a[href*='/emergency-water-extraction']")
        card.click()
        page.wait_for_url("**/emergency-water-extraction", timeout=10000)
        page.wait_for_timeout(300)
        clicks.append({"action": "home card -> emergency", "url": page.url,
                       "subpath_kept": page.url.startswith(BASE),
                       "h1": page.query_selector("main h1").inner_text().strip() if page.query_selector("main h1") else None,
                       "styled": page.evaluate("() => getComputedStyle(document.querySelector('main h1')).fontSize")})
        bl = page.query_selector("main p a[href^='/midvale-water-damage/']")
        href = bl.get_attribute("href") if bl else None
        if bl:
            bl.click()
            page.wait_for_url("**" + href.replace("/midvale-water-damage", ""), timeout=10000)
            page.wait_for_timeout(300)
            clicks.append({"action": f"body link {href}", "url": page.url,
                           "subpath_kept": page.url.startswith(BASE),
                           "h1": page.query_selector("main h1").inner_text().strip() if page.query_selector("main h1") else None})
        page.goto(BASE + "/", wait_until="networkidle")
        fl = page.query_selector("footer a[href*='cottonwood']")
        if fl:
            fl.click()
            page.wait_for_url("**/cottonwood-heights-ut", timeout=10000)
            page.wait_for_timeout(300)
            clicks.append({"action": "footer -> cottonwood", "url": page.url,
                           "subpath_kept": page.url.startswith(BASE),
                           "h1": page.query_selector("main h1").inner_text().strip() if page.query_selector("main h1") else None})
        page.goto(BASE + "/", wait_until="networkidle")
        nav_links = page.evaluate("() => [...document.querySelectorAll('header a')].map(a => a.getAttribute('href'))")
        clicks.append({"header_nav_hrefs": nav_links})
        nl = page.query_selector("header a[href*='/about']")
        if nl:
            nl.click()
            page.wait_for_url("**/about", timeout=10000)
            page.wait_for_timeout(300)
            clicks.append({"action": "header nav -> about", "url": page.url,
                           "subpath_kept": page.url.startswith(BASE),
                           "h1": page.query_selector("main h1").inner_text().strip() if page.query_selector("main h1") else None})
        else:
            clicks.append({"action": "header nav -> about", "note": "no /about link in header nav", "header_nav_hrefs": nav_links})
    except Exception as e:
        clicks.append({"action": "CLICK ERROR", "error": str(e), "url_now": page.url})
    ctx.close()
    browser.close()

json.dump({"images_after_scroll": results, "clicks": clicks},
          open(os.path.join(OUTDIR, "10x-design-images.json"), "w"), indent=1)
print("CLICKS:", json.dumps(clicks, indent=1))
print("DONE image re-check")
