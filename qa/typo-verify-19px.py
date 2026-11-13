"""Typography round verification for Midvale (v2): Button 2 scroll-0, overflow,
console errors, computed body-copy sizes. Serves out/ under /midvale-water-damage/.
v2 fixes: domcontentloaded + selector wait (no networkidle — footer Maps iframe
never idles), incremental per-page results, per-page try/except, --disable-dev-shm-usage.
Run with TMPDIR pointed at a writable dir (the VM /tmp tmpfs was 100% full)."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8931/midvale-water-damage"
ROUTES = [
 "/", "/about", "/contact", "/emergency-water-extraction", "/basement-flooding-cleanup",
 "/window-well-flooding", "/burst-pipe-water-damage", "/sewage-backup-cleanup",
 "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage", "/ceiling-water-damage",
 "/crawl-space-water-damage", "/hardwood-floor-cabinet-drying", "/condo-apartment-water-damage",
 "/commercial-water-damage", "/storm-flood-damage", "/mold-remediation", "/water-leak-detection",
 "/water-damage-repair", "/locations/cottonwood-heights-ut", "/locations/south-salt-lake-ut",
 "/locations/magna-ut", "/midvale-water-sewer-emergency-contacts", "/privacy-policy",
 "/terms-of-use", "/disclaimer", "/resources/frozen-pipes-midvale",
 "/resources/winterize-swamp-cooler-utah", "/resources/upstairs-unit-leak-who-pays-utah",
 "/resources/can-mold-grow-in-utah", "/resources/basement-flooding-spring-snowmelt-utah",
]

def url(route):
    if route == "/":
        return BASE + "/"
    return BASE + route + ".html"

EVAL = """() => {
  const btn2 = [...document.querySelectorAll('.hero-buttons .btn-help')][0];
  const r = btn2 ? btn2.getBoundingClientRect() : null;
  const cs = getComputedStyle(document.body);
  const p = document.querySelector('.page-body p, .section p, .hero p.intro');
  const li = document.querySelector('.page-body li, .section li');
  const cardP = document.querySelector('.card-body p');
  const lead = document.querySelector('.lead');
  const h1 = document.querySelector('h1');
  const h2 = document.querySelector('h2');
  const h3 = document.querySelector('h3');
  const inp = document.querySelector('.contact-form input, .contact-form textarea');
  const f = el => el ? getComputedStyle(el).fontSize : null;
  return {
    btn2Bottom: r ? Math.round(r.bottom * 10) / 10 : null,
    btn2Visible: !!r,
    overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    bodyFont: cs.fontSize,
    pFont: f(p), liFont: f(li), cardPFont: f(cardP), leadFont: f(lead),
    h1Font: f(h1), h2Font: f(h2), h3Font: f(h3), inputFont: f(inp),
  };
}"""

results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--disable-dev-shm-usage"])
    for route in ROUTES:
        rec = {"route": route, "consoleErrors": []}
        try:
            for width, height in [(320, 844), (390, 844), (1440, 900)]:
                ctx = browser.new_context(viewport={"width": width, "height": height})
                page = ctx.new_page()
                page.on("console", lambda m, w=width: rec["consoleErrors"].append(f"{w}:{m.type}:{m.text}") if m.type == "error" else None)
                page.on("pageerror", lambda e, w=width: rec["consoleErrors"].append(f"{w}:pageerror:{e}"))
                page.goto(url(route), wait_until="domcontentloaded", timeout=30000)
                page.wait_for_selector(".hero-buttons .btn-help", timeout=15000)
                page.wait_for_timeout(300)
                rec[f"w{width}"] = page.evaluate(EVAL)
                ctx.close()
        except Exception as e:
            rec["error"] = str(e)[:300]
        results.append(rec)
        json.dump(results, open("qa/typo-verify-19px-results.json", "w"), indent=1)
        print("done", route, rec.get("w320", {}).get("btn2Bottom"), rec.get("w390", {}).get("btn2Bottom"), flush=True)
    browser.close()

done = [r for r in results if "w320" in r]
print(f"pages measured: {len(done)}/31")
print(f"Button2 scroll-0 @320 (viewport 844): pass {sum(1 for r in done if r['w320']['btn2Bottom'] is not None and r['w320']['btn2Bottom'] <= 844)}/{len(done)}, worst bottom {max(r['w320']['btn2Bottom'] for r in done)}px")
print(f"Button2 scroll-0 @390 (viewport 844): pass {sum(1 for r in done if r['w390']['btn2Bottom'] is not None and r['w390']['btn2Bottom'] <= 844)}/{len(done)}, worst bottom {max(r['w390']['btn2Bottom'] for r in done)}px")
for r in done:
    if r["w320"]["btn2Bottom"] > 844 or r["w390"]["btn2Bottom"] > 844:
        print("  FAIL", r["route"], r["w320"]["btn2Bottom"], r["w390"]["btn2Bottom"])
print("overflow>0:", [(r["route"], w, r[f"w{w}"]["overflowX"]) for r in done for w in (320, 390, 1440) if r[f"w{w}"]["overflowX"] > 0] or "none")
print("console errors:", sum(len(r["consoleErrors"]) for r in results))
for r in results:
    if r["consoleErrors"]:
        print("  ", r["route"], r["consoleErrors"][:3])
    if "error" in r:
        print("  PAGE ERROR", r["route"], r["error"])
fonts = set()
for r in done:
    for w in (320, 390, 1440):
        m = r[f"w{w}"]
        fonts.add((m["bodyFont"], m["pFont"], m["liFont"], m["cardPFont"], m["h1Font"], m["h2Font"], m["h3Font"]))
print("computed fonts (body,p,li,cardP,h1,h2,h3):", sorted(fonts))
print("lead fonts:", sorted({r["w1440"]["leadFont"] for r in done}))
print("input fonts (contact):", [r["w1440"]["inputFont"] for r in done if r["route"] == "/contact"])
