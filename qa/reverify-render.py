#!/usr/bin/env python3
"""CYCLE 1 RE-VERIFY — render pass (Playwright Chromium), Midvale UT.
31 routes x 320/390/1440: Button2 scroll-0, overflow, console, failed reqs,
images render, hidden words in main, FAQ answers visible at load.
Homepage 1440/390: card grid, CTA texts vs lib/content.ts anchors, CTA style,
logo 48px. /contact radio labels 48px. Real-click nav. Writes qa/reverify-render.json."""
import json, os, re
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
BASE = "http://127.0.0.1:8410/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]
BTN2 = "Request Emergency Help"
def url(r): return BASE + "/" if r == "/" else BASE + r

JS_PAGE = """() => {
  const vw = window.innerWidth;
  const de = document.documentElement;
  const hero = document.querySelector('main section.hero, main .hero, main section:first-of-type');
  const btns = hero ? [...hero.querySelectorAll('a')].filter(a => !a.closest('nav')).map(a => {
    const b = a.getBoundingClientRect();
    return {text: a.innerText.trim(), bottom: Math.round(b.bottom), h: Math.round(b.height)};
  }) : [];
  // hidden words inside main: text in elements with display:none / visibility:hidden / hidden attr
  let hiddenWords = 0; const hiddenSamples = [];
  document.querySelectorAll('main *').forEach(e => {
    const cs = getComputedStyle(e);
    if (cs.display === 'none' || cs.visibility === 'hidden' || e.hasAttribute('hidden')) {
      const t = (e.innerText || '').trim();
      if (t && e.children.length === 0) { hiddenWords += t.split(/\\s+/).length; hiddenSamples.push(t.slice(0,60)); }
    }
  });
  // FAQ answers visible at load: details open? or answer elements visible
  const faqSecs = [...document.querySelectorAll('main details')];
  const faqClosed = faqSecs.filter(d => !d.open).length;
  const faqAns = [...document.querySelectorAll('main [class*=faq] p, main .faq-answer, main details p')].map(e => {
    const b = e.getBoundingClientRect(); const cs = getComputedStyle(e);
    return {visible: b.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden', h: Math.round(b.height)};
  });
  const imgs = [...document.querySelectorAll('main img, header img')].map(im => ({
    src: (im.getAttribute('src')||'').split('/').pop(), nw: im.naturalWidth, nh: im.naturalHeight,
    complete: im.complete, w: Math.round(im.getBoundingClientRect().width)}));
  return {vw, overflow: de.scrollWidth - de.clientWidth, scrollW: de.scrollWidth, clientW: de.clientWidth,
    buttons: btns, hiddenWords, hiddenSamples: hiddenSamples.slice(0,5),
    faqDetails: faqSecs.length, faqClosed, faqAnsVisible: faqAns.filter(x=>x.visible).length,
    faqAnsTotal: faqAns.length, imgs};
}"""

JS_HOME = """() => {
  const cards = [...document.querySelectorAll('.service-card, .card, a.area-card, .location-card')];
  const grid = document.querySelector('.cards-grid, .service-grid, main .grid');
  const cs = grid ? getComputedStyle(grid) : null;
  const ctas = [...document.querySelectorAll('.card-cta')].map(e => {
    const s = getComputedStyle(e);
    return {text: e.innerText.trim(), color: s.color, weight: s.fontWeight, size: s.fontSize,
            display: s.display, tag: e.tagName, cls: e.className};
  });
  const summaries = [...document.querySelectorAll('.card-summary, .service-card p')].map(e => e.innerText.trim().slice(0,80));
  const brand = document.querySelector('a.brand');
  const bb = brand ? brand.getBoundingClientRect() : null;
  return {cardCount: cards.length, gridCols: cs ? cs.gridTemplateColumns : null,
    gridColsCount: cs ? cs.gridTemplateColumns.split(' ').length : null,
    ctas, brandH: bb ? Math.round(bb.height) : null, brandW: bb ? Math.round(bb.width) : null};
}"""

JS_RADIO = """() => {
  const labels = [...document.querySelectorAll('.contact-form .radio-row label')].map(e => {
    const b = e.getBoundingClientRect(); return {text: e.innerText.trim(), h: Math.round(b.height), w: Math.round(b.width)};
  });
  const fields = [...document.querySelectorAll('.contact-form input, .contact-form textarea, .contact-form select')].map(e => e.tagName+':'+(e.type||''));
  const submit = document.querySelector('.contact-form button[type=submit], .contact-form input[type=submit]');
  return {labels, fields, submitText: submit ? submit.innerText.trim() : null};
}"""

results = {"pages": {}, "problems": [], "home": {}, "contact": {}, "clicks": []}
def add(s, c, p, d): results["problems"].append({"severity": s, "check": c, "page": p, "detail": d})

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for vw in (320, 390, 1440):
        ctx = br.new_context(viewport={"width": vw, "height": 700})
        ctx.route("**/*google*maps*", lambda route: route.abort())
        ctx.route("**/*googletagmanager*", lambda route: route.abort())
        ctx.route("**/*google-analytics*", lambda route: route.abort())
        for r in ROUTES:
            page = ctx.new_page()
            console, failed = [], []
            page.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
            page.on("requestfailed", lambda req: failed.append(req.url))
            page.on("response", lambda resp: failed.append(resp.url + " HTTP " + str(resp.status)) if resp.status >= 400 else None)
            try:
                page.goto(url(r), wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(1200)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(400)
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(300)
                d = page.evaluate(JS_PAGE)
            except Exception as e:
                results["pages"][f"{r}@{vw}"] = {"error": str(e)[:200]}
                add("P1", "render-goto", f"{r}@{vw}", str(e)[:200])
                page.close()
                continue
            key = f"{r}@{vw}"
            results["pages"][key] = {**d, "console_errors": console, "failed": [f for f in failed if "google.com" not in f and "maps" not in f.lower()]}
            if d["overflow"] != 0: add("P1", "overflow", key, f"overflow {d['overflow']}px")
            if console: add("P1", "console", key, str(console[:3]))
            if results["pages"][key]["failed"]: add("P1", "failed-requests", key, str(results["pages"][key]["failed"][:3]))
            b2 = [b for b in d["buttons"] if b["text"] == BTN2]
            if b2 and b2[0]["bottom"] > 700: add("P1", "button2-fold", key, f"Button2 bottom {b2[0]['bottom']} > 700")
            if not b2: add("P2", "button2-missing", key, f"buttons: {d['buttons']}")
            bad_imgs = [im for im in d["imgs"] if not im["complete"] or im["nw"] == 0]
            if bad_imgs: add("P1", "images-render", key, str(bad_imgs[:3]))
            if d["hiddenWords"]: add("P1", "hidden-words", key, f"{d['hiddenWords']} words: {d['hiddenSamples']}")
            if d["faqClosed"]: add("P1", "faq-closed", key, f"{d['faqClosed']}/{d['faqDetails']} details closed")
            if d["faqAnsTotal"] and d["faqAnsVisible"] != d["faqAnsTotal"]:
                add("P2", "faq-answers-visible", key, f"{d['faqAnsVisible']}/{d['faqAnsTotal']} visible")
            page.close()
        ctx.close()
    # homepage 1440 + 390 detail
    for vw in (1440, 390):
        ctx = br.new_context(viewport={"width": vw, "height": 900})
        page = ctx.new_page()
        page.goto(url("/"), wait_until="domcontentloaded")
        page.wait_for_timeout(800)
        page.wait_for_timeout(400)
        h = page.evaluate(JS_HOME)
        results["home"][str(vw)] = h
        page.screenshot(path=os.path.join(ROOT, "qa", f"reverify-home-{vw}.png"), full_page=True)
        ctx.close()
    # contact radios
    ctx = br.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(url("/contact"), wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    page.wait_for_timeout(400)
    results["contact"] = page.evaluate(JS_RADIO)
    # real clicks: homepage card -> service, service -> home via logo, footer link
    page.goto(url("/"), wait_until="domcontentloaded")
    page.wait_for_timeout(300)
    page.click("main a[href='/midvale-water-damage/burst-pipe-water-damage'] >> nth=0")
    page.wait_for_timeout(500)
    results["clicks"].append({"step": "card->burst-pipe", "url": page.url,
                              "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")})
    page.click("a.brand")
    page.wait_for_timeout(500)
    results["clicks"].append({"step": "logo->home", "url": page.url})
    page.goto(url("/emergency-water-extraction"), wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    page.wait_for_timeout(300)
    page.click("footer a[href='/midvale-water-damage/mold-remediation'] >> nth=0")
    page.wait_for_timeout(500)
    results["clicks"].append({"step": "footer->mold", "url": page.url,
                              "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")})
    ctx.close()
    br.close()

# CTA texts vs anchors in lib/content.ts
anchors = re.findall(r'anchor:\s*"([^"]+)"', open(os.path.join(ROOT, "lib", "content.ts")).read())
cta1440 = [c["text"].replace("\u2192", "").strip() for c in results["home"]["1440"]["ctas"]]
cta_texts_clean = [re.sub(r"\s+", " ", t).strip() for t in cta1440]
results["anchors"] = {"lib_anchors": anchors, "cta_1440": cta_texts_clean,
                      "match": sorted(anchors) == sorted(cta_texts_clean)}
if not results["anchors"]["match"]:
    add("P1", "cta-texts", "/", f"anchors {len(anchors)} vs cta {len(cta_texts_clean)}; diff={set(anchors) ^ set(cta_texts_clean)}")
if results["home"]["1440"]["brandH"] != 48: add("P1", "logo-48", "/", str(results["home"]["1440"]["brandH"]))
if results["home"]["390"]["brandH"] != 48: add("P1", "logo-48", "/@390", str(results["home"]["390"]["brandH"]))
for lab in results["contact"].get("labels", []):
    if lab["h"] != 48: add("P1", "radio-48", "/contact", str(lab))
for c in results["clicks"]:
    if "/midvale-water-damage" not in c["url"]: add("P1", "click-subpath", c["step"], c["url"])
json.dump(results, open(os.path.join(ROOT, "qa", "reverify-render.json"), "w"), indent=1)
print(json.dumps({"problems": results["problems"], "home1440": results["home"]["1440"],
                  "home390_grid": results["home"]["390"].get("gridColsCount"),
                  "contact": results["contact"], "clicks": results["clicks"],
                  "anchors_match": results["anchors"]["match"]}, indent=1, default=str))
