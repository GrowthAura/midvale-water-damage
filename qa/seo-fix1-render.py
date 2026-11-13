#!/usr/bin/env python3
"""SEO FIX 1 render verification (post-fix build):
- 1440px: header nav link heights, footer link min heights, header phone, overflow
- 390px: console errors + failed local requests on all 31 routes
- Real-click nav: home -> service -> location, subpath kept
- Maps iframe: lazy attr present in DOM on a map page, absent on location pages
Usage: python3 qa/seo-fix1-render.py <port> <out.json>"""
import json, sys, subprocess, time, signal
from playwright.sync_api import sync_playwright

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8326
OUT = sys.argv[2] if len(sys.argv) > 2 else "qa/seo-fix1-render.json"
BASE = f"http://127.0.0.1:{PORT}/midvale-water-damage"

ROUTES = ["", "/about", "/contact", "/emergency-water-extraction",
"/basement-flooding-cleanup", "/window-well-flooding", "/burst-pipe-water-damage",
"/sewage-backup-cleanup", "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage",
"/ceiling-water-damage", "/crawl-space-water-damage", "/hardwood-floor-cabinet-drying",
"/condo-apartment-water-damage", "/commercial-water-damage", "/storm-flood-damage",
"/mold-remediation", "/water-leak-detection", "/water-damage-repair",
"/locations/cottonwood-heights-ut", "/locations/south-salt-lake-ut",
"/locations/magna-ut", "/midvale-water-sewer-emergency-contacts",
"/privacy-policy", "/terms-of-use", "/disclaimer",
"/resources/frozen-pipes-midvale", "/resources/winterize-swamp-cooler-utah",
"/resources/upstairs-unit-leak-who-pays-utah", "/resources/can-mold-grow-in-utah",
"/resources/basement-flooding-spring-snowmelt-utah"]

srv = subprocess.Popen(["python3", "qa/linkfix-serve.py", str(PORT)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
res = {"desktop1440": {}, "console390": {}, "clicks": [], "maps": {}}
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        # --- 1440 desktop tap targets ---
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        for r in ["", "/emergency-water-extraction", "/locations/magna-ut", "/contact"]:
            pg.goto(BASE + (r if r else "/"), wait_until="networkidle", timeout=30000)
            m = pg.evaluate("""() => {
              const nav = [...document.querySelectorAll('.main-nav a')].map(a => Math.round(a.getBoundingClientRect().height*10)/10);
              const foot = [...document.querySelectorAll('.site-footer a')].map(a => Math.round(a.getBoundingClientRect().height*10)/10);
              const hp = document.querySelector('.header-phone');
              const brand = document.querySelector('.brand');
              return {
                navMin: nav.length ? Math.min(...nav) : null, navCount: nav.length,
                footMin: foot.length ? Math.min(...foot) : null, footCount: foot.length,
                headerPhoneH: hp ? Math.round(hp.getBoundingClientRect().height*10)/10 : null,
                brandH: brand ? Math.round(brand.getBoundingClientRect().height*10)/10 : null,
                overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
              }; }""")
            res["desktop1440"][r or "/"] = m
        pg.close()
        # --- 390 console + failed requests, all 31 ---
        pg = b.new_page(viewport={"width": 390, "height": 844})
        for r in ROUTES:
            errs, failed = [], []
            pg.on("console", lambda msg, e=errs: e.append(msg.text) if msg.type == "error" else None)
            pg.on("requestfailed", lambda req, f=failed: f.append(req.url))
            pg.on("response", lambda resp, f=failed: f.append(resp.url) if resp.status >= 400 and "google.com" not in resp.url and "127.0.0.1" in resp.url else None)
            pg.goto(BASE + (r if r else "/"), wait_until="networkidle", timeout=30000)
            res["console390"][r or "/"] = {"consoleErrors": errs, "failedLocal": failed}
        pg.close()
        # --- real-click nav ---
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(BASE + "/", wait_until="networkidle", timeout=30000)
        pg.click(".card-wrap-link[href='/midvale-water-damage/emergency-water-extraction']")
        pg.wait_for_load_state("networkidle")
        res["clicks"].append({"after": "service card click", "url": pg.url,
                              "h1": pg.evaluate("() => document.querySelector('h1').textContent")})
        pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        pg.click(".site-footer a[href='/midvale-water-damage/locations/cottonwood-heights-ut']")
        pg.wait_for_load_state("networkidle")
        res["clicks"].append({"after": "footer location click", "url": pg.url,
                              "h1": pg.evaluate("() => document.querySelector('h1').textContent")})
        pg.click(".breadcrumb a >> nth=0")
        pg.wait_for_load_state("networkidle")
        res["clicks"].append({"after": "breadcrumb Home click", "url": pg.url,
                              "h1": pg.evaluate("() => document.querySelector('h1').textContent")})
        pg.close()
        # --- maps iframe in DOM ---
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.goto(BASE + "/emergency-water-extraction", wait_until="domcontentloaded", timeout=30000)
        res["maps"]["service"] = pg.evaluate("""() => {
          const f = document.querySelector('.footer-map iframe');
          return f ? {loading: f.getAttribute('loading'), src: f.src.slice(0, 60)} : null; }""")
        pg.goto(BASE + "/locations/magna-ut", wait_until="domcontentloaded", timeout=30000)
        res["maps"]["location"] = pg.evaluate("() => document.querySelector('.footer-map iframe') ? 'PRESENT' : 'absent'")
        pg.close()
        b.close()
finally:
    srv.send_signal(signal.SIGTERM)

json.dump(res, open(OUT, "w"), indent=1)
d = res["desktop1440"]
print("1440 navMin:", {k: v["navMin"] for k, v in d.items()}, "footMin:", {k: v["footMin"] for k, v in d.items()},
      "headerPhone:", {k: v["headerPhoneH"] for k, v in d.items()}, "overflow:", {k: v["overflow"] for k, v in d.items()})
tot_err = sum(len(v["consoleErrors"]) for v in res["console390"].values())
tot_fail = sum(len(v["failedLocal"]) for v in res["console390"].values())
print(f"console errors total @390: {tot_err}; failed local requests: {tot_fail}")
for c in res["clicks"]:
    print("click:", c["after"], "->", c["url"], "|", (c["h1"] or "")[:60])
print("maps:", res["maps"])
print("wrote", OUT)
