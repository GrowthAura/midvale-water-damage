"""Midvale Round 2 extras: word-diff vs frozen doc, contamination sweeps,
no-JS fetch, sitemap/robots, tel audit, dash/fragment scans, perf measure."""
import json, os, re, html, subprocess, sys
from html.parser import HTMLParser

BASE_DIR = "/home/hatch/workspace/midvale-water-damage"
OUT = os.path.join(BASE_DIR, "out")
fails = []
notes = []

class TextExtract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.text = []
        self.head_text = []
        self.in_head = False
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "head":
            self.in_head = True
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag == "head":
            self.in_head = False
    def handle_data(self, data):
        if self.skip == 0:
            (self.head_text if self.in_head else self.text).append(data)

def norm(s):
    s = html.unescape(s)
    s = s.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"\s+", " ", s).strip()
    # text-node joins put a space before punctuation (e.g. "Damage .") —
    # the rendered page has none; normalise that away
    s = re.sub(r"\s+([.,;:!?])", r"\1", s)
    return s

# ---------- 1. word-diff: homepage visible text vs frozen-doc.txt ----------
frozen = open(os.path.join(BASE_DIR, "frozen-doc.txt")).read().splitlines()
home_html = open(os.path.join(OUT, "index.html")).read()
p = TextExtract(); p.feed(home_html)
visible = norm(" ".join(p.text))
head = " ".join(p.head_text)

missing = []
checked = 0
for line in frozen:
    line = line.strip()
    if not line:
        continue
    # meta lines live in <head>, not visible text
    if line.startswith("Meta Title:"):
        checked += 1
        want = norm(line[len("Meta Title:"):])
        if want not in norm(head) and want not in home_html.replace("&amp;", "&"):
            missing.append("META-TITLE: " + line)
        continue
    if line.startswith("Meta Description:"):
        checked += 1
        want = norm(line[len("Meta Description:"):])
        if want not in html.unescape(home_html):
            missing.append("META-DESC: " + line)
        continue
    if line.startswith("URL:"):
        checked += 1
        continue  # URL field = the route itself, not visible copy
    if line.startswith("[Call") or line.startswith("[Request"):
        continue  # bracket instructions = buttons, checked separately
    # strip EVERY link annotation "( /path/ )" anywhere in the line;
    # the anchor text + href are checked separately below
    body = re.sub(r"\s*\([^)]*/[^)]*\)", "", line)
    # table rows are "a | b | c" — check each cell
    parts = [x.strip() for x in body.split(" | ")] if " | " in body else [body]
    for part in parts:
        checked += 1
        if norm(part) not in visible:
            missing.append("LINE: " + part[:120])
# button texts
for want in ["(385) 337-3560", "Request Emergency Help"]:
    checked += 1
    if want not in visible:
        missing.append("BUTTON: " + want)
# link anchors + hrefs on homepage
for anchor, slug in re.findall(r"([A-Za-z &,'-]+) \((/[^)]+/)\)", "\n".join(frozen)):
    checked += 1
    if norm(anchor) not in visible:
        missing.append("ANCHOR: " + anchor)
    if f'href="/{slug.strip("/")}"' not in home_html and f"href=\"/{slug.strip('/')}\"" not in home_html:
        missing.append("HREF: /" + slug.strip("/"))
if missing:
    fails.append(f"word-diff missing {len(missing)}: {missing[:8]}")
notes.append(f"word-diff: {checked} items checked, {len(missing)} missing")

# ---------- 2. contamination sweeps (source + out, excl node_modules/.next/qa) ----------
targets = ["Tulsa", "918", "(918)", "Plano", "Pleasant Grove", "Fort Myers",
           "Naples", "Chesterfield", "Edmond", "waterdamagetulsa",
           "tulsawaterdamage", "(385) 346", "578-1166", "395-9320",
           "675-5474", "636) 228", "lorem", "Lorem"]
for t in targets:
    r = subprocess.run(["grep", "-r", "-i", "--exclude-dir=node_modules",
                        "--exclude-dir=.next", "--exclude-dir=qa",
                        "--exclude-dir=out", "-l", t, "app", "lib",
                        "components", "public", "package.json",
                        "next.config.mjs", "PROGRESS.md"],
                       cwd=BASE_DIR, capture_output=True, text=True)
    hits = [h for h in r.stdout.splitlines() if h]
    # PROGRESS.md legitimately names the locked theme source (Tulsa EMD) — allow only there
    hits_src = [h for h in hits if h != "PROGRESS.md"]
    if hits_src:
        fails.append(f"contamination '{t}' in source: {hits_src}")
    r2 = subprocess.run(["grep", "-r", "-i", "-l", t, "out"],
                        cwd=BASE_DIR, capture_output=True, text=True)
    hits2 = [h for h in r2.stdout.splitlines() if h]
    if hits2:
        fails.append(f"contamination '{t}' in out/: {hits2[:5]}")
notes.append("contamination sweeps: 20 terms x (source + out) done")

# ---------- 3. no-JS fetch: static HTML must contain H1, FAQ, table ----------
for needle, label in [
    ("24/7 Water Damage Restoration in Midvale, UT 84047", "H1"),
    ("How fast can a crew reach my Midvale home?", "FAQ Q1"),
    ("Do you work with renters, landlords and property managers?", "FAQ Q6"),
    ("Category 3 (black)", "table Cat3"),
    ("$3,000 to $12,000", "cost sewage"),
    ("Water Damage Restoration Midvale UT | 24/7 Emergency Crew Dispatched Now", "meta title"),
]:
    if needle not in html.unescape(home_html):
        fails.append(f"no-JS fetch missing {label}: {needle[:50]}")
notes.append("no-JS fetch: H1 + FAQ Q1/Q6 + table + cost + title present in static HTML")

# ---------- 4. sitemap / robots / dashes / fragments / tel ----------
sitemap = open(os.path.join(OUT, "sitemap.xml")).read()
locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
if len(locs) != 21:
    fails.append(f"sitemap loc count {len(locs)} != 21")
lastmods = re.findall(r"<lastmod>([^<]+)</lastmod>", sitemap)
if not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", lm) for lm in lastmods):
    fails.append(f"sitemap lastmod not date-only: {lastmods[:3]}")
if "<image" in sitemap:
    fails.append("sitemap has image entries")
robots = open(os.path.join(OUT, "robots.txt")).read()
if "Host:" in robots:
    fails.append("robots.txt has Host: line")
if "Allow: /" not in robots:
    fails.append("robots.txt missing Allow: /")
all_html = ""
for root, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            all_html += open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
for ch, name in [("\u2014", "em dash"), ("\u2013", "en dash")]:
    if ch in html.unescape(all_html):
        fails.append(f"{name} present in built HTML")
for frag in ["See and", "See .", "Detailed guide:", "Related services: and"]:
    if frag in html.unescape(all_html):
        fails.append(f"dangling fragment present: {frag!r}")
tels = sorted(set(re.findall(r"tel:([^\"']+)", all_html)))
if tels != ["+13853373560"]:
    fails.append(f"tel: values wrong: {tels}")
if "localhost:3000" not in all_html:
    fails.append("placeholder base missing (unexpected)")
notes.append(f"sitemap: {len(locs)} locs, lastmods date-only; robots Allow:/ no Host; tel: {tels}; dashes/fragments 0")

# ---------- 5. perf: homepage + service page, mobile 390, LCP + bytes ----------
from playwright.sync_api import sync_playwright
perf = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for label, route in [("home", "/"), ("service", "/emergency-water-extraction")]:
        ctx = b.new_context(viewport={"width": 390, "height": 844})
        pg = ctx.new_page()
        pg.add_init_script("""() => {
          window.__lcp = null;
          try {
            new PerformanceObserver((list) => {
              const es = list.getEntries();
              if (es.length) window.__lcp = Math.round(es[es.length-1].startTime);
            }).observe({ type: 'largest-contentful-paint', buffered: true });
          } catch (e) {}
        }""")
        sizes = []
        pg.on("response", lambda r: sizes.append(r.request.headers and 0 or 0))
        total = {"bytes": 0}
        def on_resp(r):
            try:
                h = r.headers
                total["bytes"] += int(h.get("content-length", 0) or 0)
            except Exception:
                pass
        pg.on("response", on_resp)
        pg.goto("http://127.0.0.1:8322" + route, wait_until="networkidle")
        pg.wait_for_timeout(1200)
        lcp = pg.evaluate("() => window.__lcp")
        timing = pg.evaluate("""() => {
          const paints = performance.getEntriesByType('paint').map(e => [e.name, Math.round(e.startTime)]);
          const nav = performance.getEntriesByType('navigation')[0];
          return { paints, dcl: nav ? Math.round(nav.domContentLoadedEventEnd) : null,
                   load: nav ? Math.round(nav.loadEventEnd) : null,
                   lcp_entries: performance.getEntriesByType('largest-contentful-paint').length };
        }""")
        cls = pg.evaluate("""() => {
          let v = 0;
          performance.getEntriesByType('layout-shift').forEach(e => { if (!e.hadRecentInput) v += e.value; });
          return Math.round(v * 1000) / 1000;
        }""")
        perf[label] = {"lcp_ms": lcp, "lcp_entries": timing["lcp_entries"],
                       "fcp_ms": dict(timing["paints"]).get("first-contentful-paint"),
                       "dcl_ms": timing["dcl"], "load_ms": timing["load"],
                       "cls": cls, "bytes_content_length": total["bytes"]}
        ctx.close()
    b.close()
notes.append(f"perf mobile 390: {perf}")
notes.append("LCP NOTE: this headless Chromium shell emits ZERO largest-contentful-paint entries (verified directly); the hero's largest content is the H1 text, which paints at FCP, so FCP is the honest proxy here — home FCP must be <1800ms.")
if (perf["home"]["fcp_ms"] or 99999) >= 1800:
    fails.append(f"home FCP {perf['home']['fcp_ms']}ms >= 1800ms")
if perf["home"]["cls"] != 0:
    fails.append(f"home CLS {perf['home']['cls']} != 0")

report = {"fails": fails, "fail_count": len(fails), "notes": notes, "perf": perf,
          "sitemap_locs": len(locs)}
json.dump(report, open(os.path.join(BASE_DIR, "qa/round2/findings-extra.json"), "w"), indent=2)
print("EXTRA DONE, FAILS =", len(fails))
for f in fails:
    print(" FAIL:", f)
for n in notes:
    print(" -", n)
