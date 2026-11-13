#!/usr/bin/env python3
"""Resumable render pass, ONE viewport per run. Usage: reverify-render2.py <320|390|1440>
Writes qa/reverify-render-<vw>.json after EVERY route (resume-safe)."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
BASE = "http://127.0.0.1:8410/midvale-water-damage"
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]
BTN2 = "Request Emergency Help"
VW = int(sys.argv[1])
OUTP = os.path.join(ROOT, "qa", f"reverify-render-{VW}.json")
def url(r): return BASE + "/" if r == "/" else BASE + r

JS_PAGE = """() => {
  const de = document.documentElement;
  const hero = document.querySelector('main section.hero, main .hero, main section:first-of-type');
  const btns = hero ? [...hero.querySelectorAll('a')].filter(a => !a.closest('nav')).map(a => {
    const b = a.getBoundingClientRect();
    return {text: a.innerText.trim(), bottom: Math.round(b.bottom), h: Math.round(b.height)};
  }) : [];
  let hiddenWords = 0; const hiddenSamples = [];
  document.querySelectorAll('main *:not(script):not(style):not(noscript):not(template)').forEach(e => {
    if (e.closest('script,style,noscript,template')) return;
    const cs = getComputedStyle(e);
    if (cs.display === 'none' || cs.visibility === 'hidden' || e.hasAttribute('hidden')) {
      const t = (e.innerText || '').trim();
      if (t && e.children.length === 0) { hiddenWords += t.split(/\\s+/).length; hiddenSamples.push(t.slice(0,60)); }
    }
  });
  const faqSecs = [...document.querySelectorAll('main details')];
  const faqClosed = faqSecs.filter(d => !d.open).length;
  const faqAns = [...document.querySelectorAll('main [class*=faq] p, main .faq-answer, main details p')].map(e => {
    const b = e.getBoundingClientRect(); const cs = getComputedStyle(e);
    return {visible: b.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden'};
  });
  const imgs = [...document.querySelectorAll('main img, header img')].map(im => ({
    src: (im.getAttribute('src')||'').split('/').pop(), nw: im.naturalWidth, complete: im.complete}));
  return {overflow: de.scrollWidth - de.clientWidth, buttons: btns,
    hiddenWords, hiddenSamples: hiddenSamples.slice(0,5),
    faqDetails: faqSecs.length, faqClosed, faqAnsVisible: faqAns.filter(x=>x.visible).length,
    faqAnsTotal: faqAns.length, imgs};
}"""

res = {"pages": {}, "problems": []}
if os.path.exists(OUTP):
    try:
        res = json.load(open(OUTP))
        print("resumed:", len(res["pages"]), "routes done")
    except Exception: pass
def add(s, c, p, d): res["problems"].append({"severity": s, "check": c, "page": p, "detail": d})
def save(): json.dump(res, open(OUTP, "w"), indent=1)

with sync_playwright() as pw:
    br = pw.chromium.launch(args=["--single-process", "--no-zygote", "--disable-gpu", "--disable-dev-shm-usage"])
    VH = {320: 568, 390: 844, 1440: 900}[VW]
    ctx = br.new_context(viewport={"width": VW, "height": VH})
    ctx.route("**/*google*maps*", lambda route: route.abort())
    ctx.route("**/*googletagmanager*", lambda route: route.abort())
    ctx.route("**/*google-analytics*", lambda route: route.abort())
    for r in ROUTES:
        key = f"{r}@{VW}"
        if key in res["pages"]: continue
        page = ctx.new_page()
        console, failed = [], []
        page.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
        page.on("requestfailed", lambda req: failed.append(req.url))
        page.on("response", lambda resp: failed.append(resp.url + " HTTP " + str(resp.status)) if resp.status >= 400 else None)
        try:
            page.goto(url(r), wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(900)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(300)
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(250)
            d = page.evaluate(JS_PAGE)
        except Exception as e:
            res["pages"][key] = {"error": str(e)[:200]}
            add("P1", "render-goto", key, str(e)[:200])
            save(); page.close(); continue
        lf_raw = list(failed)
        lf = [f for f in failed if "google.com" not in f and "maps" not in f.lower() and "_rsc=" not in f]
        console = [c for c in console if "RSC payload" not in c]
        res["pages"][key] = {**d, "console_errors": console, "failed": lf, "failed_raw": lf_raw}
        if d["overflow"] != 0: add("P1", "overflow", key, f"overflow {d['overflow']}px")
        if console: add("P1", "console", key, str(console[:3]))
        if lf: add("P1", "failed-requests", key, str(lf[:3]))
        b2 = [b for b in d["buttons"] if b["text"] == BTN2]
        if b2 and b2[0]["bottom"] > VH: add("P1", "button2-fold", key, f"Button2 bottom {b2[0]['bottom']} > {VH}")
        if not b2: add("P2", "button2-missing", key, f"buttons: {d['buttons']}")
        bad = [im for im in d["imgs"] if not im["complete"] or im["nw"] == 0]
        if bad: add("P1", "images-render", key, str(bad[:3]))
        if d["hiddenWords"]: add("P1", "hidden-words", key, f"{d['hiddenWords']} words: {d['hiddenSamples']}")
        if d["faqClosed"]: add("P1", "faq-closed", key, f"{d['faqClosed']}/{d['faqDetails']} details closed")
        if d["faqAnsTotal"] and d["faqAnsVisible"] != d["faqAnsTotal"]:
            add("P2", "faq-answers-visible", key, f"{d['faqAnsVisible']}/{d['faqAnsTotal']} visible")
        save()
        page.close()
        print(key, "overflow", d["overflow"], "btn2", [b["bottom"] for b in d["buttons"] if b["text"]==BTN2], "imgs", len(d["imgs"]), "bad", len(bad))
    ctx.close()
    br.close()
print("DONE", VW, "problems:", json.dumps(res["problems"], indent=1)[:3000])
