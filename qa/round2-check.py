"""Midvale QA Round 1 — fresh, independent checks on the LOCAL export.
Serves out/ at 127.0.0.1:8322 (see /tmp/midvale-serve.py).
Checks per route: status 200, H1 count/text/visibility, canonical, title,
FAQ (home), internal links resolve, overflow at 1440/390/320, computed
body font-size, hero buttons equal size, screenshots desktop full + mobile top.
Writes qa/round2/findings.json + qa/round2/*.png
"""
import json, os, re, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8322"
OUT = "/home/hatch/workspace/midvale-water-damage/qa/round2"
os.makedirs(OUT, exist_ok=True)

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

results = {}
fails = []

def check(cond, route, msg):
    if not cond:
        fails.append(f"{route}: {msg}")

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for route in ROUTES:
        slug = route.strip("/").replace("/", "_") or "home"
        r = {}
        # desktop
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        resp = page.goto(BASE + route, wait_until="networkidle")
        r["status"] = resp.status if resp else None
        check(r["status"] == 200, route, f"status {r['status']}")
        r["h1_count"] = page.locator("h1").count()
        check(r["h1_count"] == 1, route, f"H1 count {r['h1_count']}")
        r["h1_text"] = page.locator("h1").first.inner_text() if r["h1_count"] else ""
        check(r["h1_text"] == EXPECTED_H1[route], route, f"H1 text mismatch: {r['h1_text']!r}")
        r["h1_visible"] = page.locator("h1").first.is_visible() if r["h1_count"] else False
        check(r["h1_visible"], route, "H1 not visible")
        box = page.locator("h1").first.bounding_box() if r["h1_count"] else None
        r["h1_box"] = box
        check(bool(box and box["height"] > 10 and box["width"] > 50), route, "H1 box too small/blank")
        r["title"] = page.title()
        r["canonical"] = page.locator('link[rel="canonical"]').get_attribute("href")
        exp_canon = ("http://localhost:3000/" if route == "/" else "http://localhost:3000" + route)
        check(r["canonical"] == exp_canon, route, f"canonical {r['canonical']} != {exp_canon}")
        r["h2_count"] = page.locator("h2").count()
        r["h3_count"] = page.locator("h3").count()
        # overflow desktop
        r["overflow_1440"] = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(r["overflow_1440"] == 0, route, f"overflow 1440: {r['overflow_1440']}px")
        # computed body font size
        r["body_font_px"] = page.evaluate("getComputedStyle(document.body).fontSize")
        check(r["body_font_px"] == "18px", route, f"body font {r['body_font_px']}")
        # tel links all correct
        tels = page.eval_on_selector_all('a[href^="tel:"]', "els => els.map(e => e.getAttribute('href'))")
        r["tel_links"] = sorted(set(tels))
        check(all(t == "tel:+13853373560" for t in tels) and len(tels) > 0, route, f"tel links wrong: {tels}")
        # internal links
        hrefs = page.eval_on_selector_all('a[href^="/"]', "els => els.map(e => e.getAttribute('href'))")
        r["internal_links"] = sorted(set(hrefs))
        # self-links in body copy (exclude header/footer/breadcrumb/sticky): check main a[href] == route
        self_links = page.eval_on_selector_all('main a[href]', "els => els.map(e => e.getAttribute('href'))")
        r["main_self_links"] = [h for h in self_links if h == route or h == route + "/"]
        check(len(r["main_self_links"]) == 0, route, f"self-links in main: {r['main_self_links']}")
        # screenshots desktop full
        page.screenshot(path=f"{OUT}/{slug}-desktop-full.png", full_page=True)
        # hero buttons equal (home + service pages have .hero-buttons)
        btns = page.locator(".hero-buttons").first.locator(".btn")
        if btns.count() == 2:
            b1 = btns.nth(0).bounding_box(); b2 = btns.nth(1).bounding_box()
            r["btn1_box"] = b1; r["btn2_box"] = b2
            if b1 and b2:
                check(abs(b1["width"] - b2["width"]) < 2 and abs(b1["height"] - b2["height"]) < 2,
                      route, f"buttons unequal: {b1} vs {b2}")
                r["btn1_text"] = btns.nth(0).inner_text()
                check(r["btn1_text"] == "(385) 337-3560", route, f"button1 text {r['btn1_text']!r}")
                r["btn2_text"] = btns.nth(1).inner_text()
                check(r["btn2_text"] == "Request Emergency Help", route, f"button2 text {r['btn2_text']!r}")
        ctx.close()
        # mobile 390
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto(BASE + route, wait_until="networkidle")
        r["overflow_390"] = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(r["overflow_390"] == 0, route, f"overflow 390: {r['overflow_390']}px")
        r["sticky_visible_390"] = page.locator(".sticky-bar").is_visible()
        check(r["sticky_visible_390"], route, "sticky bar not visible at 390")
        r["header_phone_visible_390"] = page.locator(".header-phone").is_visible()
        check(r["header_phone_visible_390"], route, "header phone not visible at 390")
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
        print(route, "OK" if route not in " ".join(fails) else "CHECK-FAILS", flush=True)
    browser.close()

# homepage extras (single desktop context)
with sync_playwright() as pw:
    browser = pw.chromium.launch()
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
    extra["table_rows"] = page.locator("table tbody tr").count()
    check(extra["table_rows"] == 3, "/", f"category table rows {extra['table_rows']}")
    extra["h2_count_home"] = page.locator("main h2").count()
    check(extra["h2_count_home"] == 12, "/", f"home H2 count {extra['h2_count_home']}")
    extra["h3_count_home"] = page.locator("main h3").count()
    check(extra["h3_count_home"] == 24, "/", f"home H3 count {extra['h3_count_home']}")
    # JSON-LD parse
    import json as _j
    lds = page.eval_on_selector_all('script[type="application/ld+json"]', "els => els.map(e => e.textContent)")
    extra["jsonld_blocks"] = len(lds)
    parsed = []
    for t in lds:
        try: parsed.append(_j.loads(t))
        except Exception as e: fails.append(f"/: JSON-LD parse error {e}")
    extra["jsonld_types"] = [p.get("@type") for p in parsed]
    # FAQ schema == visible FAQ
    faq_schema = next((p for p in parsed if p.get("@type") == "FAQPage"), None)
    if faq_schema:
        vis = page.eval_on_selector_all("#faq .faq-item", "els => els.map(e => ({q: e.querySelector('h3').innerText, a: e.querySelector('p').innerText}))")
        sch = [(q["name"], q["acceptedAnswer"]["text"]) for q in faq_schema["mainEntity"]]
        check([(v["q"], v["a"]) for v in vis] == sch, "/", "FAQ schema != visible FAQ")
    # footer map present on home, absent on area pages
    extra["footer_map_home"] = page.locator(".footer-map iframe").count()
    check(extra["footer_map_home"] == 1, "/", "footer map missing on home")
    # console errors
    browser.close()
    results["/_extras"] = extra

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(BASE + "/locations/magna-ut", wait_until="networkidle")
    n = page.locator(".footer-map iframe").count()
    check(n == 0, "/locations/magna-ut", f"footer map present on area page ({n})")
    browser.close()

# link resolution: every internal href must map to an existing out file
import os as _os
outdir = "/home/hatch/workspace/midvale-water-damage/out"
all_hrefs = set()
for route, r in results.items():
    if route.startswith("/_"): continue
    for h in r.get("internal_links", []):
        all_hrefs.add(h.split("#")[0])
missing = []
for h in sorted(all_hrefs):
    if h in ("", "/"): continue
    fp = _os.path.join(outdir, h.lstrip("/") + ".html")
    if h.startswith("/locations/"):
        fp = _os.path.join(outdir, h.lstrip("/"), "index.html")
        fp2 = _os.path.join(outdir, h.lstrip("/") + ".html")
        if not (_os.path.exists(fp) or _os.path.exists(fp2)): missing.append(h)
    elif not _os.path.exists(fp):
        missing.append(h)
check(len(missing) == 0, "ALL", f"internal links with no file: {missing}")

report = {"routes_checked": len(ROUTES), "fails": fails, "fail_count": len(fails), "results": results,
          "internal_hrefs_total": len(all_hrefs), "internal_hrefs_missing": missing}
json.dump(report, open(f"{OUT}/findings.json", "w"), indent=2)
print(f"\nROUND1 DONE: {len(ROUTES)} routes, FAILS={len(fails)}")
for f in fails: print(" FAIL:", f)
