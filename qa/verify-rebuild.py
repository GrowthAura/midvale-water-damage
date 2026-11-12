#!/usr/bin/env python3
"""Independent static verification for the Midvale rebuild.
Reads ONLY: lib/pages-data.json, out/** (built export), public/images.
Writes: qa/verify-rebuild-static.json (this script's report).
Does NOT modify any site source file.
"""
import json, re, os, hashlib, sys
from collections import Counter
from bs4 import BeautifulSoup

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
DATA = json.load(open(os.path.join(ROOT, "lib/pages-data.json")))
PAGES = DATA["pages"]

TOKEN_RE = re.compile(r"[a-z0-9]+")

def toks(text):
    if not text:
        return []
    return TOKEN_RE.findall(text.lower())

def counter_of(texts):
    c = Counter()
    for t in texts:
        c.update(toks(t))
    return c

def expected_tokens(p):
    """All content tokens from the data record (eyebrow, h1, intro, chips, blocks, faqs)."""
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
    # NOTE: faqs are NOT appended: every FAQ q/a is already a block (h3 + following p).
    # The faqs array is a parallel copy for the JSON-LD schema. Appending it would double-count.
    return counter_of(parts)

def route_to_file(route):
    if route == "/":
        return os.path.join(OUT, "index.html")
    return os.path.join(OUT, route.strip("/") + ".html")

def visible_text(soup_elem):
    for bad in soup_elem(["script", "style", "noscript"]):
        bad.decompose()
    return soup_elem.get_text(" ")

report = {"pages": {}, "site": {}, "problems": []}
link_graph = {}   # route -> set of target routes linked from that page
all_hrefs = Counter()

for p in PAGES:
    route = p["route"]
    fpath = route_to_file(route)
    pr = {"route": route, "file": os.path.relpath(fpath, ROOT)}
    if not os.path.exists(fpath):
        pr["missing_file"] = True
        report["pages"][route] = pr
        report["problems"].append({"sev": "P1", "route": route, "what": "built HTML file missing", "file": fpath})
        continue
    html = open(fpath, encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")

    # ---- title / meta / canonical / og ----
    title = soup.title.get_text(strip=True) if soup.title else None
    pr["title_ok"] = (title == p["metaTitle"])
    if not pr["title_ok"]:
        report["problems"].append({"sev": "P2", "route": route, "what": "title mismatch", "expected": p["metaTitle"], "actual": title})
    md = soup.find("meta", attrs={"name": "description"})
    md_val = md["content"] if md and md.has_attr("content") else None
    pr["meta_ok"] = (md_val == p["metaDescription"])
    if not pr["meta_ok"]:
        report["problems"].append({"sev": "P2", "route": route, "what": "meta description mismatch", "expected": p["metaDescription"], "actual": md_val})
    can = soup.find("link", rel="canonical")
    can_href = can["href"] if can and can.has_attr("href") else None
    exp_can = "http://localhost:3000/" if route == "/" else "http://localhost:3000" + route
    pr["canonical"] = can_href
    pr["canonical_ok"] = (can_href == exp_can)
    if not pr["canonical_ok"]:
        report["problems"].append({"sev": "P2", "route": route, "what": "canonical mismatch", "expected": exp_can, "actual": can_href})
    og = soup.find("meta", attrs={"property": "og:url"})
    pr["og_url"] = og["content"] if og and og.has_attr("content") else None

    # ---- h1 ----
    h1s = main.find_all("h1") if main else []
    pr["h1_count"] = len(h1s)
    pr["h1_text"] = h1s[0].get_text(" ", strip=True) if h1s else None
    pr["h1_ok"] = (len(h1s) == 1 and pr["h1_text"] == p["h1"])
    if not pr["h1_ok"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "H1 count/text wrong", "count": len(h1s), "expected": p["h1"], "actual": pr["h1_text"]})

    # ---- h2 / h3 sequences (data blocks only; FAQ heading + FAQ qs handled separately) ----
    data_h2 = [b["text"] for b in p["blocks"] if b["type"] == "h2"]
    data_h3 = [b["text"] for b in p["blocks"] if b["type"] == "h3"]
    rendered_h2 = [h.get_text(" ", strip=True) for h in main.find_all("h2")] if main else []
    rendered_h3 = [h.get_text(" ", strip=True) for h in main.find_all("h3")] if main else []
    # FAQ section heading is chrome (e.g. "Emergency Water Extraction FAQ"); closing CTA h2 IS in data.
    pr["h2_rendered"] = rendered_h2
    pr["h2_data"] = data_h2
    pr["h2_missing"] = [t for t in data_h2 if t not in rendered_h2]
    pr["h2_extra"] = [t for t in rendered_h2 if t not in data_h2]
    if pr["h2_missing"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "H2 missing from render", "missing": pr["h2_missing"]})
    pr["h3_data_count"] = len(data_h3)
    faq_qs = [f["q"] for f in p["faqs"]]
    pr["h3_rendered_count"] = len(rendered_h3)
    pr["h3_expected_total"] = len(data_h3) + len(faq_qs)
    pr["h3_missing_data"] = [t for t in data_h3 if t not in rendered_h3]
    pr["h3_missing_faq"] = [t for t in faq_qs if t not in rendered_h3]
    pr["h3_extra"] = [t for t in rendered_h3 if t not in data_h3 and t not in faq_qs]
    if pr["h3_missing_data"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "H3 (content) missing from render", "missing": pr["h3_missing_data"]})
    if pr["h3_missing_faq"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "FAQ question missing as H3", "missing": pr["h3_missing_faq"]})
    if pr["h3_extra"]:
        report["problems"].append({"sev": "P3", "route": route, "what": "extra H3 in render (chrome or invented)", "extra": pr["h3_extra"]})

    # ---- tables ----
    data_tables = [b for b in p["blocks"] if b["type"] == "table"]
    rendered_tables = main.find_all("table") if main else []
    pr["tables_data"] = len(data_tables)
    pr["tables_rendered"] = len(rendered_tables)
    table_cell_mismatch = []
    for i, tb in enumerate(data_tables):
        if i >= len(rendered_tables):
            table_cell_mismatch.append(f"table {i} not rendered")
            continue
        cells = [c.get_text(" ", strip=True) for c in rendered_tables[i].find_all(["th", "td"])]
        exp_cells = list(tb["headers"]) + [c for r in tb["rows"] for c in r]
        if cells != exp_cells:
            table_cell_mismatch.append({"table": i, "expected": exp_cells, "actual": cells})
    pr["table_cell_mismatch"] = table_cell_mismatch
    if table_cell_mismatch:
        report["problems"].append({"sev": "P1", "route": route, "what": "table content mismatch", "detail": table_cell_mismatch})

    # ---- FAQ JSON-LD vs visible ----
    faq_visible = {}
    faq_sec = soup.find("section", id="faq") or (main.find("section", id="faq") if main else None)
    if faq_sec:
        for h in faq_sec.find_all("h3"):
            q = h.get_text(" ", strip=True)
            # answer = following sibling text until next h3
            ans_parts = []
            for sib in h.next_siblings:
                if getattr(sib, "name", None) == "h3":
                    break
                if hasattr(sib, "get_text"):
                    ans_parts.append(sib.get_text(" ", strip=True))
            faq_visible[q] = " ".join(ans_parts).strip()
    pr["faq_visible_count"] = len(faq_visible)
    pr["faq_data_count"] = len(p["faqs"])
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
    pr["faq_ld_count"] = len(ld_faq)
    ld_mismatch = []
    for _f in p["faqs"]:
        q, a = _f["q"], _f["a"]
        hit = [x for x in ld_faq if x[0] == q]
        if not hit:
            ld_mismatch.append({"q": q, "issue": "not in FAQPage schema"})
        elif toks(hit[0][1]) != toks(a):
            ld_mismatch.append({"q": q, "issue": "schema answer text differs from visible/data answer"})
        vis = faq_visible.get(q)
        if vis is None:
            ld_mismatch.append({"q": q, "issue": "question not visible in #faq section"})
        elif toks(vis) != toks(a):
            ld_mismatch.append({"q": q, "issue": "visible answer text differs from data answer"})
    pr["faq_ld_mismatch"] = ld_mismatch
    if ld_mismatch:
        report["problems"].append({"sev": "P1", "route": route, "what": "FAQ schema/visible mismatch", "detail": ld_mismatch})

    # ---- schema types present ----
    types = set()
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(sc.string)
        except Exception:
            continue
        def walk(o):
            if isinstance(o, dict):
                if "@type" in o:
                    types.add(o["@type"])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(j)
    pr["schema_types"] = sorted(types)


    # ---- main visible text vs expected content (multiset) ----
    main_text = visible_text(main) if main else ""
    actual = counter_of([main_text])
    expected = expected_tokens(p)
    missing = expected - actual
    extra = actual - expected
    pr["main_words"] = sum(actual.values())
    pr["expected_words"] = sum(expected.values())
    pr["missing_words"] = sum(missing.values())
    pr["extra_words"] = sum(extra.values())
    pr["missing_detail"] = dict(missing.most_common(40))
    pr["extra_detail"] = dict(extra.most_common(40))
    # fullness gate on MAIN-BODY words: main visible words (incl. chrome) vs expected content words
    pr["fullness"] = "FULL" if pr["main_words"] >= 300 else ("THIN" if pr["main_words"] >= 100 else "EMPTY")
    if pr["fullness"] != "FULL":
        report["problems"].append({"sev": "P1", "route": route, "what": f"fullness gate {pr['fullness']}", "main_words": pr["main_words"]})
    if missing:
        report["problems"].append({"sev": "P1", "route": route, "what": "content words missing from render", "count": sum(missing.values()), "sample": dict(missing.most_common(20))})

    # ---- links ----
    page_targets = set()
    self_links_body = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        all_hrefs[href] += 1
        if href == "/midvale-water-damage" or href.startswith("/midvale-water-damage/") or href.startswith("/midvale-water-damage#"):
            tgt = href[len("/midvale-water-damage"):] or "/"
            tgt = tgt.split("#")[0].split("?")[0] or "/"
            page_targets.add(tgt)
            # body self-link: inside <main> but outside nav (breadcrumb)
            inside_main = main and a in main.find_all("a")
            inside_nav = a.find_parent("nav") is not None
            if inside_main and not inside_nav and tgt == route:
                self_links_body.append({"href": href, "text": a.get_text(" ", strip=True)[:80]})
        elif href.startswith("/") and not href.startswith("//"):
            report["problems"].append({"sev": "P1", "route": route, "what": "unprefixed root-relative href", "href": href})
    link_graph[route] = page_targets
    pr["self_links_body"] = self_links_body
    if self_links_body:
        report["problems"].append({"sev": "P2", "route": route, "what": "body self-link(s)", "detail": self_links_body})
    # link existence
    broken = []
    for tgt in page_targets:
        if tgt == "/":
            fp = os.path.join(OUT, "index.html")
        else:
            fp = os.path.join(OUT, tgt.strip("/") + ".html")
        if not os.path.exists(fp):
            broken.append(tgt)
    pr["broken_internal_links"] = broken
    if broken:
        report["problems"].append({"sev": "P1", "route": route, "what": "broken internal link(s)", "detail": broken})

    # ---- images ----
    imgs = soup.find_all("img")
    pr["img_count"] = len(imgs)
    img_issues = []
    for im in imgs:
        src = im.get("src", "")
        alt = im.get("alt", "")
        if not src.startswith("/midvale-water-damage/"):
            img_issues.append({"src": src, "issue": "unprefixed img src"})
        else:
            rel = src[len("/midvale-water-damage/"):]
            if not os.path.exists(os.path.join(OUT, rel)):
                img_issues.append({"src": src, "issue": "img file missing from out/"})
        if not alt:
            img_issues.append({"src": src, "issue": "img missing alt"})
        if re.search(r"\bAI\b", alt):
            img_issues.append({"src": src, "issue": "alt contains standalone AI word"})
    pr["img_issues"] = img_issues
    if img_issues:
        report["problems"].append({"sev": "P2", "route": route, "what": "image issue(s)", "detail": img_issues})

    # ---- hero buttons ----
    hero = main.find("section", class_="hero") if main else None
    if hero:
        btns = [a for a in hero.find_all("a") if a.find_parent("nav") is None]
        btn_texts = [b.get_text(" ", strip=True) for b in btns]
        pr["hero_buttons"] = btn_texts
        pr["hero_btn1_ok"] = any(t == "(385) 337-3560" for t in btn_texts)
        pr["hero_btn2_ok"] = any(t == "Request Emergency Help" for t in btn_texts)
        if not (pr["hero_btn1_ok"] and pr["hero_btn2_ok"]):
            report["problems"].append({"sev": "P2", "route": route, "what": "hero buttons missing/wrong", "buttons": btn_texts})
    else:
        pr["hero_buttons"] = []
        report["problems"].append({"sev": "P1", "route": route, "what": "no hero section in main"})

    report["pages"][route] = pr

# ---- orphans: every route linked from >=1 other page (excluding self) ----
all_routes = set(p["route"] for p in PAGES)
linked_to = Counter()
for src, tgts in link_graph.items():
    for t in tgts:
        if t != src:
            linked_to[t] += 1
orphans = [r for r in all_routes if linked_to.get(r, 0) == 0]
report["site"]["orphans"] = orphans
report["site"]["linked_to_counts"] = {r: linked_to.get(r, 0) for r in sorted(all_routes)}
if orphans:
    report["problems"].append({"sev": "P2", "what": "orphan route(s) — no other page links to them", "routes": orphans})

# ---- sitemap / robots / llms ----
sm = open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", sm)
report["site"]["sitemap_locs"] = len(locs)
report["site"]["sitemap_lastmods"] = len(lastmods)
report["site"]["sitemap_lastmod_values"] = sorted(set(lastmods))
report["site"]["sitemap_urls"] = locs
exp_locs = {"http://localhost:3000" + ("" if r == "/" else r) for r in all_routes}
if set(locs) != exp_locs:
    report["problems"].append({"sev": "P1", "what": "sitemap loc set != 31 routes", "missing": sorted(exp_locs - set(locs)), "extra": sorted(set(locs) - exp_locs)})
if sorted(set(lastmods)) != ["2026-11-12"]:
    report["problems"].append({"sev": "P2", "what": "sitemap lastmod not all date-only 2026-11-12", "values": sorted(set(lastmods))})
robots = open(os.path.join(OUT, "robots.txt"), encoding="utf-8").read()
report["site"]["robots"] = robots
if "Host:" in robots:
    report["problems"].append({"sev": "P2", "what": "robots.txt contains Host: line"})
if "Allow: /" not in robots:
    report["problems"].append({"sev": "P2", "what": "robots.txt missing Allow: /"})
llms = open(os.path.join(OUT, "llms.txt"), encoding="utf-8").read()
llms_urls = [l.strip() for l in llms.splitlines() if l.strip().startswith("http")]
report["site"]["llms_url_count"] = len(llms_urls)
if set(llms_urls) != exp_locs:
    report["problems"].append({"sev": "P2", "what": "llms.txt URL set != 31 routes", "missing": sorted(exp_locs - set(llms_urls)), "extra": sorted(set(llms_urls) - exp_locs)})

# ---- grep gates over built HTML ----
double_slash = 0
unpref_href_src = 0
unpref_img = 0
favicon_ok = True
for dp, _, fns in os.walk(OUT):
    for fn in fns:
        if not fn.endswith(".html"):
            continue
        h = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
        double_slash += h.count("//midvale-water-damage")
        for m in re.finditer(r'(?:href|src)="(/[^"]*)"', h):
            v = m.group(1)
            if not v.startswith("/midvale-water-damage"):
                unpref_href_src += 1
        for m in re.finditer(r'<img[^>]*src="(/[^"]*)"', h):
            if not m.group(1).startswith("/midvale-water-damage"):
                unpref_img += 1
        if 'rel="icon"' in h and '/midvale-water-damage/favicon' not in h:
            favicon_ok = False
report["site"]["grep_double_slash"] = double_slash
report["site"]["grep_unprefixed_href_src"] = unpref_href_src
report["site"]["grep_unprefixed_img"] = unpref_img
report["site"]["favicon_prefixed_all_pages"] = favicon_ok
if double_slash:
    report["problems"].append({"sev": "P1", "what": "double-slash prefix in built HTML", "count": double_slash})
if unpref_href_src:
    report["problems"].append({"sev": "P1", "what": "unprefixed root-relative href/src in built HTML", "count": unpref_href_src})
if unpref_img:
    report["problems"].append({"sev": "P1", "what": "unprefixed img src in built HTML", "count": unpref_img})
if not favicon_ok:
    report["problems"].append({"sev": "P2", "what": "favicon not prefixed on some page"})

# ---- traces ----
BANNED = ["Tulsa", "Lancaster", "Plano", "Fort Myers", "Naples", "Stockbridge",
          "McDonough", "Boynton Beach", "Broken Arrow", "Lynnwood", "San Bruno",
          "Pleasant Grove", "Acworth", "Apopka", "Elyria", "Belleville",
          "Chesterfield", "Edmond", "Owasso", "Krum", "Justin", "Pilot Point",
          "lorem", "Lorem", "TODO", "FIXME", "AI-generated", "AI generated",
          "(918)", "(385) 346", "(407) 787", "(470) 672", "(618) 330", "(636) 228",
          "noorullah", "growthaura", "github.io"]
trace_hits = []
for dp, _, fns in os.walk(OUT):
    for fn in fns:
        if not (fn.endswith(".html") or fn.endswith(".txt") or fn.endswith(".xml")):
            continue
        if fn.endswith(".txt") and ("chunks" in dp or True) and fn not in ("llms.txt", "robots.txt"):
            pass
        pth = os.path.join(dp, fn)
        try:
            h = open(pth, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        # skip RSC flight payloads (out/*.txt) for trace scan of visible text; still scan html
        if fn.endswith(".txt") and fn != "llms.txt":
            continue
        for term in BANNED:
            if term in h:
                # localhost is allowed in sitemap/robots/llms/canonicals; handled separately
                trace_hits.append({"file": os.path.relpath(pth, OUT), "term": term})
report["site"]["trace_hits"] = trace_hits
if trace_hits:
    report["problems"].append({"sev": "P2", "what": "old-site/other-site trace term(s) in built output", "detail": trace_hits[:30]})

# localhost outside allowed files
lh_files = []
for dp, _, fns in os.walk(OUT):
    for fn in fns:
        if not fn.endswith(".html"):
            continue
        h = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
        if "localhost" in h:
            lh_files.append(os.path.relpath(os.path.join(dp, fn), OUT))
report["site"]["localhost_in_html"] = lh_files
if lh_files:
    report["problems"].append({"sev": "P3", "what": "localhost string in built HTML page(s) (expected only in sitemap/robots/llms/canonicals)", "files": lh_files})

# ---- images: md5 within site ----
img_dir = os.path.join(ROOT, "public", "images")
hashes = {}
for dp, _, fns in os.walk(img_dir):
    for fn in fns:
        fp = os.path.join(dp, fn)
        md5 = hashlib.md5(open(fp, "rb").read()).hexdigest()
        hashes.setdefault(md5, []).append(os.path.relpath(fp, ROOT))
dups = {k: v for k, v in hashes.items() if len(v) > 1}
report["site"]["image_files"] = sum(len(v) for v in hashes.values())
report["site"]["image_md5_dup_groups"] = dups
if dups:
    report["problems"].append({"sev": "P1", "what": "duplicate image files by md5 within site", "detail": dups})

json.dump(report, open(os.path.join(ROOT, "qa", "verify-rebuild-static.json"), "w"), indent=1)

# ---- console summary ----
print(f"pages checked: {len(report['pages'])}")
print(f"problems: {len(report['problems'])}")
for prob in report["problems"]:
    print(" -", prob["sev"], prob.get("route", ""), prob["what"], str(prob.get("detail", prob.get("missing", prob.get("sample", ""))))[:220])
print("--- per-page main words vs expected ---")
for r, pr in report["pages"].items():
    print(f"{r}: main={pr.get('main_words')} expected={pr.get('expected_words')} missing={pr.get('missing_words')} extra={pr.get('extra_words')} fullness={pr.get('fullness')} h1_ok={pr.get('h1_ok')} title_ok={pr.get('title_ok')} meta_ok={pr.get('meta_ok')} faq_ld={pr.get('faq_ld_count')}/{pr.get('faq_data_count')}")
print("--- site ---")
print("orphans:", report["site"]["orphans"])
print("sitemap locs:", report["site"]["sitemap_locs"], "lastmods:", report["site"]["sitemap_lastmod_values"])
print("llms urls:", report["site"]["llms_url_count"])
print("gates: double-slash", double_slash, "unpref href/src", unpref_href_src, "unpref img", unpref_img, "favicon ok", favicon_ok)
print("trace hits:", len(trace_hits), "localhost in html:", lh_files)
print("images:", report["site"]["image_files"], "md5 dup groups:", len(dups))
