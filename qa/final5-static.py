#!/usr/bin/env python3
"""W1 — Stage 5 FINAL static checks for Midvale UT (fresh, independent).
Reads only out/ + lib/pages-data.json; writes qa/final5-static.json.
Server: http://127.0.0.1:8350/midvale-water-damage/ (subpath mirror of out/).
Data sha256 must be 21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f.
"""
import json, re, os, sys, hashlib, urllib.request, urllib.error
from collections import Counter, defaultdict
from bs4 import BeautifulSoup

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
BASE = "http://127.0.0.1:8350/midvale-water-damage"
SITE = "https://growthaura.github.io/midvale-water-damage"
EXPECTED_SHA = "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f"
TOKEN_RE = re.compile(r"[a-z0-9]+")
WS_RE = re.compile(r"\s+")
# Doc link annotations "Name (/route/)" rendered as real links (or plain anchor text
# where the target is already linked on the page). The syntax itself must not appear.
ANN_RE = re.compile(r"\(\s*/[a-z0-9][a-z0-9/_.\-]*\s*/\s*\)", re.I)
ANN_FIND = re.compile(r"\(\s*(/[a-z0-9][a-z0-9/_.\-]*\s*/)\s*\)", re.I)

def anchor_before(text, paren_start):
    """Anchor phrase immediately before an annotation paren: text after the last
    sentence boundary, minus a leading 'see'."""
    before = text[:paren_start].rstrip()
    idx = max(before.rfind(". "), before.rfind("! "), before.rfind("? "),
              before.rfind("; "), before.rfind(": "), before.rfind("— "), before.rfind("– "))
    cand = before[idx + 2:] if idx >= 0 else before
    cand = re.sub(r"^(see|See)\s+", "", cand)
    return cand.strip()

def toks(text):
    return TOKEN_RE.findall((text or "").lower())

def norm(text):
    return " ".join(toks(text))

def find_subseq(hay, needle):
    n, m = len(hay), len(needle)
    if m == 0:
        return 0
    if m > n:
        return -1
    first = needle[0]
    for i in range(n - m + 1):
        if hay[i] == first and hay[i:i + m] == needle:
            return i
    return -1

def longest_prefix(hay, needle):
    for L in range(len(needle), 0, -1):
        if find_subseq(hay, needle[:L]) >= 0:
            return L
    return 0

def route_to_file(route):
    return os.path.join(OUT, "index.html") if route == "/" else os.path.join(OUT, route.strip("/") + ".html")

def local_url(path):
    """Map a site path (e.g. /midvale-water-damage/about or /about) to local URL."""
    if path.startswith("/midvale-water-damage"):
        rel = path[len("/midvale-water-damage"):]
    else:
        rel = path
    if rel == "" or rel == "/":
        return BASE + "/"
    return BASE + rel

def curl_status(url, timeout=10):
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "final5-static/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            r.read(1)
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"ERR:{type(e).__name__}:{e}"

# ---------- 0. data integrity ----------
sha = hashlib.sha256(open(os.path.join(ROOT, "lib/pages-data.json"), "rb").read()).hexdigest()
if sha != EXPECTED_SHA:
    print(f"FATAL: pages-data.json sha {sha} != expected {EXPECTED_SHA}")
    sys.exit(2)
DATA = json.load(open(os.path.join(ROOT, "lib/pages-data.json"), encoding="utf-8"))
PAGES = DATA["pages"]
ROUTES = [p["route"] for p in PAGES]

# sitemap routes (authoritative route list per task)
sitemap = open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", sitemap)
sitemap_routes = []
for loc in locs:
    assert loc.startswith(SITE), f"sitemap loc off-site: {loc}"
    sitemap_routes.append(loc[len(SITE):] or "/")
assert sorted(sitemap_routes) == sorted(ROUTES), "sitemap routes != pages-data routes"

report = {"data_sha256": sha, "routes": len(ROUTES), "checks": {}}
soups = {}
for route in ROUTES:
    soups[route] = BeautifulSoup(open(route_to_file(route), encoding="utf-8").read(), "html.parser")

# ---------- 1. Fullness (fresh parse per page; NEVER mutate the shared soups) ----------
full = {}
for route in ROUTES:
    fs = BeautifulSoup(open(route_to_file(route), encoding="utf-8").read(), "html.parser")
    for bad in fs(["script", "style", "noscript"]):
        bad.decompose()
    total_words = len(fs.get_text(" ").split())
    main = fs.find("main")
    main_words = len(main.get_text(" ").split()) if main else 0
    full[route] = {"total_visible_words": total_words, "main_words": main_words,
                   "status": "FULL" if main_words >= 300 else ("EMPTY" if main_words < 100 else "THIN")}
thin = [r for r, v in full.items() if v["status"] != "FULL"]
report["checks"]["fullness"] = {
    "pass": len(thin) == 0,
    "pages": full,
    "empty_pages": [r for r, v in full.items() if v["status"] == "EMPTY"],
    "thin_pages": [r for r, v in full.items() if v["status"] == "THIN"],
    "total_main_words": sum(v["main_words"] for v in full.values()),
    "total_visible_words": sum(v["total_visible_words"] for v in full.values()),
}

# ---------- 2. Verbatim segments ----------
# Data segments carry doc link annotations "Name (/route/)" which the build renders
# as real <a class="body-link"> links (or, where the target is already linked on the
# page e.g. homepage cards, as plain anchor text). The annotation syntax itself must
# NOT appear visibly (check 6). So verbatim is measured TWO ways:
#   (a) raw: segment text exactly as in data (annotation syntax included)
#   (b) normalized: annotation "(/.../)" stripped, matching the rendered form
# Plus a per-annotation audit: every annotation's anchor words must be in <main>,
# and its target route must be linked on the same page (body-link in <main>, or
# card/nav/footer link for deduped targets — one link per target per page).
verb = {}
ann_audit = {}
for p in PAGES:
    route = p["route"]
    main = soups[route].find("main")
    actual = toks(main.get_text(" "))
    segs = []
    if p.get("eyebrow"):
        segs.append(("eyebrow", p["eyebrow"]))
    segs.append(("h1", p["h1"]))
    segs.append(("intro", p["intro"]))
    for i, ch in enumerate(p.get("trustChips") or []):
        segs.append((f"trustChip{i}", ch))
    for bi, b in enumerate(p["blocks"]):
        t = b["type"]
        if t in ("h2", "h3"):
            segs.append((f"block{bi}:{t}", b["text"]))
        elif t == "p":
            segs.append((f"block{bi}:p", "".join(s["t"] for s in b["segments"])))
        elif t in ("ul", "ol"):
            for ii, it in enumerate(b["items"]):
                segs.append((f"block{bi}:{t}[{ii}]", "".join(s["t"] for s in it["segments"])))
        elif t == "table":
            segs.append((f"block{bi}:table-headers", " ".join(b["headers"])))
            for ri, r in enumerate(b["rows"]):
                segs.append((f"block{bi}:table-row{ri}", " ".join(r)))
        else:
            segs.append((f"block{bi}:UNKNOWN-TYPE-{t}", ""))
    for fi, f in enumerate(p.get("faqs") or []):
        segs.append((f"faq{fi}:q", f["q"]))
        segs.append((f"faq{fi}:a", f["a"]))
    missing, changed = [], []
    missing_norm, changed_norm = [], []
    anns = []
    for label, text in segs:
        # collect annotations in this segment (anchor phrase + target route)
        for m in ANN_FIND.finditer(text):
            anns.append({"seg": label, "anchor": anchor_before(text, m.start()),
                         "route": m.group(1).strip()})
        nt = toks(text)
        if find_subseq(actual, nt) < 0:
            sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
            all_present = bool(sents) and all(find_subseq(actual, toks(s)) >= 0 for s in sents)
            entry = {"seg": label, "tokens": len(nt),
                     "present_prefix_tokens": longest_prefix(actual, nt), "text": text[:240]}
            if all_present:
                changed.append({**entry, "kind": "reordered (all sentences present, not contiguous)"})
            else:
                missing.append({**entry, "kind": "missing sentences",
                                "missing_sentences": [s[:200] for s in sents if find_subseq(actual, toks(s)) < 0][:4]})
        # normalized pass: annotation syntax stripped
        ntext = ANN_RE.sub("", text)
        nnt = toks(ntext)
        if find_subseq(actual, nnt) < 0:
            sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", ntext) if s.strip()]
            all_present = bool(sents) and all(find_subseq(actual, toks(s)) >= 0 for s in sents)
            entry = {"seg": label, "tokens": len(nnt),
                     "present_prefix_tokens": longest_prefix(actual, nnt), "text": ntext[:240]}
            if all_present:
                changed_norm.append({**entry, "kind": "reordered (all sentences present, not contiguous)"})
            else:
                missing_norm.append({**entry, "kind": "missing sentences",
                                     "missing_sentences": [s[:200] for s in sents if find_subseq(actual, toks(s)) < 0][:4]})
    # annotation -> rendered link audit for this page (ROUTE-level reconciliation).
    # Per-page rule (one link per target per page): each distinct annotation route must
    # be linked on the page (body-link in <main>, or card/nav/footer link), and every
    # body-link's route must come from an annotation (no builder-added body links).
    # Anchor wording is proven separately by the normalized verbatim check (0 missing).
    soup = soups[route]
    ann_routes = [a["route"].rstrip("/") or "/" for a in anns]
    body_routes = []
    for a in (main.find_all("a", href=True) if main else []):
        if "body-link" in (a.get("class") or []):
            href = a["href"].split("#")[0].split("?")[0]
            if href.startswith("/midvale-water-damage"):
                href = href[len("/midvale-water-damage"):] or "/"
            if href.startswith("/"):
                body_routes.append(href)
    page_routes = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#")[0].split("?")[0]
        if href.startswith("/midvale-water-damage"):
            href = href[len("/midvale-water-damage"):] or "/"
        if href.startswith("/"):
            page_routes.add(href)
    ann_results = []
    for an, target in zip(anns, ann_routes):
        ann_results.append({**an, "target": target,
                            "route_linked_via_body_link": target in body_routes,
                            "target_linked_on_page": target in page_routes})
    ann_audit[route] = {"annotations": ann_results,
                        "ann_count": len(anns),
                        "ann_distinct_routes": len(set(ann_routes)),
                        "body_link_count": len(body_routes),
                        "body_routes_not_in_annotations": sorted(set(body_routes) - set(ann_routes)),
                        "ann_routes_not_linked_on_page": sorted(set(ann_routes) - page_routes)}
    verb[route] = {"segments": len(segs), "missing": len(missing), "changed_reordered": len(changed),
                   "missing_detail": missing, "changed_detail": changed,
                   "missing_normalized": len(missing_norm), "changed_normalized": len(changed_norm),
                   "missing_norm_detail": missing_norm, "changed_norm_detail": changed_norm,
                   "annotations": len(anns)}
tot_seg = sum(v["segments"] for v in verb.values())
tot_miss = sum(v["missing"] for v in verb.values())
tot_chg = sum(v["changed_reordered"] for v in verb.values())
tot_miss_n = sum(v["missing_normalized"] for v in verb.values())
tot_chg_n = sum(v["changed_normalized"] for v in verb.values())
tot_ann = sum(v["ann_count"] for v in ann_audit.values())
tot_ann_distinct = sum(v["ann_distinct_routes"] for v in ann_audit.values())
ann_no_link = [a for v in ann_audit.values() for a in v["annotations"] if not a["target_linked_on_page"]]
ann_body_routes_unmatched = [r for v in ann_audit.values() for r in v["body_routes_not_in_annotations"]]
ann_routes_unlinked = [r for v in ann_audit.values() for r in v["ann_routes_not_linked_on_page"]]
ann_body = sum(v["body_link_count"] for v in ann_audit.values())  # == rendered body-links (143)
ann_plain = tot_ann - ann_body  # rendered as plain text (deduped: target linked elsewhere on page)
report["checks"]["verbatim"] = {"pass": tot_miss_n == 0 and tot_chg_n == 0 and not ann_no_link
                                and not ann_body_routes_unmatched and not ann_routes_unlinked,
                                "total_segments": tot_seg,
                                "missing_raw_annotation_syntax": tot_miss, "changed_reordered_raw": tot_chg,
                                "missing_normalized": tot_miss_n, "changed_normalized": tot_chg_n,
                                "annotations_total": tot_ann,
                                "annotations_distinct_routes_per_page_sum": tot_ann_distinct,
                                "annotations_as_body_links": ann_body,
                                "annotations_as_plain_text_deduped": ann_plain,
                                "annotations_with_target_not_linked_on_page": ann_no_link,
                                "body_link_routes_not_in_annotations": ann_body_routes_unmatched,
                                "annotation_routes_not_linked_on_page": ann_routes_unlinked,
                                "per_page": verb, "annotation_audit": ann_audit}

# ---------- 3. FAQ visible vs schema ----------
faq_vis_total = 0
faq_detail = {}
for route, soup in soups.items():
    items = soup.find_all(class_="faq-item")
    vis = []
    for it in items:
        h = it.find("h3")
        a = it.find("p")
        vis.append({"q": norm(h.get_text()) if h else "", "a": norm(a.get_text()) if a else ""})
    faq_vis_total += len(vis)
    # schema FAQPage
    schema_qs = []
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(sc.string)
        except Exception:
            continue
        if isinstance(d, dict) and d.get("@type") == "FAQPage":
            for e in d.get("mainEntity") or []:
                ans = e.get("acceptedAnswer") or {}
                schema_qs.append({"q": norm(e.get("name", "")), "a": norm(ans.get("text", ""))})
    data_qs = [{"q": norm(ANN_RE.sub("", f["q"])), "a": norm(ANN_RE.sub("", f["a"]))}
               for f in next(p for p in PAGES if p["route"] == route).get("faqs") or []]
    q_match = sorted(x["q"] for x in vis) == sorted(x["q"] for x in schema_qs)
    a_match = sorted(x["a"] for x in vis) == sorted(x["a"] for x in schema_qs)
    faq_detail[route] = {"visible": len(vis), "schema": len(schema_qs), "data": len(data_qs),
                         "q_text_match": q_match, "a_text_match": a_match,
                         "visible_eq_data": vis == data_qs}
faq_bad = [r for r, v in faq_detail.items() if not (v["q_text_match"] and v["a_text_match"] and v["visible_eq_data"])]
report["checks"]["faq"] = {"pass": faq_vis_total == 142 and not faq_bad,
                           "visible_total": faq_vis_total, "expected": 142,
                           "mismatched_pages": faq_bad, "per_page": faq_detail}

# ---------- 4. Tables ----------
tables_total = sum(len(s.find_all("table")) for s in soups.values())
report["checks"]["tables"] = {"pass": tables_total == 43, "total": tables_total, "expected": 43,
                              "per_page": {r: len(s.find_all("table")) for r, s in soups.items()}}

# ---------- 5. Links ----------
body_links = 0
card_links = 0
internal_hrefs = Counter()
external_hrefs = Counter()
self_body = []
incoming = defaultdict(set)   # route -> set of source routes linking to it (other pages only)
all_page_links = {}
for route, soup in soups.items():
    page_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        cls = a.get("class") or []
        is_card = "card-wrap-link" in cls
        is_body = "body-link" in cls
        if is_card:
            card_links += 1
        if is_body:
            body_links += 1
        if href.startswith("tel:") or href.startswith("mailto:") or href == "" or href.startswith("#"):
            continue
        if href.startswith("http://") or href.startswith("https://"):
            external_hrefs[href] += 1
            continue
        # internal
        path = href.split("#")[0].split("?")[0]
        if path.startswith("/midvale-water-damage"):
            path = path[len("/midvale-water-damage"):] or "/"
        internal_hrefs[path] += 1
        page_links.append({"href": href, "path": path, "class": " ".join(cls), "text": a.get_text(" ").strip()[:60]})
        if path != route:
            incoming[path].add(route)
        if is_body and path == route:
            self_body.append({"route": route, "href": href, "text": a.get_text(" ").strip()[:80]})
    all_page_links[route] = page_links

# curl every unique internal target (paths that look like site routes)
targets = sorted({p for p in internal_hrefs if p.startswith("/")})
curl_results = {}
for p in targets:
    curl_results[p] = curl_status(local_url(p))
broken = {p: s for p, s in curl_results.items() if s != 200}
orphans = [r for r in ROUTES if len(incoming.get(r, set())) == 0]
report["checks"]["links"] = {
    "pass": body_links == 143 and card_links == 19 and not broken and not orphans and not self_body,
    "body_links": body_links, "expected_body": 143,
    "card_wrap_links": card_links, "expected_card": 19,
    "total_body_plus_card": body_links + card_links, "expected_total": 162,
    "unique_internal_targets": len(targets),
    "total_internal_href_instances": sum(internal_hrefs.values()),
    "external_href_instances": sum(external_hrefs.values()),
    "broken_targets": broken,
    "orphan_routes": orphans,
    "self_links_body_copy": self_body,
    "curl_results": curl_results,
}

# ---------- 6. Parenthetical path annotations ----------
paren_re = re.compile(r"\(\s*/[a-z0-9][a-z0-9/_.\-]*\s*\)", re.I)
paren_hits = {}
for route, soup in soups.items():
    txt = soup.get_text(" ")
    hits = paren_re.findall(txt)
    if hits:
        paren_hits[route] = hits
report["checks"]["paren_paths"] = {"pass": not paren_hits, "total": sum(len(v) for v in paren_hits.values()),
                                   "hits": paren_hits}

# ---------- 7. localhost:3000 ----------
lh_hits = []
for root, _, files in os.walk(OUT):
    for fn in files:
        if fn.endswith((".html", ".xml", ".txt")):
            fp = os.path.join(root, fn)
            data = open(fp, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r"http://localhost:3000", data):
                lh_hits.append({"file": os.path.relpath(fp, OUT), "context": data[max(0, m.start() - 80):m.end() + 80]})
# _next JS chunks separately (framework code note)
lh_js = []
for root, _, files in os.walk(os.path.join(OUT, "_next")):
    for fn in files:
        fp = os.path.join(root, fn)
        data = open(fp, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"localhost:3000", data):
            lh_js.append({"file": os.path.relpath(fp, OUT), "context": data[max(0, m.start() - 80):m.end() + 80]})
report["checks"]["localhost"] = {"pass": not lh_hits, "html_xml_txt_hits": lh_hits,
                                 "next_js_chunk_hits": len(lh_js), "next_js_contexts": lh_js[:5]}

# ---------- 8. Double-slash absolute URLs ----------
ds_hits = []
for root, _, files in os.walk(OUT):
    for fn in files:
        if fn.endswith((".html", ".xml", ".txt")):
            fp = os.path.join(root, fn)
            data = open(fp, encoding="utf-8", errors="replace").read()
            for m in re.finditer(re.escape(SITE) + r"//", data):
                ds_hits.append({"file": os.path.relpath(fp, OUT), "context": data[max(0, m.start() - 60):m.end() + 60]})
report["checks"]["double_slash"] = {"pass": not ds_hits, "total": len(ds_hits), "hits": ds_hits}

# ---------- 9. robots.txt + sitemap ----------
robots = open(os.path.join(OUT, "robots.txt"), encoding="utf-8").read()
robots_lines = [l.strip() for l in robots.strip().splitlines() if l.strip()]
sitemap_status = {}
for loc in locs:
    path = loc[len(SITE):] or "/"
    sitemap_status[loc] = curl_status(local_url(path))
sitemap_bad = {u: s for u, s in sitemap_status.items() if s != 200}
lastmod_ok = all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", lm) for lm in lastmods) and len(lastmods) == len(locs)
report["checks"]["robots_sitemap"] = {
    "pass": ("Allow: /" in robots_lines and not any(l.lower().startswith("host:") for l in robots_lines)
             and f"Sitemap: {SITE}/sitemap.xml" in robots_lines and len(locs) == 31 and lastmod_ok and not sitemap_bad),
    "robots_lines": robots_lines,
    "has_allow_root": "Allow: /" in robots_lines,
    "has_host_line": any(l.lower().startswith("host:") for l in robots_lines),
    "sitemap_line": f"Sitemap: {SITE}/sitemap.xml" in robots_lines,
    "sitemap_locs": len(locs), "lastmod_all_date_only": lastmod_ok,
    "sitemap_non200": sitemap_bad,
}

# ---------- 10. robots meta ----------
meta_404 = BeautifulSoup(open(os.path.join(OUT, "404.html"), encoding="utf-8").read(), "html.parser")
m404 = [m.get("content") for m in meta_404.find_all("meta", attrs={"name": "robots"})]
meta_pages = {}
for route, soup in soups.items():
    meta_pages[route] = [m.get("content") for m in soup.find_all("meta", attrs={"name": "robots"})]
meta_bad = {r: v for r, v in meta_pages.items() if v != ["index, follow"]}
report["checks"]["robots_meta"] = {
    "pass": m404 == ["noindex"] and not meta_bad,
    "page_404_meta": m404,
    "pages_not_exactly_index_follow": meta_bad,
}

# ---------- 11. JSON-LD ----------
type_counts = Counter()
parse_errors = []
schema_localhost = []
schema_dslash = []
image_urls = []
for route, soup in soups.items():
    for sc in soup.find_all("script", type="application/ld+json"):
        raw = sc.string or ""
        if "localhost" in raw:
            schema_localhost.append({"route": route, "snippet": raw[raw.find("localhost") - 40:raw.find("localhost") + 60]})
        if SITE + "//" in raw:
            schema_dslash.append({"route": route})
        try:
            d = json.loads(raw)
        except Exception as e:
            parse_errors.append({"route": route, "error": str(e), "snippet": raw[:200]})
            continue
        items = d if isinstance(d, list) else [d]
        for it in items:
            t = it.get("@type")
            type_counts[t] += 1
            if t == "ImageObject":
                image_urls.append({"route": route, "contentUrl": it.get("contentUrl")})
total_blocks = sum(type_counts.values())
expected_types = {"BreadcrumbList": 31, "FAQPage": 28, "WebPage": 31, "ImageObject": 31,
                  "HowTo": 36, "Service": 19, "HomeAndConstructionBusiness": 1, "WebSite": 1}
type_mismatch = {t: (type_counts.get(t, 0), e) for t, e in expected_types.items() if type_counts.get(t, 0) != e}
extra_types = {t: c for t, c in type_counts.items() if t not in expected_types}
# ImageObject contentUrl curls
img_status = {}
doubled_subpath = []
for iu in image_urls:
    u = iu["contentUrl"] or ""
    if "/midvale-water-damage/midvale-water-damage/" in u:
        doubled_subpath.append(iu)
    if u.startswith(SITE):
        img_status[u] = curl_status(u.replace(SITE, BASE))
    elif u.startswith("/"):
        img_status[u] = curl_status(local_url(u))
    else:
        img_status[u] = "NOT-SITE-URL"
img_bad = {u: s for u, s in img_status.items() if s != 200}
report["checks"]["jsonld"] = {
    "pass": total_blocks == 178 and not type_mismatch and not extra_types and not parse_errors
            and not img_bad and not doubled_subpath and not schema_localhost and not schema_dslash,
    "total_blocks": total_blocks, "expected_total": 178,
    "type_counts": dict(type_counts), "expected_types": expected_types,
    "type_mismatches": type_mismatch, "unexpected_types": extra_types,
    "parse_errors": parse_errors,
    "imageobject_count": len(image_urls),
    "imageobject_non200": img_bad,
    "imageobject_doubled_subpath": doubled_subpath,
    "schema_localhost_hits": schema_localhost,
    "schema_double_slash_hits": schema_dslash,
}

# 404.html JSON-LD (informational only, not in the 178)
s404 = BeautifulSoup(open(os.path.join(OUT, "404.html"), encoding="utf-8").read(), "html.parser")
report["info_404_jsonld_blocks"] = len(s404.find_all("script", type="application/ld+json"))

# overall
report["overall_pass"] = all(c.get("pass") for c in report["checks"].values())
json.dump(report, open(os.path.join(ROOT, "qa", "final5-static.json"), "w"), indent=1)

for name, c in report["checks"].items():
    print(f"{name}: {'PASS' if c.get('pass') else 'FAIL'}")
print("OVERALL:", "PASS" if report["overall_pass"] else "FAIL")
print(f"fullness: total main words {report['checks']['fullness']['total_main_words']}, "
      f"thin={report['checks']['fullness']['thin_pages']} empty={report['checks']['fullness']['empty_pages']}")
print(f"verbatim: segs={tot_seg} missing_raw={tot_miss} reordered_raw={tot_chg} "
      f"missing_normalized={tot_miss_n} reordered_normalized={tot_chg_n} "
      f"annotations={tot_ann} distinct_routes={tot_ann_distinct} as_body_links={ann_body} as_plain_text={ann_plain} "
      f"no_link={len(ann_no_link)} body_routes_unmatched={ann_body_routes_unmatched} ann_routes_unlinked={ann_routes_unlinked}")
print(f"faq visible={faq_vis_total} mismatched_pages={faq_bad}")
print(f"tables={tables_total}")
print(f"links body={body_links} card={card_links} broken={broken} orphans={orphans} self_body={len(self_body)}")
print(f"paren={report['checks']['paren_paths']['total']} localhost_html={len(lh_hits)} localhost_js={len(lh_js)} dslash={len(ds_hits)}")
print(f"jsonld total={total_blocks} types={dict(type_counts)} parse_err={len(parse_errors)} img_bad={img_bad}")
print(f"sitemap locs={len(locs)} non200={sitemap_bad} lastmod_ok={lastmod_ok}")
print(f"robots meta 404={m404} bad_pages={list(meta_bad)}")
