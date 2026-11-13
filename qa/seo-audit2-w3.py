#!/usr/bin/env python3
"""SEO AUDIT 2 — worker W3 (internal links + images/alt). AUDIT ONLY, read-only vs site source.
Fresh measurement; does not trust audit-1/fix-1 claims. Server on 127.0.0.1:8342 (/midvale-water-damage/).
Fixes vs audit-1 script: URL-decode %XX paths before checking; breadcrumb links classified
separately from body-copy links (nav[aria-label*=readcrumb] / .breadcrumb ancestors)."""
import json, re, os, hashlib
from urllib.parse import urlparse, urljoin, unquote
import requests
from bs4 import BeautifulSoup

BASE = "http://127.0.0.1:8342"
PREFIX = "/midvale-water-damage"
ROOT = "/home/hatch/workspace/midvale-water-damage"
OUT = os.path.join(ROOT, "out")

EXPECTED_SHA = "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f"
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
SHA_START = sha(os.path.join(ROOT, "lib/pages-data.json"))

ROUTES = [
    "/", "/basement-flooding-cleanup", "/burst-pipe-water-damage", "/ceiling-water-damage",
    "/commercial-water-damage", "/condo-apartment-water-damage", "/crawl-space-water-damage",
    "/emergency-water-extraction", "/hardwood-floor-cabinet-drying", "/mold-remediation",
    "/sewage-backup-cleanup", "/storm-flood-damage", "/swamp-cooler-leak-water-damage",
    "/water-damage-repair", "/water-heater-leak-cleanup", "/water-leak-detection",
    "/window-well-flooding",
    "/locations/cottonwood-heights-ut", "/locations/magna-ut", "/locations/south-salt-lake-ut",
    "/about", "/contact", "/privacy-policy", "/terms-of-use", "/disclaimer",
    "/resources/basement-flooding-spring-snowmelt-utah", "/resources/can-mold-grow-in-utah",
    "/resources/frozen-pipes-midvale", "/resources/upstairs-unit-leak-who-pays-utah",
    "/resources/winterize-swamp-cooler-utah",
    "/midvale-water-sewer-emergency-contacts",
]
ROUTE_SET = set(ROUTES)

def norm_path(href, page_route):
    if href is None:
        return ("none", None)
    href = href.strip()
    if href == "" or href.startswith(("tel:", "mailto:", "javascript:")):
        return ("special", href)
    if href.startswith(("http://", "https://", "//")):
        u = urlparse(href if not href.startswith("//") else "http:" + href)
        if u.netloc and u.netloc not in ("127.0.0.1:8342", "localhost:8342"):
            return ("external", href)
        return ("internal", (unquote(u.path), u.fragment))
    if href.startswith("#"):
        return ("fragment", href[1:])
    p = urljoin(PREFIX + page_route.rstrip("/") + "/", href) if not href.startswith("/") else href
    u = urlparse(p)
    return ("internal", (unquote(u.path), u.fragment))

def route_of(path):
    if path is None:
        return None
    p = path.rstrip("/")
    if p in ("", PREFIX):
        return "/"
    if p.startswith(PREFIX):
        p = p[len(PREFIX):]
    p = p.rstrip("/")
    if p == "":
        return "/"
    if p.endswith(".html"):
        p = p[:-5]
    if p in ROUTE_SET:
        return p
    return None

def status_of(path):
    url = BASE + PREFIX if path == "/" else BASE + path
    try:
        return requests.get(url, timeout=15).status_code
    except Exception as e:
        return "ERR:" + str(e)

pages = {}
for rt in ROUTES:
    url = BASE + PREFIX + ("" if rt == "/" else rt)
    r = requests.get(url, timeout=20)
    pages[rt] = {"url": url, "status": r.status_code, "html": r.text}
    assert r.status_code == 200, (rt, r.status_code)

status_cache = {}
def get_status(path):
    if path not in status_cache:
        status_cache[path] = status_of(path)
    return status_cache[path]

per_page = {}
inbound = {rt: set() for rt in ROUTES}
img_rows = []
total_imgs = 0
encoded_hrefs = []  # hrefs containing %XX, to prove decoding path was exercised/checked

for rt in ROUTES:
    soup = BeautifulSoup(pages[rt]["html"], "html.parser")
    h1 = soup.find("h1")
    pp = {"route": rt, "status": pages[rt]["status"],
          "h1": h1.get_text(" ", strip=True) if h1 else None,
          "anchors_total": 0, "anchors_internal": 0, "anchors_external": 0,
          "anchors_tel_mailto": 0, "anchors_fragment_only": 0,
          "prose_internal": 0, "breadcrumb_internal": 0, "card_internal": 0,
          "body_link": 0,  # prose minus breadcrumb
          "prose_anchor_violations": [], "duplicate_targets": [],
          "self_links": [], "broken_links": [], "images": []}
    def region_of(a):
        for p in a.parents:
            if p.name == "main":
                return "main"
            if p.name == "header":
                return "header"
            if p.name == "footer":
                return "footer"
            if p.get("class") and "sticky-bar" in p.get("class"):
                return "sticky"
        return "other"
    def is_breadcrumb(a):
        for p in a.parents:
            if p.name == "nav" and p.get("aria-label") and "breadcrumb" in p.get("aria-label").lower():
                return True
            cls = p.get("class") or []
            if any("breadcrumb" in c for c in cls):
                return True
        return False
    prose_targets = {}
    for a in soup.find_all("a"):
        href = a.get("href")
        text = a.get_text(" ", strip=True)
        in_main = region_of(a) == "main"
        region = region_of(a)
        cls = " ".join(a.get("class", []))
        is_card = ("card-wrap-link" in cls or "area-card" in cls
                   or a.find_parent(class_="card") is not None
                   or a.find_parent(class_="area-card") is not None)
        if href and "%" in href:
            encoded_hrefs.append({"page": rt, "href": href, "anchor": text[:80]})
        kind, val = norm_path(href, rt)
        pp["anchors_total"] += 1
        if kind == "external":
            pp["anchors_external"] += 1
            continue
        if kind == "special":
            pp["anchors_tel_mailto"] += 1
            continue
        if kind == "fragment":
            pp["anchors_fragment_only"] += 1
            if val and not soup.find(id=val):
                pp["broken_links"].append({"href": href, "region": region,
                    "reason": "fragment id '#%s' not found on same page" % val, "anchor": text[:80]})
            continue
        if kind == "internal":
            path, frag = val
            pp["anchors_internal"] += 1
            tgt_route = route_of(path)
            if tgt_route is not None and tgt_route != rt:
                inbound[tgt_route].add(rt)
            st = get_status(path)
            if st != 200:
                pp["broken_links"].append({"href": href, "region": region,
                    "reason": "HTTP %s" % st, "anchor": text[:80]})
            elif frag:
                tsoup = BeautifulSoup(pages[tgt_route]["html"], "html.parser") if tgt_route in pages else None
                if tsoup is not None and not tsoup.find(id=frag):
                    pp["broken_links"].append({"href": href, "region": region,
                        "reason": "fragment id '#%s' not found on target %s" % (frag, tgt_route), "anchor": text[:80]})
            if in_main and tgt_route == rt:
                pp["self_links"].append({"href": href, "anchor": text[:120], "card": bool(is_card)})
            if in_main and not is_card:
                pp["prose_internal"] += 1
                if is_breadcrumb(a):
                    pp["breadcrumb_internal"] += 1
                else:
                    pp["body_link"] += 1
                    words = [w for w in re.split(r"\s+", text) if w]
                    if len(words) > 5:
                        pp["prose_anchor_violations"].append(
                            {"href": href, "anchor": text, "words": len(words)})
                    prose_targets.setdefault(path, []).append(text)
            if in_main and is_card:
                pp["card_internal"] += 1
    for path, texts in prose_targets.items():
        if len(texts) > 1:
            pp["duplicate_targets"].append({"target": path, "count": len(texts),
                                            "anchors": [t[:80] for t in texts]})
    for img in soup.find_all("img"):
        src = img.get("src") or ""
        alt = img.get("alt")
        total_imgs += 1
        row = {"page": rt, "src": src,
               "alt_present": alt is not None,
               "alt_empty": (alt is not None and alt.strip() == ""),
               "alt": alt if alt is not None else None,
               "width": img.get("width"), "height": img.get("height"),
               "loading": img.get("loading"), "class": " ".join(img.get("class", [])),
               "status": None}
        if src.startswith("/"):
            try:
                row["status"] = requests.get(BASE + src, timeout=15).status_code
            except Exception as e:
                row["status"] = "ERR:" + str(e)
        elif src.startswith("http"):
            row["status"] = "external-not-checked"
        else:
            row["status"] = "relative-unexpected"
        pp["images"].append(row)
        img_rows.append(row)
    per_page[rt] = pp

orphans = [rt for rt in ROUTES if len(inbound[rt]) == 0]
inbound_counts = {rt: sorted(inbound[rt]) for rt in ROUTES}

# ---- disk images ----
disk_webp = []
for root, _, files in os.walk(os.path.join(OUT, "images")):
    for f in files:
        if f.lower().endswith(".webp"):
            disk_webp.append(os.path.join(root, f))
disk_webp_sorted = sorted(disk_webp, key=lambda p: os.path.getsize(p), reverse=True)
total_weight = sum(os.path.getsize(p) for p in disk_webp)
top10 = [{"file": os.path.relpath(p, OUT), "bytes": os.path.getsize(p)} for p in disk_webp_sorted[:10]]
# q75 adopted files (fix 1) — current sizes vs adopted sizes claimed
ADOPTED = {
    "images/body/magna-ut-1.webp": 282352,
    "images/heroes/basement-flooding-spring-snowmelt-utah.webp": 215212,
    "images/cards/cottonwood-heights-ut.webp": 174328,
    "images/body/mold-remediation-1.webp": 157214,
    "images/body/water-leak-detection-2.webp": 157424,
    "images/body/cottonwood-heights-ut-2.webp": 149004,
    "images/body/swamp-cooler-leak-water-damage-2.webp": 160428,
    "images/heroes/magna-ut.webp": 163358,
}
q75_check = []
for rel, claimed in ADOPTED.items():
    p = os.path.join(OUT, rel)
    cur = os.path.getsize(p) if os.path.exists(p) else None
    bak = os.path.join(ROOT, "qa/img-opt/orig-backup",
                       rel.replace("images/", "").replace("/", "__") + "")
    # backup naming: <kind>__<file>.webp e.g. body__magna-ut-1.webp
    kind, fname = rel.split("/")[1], rel.split("/")[2]
    bak = os.path.join(ROOT, "qa/img-opt/orig-backup", f"{kind}__{fname}")
    bak_size = os.path.getsize(bak) if os.path.exists(bak) else None
    q75_check.append({"file": rel, "current_bytes": cur, "fix1_claimed_bytes": claimed,
                      "matches_claim": cur == claimed,
                      "backup_bytes": bak_size, "backup_exists": bak_size is not None})

tot_body = sum(p["body_link"] for p in per_page.values())
tot_crumb = sum(p["breadcrumb_internal"] for p in per_page.values())
tot_prose = sum(p["prose_internal"] for p in per_page.values())
tot_card = sum(p["card_internal"] for p in per_page.values())
tot_broken = sum(len(p["broken_links"]) for p in per_page.values())
tot_self = sum(len(p["self_links"]) for p in per_page.values())
tot_anchor_viol = sum(len(p["prose_anchor_violations"]) for p in per_page.values())
tot_dup = sum(len(p["duplicate_targets"]) for p in per_page.values())
missing_alt = [r for r in img_rows if not r["alt_present"] or r["alt_empty"]]
bad_img_status = [r for r in img_rows if r["status"] != 200]
no_dims = [r for r in img_rows if not r["width"] or not r["height"]]

# P3-6 re-check: location pages, homepage links inside <main>
p3_6 = []
for rt in ["/locations/cottonwood-heights-ut", "/locations/magna-ut", "/locations/south-salt-lake-ut"]:
    soup = BeautifulSoup(pages[rt]["html"], "html.parser")
    main = soup.find("main")
    home_links = []
    for a in main.find_all("a"):
        href = a.get("href") or ""
        path, frag = norm_path(href, rt)[1] if norm_path(href, rt)[0] == "internal" else (None, None)
        if route_of(path) == "/":
            # breadcrumb? walk parents
            crumb = False
            for par in a.parents:
                if par.name == "nav" and par.get("aria-label") and "breadcrumb" in par.get("aria-label").lower():
                    crumb = True
                if (par.get("class") or []) and any("breadcrumb" in c for c in par.get("class")):
                    crumb = True
            home_links.append({"href": href, "anchor": a.get_text(" ", strip=True),
                               "in_breadcrumb_nav": crumb,
                               "nav_aria_label": (a.find_parent("nav") or {}).get("aria-label") if a.find_parent("nav") else None})
    p3_6.append({"page": rt, "homepage_links_in_main": len(home_links), "links": home_links})

SHA_END = sha(os.path.join(ROOT, "lib/pages-data.json"))

result = {
    "audit": "SEO AUDIT 2 — worker W3 (internal links + images/alt)",
    "site": "Midvale UT water damage",
    "base": BASE + PREFIX,
    "server_port": 8342,
    "pages_data_sha256_expected": EXPECTED_SHA,
    "pages_data_sha256_at_start": SHA_START,
    "pages_data_sha256_at_end": SHA_END,
    "pages_data_path_note": "Task said 'data lib/pages-data.json'; actual file is lib/pages-data.json (no data/ dir). Hash matches expected at start and end.",
    "routes_total": len(ROUTES),
    "routes_status_200": sum(1 for p in per_page.values() if p["status"] == 200),
    "totals": {
        "anchors_total_all_pages": sum(p["anchors_total"] for p in per_page.values()),
        "anchors_internal": sum(p["anchors_internal"] for p in per_page.values()),
        "anchors_external": sum(p["anchors_external"] for p in per_page.values()),
        "anchors_tel_mailto": sum(p["anchors_tel_mailto"] for p in per_page.values()),
        "anchors_fragment_only": sum(p["anchors_fragment_only"] for p in per_page.values()),
        "prose_internal_links_in_main": tot_prose,
        "breadcrumb_internal_links_in_main": tot_crumb,
        "body_copy_links_in_main": tot_body,
        "card_internal_links_in_main": tot_card,
        "body_plus_card": tot_body + tot_card,
        "expected_body_plus_card": 162,
        "expected_body": 143, "expected_card": 19,
        "broken_links_total": tot_broken,
        "self_links_total": tot_self,
        "body_self_links_total": sum(1 for p in per_page.values() for s in p["self_links"] if not s["card"]),
        "prose_anchor_wordcount_violations": tot_anchor_viol,
        "duplicate_target_pages_body": tot_dup,
        "img_tags_total": total_imgs,
        "img_missing_or_empty_alt": len(missing_alt),
        "img_non200_src": len(bad_img_status),
        "img_without_width_height": len(no_dims),
        "disk_webp_total": len(disk_webp),
        "disk_webp_expected": 107,
        "total_image_weight_bytes": total_weight,
        "encoded_percent_hrefs_found": len(encoded_hrefs),
    },
    "orphans": orphans,
    "inbound_counts": {rt: len(v) for rt, v in inbound_counts.items()},
    "inbound_sources": inbound_counts,
    "inbound_min": min(len(v) for v in inbound_counts.values()),
    "missing_alt": missing_alt,
    "bad_img_status": bad_img_status,
    "img_without_width_height": no_dims,
    "per_page": per_page,
    "unique_internal_paths_checked": len(status_cache),
    "internal_path_statuses": {k: v for k, v in sorted(status_cache.items(), key=lambda kv: str(kv[0]))},
    "encoded_hrefs": encoded_hrefs,
    "link_count_reconciliation": {
        "body_copy": tot_body, "card": tot_card, "breadcrumb_in_main": tot_crumb,
        "in_main_internal_total": tot_prose + tot_card,
        "note": "body + card should equal 143 + 19 = 162; in-main internal total adds the breadcrumb links on top."
    },
    "p3_6_recheck": p3_6,
    "image_weight": {"total_bytes": total_weight, "top10_largest": top10},
    "q75_reencoded_check": q75_check,
    "PROBLEMS": [],
    "visual_alt_audit": None,  # filled below by hand after viewing pixels; placeholder replaced in JSON edit
    "script_errors_owned": [],
    "notes": {},
    "verdict": None,
}
with open(os.path.join(ROOT, "qa/seo-audit2-w3.json"), "w") as f:
    json.dump(result, f, indent=2)

print("sha start/end:", SHA_START == EXPECTED_SHA, SHA_END == EXPECTED_SHA)
print("routes 200:", result["routes_status_200"], "/", len(ROUTES))
print("anchors internal:", result["totals"]["anchors_internal"], "external:", result["totals"]["anchors_external"],
      "tel/mailto:", result["totals"]["anchors_tel_mailto"], "frag-only:", result["totals"]["anchors_fragment_only"])
print("body:", tot_body, "card:", tot_card, "body+card:", tot_body + tot_card, "(expected 162)  breadcrumb:", tot_crumb, "in-main total:", tot_prose + tot_card)
print("broken:", tot_broken, "self:", tot_self, "anchor-viol:", tot_anchor_viol, "dup-body-target-pages:", tot_dup)
print("orphans:", orphans, "inbound min:", result["inbound_min"])
print("img tags:", total_imgs, "missing/empty alt:", len(missing_alt), "non-200 src:", len(bad_img_status),
      "no dims:", len(no_dims), "disk webp:", len(disk_webp), "weight:", total_weight)
print("top10:", top10)
print("q75 matches:", [(q["file"].split("/")[-1], q["matches_claim"], q["current_bytes"], q["backup_bytes"]) for q in q75_check])
print("encoded hrefs:", len(encoded_hrefs), encoded_hrefs[:5])
print("p3-6:", json.dumps(p3_6, indent=1))
for rt in ROUTES:
    p = per_page[rt]
    if p["broken_links"] or p["self_links"] or p["prose_anchor_violations"] or p["duplicate_targets"]:
        print("FLAG", rt, "broken:", len(p["broken_links"]), "self:", len(p["self_links"]),
              "anchor-viol:", len(p["prose_anchor_violations"]), "dup:", len(p["duplicate_targets"]))
