#!/usr/bin/env python3
"""W3 follow-up adjudication v2 — crash-hardened.
Fresh browser per route, per-route retry, incremental progress save.
"""
import json, os, time, xml.etree.ElementTree as ET
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.expanduser("~/workspace/midvale-water-damage")
BASE_URL = "http://127.0.0.1:8350/midvale-water-damage"
QA_DIR = os.path.join(BASE_DIR, "qa")
PROGRESS = os.path.join(QA_DIR, "final5-adjudication.progress.json")

def slug_for(path):
    p = path.strip("/")
    return "home" if not p else p.replace("/", "-")

def routes():
    t = ET.parse(os.path.join(BASE_DIR, "out", "sitemap.xml"))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    out = []
    for e in t.getroot().findall(".//s:loc", ns):
        u = urlparse(e.text)
        out.append(u.path.replace("/midvale-water-damage", "") or "/")
    return out

IMG_JS = r"""
async () => {
  const H = document.documentElement.scrollHeight;
  for (let y = 0; y <= H; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 250)); }
  window.scrollTo(0, document.documentElement.scrollHeight);
  await new Promise(r => setTimeout(r, 1200));
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 600));
  const imgs = Array.from(document.querySelectorAll('img'));
  return {
    total: imgs.length,
    loaded: imgs.filter(i => i.complete && i.naturalWidth > 0).length,
    stillBroken: imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => ({
      src: i.getAttribute('src'), loading: i.getAttribute('loading'),
      cls: i.className, complete: i.complete, nw: i.naturalWidth
    })),
  };
}
"""

SPAN_JS = r"""
() => {
  const vw = window.innerWidth;
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0) return;
    if (r.right > vw + 1 || r.left < -1) {
      if (el.closest('.table-wrap')) return;
      if (getComputedStyle(el).position === 'fixed') return;
      let clip = null, a = el.parentElement;
      while (a && a !== document.body) {
        const cs = getComputedStyle(a);
        if (cs.overflowX === 'hidden' || cs.overflowX === 'clip' || cs.overflow === 'hidden') { clip = a.tagName + '.' + (typeof a.className === 'string' ? a.className.split(' ')[0] : ''); break; }
        a = a.parentElement;
      }
      out.push({tag: el.tagName, cls: typeof el.className === 'string' ? el.className : '', text: (el.textContent || '').trim().slice(0, 60),
                right: Math.round(r.right), left: Math.round(r.left), top: Math.round(r.top),
                clippedBy: clip, display: getComputedStyle(el).display});
    }
  });
  return out;
}
"""

FONT_JS = r"""
() => {
  const ps = Array.from(document.querySelectorAll('main p')).filter(p =>
    !p.classList.contains('eyebrow') && !p.closest('.hero') && !p.classList.contains('hero-intro'));
  const sizes = ps.map(p => getComputedStyle(p).fontSize);
  const eyebrow = document.querySelector('.eyebrow');
  return {bodyCopyCount: ps.length, bodyCopySizes: [...new Set(sizes)],
          eyebrowSize: eyebrow ? getComputedStyle(eyebrow).fontSize : null,
          heroIntroSize: (() => { const h = document.querySelector('.hero-intro'); return h ? getComputedStyle(h).fontSize : null; })()};
}
"""

TABLE_JS = r"""
() => {
  return Array.from(document.querySelectorAll('.table-wrap')).map((w, i) => {
    const over = w.scrollWidth > w.clientWidth + 1;
    let moved = null;
    if (over) { const b = w.scrollLeft; w.scrollLeft = 60; moved = w.scrollLeft > b; w.scrollLeft = 0; }
    const cue = getComputedStyle(w, '::after');
    return {i, over, cueOpacity: cue.opacity, swipeMoved: moved,
            wrapperW: w.clientWidth, scrollW: w.scrollWidth};
  });
}
"""

def check_route(p, path, slug):
    url = BASE_URL + ("" if path == "/" else path)
    browser = p.chromium.launch(channel="chromium", args=["--disable-dev-shm-usage"])
    try:
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(1500)
        img = page.evaluate(IMG_JS)
        fonts = page.evaluate(FONT_JS)
        tables390 = page.evaluate(TABLE_JS)
        ctx.close()
        ctx2 = browser.new_context(viewport={"width": 320, "height": 568})
        page2 = ctx2.new_page()
        page2.goto(url, wait_until="domcontentloaded", timeout=30000)
        page2.wait_for_timeout(1500)
        spans = page2.evaluate(SPAN_JS)
        tables320 = page2.evaluate(TABLE_JS)
        ctx2.close()
        return {"slug": slug, "img": img, "fonts": fonts, "tables390": tables390,
                "tables320": tables320, "spans320": spans}
    finally:
        browser.close()

def menu_test_corrected(p, slug, url):
    browser = p.chromium.launch(channel="chromium", args=["--disable-dev-shm-usage"])
    try:
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        res = {"slug": slug, "pass": True, "steps": {}}
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, 600)")
        page.wait_for_timeout(400)
        y0 = page.evaluate("window.scrollY")
        res["steps"]["scrollBefore"] = y0
        page.locator(".menu-btn").click()
        page.wait_for_timeout(500)
        res["steps"]["ariaExpandedOpen"] = page.locator(".menu-btn").get_attribute("aria-expanded")
        res["steps"]["navClassOpen"] = page.evaluate("document.getElementById('main-nav').className")
        links = page.evaluate("""() => Array.from(document.querySelectorAll('#main-nav a')).map(a => { const r = a.getBoundingClientRect(); return {t: a.textContent.trim(), vis: r.width > 0 && r.height > 0 && r.top >= 0 && r.bottom <= window.innerHeight}; })""")
        res["steps"]["linksVisible"] = f"{sum(1 for l in links if l['vis'])}/{len(links)}"
        lock = page.evaluate("() => { const cs = getComputedStyle(document.body); return {position: cs.position, top: cs.top}; }")
        res["steps"]["bodyLockStyle"] = lock
        page.evaluate("window.scrollTo(0, 1400)")
        page.wait_for_timeout(300)
        lock2 = page.evaluate("() => { const cs = getComputedStyle(document.body); return {position: cs.position, top: cs.top, scrollY: window.scrollY}; }")
        res["steps"]["afterScrollAttempt"] = lock2
        res["steps"]["scrollLocked"] = (lock2["top"] == "-600px" and lock2["position"] == "fixed")
        page.locator(".menu-btn").click()
        page.wait_for_timeout(500)
        res["steps"]["ariaExpandedClose"] = page.locator(".menu-btn").get_attribute("aria-expanded")
        res["steps"]["navClassClose"] = page.evaluate("document.getElementById('main-nav').className")
        y_after = page.evaluate("window.scrollY")
        res["steps"]["scrollYAfterClose"] = y_after
        res["steps"]["scrollRestored"] = (y_after == y0)
        res["pass"] = (res["steps"]["ariaExpandedOpen"] == "true" and "open" in res["steps"]["navClassOpen"]
                       and res["steps"]["linksVisible"].startswith(str(len(links)) + "/")
                       and res["steps"]["scrollLocked"]
                       and res["steps"]["ariaExpandedClose"] == "false" and "open" not in res["steps"]["navClassClose"]
                       and res["steps"]["scrollRestored"])
        return res
    finally:
        browser.close()

def main():
    all_routes = routes()
    out = {"routes": [], "menu": []}
    done = set()
    if os.path.exists(PROGRESS):
        try:
            prev = json.load(open(PROGRESS))
            out = prev
            done = {r["slug"] for r in out["routes"]}
            print(f"resumed: {len(done)} routes done")
        except Exception as e:
            print("progress unreadable:", e)
    with sync_playwright() as p:
        for path in all_routes:
            slug = slug_for(path)
            if slug in done:
                continue
            entry = None
            for attempt in range(3):
                try:
                    entry = check_route(p, path, slug)
                    break
                except Exception as e:
                    print(f"  !! {slug} attempt {attempt+1}: {str(e)[:150]}")
                    time.sleep(3)
            if entry is None:
                entry = {"slug": slug, "error": "renderer crash after 3 attempts"}
            out["routes"].append(entry)
            done.add(slug)
            with open(PROGRESS, "w") as f:
                json.dump(out, f, indent=2)
            if "img" in entry:
                print(f"done {slug}: imgs {entry['img']['loaded']}/{entry['img']['total']} stillBroken={len(entry['img']['stillBroken'])} spans320={len(entry['spans320'])}")
            else:
                print(f"done {slug}: ERROR {entry.get('error')}")
        for slug in ["home", "emergency-water-extraction", "mold-remediation"]:
            path = "/" if slug == "home" else f"/{slug}"
            res = None
            for attempt in range(3):
                try:
                    res = menu_test_corrected(p, slug, BASE_URL + ("" if path == "/" else path))
                    break
                except Exception as e:
                    print(f"  !! menu {slug} attempt {attempt+1}: {str(e)[:150]}")
                    time.sleep(3)
            if res is None:
                res = {"slug": slug, "pass": False, "error": "crash after 3 attempts"}
            out["menu"].append(res)
            print(f"menu {slug}: pass={res['pass']} {res.get('steps', {})}")
            with open(PROGRESS, "w") as f:
                json.dump(out, f, indent=2)
    with open(os.path.join(QA_DIR, "final5-render-mobile-adjudication.json"), "w") as f:
        json.dump(out, f, indent=2)
    tot_imgs = sum(x["img"]["total"] for x in out["routes"] if "img" in x)
    tot_loaded = sum(x["img"]["loaded"] for x in out["routes"] if "img" in x)
    tot_broken = sum(len(x["img"]["stillBroken"]) for x in out["routes"] if "img" in x)
    print(f"IMAGES AFTER SCROLL: {tot_loaded}/{tot_imgs} loaded, still broken {tot_broken}")
    for x in out["routes"]:
        if "img" in x and x["img"]["stillBroken"]:
            print("  STILL BROKEN", x["slug"], x["img"]["stillBroken"])
    print("FONTS bodyCopySizes:", set(tuple(sorted(set(f['fonts']['bodyCopySizes']))) for f in out["routes"] if "fonts" in f),
          "eyebrow@390:", set(f["fonts"]["eyebrowSize"] for f in out["routes"] if "fonts" in f),
          "heroIntro:", set(f["fonts"]["heroIntroSize"] for f in out["routes"] if "fonts" in f))
    print("SPAN320 routes with spans:", sum(1 for s in out["routes"] if s.get("spans320")))
    for s in out["routes"]:
        if s.get("spans320"):
            print("  ", s["slug"], s["spans320"])
    n_ov = sum(1 for t in out["routes"] for tb in t.get("tables390", []) + t.get("tables320", []) if tb["over"])
    n_cue = sum(1 for t in out["routes"] for tb in t.get("tables390", []) + t.get("tables320", []) if tb["over"] and tb["cueOpacity"] == "0")
    n_swipe = sum(1 for t in out["routes"] for tb in t.get("tables390", []) + t.get("tables320", []) if tb["over"] and tb["swipeMoved"] is False)
    print(f"TABLES: {n_ov} overflowing wrappers, cue missing {n_cue}, not swipeable {n_swipe}")
    print("MENU:", [(m["slug"], m["pass"]) for m in out["menu"]])

if __name__ == "__main__":
    main()
