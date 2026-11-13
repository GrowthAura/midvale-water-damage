#!/usr/bin/env python3
"""DESIGN-ROUND CSS verification for Midvale (2026-11-13).
Playwright Chromium on the local subpath mirror (port 8331).
Per route x 3 viewports: overflow, H1 count, Button 2 at scroll-0
(320/390), buttons equal, underline computed-style on EVERY internal
link, header/footer em/en-dash count, visible (/.../) paren gate,
body-copy font-size >= 18px, H2/H3 computed colours + ::after bar,
contact form, footer links, link inventory (self-links / orphans),
body-image tags (0 expected while lib/body-images.json is absent).
Reads only the built export (serves it). Writes qa/verify-design-css.json
+ screenshots to qa/render-design/. Does NOT modify site sources.
"""
import json, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "qa", "render-design")
os.makedirs(OUT, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
BASE = "http://localhost:8331/midvale-water-damage"
ROUTES = [p["route"] for p in DATA["pages"]]
PAREN_RE = re.compile(r"\([^)]*\)")
PAREN_PATH_RE = re.compile(r"\(/[^)]+/\)")
PHONE = "(385) 337-3560"

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def url(route):
    return BASE + "/" if route == "/" else BASE + route

results = {}
all_hrefs = {}  # route -> set of normalized internal hrefs (no hash)

srv = subprocess.Popen([sys.executable, "/tmp/linkfix-serve.py", "8331"],
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
                    page.goto(url(route), wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(600)
                except Exception as e:
                    r[label] = {"goto_error": str(e)}
                    ctx.close()
                    continue
                d = page.evaluate("""() => {
                    const cs = (el, prop) => getComputedStyle(el)[prop];
                    const h1s = [...document.querySelectorAll('main h1')];
                    const hero = document.querySelector('main section.hero');
                    const heroLinks = hero ? [...hero.querySelectorAll('a')].filter(a => !a.closest('nav')) : [];
                    const b1 = heroLinks.find(a => a.innerText.trim() === '(385) 337-3560');
                    const b2 = heroLinks.find(a => a.innerText.trim() === 'Request Emergency Help');
                    const rect = (a) => { const b = a.getBoundingClientRect(); return {x: b.x, y: b.y, w: b.width, h: b.height, bottom: b.bottom}; };
                    // every internal link on the page (header, main, footer)
                    const links = [...document.querySelectorAll('header a, main a, footer a')];
                    const under = links.filter(a => {
                        const s = getComputedStyle(a);
                        return (s.textDecorationLine && s.textDecorationLine !== 'none')
                            || (s.borderBottomStyle && s.borderBottomStyle !== 'none' && parseFloat(s.borderBottomWidth) > 0);
                    }).map(a => ({text: a.innerText.trim().slice(0, 40), href: a.getAttribute('href'),
                                   td: getComputedStyle(a).textDecorationLine,
                                   bb: getComputedStyle(a).borderBottomWidth + '/' + getComputedStyle(a).borderBottomStyle}));
                    // body-copy font sizes: every p/li/td/th in main
                    const small = [...document.querySelectorAll('main p, main li, main td, main th, main label, main input, main textarea, main legend')]
                        .filter(el => parseFloat(getComputedStyle(el).fontSize) < 18)
                        .map(el => ({tag: el.tagName, cls: (el.className.baseVal !== undefined ? '' : el.className || '').toString().slice(0, 30),
                                     px: getComputedStyle(el).fontSize, text: (el.innerText || el.value || '').trim().slice(0, 40)}));
                    const h2 = document.querySelector('main h2');
                    const h3 = document.querySelector('main h3');
                    const h2after = h2 ? getComputedStyle(h2, '::after') : null;
                    const header = document.querySelector('header');
                    const footer = document.querySelector('footer');
                    return {
                        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                        h1: h1s.length,
                        h1text: h1s.length ? h1s[0].innerText.trim() : null,
                        btn1: b1 ? rect(b1) : null,
                        btn2: b2 ? rect(b2) : null,
                        vh: window.innerHeight,
                        underline_violations: under,
                        underline_total: links.length,
                        small_text: small.slice(0, 10),
                        small_count: small.length,
                        h2color: h2 ? cs(h2, 'color') : null,
                        h3color: h3 ? cs(h3, 'color') : null,
                        h2bar: h2after ? {w: h2after.width, h: h2after.height, bg: h2after.backgroundColor} : null,
                        header_dashes: (header.innerText.match(/[\\u2014\\u2013]/g) || []).length,
                        footer_dashes: (footer.innerText.match(/[\\u2014\\u2013]/g) || []).length,
                        header_text: header.innerText.replace(/\\n/g, ' | ').slice(0, 200),
                        footer_text: footer.innerText.replace(/\\n/g, ' | ').slice(0, 300),
                        main_text: document.querySelector('main').innerText,
                        body_imgs: [...document.querySelectorAll('img.body-img')].map(im => ({
                            src: im.getAttribute('src'), alt: im.getAttribute('alt'),
                            w: im.getAttribute('width'), h: im.getAttribute('height'),
                            loading: im.getAttribute('loading'), decoding: im.getAttribute('decoding'),
                            sticky: !!im.closest('figure.sticky'),
                            cls: im.className, rect: (() => { const b = im.getBoundingClientRect(); return {w: b.width, h: b.height, x: b.x}; })()
                        })),
                        grid_sections: document.querySelectorAll('.h2-section.with-image').length,
                        hrefs: links.map(a => a.getAttribute('href')),
                        footer_links: [...document.querySelectorAll('footer a')].map(a => a.getAttribute('href')),
                        contact_form: !!document.querySelector('.contact-form form'),
                        contact_fields: [...document.querySelectorAll('.contact-form input, .contact-form textarea, .contact-form button')].map(el => el.id || el.name || el.type || el.tagName),
                        errors: [],
                    };
                }""")
                d["errors"] = errors
                d["failed"] = [f for f in failed if "google.com/maps" not in f and "maps.googleapis" not in f]
                d["failed_external"] = [f for f in failed if "google.com/maps" in f or "maps.googleapis" in f]
                # paren-path gate on main text
                d["paren_paths"] = PAREN_PATH_RE.findall(d.pop("main_text"))
                d["btn2_visible_scroll0"] = bool(d["btn2"] and d["btn2"]["bottom"] <= d["vh"] + 0.5)
                d["btn_equal"] = bool(d["btn1"] and d["btn2"] and abs(d["btn1"]["h"] - d["btn2"]["h"]) < 0.5 and abs(d["btn1"]["w"] - d["btn2"]["w"]) < 1.0)
                if label == "desktop":
                    all_hrefs[route] = d["hrefs"]
                    if route in ("/", "/emergency-water-extraction", "/locations/cottonwood-heights-ut"):
                        page.screenshot(path=os.path.join(OUT, f"{slug(route)}-{label}.png"))
                if label == "m390" and route in ("/", "/emergency-water-extraction", "/locations/cottonwood-heights-ut"):
                    page.screenshot(path=os.path.join(OUT, f"{slug(route)}-{label}.png"))
                r[label] = d
                ctx.close()
            results[route] = r
finally:
    srv.terminate()

# cross-page link analysis: orphans + self-links
route_set = set(ROUTES)
def norm(h):
    if not h:
        return None
    h = h.split("#")[0].split("?")[0]
    if not h or h.startswith("tel:") or h.startswith("mailto:") or h.startswith("http"):
        return None
    if not h.startswith("/"):
        return None
    h = h.rstrip("/") or "/"
    return h
self_links, orphans, total_internal = [], [], 0
for route, hrefs in all_hrefs.items():
    for h in hrefs:
        n = norm(h)
        if n is None:
            continue
        total_internal += 1
        if n == route:
            self_links.append((route, h))
        elif n not in route_set:
            orphans.append((route, h))

json.dump({"per_route": results}, open(os.path.join(ROOT, "qa", "verify-design-css-raw.json"), "w"), indent=1)
summary = {
    "routes": len(ROUTES),
    "overflow_nonzero": {rt: {k: v["overflow"] for k, v in r.items() if isinstance(v, dict) and v.get("overflow")} for rt, r in results.items()},
    "h1_bad": {rt: r["desktop"]["h1"] for rt, r in results.items() if r["desktop"].get("h1") != 1},
    "btn2_not_visible_320": {rt: r["m320"]["btn2"] for rt, r in results.items() if not r["m320"].get("btn2_visible_scroll0")},
    "btn2_not_visible_390": {rt: r["m390"]["btn2"] for rt, r in results.items() if not r["m390"].get("btn2_visible_scroll0")},
    "btn_not_equal": {rt: {k: r[k].get("btn_equal") for k in ("desktop", "m390", "m320")} for rt, r in results.items() if not all(r[k].get("btn_equal") for k in ("desktop", "m390", "m320"))},
    "underline_violations": {rt: {k: v["underline_violations"] for k, v in r.items() if isinstance(v, dict) and v.get("underline_violations")} for rt, r in results.items()},
    "underline_total_links_checked": sum(r["desktop"]["underline_total"] for r in results.values()),
    "small_text": {rt: {k: v["small_text"] for k, v in r.items() if isinstance(v, dict) and v.get("small_count")} for rt, r in results.items()},
    "header_dashes": {rt: r["desktop"]["header_dashes"] for rt, r in results.items() if r["desktop"].get("header_dashes")},
    "footer_dashes": {rt: r["desktop"]["footer_dashes"] for rt, r in results.items() if r["desktop"].get("footer_dashes")},
    "paren_paths": {rt: r["desktop"]["paren_paths"] for rt, r in results.items() if r["desktop"].get("paren_paths")},
    "h2_colors": sorted({r["desktop"]["h2color"] for r in results.values() if r["desktop"].get("h2color")}),
    "h3_colors": sorted({r["desktop"]["h3color"] for r in results.values() if r["desktop"].get("h3color")}),
    "h2_bar_sample": results["/emergency-water-extraction"]["desktop"]["h2bar"],
    "body_imgs_total": sum(len(r["desktop"]["body_imgs"]) for r in results.values()),
    "grid_sections_total": sum(r["desktop"]["grid_sections"] for r in results.values()),
    "contact_form": results["/contact"]["desktop"]["contact_form"],
    "contact_fields": results["/contact"]["desktop"]["contact_fields"],
    "footer_links_per_page": sorted({len(r["desktop"]["footer_links"]) for r in results.values() if r["desktop"].get("footer_links") is not None}),
    "console_errors": {rt: {k: v["errors"] for k, v in r.items() if isinstance(v, dict) and v.get("errors")} for rt, r in results.items()},
    "failed_requests_local": {rt: {k: v["failed"] for k, v in r.items() if isinstance(v, dict) and v.get("failed")} for rt, r in results.items()},
    "total_internal_links": total_internal,
    "self_links": self_links,
    "orphans": orphans,
}
json.dump({"summary": summary, "per_route": results}, open(os.path.join(ROOT, "qa", "verify-design-css.json"), "w"), indent=1)
print(json.dumps(summary, indent=1)[:6000])
print("... full JSON in qa/verify-design-css.json")
