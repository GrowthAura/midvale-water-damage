#!/usr/bin/env python3
"""Re-verify follow-up: visible-text-only verbatim + fullness + tables + links + paren.
Writes qa/reverify-visible.json."""
import json, re, html, urllib.request, urllib.error
from collections import Counter as C
from pathlib import Path

ROOT = Path.home() / "workspace/midvale-water-damage"
OUT = ROOT / "out"
SITE = "https://growthaura.github.io/midvale-water-damage"
data = json.loads((ROOT / "lib/pages-data.json").read_text())
pages = data["pages"]
problems = []
def add(s, c, p, d): problems.append({"severity": s, "check": c, "page": p, "detail": d})
def strip_tags(s): return html.unescape(re.sub(r"<[^>]+>", " ", s))
def norm_tokens(t): return re.findall(r"[a-z0-9']+", t.lower())
def visible_main(raw):
    m = re.search(r"<main[^>]*>(.*?)</main>", raw, re.S)
    h = m.group(1) if m else ""
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    return h, strip_tags(h)
def nt(s): return norm_tokens(re.sub(r"\([^)]*?/[^)]*?\)", " ", str(s)))
def doc_tokens(p):
    toks = []
    toks += nt(p.get("h1", "") or "")
    toks += nt(p.get("intro", "") or "")
    for b in p.get("blocks", []):
        if isinstance(b, dict):
            if "text" in b: toks += nt(b["text"])
            for seg in b.get("segments", []):
                toks += nt(seg.get("t", "")) if isinstance(seg, dict) else nt(seg)
            for row in b.get("rows", []) or []:
                for c in row: toks += nt(str(c))
            for cell in b.get("cells", []) or []: toks += nt(str(cell))
    for f in p.get("faqs", []):
        toks += nt(f.get("q", "")); toks += nt(f.get("a", ""))
    return toks

def route_file(r): return OUT / "index.html" if r == "/" else OUT / (r.strip("/") + ".html")

res = {}
for p in pages:
    route = p["route"]; raw = route_file(route).read_text()
    mh, mt = visible_main(raw)
    vis = C(norm_tokens(mt)); doc = C(doc_tokens(p))
    missing = sum((doc - vis).values())
    # tables rendered
    tables = len(re.findall(r"<table", mh))
    # links in main
    hrefs = re.findall(r'href="([^"]+)"', mh)
    # visible paren with slash inside visible main text
    paren = re.findall(r"\([^)]*?/[^)]*?\)", mt)
    # FAQ answers visible: each faq answer's first 8 words present in visible text
    faq_missing = []
    for f in p.get("faqs", []):
        a_words = norm_tokens(f.get("a", ""))[:8]
        if a_words and not all(w in vis for w in a_words):
            faq_missing.append(f.get("q", "")[:60])
    res[route] = {"visible_main_words": sum(vis.values()),
                  "doc_words_counts": p["counts"]["words"],
                  "doc_tokens_counted": sum(doc.values()),
                  "missing_tokens_visible_only": missing,
                  "missing_sample": list((doc - vis).elements())[:8],
                  "tables_rendered": tables, "tables_doc": p["counts"].get("tables", 0),
                  "main_hrefs": len(hrefs), "visible_paren": paren[:5],
                  "faq_answers_missing_visible": faq_missing}
    if missing: add("P1", "verbatim-visible", route, f"missing {missing}: {res[route]['missing_sample']}")
    if tables != p["counts"].get("tables", 0): add("P1", "tables", route, f"rendered {tables} vs doc {p['counts'].get('tables',0)}")
    if paren: add("P1", "visible-paren", route, str(paren[:3]))
    if faq_missing: add("P1", "faq-visible", route, str(faq_missing))
    if sum(vis.values()) < 100: add("P1", "fullness", route, f"visible main {sum(vis.values())} words")

# global links: all hrefs across out html
all_hrefs = {}
for f in OUT.rglob("*.html"):
    if f.name == "404.html": continue
    raw = f.read_text()
    for h in re.findall(r'href="([^"]+)"', raw):
        all_hrefs[h] = all_hrefs.get(h, 0) + 1
internal = {h: c for h, c in all_hrefs.items() if h.startswith("/midvale-water-damage")}
broken = {}
import urllib.request
for h in sorted(internal):
    if h.endswith(".css") or h.endswith(".js"): continue
    url = "http://127.0.0.1:8410" + h
    try:
        with urllib.request.urlopen(url, timeout=10) as r: code = r.status
    except urllib.error.HTTPError as e: code = e.code
    except Exception as e: code = f"ERR:{e}"
    if code != 200: broken[h] = code
# self-links: page linking to itself in body (main) — check per page
selflinks = {}
for p in pages:
    raw = route_file(p["route"]).read_text()
    mh, _ = visible_main(raw)
    hrefs = re.findall(r'href="([^"]+)"', mh)
    own = "/midvale-water-damage" + ("" if p["route"] == "/" else p["route"])
    own_slash = own + "/"
    hits = [h for h in hrefs if h.rstrip("/") == own.rstrip("/") or h == own_slash]
    if hits: selflinks[p["route"]] = hits
# orphans: routes in data not linked from anywhere? use body links set
body_targets = set()
for p in pages:
    raw = route_file(p["route"]).read_text()
    mh, _ = visible_main(raw)
    for h in re.findall(r'href="([^"]+)"', mh):
        body_targets.add(h.rstrip("/"))
orphans = []
for p in pages:
    t = "/midvale-water-damage" + ("" if p["route"] == "/" else p["route"])
    if t not in body_targets and p["route"] != "/":
        orphans.append(p["route"])
links = {"total_distinct_internal": len(internal), "total_href_instances": sum(internal.values()),
         "broken": broken, "self_links": selflinks, "orphans": orphans,
         "body_link_instances": sum(res[r]["main_hrefs"] for r in res)}
if broken: add("P1", "links-broken", "-", str(broken))
if selflinks: add("P1", "links-self", "-", str(selflinks))
if orphans: add("P2", "links-orphans", "-", str(orphans))
out = {"per_page": res, "links": links, "problems": problems,
       "visible_main_min": min(v["visible_main_words"] for v in res.values()),
       "missing_total_visible": sum(v["missing_tokens_visible_only"] for v in res.values()),
       "tables_total": sum(v["tables_rendered"] for v in res.values())}
(ROOT / "qa/reverify-visible.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1)[:6000])
