import subprocess, time, signal
from playwright.sync_api import sync_playwright
srv = subprocess.Popen(["python3", "qa/linkfix-serve.py", "8330"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.goto("http://127.0.0.1:8330/midvale-water-damage/", wait_until="networkidle")
        pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.8)
        pg.screenshot(path="qa/seo-fix1-footer-390.png")
        pg.close()
        pg = b.new_page(viewport={"width": 320, "height": 568})
        pg.goto("http://127.0.0.1:8330/midvale-water-damage/emergency-water-extraction", wait_until="networkidle")
        time.sleep(0.5)
        pg.screenshot(path="qa/seo-fix1-hero-320.png")
        b.close()
    print("shots saved")
finally:
    srv.send_signal(signal.SIGTERM)
