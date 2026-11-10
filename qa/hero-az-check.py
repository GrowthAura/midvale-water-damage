"""Midvale HERO + A-to-Z round — fresh browser checks on the LOCAL export.
Serves out/ at 127.0.0.1:8323. Checks per route: status 200, H1 1/visible/
verbatim, photo hero present with loaded unique image, intro INSIDE hero
(verbatim), og:image == own hero, canonical, buttons equal + both fully
visible at mobile first paint (not covered by sticky bar), overflow
1440/390/320, body 18px, card images loaded + unique, perf (FCP/CLS/weight).
Writes qa/hero-az/findings.json + qa/hero-az/*.png
"""
import json, os, subprocess, sys, time, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial

BASE_DIR = "/home/hatch/workspace/midvale-water-damage"
OUT = os.path.join(BASE_DIR, "qa", "hero-az")
os.makedirs(OUT, exist_ok=True)
PORT = 8323
BASE = f"http://127.0.0.1:{PORT}"

ROUTES = ["/", "/emergency-water-extraction", "/basement-flooding-cleanup",
 "/window-well-flooding", "/burst-pipe-water-damage", "/sewage-backup-cleanup",
 "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage",
 "/ceiling-water-damage", "/crawl-space-water-damage",
 "/hardwood-floor-cabinet-drying", "/condo-apartment-water-damage",
 "/commercial-water-damage", "/storm-flood-damage", "/mold-remediation",
 "/water-leak-detection", "/water-damage-repair",
 "/midvale-water-sewer-emergency-contacts",
 "/locations/cottonwood-heights-ut", "/locations/south-salt-lake-ut",
 "/locations/magna-ut"]

EXPECTED_H1 = {
 "/": "24/7 Water Damage Restoration in Midvale, UT 84047",
 "/emergency-water-extraction": "Emergency Water Extraction in Midvale, UT",
 "/basement-flooding-cleanup": "Basement Flooding Cleanup in Midvale, UT",
 "/window-well-flooding": "Window Well Flooding in Midvale, UT",
 "/burst-pipe-water-damage": "Burst Pipe Water Damage in Midvale, UT",
 "/sewage-backup-cleanup": "Sewage Backup Cleanup in Midvale, UT",
 "/water-heater-leak-cleanup": "Water Heater Leak Cleanup in Midvale, UT",
 "/swamp-cooler-leak-water-damage": "Swamp Cooler Leak Water Damage in Midvale, UT",
 "/ceiling-water-damage": "Ceiling Water Damage in Midvale, UT",
 "/crawl-space-water-damage": "Crawl Space Water Damage in Midvale, UT",
 "/hardwood-floor-cabinet-drying": "Hardwood Floor & Cabinet Drying in Midvale, UT",
 "/condo-apartment-water-damage": "Condo & Apartment Water Damage in Midvale, UT",
 "/commercial-water-damage": "Commercial Water Damage in Midvale, UT",
 "/storm-flood-damage": "Storm Water Damage in Midvale, UT",
 "/mold-remediation": "Mold Remediation in Midvale, UT",
 "/water-leak-detection": "Water Leak Detection in Midvale, UT",
 "/water-damage-repair": "Water Damage Repair in Midvale, UT",
 "/midvale-water-sewer-emergency-contacts": "Midvale Water & Sewer Emergency Contacts",
 "/locations/cottonwood-heights-ut": "Water Damage Restoration Cottonwood Heights, UT",
 "/locations/south-salt-lake-ut": "Water Damage Restoration South Salt Lake, UT",
 "/locations/magna-ut": "Water Damage Restoration Magna, UT",
}

HERO_SRC = {
 "/": "/images/heroes/home.webp",
 "/emergency-water-extraction": "/images/heroes/emergency-water-extraction.webp",
 "/basement-flooding-cleanup": "/images/heroes/basement-flooding-cleanup.webp",
 "/window-well-flooding": "/images/heroes/window-well-flooding.webp",
 "/burst-pipe-water-damage": "/images/heroes/burst-pipe-water-damage.webp",
 "/sewage-backup-cleanup": "/images/heroes/sewage-backup-cleanup.webp",
 "/water-heater-leak-cleanup": "/images/heroes/water-heater-leak-cleanup.webp",
 "/swamp-cooler-leak-water-damage": "/images/heroes/swamp-cooler-leak-water-damage.webp",
 "/ceiling-water-damage": "/images/heroes/ceiling-water-damage.webp",
 "/crawl-space-water-damage": "/images/heroes/crawl-space-water-damage.webp",
 "/hardwood-floor-cabinet-drying": "/images/heroes/hardwood-floor-cabinet-drying.webp",
 "/condo-apartment-water-damage": "/images/heroes/condo-apartment-water-damage.webp",
 "/commercial-water-damage": "/images/heroes/commercial-water-damage.webp",
 "/storm-flood-damage": "/images/heroes/storm-flood-damage.webp",
 "/mold-remediation": "/images/heroes/mold-remediation.webp",
 "/water-leak-detection": "/images/heroes/water-leak-detection.webp",
 "/water-damage-repair": "/images/heroes/water-damage-repair.webp",
 "/midvale-water-sewer-emergency-contacts": "/images/heroes/midvale-water-sewer-emergency-contacts.webp",
 "/locations/cottonwood-heights-ut": "/images/heroes/cottonwood-heights-ut.webp",
 "/locations/south-salt-lake-ut": "/images/heroes/south-salt-lake-ut.webp",
 "/locations/magna-ut": "/images/heroes/magna-ut.webp",
}

# verbatim hero intros (must appear INSIDE .hero-photo)
HERO_INTRO = {
 "/": "Burst pipe, flooded basement or sewage coming up the floor drain?",
 "/emergency-water-extraction": "Truck-mounted and submersible pumps remove standing water fast",
 "/basement-flooding-cleanup": "Finished basements in Midvale ramblers and split-levels hold water",
 "/window-well-flooding": "When a window well fills with snowmelt or storm water",
 "/burst-pipe-water-damage": "A split line inside a wall can soak insulation, drywall and floors",
 "/sewage-backup-cleanup": "Sewage is Category 3 water.",
 "/water-heater-leak-cleanup": "Hard water wears out tanks, valves and supply lines.",
 "/swamp-cooler-leak-water-damage": "A stuck float valve or clogged drain pan can soak a roof deck",
 "/ceiling-water-damage": "Upstairs bathrooms, ice dams and roof leaks show up as stains",
 "/crawl-space-water-damage": "Older homes near Historic Main Street often sit over dirt crawl spaces.",
 "/hardwood-floor-cabinet-drying": "Floor drying mats and cavity drying can save cupped hardwood",
 "/condo-apartment-water-damage": "Water moves between stacked units fast.",
 "/commercial-water-damage": "Offices, shops and restaurants along Fort Union Blvd",
 "/storm-flood-damage": "Summer storms and runoff can push dirty water into garages",
 "/mold-remediation": "If a leak sat too long, we contain the area",
 "/water-leak-detection": "Thermal imaging and moisture meters find hidden water",
 "/water-damage-repair": "Once everything is dry, we put drywall, texture, paint, flooring",
 "/midvale-water-sewer-emergency-contacts": "For sewer backups, the Midvale Water & Sewer Emergency Contacts page lists",
 "/locations/cottonwood-heights-ut": "Cottonwood Heights, UT 84121:",
 "/locations/south-salt-lake-ut": "South Salt Lake, UT 84115:",
 "/locations/magna-ut": "Magna, UT 84044:",
}

from playwright.sync_api import sync_playwright

results = {}
fails = []

def check(cond, route, msg):
    if not cond:
        fails.append(f"{route}: {msg}")

def serve():
    # Static export serves extensionless routes (Vercel behaviour): map
    # /slug -> /slug.html, /locations/x -> /locations/x.html (or index.html).
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            path = self.path.split("?")[0].split("#")[0]
            if path != "/" and not os.path.splitext(path)[1]:
                cand = os.path.join(self.directory, path.lstrip("/") + ".html")
                if os.path.exists(cand):
                    self.path = path + ".html"
                else:
                    idx = os.path.join(self.directory, path.lstrip("/"), "index.html")
                    if os.path.exists(idx):
                        self.path = path + "/index.html"
            return super().do_GET()
    handler = partial(Handler, directory=os.path.join(BASE_DIR, "out"))
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

CLS_SNIPPET = """
window.__cls = 0;
new PerformanceObserver((list) => {
  for (const e of list.getEntries()) { if (!e.hadRecentInput) window.__cls += e.value; }
}).observe({type: 'layout-shift', buffered: true});
"""

httpd = serve()
time.sleep(1)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    all_img_srcs = []
    for route in ROUTES:
        slug = route.strip("/").replace("/", "_") or "home"
        r = {}
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.add_init_script(CLS_SNIPPET)
        resp = page.goto(BASE + route, wait_until="networkidle")
        r["status"] = resp.status if resp else None
        check(r["status"] == 200, route, f"status {r['status']}")
        r["h1_count"] = page.locator("h1").count()
        check(r["h1_count"] == 1, route, f"H1 count {r['h1_count']}")
        r["h1_text"] = page.locator("h1").first.inner_text() if r["h1_count"] else ""
        check(r["h1_text"] == EXPECTED_H1[route], route, f"H1 text mismatch: {r['h1_text']!r}")
        check(page.locator("h1").first.is_visible(), route, "H1 not visible")
        # --- HERO ---
        r["hero_sections"] = page.locator("section.hero-photo").count()
        check(r["hero_sections"] == 1, route, f"hero-photo sections {r['hero_sections']}")
        hero = page.locator("section.hero-photo").first
        r["hero_img_src"] = hero.locator("img.hero-img").get_attribute("src") if hero.locator("img.hero-img").count() else None
        check(r["hero_img_src"] == HERO_SRC[route], route, f"hero img {r['hero_img_src']} != {HERO_SRC[route]}")
        if hero.locator("img.hero-img").count():
            nat = page.evaluate("""() => { const i = document.querySelector('img.hero-img');
                return {complete: i.complete, naturalWidth: i.naturalWidth, naturalHeight: i.naturalHeight}; }""")
            r["hero_img_loaded"] = nat
            check(nat["complete"] and nat["naturalWidth"] > 0, route, f"hero img not loaded: {nat}")
            check(nat["naturalWidth"] >= 1200, route, f"hero img too narrow: {nat['naturalWidth']}")
        # intro INSIDE hero, verbatim start
        hero_text = hero.inner_text() if r["hero_sections"] else ""
        r["hero_intro_present"] = HERO_INTRO[route] in hero_text
        check(r["hero_intro_present"], route, "hero intro missing/not verbatim inside hero")
        # h1 + intro + buttons order in DOM inside hero
        order = page.evaluate("""() => {
            const h = document.querySelector('section.hero-photo');
            if (!h) return [];
            return [...h.querySelectorAll('h1, p.intro, .hero-buttons, .hero-trust')].map(e => e.tagName + '.' + (e.className||''));
        }""")
        r["hero_dom_order"] = order
        # og:image == own hero (evaluate: None if missing, no 30s wait)
        r["og_image"] = page.evaluate("() => document.querySelector('meta[property=\"og:image\"]')?.content ?? null")
        check(r["og_image"] == "http://localhost:3000" + HERO_SRC[route], route, f"og:image {r['og_image']}")
        # canonical
        r["canonical"] = page.evaluate("() => document.querySelector('link[rel=\"canonical\"]')?.href ?? null")
        exp_canon = "http://localhost:3000/" if route == "/" else "http://localhost:3000" + route
        check(r["canonical"] == exp_canon, route, f"canonical {r['canonical']} != {exp_canon}")
        # preload link for hero
        r["preload_hero"] = page.locator('link[rel="preload"][as="image"]').count()
        check(r["preload_hero"] >= 1, route, "no preload for hero image")
        # buttons equal
        btns = page.locator(".hero-buttons").first.locator(".btn")
        if btns.count() == 2:
            b1 = btns.nth(0).bounding_box(); b2 = btns.nth(1).bounding_box()
            r["btn1_box"] = b1; r["btn2_box"] = b2
            if b1 and b2:
                check(abs(b1["width"] - b2["width"]) < 2 and abs(b1["height"] - b2["height"]) < 2,
                      route, f"buttons unequal: {b1} vs {b2}")
            check(btns.nth(0).inner_text() == "(385) 337-3560", route, "button1 text wrong")
            check(btns.nth(1).inner_text() == "Request Emergency Help", route, "button2 text wrong")
        else:
            check(False, route, f"hero buttons count {btns.count()}")
        # trust chips in hero
        r["hero_trust"] = hero.locator(".hero-trust").count()
        check(r["hero_trust"] == 1, route, "hero trust chips missing")
        # overflow + font
        r["overflow_1440"] = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(r["overflow_1440"] == 0, route, f"overflow 1440: {r['overflow_1440']}px")
        r["body_font_px"] = page.evaluate("getComputedStyle(document.body).fontSize")
        check(r["body_font_px"] == "18px", route, f"body font {r['body_font_px']}")
        # all imgs loaded + collect srcs — scroll through first so lazy
        # below-fold images actually load. NOTE: html has scroll-behavior:
        # smooth, so stepped scrollTo() never reaches the bottom — disable
        # smooth scrolling first (run-2 bug: 3 area cards never loaded).
        page.evaluate("""async () => {
            document.documentElement.style.scrollBehavior = 'auto';
            for (let y = 0; y <= document.body.scrollHeight; y += 600) {
                window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80));
            }
            window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 400));
        }""")
        page.wait_for_timeout(1500)
        imgs = page.eval_on_selector_all("img", "els => els.map(e => ({src: e.getAttribute('src'), ok: e.complete && e.naturalWidth > 0, w: e.naturalWidth, h: e.naturalHeight}))")
        r["imgs"] = imgs
        for im in imgs:
            check(im["ok"], route, f"img not loaded: {im['src']}")
            all_img_srcs.append(im["src"])
        # h1 computed colour must be white (contrast on dark hero)
        r["h1_color"] = page.evaluate("getComputedStyle(document.querySelector('section.hero-photo h1')).color")
        check(r["h1_color"] == "rgb(255, 255, 255)", route, f"h1 color {r['h1_color']}")
        # perf
        r["fcp_ms"] = page.evaluate("""() => { const e = performance.getEntriesByType('paint').find(x => x.name === 'first-contentful-paint'); return e ? Math.round(e.startTime) : null; }""")
        r["cls"] = page.evaluate("window.__cls")
        check(r["cls"] is not None and r["cls"] < 0.05, route, f"CLS {r['cls']}")
        r["page_kb"] = page.evaluate("() => Math.round(performance.getEntriesByType('resource').reduce((a, e) => a + (e.transferSize || 0), 0) / 1024)")
        page.screenshot(path=f"{OUT}/{slug}-desktop-full.png", full_page=True)
        ctx.close()
        # mobile 390 — first paint, no scroll
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto(BASE + route, wait_until="networkidle")
        r["overflow_390"] = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(r["overflow_390"] == 0, route, f"overflow 390: {r['overflow_390']}px")
        # both HERO buttons fully visible above the sticky bar (bar ~56px tall
        # at bottom) — scope to the hero only: run 1 matched every .btn on the
        # page (hero + body + final CTA) and failed on the below-fold ones.
        bb = page.eval_on_selector_all("section.hero-photo .hero-buttons .btn", """els => els.map(e => { const b = e.getBoundingClientRect();
            const cs = getComputedStyle(e); return {top: Math.round(b.top), bottom: Math.round(b.bottom),
            visible: cs.display !== 'none' && cs.visibility !== 'hidden' && b.height > 40}; })""")
        r["mobile_buttons"] = bb
        check(len(bb) == 2 and all(b["visible"] and b["top"] >= 0 and b["bottom"] <= 844 - 56 for b in bb),
              route, f"mobile buttons not fully visible at first paint: {bb}")
        # h1 visible at first paint on mobile too
        h1b = page.locator("h1").first.bounding_box()
        r["mobile_h1_top"] = h1b["y"] if h1b else None
        check(h1b is not None and h1b["y"] < 844, route, "mobile h1 below fold")
        page.screenshot(path=f"{OUT}/{slug}-mobile-top.png")
        ctx.close()
        # 320 width
        ctx = browser.new_context(viewport={"width": 320, "height": 700})
        page = ctx.new_page()
        page.goto(BASE + route, wait_until="networkidle")
        r["overflow_320"] = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(r["overflow_320"] == 0, route, f"overflow 320: {r['overflow_320']}px")
        ctx.close()
        results[route] = r
        print(route, "done", flush=True)
    # homepage extras
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(BASE + "/", wait_until="networkidle")
    extra = {}
    extra["faq_h3"] = page.locator("#faq h3").count()
    check(extra["faq_h3"] == 6, "/", f"FAQ H3 count {extra['faq_h3']}")
    extra["service_cards"] = page.locator("#services .card").count()
    check(extra["service_cards"] == 16, "/", f"service cards {extra['service_cards']}")
    extra["area_cards"] = page.locator("#areas .card").count()
    check(extra["area_cards"] == 3, "/", f"area cards {extra['area_cards']}")
    extra["service_card_imgs"] = page.locator("#services .card img.card-img").count()
    check(extra["service_card_imgs"] == 16, "/", f"service card photos {extra['service_card_imgs']}")
    extra["area_card_imgs"] = page.locator("#areas .card img.card-img").count()
    check(extra["area_card_imgs"] == 3, "/", f"area card photos {extra['area_card_imgs']}")
    extra["h2_count_home"] = page.locator("main h2").count()
    check(extra["h2_count_home"] == 12, "/", f"home H2 count {extra['h2_count_home']}")
    extra["h3_count_home"] = page.locator("main h3").count()
    check(extra["h3_count_home"] == 24, "/", f"home H3 count {extra['h3_count_home']}")
    extra["footer_map_home"] = page.locator(".footer-map iframe").count()
    check(extra["footer_map_home"] == 1, "/", "footer map missing on home")
    results["/_extras"] = extra
    # area page: no footer map
    page.goto(BASE + "/locations/magna-ut", wait_until="networkidle")
    check(page.locator(".footer-map iframe").count() == 0, "/locations/magna-ut", "footer map present on area page")
    browser.close()

# image uniqueness site-wide (hero + card srcs must never repeat)
from collections import Counter
c = Counter(all_img_srcs)
dups = {k: v for k, v in c.items() if v > 1}
check(len(dups) == 0, "ALL", f"repeated image srcs across pages: {dups}")
# expected: 21 heroes (1/page) + 19 cards on home = 40 unique image uses
check(len(set(all_img_srcs)) == 40, "ALL", f"unique image srcs {len(set(all_img_srcs))} != 40")

report = {"routes_checked": len(ROUTES), "fails": fails, "fail_count": len(fails),
          "results": results, "unique_image_srcs": len(set(all_img_srcs)), "dup_srcs": dups}
json.dump(report, open(f"{OUT}/findings.json", "w"), indent=2)
print(f"\nHERO-AZ DONE: {len(ROUTES)} routes, FAILS={len(fails)}")
for f in fails:
    print(" FAIL:", f)
httpd.shutdown()
