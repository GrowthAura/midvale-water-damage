#!/usr/bin/env python3
"""Definitive click test: use wait_for_url (not networkidle) after each
client-side navigation, so the URL is read only after the nav commits."""
import subprocess, time, signal
from playwright.sync_api import sync_playwright

PORT = 8329
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
        pg.wait_for_url("**/emergency-water-extraction", timeout=15000)
        time.sleep(0.5)
        print("after card click:", pg.url, "| h1:", pg.evaluate("() => document.querySelector('h1').textContent"))
        pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        pg.click(".site-footer a[href='/midvale-water-damage/locations/cottonwood-heights-ut']")
        pg.wait_for_url("**/locations/cottonwood-heights-ut", timeout=15000)
        time.sleep(0.5)
        print("after footer click:", pg.url, "| h1:", pg.evaluate("() => document.querySelector('h1').textContent"))
        pg.click(".breadcrumb a >> nth=0")
        # NOTE: the visible breadcrumb Home href is "/midvale-water-damage"
        # (no trailing slash — Next basePath form); the URL lands without
        # the slash while the canonical keeps it. Wait on the H1 instead.
        pg.wait_for_selector("h1", timeout=15000)
        time.sleep(0.5)
        assert "24/7 Water Damage Restoration in Midvale" in pg.evaluate("() => document.querySelector('h1').textContent")
        print("after breadcrumb Home:", pg.url, "| h1:", pg.evaluate("() => document.querySelector('h1').textContent"))
        # mobile: menu open -> nav link click
        pg2 = b.new_page(viewport={"width": 390, "height": 844})
        pg2.goto(BASE + "/", wait_until="networkidle", timeout=30000)
        pg2.click(".menu-btn")
        pg2.wait_for_selector(".main-nav.open", timeout=5000)
        pg2.click(".main-nav.open a[href='/midvale-water-damage/sewage-backup-cleanup']")
        pg2.wait_for_url("**/sewage-backup-cleanup", timeout=15000)
        time.sleep(0.5)
        print("mobile menu nav:", pg2.url, "| h1:", pg2.evaluate("() => document.querySelector('h1').textContent"))
        b.close()
    print("CLICKS OK")
finally:
    srv.send_signal(signal.SIGTERM)
