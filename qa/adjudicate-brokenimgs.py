#!/usr/bin/env python3
"""Broken-image adjudication for Midvale fill+19px round (2026-11-13).
Targeted re-check of every image flagged broken by the main render run
(and by the cancelled qa/fullpage-shoot.log): homepage desktop/m390,
basement m390, plus any other flagged page/src in
qa/verify-fill-19px-render.json.
Method per flagged image: load page, scroll SLOWLY (400px steps, 300ms),
scrollIntoView() the exact <img>, wait 2s, record complete/naturalWidth;
record every network request for local image URLs and its HTTP status.
Also curls each flagged file from the local server (expect 200) and
compares out/ bytes vs public/ bytes.
Writes qa/brokenimgs-adjudication.json. TEST ONLY (no site files modified).
"""
import json, os, subprocess, sys, time, socket, hashlib
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
PORT = 8933
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

render = json.load(open(os.path.join(ROOT, "qa", "verify-fill-19px-render.json")))
flagged = {}  # route -> set of srcs
for p in render["pages"]:
    for key in ("img_broken_render", "img_broken_390"):
        for i in p.get(key, []):
            flagged.setdefault(p["route"], set()).add(i["src"])
# also the cancelled shoot log's flagged pages (no srcs listed there, so re-check ALL imgs on those pages)
for r in ("/", "/basement-flooding-cleanup"):
    flagged.setdefault(r, set())
print("flagged routes:", {r: sorted(s) for r, s in flagged.items()}, flush=True)

srv = subprocess.Popen([sys.executable, os.path.join(ROOT, "qa", "linkfix-serve.py"), str(PORT)],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       env={**os.environ, "TMPDIR": os.path.join(ROOT, "qa", "tmpdir")})
assert wait_port(PORT), "server did not start"

def url(route):
    return BASE + "/" if route == "/" else BASE + route + ".html"

out = {"pages": {}, "curl": {}}
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--disable-dev-shm-usage"])
        for route, srcs in flagged.items():
            rec = {"route": route, "flagged_srcs": sorted(srcs), "img_requests": {}, "after_slow_scroll": []}
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            page.on("request", lambda r: rec["img_requests"].__setitem__(r.url, "requested") if "/images/" in r.url else None)
            page.on("response", lambda r: rec["img_requests"].__setitem__(r.url, f"HTTP {r.status}") if "/images/" in r.url else None)
            page.on("requestfailed", lambda r: rec["img_requests"].__setitem__(r.url, f"FAILED {r.failure}") if "/images/" in r.url else None)
            page.goto(url(route), wait_until="domcontentloaded", timeout=30000)
            page.wait_for_selector("h1", timeout=15000)
            page.wait_for_timeout(800)
            # slow scroll through the whole page
            page.evaluate("""async () => {
                const h = document.documentElement.scrollHeight;
                for (let y = 0; y < h; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 300)); }
                window.scrollTo(0, document.documentElement.scrollHeight);
                await new Promise(r => setTimeout(r, 800));
            }""")
            page.wait_for_timeout(1500)
            # scroll each flagged img into view individually and wait
            for src in sorted(srcs):
                page.evaluate("""(src) => {
                    const img = [...document.images].find(i => i.getAttribute('src') === src);
                    if (img) img.scrollIntoView({block: 'center'});
                }""", src)
                page.wait_for_timeout(2000)
            # final state of ALL images on the page
            rec["after_slow_scroll"] = page.evaluate("""() => [...document.images].map(i => ({
                src: i.getAttribute('src'), loading: i.getAttribute('loading'),
                complete: i.complete, naturalWidth: i.naturalWidth}))""")
            rec["still_broken"] = [i for i in rec["after_slow_scroll"] if not i["complete"] or i["naturalWidth"] == 0]
            ctx.close()
            out["pages"][route] = rec
            print(f"adjudicated {route}: flagged={len(srcs)} still_broken={len(rec['still_broken'])} "
                  f"img_requests={len(rec['img_requests'])}", flush=True)
            for b in rec["still_broken"]:
                print("  STILL BROKEN:", b, flush=True)
        browser.close()
        # curl each flagged file + compare out/ vs public/ bytes
        for route, srcs in flagged.items():
            for src in sorted(srcs):
                rel = src[len("/midvale-water-damage/"):] if src.startswith("/midvale-water-damage/") else src.lstrip("/")
                u = BASE + "/" + rel
                r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{size_download}", u],
                                   capture_output=True, text=True, timeout=30)
                out_p = os.path.join(ROOT, "out", rel)
                pub_p = os.path.join(ROOT, "public", rel)
                def h(p):
                    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12] if os.path.exists(p) else None
                out["curl"][src] = {"http": r.stdout.strip(), "out_exists": os.path.exists(out_p),
                                    "out_sha": h(out_p), "public_sha": h(pub_p),
                                    "bytes_match": h(out_p) == h(pub_p) and h(out_p) is not None}
        print("curl:", json.dumps(out["curl"], indent=1), flush=True)
finally:
    srv.terminate()

json.dump(out, open(os.path.join(ROOT, "qa", "brokenimgs-adjudication.json"), "w"), indent=1)
n_still = sum(len(v["still_broken"]) for v in out["pages"].values())
n_flagged = sum(len(v["flagged_srcs"]) for v in out["pages"].values())
print(f"ADJUDICATION: {n_flagged} flagged srcs re-checked, {n_still} still broken after slow scroll + scrollIntoView", flush=True)
print(f"curl non-200: {[s for s, c in out['curl'].items() if not c['http'].startswith('200')]}", flush=True)
print(f"bytes mismatch: {[s for s, c in out['curl'].items() if not c['bytes_match']]}", flush=True)
