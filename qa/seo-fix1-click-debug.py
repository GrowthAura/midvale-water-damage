#!/usr/bin/env python3
"""Debug the footer-location click: home -> service card -> footer location
link -> breadcrumb Home, with per-step URL + element diagnostics."""
import subprocess, time, signal
from playwright.sync_api import sync_playwright

PORT = 8328
BASE = f"http://127.0.0.1:{PORT}/midvale-water-damage"
srv = subprocess.Popen(["python3", "qa/linkfix-serve.py", str(PORT)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(BASE + "/", wait_until="networkidle", timeout=30000)
        print("start:", pg.url)
        pg.click(".card-wrap-link[href='/midvale-water-damage/emergency-water-extraction']")
        pg.wait_for_load_state("networkidle")
        print("after card click:", pg.url, "| h1:", pg.evaluate("() => document.querySelector('h1').textContent"))
        info = pg.evaluate("""() => {
          const a = document.querySelector(".site-footer a[href='/midvale-water-damage/locations/cottonwood-heights-ut']");
          if (!a) return {found: false};
          const r = a.getBoundingClientRect();
          const cs = getComputedStyle(a);
          return {found: true, href: a.getAttribute('href'), rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)], display: cs.display, visibility: cs.visibility,
                  navText: a.closest('nav') ? a.closest('nav').getAttribute('aria-label') : null};
        }""")
        print("footer link info:", info)
        pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        pg.click(".site-footer a[href='/midvale-water-damage/locations/cottonwood-heights-ut']")
        pg.wait_for_load_state("networkidle")
        print("after footer click:", pg.url, "| h1:", pg.evaluate("() => document.querySelector('h1').textContent"))
        pg.click(".breadcrumb a >> nth=0")
        pg.wait_for_load_state("networkidle")
        print("after breadcrumb Home:", pg.url, "| h1:", pg.evaluate("() => document.querySelector('h1').textContent"))
        # also: plain <a> click via dispatch (no Playwright scrolling) as a control
        pg.goto(BASE + "/emergency-water-extraction", wait_until="networkidle", timeout=30000)
        pg.evaluate("() => document.querySelector(\".site-footer a[href='/midvale-water-damage/locations/cottonwood-heights-ut']\").click()")
        pg.wait_for_load_state("networkidle")
        print("after JS .click() on footer link:", pg.url)
        b.close()
finally:
    srv.send_signal(signal.SIGTERM)
