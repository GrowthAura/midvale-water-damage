#!/usr/bin/env python3
"""INDEPENDENT verification for the Midvale fill + 19px round (2026-11-13).
Written fresh for this task. TEST ONLY except: it starts a local server
(linkfix-serve.py) and writes qa/verify-fill-19px.json + qa/render-fill19px/*.png.
Does NOT modify site source, CSS, or lib/body-images.json.
Static gates read lib/pages-data.json, qa/link-inventory.json, out/**.
Render gates use Playwright Chromium with --disable-dev-shm-usage,
TMPDIR pointed at qa/tmpdir (VM /tmp tmpfs was reported full).
"""
import json, re, os, sys, hashlib, subprocess, time, socket
from collections import Counter
from bs4 import BeautifulSoup

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
PAGES = DATA["pages"]
INV = json.load(open(os.path.join(ROOT, "qa", "link-inventory.json")))
MANIFEST = json.load(open(os.path.join(ROOT, "lib", "body-images.json")))
TOKEN_RE = re.compile(r"[a-z0-9]+")
PAREN_RE = re.compile(r" \(/[^)]*\)")
PAREN_ANY_RE = re.compile(r"\(/[^)]+/\)")
BASE = "/midvale-water-damage"
EXPECTED_SHA = "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f"
NEW7 = ["emergency-water-extraction-1.webp", "emergency-water-extraction-3.webp",
        "crawl-space-water-damage-1.webp", "crawl-space-water-damage-2.webp",
        "water-heater-leak-cleanup-2.webp", "south-salt-lake-ut-3.webp",
        "commercial-water-damage-3.webp"]

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

def visible_text(elem):
    for bad in elem(["script", "style", "noscript"]):
        bad.decompose()
    return elem.get_text(" ")

def norm_href(href):
    if href == BASE or href == BASE + "/" or href.startswith(BASE + "#") or href.startswith(BASE + "?"):
        return "/", "internal"
    if href.startswith(BASE + "/"):
        t = href[len(BASE):].split("#")[0].split("?")[0] or "/"
        return t, "internal"
    if href.startswith("/"):
        return href.split("#")[0].split("?")[0] or "/", "UNPREFIXED"
    if href.startswith(("http", "tel:", "mailto:", "#")):
        return None, "external-or-anchor"
    return href, "other"

report = {"pages": {}, "site": {}, "problems": []}
def prob(sev, route, what, **kw):
    d = {"sev": sev, "route": route, "what": what}
    d.update(kw)
    report["problems"].append(d)

# ---------- SHA ----------
data_sha = hashlib.sha256(open(os.path.join(ROOT, "lib", "pages-data.json"), "rb").read()).hexdigest()
report["site"]["pages_data_sha256"] = data_sha
report["site"]["sha_match"] = (data_sha == EXPECTED_SHA)
if data_sha != EXPECTED_SHA:
    prob("P1", None, "pages-data.json sha256 CHANGED vs expected", sha=data_sha)
    print("SHA MISMATCH — STOP", flush=True)

# ---------- annotation path tokens ----------
path_tokens = {}
inv_records = {}
for rec in INV["records"]:
    if "SCHEMA-ONLY" in rec.get("unit", ""):
        continue
    r = rec["route"]
    path_tokens.setdefault(r, Counter()).update(toks(rec["target"]))
    inv_records.setdefault(r, []).append(rec)
inv_per_route = INV["per_route"]

# ---------- manifest / new-7 file checks ----------
from PIL import Image
report["site"]["manifest_routes"] = len(MANIFEST)
report["site"]["manifest_body_total"] = sum(len(v) for v in MANIFEST.values())
report["site"]["manifest_per_route_ok"] = all(len(v) == 3 for v in MANIFEST.values())
new7 = {}
for f in NEW7:
    p = os.path.join(ROOT, "public", "images", "body", f)
    try:
        im = Image.open(p)
        new7[f] = {"exists": True, "size": list(im.size), "format": im.format,
                   "exif_keys": sorted(im.info.keys()), "bytes": os.path.getsize(p),
                   "ai_in_filename": ("ai" in f.lower().split("-"))}
    except Exception as e:
        new7[f] = {"exists": False, "error": str(e)}
        prob("P1", None, "new image file missing/unreadable", file=f, error=str(e))
for f, d in new7.items():
    if d.get("size") != [1200, 675]:
        prob("P1", None, "new image not 1200x675", file=f, size=d.get("size"))
    if d.get("format") != "WEBP":
        prob("P1", None, "new image not WebP", file=f, format=d.get("format"))
    if d.get("exif_keys") not in ([], ["background", "loop"]):
        prob("P2", None, "new image carries unexpected metadata keys", file=f, keys=d.get("exif_keys"))
report["site"]["new7"] = new7
# alt text of the 7 (no "AI" word)
for route, items in MANIFEST.items():
    for it in items:
        fn = it["src"].split("/")[-1]
        if fn in NEW7 and re.search(r"\bai\b", it["alt"], re.I):
            prob("P2", route, '"AI" word in new-image alt', file=fn, alt=it["alt"])

# ---------- static per page ----------
link_graph = {}
total_body = total_card = 0
for p in PAGES:
    route = p["route"]
    fpath = route_to_file(route)
    pr = {"route": route}
    if not os.path.exists(fpath):
        pr["missing_file"] = True
        report["pages"][route] = pr
        prob("P1", route, "built HTML file missing")
        continue
    html = open(fpath, encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    main_text_raw = main.get_text(" ") if main else ""
    # paren-path visible text (main + whole file)
    pr["paren_in_main"] = len(PAREN_ANY_RE.findall(main_text_raw))
    pr["paren_in_html_file"] = len(PAREN_ANY_RE.findall(html))
    if pr["paren_in_main"]:
        prob("P1", route, "visible (/.../) path text in MAIN", count=pr["paren_in_main"],
             samples=PAREN_ANY_RE.findall(main_text_raw)[:3])
    if pr["paren_in_html_file"]:
        prob("P1", route, "visible (/.../) path text in out/ HTML", count=pr["paren_in_html_file"],
             samples=PAREN_ANY_RE.findall(html)[:3])
    # title / meta / h1
    title = soup.title.get_text(strip=True) if soup.title else None
    md = soup.find("meta", attrs={"name": "description"})
    md_val = md["content"] if md and md.has_attr("content") else None
    pr["title_ok"] = (title == p["metaTitle"])
    pr["meta_ok"] = (md_val == p["metaDescription"])
    if not pr["title_ok"]:
        prob("P2", route, "title mismatch", expected=p["metaTitle"], actual=title)
    if not pr["meta_ok"]:
        prob("P2", route, "meta description mismatch", expected=p["metaDescription"], actual=md_val)
    h1s = main.find_all("h1") if main else []
    pr["h1_count"] = len(h1s)
    pr["h1_ok"] = (len(h1s) == 1 and h1s[0].get_text(" ", strip=True) == p["h1"])
    if not pr["h1_ok"]:
        prob("P1", route, "H1 count/text wrong", count=len(h1s), expected=p["h1"],
             actual=h1s[0].get_text(" ", strip=True) if h1s else None)
    # tables
    data_tables = [b for b in p["blocks"] if b["type"] == "table"]
    rendered_tables = main.find_all("table") if main else []
    pr["tables_data"] = len(data_tables)
    pr["tables_rendered"] = len(rendered_tables)
    tc_mismatch = []
    for i, tb in enumerate(data_tables):
        if i >= len(rendered_tables):
            tc_mismatch.append(f"table {i} not rendered")
            continue
        cells = [c.get_text(" ", strip=True) for c in rendered_tables[i].find_all(["th", "td"])]
        exp_cells = [strip_parens(c) for c in list(tb["headers"]) + [c for r in tb["rows"] for c in r]]
        if cells != exp_cells:
            tc_mismatch.append({"table": i, "expected": exp_cells, "actual": cells})
    pr["table_cell_mismatch"] = tc_mismatch
    if tc_mismatch:
        prob("P1", route, "table content mismatch", detail=tc_mismatch)
    # FAQ visible + LD
    faq_visible = {}
    faq_sec = soup.find("section", id="faq")
    if faq_sec:
        for h in faq_sec.find_all("h3"):
            q = h.get_text(" ", strip=True)
            ans_parts = []
            for sib in h.next_siblings:
                if getattr(sib, "name", None) == "h3":
                    break
                if hasattr(sib, "get_text"):
                    ans_parts.append(sib.get_text(" ", strip=True))
            faq_visible[q] = " ".join(ans_parts).strip()
    ld_faq = []
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(sc.string)
        except Exception:
            continue
        graphs = j if isinstance(j, list) else [j]
        for g in graphs:
            if isinstance(g, dict) and g.get("@type") == "FAQPage":
                for e in g.get("mainEntity", []):
                    a = e.get("acceptedAnswer", {})
                    ld_faq.append((e.get("name", ""), a.get("text", "") if isinstance(a, dict) else ""))
            if isinstance(g, dict) and "@graph" in g:
                for n in g["@graph"]:
                    if isinstance(n, dict) and n.get("@type") == "FAQPage":
                        for e in n.get("mainEntity", []):
                            a = e.get("acceptedAnswer", {})
                            ld_faq.append((e.get("name", ""), a.get("text", "") if isinstance(a, dict) else ""))
    pr["faq_data_count"] = len(p["faqs"])
    pr["faq_ld_count"] = len(ld_faq)
    pr["faq_visible_count"] = len(faq_visible)
    faq_mismatch = []
    for f in p["faqs"]:
        q, a = f["q"], f["a"]
        exp_a = toks(strip_parens(a))
        hit = [x for x in ld_faq if x[0] == q]
        if not hit:
            faq_mismatch.append({"q": q, "issue": "not in FAQPage schema"})
        elif toks(hit[0][1]) != exp_a:
            faq_mismatch.append({"q": q, "issue": "schema answer != stripped data answer"})
        vis = faq_visible.get(q)
        if vis is None:
            faq_mismatch.append({"q": q, "issue": "question not visible in #faq section"})
        elif toks(vis) != exp_a:
            faq_mismatch.append({"q": q, "issue": "visible answer != stripped data answer"})
    pr["faq_mismatch"] = faq_mismatch
    if faq_mismatch:
        prob("P1", route, "FAQ schema/visible mismatch", detail=faq_mismatch[:5])
    # verbatim annotation-adjusted
    main_tokens = counter_of([visible_text(main)]) if main else Counter()
    expected = expected_tokens(p)
    expected_visible = expected - path_tokens.get(route, Counter())
    missing = expected_visible - main_tokens
    extra = main_tokens - expected_visible
    pr["main_words"] = sum(main_tokens.values())
    pr["expected_words_visible"] = sum(expected_visible.values())
    pr["missing_words"] = sum(missing.values())
    pr["extra_words"] = sum(extra.values())
    pr["missing_detail"] = dict(missing.most_common(40))
    pr["extra_detail"] = dict(extra.most_common(40))
    pr["fullness"] = "FULL" if pr["main_words"] >= 300 else ("THIN" if pr["main_words"] >= 100 else "EMPTY")
    if pr["fullness"] != "FULL":
        prob("P1", route, f"fullness gate {pr['fullness']}", main_words=pr["main_words"])
    if missing:
        prob("P1", route, "content words missing (annotation-adjusted)", count=sum(missing.values()),
             sample=dict(missing.most_common(20)))
    # links
    body_links = soup.find_all("a", class_="body-link")
    card_links = soup.find_all("a", class_="card-wrap-link")
    pr["body_link_count"] = len(body_links)
    pr["card_link_count"] = len(card_links)
    total_body += len(body_links)
    total_card += len(card_links)
    page_targets = set()
    broken, self_links_body, unprefixed = [], [], []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        tgt, kind = norm_href(href)
        if kind == "UNPREFIXED":
            unprefixed.append(href)
        if tgt is None:
            continue
        page_targets.add(tgt)
        inside_main = main and a in main.find_all("a")
        inside_nav = a.find_parent("nav") is not None
        if inside_main and not inside_nav and tgt == route:
            self_links_body.append({"href": href, "text": a.get_text(" ", strip=True)[:80]})
        if kind == "internal":
            fp = os.path.join(OUT, "index.html") if tgt == "/" else os.path.join(OUT, tgt.strip("/") + ".html")
            if not os.path.exists(fp):
                broken.append(tgt)
    pr["self_links_body"] = self_links_body
    pr["broken_internal_links"] = sorted(set(broken))
    pr["unprefixed_hrefs"] = sorted(set(unprefixed))
    if self_links_body:
        prob("P2", route, "body self-link(s)", detail=self_links_body)
    if broken:
        prob("P1", route, "broken internal link(s)", detail=sorted(set(broken)))
    if unprefixed:
        prob("P1", route, "unprefixed root-relative href(s)", detail=sorted(set(unprefixed)))
    link_graph[route] = page_targets
    exp_kept = inv_per_route.get(route, {}).get("kept", 0)
    exp_card = 19 if route == "/" else 0
    exp_body = exp_kept - exp_card
    pr["expected_body_links"] = exp_body
    pr["expected_card_links"] = exp_card
    if len(body_links) != exp_body:
        prob("P1", route, "body-link count != inventory kept-minus-cards", expected=exp_body, actual=len(body_links))
    if len(card_links) != exp_card:
        prob("P1", route, "card-wrap-link count != expected", expected=exp_card, actual=len(card_links))
    # inventory record check
    rec_problems = []
    for rec in inv_records.get(route, []):
        anchor, target, status = rec["anchor"], rec["target"], rec["status"]
        linked = [a for a in soup.find_all("a", href=True)
                  if a.get("class") and ("body-link" in a.get("class") or "card-wrap-link" in a.get("class"))
                  and norm_href(a["href"])[0] == target]
        anchor_in_linked = [a for a in linked if anchor in re.sub(r"\s+", " ", a.get_text(" ", strip=True))]
        if status == "kept":
            if not anchor_in_linked:
                rec_problems.append({"record": rec["unit"], "target": target, "anchor": anchor,
                                     "issue": "kept link missing", "links_with_href": len(linked)})
        else:
            if anchor not in re.sub(r"\s+", " ", main_text_raw):
                rec_problems.append({"record": rec["unit"], "target": target, "anchor": anchor,
                                     "issue": "dup-dropped anchor text MISSING from visible text"})
    pr["record_problems"] = rec_problems
    if rec_problems:
        prob("P1", route, "inventory record mismatch", detail=rec_problems[:5])
    # hero buttons
    hero = main.find("section", class_="hero") if main else None
    if hero:
        btns = [a.get_text(" ", strip=True) for a in hero.find_all("a") if a.find_parent("nav") is None]
        pr["hero_buttons"] = btns
        if "(385) 337-3560" not in btns or "Request Emergency Help" not in btns:
            prob("P2", route, "hero buttons missing/wrong", buttons=btns)
    else:
        prob("P1", route, "no hero section in main")
    # ---- images (static, out/ HTML) ----
    imgs = soup.find_all("img")
    pr["img_total_static"] = len(imgs)
    pr["img_srcs"] = [i.get("src") for i in imgs]
    pr["img_missing_alt"] = [i.get("src") for i in imgs if not i.get("alt")]
    pr["img_file_missing"] = []
    for src in pr["img_srcs"]:
        if not src:
            pr["img_file_missing"].append("(empty src)")
            continue
        rel = src[len(BASE):] if src.startswith(BASE) else src
        cand = os.path.join(OUT, rel.lstrip("/"))
        if not os.path.isfile(cand):
            pr["img_file_missing"].append(src)
    if pr["img_file_missing"]:
        prob("P1", route, "img src file missing from out/", detail=pr["img_file_missing"])
    if pr["img_missing_alt"]:
        prob("P3", route, "img missing alt", detail=pr["img_missing_alt"])
    # body images vs manifest (19 service+location pages)
    if route in MANIFEST:
        exp_body_srcs = [it["src"] for it in MANIFEST[route]]
        got_body = [s for s in pr["img_srcs"] if s and "/images/body/" in s]
        pr["body_imgs_static"] = got_body
        pr["body_imgs_expected"] = [BASE + s for s in exp_body_srcs]
        if sorted(got_body) != sorted(pr["body_imgs_expected"]):
            prob("P1", route, "body images != manifest", expected=pr["body_imgs_expected"], actual=got_body)
        heroes = [s for s in pr["img_srcs"] if s and "/images/heroes/" in s]
        pr["hero_imgs_static"] = heroes
        if len(pr["img_srcs"]) != 4:
            prob("P1", route, "total images != 4 on service/location page", total=len(pr["img_srcs"]),
                 srcs=pr["img_srcs"])
    report["pages"][route] = pr

report["site"]["total_body_links"] = total_body
report["site"]["total_card_links"] = total_card
report["site"]["total_links"] = total_body + total_card
if total_body != 143:
    prob("P1", None, "total body links != 143", actual=total_body)
if total_card != 19:
    prob("P1", None, "total card links != 19", actual=total_card)
# orphans: inbound count per route
inbound = Counter()
for src, tgts in link_graph.items():
    for t in tgts:
        inbound[t] += 1
all_routes = set(p["route"] for p in PAGES)
orphans = [r for r in all_routes if r != "/" and inbound.get(r, 0) == 0]
report["site"]["orphans"] = orphans
report["site"]["inbound_min"] = min(inbound.get(r, 0) for r in all_routes)
if orphans:
    prob("P2", None, "orphan route(s) with zero inbound links", detail=orphans)
report["site"]["faq_total_data"] = sum(p["faq_data_count"] for p in report["pages"].values() if "faq_data_count" in p)
report["site"]["faq_total_visible"] = sum(p["faq_visible_count"] for p in report["pages"].values() if "faq_visible_count" in p)
report["site"]["faq_total_ld"] = sum(p["faq_ld_count"] for p in report["pages"].values() if "faq_ld_count" in p)
report["site"]["tables_total_data"] = sum(p["tables_data"] for p in report["pages"].values() if "tables_data" in p)
report["site"]["tables_total_rendered"] = sum(p["tables_rendered"] for p in report["pages"].values() if "tables_rendered" in p)

json.dump(report, open(os.path.join(ROOT, "qa", "verify-fill-19px-static.json"), "w"), indent=1)
print("STATIC done. problems so far:", len(report["problems"]), flush=True)
for pb in report["problems"]:
    print(" ", pb["sev"], pb["route"], pb["what"], str(pb)[:220], flush=True)
print(f"links body={total_body} card={total_card} faq data={report['site']['faq_total_data']} "
      f"visible={report['site']['faq_total_visible']} ld={report['site']['faq_total_ld']} "
      f"tables {report['site']['tables_total_data']}/{report['site']['tables_total_rendered']}", flush=True)
print(f"fullness: {sum(1 for p in report['pages'].values() if p.get('fullness')=='FULL')}/31 FULL; "
      f"missing words total={sum(p.get('missing_words',0) for p in report['pages'].values())}; "
      f"extra words total={sum(p.get('extra_words',0) for p in report['pages'].values())}", flush=True)
print(f"img totals static: " + ", ".join(f"{r}:{report['pages'][r].get('img_total_static')}" for r in report["pages"]), flush=True)
