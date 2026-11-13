#!/usr/bin/env python3
"""Contact radios + clicks, split runs. Usage: reverify-contact.py <radios|clicks>"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
BASE = "http://127.0.0.1:8410/midvale-water-damage"
PART = sys.argv[1]
JS_RADIO = """() => {
  const labels = [...document.querySelectorAll('.contact-form .radio-row label')].map(e => {
    const b = e.getBoundingClientRect(); return {text: e.innerText.trim(), h: Math.round(b.height)};
  });
  const fields = [...document.querySelectorAll('.contact-form input, .contact-form textarea')].map(e => (e.type||e.tagName)+':'+(e.name||e.placeholder||''));
  const submit = document.querySelector('.contact-form button[type=submit]');
  return {labels, fields, submitText: submit ? submit.innerText.trim() : null};
}"""
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(args=["--single-process", "--no-zygote", "--disable-gpu", "--disable-dev-shm-usage"])
    ctx = br.new_context(viewport={"width": 1440, "height": 900})
    ctx.route("**/*google*maps*", lambda route: route.abort())
    page = ctx.new_page()
    if PART == "radios":
        page.goto(BASE + "/contact", wait_until="domcontentloaded")
        page.wait_for_timeout(900)
        res = page.evaluate(JS_RADIO)
    else:
        page.goto(BASE + "/", wait_until="domcontentloaded")
        page.wait_for_timeout(700)
        page.click("main a[href='/midvale-water-damage/burst-pipe-water-damage'] >> nth=0")
        page.wait_for_timeout(600)
        res["clicks"] = [{"step": "card->burst-pipe", "url": page.url,
                          "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")}]
        json.dump(res, open(os.path.join(ROOT, "qa", "reverify-contact-clicks.json"), "w"), indent=1)
        page.click("a.brand")
        page.wait_for_url("**/midvale-water-damage", timeout=10000)
        page.wait_for_timeout(600)
        res["clicks"].append({"step": "logo->home", "url": page.url})
        json.dump(res, open(os.path.join(ROOT, "qa", "reverify-contact-clicks.json"), "w"), indent=1)
        page.goto(BASE + "/emergency-water-extraction", wait_until="domcontentloaded")
        page.wait_for_timeout(700)
        page.click("footer a[href='/midvale-water-damage/mold-remediation'] >> nth=0")
        page.wait_for_timeout(600)
        res["clicks"].append({"step": "footer->mold", "url": page.url,
                              "h1": page.evaluate("() => document.querySelector('main h1')?.innerText")})
    ctx.close()
    br.close()
json.dump(res, open(os.path.join(ROOT, "qa", f"reverify-contact-{PART}.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
