#!/usr/bin/env python3
"""Home-detail in small single-purpose runs. Usage: reverify-home2.py <1440|390|320|contact>
Writes qa/reverify-home-<part>.json immediately after its run."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
BASE = "http://127.0.0.1:8410/midvale-water-damage"
PART = sys.argv[1]
JS_HOME = """() => {
  const cards = [...document.querySelectorAll('#services article.card, #areas article.card')];
  const grid = document.querySelector('#services .card-grid');
  const gridAreas = document.querySelector('#areas .card-grid');
  const csA = gridAreas ? getComputedStyle(gridAreas) : null;
  const cs = grid ? getComputedStyle(grid) : null;
  const ctas = [...document.querySelectorAll('.card-cta')].map(e => {
    const s = getComputedStyle(e);
    const r = e.getBoundingClientRect();
    return {text: e.innerText.trim(), color: s.color, weight: s.fontWeight, size: s.fontSize,
            display: s.display, tag: e.tagName};
  });
  const brand = document.querySelector('a.brand');
  const bb = brand ? brand.getBoundingClientRect() : null;
  const svc = [...document.querySelectorAll('#services article.card')].map(e => {
    const r = e.getBoundingClientRect(); return {top: Math.round(r.top), w: Math.round(r.width)};
  });
  const locCards = [...document.querySelectorAll('#areas article.card')].map(e => {
    const r = e.getBoundingClientRect(); return {top: Math.round(r.top), w: Math.round(r.width)};
  });
  const rows = {};
  svc.forEach(c => { rows[c.top] = (rows[c.top] || 0) + 1; });
  const loc = locCards;
  const locRows = {};
  loc.forEach(c => { locRows[c.top] = (locRows[c.top] || 0) + 1; });
  // CTA bottom alignment per row: cta tops grouped
  const ctaTops = {};
  ctas.forEach(c => { ctaTops[c.top] = (ctaTops[c.top] || 0) + 1; });
  return {cardCount: cards.length, svcCount: svc.length, rows, locRows,
    gridAreasCols: csA ? csA.gridTemplateColumns.split(' ').length : null, locCardCount: locCards.length,
    gridCols: cs ? cs.gridTemplateColumns : null,
    gridColsCount: cs ? cs.gridTemplateColumns.split(' ').length : null,
    ctas, brandH: bb ? Math.round(bb.height) : null, brandW: bb ? Math.round(bb.width) : null};
}"""
JS_RADIO = """() => {
  const labels = [...document.querySelectorAll('.contact-form .radio-row label')].map(e => {
    const b = e.getBoundingClientRect(); return {text: e.innerText.trim(), h: Math.round(b.height)};
  });
  const fields = [...document.querySelectorAll('.contact-form input, .contact-form textarea')].map(e => (e.type||e.tagName)+':'+(e.name||e.placeholder||''));
  const submit = document.querySelector('.contact-form button[type=submit]');
  return {labels, fields, submitText: submit ? submit.innerText.trim() : null};
}"""

def launch(pw):
    for attempt in range(4):
        try:
            return pw.chromium.launch(args=["--single-process", "--no-zygote", "--disable-gpu", "--disable-dev-shm-usage"])
        except Exception as e:
            print("launch attempt", attempt, "failed:", str(e)[:120]); time.sleep(15)
    raise RuntimeError("browser launch failed 4x")

res = {}
with sync_playwright() as pw:
    br = launch(pw)
    if PART in ("1440", "390", "320"):
        vw = int(PART)
        vh = 900 if vw == 1440 else (844 if vw == 390 else 568)
        ctx = br.new_context(viewport={"width": vw, "height": vh})
        ctx.route("**/*google*maps*", lambda route: route.abort())
        page = ctx.new_page()
        page.goto(BASE + "/", wait_until="domcontentloaded")
        page.wait_for_timeout(900)
        res = page.evaluate(JS_HOME)
        # scroll to cards for the screenshot
        page.evaluate("document.querySelector('.card-cta')?.scrollIntoView({block:'center'})")
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(ROOT, "qa", f"reverify-home-{vw}-cards.png"))
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(ROOT, "qa", f"reverify-home-{vw}-top.png"))
        ctx.close()
    elif PART == "contact":
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
        res["clicks"] = [{"step": "card->burst-pipe", "url": page.url,
                          "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")}]
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
json.dump(res, open(os.path.join(ROOT, "qa", f"reverify-home-{PART}.json"), "w"), indent=1)
print(json.dumps(res, indent=1)[:3500])
