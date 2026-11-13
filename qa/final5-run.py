#!/usr/bin/env python3
"""W4 — Midvale final friendly check Stage 5: real-click nav + speed + image screenshots.
READ-ONLY on site source. Writes qa/final5-clicks-speed.json + qa/final5-img-*.png only.
Local server: http://127.0.0.1:8350/midvale-water-damage/ (subpath mirror of fresh out/ export).
"""
import json, statistics, time, os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8350/midvale-water-damage"
OUTDIR = "/home/hatch/workspace/midvale-water-damage/qa"
os.makedirs(OUTDIR, exist_ok=True)

PERF_INIT = """
window.__perf = {fcp: null, lcp: null, cls: 0, lcpEl: null, lcpSrc: null};
try {
  new PerformanceObserver(e => { for (const x of e.getEntries()) { if (x.name === 'first-contentful-paint') window.__perf.fcp = x.startTime; } }).observe({type:'paint', buffered:true});
  new PerformanceObserver(e => { const es = e.getEntries(); const last = es[es.length-1];
    window.__perf.lcp = last.startTime;
    if (last.element) { const el = last.element;
      window.__perf.lcpEl = el.tagName + (el.id ? '#'+el.id : '') + (el.className && typeof el.className==='string' ? '.'+el.className.trim().split(/\\s+/).join('.') : '');
      window.__perf.lcpSrc = el.currentSrc || el.src || null; }
    else if (last.url) { window.__perf.lcpEl = 'text/other'; window.__perf.lcpSrc = last.url; }
  }).observe({type:'largest-contentful-paint', buffered:true});
  new PerformanceObserver(e => { for (const x of e.getEntries()) { if (!x.hadRecentInput) window.__perf.cls += x.value; } }).observe({type:'layout-shift', buffered:true});
} catch (err) { window.__perfErr = String(err); }
"""

IMAGES = [
    # (file rel to /images/, alt text from source, kind)
    ("heroes/basement-flooding-spring-snowmelt-utah.webp",
     "Spring snowmelt water pooling at a home foundation as a downspout discharges, with melting snow piles and snowy hills behind",
     "blog hero (alt fixed this round)"),
    ("cards/cottonwood-heights-ut.webp",
     "Winding canyon highway with cars through steep rocky autumn slopes in Cottonwood Canyon, Utah",
     "location card (alt fixed this round)"),
    ("heroes/commercial-water-damage.webp",
     "After-hours drying in a dark Midvale restaurant, air movers running",
     "service hero (was B&W in old round — confirm colour)"),
    ("heroes/burst-pipe-water-damage.webp",
     "Split copper pipe spraying water inside a dark wall cavity",
     "service hero"),
    ("heroes/sewage-backup-cleanup.webp",
     "Crew in protective gear cleaning a sewage backup in a Midvale bathroom",
     "service hero"),
    ("heroes/storm-flood-damage.webp",
     "Storm runoff flooding a Midvale garage at night",
     "service hero"),
    ("body/burst-pipe-water-damage-1.webp",
     "A frozen copper water supply pipe split open in a basement, coated in frost with icicles and water spraying from the break.",
     "body image"),
    ("body/mold-remediation-2.webp",
     "A worker in a white protective suit, respirator and blue gloves treating a room with a fogging hose",
     "body image"),
    ("body/water-heater-leak-cleanup-1.webp",
     "A tall white tank water heater with copper pipes beside a washer and dryer in a basement utility area, with a puddle at its base.",
     "body image"),
    ("cards/south-salt-lake-ut.webp",
     "Apartment blocks and warehouse buildings in South Salt Lake, Utah",
     "location card"),
    ("cards/magna-ut.webp",
     "Older brick homes and storefronts on historic Main Street in Magna, Utah",
     "location card"),
    ("heroes/can-mold-grow-in-utah.webp",
     "Mold growth on damp drywall in a dark Midvale basement corner",
     "blog hero"),
]

SPEED_PAGES = [
    ("homepage", "/"),
    ("service: emergency-water-extraction", "/emergency-water-extraction"),
    ("service: burst-pipe-water-damage", "/burst-pipe-water-damage"),
    ("service: mold-remediation", "/mold-remediation"),
    ("location: cottonwood-heights-ut", "/locations/cottonwood-heights-ut"),
    ("resource: frozen-pipes-midvale", "/resources/frozen-pipes-midvale"),
]

def h1_of(page):
    try:
        return page.locator("h1").first.inner_text().strip()
    except Exception as e:
        return f"H1 READ ERROR: {e}"

def subpath_kept(url):
    return url.startswith(BASE + "/") or url.rstrip("/") == BASE

results = {"partA_clicks": [], "partB_speed": [], "partC_images": [], "notes": []}

with sync_playwright() as p:
    browser = p.chromium.launch()

    # ---------------- PART A ----------------
    def click_test(name, start_path, viewport, click_fn, expect_path_contains=None):
        ctx = browser.new_context(viewport=viewport)
        page = ctx.new_page()
        start_url = BASE + start_path
        page.goto(start_url, wait_until="load")
        page.wait_for_timeout(800)
        clicked_desc, extra = click_fn(page)
        page.wait_for_timeout(1200)
        try:
            page.wait_for_load_state("load", timeout=8000)
        except Exception:
            pass
        end_url = page.url
        rec = {
            "test": name,
            "start_url": start_url,
            "clicked_element": clicked_desc,
            "end_url": end_url,
            "end_h1": h1_of(page),
            "subpath_kept": subpath_kept(end_url),
            "http_status": page.evaluate("() => performance.getEntriesByType('navigation')[0]?.responseStatus ?? null"),
        }
        if extra:
            rec.update(extra)
        results["partA_clicks"].append(rec)
        print(json.dumps(rec, indent=1))
        ctx.close()
        return rec

    # A1: homepage service card -> service page
    def a1(page):
        loc = page.locator('a.card-wrap-link[href="/midvale-water-damage/emergency-water-extraction"]')
        if loc.count() == 0:
            loc = page.locator('main a[href="/midvale-water-damage/emergency-water-extraction"]').first
        else:
            loc = loc.first
        desc = loc.evaluate("el => el.outerHTML.slice(0,220)")
        loc.click()
        return desc, {"selector_used": "card link to emergency-water-extraction"}
    click_test("A1 homepage service card", "/", {"width": 1440, "height": 900}, a1)

    # A2: footer location link (Cottonwood Heights)
    def a2(page):
        loc = page.locator('footer a[href="/midvale-water-damage/locations/cottonwood-heights-ut"]').first
        desc = loc.evaluate("el => el.outerHTML.slice(0,220)")
        loc.scroll_into_view_if_needed()
        loc.click()
        return desc, {}
    click_test("A2 footer location link Cottonwood Heights", "/", {"width": 1440, "height": 900}, a2)

    # A3: breadcrumb Home on service page -> homepage
    def a3(page):
        loc = page.locator('nav.breadcrumb a').first
        desc = loc.evaluate("el => el.outerHTML.slice(0,200)")
        loc.click()
        return desc, {}
    click_test("A3 breadcrumb Home on service page", "/emergency-water-extraction", {"width": 1440, "height": 900}, a3)

    # A4: mobile menu link at 390px
    def a4(page):
        page.locator("button.menu-btn").click()
        page.wait_for_timeout(600)
        menu_open = page.locator("#main-nav").evaluate("el => getComputedStyle(el).display + '|' + el.getAttribute('aria-hidden')")
        # mobile nav carries only 3 links (Home, Emergency, Sewage) — verified in out/index.html
        loc = page.locator('#main-nav a[href="/midvale-water-damage/sewage-backup-cleanup"]').first
        desc = loc.evaluate("el => el.outerHTML.slice(0,200)")
        loc.click()
        return desc, {"menu_state_before_click": menu_open}
    click_test("A4 mobile menu link (390px)", "/", {"width": 390, "height": 844}, a4)

    # A5: footer About link
    def a5(page):
        loc = page.locator('footer a[href="/midvale-water-damage/about"]').first
        desc = loc.evaluate("el => el.outerHTML.slice(0,200)")
        loc.scroll_into_view_if_needed()
        loc.click()
        return desc, {}
    click_test("A5 footer About link", "/", {"width": 1440, "height": 900}, a5)

    # A6: body-copy internal link on burst-pipe page -> water-leak-detection
    # (genuine <p>-wrapped body link, verified live in DOM; the earlier
    #  emergency-water-extraction anchor on this page is header/footer nav only)
    def a6(page):
        loc = page.locator('main p a[href="/midvale-water-damage/water-leak-detection"]').first
        desc = loc.evaluate("el => 'text=' + el.textContent.trim() + ' | context=' + el.closest('p').textContent.trim().slice(0,180)")
        loc.scroll_into_view_if_needed()
        loc.click()
        return desc, {}
    click_test("A6 body-copy link on burst-pipe page", "/burst-pipe-water-damage", {"width": 1440, "height": 900}, a6)

    # A7: sticky call-bar tel link — verify href (clicking tel: does not navigate in headless Chromium)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(BASE + "/", wait_until="load")
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(800)
    bar = page.locator(".sticky-bar")
    bar_class = bar.evaluate("el => el.className")
    tel = page.locator('.sticky-bar a[href^="tel:"]').first
    href = tel.get_attribute("href")
    href_ok = href == "tel:+13853373560"
    url_before = page.url
    try:
        tel.click(timeout=5000)
        page.wait_for_timeout(800)
        click_outcome = "clicked, no navigation (expected for tel: in headless Chromium)"
    except Exception as e:
        click_outcome = f"click raised: {type(e).__name__}: {str(e)[:200]}"
    rec = {
        "test": "A7 sticky call-bar phone link",
        "start_url": BASE + "/",
        "clicked_element": ".sticky-bar a[href^='tel:'] text=" + (tel.inner_text().strip() if tel.count() else "?"),
        "sticky_bar_class_after_scroll": bar_class,
        "tel_href": href,
        "tel_href_expected": "tel:+13853373560",
        "tel_href_correct": href_ok,
        "click_outcome": click_outcome,
        "end_url": page.url,
        "url_unchanged": page.url == url_before,
        "end_h1": h1_of(page),
        "subpath_kept": subpath_kept(page.url),
    }
    results["partA_clicks"].append(rec)
    print(json.dumps(rec, indent=1))
    ctx.close()

    # ---------------- PART B ----------------
    def measure_once(page, path):
        page.goto(BASE + path, wait_until="load")
        page.wait_for_timeout(4500)  # let LCP settle, images decode
        return page.evaluate("() => window.__perf")

    for label, path in SPEED_PAGES:
        for vp_name, vp, throttle in [
            ("desktop-1440", {"width": 1440, "height": 900}, "cpu-x4, no network throttle"),
            ("mobile-390", {"width": 390, "height": 844}, "cpu-x4 + Fast 3G (1.6Mbps/750kbps, 150ms RTT)"),
        ]:
            runs = []
            for run_i in range(3):
                ctx = browser.new_context(viewport=vp, device_scale_factor=1,
                                          is_mobile=(vp_name == "mobile-390"))
                page = ctx.new_page()
                page.add_init_script(PERF_INIT)
                cdp = ctx.new_cdp_session(page)
                cdp.send("Network.enable")
                if vp_name == "mobile-390":
                    cdp.send("Network.emulateNetworkConditions", {
                        "offline": False, "latency": 150,
                        "downloadThroughput": 1.6 * 1024 * 1024 / 8,
                        "uploadThroughput": 750 * 1024 / 8})
                cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
                try:
                    m = measure_once(page, path)
                except Exception as e:
                    m = {"error": str(e)}
                runs.append(m)
                ctx.close()
            fcp = [r["fcp"] for r in runs if r.get("fcp") is not None]
            lcp = [r["lcp"] for r in runs if r.get("lcp") is not None]
            cls = [r["cls"] for r in runs if r.get("cls") is not None]
            lcp_els = [r.get("lcpEl") for r in runs if r.get("lcpEl")]
            lcp_srcs = [r.get("lcpSrc") for r in runs if r.get("lcpSrc")]
            row = {
                "page": label,
                "path": path,
                "viewport": vp_name,
                "conditions": throttle,
                "runs": runs,
                "fcp_ms_median": round(statistics.median(fcp), 0) if fcp else None,
                "lcp_ms_median": round(statistics.median(lcp), 0) if lcp else None,
                "cls_median": round(statistics.median(cls), 4) if cls else None,
                "lcp_element": statistics.mode(lcp_els) if lcp_els else None,
                "lcp_element_all_runs": lcp_els,
                "lcp_src": statistics.mode(lcp_srcs) if lcp_srcs else None,
            }
            results["partB_speed"].append(row)
            print(label, vp_name, "FCP", row["fcp_ms_median"], "LCP", row["lcp_ms_median"], "CLS", row["cls_median"], "LCP-el", row["lcp_element"])

    # ---------------- PART C screenshots ----------------
    ctx = browser.new_context(viewport={"width": 1600, "height": 1000})
    page = ctx.new_page()
    for i, (rel, alt, kind) in enumerate(IMAGES, 1):
        url = f"{BASE}/images/{rel}"
        page.goto(url, wait_until="load")
        page.wait_for_timeout(500)
        dims = page.evaluate("""() => { const img = document.querySelector('img');
            return img ? {w: img.naturalWidth, h: img.naturalHeight} : null; }""")
        shot = f"{OUTDIR}/final5-img-{i:02d}-{rel.split('/')[-1].replace('.webp', '')}.png"
        page.screenshot(path=shot, full_page=True)
        # objective colour support: mean saturation via PIL on the source file
        sat = None
        try:
            from PIL import Image
            import colorsys
            im = Image.open(f"/home/hatch/workspace/midvale-water-damage/public/images/{rel}").convert("RGB")
            im_small = im.resize((80, 80))
            px = list(im_small.getdata())
            sats = [colorsys.rgb_to_hsv(r/255, g/255, b/255)[1] for r, g, b in px]
            sat = round(sum(sats)/len(sats), 3)
        except Exception as e:
            sat = f"PIL error: {e}"
        results["partC_images"].append({
            "n": i, "file": f"public/images/{rel}", "kind": kind, "alt": alt,
            "served_url": url, "natural_px": dims, "screenshot": shot,
            "mean_saturation_0to1": sat,
            "shows": None, "alt_matches": None, "alt_match_why": None,
            "topic_fit": None, "topic_fit_why": None,
        })
        print(i, rel, dims, "sat", sat)
    ctx.close()
    browser.close()

results["meta"] = {
    "base": BASE,
    "caveat": "LOCAL LAB numbers only — served from 127.0.0.1 on this VM, not field data and not the live GitHub Pages host. Desktop runs: CPU x4, no network throttle. Mobile runs: CPU x4 + Fast 3G emulation.",
    "date": time.strftime("%Y-%m-%d %H:%M %Z"),
}
with open(f"{OUTDIR}/final5-clicks-speed.json", "w") as f:
    json.dump(results, f, indent=2)
print("WROTE", f"{OUTDIR}/final5-clicks-speed.json")
