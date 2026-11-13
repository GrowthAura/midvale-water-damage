#!/usr/bin/env python3
"""INDEPENDENT render verification for the Midvale fill + 19px round (2026-11-13).
Fresh code for this task. Serves out/ via qa/linkfix-serve.py on port 8932,
drives Chromium via Playwright with --disable-dev-shm-usage and
TMPDIR=qa/tmpdir. Writes qa/verify-fill-19px-render.json and viewport
screenshots to qa/render-fill19px/ (desktop 1440x900 + m390 390x844, scroll-0).
Does NOT modify site source, CSS, or the image manifest.
"""
import json, os, subprocess, time, socket, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
PORT = 8932
BASE = f"http://127.0.0.1:{PORT}/midvale-water-damage"
RENDER = os.path.join(ROOT, "qa", "render-fill19px")
os.makedirs(RENDER, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
ROUTES = [p["route"] for p in DATA["pages"]]
H1 = {p["route"]: p["h1"] for p in DATA["pages"]}

def slug(route):
    return "home" if route == "/" else route.strip("/").replace("/", "__")

def url(route):
    return BASE + "/" if route == "/" else BASE + route + ".html"

def wait_port(port, timeout=20):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.3)
    return False

srv = subprocess.Popen([sys.executable, os.path.join(ROOT, "qa", "linkfix-serve.py"), str(PORT)],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       env={**os.environ, "TMPDIR": os.path.join(ROOT, "qa", "tmpdir")})
assert wait_port(PORT), "server did not start"

FONTS_EVAL = """() => {
  const out = {body: getComputedStyle(document.body).fontSize, below19: [], h1: null, h2: null, h3: null};
  const h1 = document.querySelector('h1'); if (h1) out.h1 = getComputedStyle(h1).fontSize;
  const h2 = document.querySelector('h2'); if (h2) out.h2 = getComputedStyle(h2).fontSize;
  const h3 = document.querySelector('h3'); if (h3) out.h3 = getComputedStyle(h3).fontSize;
  const main = document.querySelector('main');
  const els = main ? [...main.querySelectorAll('p, li, td, th')] : [];
  // card text + faq answers + form inputs (inside main or page-wide for contact form)
  document.querySelectorAll('.card-body p, #faq p, .contact-form input, .contact-form textarea, .contact-form select, .lead').forEach(e => els.push(e));
  const seen = new Set();
  for (const el of els) {
    if (seen.has(el)) continue; seen.add(el);
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 19) {
      out.below19.push({tag: el.tagName.toLowerCase(), cls: (el.className||'').toString().slice(0,60),
        fontSize: getComputedStyle(el).fontSize,
        text: (el.innerText||el.value||'').trim().slice(0,80)});
    }
  }
  return out;
}"""

IMGS_EVAL = """() => [...document.images].map(i => ({
  src: i.getAttribute('src'), alt: (i.getAttribute('alt')||'').slice(0,60),
  loading: i.getAttribute('loading'), complete: i.complete, naturalWidth: i.naturalWidth,
  displayed: Math.round(i.getBoundingClientRect().width) + 'x' + Math.round(i.getBoundingClientRect().height)
}))"""

BTN_EVAL = """() => {
  const b = [...document.querySelectorAll('.hero-buttons .btn-help')][0];
  if (!b) return {found: false};
  const r = b.getBoundingClientRect();
  return {found: true, text: b.innerText.trim(), bottom: Math.round(r.bottom*10)/10,
          top: Math.round(r.top*10)/10, vh: window.innerHeight, visible: r.bottom <= window.innerHeight && r.top >= 0};
}"""

results = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--disable-dev-shm-usage"])
        # ---- homepage identity ----
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.goto(url("/"), wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_selector("h1", timeout=15000)
        pg.wait_for_timeout(800)
        ident = pg.evaluate("""() => ({h1: (document.querySelector('h1')||{}).innerText || '',
          phone: document.body.innerText.includes('(385) 337-3560'),
          title: document.title})""")
        print("IDENTITY:", ident, flush=True)
        results_identity = ident
        ctx.close()
        # ---- per-page render ----
        for route in ROUTES:
            rec = {"route": route, "consoleErrors": [], "failedRequests": [], "pageerrors": []}
            try:
                # 1440: full scroll, images, fonts, overflow, screenshot
                ctx = browser.new_context(viewport={"width": 1440, "height": 900})
                page = ctx.new_page()
                page.on("console", lambda m: rec["consoleErrors"].append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: rec["pageerrors"].append(str(e)))
                page.on("requestfailed", lambda r: rec["failedRequests"].append(f"{r.url} :: {r.failure}"))
                page.on("response", lambda r: rec["failedRequests"].append(f"{r.url} :: HTTP {r.status}") if r.status >= 400 else None)
                page.goto(url(route), wait_until="domcontentloaded", timeout=30000)
                page.wait_for_selector("h1", timeout=15000)
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(RENDER, slug(route) + "-desktop.png"))
                page.evaluate("""async () => {
                    const h = document.body.scrollHeight;
                    for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 110)); }
                    window.scrollTo(0, 0);
                }""")
                page.wait_for_timeout(600)
                page.evaluate("""async () => {
                    await document.fonts.ready;
                    const imgs = [...document.images];
                    await Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = r; i.onerror = r; setTimeout(r, 5000); })));
                }""")
                page.wait_for_timeout(400)
                rec["imgs1440"] = page.evaluate(IMGS_EVAL)
                rec["img_total_render"] = len(rec["imgs1440"])
                rec["img_broken_render"] = [i for i in rec["imgs1440"] if not i["complete"] or i["naturalWidth"] == 0]
                rec["fonts1440"] = page.evaluate(FONTS_EVAL)
                rec["overflow1440"] = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                rec["btn2_1440"] = page.evaluate(BTN_EVAL)
                ctx.close()
                # 390: button2 + overflow + fonts + screenshot + broken imgs
                ctx = browser.new_context(viewport={"width": 390, "height": 844})
                page = ctx.new_page()
                page.on("console", lambda m: rec["consoleErrors"].append("390:" + m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: rec["pageerrors"].append("390:" + str(e)))
                page.on("requestfailed", lambda r: rec["failedRequests"].append("390:" + r.url + " :: " + str(r.failure)))
                page.on("response", lambda r: rec["failedRequests"].append("390:" + r.url + f" :: HTTP {r.status}") if r.status >= 400 else None)
                page.goto(url(route), wait_until="domcontentloaded", timeout=30000)
                page.wait_for_selector("h1", timeout=15000)
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(RENDER, slug(route) + "-m390.png"))
                rec["btn2_390"] = page.evaluate(BTN_EVAL)
                rec["overflow390"] = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                rec["fonts390"] = page.evaluate(FONTS_EVAL)
                page.evaluate("""async () => {
                    const h = document.body.scrollHeight;
                    for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 110)); }
                    window.scrollTo(0, 0);
                }""")
                page.wait_for_timeout(600)
                page.evaluate("""async () => {
                    const imgs = [...document.images];
                    await Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = r; i.onerror = r; setTimeout(r, 5000); })));
                }""")
                page.wait_for_timeout(400)
                rec["imgs390"] = page.evaluate(IMGS_EVAL)
                rec["img_broken_390"] = [i for i in rec["imgs390"] if not i["complete"] or i["naturalWidth"] == 0]
                ctx.close()
                # 320: button2 + overflow + fonts
                ctx = browser.new_context(viewport={"width": 320, "height": 844})
                page = ctx.new_page()
                page.on("console", lambda m: rec["consoleErrors"].append("320:" + m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: rec["pageerrors"].append("320:" + str(e)))
                page.goto(url(route), wait_until="domcontentloaded", timeout=30000)
                page.wait_for_selector("h1", timeout=15000)
                page.wait_for_timeout(400)
                rec["btn2_320"] = page.evaluate(BTN_EVAL)
                rec["overflow320"] = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                rec["fonts320"] = page.evaluate(FONTS_EVAL)
                ctx.close()
            except Exception as e:
                rec["error"] = str(e)[:400]
            results.append(rec)
            json.dump({"identity": results_identity, "pages": results},
                      open(os.path.join(ROOT, "qa", "verify-fill-19px-render.json"), "w"), indent=1)
            b320 = rec.get("btn2_320", {}).get("bottom"); b390 = rec.get("btn2_390", {}).get("bottom")
            print(f"done {route} imgs={rec.get('img_total_render')} broken1440={len(rec.get('img_broken_render', []))} "
                  f"broken390={len(rec.get('img_broken_390', []))} btn2 320={b320} 390={b390} "
                  f"ov={rec.get('overflow320')}/{rec.get('overflow390')}/{rec.get('overflow1440')} "
                  f"console={len(rec['consoleErrors'])} failed={len(rec['failedRequests'])}", flush=True)
        # ---- click navigation (subpath retention) ----
        clicks = []
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(url("/"), wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector(".card-wrap-link", timeout=15000)
        for i in range(5):
            page.goto(url("/"), wait_until="domcontentloaded", timeout=30000)
            page.wait_for_selector(".card-wrap-link", timeout=15000)
            link = page.query_selector_all(".card-wrap-link")[i]
            href = link.get_attribute("href")
            link.click()
            page.wait_for_selector("h1", timeout=15000)
            page.wait_for_timeout(400)
            clicks.append({"n": i + 1, "href": href, "landed": page.url,
                           "subpath_kept": "/midvale-water-damage/" in page.url,
                           "h1": page.evaluate("() => (document.querySelector('h1')||{}).innerText || '')")})
        # body-link click from an inner page
        page.goto(url("/emergency-water-extraction"), wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector(".body-link", timeout=15000)
        bl = page.query_selector(".body-link")
        bh = bl.get_attribute("href")
        bl.click()
        page.wait_for_selector("h1", timeout=15000)
        page.wait_for_timeout(400)
        clicks.append({"n": 6, "kind": "body-link", "href": bh, "landed": page.url,
                       "subpath_kept": "/midvale-water-damage/" in page.url,
                       "h1": page.evaluate("() => (document.querySelector('h1')||{}).innerText || '')")})
        ctx.close()
        # ---- contact form ----
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(url("/contact"), wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector(".contact-form", timeout=15000)
        form = page.evaluate("""() => {
          const f = document.querySelector('.contact-form');
          const fields = [...f.querySelectorAll('input, textarea, select')].map(e => ({
            tag: e.tagName.toLowerCase(), type: e.getAttribute('type'), name: e.getAttribute('name'),
            label: (f.querySelector(`label[for="${e.id}"]`)||{}).innerText || ''}));
          const submit = [...f.querySelectorAll('button, input[type=submit]')].map(b => b.innerText || b.value);
          return {fields, submit, action: f.getAttribute('action'), method: f.getAttribute('method')};
        }""")
        ctx.close()
        browser.close()
        json.dump({"identity": results_identity, "pages": results, "clicks": clicks, "contact_form": form},
                  open(os.path.join(ROOT, "qa", "verify-fill-19px-render.json"), "w"), indent=1)
        print("CLICKS:", json.dumps(clicks, indent=1), flush=True)
        print("CONTACT FORM:", json.dumps(form, indent=1), flush=True)
finally:
    srv.terminate()

done = [r for r in results if "btn2_320" in r]
print(f"pages measured: {len(done)}/31")
print(f"identity h1 ok: {results_identity['h1'] == H1['/']} phone: {results_identity['phone']}")
print(f"Button2 scroll-0 @320 pass {sum(1 for r in done if r['btn2_320'].get('bottom') is not None and r['btn2_320']['bottom'] <= 844)}/{len(done)}, worst bottom {max(r['btn2_320']['bottom'] for r in done if r['btn2_320'].get('bottom') is not None)}")
print(f"Button2 scroll-0 @390 pass {sum(1 for r in done if r['btn2_390'].get('bottom') is not None and r['btn2_390']['bottom'] <= 844)}/{len(done)}, worst bottom {max(r['btn2_390']['bottom'] for r in done if r['btn2_390'].get('bottom') is not None)}")
print("overflow>0:", [(r["route"], r.get("overflow320"), r.get("overflow390"), r.get("overflow1440")) for r in done if (r.get("overflow320") or 0) > 0 or (r.get("overflow390") or 0) > 0 or (r.get("overflow1440") or 0) > 0] or "none")
print("console errors total:", sum(len(r.get("consoleErrors", [])) for r in results))
for r in results:
    if r.get("consoleErrors"): print("  console", r["route"], r["consoleErrors"][:3])
    if r.get("pageerrors"): print("  pageerror", r["route"], r["pageerrors"][:3])
    if r.get("failedRequests"): print("  failedReq", r["route"], r["failedRequests"][:5])
print("broken imgs 1440:", {r["route"]: [i["src"] for i in r.get("img_broken_render", [])] for r in results if r.get("img_broken_render")})
print("broken imgs 390:", {r["route"]: [i["src"] for i in r.get("img_broken_390", [])] for r in results if r.get("img_broken_390")})
print("fonts1440 distinct:", sorted({(r["fonts1440"]["body"], r["fonts1440"]["h1"], r["fonts1440"]["h2"], r["fonts1440"]["h3"]) for r in done if "fonts1440" in r}))
print("below-19px elements:", [(r["route"], r["fonts1440"]["below19"]) for r in done if "fonts1440" in r and r["fonts1440"]["below19"]] or "none @1440")
print("below-19px @390:", [(r["route"], r["fonts390"]["below19"]) for r in done if "fonts390" in r and r["fonts390"]["below19"]] or "none @390")
print("below-19px @320:", [(r["route"], r["fonts320"]["below19"]) for r in done if "fonts320" in r and r["fonts320"]["below19"]] or "none @320")
