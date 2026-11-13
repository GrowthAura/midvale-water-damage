#!/usr/bin/env python3
"""Follow-up to qa/verify-fill-19px-render.py, which crashed AFTER the per-page
loop (my JS syntax error in the click section — one stray paren) before the
click-navigation and contact-form checks ran. This script runs ONLY those two
checks, fresh, against the same export, and merges results into
qa/verify-fill-19px-render.json under keys 'clicks' and 'contact_form'.
"""
import json, os, subprocess, time, socket, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
PORT = 8934
BASE = f"http://127.0.0.1:{PORT}/midvale-water-damage"

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

def url(route):
    return BASE + "/" if route == "/" else BASE + route + ".html"

H1_EVAL = "() => { const h = document.querySelector('h1'); return h ? h.innerText : ''; }"
clicks = []
form = None
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--disable-dev-shm-usage"])
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        # 5 real clicks on homepage card links
        for i in range(5):
            page.goto(url("/"), wait_until="domcontentloaded", timeout=30000)
            page.wait_for_selector(".card-wrap-link", timeout=15000)
            link = page.query_selector_all(".card-wrap-link")[i]
            href = link.get_attribute("href")
            link.click()
            page.wait_for_selector("h1", timeout=15000)
            page.wait_for_timeout(400)
            clicks.append({"n": i + 1, "kind": "card-link", "href": href, "landed": page.url,
                           "subpath_kept": "/midvale-water-damage/" in page.url,
                           "h1": page.evaluate(H1_EVAL)})
            print("click", clicks[-1], flush=True)
        # 1 real click on a body link from an inner page
        page.goto(url("/emergency-water-extraction"), wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector(".body-link", timeout=15000)
        bl = page.query_selector(".body-link")
        bh = bl.get_attribute("href")
        bl.click()
        page.wait_for_selector("h1", timeout=15000)
        page.wait_for_timeout(400)
        clicks.append({"n": 6, "kind": "body-link", "href": bh, "landed": page.url,
                       "subpath_kept": "/midvale-water-damage/" in page.url,
                       "h1": page.evaluate(H1_EVAL)})
        print("click", clicks[-1], flush=True)
        ctx.close()
        # contact form
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(url("/contact"), wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector(".contact-form", timeout=15000)
        page.wait_for_timeout(400)
        form = page.evaluate("""() => {
          const f = document.querySelector('.contact-form');
          const fields = [...f.querySelectorAll('input, textarea, select')].map(e => ({
            tag: e.tagName.toLowerCase(), type: e.getAttribute('type'), name: e.getAttribute('name'),
            id: e.id, label: (f.querySelector('label[for="' + e.id + '"]') || {}).innerText || '',
            fontSize: getComputedStyle(e).fontSize}));
          const submit = [...f.querySelectorAll('button, input[type=submit]')].map(b => (b.innerText || b.value || '').trim());
          return {fields, submit, action: f.getAttribute('action'), method: f.getAttribute('method'),
                  notice: (f.innerText || '').slice(0, 400)};
        }""")
        print("CONTACT FORM:", json.dumps(form, indent=1), flush=True)
        ctx.close()
        browser.close()
finally:
    srv.terminate()

path = os.path.join(ROOT, "qa", "verify-fill-19px-render.json")
d = json.load(open(path))
d["clicks"] = clicks
d["contact_form"] = form
json.dump(d, open(path, "w"), indent=1)
print(f"clicks: {len(clicks)}, subpath kept: {sum(1 for c in clicks if c['subpath_kept'])}/{len(clicks)}", flush=True)
print(f"form fields: {len(form['fields'])}, submit: {form['submit']}", flush=True)
