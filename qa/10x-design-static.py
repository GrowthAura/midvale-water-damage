#!/usr/bin/env python3
"""FRESH independent static verification for Midvale 10x design round (2026-11-13).
TEST ONLY — reads lib/pages-data.json, qa/link-inventory.json, out/**.
Writes qa/10x-design/10x-design-static.json.
Verbatim method (own implementation): rendered <main> token multiset vs
data content tokens (eyebrow+h1+intro+trustChips+blocks) MINUS link-annotation
path tokens (visible inventory records only). FAQ text is NOT in expected
blocks (faqs array checked separately) so FAQ words show as EXTRA — expected.
Does NOT modify any site source file.
"""
import json, re, os
from urllib.parse import unquote
from collections import Counter
from bs4 import BeautifulSoup

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
OUTDIR = os.path.join(ROOT, "qa", "10x-design")
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
PAGES = DATA["pages"]
INV = json.load(open(os.path.join(ROOT, "qa", "link-inventory.json")))
BASE = "/midvale-water-damage"
TOKEN_RE = re.compile(r"[a-z0-9]+")
PAREN_RE = re.compile(r" \(/[^)]*\)")
PAREN_ANY_RE = re.compile(r"\(/[^)]+/\)")

def toks(text):
    return TOKEN_RE.findall((text or "").lower())

def counter_of(texts):
    c = Counter()
    for t in texts:
        c.update(toks(t))
    return c

def strip_parens(text):
    return PAREN_RE.sub("", text or "")

def expected_tokens(p):
    parts = []
    if p.get("eyebrow"):
        parts.append(p["eyebrow"])
    parts.append(p["h1"])
    parts.append(p["intro"])
    for ch in (p.get("trustChips") or []):
        parts.append(ch)
    for b in p["blocks"]:
        t = b["type"]
        if t in ("h2", "h3"):
            parts.append(b["text"])
        elif t == "p":
            parts.append("".join(s["t"] for s in b["segments"]))
        elif t in ("ul", "ol"):
            for it in b["items"]:
                parts.append("".join(s["t"] for s in it["segments"]))
        elif t == "table":
            parts.extend(b["headers"])
            for r in b["rows"]:
                parts.extend(r)
    return counter_of(parts)

def route_to_file(route):
    return os.path.join(OUT, "index.html") if route == "/" else os.path.join(OUT, route.strip("/") + ".html")

path_tokens = {}
for rec in INV["records"]:
    if "SCHEMA-ONLY" in rec.get("unit", ""):
        continue
    r = rec["route"]
    path_tokens.setdefault(r, Counter()).update(toks(rec["target"]))

report = {"pages": {}, "site": {}, "problems": []}
all_routes = set(p["route"] for p in PAGES)

# ---- sitemap ----
smap = open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", smap)
report["site"]["sitemap_locs"] = len(locs)
report["site"]["sitemap_routes"] = sorted(set(re.sub(r"^https?://[^/]+", "", l).replace(BASE, "") or "/" for l in locs))
smap_routes = set(report["site"]["sitemap_routes"])
if smap_routes != all_routes:
    report["problems"].append({"sev": "P1", "what": "sitemap routes != 31 data routes",
                               "missing": sorted(all_routes - smap_routes), "extra": sorted(smap_routes - all_routes)})

# ---- per-page static ----
link_graph = {}   # route -> set of internal target routes linked from anywhere on page
body_links = {}   # route -> [(href,target)] links inside <main>
all_internal_hrefs = Counter()
for p in PAGES:
    route = p["route"]
    fpath = route_to_file(route)
    pr = {"route": route}
    html = open(fpath, encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    main_text = main.get_text(" ") if main else ""
    # title/meta/h1
    title = soup.title.get_text(strip=True) if soup.title else None
    md = soup.find("meta", attrs={"name": "description"})
    pr["title_ok"] = title == p["metaTitle"]
    pr["meta_ok"] = (md["content"] if md and md.has_attr("content") else None) == p["metaDescription"]
    h1s = main.find_all("h1") if main else []
    pr["h1_count"] = len(h1s)
    pr["h1_ok"] = len(h1s) == 1 and h1s[0].get_text(" ", strip=True) == p["h1"]
    if not pr["title_ok"]:
        report["problems"].append({"sev": "P2", "route": route, "what": "title mismatch", "expected": p["metaTitle"], "actual": title})
    if not pr["meta_ok"]:
        report["problems"].append({"sev": "P2", "route": route, "what": "meta description mismatch"})
    if not pr["h1_ok"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "H1 count/text wrong",
                                   "count": len(h1s), "expected": p["h1"],
                                   "actual": h1s[0].get_text(" ", strip=True) if h1s else None})
    # paren-path leakage in visible main text
    pr["paren_in_main"] = len(PAREN_ANY_RE.findall(main_text))
    if pr["paren_in_main"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "paren-path visible in main text",
                                   "count": pr["paren_in_main"], "samples": PAREN_ANY_RE.findall(main_text)[:3]})
    # verbatim multiset
    main_tokens = counter_of([main_text])
    expected = expected_tokens(p)
    expected_visible = expected - path_tokens.get(route, Counter())
    missing = expected_visible - main_tokens
    extra = main_tokens - expected_visible
    pr["main_words"] = sum(main_tokens.values())
    pr["expected_words_visible"] = sum(expected_visible.values())
    pr["missing_words"] = sum(missing.values())
    pr["extra_words"] = sum(extra.values())
    pr["missing_detail"] = dict(missing.most_common(30))
    pr["extra_detail"] = dict(extra.most_common(30))
    pr["fullness"] = "FULL" if pr["main_words"] >= 300 else ("THIN" if pr["main_words"] >= 100 else "EMPTY")
    if missing:
        report["problems"].append({"sev": "P1", "route": route, "what": "content words missing from render",
                                   "count": sum(missing.values()), "sample": dict(missing.most_common(20))})
    if pr["fullness"] != "FULL":
        report["problems"].append({"sev": "P1", "route": route, "what": f"fullness {pr['fullness']}", "main_words": pr["main_words"]})
    # FAQ visible count
    faq_sec = soup.find("section", id="faq")
    pr["faq_visible"] = len(faq_sec.find_all("h3")) if faq_sec else 0
    pr["faq_data"] = len(p["faqs"])
    if pr["faq_visible"] != pr["faq_data"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "FAQ visible count != data",
                                   "visible": pr["faq_visible"], "data": pr["faq_data"]})
    # tables
    pr["tables_data"] = len([b for b in p["blocks"] if b["type"] == "table"])
    pr["tables_rendered"] = len(main.find_all("table")) if main else 0
    if pr["tables_data"] != pr["tables_rendered"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "table count mismatch",
                                   "data": pr["tables_data"], "rendered": pr["tables_rendered"]})
    # links: whole page + body
    targets = set()
    blist = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        all_internal_hrefs[href] += 1
        t = None
        if href == BASE or href == BASE + "/" or href.startswith(BASE + "#"):
            t = "/"
        elif href.startswith(BASE + "/"):
            t = href[len(BASE):].split("#")[0].split("?")[0] or "/"
        elif href.startswith("/") and not href.startswith("//"):
            report["problems"].append({"sev": "P1", "route": route, "what": "UNPREFIXED root-relative href", "href": href})
            t = href.split("#")[0].split("?")[0] or "/"
        if t is not None:
            targets.add(t)
            if main and a in main.find_all("a", href=True):
                blist.append((href, t))
    link_graph[route] = targets
    body_links[route] = blist
    # body self-links
    selfs = [h for h, t in blist if t == route]
    pr["body_self_links"] = len(selfs)
    if selfs:
        report["problems"].append({"sev": "P1", "route": route, "what": "body self-link(s)", "hrefs": selfs[:5]})
    # images in html
    pr["img_tags"] = len(soup.find_all("img"))
    pr["img_missing_alt"] = [im.get("src") for im in soup.find_all("img") if not (im.get("alt") or "").strip()]
    if pr["img_missing_alt"]:
        report["problems"].append({"sev": "P2", "route": route, "what": "img without alt", "srcs": pr["img_missing_alt"]})
    report["pages"][route] = pr

# ---- broken internal links (file existence) ----
broken = []
for href, n in all_internal_hrefs.items():
    if href.startswith("http") or href.startswith("tel:") or href.startswith("mailto:") or href.startswith("#"):
        continue
    if href == BASE or href == BASE + "/" or href.startswith(BASE + "#"):
        continue
    if href.startswith(BASE + "/"):
        rel = href[len(BASE) + 1:].split("#")[0].split("?")[0]
    elif href.startswith("/"):
        rel = href[1:].split("#")[0].split("?")[0]
    else:
        continue
    if not rel:
        continue
    cand = os.path.join(OUT, rel)
    ok = os.path.isfile(cand) or os.path.isfile(cand + ".html") or os.path.isfile(os.path.join(cand, "index.html"))
    if not ok:
        broken.append({"href": href, "count": n})
report["site"]["broken_internal_links"] = broken
if broken:
    report["problems"].append({"sev": "P1", "what": "broken internal links", "detail": broken})
# ---- orphans ----
reachable = set(["/"])
for targets in link_graph.values():
    reachable |= targets
orphans = sorted(all_routes - reachable)
report["site"]["orphans"] = orphans
if orphans:
    report["problems"].append({"sev": "P1", "what": "orphan routes (unreachable from any link)", "routes": orphans})
# ---- asset existence for every img src / css / js in out html ----
missing_assets = set()
for p in PAGES:
    soup = BeautifulSoup(open(route_to_file(p["route"]), encoding="utf-8"), "html.parser")
    for tag, attr in (("img", "src"), ("link", "href"), ("script", "src")):
        for el in soup.find_all(tag):
            v = el.get(attr)
            if not v or v.startswith(("http", "data:", "tel:", "mailto:", "#")):
                continue
            rel = v[len(BASE) + 1:] if v.startswith(BASE + "/") else (v[1:] if v.startswith("/") else v.split("#")[0])
            rel = unquote(rel.split("#")[0].split("?")[0])
            if rel and not os.path.isfile(os.path.join(OUT, rel)):
                missing_assets.add(v)
report["site"]["missing_assets"] = sorted(missing_assets)
if missing_assets:
    report["problems"].append({"sev": "P1", "what": "missing referenced assets", "assets": sorted(missing_assets)})

json.dump(report, open(os.path.join(OUTDIR, "10x-design-static.json"), "w"), indent=1)
print("PROBLEMS:", len(report["problems"]))
for pb in report["problems"]:
    print(" ", pb.get("sev"), pb.get("route", ""), pb.get("what"), str(pb)[:200])
print("orphans:", orphans)
print("broken links:", broken)
print("missing assets:", sorted(missing_assets))
print("sitemap locs:", report["site"]["sitemap_locs"])
tot_missing = sum(v["missing_words"] for v in report["pages"].values())
tot_extra = sum(v["extra_words"] for v in report["pages"].values())
print(f"total missing words: {tot_missing}, total extra words: {tot_extra}")
for r, v in report["pages"].items():
    if v["missing_words"] or v["extra_words"] > 400:
        print(f"  {r}: missing={v['missing_words']} extra={v['extra_words']} extra_sample={list(v['extra_detail'].items())[:12]}")
