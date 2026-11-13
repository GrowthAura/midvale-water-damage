#!/usr/bin/env python3
"""CYCLE 1 OPT — static technical SEO audit (crawl/index/meta/headings/schema-presence/404),
Midvale UT. AUDIT ONLY — reads out/ + lib/pages-data.json via local server on 8325.
Fresh export already run by coordinator; this script does NOT rebuild.
Writes qa/opt1-static.json."""
import json, re, html, hashlib, urllib.request, urllib.error
from collections import Counter
from pathlib import Path

ROOT = Path.home() / "workspace/midvale-water-damage"
OUT = ROOT / "out"
BASE_HTTP = "http://127.0.0.1:8325/midvale-water-damage"
BASE_SERVER = "http://127.0.0.1:8325"
SITE = "https://growthaura.github.io/midvale-water-damage"
EXPECTED_SHA = "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f"

problems = []
def add(sev, check, page, detail):
    problems.append({"severity": sev, "check": check, "page": page, "detail": detail})

sha = hashlib.sha256((ROOT / "lib/pages-data.json").read_bytes()).hexdigest()
data_ok = sha == EXPECTED_SHA
if not data_ok:
    add("P1", "data-integrity", "-", f"pages-data.json sha256 {sha} != expected {EXPECTED_SHA}")
    raise SystemExit("DATA HASH MISMATCH — stopping per task instructions")
data = json.loads((ROOT / "lib/pages-data.json").read_text())
pages = data["pages"]
assert len(pages) == 31, f"expected 31 pages in data, got {len(pages)}"

def route_to_file(route):
    return OUT / "index.html" if route == "/" else OUT / (route.strip("/") + ".html")

def route_to_url(route):
    return SITE + "/" if route == "/" else SITE + route.rstrip("/")

def route_to_served(route):
    return BASE_HTTP + "/" if route == "/" else BASE_HTTP + route.rstrip("/")

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
robots_file = (OUT / "robots.txt").read_text()
robots = {
    "served_status": http_status(BASE_HTTP + "/robots.txt"),
    "exact_content": robots_file,
    "served_matches_file": robots_served == robots_file,
    "has_allow_root": bool(re.search(r"^Allow:\s*/\s*$", robots_file, re.M)),
    "has_host_line": bool(re.search(r"^Host:", robots_file, re.M | re.I)),
    "sitemap_line": [l for l in robots_file.splitlines() if l.lower().startswith("sitemap:")],
}
if not robots["has_allow_root"]:
    add("P1", "robots", "-", "robots.txt missing 'Allow: /'")
if robots["has_host_line"]:
    add("P1", "robots", "-", "robots.txt contains a Host: line")
if not robots["served_matches_file"]:
    add("P2", "robots", "-", "served robots.txt differs from out/robots.txt")
if robots["sitemap_line"] != [f"Sitemap: {SITE}/sitemap.xml"]:
    add("P2", "robots", "-", f"robots Sitemap line unexpected: {robots['sitemap_line']}")

# ---- 2. sitemap.xml ----
sm_raw = (OUT / "sitemap.xml").read_text()
locs = re.findall(r"<loc>(.*?)</loc>", sm_raw)
lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", sm_raw)
sm = {
    "served_status": http_status(BASE_HTTP + "/sitemap.xml"),
    "loc_count": len(locs),
    "duplicates": [u for u, c in Counter(locs).items() if c > 1],
    "lastmod_all_date_only": all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", lm) for lm in lastmods),
    "lastmod_values": sorted(set(lastmods)),
    "lastmod_count": len(lastmods),
    "all_on_pages_url": all(u.startswith(SITE) for u in locs),
    "homepage_is_root_only": (SITE + "/") in locs,
    "non_home_trailing_slash": [u for u in locs if u != SITE + "/" and u.endswith("/")],
    "set_matches_expected": sorted(set(locs)) == sorted(route_to_url(p["route"]) for p in pages),
    "missing": sorted(set(route_to_url(p["route"]) for p in pages) - set(locs)),
    "extra": sorted(set(locs) - set(route_to_url(p["route"]) for p in pages)),
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
    add("P1", "sitemap", "-", f"sitemap set mismatch missing={sm['missing']} extra={sm['extra']}")
sm_statuses = {}
for loc in locs:
    path = loc[len(SITE):] or "/"
    sm_statuses[loc] = http_status(BASE_HTTP + path)
sm["loc_http_statuses"] = sm_statuses
sm["loc_non_200"] = {u: s for u, s in sm_statuses.items() if s != 200}
if sm["loc_non_200"]:
    add("P1", "sitemap", "-", f"locs not returning 200 via server: {sm['loc_non_200']}")

# ---- 3. llms.txt ----
llms_raw = (OUT / "llms.txt").read_text()
llms_urls = [l.strip() for l in llms_raw.splitlines() if l.strip().startswith("http")]
llms = {
    "served_status": http_status(BASE_HTTP + "/llms.txt"),
    "url_count": len(llms_urls),
    "set_matches_expected": sorted(set(llms_urls)) == sorted(route_to_url(p["route"]) for p in pages),
    "missing": sorted(set(route_to_url(p["route"]) for p in pages) - set(llms_urls)),
    "extra": sorted(set(llms_urls) - set(route_to_url(p["route"]) for p in pages)),
    "all_on_pages_url": all(u.startswith(SITE) for u in llms_urls),
}
if llms["missing"] or llms["extra"]:
    add("P1", "llms", "-", f"llms.txt missing={llms['missing']} extra={llms['extra']}")
if llms["url_count"] != 31:
    add("P1", "llms", "-", f"llms.txt lists {llms['url_count']} URLs, expected 31")

# ---- 4. 404.html ----
f404 = OUT / "404.html"
h404 = f404.read_text()
noindex_tags_404 = re.findall(r'<meta[^>]*name=["\']robots["\'][^>]*>', h404, re.I)
noindex_404 = [t for t in noindex_tags_404 if "noindex" in t.lower()]
f404_rec = {
    "exists": f404.exists(),
    "served_status": http_status(BASE_HTTP + "/this-page-does-not-exist-xyz"),
    "robots_meta_tags": noindex_tags_404,
    "noindex_tag_count": len(noindex_404),
    "has_canonical": bool(re.search(r'rel=["\']canonical["\']', h404, re.I)),
}
if len(noindex_404) != 1:
    add("P2" if len(noindex_404) > 1 else "P1", "404-noindex", "/404",
        f"404.html carries {len(noindex_404)} noindex meta tags, expected exactly 1: {noindex_tags_404}")

# ---- 5. localhost / double-slash scans over out/ HTML+XML+TXT ----
localhost_hits = []
doubleslash_hits = []
for p in sorted(OUT.rglob("*")):
    if p.is_file() and p.suffix.lower() in (".html", ".xml", ".txt"):
        t = p.read_text(errors="ignore")
        for m in re.finditer(r"localhost", t):
            localhost_hits.append({"file": str(p.relative_to(OUT)), "pos": m.start(),
                                   "context": t[max(0, m.start()-60):m.start()+60]})
        for m in re.finditer(r'https?://growthaura\.github\.io//', t):
            doubleslash_hits.append({"file": str(p.relative_to(OUT)), "pos": m.start()})
        for m in re.finditer(r'"//midvale-water-damage/', t):
            doubleslash_hits.append({"file": str(p.relative_to(OUT)), "pos": m.start(),
                                     "note": "protocol-relative double-slash prefix"})
scans = {"localhost_occurrences": len(localhost_hits), "localhost_hits": localhost_hits,
         "doubleslash_occurrences": len(doubleslash_hits), "doubleslash_hits": doubleslash_hits}
if localhost_hits:
    # allow the known Next.js URL-parser polyfill string only
    real = [h for h in localhost_hits if "localhost\"===s.host" not in h["context"]
            and '"localhost"===s.host' not in h["context"]]
    if real:
        add("P1", "localhost-leak", "-", f"{len(real)} localhost occurrences outside the known polyfill chunk: {real[:5]}")
    scans["localhost_non_polyfill"] = len(real)
if doubleslash_hits:
    add("P1", "double-slash", "-", f"{len(doubleslash_hits)} double-slash absolute URLs: {doubleslash_hits[:5]}")

# ---- per-page ----
title_counter, desc_counter, canon_counter = Counter(), Counter(), Counter()
all_resources = {}
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

    # meta robots — exactly 1, index,follow
    robots_metas = re.findall(r'<meta[^>]*name=["\']robots["\'][^>]*>', h, re.I)
    rec["meta_robots_tag_count"] = len(robots_metas)
    rec["meta_robots_tags"] = robots_metas
    contents = []
    for tag in robots_metas:
        m = re.search(r'content=["\']([^"\']*)["\']', tag, re.I)
        contents.append(m.group(1).lower().replace(" ", "") if m else "")
    rec["meta_robots_contents"] = contents
    if len(robots_metas) != 1 or contents != ["index,follow"]:
        add("P1", "indexability", route,
            f"meta robots tags={len(robots_metas)} contents={contents}, expected exactly 1 'index, follow'")

    # viewport
    rec["viewport_present"] = bool(re.search(
        r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\']width=device-width', h, re.I))

    # canonical
    canons = re.findall(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', h, re.I)
    if not canons:
        canons = re.findall(r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', h, re.I)
    rec["canonical_tags"] = canons
    expected_canon = route_to_url(route)
    rec["canonical_expected"] = expected_canon
    rec["canonical_self_referential"] = (len(canons) == 1 and canons[0] == expected_canon)
    if len(canons) != 1:
        add("P1", "canonical", route, f"{len(canons)} canonical tags, expected exactly 1: {canons}")
    elif canons[0] != expected_canon:
        add("P1", "canonical", route, f"canonical not self-referential: actual {canons[0]} expected {expected_canon}")
    else:
        canon_counter[canons[0]] += 1

    # og:url
    ogs = re.findall(r'<meta[^>]*property=["\']og:url["\'][^>]*content=["\']([^"\']+)["\']', h, re.I)
    if not ogs:
        ogs = re.findall(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:url["\']', h, re.I)
    rec["og_url"] = ogs
    rec["og_url_matches_canonical"] = (len(ogs) == 1 and ogs[0] == expected_canon)
    if len(ogs) != 1 or ogs[0] != expected_canon:
        add("P2", "og-url", route, f"og:url {ogs}, expected exactly [{expected_canon}]")

    # title / description verbatim
    tm = re.search(r"<title>(.*?)</title>", h, re.S)
    actual_title = html.unescape(tm.group(1)).strip() if tm else None
    dm = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content="([^"]*)"', h, re.I)
    if not dm:
        dm = re.search(r'<meta[^>]*content="([^"]*)"[^>]*name=["\']description["\']', h, re.I)
    actual_desc = html.unescape(dm.group(1)) if dm else None
    rec["title_expected"] = pg["metaTitle"]
    rec["title_actual"] = actual_title
    rec["title_len"] = len(actual_title) if actual_title is not None else None
    rec["title_verbatim_match"] = actual_title == pg["metaTitle"]
    rec["desc_expected"] = pg["metaDescription"]
    rec["desc_actual"] = actual_desc
    rec["desc_len"] = len(actual_desc) if actual_desc is not None else None
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
    # title/desc length observations (not defects per se — verbatim wins)
    rec["title_len_chars"] = len(pg["metaTitle"])
    rec["desc_len_chars"] = len(pg["metaDescription"])

    # headings
    heads = [(int(m.group(1)), strip_tags(m.group(2))) for m in
             re.finditer(r"<h([1-6])[^>]*>(.*?)</h\1>", h, re.S | re.I)]
    heads = [(lvl, t) for lvl, t in heads if t]
    rec["heading_count"] = len(heads)
    h1s = [t for lvl, t in heads if lvl == 1]
    rec["h1_count"] = len(h1s)
    rec["h1_text"] = h1s[0] if h1s else None
    rec["h1_expected"] = pg["h1"]
    rec["h1_match"] = len(h1s) == 1 and h1s[0] == pg["h1"]
    if len(h1s) != 1:
        add("P1", "headings-h1", route, f"H1 count {len(h1s)}, expected 1: {h1s}")
    elif h1s[0] != pg["h1"]:
        add("P1", "headings-h1", route, f"H1 text mismatch — expected {pg['h1']!r} actual {h1s[0]!r}")
    skips = []
    prev = 0
    for lvl, t in heads:
        if prev and lvl > prev + 1:
            skips.append(f"H{prev} -> H{lvl} at {t[:60]!r}")
        prev = lvl
    rec["hierarchy_skips"] = skips
    if skips:
        add("P2", "headings-hierarchy", route, f"skipped heading levels: {skips}")
    expected_h2 = [b["text"] for b in pg["blocks"] if b["type"] == "h2"]
    expected_h3 = [b["text"] for b in pg["blocks"] if b["type"] == "h3"]
    actual_h2 = [t for lvl, t in heads if lvl == 2]
    actual_h3 = [t for lvl, t in heads if lvl == 3]
    rec["h2_expected_count"] = len(expected_h2)
    rec["h2_actual_count"] = len(actual_h2)
    rec["h3_expected_count"] = len(expected_h3)
    rec["h3_actual_count"] = len(actual_h3)
    h2_mismatch = [f"#{i} expected {e!r} actual {a!r}" for i, (e, a) in enumerate(zip(expected_h2, actual_h2)) if e != a]
    h3_mismatch = [f"#{i} expected {e!r} actual {a!r}" for i, (e, a) in enumerate(zip(expected_h3, actual_h3)) if e != a]
    if len(expected_h2) != len(actual_h2):
        h2_mismatch.append(f"count: expected {len(expected_h2)} actual {len(actual_h2)}")
    if len(expected_h3) != len(actual_h3):
        h3_mismatch.append(f"count: expected {len(expected_h3)} actual {len(actual_h3)}")
    rec["h2_mismatches"] = h2_mismatch
    rec["h3_mismatches"] = h3_mismatch
    if h2_mismatch:
        add("P1", "headings-h2", route, f"H2 mismatches vs doc: {h2_mismatch}")
    if h3_mismatch:
        add("P1", "headings-h3", route, f"H3 mismatches vs doc: {h3_mismatch}")
    rec["h4_plus"] = [t for lvl, t in heads if lvl >= 4]

    # JSON-LD presence + parse (depth is the schema worker's job)
    ld_blocks = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', h, re.S | re.I)
    rec["jsonld_block_count"] = len(ld_blocks)
    parsed = []
    parse_failures = []
    for i, b in enumerate(ld_blocks):
        try:
            parsed.append(json.loads(b))
        except Exception as e:
            parse_failures.append({"block": i, "error": str(e)})
    rec["jsonld_parse_failures"] = parse_failures
    rec["jsonld_types"] = [p.get("@type") if isinstance(p, dict) else type(p).__name__ for p in parsed]
    if parse_failures:
        add("P1", "schema-parse", route, f"{len(parse_failures)} JSON-LD blocks fail to parse: {parse_failures}")
    if len(ld_blocks) == 0:
        add("P2", "schema-presence", route, "no JSON-LD blocks on page")

    # maps iframes lazy
    iframes = re.findall(r"<iframe[^>]*>", h, re.I)
    rec["iframe_count"] = len(iframes)
    rec["iframes_without_lazy"] = [t for t in iframes if "loading" not in t.lower()]
    if rec["iframes_without_lazy"]:
        add("P2", "maps-lazy", route, f"{len(rec['iframes_without_lazy'])} iframe(s) without loading=lazy")

    # local resource refs (css/js/img) — fetch via server
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
    refs = {u for u in refs if not u.startswith(("http://", "https://", "//", "mailto:", "tel:", "#", "data:"))}
    rec["local_refs_count"] = len(refs)
    fails = {}
    for u in refs:
        check_url = BASE_SERVER + u if u.startswith("/") else BASE_HTTP + "/" + u
        st = http_status(check_url)
        all_resources[check_url] = st
        if st != 200:
            fails[u] = st
    rec["resource_failures"] = fails
    if fails:
        add("P1", "resources", route, f"non-200 local resources: {fails}")
    per_page[route] = rec

dup_titles = {t: c for t, c in title_counter.items() if c > 1}
dup_descs = {t: c for t, c in desc_counter.items() if c > 1}
dup_canons = {t: c for t, c in canon_counter.items() if c > 1}
if dup_titles:
    add("P1", "meta-duplicates", "-", f"duplicate titles: {dup_titles}")
if dup_descs:
    add("P1", "meta-duplicates", "-", f"duplicate descriptions: {dup_descs}")
if dup_canons:
    add("P1", "canonical-duplicates", "-", f"duplicate canonical URLs: {dup_canons}")

report = {
    "audit": "CYCLE 1 OPT — static technical SEO audit (crawl/index/meta/headings/schema-presence)",
    "site": "Midvale UT water damage",
    "date": "2026-11-13",
    "server": BASE_HTTP + "/ (port 8325, qa/linkfix-serve.py copy in /tmp)",
    "export_note": "Fresh export run by coordinator before this audit (exit 0, NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage, no trailing slash). This script did NOT rebuild.",
    "data_source": "lib/pages-data.json",
    "data_sha256": sha,
    "data_sha256_expected": EXPECTED_SHA,
    "data_sha256_match": data_ok,
    "routes_expected": 31,
    "robots": robots,
    "sitemap": sm,
    "llms": llms,
    "page_404": f404_rec,
    "scans": scans,
    "resource_summary": {
        "total_distinct_local_refs_checked": len(all_resources),
        "non_200": {u: s for u, s in all_resources.items() if s != 200},
    },
    "duplicate_titles": dup_titles,
    "duplicate_descriptions": dup_descs,
    "duplicate_canonicals": dup_canons,
    "jsonld_total_blocks": sum(p.get("jsonld_block_count", 0) for p in per_page.values()),
    "jsonld_total_parse_failures": sum(len(p.get("jsonld_parse_failures", [])) for p in per_page.values()),
    "per_page": per_page,
    "problems": problems,
    "problem_counts": {
        "P1": sum(1 for p in problems if p["severity"] == "P1"),
        "P2": sum(1 for p in problems if p["severity"] == "P2"),
        "P3": sum(1 for p in problems if p["severity"] == "P3"),
        "total": len(problems),
    },
}
(ROOT / "qa/opt1-static.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
print("PROBLEMS:", report["problem_counts"])
for p in problems:
    print(p["severity"], "|", p["check"], "|", p["page"], "|", p["detail"][:400])
print("jsonld blocks:", report["jsonld_total_blocks"], "parse failures:", report["jsonld_total_parse_failures"])
print("distinct resources:", len(all_resources), "non-200:", report["resource_summary"]["non_200"])
print("localhost:", scans["localhost_occurrences"], "doubleslash:", scans["doubleslash_occurrences"])
