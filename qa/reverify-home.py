#!/usr/bin/env python3
"""Re-verify home detail: grid, CTA texts vs lib/content.ts anchors, CTA style,
logo 48px @1440/390/320, contact radios, real clicks. Writes qa/reverify-home.json."""
import json, os, re
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
BASE = "http://127.0.0.1:8410/midvale-water-damage"
JS_HOME = """() => {
  const cards = [...document.querySelectorAll('main .service-card, main a.area-card, main .location-card')];
  const grid = document.querySelector('main .cards-grid, main .service-grid, main .grid');
  const cs = grid ? getComputedStyle(grid) : null;
  const ctas = [...document.querySelectorAll('.card-cta')].map(e => {
    const s = getComputedStyle(e);
    const r = e.getBoundingClientRect();
    return {text: e.innerText.trim(), color: s.color, weight: s.fontWeight, size: s.fontSize,
            display: s.display, tag: e.tagName, top: Math.round(r.top)};
  });
  const brand = document.querySelector('a.brand');
  const bb = brand ? brand.getBoundingClientRect() : null;
  // card rows: group service cards by top
  const svc = [...document.querySelectorAll('main .service-card')].map(e => {
    const r = e.getBoundingClientRect(); return {top: Math.round(r.top), w: Math.round(r.width)};
  });
  const rows = {};
  svc.forEach(c => { rows[c.top] = rows.get(c.top, 0) + 1; });
  return {cardCount: cards.length, svcCount: svc.length, rows,
    gridCols: cs ? cs.gridTemplateColumns : null,
    gridColsCount: cs ? cs.gridTemplateColumns.split(' ').length : null,
    ctas, brandH: bb ? Math.round(bb.height) : null};
}"""
JS_RADIO = """() => {
  const labels = [...document.querySelectorAll('.contact-form .radio-row label')].map(e => {
    const b = e.getBoundingClientRect(); return {text: e.innerText.trim(), h: Math.round(b.height)};
  });
  const fields = [...document.querySelectorAll('.contact-form input, .contact-form textarea')].map(e => (e.type||e.tagName)+':'+(e.name||e.placeholder||''));
  const submit = document.querySelector('.contact-form button[type=submit]');
  return {labels, fields, submitText: submit ? submit.innerText.trim() : null};
}"""
res = {"home": {}, "contact": {}, "clicks": [], "problems": []}
def add(s, c, p, d): res["problems"].append({"severity": s, "check": c, "page": p, "detail": d})
with sync_playwright() as pw:
    br = pw.chromium.launch(args=["--single-process", "--no-zygote", "--disable-gpu", "--disable-dev-shm-usage"])
    for vw in (1440, 390, 320):
        ctx = br.new_context(viewport={"width": vw, "height": 900 if vw == 1440 else (844 if vw == 390 else 568)})
        ctx.route("**/*google*maps*", lambda route: route.abort())
        page = ctx.new_page()
        page.goto(BASE + "/", wait_until="domcontentloaded")
        page.wait_for_timeout(900)
        h = page.evaluate(JS_HOME)
        res["home"][str(vw)] = h
        page.screenshot(path=os.path.join(ROOT, "qa", f"reverify-home-{vw}.png"))
        if vw == 1440:
            page.screenshot(path=os.path.join(ROOT, "qa", "reverify-home-1440-top.png"))
        ctx.close()
    ctx = br.new_context(viewport={"width": 1440, "height": 900})
    ctx.route("**/*google*maps*", lambda route: route.abort())
    page = ctx.new_page()
    page.goto(BASE + "/contact", wait_until="domcontentloaded")
    page.wait_for_timeout(900)
    res["contact"] = page.evaluate(JS_RADIO)
    page.goto(BASE + "/", wait_until="domcontentloaded")
    page.wait_for_timeout(700)
    page.click("main a[href='/midvale-water-damage/burst-pipe-water-damage'] >> nth=0")
    page.wait_for_timeout(600)
    res["clicks"].append({"step": "card->burst-pipe", "url": page.url,
                          "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")})
    page.click("a.brand")
    page.wait_for_timeout(600)
    res["clicks"].append({"step": "logo->home", "url": page.url})
    page.goto(BASE + "/emergency-water-extraction", wait_until="domcontentloaded")
    page.wait_for_timeout(700)
    page.click("footer a[href='/midvale-water-damage/mold-remediation'] >> nth=0")
    page.wait_for_timeout(600)
    res["clicks"].append({"step": "footer->mold", "url": page.url,
                          "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")})
    ctx.close()
    br.close()
anchors = re.findall(r'anchor:\s*"([^"]+)"', open(os.path.join(ROOT, "lib", "content.ts")).read())
cta = [re.sub(r"\s+", " ", c["text"].replace("\u2192", "")).strip() for c in res["home"]["1440"]["ctas"]]
res["anchors"] = {"lib_anchors": anchors, "cta_1440": cta, "match": sorted(anchors) == sorted(cta)}
if not res["anchors"]["match"]: add("P1", "cta-texts", "/", f"diff={set(anchors) ^ set(cta)}")
for vw in ("1440", "390", "320"):
    if res["home"][vw]["brandH"] != 48: add("P1", "logo-48", f"/@{vw}", str(res["home"][vw]["brandH"]))
for lab in res["contact"].get("labels", []):
    if lab["h"] != 48: add("P1", "radio-48", "/contact", str(lab))
for c in res["clicks"]:
    if "/midvale-water-damage" not in c["url"]: add("P1", "click-subpath", c["step"], c["url"])
json.dump(res, open(os.path.join(ROOT, "qa", "reverify-home.json"), "w"), indent=1)
print(json.dumps(res, indent=1, default=str)[:5000])
