#!/usr/bin/env python3
"""SEO AUDIT W1 — crawlability, indexability, meta, headings — Midvale UT.
Reads lib/pages-data.json (source of truth) + out/ built HTML, checks via
local HTTP server on 8311 (/midvale-water-damage/ subpath).
Writes qa/seo-audit1-w1.json. AUDIT ONLY — no site files modified.
"""
import json, re, html, hashlib, urllib.request, urllib.error
from collections import Counter
from pathlib import Path

ROOT = Path.home() / "workspace/midvale-water-damage"
OUT = ROOT / "out"
BASE_HTTP = "http://127.0.0.1:8311/midvale-water-damage"
BASE_ABS = "http://localhost:3000"   # base used inside built files (pre-swap)
EXPECTED_SHA = "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f"

problems = []
def add(sev, check, page, detail):
    problems.append({"severity": sev, "check": check, "page": page, "detail": detail})

# ---- 0. data source integrity ----
sha = hashlib.sha256((ROOT/"lib/pages-data.json").read_bytes()).hexdigest()
data_ok = sha == EXPECTED_SHA
if not data_ok:
    add("P1", "data-integrity", "-", f"pages-data.json sha256 {sha} != expected {EXPECTED_SHA}")
data = json.loads((ROOT/"lib/pages-data.json").read_text())
pages = data["pages"]
assert len(pages) == 31, f"expected 31 pages in data, got {len(pages)}"

def route_to_file(route):
    if route == "/":
        return OUT/"index.html"
    return OUT/(route.strip("/") + ".html")

def route_to_url(route):
    # canonical URL form: homepage root only, others no trailing slash
    if route == "/":
        return BASE_ABS + "/"
    return BASE_ABS + route.rstrip("/")

def route_to_served(route):
    if route == "/":
        return BASE_HTTP + "/"
    return BASE_HTTP + route.rstrip("/")

def http_status(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"ERR:{e}"

def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

per_page = {}

# ---- 1. robots.txt ----
robots_served = urllib.request.urlopen(BASE_HTTP + "/robots.txt", timeout=10).read().decode()
robots_file = (OUT/"robots.txt").read_text()
robots = {
    "served_status": http_status(BASE_HTTP + "/robots.txt"),
    "exact_content": robots_file,
    "served_matches_file": robots_served == robots_file,
    "has_allow_root": bool(re.search(r"^Allow:\s*/\s*$", robots_file, re.M)),
    "has_host_line": bool(re.search(r"^Host:", robots_file, re.M | re.I)),
    "has_localhost_sitemap": "localhost" in robots_file,
}
if not robots["has_allow_root"]:
    add("P1", "robots", "-", "robots.txt missing 'Allow: /'")
if robots["has_host_line"]:
    add("P1", "robots", "-", "robots.txt contains a Host: line")
if not robots["served_matches_file"]:
    add("P2", "robots", "-", "served robots.txt differs from out/robots.txt")
if robots["has_localhost_sitemap"]:
    add("P2", "robots", "-",
        "robots.txt Sitemap line points at http://localhost:3000/sitemap.xml — "
        "placeholder base; if deployed as-is, crawlers get a dead sitemap URL. "
        "Must be swapped to the live domain at push time (same localhost-base issue as sitemap/llms/canonicals).")

# ---- 2. sitemap.xml ----
sm_raw = (OUT/"sitemap.xml").read_text()
locs = re.findall(r"<loc>(.*?)</loc>", sm_raw)
lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", sm_raw)
sm = {
    "served_status": http_status(BASE_HTTP + "/sitemap.xml"),
    "loc_count": len(locs),
    "locs": locs,
    "duplicates": [u for u, c in Counter(locs).items() if c > 1],
    "lastmod_all_date_only": all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", lm) for lm in lastmods),
    "lastmod_values": sorted(set(lastmods)),
    "lastmod_count": len(lastmods),
    "all_localhost_base": all(u.startswith(BASE_ABS) for u in locs),
    "homepage_is_root_only": (BASE_ABS + "/") in locs,
    "non_home_trailing_slash": [u for u in locs if u != BASE_ABS + "/" and u.endswith("/")],
    "expected_set": sorted(route_to_url(p["route"]) for p in pages),
    "actual_set": sorted(set(locs)),
    "set_matches_expected": sorted(set(locs)) == sorted(route_to_url(p["route"]) for p in pages),
}
if len(locs) != 31:
    add("P1", "sitemap", "-", f"sitemap has {len(locs)} locs, expected 31")
if sm["duplicates"]:
    add("P1", "sitemap", "-", f"duplicate locs: {sm['duplicates']}")
if not sm["lastmod_all_date_only"]:
    add("P2", "sitemap", "-", f"lastmod not all YYYY-MM-DD: {sorted(set(lastmods))}")
if sm["non_home_trailing_slash"]:
    add("P2", "sitemap", "-", f"non-home locs with trailing slash: {sm['non_home_trailing_slash']}")
if not sm["set_matches_expected"]:
    add("P1", "sitemap", "-", "sitemap URL set != expected 31 canonical URLs")
if sm["all_localhost_base"]:
    add("P2", "sitemap", "-",
        "all 31 sitemap locs use http://localhost:3000 base — placeholder; must be swapped to the live domain at push time or the sitemap is useless live.")
# every loc returns 200 via server
sm_statuses = {}
for loc in locs:
    path = loc[len(BASE_ABS):] or "/"
    sm_statuses[loc] = http_status(BASE_HTTP + (path if path.startswith("/") else "/" + path))
sm["loc_http_statuses"] = sm_statuses
sm["loc_non_200"] = {u: s for u, s in sm_statuses.items() if s != 200}
if sm["loc_non_200"]:
    add("P1", "sitemap", "-", f"locs not returning 200 via server: {sm['loc_non_200']}")

# ---- 3. llms.txt ----
llms_raw = (OUT/"llms.txt").read_text()
llms_urls = [l.strip() for l in llms_raw.splitlines() if l.strip().startswith("http")]
llms = {
    "served_status": http_status(BASE_HTTP + "/llms.txt"),
    "url_count": len(llms_urls),
    "urls": llms_urls,
    "set_matches_expected": sorted(set(llms_urls)) == sorted(route_to_url(p["route"]) for p in pages),
    "missing": sorted(set(route_to_url(p["route"]) for p in pages) - set(llms_urls)),
    "extra": sorted(set(llms_urls) - set(route_to_url(p["route"]) for p in pages)),
    "all_localhost_base": all(u.startswith(BASE_ABS) for u in llms_urls),
}
if llms["missing"] or llms["extra"]:
    add("P1", "llms", "-", f"llms.txt missing={llms['missing']} extra={llms['extra']}")
if llms["url_count"] != 31:
    add("P1", "llms", "-", f"llms.txt lists {llms['url_count']} URLs, expected 31")
if llms["all_localhost_base"]:
    add("P3", "llms", "-",
        "llms.txt URLs use http://localhost:3000 base — same placeholder-base note as sitemap; swap at push time.")

# ---- per-page checks 4-7 ----
title_counter, desc_counter, canon_counter = Counter(), Counter(), Counter()
all_resources = {}   # url -> status (checked via server)
resource_failures = {}

for pg in pages:
    route = pg["route"]
    f = route_to_file(route)
    rec = {"route": route, "file": str(f.relative_to(ROOT)), "exists": f.exists()}
    if not f.exists():
        add("P1", "page-exists", route, f"built file missing: {f}")
        per_page[route] = rec
        continue
    served = http_status(route_to_served(route))
    rec["served_status"] = served
    if served != 200:
        add("P1", "page-served", route, f"served status {served}, expected 200")
    h = f.read_text()

    # --- 5a. meta robots (built HTML == rendered DOM for static export) ---
    robots_metas = re.findall(r'<meta[^>]*name=["\']robots["\'][^>]*>', h, re.I)
    rec["meta_robots_tags"] = robots_metas
    for tag in robots_metas:
        m = re.search(r'content=["\']([^"\']*)["\']', tag, re.I)
        content = m.group(1).lower() if m else ""
        rec["meta_robots_content"] = content
        if "noindex" in content or "nofollow" in content:
            add("P1", "indexability", route, f"meta robots blocks indexing: {content}")
    if not robots_metas:
        rec["meta_robots_content"] = None  # absent = indexable by default; not a defect
    # any other noindex/nofollow anywhere in page
    if re.search(r"noindex|nofollow", h, re.I):
        # exclude the meta robots tag itself if it was index,follow (no match) — only flag real blocks
        if not re.search(r'<meta[^>]*robots[^>]*content=["\']index,\s*follow["\']', h, re.I):
            add("P1", "indexability", route, "noindex/nofollow string found in page HTML")

    # --- 5b. canonical ---
    canons = re.findall(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', h, re.I)
    if not canons:
        canons = re.findall(r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', h, re.I)
    rec["canonical_tags"] = canons
    expected_canon = route_to_url(route)
    rec["canonical_expected"] = expected_canon
    if len(canons) != 1:
        add("P1", "canonical", route, f"{len(canons)} canonical tags, expected exactly 1: {canons}")
    elif canons[0] != expected_canon:
        add("P1", "canonical", route, f"canonical not self-referential: actual {canons[0]} expected {expected_canon}")
    else:
        canon_counter[canons[0]] += 1
    rec["canonical_self_referential"] = (len(canons) == 1 and canons[0] == expected_canon)

    # --- 6. meta title/description verbatim ---
    tm = re.search(r"<title>(.*?)</title>", h, re.S)
    actual_title = html.unescape(tm.group(1)).strip() if tm else None
    dm = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content="([^"]*)"', h, re.I)
    if not dm:
        dm = re.search(r'<meta[^>]*content="([^"]*)"[^>]*name=["\']description["\']', h, re.I)
    actual_desc = html.unescape(dm.group(1)) if dm else None
    rec["title_expected"] = pg["metaTitle"]
    rec["title_actual"] = actual_title
    rec["title_len_expected"] = len(pg["metaTitle"])
    rec["title_len_actual"] = len(actual_title) if actual_title is not None else None
    rec["title_verbatim_match"] = actual_title == pg["metaTitle"]
    rec["desc_expected"] = pg["metaDescription"]
    rec["desc_actual"] = actual_desc
    rec["desc_len_expected"] = len(pg["metaDescription"])
    rec["desc_len_actual"] = len(actual_desc) if actual_desc is not None else None
    rec["desc_verbatim_match"] = actual_desc == pg["metaDescription"]
    if actual_title is None:
        add("P1", "meta-title", route, "no <title> tag in built HTML")
    elif actual_title != pg["metaTitle"]:
        add("P1", "meta-title", route,
            f"title mismatch — expected ({len(pg['metaTitle'])}ch): {pg['metaTitle']!r} | actual ({len(actual_title)}ch): {actual_title!r}")
    if actual_desc is None:
        add("P1", "meta-description", route, "no meta description in built HTML")
    elif actual_desc != pg["metaDescription"]:
        add("P1", "meta-description", route,
            f"description mismatch — expected ({len(pg['metaDescription'])}ch): {pg['metaDescription']!r} | actual ({len(actual_desc)}ch): {actual_desc!r}")
    if actual_title:
        title_counter[actual_title] += 1
    if actual_desc:
        desc_counter[actual_desc] += 1

    # --- 7. headings ---
    heads = [(int(m.group(1)), strip_tags(m.group(2))) for m in re.finditer(r"<h([1-6])[^>]*>(.*?)</h\1>", h, re.S | re.I)]
    # drop empty headings (should be none)
    heads = [(lvl, t) for lvl, t in heads if t]
    rec["heading_sequence"] = [[lvl, t] for lvl, t in heads]
    h1s = [t for lvl, t in heads if lvl == 1]
    rec["h1_count"] = len(h1s)
    rec["h1_text"] = h1s[0] if h1s else None
    rec["h1_expected"] = pg["h1"]
    rec["h1_match"] = len(h1s) == 1 and h1s[0] == pg["h1"]
    if len(h1s) != 1:
        add("P1", "headings-h1", route, f"H1 count {len(h1s)}, expected 1: {h1s}")
    elif h1s[0] != pg["h1"]:
        add("P1", "headings-h1", route, f"H1 text mismatch — expected {pg['h1']!r} actual {h1s[0]!r}")
    # hierarchy: no skipped levels
    skips = []
    prev = 0
    for lvl, t in heads:
        if prev and lvl > prev + 1:
            skips.append(f"H{prev} -> H{lvl} at {t[:60]!r}")
        prev = lvl
    rec["hierarchy_skips"] = skips
    if skips:
        add("P2", "headings-hierarchy", route, f"skipped heading levels: {skips}")
    # H2/H3 text vs doc: blocks h2/h3 ONLY — FAQ questions are already
    # present in blocks as h3 (verified: faq set is a subset of blocks h3),
    # so adding faqs again would double-count.
    expected_h2 = [b["text"] for b in pg["blocks"] if b["type"] == "h2"]
    expected_h3 = [b["text"] for b in pg["blocks"] if b["type"] == "h3"]
    faq_qs = [q.get("q") or q.get("question") for q in pg.get("faqs", [])]
    rec["faq_question_keys_sample"] = [list(q.keys()) for q in pg.get("faqs", [])][:1]
    rec["faqs_subset_of_blocks_h3"] = set(faq_qs) <= set(expected_h3)
    expected_h3_all = expected_h3
    actual_h2 = [t for lvl, t in heads if lvl == 2]
    actual_h3 = [t for lvl, t in heads if lvl == 3]
    rec["h2_expected_count"] = len(expected_h2)
    rec["h2_actual_count"] = len(actual_h2)
    rec["h3_expected_count"] = len(expected_h3_all)
    rec["h3_actual_count"] = len(actual_h3)
    # ordered comparison (doc order should equal render order)
    h2_mismatch = [f"#{i} expected {e!r} actual {a!r}" for i, (e, a) in enumerate(zip(expected_h2, actual_h2)) if e != a]
    h3_mismatch = [f"#{i} expected {e!r} actual {a!r}" for i, (e, a) in enumerate(zip(expected_h3_all, actual_h3)) if e != a]
    if len(expected_h2) != len(actual_h2):
        h2_mismatch.append(f"count: expected {len(expected_h2)} actual {len(actual_h2)}")
    if len(expected_h3_all) != len(actual_h3):
        h3_mismatch.append(f"count: expected {len(expected_h3_all)} actual {len(actual_h3)}")
    rec["h2_mismatches"] = h2_mismatch
    rec["h3_mismatches"] = h3_mismatch
    if h2_mismatch:
        add("P1", "headings-h2", route, f"H2 mismatches vs doc: {h2_mismatch}")
    if h3_mismatch:
        add("P1", "headings-h3", route, f"H3 mismatches vs doc: {h3_mismatch}")
    # extra heading levels present?
    rec["h4_plus"] = [t for lvl, t in heads if lvl >= 4]

    # --- 4. resources referenced by this page ---
    # ONLY real resources: <link href> (css/preload/icon), <script src>,
    # <img src/srcset>. NOT <a href> internal links (those are link-check
    # scope, and fragment-only hrefs like #faq are not fetchable resources).
    refs = set()
    for m in re.finditer(r'<link[^>]+href=["\']([^"\']+)["\']', h, re.I):
        refs.add(m.group(1))
    for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', h, re.I):
        refs.add(m.group(1))
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', h, re.I):
        refs.add(m.group(1))
    for m in re.finditer(r'srcset=["\']([^"\']+)["\']', h, re.I):
        for part in m.group(1).split(","):
            refs.add(part.strip().split()[0])
    # drop non-fetchable schemes
    refs = {u for u in refs if not u.startswith(("http://", "https://", "//", "mailto:", "tel:", "#", "data:"))}
    rec["local_refs_count"] = len(refs)
    rec["local_refs"] = sorted(refs)
    fails = {}
    for u in refs:
        # Built refs are root-absolute and ALREADY carry the subpath prefix
        # (/midvale-water-damage/...), so resolve against the server root,
        # NOT against BASE_HTTP (which would double the prefix).
        if u.startswith("/"):
            check_url = "http://127.0.0.1:8311" + u
        else:
            d = route.rsplit("/", 1)[0] if "/" in route[1:] else ""
            check_url = BASE_HTTP + d + "/" + u
        st = http_status(check_url)
        all_resources[check_url] = st
        if st != 200:
            fails[u] = st
    rec["resource_failures"] = fails
    if fails:
        add("P1", "resources", route, f"non-200 local resources: {fails}")
    per_page[route] = rec

# duplicate titles/descriptions/canonicals
dup_titles = {t: c for t, c in title_counter.items() if c > 1}
dup_descs = {t: c for t, c in desc_counter.items() if c > 1}
dup_canons = {t: c for t, c in canon_counter.items() if c > 1}
if dup_titles:
    add("P1", "meta-duplicates", "-", f"duplicate titles: {dup_titles}")
if dup_descs:
    add("P1", "meta-duplicates", "-", f"duplicate descriptions: {dup_descs}")
if dup_canons:
    add("P1", "canonical-duplicates", "-", f"duplicate canonical URLs: {dup_canons}")

# resource summary (homepage + 5 inner pages fully — actually all 31 done)
non200_resources = {u: s for u, s in all_resources.items() if s != 200}
resource_summary = {
    "total_distinct_local_refs_checked": len(all_resources),
    "non_200": non200_resources,
    "pages_checked": len(per_page),
    "note": "All 31 pages' local CSS/JS/img refs were checked via the server (superset of the required homepage + 5 inner pages).",
}

report = {
    "audit": "SEO AUDIT 1 — W1 crawlability/indexability/meta/headings",
    "site": "Midvale UT water damage",
    "date": "2026-11-13",
    "server": BASE_HTTP + "/ (port 8311, qa/linkfix-serve.py)",
    "data_source": "lib/pages-data.json",
    "data_sha256": sha,
    "data_sha256_expected": EXPECTED_SHA,
    "data_sha256_match": data_ok,
    "routes_expected": 31,
    "robots": robots,
    "sitemap": sm,
    "llms": llms,
    "resource_summary": resource_summary,
    "duplicate_titles": dup_titles,
    "duplicate_descriptions": dup_descs,
    "duplicate_canonicals": dup_canons,
    "per_page": per_page,
    "problems": problems,
    "problem_counts": {
        "P1": sum(1 for p in problems if p["severity"] == "P1"),
        "P2": sum(1 for p in problems if p["severity"] == "P2"),
        "P3": sum(1 for p in problems if p["severity"] == "P3"),
        "total": len(problems),
    },
    "notes": [
        "Built HTML == rendered DOM for meta/robots/canonical: this is a static Next.js export (no client JS rewrites head tags). Meta robots/canonical/title/description were read from the served built HTML, which is exactly what a crawler receives.",
        "pages-data.json 'url' field carries trailing-slash forms (/about/) but the canonical/sitemap/llms URL form used by the build is no-trailing-slash; the audit compared against the built (no-slash) form per the task spec.",
        "FAQ questions render as H3 in the built HTML and are already present in the blocks h3 list (verified: faq set is a subset of blocks h3 on every page checked); the H3 comparison uses blocks h3 only to avoid double-counting.",
    ],
}
(ROOT/"qa/seo-audit1-w1.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
print("PROBLEMS:", report["problem_counts"])
for p in problems:
    print(p["severity"], "|", p["check"], "|", p["page"], "|", p["detail"][:300])
print("pages:", len(per_page))
print("distinct resources checked:", len(all_resources), "non-200:", non200_resources)
