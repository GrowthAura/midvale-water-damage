#!/usr/bin/env python3
"""INDEPENDENT SCHEMA VERIFIER — Midvale UT, Stage 4 (2026-11-13).
Fresh, independent re-measurement of the schema implementation.
Reads ONLY out/ + lib/pages-data.json + lib/content.ts (for hero alts / footer map).
Writes JSON + human-readable summary to qa/verify-schema-2026-11-13.json.
Does NOT modify any site source file.

RE-VERIFY EDITS (2026-11-13, after FIX 1 + FIX 2):
- City allowlist: postalCode REMOVED (its schema.org domain is PostalAddress
  only); City gains `address`. New PostalAddress allowlist entry
  (addressRegion/postalCode et al.). The old postalCode-on-City UNVERIFIED
  block is replaced by a strict PostalAddress-shape check: every postalCode
  must sit inside a PostalAddress node, every City address must BE a
  PostalAddress with addressRegion + postalCode (counted in
  results["postal_address_nodes"]).
- areaServed honest extractor reads postalCode from inside `address`
  (was top-level a.get("postalCode")); new Service areaServed check
  (16 service pages -> Midvale/84047; 3 location pages -> their LOCATIONS
  city/ZIP from lib/content.ts).
"""
import json, re, sys, html as htmlmod
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path.home() / "workspace" / "midvale-water-damage"
OUT = ROOT / "out"
BASE = "https://growthaura.github.io/midvale-water-damage"
DATA = json.loads((ROOT / "lib" / "pages-data.json").read_text())
PAGES = {p["route"]: p for p in DATA["pages"]}

from bs4 import BeautifulSoup

def norm_ws(s):
    return re.sub(r"\s+", " ", (s or "").strip())

def strip_annotations(text):
    """Mirror lib/links.tsx stripAnnotations: remove ` (/path/)` (+1 space),
    \u2028 -> -, em dash -> - ."""
    out = re.sub(r" \(/[^)]*\)", "", text)
    out = out.replace("\u2028", "-").replace("\u2014", "-")
    return out

def words(s):
    s = norm_ws(s).lower()
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("\u2019", "'")
    toks = re.findall(r"[a-z0-9][a-z0-9'’\-/]*", s)
    # drop annotation-path tokens and bare slashes
    return [t for t in toks if "/" not in t]

# ---------- route discovery ----------
html_files = sorted(OUT.rglob("*.html"))
routes = {}
for f in html_files:
    rel = f.relative_to(OUT).as_posix()
    if rel == "index.html":
        route = "/"
    elif rel == "404.html":
        route = "/404"
    else:
        route = "/" + rel[:-5]  # strip .html
    routes[route] = f
assert len(routes) == 32, f"expected 32 html files (31 routes + 404), got {len(routes)}"
assert set(PAGES) == set(r for r in routes if r != "/404"), \
    f"route/data mismatch: {set(PAGES) ^ set(r for r in routes if r != '/404')}"

LD_RE = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)

results = {
    "routes": {}, "totals_by_type": Counter(), "total_blocks": 0,
    "parse_errors": [], "dup_ids": {}, "unresolved_refs": [],
    "cross_page_refs": [], "forbidden": {}, "url_problems": [],
    "prop_problems": [], "unverified_props": [], "postal_address_nodes": [],
    "honest": {}, "schema_visible": {}, "regression": {},
}
FORBIDDEN_KEYS = ["totalTime", "supply", "tool", "priceRange", "sameAs",
                  "reviews", "aggregateRating", "potentialAction", "SearchAction"]

# schema.org property allowlist (from schema.org knowledge).
# Properties I am NOT fully certain about go in UNVERIFIED, not in the allowlist.
ALLOW = {
    "WebPage": {"name", "description", "url", "inLanguage", "isPartOf",
                "breadcrumb", "primaryImageOfPage", "speakable"},
    "ImageObject": {"contentUrl", "caption", "representativeOfPage"},
    "HowTo": {"name", "step"},
    "HowToStep": {"name", "text", "url", "image"},
    "FAQPage": {"mainEntity"},
    "Question": {"name", "acceptedAnswer"},
    "Answer": {"text"},
    "BreadcrumbList": {"itemListElement"},
    "ListItem": {"position", "name", "item"},
    "Service": {"name", "serviceType", "description", "image", "url",
                "areaServed", "provider"},
    "HomeAndConstructionBusiness": {"name", "description", "telephone", "url",
                "hasMap", "areaServed", "openingHours"},
    "WebSite": {"name", "url", "publisher", "inLanguage"},
    "SpeakableSpecification": {"cssSelector", "xpath"},
    # City: `address` is a property of Place (City is a Place subtype), and
    # addressRegion IS a valid Place property, so both stay allowed.
    # postalCode is NOT allowed directly on City: schema.org lists its
    # domain as PostalAddress only — it must live inside address.
    # RE-VERIFY EDIT 2026-11-13 (FIX 2): postalCode removed from City.
    "City": {"name", "address", "addressRegion"},
    # RE-VERIFY EDIT 2026-11-13 (FIX 2): new PostalAddress entry.
    # schema.org/PostalAddress properties (full standard set; our nodes
    # use addressRegion + postalCode).
    "PostalAddress": {"streetAddress", "addressLocality", "addressRegion",
                      "postalCode", "addressCountry", "postOfficeBoxNumber"},
}
# postalCode on City was flagged UNVERIFIED in the first verification
# (2026-11-13 ~11:30); FIX 2 wrapped it into PostalAddress, so the
# UNVERIFIED note is retired and replaced by the strict shape check below
# (every postalCode inside a PostalAddress; every City address a
# PostalAddress with addressRegion + postalCode).
REQUIRED = {
    "WebPage": ["name", "description", "url"],
    "ImageObject": ["contentUrl"],
    "HowTo": ["name", "step"],
    "HowToStep": ["text"],
    "FAQPage": ["mainEntity"],
    "Question": ["name", "acceptedAnswer"],
    "Answer": ["text"],
    "BreadcrumbList": ["itemListElement"],
    "ListItem": ["position", "name", "item"],
    "Service": ["name", "description"],
    "HomeAndConstructionBusiness": ["name"],
    "WebSite": ["name", "url"],
    "City": ["name"],
    "PostalAddress": ["addressRegion", "postalCode"],
}

def walk_nodes(node, path=""):
    """Yield (node_dict, path) for every dict with @type."""
    if isinstance(node, dict):
        if "@type" in node:
            yield node, path
        for k, v in node.items():
            yield from walk_nodes(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_nodes(v, f"{path}[{i}]")

def collect_ids_refs(block):
    """defs: @id values on nodes that have other props; refs: {'@id': x} only."""
    defs, refs = [], []
    def rec(n):
        if isinstance(n, dict):
            keys = set(n.keys())
            if "@id" in n:
                if keys <= {"@id"}:
                    refs.append(n["@id"])
                else:
                    defs.append(n["@id"])
            for v in n.values():
                rec(v)
        elif isinstance(n, list):
            for v in n:
                rec(v)
    rec(block)
    return defs, refs

# homepage-defined ids (for cross-page ref classification)
home_defs = set()

for route, f in sorted(routes.items()):
    raw = f.read_text()
    soup = BeautifulSoup(raw, "html.parser")
    blocks_raw = LD_RE.findall(raw)
    blocks = []
    for br in blocks_raw:
        try:
            blocks.append(json.loads(htmlmod.unescape(br.strip())))
        except Exception as e:
            results["parse_errors"].append({"route": route, "error": str(e),
                                           "snippet": br.strip()[:200]})
    entry = {"file": str(f.relative_to(OUT)), "n_blocks": len(blocks_raw),
             "types": Counter(), "nested_types": Counter(), "ids": [],
             "checks": []}
    results["total_blocks"] += len(blocks)
    for b in blocks:
        t = b.get("@type")
        entry["types"][t] += 1
        results["totals_by_type"][t] += 1
        for node, p in walk_nodes(b):
            nt = node.get("@type")
            if node is not b:
                entry["nested_types"][nt] += 1
        # property conformance (top-level + nested)
        for node, p in walk_nodes(b):
            nt = node.get("@type")
            if nt in ALLOW:
                props = set(node.keys()) - {"@context", "@type", "@id"}
                bad = props - ALLOW[nt]
                for prop in sorted(bad):
                    results["prop_problems"].append(
                        {"route": route, "type": nt, "path": p, "property": prop})
                for req in REQUIRED.get(nt, []):
                    if req not in node:
                        results["prop_problems"].append(
                            {"route": route, "type": nt, "path": p,
                             "property": f"MISSING required: {req}"})
            else:
                results["unverified_props"].append(
                    {"route": route, "type": nt, "path": p,
                     "note": f"no allowlist entry for @type {nt}"})
            # URL shape: every string value that looks like a URL
            for k, v in node.items():
                if isinstance(v, str) and v.startswith("http"):
                    if v.startswith("http://localhost") or "localhost" in v:
                        results["url_problems"].append(
                            {"route": route, "type": nt, "prop": k, "value": v,
                             "issue": "localhost URL"})
                    elif "//" in v.replace("https://", "").replace("http://", ""):
                        results["url_problems"].append(
                            {"route": route, "type": nt, "prop": k, "value": v,
                             "issue": "double-slash in URL"})
                    elif k in ("url", "contentUrl", "item") and not v.startswith(BASE) \
                            and not v.startswith("https://www.google.com/maps"):
                        results["url_problems"].append(
                            {"route": route, "type": nt, "prop": k, "value": v,
                             "issue": "URL not on Pages base"})
                    elif v.startswith(BASE):
                        # BASE already ends in /midvale-water-damage: the path
                        # after BASE must not repeat the subpath again.
                        rest = v[len(BASE):]
                        if rest.startswith("/midvale-water-damage"):
                            results["url_problems"].append(
                                {"route": route, "type": nt, "prop": k, "value": v,
                                 "issue": "DOUBLE subpath prefix after Pages base"})
        # forbidden keys inside this block (JSON keys only)
        for fk in FORBIDDEN_KEYS:
            if re.search(r'"' + fk + r'"\s*:', json.dumps(b)):
                results["forbidden"].setdefault(route, []).append(fk)
        # PostalAddress shape (RE-VERIFY EDIT 2026-11-13, FIX 2): replaces the
        # old postalCode-on-City UNVERIFIED note. schema.org reasoning:
        # `address` is a property of Place and City is a Place subtype, so
        # City.address is valid; `postalCode`'s domain is PostalAddress, so
        # it must live ONLY inside a PostalAddress node. Enforce both:
        # (a) any postalCode key on a non-PostalAddress node is a PROP
        # PROBLEM; (b) every City `address` must be a PostalAddress object
        # (its addressRegion/postalCode presence is enforced by REQUIRED
        # above). Count every PostalAddress node for the totals check.
        for node, p in walk_nodes(b):
            if "postalCode" in node and node.get("@type") != "PostalAddress":
                results["prop_problems"].append(
                    {"route": route, "type": node.get("@type"), "path": p,
                     "property": "postalCode outside PostalAddress"})
            if node.get("@type") == "PostalAddress":
                results["postal_address_nodes"].append(
                    {"route": route, "path": p,
                     "addressRegion": node.get("addressRegion"),
                     "postalCode": node.get("postalCode")})
            if node.get("@type") == "City":
                addr = node.get("address")
                if not isinstance(addr, dict) or addr.get("@type") != "PostalAddress":
                    results["prop_problems"].append(
                        {"route": route, "type": "City", "path": p,
                         "property": "address is not a PostalAddress object"})
        defs, refs = collect_ids_refs(b)
        entry["ids"].extend(defs)
        entry.setdefault("refs", []).extend(refs)
    # duplicate @ids on this page
    c = Counter(entry["ids"])
    dups = {k: v for k, v in c.items() if v > 1}
    if dups:
        results["dup_ids"][route] = dups
    if route == "/":
        home_defs = set(entry["ids"])
    results["routes"][route] = entry

# resolve refs (second pass — homepage defs known now)
for route, entry in results["routes"].items():
    own = set(entry["ids"])
    for ref in entry.get("refs", []):
        if ref in own:
            continue
        if ref in home_defs:
            results["cross_page_refs"].append(
                {"route": route, "ref": ref, "defined_on": "homepage"})
        else:
            results["unresolved_refs"].append({"route": route, "ref": ref})

# ---------- honest-only + schema==visible ----------
content_ts = (ROOT / "lib" / "content.ts").read_text()
# hero alts from content.ts HERO_IMAGE map
hero_alts = {k: a for k, s, a in re.findall(r"(\w+):\s*\{\s*src:\s*\"([^\"]+)\",\s*alt:\s*\"([^\"]+)\"", content_ts)}
# RE-VERIFY EDIT 2026-11-13 (FIX 2): location city/ZIP source for the
# Service areaServed check — LOCATIONS in lib/content.ts (slug -> city, zip).
locs = {slug: (city, zip) for slug, city, zip in
        re.findall(r'slug:\s*"([^"]+)",\s*city:\s*"([^"]+)",\s*zip:\s*"([^"]+)"', content_ts)}
# footer map query
m = re.search(r"google\.com/maps\?q=([^\"&]+)", (ROOT / "components" / "site.tsx").read_text())
footer_map_q = m.group(1) if m else None
# homepage FAQ + PROCESS from content.ts (raw TS parse, light-weight)
faq_home = None
proc_home = None
fm = re.search(r"export const FAQ[^=]*=\s*\[(.*?)\n\];", content_ts, re.S)
if fm:
    faq_home = re.findall(r'\{\s*q:\s*"((?:[^"\\]|\\.)*)",\s*a:\s*"((?:[^"\\]|\\.)*)"\s*,?\s*\}', fm.group(1), re.S)
    faq_home = [(a.replace('\\"', '"'), b.replace('\\"', '"')) for a, b in faq_home]
pm = re.search(r"export const PROCESS[^=]*=\s*\[(.*?)\n\];", content_ts, re.S)
if pm:
    proc_home = re.findall(r'\{\s*lead:\s*"((?:[^"\\]|\\.)*)",\s*rest:\s*"((?:[^"\\]|\\.)*)"\s*,?\s*\}', pm.group(1), re.S)
    proc_home = [(a.replace('\\"', '"'), b.replace('\\"', '"')) for a, b in proc_home]

honest = results["honest"]
honest["hero_alts_found"] = len(hero_alts)
honest["footer_map_query"] = footer_map_q
honest["home_faq_parsed"] = len(faq_home) if faq_home else 0
honest["home_process_parsed"] = len(proc_home) if proc_home else 0
honest["mismatches"] = []

def by_type(route, t):
    raw = (OUT / results["routes"][route]["file"]).read_text()
    out = []
    for br in LD_RE.findall(raw):
        try:
            b = json.loads(htmlmod.unescape(br.strip()))
        except Exception:
            continue
        if b.get("@type") == t:
            out.append(b)
    return out

def visible_text(soup):
    for tag in soup(["script", "style"]):
        tag.decompose()
    return norm_ws(soup.get_text(" "))

for route, page in PAGES.items():
    f = routes[route]
    raw = f.read_text()
    soup = BeautifulSoup(raw, "html.parser")
    # --- WebPage name/description vs data + rendered meta ---
    wp = by_type(route, "WebPage")
    title_tag = norm_ws(soup.title.string) if soup.title and soup.title.string else ""
    meta_desc = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md:
        meta_desc = md.get("content", "")
    if len(wp) != 1:
        honest["mismatches"].append({"route": route, "check": "WebPage count", "got": len(wp), "want": 1})
    else:
        if wp[0].get("name") != page["metaTitle"]:
            honest["mismatches"].append({"route": route, "check": "WebPage.name vs metaTitle",
                "schema": wp[0].get("name"), "data": page["metaTitle"]})
        if wp[0].get("description") != page["metaDescription"]:
            honest["mismatches"].append({"route": route, "check": "WebPage.description vs metaDescription",
                "schema": wp[0].get("description"), "data": page["metaDescription"]})
        if wp[0].get("name") != title_tag:
            honest["mismatches"].append({"route": route, "check": "WebPage.name vs <title>",
                "schema": wp[0].get("name"), "rendered": title_tag})
        if wp[0].get("description") != meta_desc:
            honest["mismatches"].append({"route": route, "check": "WebPage.description vs meta description",
                "schema": wp[0].get("description"), "rendered": meta_desc})
    # --- ImageObject caption vs rendered hero img alt; contentUrl vs hero src ---
    imgs = by_type(route, "ImageObject")
    hero_imgs = soup.select(".hero img, header img")
    hero_alt = hero_imgs[0].get("alt", "") if hero_imgs else ""
    hero_src = hero_imgs[0].get("src", "") if hero_imgs else ""
    if len(imgs) != 1:
        honest["mismatches"].append({"route": route, "check": "ImageObject count", "got": len(imgs), "want": 1})
    else:
        if imgs[0].get("caption") != hero_alt:
            honest["mismatches"].append({"route": route, "check": "ImageObject.caption vs hero alt",
                "schema": imgs[0].get("caption"), "rendered_alt": hero_alt})
        want_url = BASE + hero_src
        # hero_src rendered is ASSET_PREFIX + data src (single prefix).
        # The correct absolute URL is BASE + data src — i.e. strip ONE
        # leading subpath from the rendered src. (BASE itself already ends
        # in /midvale-water-damage, so BASE + rendered src double-prefixes.)
        if hero_src.startswith("/midvale-water-damage/"):
            want_url = BASE + hero_src[len("/midvale-water-damage"):]
        if imgs[0].get("contentUrl") != want_url:
            honest["mismatches"].append({"route": route, "check": "ImageObject.contentUrl vs hero src",
                "schema": imgs[0].get("contentUrl"), "rendered": want_url})
        # contentUrl must resolve to a real file in out/
        from urllib.parse import urlparse as _up
        _p = _up(imgs[0].get("contentUrl") or "").path
        _rel = _p[len("/midvale-water-damage/"):] if _p.startswith("/midvale-water-damage/") else _p.lstrip("/")
        if not (OUT / _rel).exists():
            honest["mismatches"].append({"route": route, "check": "ImageObject.contentUrl file exists in out/",
                "schema": imgs[0].get("contentUrl"), "resolved_path": _rel})
    # --- FAQPage vs data + visible ---
    faqs = by_type(route, "FAQPage")
    want_faq = len(page.get("faqs", []))
    if route == "/":
        want_faq = len(faq_home) if faq_home else want_faq
    if len(faqs) != (1 if want_faq > 0 else 0):
        honest["mismatches"].append({"route": route, "check": "FAQPage count",
            "got": len(faqs), "want": 1 if want_faq > 0 else 0})
    if faqs:
        ents = faqs[0].get("mainEntity", [])
        # visible FAQ
        vis_q, vis_a = [], []
        for item in soup.select("#faq .faq-item"):
            h3 = item.find("h3")
            p = item.find("p")
            vis_q.append(norm_ws(h3.get_text("")) if h3 else "")
            vis_a.append(norm_ws(p.get_text("")) if p else "")
        if route == "/":
            src_faqs = [(q, strip_annotations(a)) for q, a in (faq_home or [])]
        else:
            src_faqs = [(f["q"], strip_annotations(f["a"])) for f in page.get("faqs", [])]
        if len(ents) != len(src_faqs):
            honest["mismatches"].append({"route": route, "check": "FAQPage mainEntity count vs data",
                "got": len(ents), "want": len(src_faqs)})
        for i, (q, a) in enumerate(src_faqs):
            if i >= len(ents):
                break
            if ents[i].get("name") != q:
                honest["mismatches"].append({"route": route, "check": f"FAQ[{i}] question",
                    "schema": ents[i].get("name"), "data": q})
            if ents[i].get("acceptedAnswer", {}).get("text") != a:
                honest["mismatches"].append({"route": route, "check": f"FAQ[{i}] answer vs stripped data",
                    "schema": ents[i].get("acceptedAnswer", {}).get("text"), "data": a})
        if len(vis_q) != len(ents):
            honest["mismatches"].append({"route": route, "check": "FAQ visible count vs schema",
                "visible": len(vis_q), "schema": len(ents)})
        for i in range(min(len(vis_q), len(ents))):
            if vis_q[i] != ents[i].get("name"):
                honest["mismatches"].append({"route": route, "check": f"FAQ[{i}] visible Q vs schema",
                    "visible": vis_q[i], "schema": ents[i].get("name")})
            if vis_a[i] != ents[i].get("acceptedAnswer", {}).get("text"):
                honest["mismatches"].append({"route": route, "check": f"FAQ[{i}] visible A vs schema",
                    "visible": vis_a[i], "schema": ents[i].get("acceptedAnswer", {}).get("text")})
    # --- HowTo vs data ol blocks + visible ol ---
    hows = by_type(route, "HowTo")
    ol_blocks = []
    cur_h2 = None
    for b in page.get("blocks", []):
        if b["type"] == "h2":
            cur_h2 = b["text"]
        elif b["type"] == "ol":
            ol_blocks.append((cur_h2, b["items"]))
    if route == "/":
        # homepage HowTo comes from PROCESS (content.ts), not tab blocks
        ol_blocks = []
    if len(hows) != len(ol_blocks) and route != "/":
        honest["mismatches"].append({"route": route, "check": "HowTo count vs ol blocks",
            "got": len(hows), "want": len(ol_blocks)})
    for hi, (h2, items) in enumerate(ol_blocks):
        if hi >= len(hows):
            break
        if hows[hi].get("name") != h2:
            honest["mismatches"].append({"route": route, "check": f"HowTo[{hi}] name vs H2",
                "schema": hows[hi].get("name"), "data_h2": h2})
        steps = hows[hi].get("step", [])
        if len(steps) != len(items):
            honest["mismatches"].append({"route": route, "check": f"HowTo[{hi}] step count",
                "got": len(steps), "want": len(items)})
        for si, item in enumerate(items):
            want = strip_annotations("".join(s["t"] for s in item["segments"]))
            if si < len(steps) and steps[si].get("text") != want:
                honest["mismatches"].append({"route": route, "check": f"HowTo[{hi}] step[{si}] text",
                    "schema": steps[si].get("text"), "data": want})
    # visible ol comparison (all pages incl. homepage)
    vis_ols = [ol for ol in soup.find_all("ol") if ol.find_parent("nav") is None]
    # exclude breadcrumb ol (inside nav.breadcrumb) — already excluded via find_parent nav
    vis_ol_items = [[norm_ws(li.get_text("")) for li in ol.find_all("li", recursive=False)] or
                    [norm_ws(li.get_text("")) for li in ol.find_all("li")] for ol in vis_ols]
    schema_steps_all = [s.get("text") for h in hows for s in h.get("step", [])]
    vis_items_all = [it for ol in vis_ol_items for it in ol]
    if route == "/":
        # homepage: visible steps ol is ol.steps; schema steps from PROCESS
        if proc_home:
            want_steps = [norm_ws(l + " " + r) for l, r in proc_home]
            if schema_steps_all != want_steps:
                honest["mismatches"].append({"route": route, "check": "home HowTo steps vs PROCESS",
                    "schema": schema_steps_all, "data": want_steps})
            steps_ol = soup.select("ol.steps li")
            vis_steps = [norm_ws(li.get_text("")) for li in steps_ol]
            if vis_steps != want_steps:
                honest["mismatches"].append({"route": route, "check": "home visible steps vs PROCESS",
                    "visible": vis_steps, "data": want_steps})
            # HowTo name vs preceding H2
            h2s = [norm_ws(h.get_text()) for h in soup.find_all("h2")]
            if hows and hows[0].get("name") not in h2s:
                honest["mismatches"].append({"route": route, "check": "home HowTo name vs visible H2",
                    "schema": hows[0].get("name"), "visible_h2s": h2s})
    else:
        if schema_steps_all != vis_items_all:
            honest["mismatches"].append({"route": route, "check": "HowTo steps vs visible <ol> items",
                "schema": schema_steps_all, "visible": vis_items_all})
    # --- Service vs data ---
    svcs = by_type(route, "Service")
    if route != "/":
        # serviceKind known from route lists in content.ts / app routing: check later via source grep
        pass
    for s in svcs:
        if s.get("name") != page["h1"]:
            honest["mismatches"].append({"route": route, "check": "Service.name vs h1",
                "schema": s.get("name"), "data": page["h1"]})
        if s.get("serviceType") != page["h1"]:
            honest["mismatches"].append({"route": route, "check": "Service.serviceType vs h1",
                "schema": s.get("serviceType"), "data": page["h1"]})
        if s.get("description") != strip_annotations(page["intro"]):
            honest["mismatches"].append({"route": route, "check": "Service.description vs intro",
                "schema": s.get("description"), "data": strip_annotations(page["intro"])})
        # RE-VERIFY EDIT 2026-11-13 (FIX 2): Service areaServed shape + values.
        # 16 service pages -> Midvale/84047; 3 location pages -> their own
        # LOCATIONS city/ZIP. postalCode read from inside `address`.
        ar = s.get("areaServed") or {}
        addr = ar.get("address") or {}
        if route.startswith("/locations/"):
            want_city, want_zip = locs.get(route.rsplit("/", 1)[-1], (None, None))
        else:
            want_city, want_zip = "Midvale", "84047"
        got_area = (ar.get("@type"), ar.get("name"), addr.get("@type"),
                    addr.get("addressRegion"), addr.get("postalCode"))
        if got_area != ("City", want_city, "PostalAddress", "UT", want_zip):
            honest["mismatches"].append({"route": route, "check": "Service.areaServed City/PostalAddress",
                "schema": got_area, "want": ("City", want_city, "PostalAddress", "UT", want_zip)})
    # --- BreadcrumbList vs visible breadcrumb ---
    bcs = by_type(route, "BreadcrumbList")
    vis_crumb = soup.select("nav.breadcrumb ol li")
    vis_labels = [norm_ws(li.get_text(" ")) for li in vis_crumb]
    # strip separators like › / /
    vis_labels = [re.sub(r"[›»/]+$", "", l).strip() for l in vis_labels]
    if len(bcs) != 1:
        honest["mismatches"].append({"route": route, "check": "BreadcrumbList count", "got": len(bcs), "want": 1})
    elif route == "/" and not vis_crumb:
        # Homepage renders no visible breadcrumb by design; schema carries a
        # single-item "Home" breadcrumb. Not a mismatch — recorded, not counted.
        honest.setdefault("notes", []).append({"route": route,
            "note": "homepage has no visible breadcrumb nav by design; schema BreadcrumbList is single-item ['Home']"})
    else:
        items = bcs[0].get("itemListElement", [])
        names = [it.get("name") for it in items]
        if names != vis_labels:
            honest["mismatches"].append({"route": route, "check": "Breadcrumb names vs visible",
                "schema": names, "visible": vis_labels})
        for i, it in enumerate(items):
            if it.get("position") != i + 1:
                honest["mismatches"].append({"route": route, "check": "Breadcrumb position",
                    "index": i, "got": it.get("position")})
    # --- SpeakableSpecification selectors match DOM ---
    wp0 = wp[0] if wp else {}
    spk = wp0.get("speakable", {})
    sels = spk.get("cssSelector", []) if isinstance(spk, dict) else []
    for sel in sels:
        try:
            n = len(soup.select(sel))
        except Exception as e:
            n = -1
        if n < 1:
            honest["mismatches"].append({"route": route, "check": f"Speakable selector no match: {sel}",
                "matches": n})

# homepage-only blocks
home_raw = (OUT / "index.html").read_text()
home_soup = BeautifulSoup(home_raw, "html.parser")
lb = by_type("/", "HomeAndConstructionBusiness")
ws = by_type("/", "WebSite")
if len(lb) != 1:
    honest["mismatches"].append({"route": "/", "check": "HomeAndConstructionBusiness count", "got": len(lb), "want": 1})
else:
    b = lb[0]
    if b.get("name") != "Water Damage Restoration Midvale UT":
        honest["mismatches"].append({"route": "/", "check": "LocalBusiness.name vs brand", "schema": b.get("name")})
    if b.get("description") != PAGES["/"]["metaDescription"]:
        honest["mismatches"].append({"route": "/", "check": "LocalBusiness.description vs metaDescription",
            "schema": b.get("description"), "data": PAGES["/"]["metaDescription"]})
    if b.get("telephone") != "+13853373560":
        honest["mismatches"].append({"route": "/", "check": "LocalBusiness.telephone", "schema": b.get("telephone")})
    if b.get("hasMap") != "https://www.google.com/maps?q=Midvale,+UT+84047":
        honest["mismatches"].append({"route": "/", "check": "LocalBusiness.hasMap value", "schema": b.get("hasMap")})
    # footer map iframe src must carry the same query
    ifr = home_soup.find("iframe")
    if ifr:
        honest["footer_iframe_src"] = ifr.get("src", "")
        q = re.search(r"q=([^&]+)", ifr.get("src", "") or "")
        if q and q.group(1).replace("%2C", ",").replace("%20", " ").replace("+", " ") not in (
                "Midvale, UT 84047",):
            honest["mismatches"].append({"route": "/", "check": "hasMap vs footer map query",
                "schema": b.get("hasMap"), "footer": ifr.get("src", "")})
    else:
        honest["mismatches"].append({"route": "/", "check": "footer map iframe", "got": "none found"})
    # areaServed cities/ZIPs vs location data
    # RE-VERIFY EDIT 2026-11-13 (FIX 2): postalCode now lives inside
    # `address` (PostalAddress), not top-level on the City node.
    want_areas = {("Midvale", "84047"), ("Cottonwood Heights", "84121"),
                  ("South Salt Lake", "84115"), ("Magna", "84044")}
    got_areas = {(a.get("name"), (a.get("address") or {}).get("postalCode"))
                 for a in b.get("areaServed", [])}
    if got_areas != want_areas:
        honest["mismatches"].append({"route": "/", "check": "LocalBusiness.areaServed",
            "schema": sorted(got_areas), "want": sorted(want_areas)})
if len(ws) != 1:
    honest["mismatches"].append({"route": "/", "check": "WebSite count", "got": len(ws), "want": 1})
else:
    if ws[0].get("name") != "Water Damage Restoration Midvale UT":
        honest["mismatches"].append({"route": "/", "check": "WebSite.name vs brand", "schema": ws[0].get("name")})
    if ws[0].get("url") != BASE + "/":
        honest["mismatches"].append({"route": "/", "check": "WebSite.url", "schema": ws[0].get("url")})

# 404 page
raw404 = (OUT / "404.html").read_text()
results["routes"]["/404"]["ld_blocks_404"] = len(LD_RE.findall(raw404))

# ---------- regression (static) ----------
reg = results["regression"]
reg["h1_counts"] = {}
reg["title_meta_ok"] = {}
reg["visible_words"] = {}
reg["missing_words"] = {}
reg["tables"] = {}
reg["robots"] = {}
all_hrefs = []
body_links = 0
card_links = 0
self_links = []
orphan_links = []
broken_links = []
visible_paren_pages = []
localhost_hits = []
doubleslash_hits = []
known_routes = set(PAGES.keys())
for route, page in PAGES.items():
    f = routes[route]
    raw = f.read_text()
    soup = BeautifulSoup(raw, "html.parser")
    h1s = soup.find_all("h1")
    reg["h1_counts"][route] = len(h1s)
    title_tag = norm_ws(soup.title.string) if soup.title and soup.title.string else ""
    md = soup.find("meta", attrs={"name": "description"})
    meta_desc = md.get("content", "") if md else ""
    reg["title_meta_ok"][route] = (title_tag == page["metaTitle"] and meta_desc == page["metaDescription"])
    # visible words + missing words (data-derived expected content)
    vis = visible_text(soup)
    reg["visible_words"][route] = len(vis.split())
    exp_parts = [page.get("eyebrow") or "", page["h1"], page["intro"]]
    for b in page.get("blocks", []):
        if b["type"] in ("h2", "h3"):
            exp_parts.append(b["text"])
        elif b["type"] == "p":
            exp_parts.append(strip_annotations("".join(s["t"] for s in b["segments"])))
        elif b["type"] in ("ul", "ol"):
            for it in b["items"]:
                exp_parts.append(strip_annotations("".join(s["t"] for s in it["segments"])))
        elif b["type"] == "table":
            exp_parts.append(" ".join(b["headers"]))
            for r in b["rows"]:
                exp_parts.append(" ".join(r))
    for fq in page.get("faqs", []):
        exp_parts.append(fq["q"])
        exp_parts.append(strip_annotations(fq["a"]))
    exp_words = set(words(" ".join(exp_parts)))
    vis_words = set(words(vis))
    missing = sorted(exp_words - vis_words)
    reg["missing_words"][route] = missing
    # tables
    reg["tables"][route] = len(soup.find_all("table"))
    # robots
    robots = [m.get("content", "") for m in soup.find_all("meta", attrs={"name": "robots"})]
    reg["robots"][route] = robots
    # links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        all_hrefs.append((route, href))
        cls = " ".join(a.get("class", []))
        if "body-link" in cls:
            body_links += 1
        if "card" in cls or a.find_parent("a") is None and a.find("img") is not None:
            pass
        # self-link: internal href == own route (no-slash form)
        if href.startswith("/midvale-water-damage/"):
            tgt = "/" + href[len("/midvale-water-damage/"):]
            if tgt == "" :
                tgt = "/"
            if tgt.rstrip("/") == route.rstrip("/") and route != "/":
                # exclude header/footer/sticky: only body links count as self-links
                if "body-link" in cls:
                    self_links.append((route, href))
            if tgt not in known_routes and tgt != "/":
                orphan_links.append((route, href))
    if re.search(r"\(/", vis):
        visible_paren_pages.append(route)
# card links: anchors with class containing card OR service-card images
card_count = 0
for route, page in PAGES.items():
    soup = BeautifulSoup(routes[route].read_text(), "html.parser")
    for a in soup.find_all("a", href=True):
        if a.find("img") is not None and a["href"].startswith("/midvale-water-damage/"):
            card_count += 1
reg["total_links"] = len(all_hrefs)
reg["body_links"] = body_links
reg["card_links_img"] = card_count
reg["self_links"] = self_links
reg["orphan_links"] = orphan_links
reg["visible_paren_pages"] = visible_paren_pages
# broken: internal link targets must exist as files in out/
for route, href in all_hrefs:
    if href.startswith("/midvale-water-damage/"):
        p = href[len("/midvale-water-damage/"):]
        if p == "":
            p = "index.html"
        elif p.startswith("images/") or p.startswith("_next/") or p in ("favicon.svg",):
            continue
        elif "." not in p.split("/")[-1]:
            p = p + ".html"
        if not (OUT / p).exists():
            broken_links.append((route, href))
reg["broken_links"] = broken_links
# localhost + double-slash across out/ html/xml/txt
for f in sorted(OUT.rglob("*")):
    if f.is_file() and f.suffix in (".html", ".xml", ".txt"):
        t = f.read_text(errors="ignore")
        if "localhost" in t:
            localhost_hits.append(str(f.relative_to(OUT)))
        # double-slash outside scheme: look for // after base path or in attrs
        for mm in re.finditer(r'(?:href|src|content)="([^"]*)"', t):
            v = mm.group(1)
            v2 = re.sub(r"^https?://", "", v)
            if "//" in v2:
                doubleslash_hits.append((str(f.relative_to(OUT)), v))
reg["localhost_files"] = localhost_hits
reg["doubleslash_attrs"] = doubleslash_hits
# tables total from data
reg["tables_data_total"] = sum(1 for p in PAGES.values() for b in p.get("blocks", []) if b["type"] == "table")
reg["tables_rendered_total"] = sum(reg["tables"].values())
reg["faq_total_data"] = sum(len(p.get("faqs", [])) for p in PAGES.values())
reg["faq_total_schema"] = sum(
    len(by_type(r, "FAQPage")[0].get("mainEntity", [])) if by_type(r, "FAQPage") else 0
    for r in PAGES)
reg["howto_total_schema"] = sum(len(by_type(r, "HowTo")) for r in PAGES)
reg["howto_steps_schema"] = sum(len(h.get("step", [])) for r in PAGES for h in by_type(r, "HowTo"))
reg["ol_blocks_data"] = sum(1 for p in PAGES.values() for b in p.get("blocks", []) if b["type"] == "ol")
# image contentUrls 200 check is done against the live-served export by the render script;
# here record the distinct contentUrls
reg["image_content_urls"] = sorted({by_type(r, "ImageObject")[0]["contentUrl"]
                                    for r in PAGES if by_type(r, "ImageObject")})

# serialize
def default(o):
    if isinstance(o, Counter):
        return dict(o)
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(repr(o))
(ROOT / "qa" / "verify-schema-2026-11-13.json").write_text(
    json.dumps(results, indent=1, default=default))
print("TOTAL BLOCKS:", results["total_blocks"])
print("BY TYPE:", dict(results["totals_by_type"]))
print("PARSE ERRORS:", len(results["parse_errors"]))
print("DUP IDS:", results["dup_ids"])
print("UNRESOLVED REFS:", results["unresolved_refs"])
print("CROSS-PAGE REFS:", len(results["cross_page_refs"]))
print("FORBIDDEN:", results["forbidden"])
print("URL PROBLEMS:", results["url_problems"])
print("PROP PROBLEMS:", results["prop_problems"])
print("POSTALADDRESS NODES:", len(results["postal_address_nodes"]),
      sorted({(n["addressRegion"], n["postalCode"]) for n in results["postal_address_nodes"]}))
print("UNVERIFIED PROPS:", len(results["unverified_props"]))
print("HONEST MISMATCHES:", len(honest["mismatches"]))
for mm in honest["mismatches"][:40]:
    print("  MISMATCH:", json.dumps(mm)[:400])
print("H1 COUNTS != 1:", {k: v for k, v in reg["h1_counts"].items() if v != 1})
print("TITLE/META FAIL:", [k for k, v in reg["title_meta_ok"].items() if not v])
print("MISSING WORDS:", {k: v for k, v in reg["missing_words"].items() if v})
print("TABLES data/rendered:", reg["tables_data_total"], reg["tables_rendered_total"])
print("FAQ data/schema:", reg["faq_total_data"], reg["faq_total_schema"])
print("HOWTO blocks data/schema:", reg["ol_blocks_data"], reg["howto_total_schema"],
      "steps:", reg["howto_steps_schema"])
print("LINKS total/body/img-card:", reg["total_links"], reg["body_links"], reg["card_links_img"])
print("SELF:", reg["self_links"])
print("ORPHANS:", reg["orphan_links"])
print("BROKEN:", reg["broken_links"])
print("VISIBLE PAREN:", reg["visible_paren_pages"])
print("LOCALHOST FILES:", reg["localhost_files"])
print("DOUBLESLASH:", reg["doubleslash_attrs"][:10])
print("ROBOTS non index,follow:", {k: v for k, v in reg["robots"].items() if v != ["index, follow"]})
print("404 ld blocks:", results["routes"]["/404"].get("ld_blocks_404"))
print("VISIBLE WORDS:", reg["visible_words"])
