#!/usr/bin/env python3
"""SEO AUDIT 2 W2 — structured data / schema — Midvale UT.
Fresh measurement on the re-exported out/ (NEXT_PUBLIC_SITE_URL=
https://growthaura.github.io/midvale-water-damage), served at
http://127.0.0.1:8342/midvale-water-damage/.
Reads lib/pages-data.json (source of truth) + out/ HTML directly.
Writes qa/seo-audit2-w2.json. AUDIT ONLY — no site files modified.
"""
import json, re, html, hashlib, urllib.request, urllib.error
from collections import Counter
from pathlib import Path

ROOT = Path.home() / "workspace/midvale-water-damage"
OUT = ROOT / "out"
BASE_HTTP = "http://127.0.0.1:8342/midvale-water-damage"
BASE_ABS = "https://growthaura.github.io/midvale-water-damage"
EXPECTED_SHA = "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f"

problems = []
def add(sev, check, page, detail, evidence=""):
    problems.append({"severity": sev, "check": check, "page": page,
                     "detail": detail, "evidence": evidence})

sha_start = hashlib.sha256((ROOT / "lib/pages-data.json").read_bytes()).hexdigest()
if sha_start != EXPECTED_SHA:
    add("P1", "data-integrity", "-", f"pages-data.json sha256 {sha_start} != expected {EXPECTED_SHA}")
    print("DATA SHA MISMATCH — STOP")
    raise SystemExit(1)
data = json.loads((ROOT / "lib/pages-data.json").read_text())
pages = data["pages"]
assert len(pages) == 31, f"expected 31 pages in data, got {len(pages)}"
by_route = {p["route"]: p for p in pages}

def route_to_file(route):
    if route == "/":
        return OUT / "index.html"
    return OUT / (route.strip("/") + ".html")

def route_to_served(route):
    if route == "/":
        return BASE_HTTP + "/"
    return BASE_HTTP + route.rstrip("/")

def http_get(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return f"ERR:{e}", ""

def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))

def norm(s):
    return re.sub(r"\s+", " ", strip_tags(s)).strip()

def norm_link_annotations(s):
    """Data answers may carry a link annotation 'Anchor (/path/)'; the visible
    page renders it as an anchor whose stripped text is just 'Anchor', and the
    schema carries the same plain text. Strip only parentheticals holding a
    /-led path so the comparison is against rendered text, not raw annotation."""
    return re.sub(r"\s*\([^)]*/[^)]*\)", "", s)

def collect_keys(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.append(k)
            collect_keys(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_keys(v, out)

def collect_urls(obj, out, _key=None):
    if isinstance(obj, dict):
        for k, v in obj.items():
            collect_urls(v, out, _key=k)
    elif isinstance(obj, list):
        for v in obj:
            collect_urls(v, out, _key=_key)
    elif isinstance(obj, str) and re.match(r"https?://", obj):
        # @context is the schema.org vocabulary URI, not a site URL
        if _key != "@context":
            out.append(obj)

FORBIDDEN_KEYS = ["aggregateRating", "ratingValue", "reviewCount", "foundingDate",
                  "priceRange", "price", "streetAddress", "hasCredential", "award", "sameAs"]

per_page = {}
tot_faq_data = tot_faq_schema = tot_faq_visible = 0
total_blocks = total_invalid = 0
type_counts = Counter()
localhost_pages = []
non_pages_urls = []   # absolute URLs in JSON-LD not on the Pages base
http_plain_urls = []  # http:// (non-https) URLs in JSON-LD
all_telephones = set()
all_area_cities = set()
all_area_zips = set()

# data-side 24/7 trace
data_text_247 = sum(json.dumps(p).count("24/7") for p in pages)

for p in pages:
    route = p["route"]
    f = route_to_file(route)
    raw = f.read_text()
    status, served = http_get(route_to_served(route))
    entry = {"route": route, "file": str(f.relative_to(OUT)), "http": status,
             "served_equals_disk": (served == raw) if isinstance(status, int) else False}
    # ---- H1 / canonical ----
    h1m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    entry["h1"] = norm(h1m.group(1)) if h1m else None
    entry["h1_matches_data"] = (entry["h1"] == p["h1"])
    cm = re.search(r'<link rel="canonical" href="([^"]+)"', raw)
    entry["canonical"] = cm.group(1) if cm else None
    # ---- JSON-LD blocks ----
    blocks_raw = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)
    entry["json_ld_blocks"] = len(blocks_raw)
    total_blocks += len(blocks_raw)
    entry["json_ld_invalid"] = 0
    entry["json_ld_invalid_detail"] = []
    entry["localhost_in_schema"] = sum(b.count("localhost") for b in blocks_raw)
    if entry["localhost_in_schema"]:
        localhost_pages.append({"page": route, "count": entry["localhost_in_schema"]})
    parsed = []
    for i, b in enumerate(blocks_raw):
        try:
            parsed.append(json.loads(b))
        except Exception as e:
            entry["json_ld_invalid"] += 1
            total_invalid += 1
            entry["json_ld_invalid_detail"].append({"block": i, "error": str(e), "raw_head": b[:200]})
    types = []
    for obj in parsed:
        t = obj.get("@type")
        types.append(t)
        type_counts[t] += 1
    entry["types"] = types
    # forbidden keys + urls
    keys = []
    urls = []
    for obj in parsed:
        collect_keys(obj, keys)
        collect_urls(obj, urls)
    entry["suspicious_schema_keys"] = sorted(set(k for k in keys if k in FORBIDDEN_KEYS))
    entry["schema_absolute_urls"] = urls
    for u in urls:
        if not u.startswith(BASE_ABS):
            non_pages_urls.append({"page": route, "url": u})
        if u.startswith("http://"):
            http_plain_urls.append({"page": route, "url": u})
    # ---- FAQ ----
    faq_data = [(q["q"], q["a"]) for q in p.get("faqs", [])]
    entry["faq_data"] = len(faq_data)
    tot_faq_data += len(faq_data)
    faq_schema = []
    for obj in parsed:
        if obj.get("@type") == "FAQPage":
            for q in obj.get("mainEntity", []):
                faq_schema.append((q.get("name", ""),
                                   q.get("acceptedAnswer", {}).get("text", "")))
    entry["faq_schema"] = len(faq_schema)
    tot_faq_schema += len(faq_schema)
    # visible FAQ: <section id="faq"> .faq-item h3 + p
    faq_visible = []
    fm = re.search(r'<section[^>]*id="faq"[^>]*>(.*?)</section>', raw, re.S)
    if fm:
        for item in re.findall(r'<div class="faq-item">(.*?)</div>', fm.group(1), re.S):
            qm = re.search(r"<h3[^>]*>(.*?)</h3>", item, re.S)
            am = re.search(r"<p[^>]*>(.*?)</p>", item, re.S)
            if qm and am:
                faq_visible.append((norm(qm.group(1)), norm(am.group(1))))
    entry["faq_visible"] = len(faq_visible)
    tot_faq_visible += len(faq_visible)
    entry["faq_visible_section_present"] = fm is not None
    # comparisons (exact after strip/unescape/collapse)
    def pairs_exact(a_list, b_list):
        return len(a_list) == len(b_list) and all(
            norm(x[0]) == norm(y[0]) and norm(x[1]) == norm(y[1])
            for x, y in zip(a_list, b_list))
    sv_exact = pairs_exact(faq_schema, faq_visible)
    sd_raw = pairs_exact(faq_schema, faq_data)
    sd_norm = pairs_exact(
        faq_schema,
        [(q, norm_link_annotations(a)) for q, a in faq_data])
    vd_norm = pairs_exact(
        faq_visible,
        [(q, norm_link_annotations(a)) for q, a in faq_data])
    if not faq_data and not faq_schema and not faq_visible:
        entry["faq_schema_vs_visible"] = "n/a (no FAQ anywhere)"
        entry["faq_schema_vs_data"] = "n/a"
        entry["faq_visible_vs_data"] = "n/a"
    else:
        entry["faq_schema_vs_visible"] = "EXACT MATCH" if sv_exact else "MISMATCH"
        entry["faq_schema_vs_data"] = ("EXACT MATCH" if sd_raw else
            ("EXACT MATCH after link-annotation normalisation" if sd_norm else "MISMATCH"))
        entry["faq_visible_vs_data"] = ("EXACT MATCH" if pairs_exact(faq_visible, faq_data) else
            ("EXACT MATCH after link-annotation normalisation" if vd_norm else "MISMATCH"))
        if entry["faq_schema_vs_visible"] != "EXACT MATCH":
            entry["faq_schema_vs_visible_diff"] = [
                {"i": i, "schema": s, "visible": v}
                for i, (s, v) in enumerate(zip(faq_schema, faq_visible))
                if norm(s[0]) != norm(v[0]) or norm(s[1]) != norm(v[1])]
        if entry["faq_schema_vs_data"] == "MISMATCH":
            entry["faq_schema_vs_data_diff"] = [
                {"i": i, "schema": s, "data": d}
                for i, (s, d) in enumerate(zip(faq_schema, faq_data))
                if norm(s[0]) != norm(d[0]) or norm(s[1]) != norm(d[1])]
        if entry["faq_schema_vs_data"].startswith("EXACT MATCH after"):
            entry["faq_schema_vs_data_annotation_note"] = [
                {"i": i, "schema_answer": s[1], "data_answer_raw": d[1]}
                for i, (s, d) in enumerate(zip(faq_schema, faq_data))
                if norm(s[1]) != norm(d[1])]
    # ---- Breadcrumb ----
    bc_schema = []
    for obj in parsed:
        if obj.get("@type") == "BreadcrumbList":
            for el in obj.get("itemListElement", []):
                bc_schema.append({"position": el.get("position"),
                                  "name": el.get("name"),
                                  "item": el.get("item")})
    bc_schema.sort(key=lambda x: x["position"])
    entry["breadcrumb_schema"] = bc_schema
    entry["breadcrumb_positions_sequential"] = (
        [b["position"] for b in bc_schema] == list(range(1, len(bc_schema) + 1)))
    bm = re.search(r'<nav class="breadcrumb"[^>]*>(.*?)</nav>', raw, re.S)
    bc_vis = []
    if bm:
        for li in re.findall(r"<li>(.*?)</li>", bm.group(1), re.S):
            am = re.search(r'<a href="([^"]*)"[^>]*>(.*?)</a>', li, re.S)
            sm = re.search(r'<span[^>]*>(.*?)</span>', li, re.S)
            if am:
                bc_vis.append({"name": norm(am.group(2)), "href": am.group(1), "current": False})
            elif sm:
                bc_vis.append({"name": norm(sm.group(1)), "href": None, "current": True})
    entry["breadcrumb_visible"] = bc_vis
    entry["breadcrumb_visible_present"] = bm is not None
    entry["breadcrumb_names_match_visible"] = (
        [b["name"] for b in bc_schema] == [v["name"] for v in bc_vis]) if bc_vis else None
    # ---- Service ----
    svc = None
    for obj in parsed:
        if obj.get("@type") == "Service":
            svc = obj
    if svc is not None:
        prov = svc.get("provider", {}) or {}
        svc_area = svc.get("areaServed", {}) or {}
        entry["service"] = {
            "name": svc.get("name"),
            "serviceType": svc.get("serviceType"),
            "url": svc.get("url"),
            "name_equals_h1": svc.get("name") == entry["h1"],
            "serviceType_equals_h1": svc.get("serviceType") == entry["h1"],
            "areaServed": svc_area,
            "provider": {"@type": prov.get("@type"), "name": prov.get("name"),
                         "telephone": prov.get("telephone"), "url": prov.get("url")},
        }
        if prov.get("telephone"):
            all_telephones.add(prov["telephone"])
        if isinstance(svc_area, dict):
            all_area_cities.add(svc_area.get("name"))
            all_area_zips.add(svc_area.get("postalCode"))
    else:
        entry["service"] = None
    # ---- LocalBusiness standalone ----
    lb = None
    for obj in parsed:
        if obj.get("@type") == "HomeAndConstructionBusiness":
            lb = obj
    if lb is not None:
        entry["localbusiness"] = {
            "type": lb.get("@type"), "name": lb.get("name"),
            "telephone": lb.get("telephone"), "url": lb.get("url"),
            "areaServed": lb.get("areaServed"),
            "openingHours": lb.get("openingHours"),
            "address": lb.get("address"),
        }
        if lb.get("telephone"):
            all_telephones.add(lb["telephone"])
        for c in (lb.get("areaServed") or []):
            if isinstance(c, dict):
                all_area_cities.add(c.get("name"))
                all_area_zips.add(c.get("postalCode"))
    else:
        entry["localbusiness"] = None
    per_page[route] = entry

# ---- aggregate checks / problems ----
service_pages = [r for r, e in per_page.items() if e["service"] is not None]
if total_invalid:
    add("P1", "schema-invalid-json", "site-wide",
        f"{total_invalid} invalid JSON-LD block(s) of {total_blocks}",
        json.dumps([e for e in per_page.values() if e["json_ld_invalid"]], default=str)[:1000])
if len(service_pages) != 19:
    add("P1", "service-count", "site-wide",
        f"Service schema on {len(service_pages)} pages, expected exactly 19: {sorted(service_pages)}")
for r, e in per_page.items():
    if e["service"] is not None and not e["service"]["name_equals_h1"]:
        add("P1", "service-name-not-h1", r,
            f"Service name {e['service']['name']!r} != H1 {e['h1']!r}")
    if e["faq_data"] and e["faq_schema_vs_visible"] != "EXACT MATCH":
        add("P1", "faq-schema-vs-visible", r, e["faq_schema_vs_visible"],
            json.dumps(e.get("faq_schema_vs_visible_diff", []))[:2000])
    if e["faq_data"] and e["faq_schema_vs_data"] == "MISMATCH":
        add("P1", "faq-schema-vs-data", r, "schema FAQ != data FAQ",
            json.dumps(e.get("faq_schema_vs_data_diff", []))[:2000])
    if e["faq_data"] and e["faq_visible_vs_data"] == "MISMATCH":
        add("P1", "faq-visible-vs-data", r, "visible FAQ != data FAQ")
    if e["breadcrumb_schema"] and not e["breadcrumb_positions_sequential"]:
        add("P1", "breadcrumb-positions", r,
            f"positions not 1..n sequential: {[b['position'] for b in e['breadcrumb_schema']]}")
    if e["breadcrumb_visible"] and e["breadcrumb_names_match_visible"] is False:
        add("P1", "breadcrumb-name-mismatch", r,
            f"schema {[b['name'] for b in e['breadcrumb_schema']]} vs visible {[v['name'] for v in e['breadcrumb_visible']]}")
    if e["suspicious_schema_keys"]:
        add("P1", "schema-invented-fact-keys", r,
            f"forbidden keys present: {e['suspicious_schema_keys']}")
    if e["localhost_in_schema"]:
        add("P1", "schema-localhost-url", r,
            f"{e['localhost_in_schema']} 'localhost' occurrence(s) inside JSON-LD")
    if e["http"] != 200:
        add("P2", "http-not-200", r, f"served HTTP {e['http']}")
    if not e["served_equals_disk"]:
        add("P2", "served-differs-disk", r, "served HTML != out/ HTML on disk")
    if not e["h1_matches_data"]:
        add("P1", "h1-vs-data", r, f"H1 {e['h1']!r} != data H1 {by_route[r]['h1']!r}")

# P3-4 re-check: schema Home item URL vs canonical (homepage)
home = per_page["/"]
home_bc = home["breadcrumb_schema"][0] if home["breadcrumb_schema"] else {}
p34 = {"schema_home_item": home_bc.get("item"),
       "canonical_homepage": home["canonical"],
       "match": home_bc.get("item") == home["canonical"],
       "visible_home_href": (home["breadcrumb_visible"][0]["href"]
                             if home["breadcrumb_visible"] else None),
       "homepage_visible_breadcrumb_present": home["breadcrumb_visible_present"]}
if not p34["match"]:
    add("P3", "breadcrumb-home-url-vs-canonical", "/",
        f"schema Home item {p34['schema_home_item']!r} != canonical {p34['canonical_homepage']!r}",
        json.dumps(p34))
# P3-3: homepage visible breadcrumb?
if not home["breadcrumb_visible_present"]:
    add("P3", "breadcrumb-no-visible", "/",
        "BreadcrumbList schema present but no visible breadcrumb nav found (homepage only; single-item Home breadcrumb)")
# location serviceType re-check (P3-2)
loc_service_types = {}
for r in ["/locations/cottonwood-heights-ut", "/locations/south-salt-lake-ut", "/locations/magna-ut"]:
    e = per_page[r]
    loc_service_types[r] = {"serviceType": e["service"]["serviceType"],
                            "h1": e["h1"],
                            "equals_h1": e["service"]["serviceType_equals_h1"]}
    if not e["service"]["serviceType_equals_h1"]:
        add("P3", "service-type-generic", r,
            f"serviceType {e['service']['serviceType']!r} != page H1 {e['h1']!r}")
# non-Pages URLs in schema
if non_pages_urls:
    add("P1", "schema-url-off-base", "site-wide",
        f"{len(non_pages_urls)} absolute URL(s) in JSON-LD not on {BASE_ABS}",
        json.dumps(non_pages_urls)[:2000])
if http_plain_urls:
    add("P2", "schema-url-http-not-https", "site-wide",
        f"{len(http_plain_urls)} http:// (non-https) URL(s) in JSON-LD",
        json.dumps(http_plain_urls)[:2000])

sha_end = hashlib.sha256((ROOT / "lib/pages-data.json").read_bytes()).hexdigest()

result = {
    "audit": "seo-audit2-w2 structured data / schema",
    "site": "Midvale UT",
    "data_path": "lib/pages-data.json (task named data/lib/pages-data.json; no such path exists — actual file is lib/pages-data.json)",
    "data_sha256_start": sha_start,
    "data_sha256_end": sha_end,
    "data_sha256_expected": EXPECTED_SHA,
    "data_sha256_match_start_and_end": sha_start == EXPECTED_SHA == sha_end,
    "served_from": BASE_HTTP,
    "export_base_url": BASE_ABS,
    "routes_audited": len(per_page),
    "totals": {
        "json_ld_blocks": total_blocks,
        "json_ld_invalid": total_invalid,
        "faq_data": tot_faq_data,
        "faq_schema": tot_faq_schema,
        "faq_visible": tot_faq_visible,
        "faq_pages_with_faqs": sum(1 for e in per_page.values() if e["faq_data"] > 0),
        "schema_type_counts": dict(type_counts),
        "pages_with_service": len(service_pages),
        "service_pages": sorted(service_pages),
        "pages_with_breadcrumb": sum(1 for e in per_page.values() if e["breadcrumb_schema"]),
        "pages_with_localhost_in_schema": len(localhost_pages),
        "localhost_occurrences_in_schema_total": sum(p["count"] for p in localhost_pages),
        "telephones_in_schema": sorted(all_telephones),
        "areaserved_cities": sorted(c for c in all_area_cities if c),
        "areaserved_postalCodes": sorted(z for z in all_area_zips if z),
        "absolute_urls_in_schema_not_on_pages_base": len(non_pages_urls),
        "http_plain_urls_in_schema": len(http_plain_urls),
        "data_247_occurrences": data_text_247,
    },
    "p3_4_recheck": p34,
    "location_service_types": loc_service_types,
    "homepage_localbusiness": home["localbusiness"],
    "localhost_pages": localhost_pages,
    "non_pages_urls": non_pages_urls,
    "http_plain_urls": http_plain_urls,
    "per_page": per_page,
    "problems": problems,
}
out_path = ROOT / "qa/seo-audit2-w2.json"
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
print(f"blocks={total_blocks} invalid={total_invalid} faq data/schema/visible={tot_faq_data}/{tot_faq_schema}/{tot_faq_visible}")
print(f"types={dict(type_counts)} service_pages={len(service_pages)}")
print(f"localhost_pages={len(localhost_pages)} non_pages_urls={len(non_pages_urls)} http_plain={len(http_plain_urls)}")
print(f"problems={len(problems)}")
for pr in problems:
    print(" ", pr["severity"], pr["check"], pr["page"], "-", pr["detail"][:160])
print("sha_end_match:", sha_end == EXPECTED_SHA)
print("wrote", out_path)
