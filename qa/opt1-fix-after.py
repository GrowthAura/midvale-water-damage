#!/usr/bin/env python3
"""F4 AFTER verification — Midvale Cycle 1 UI/UX fix.
Runs against the FRESH out/ (post-fix export) served on port 8401.
Checks: ids #breadcrumb/#hero-image/#service/#howto-N 31/31, hero attrs
1600x1066, logo 48px @1440/390/320, radio labels 48px, card CTA 19/19
(anchor text verbatim), card grid 4 cols rows 4/4/4/4 @1440, Button 2
31/31 @320/@390, overflow 0, console 0, form 6 fields + verbatim submit.
Screenshots to qa/opt1-fix-uiux/after/.
Usage: python3 qa/opt1-fix-after.py
"""
import json, os, re
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8401/midvale-water-damage"
ROUTES = [
    "/", "/about", "/contact", "/emergency-water-extraction",
    "/basement-flooding-cleanup", "/window-well-flooding",
    "/burst-pipe-water-damage", "/sewage-backup-cleanup",
    "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage",
    "/ceiling-water-damage", "/crawl-space-water-damage",
    "/hardwood-floor-cabinet-drying", "/condo-apartment-water-damage",
    "/commercial-water-damage", "/storm-flood-damage", "/mold-remediation",
    "/water-leak-detection", "/water-damage-repair",
    "/locations/cottonwood-heights-ut", "/locations/south-salt-lake-ut",
    "/locations/magna-ut", "/midvale-water-sewer-emergency-contacts",
    "/privacy-policy", "/terms-of-use", "/disclaimer",
    "/resources/frozen-pipes-midvale",
    "/resources/winterize-swamp-cooler-utah",
    "/resources/upstairs-unit-leak-who-pays-utah",
    "/resources/can-mold-grow-in-utah",
    "/resources/basement-flooding-spring-snowmelt-utah",
]
OUT = os.path.expanduser("~/workspace/midvale-water-damage/qa/opt1-fix-uiux/after")
os.makedirs(OUT, exist_ok=True)
WIDE = ["/", "/about", "/locations/cottonwood-heights-ut",
        "/locations/magna-ut", "/locations/south-salt-lake-ut"]
SERVICE_SHOTS = ["/emergency-water-extraction", "/basement-flooding-cleanup"]

res = {"routes": {}, "button2_320": {}, "logo": {}, "radio": {},
       "console_errors": [], "home": {}, "form": {}}

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    for r in ROUTES:
        errs = []
        pg.on("console", lambda m, e=errs: e.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e, errs=errs: errs.append(str(e)))
        pg.goto(BASE + ("" if r == "/" else r), wait_until="load")
        pg.wait_for_timeout(400)
        m = pg.evaluate("""() => {
          const img = document.querySelector('.hero-img');
          const r = img ? img.getBoundingClientRect() : null;
          const b2 = [...document.querySelectorAll('.hero-buttons .btn-help')][0];
          const b2r = b2 ? b2.getBoundingClientRect() : null;
          const ld = [...document.querySelectorAll('script[type="application/ld+json"]')]
            .map(s => s.textContent).join(' ');
          return {
            hero: r ? {w: Math.round(r.width), h: Math.round(r.height)} : null,
            b2bottom390: b2r ? Math.round(b2r.bottom * 10) / 10 : null,
            overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            imgW: img ? img.getAttribute('width') : null,
            imgH: img ? img.getAttribute('height') : null,
            idBreadcrumb: !!document.getElementById('breadcrumb'),
            idHeroImage: !!document.getElementById('hero-image'),
            idService: !!document.getElementById('service'),
            howtoIds: [...document.querySelectorAll('[id^="howto-"]')].map(e => e.id),
            ldHasBreadcrumbFrag: ld.includes('#breadcrumb'),
            ldHasHeroImageFrag: ld.includes('#hero-image'),
          };
        }""")
        if m["hero"]:
            scale = max(m["hero"]["w"] / 1600, m["hero"]["h"] / 1066)
            m["hero"]["visible_pct"] = round(m["hero"]["w"] / (1600 * scale) * 100, 1)
        res["routes"][r] = m
        if errs:
            res["console_errors"].append({"route": r, "errors": errs})
        if r in WIDE:
            slug = "home" if r == "/" else r.strip("/").replace("/", "-")
            pg.screenshot(path=f"{OUT}/{slug}-m390-hero.png")
    pg.close()

    pg = b.new_page(viewport={"width": 320, "height": 568})
    for r in ROUTES:
        pg.goto(BASE + ("" if r == "/" else r), wait_until="load")
        pg.wait_for_timeout(300)
        res["button2_320"][r] = pg.evaluate("""() => {
          const b = [...document.querySelectorAll('.hero-buttons .btn-help')][0];
          return b ? Math.round(b.getBoundingClientRect().bottom * 10) / 10 : null;
        }""")
        if r == "/":
            res["logo"]["320"] = pg.evaluate(
                "() => { const a=document.querySelector('a.brand'); const r=a.getBoundingClientRect(); return {w:Math.round(r.width),h:Math.round(r.height)}; }")
    pg.close()

    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE, wait_until="load")
    pg.wait_for_timeout(500)
    res["logo"]["1440"] = pg.evaluate(
        "() => { const a=document.querySelector('a.brand'); const r=a.getBoundingClientRect(); return {w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10}; }")
    res["home"] = pg.evaluate("""() => {
      const ctas = [...document.querySelectorAll('.card-cta')].map(e => ({
        text: e.textContent.replace(/\\s+/g, ' ').trim(),
        cls: getComputedStyle(e),
      })).map(c => ({
        text: c.text, color: c.cls.color, fontWeight: c.cls.fontWeight,
        fontSize: c.cls.fontSize, display: c.cls.display,
      }));
      const grid = document.querySelector('#services .card-grid');
      const cards = [...document.querySelectorAll('#services .card')];
      const rows = {};
      cards.forEach(c => { const y = Math.round(c.getBoundingClientRect().top); rows[y] = (rows[y] || 0) + 1; });
      const locCards = [...document.querySelectorAll('#areas .card')];
      const locRows = {};
      locCards.forEach(c => { const y = Math.round(c.getBoundingClientRect().top); locRows[y] = (locRows[y] || 0) + 1; });
      // CTA bottom-alignment within each row: max spread of CTA bottoms per row
      const ctaRows = {};
      [...document.querySelectorAll('#services .card .card-cta')].forEach(e => {
        const y = Math.round(e.closest('.card').getBoundingClientRect().top);
        (ctaRows[y] = ctaRows[y] || []).push(Math.round(e.getBoundingClientRect().bottom));
      });
      const spreads = Object.values(ctaRows).map(v => Math.max(...v) - Math.min(...v));
      return {
        ctaCount: ctas.length, ctas,
        gridCols: grid ? getComputedStyle(grid).gridTemplateColumns.split(' ').length : null,
        serviceRows: Object.values(rows), locRows: Object.values(locRows),
        ctaBottomSpreadPerRow: spreads,
        cardWidths: [...new Set(cards.map(c => Math.round(c.getBoundingClientRect().width)))],
      };
    }""")
    pg.screenshot(path=f"{OUT}/home-desktop-full.png", full_page=True)
    el = pg.query_selector("#services .card-grid")
    if el:
        el.screenshot(path=f"{OUT}/home-desktop-cards.png")
    pg.goto(BASE + "/contact", wait_until="load")
    pg.wait_for_timeout(400)
    res["radio"]["1440"] = pg.evaluate("""() => {
      return [...document.querySelectorAll('.radio-row label')].map(l => {
        const r = l.getBoundingClientRect(); return {text: l.textContent.trim(), w: Math.round(r.width), h: Math.round(r.height)};
      });
    }""")
    res["form"] = pg.evaluate("""() => {
      const labels = [...document.querySelectorAll('.contact-form label, .contact-form legend')]
        .map(e => e.textContent.trim());
      const submit = document.querySelector('.contact-form button[type="submit"]');
      return {labels, submit: submit ? submit.textContent.trim() : null};
    }""")
    form = pg.query_selector(".contact-form")
    if form:
        form.screenshot(path=f"{OUT}/contact-desktop-form.png")
    # service pages before/after comparison shots
    for r in SERVICE_SHOTS:
        slug = r.strip("/")
        pg.goto(BASE + r, wait_until="load")
        pg.wait_for_timeout(400)
        pg.screenshot(path=f"{OUT}/{slug}-desktop-full.png", full_page=True)
    pg2 = b.new_page(viewport={"width": 390, "height": 844})
    pg2.goto(BASE, wait_until="load")
    pg2.wait_for_timeout(400)
    res["logo"]["390"] = pg2.evaluate(
        "() => { const a=document.querySelector('a.brand'); const r=a.getBoundingClientRect(); return {w:Math.round(r.width),h:Math.round(r.height)}; }")
    pg2.screenshot(path=f"{OUT}/home-m390-full.png", full_page=True)
    el2 = pg2.query_selector("#services .card-grid")
    if el2:
        el2.screenshot(path=f"{OUT}/home-m390-cards.png")
    for r in SERVICE_SHOTS:
        slug = r.strip("/")
        pg2.goto(BASE + r, wait_until="load")
        pg2.wait_for_timeout(400)
        pg2.screenshot(path=f"{OUT}/{slug}-m390-full.png", full_page=True)
    pg2.close()
    b.close()

json.dump(res, open(os.path.expanduser(
    "~/workspace/midvale-water-damage/qa/opt1-fix-after.json"), "w"), indent=2)

R = res["routes"]
print("ids: breadcrumb %d/31  hero-image %d/31  service %d/19  howto pages %d/31" % (
    sum(1 for r in ROUTES if R[r]["idBreadcrumb"]),
    sum(1 for r in ROUTES if R[r]["idHeroImage"]),
    sum(1 for r in ROUTES if R[r]["idService"]),
    sum(1 for r in ROUTES if R[r]["howtoIds"])))
print("LD fragments: #breadcrumb %d/31  #hero-image %d/31" % (
    sum(1 for r in ROUTES if R[r]["ldHasBreadcrumbFrag"]),
    sum(1 for r in ROUTES if R[r]["ldHasHeroImageFrag"])))
print("hero attrs:", set((R[r]["imgW"], R[r]["imgH"]) for r in ROUTES))
print("hero visible %% @390: min %.1f max %.1f mean %.1f" % (
    min(R[r]["hero"]["visible_pct"] for r in ROUTES),
    max(R[r]["hero"]["visible_pct"] for r in ROUTES),
    sum(R[r]["hero"]["visible_pct"] for r in ROUTES) / 31))
print("Button2 worst @320: %.1f (fold 568)  @390: %.1f (fold 844)" % (
    max(v for v in res["button2_320"].values() if v),
    max(R[r]["b2bottom390"] for r in ROUTES)))
print("overflow>0:", [r for r in ROUTES if R[r]["overflow"] > 0])
print("console errors:", len(res["console_errors"]))
print("logo:", res["logo"])
print("radio:", res["radio"]["1440"])
print("home CTA count:", res["home"]["ctaCount"], "grid cols:", res["home"]["gridCols"],
      "service rows:", res["home"]["serviceRows"], "loc rows:", res["home"]["locRows"])
print("CTA bottom spread/row:", res["home"]["ctaBottomSpreadPerRow"])
print("CTA styles:", set((c["color"], c["fontWeight"], c["fontSize"], c["display"]) for c in res["home"]["ctas"]))
print("form labels:", res["form"]["labels"])
print("submit:", repr(res["form"]["submit"]))
