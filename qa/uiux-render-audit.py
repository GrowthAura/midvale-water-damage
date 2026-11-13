#!/usr/bin/env python3
"""Render audit: screenshot all 31 Midvale routes at desktop 1440 + mobile 390,
full-page, after slow scroll (lazy images). Collect per-page section catalogue
+ overflow/broken-image metrics. Writes qa/uiux-render-data.json.
Audit only — no source edits."""
import json, os, time, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8341/midvale-water-damage"
OUT = os.path.expanduser("~/workspace/midvale-water-damage/qa/uiux-render")
os.makedirs(OUT, exist_ok=True)

ROUTES = [
    ("home", ""),
    ("about", "about"),
    ("basement-flooding-cleanup", "basement-flooding-cleanup"),
    ("burst-pipe-water-damage", "burst-pipe-water-damage"),
    ("ceiling-water-damage", "ceiling-water-damage"),
    ("commercial-water-damage", "commercial-water-damage"),
    ("condo-apartment-water-damage", "condo-apartment-water-damage"),
    ("contact", "contact"),
    ("crawl-space-water-damage", "crawl-space-water-damage"),
    ("disclaimer", "disclaimer"),
    ("emergency-water-extraction", "emergency-water-extraction"),
    ("hardwood-floor-cabinet-drying", "hardwood-floor-cabinet-drying"),
    ("locations-cottonwood-heights-ut", "locations/cottonwood-heights-ut"),
    ("locations-magna-ut", "locations/magna-ut"),
    ("locations-south-salt-lake-ut", "locations/south-salt-lake-ut"),
    ("midvale-water-sewer-emergency-contacts", "midvale-water-sewer-emergency-contacts"),
    ("mold-remediation", "mold-remediation"),
    ("privacy-policy", "privacy-policy"),
    ("resources-basement-flooding-spring-snowmelt-utah", "resources/basement-flooding-spring-snowmelt-utah"),
    ("resources-can-mold-grow-in-utah", "resources/can-mold-grow-in-utah"),
    ("resources-frozen-pipes-midvale", "resources/frozen-pipes-midvale"),
    ("resources-upstairs-unit-leak-who-pays-utah", "resources/upstairs-unit-leak-who-pays-utah"),
    ("resources-winterize-swamp-cooler-utah", "resources/winterize-swamp-cooler-utah"),
    ("sewage-backup-cleanup", "sewage-backup-cleanup"),
    ("storm-flood-damage", "storm-flood-damage"),
    ("swamp-cooler-leak-water-damage", "swamp-cooler-leak-water-damage"),
    ("terms-of-use", "terms-of-use"),
    ("water-damage-repair", "water-damage-repair"),
    ("water-heater-leak-cleanup", "water-heater-leak-cleanup"),
    ("water-leak-detection", "water-leak-detection"),
    ("window-well-flooding", "window-well-flooding"),
]

METRICS_JS = r"""
() => {
  const q = s => document.querySelectorAll(s).length;
  const main = document.querySelector('main') || document.body;
  const h1 = [...document.querySelectorAll('h1')].map(h => h.innerText.trim());
  const h2s = [...main.querySelectorAll('h2')].map(h => h.innerText.trim());
  const h3s = [...main.querySelectorAll('h3')].map(h => h.innerText.trim());
  // sections in order: top-level sections inside main, else h2 groups
  const sections = [...main.querySelectorAll('section')].map(s => {
    const h = s.querySelector('h2, h3');
    return {heading: h ? h.innerText.trim().slice(0,120) : '(no heading)',
            cls: (s.className||'').toString().slice(0,80),
            p: s.querySelectorAll('p').length,
            img: s.querySelectorAll('img').length,
            table: s.querySelectorAll('table').length,
            list: s.querySelectorAll('ul,ol').length,
            height: Math.round(s.getBoundingClientRect().height)};
  });
  const imgs = [...document.querySelectorAll('img')].map(im => ({
    src: (im.getAttribute('src')||'').slice(-60),
    natural: im.naturalWidth, complete: im.complete,
    disp: Math.round(im.getBoundingClientRect().width) + 'x' + Math.round(im.getBoundingClientRect().height),
    loading: im.getAttribute('loading') || 'eager'
  }));
  const brokenLocal = imgs.filter(i => !i.src.includes('google') && !i.src.includes('maps') && (i.natural === 0 && i.complete));
  // blank-band heuristic: visible block elements in main taller than 300px with no visible text and no img
  const blanks = [];
  document.querySelectorAll('main section, main div').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.height > 400 && el.innerText.trim().length < 10 && el.querySelectorAll('img').length === 0) {
      blanks.push({tag: el.tagName, cls: (el.className||'').toString().slice(0,60), h: Math.round(r.height)});
    }
  });
  // elements wider than viewport (overflow contributors)
  const vw = document.documentElement.clientWidth;
  const wide = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > vw + 1 && r.width < 5000) {
      wide.push({tag: el.tagName, cls: (el.className||'').toString().slice(0,60), w: Math.round(r.width)});
    }
  });
  return {
    title: document.title,
    h1, h2s, h3s, sections,
    counts: {p: q('main p'), img: q('main img'), table: q('main table'),
             ul: q('main ul'), ol: q('main ol'),
             faq: q('main [id*="faq" i], main details, main .faq'),
             a: q('main a')},
    scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
    docHeight: document.documentElement.scrollHeight,
    imgs, brokenLocal, blanks: blanks.slice(0,10), wide: wide.slice(0,10),
    bodyText: main.innerText.length
  };
}
"""

def shot_full_page(page, path, vw, vh):
    """Full-page screenshot with segmented fallback (renderer crashes on very
    tall pages in this VM)."""
    try:
        page.screenshot(path=path, full_page=True, timeout=180000)
        return "full"
    except Exception as e:
        print(f"  full-page shot failed ({e}); segmented fallback", flush=True)
    total = page.evaluate("document.documentElement.scrollHeight")
    slices = []
    y = 0
    i = 0
    while y < total:
        h = min(vh, total - y)
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(400)
        tmp = f"/tmp/uiux-slice-{i}.png"
        page.screenshot(path=tmp, clip={"x": 0, "y": y, "width": vw, "height": h})
        slices.append((tmp, h))
        y += vh
        i += 1
    from PIL import Image
    out = Image.new("RGB", (vw, total))
    off = 0
    for tmp, h in slices:
        im = Image.open(tmp).convert("RGB")
        out.paste(im, (0, off))
        off += h
        os.remove(tmp)
    out.save(path)
    return f"segmented-{len(slices)}"

def slow_scroll(page):
    h = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(120)
        y += 600
        h = page.evaluate("document.documentElement.scrollHeight")
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(600)

results = {}
DATA_PATH = os.path.expanduser("~/workspace/midvale-water-damage/qa/uiux-render-data.json")
if os.path.exists(DATA_PATH):
    try:
        results = json.load(open(DATA_PATH))
    except Exception:
        results = {}
with sync_playwright() as pw:
    def new_browser():
        return pw.chromium.launch(args=['--single-process', '--no-zygote',
                                        '--disable-gpu', '--disable-dev-shm-usage'])
    for slug, path in ROUTES:
        if slug in results and "desktop" in results[slug] and "m390" in results[slug]:
            print(f"SKIP {slug} (already in json)", flush=True)
            continue
        url = f"{BASE}/{path}" if path else f"{BASE}/"
        entry = results.get(slug, {"url": url})
        for label, w, hgt in (("desktop", 1440, 900), ("m390", 390, 844)):
            if label in entry and isinstance(entry[label], dict) and "scrollW" in entry[label]:
                print(f"SKIP {slug} {label} (metrics done)", flush=True)
                continue
            for attempt in (1, 2):
                browser = None
                try:
                    browser = new_browser()
                    ctx = browser.new_context(viewport={"width": w, "height": hgt},
                                              device_scale_factor=1, is_mobile=(label == "m390"))
                    page = ctx.new_page()
                    try:
                        page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    except Exception as e:
                        entry[label + "_goto_note"] = f"domcontentloaded timeout: {e}"
                    page.wait_for_timeout(1500)
                    slow_scroll(page)
                    page.wait_for_timeout(800)
                    m = page.evaluate(METRICS_JS)
                    entry[label] = m
                    shot = f"{OUT}/{slug}-{label}-full.png"
                    if not os.path.exists(shot):
                        entry[label + "_shot_mode"] = shot_full_page(page, shot, w, hgt)
                    else:
                        entry[label + "_shot_reused"] = True
                    entry[label + "_shot"] = shot
                    ctx.close()
                    browser.close()
                    break
                except Exception as e:
                    print(f"  FAIL {slug} {label} attempt {attempt}: {e}", flush=True)
                    entry[label + "_error_attempt" + str(attempt)] = str(e)[:300]
                    try:
                        ctx.close()
                    except Exception:
                        pass
                    try:
                        if browser is not None:
                            browser.close()
                    except Exception:
                        pass
                    if attempt == 2:
                        entry[label + "_error"] = str(e)[:300]
            print(f"{slug} {label}: " + (f"H={entry[label]['docHeight']} scrollW={entry[label]['scrollW']} clientW={entry[label]['clientW']} imgs={entry[label]['counts']['img']} brokenLocal={len(entry[label]['brokenLocal'])} blanks={len(entry[label]['blanks'])} wide={len(entry[label]['wide'])}" if isinstance(entry.get(label), dict) and 'docHeight' in entry[label] else "ERROR"), flush=True)
        results[slug] = entry
        with open(DATA_PATH, "w") as f:
            json.dump(results, f, indent=1)

with open(DATA_PATH, "w") as f:
    json.dump(results, f, indent=1)
print("DONE", len(results), "routes")
