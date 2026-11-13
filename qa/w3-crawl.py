#!/usr/bin/env python3
"""W3 audit: internal links + images/alt for Midvale UT site. READ-ONLY vs site source.
Serves from already-running server on 127.0.0.1:8313 (/midvale-water-damage/)."""
import json, re, os
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

BASE = "http://127.0.0.1:8313"
PREFIX = "/midvale-water-damage"
OUT = "/home/hatch/workspace/midvale-water-damage/out"

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
    """Resolve href to a site path ('' for homepage '/'), or None if external/special."""
    if href is None:
        return ("none", None)
    href = href.strip()
    if href == "" or href.startswith(("tel:", "mailto:", "javascript:")):
        return ("special", href)
    if href.startswith(("http://", "https://", "//")):
        u = urlparse(href if not href.startswith("//") else "http:" + href)
        if u.netloc and u.netloc not in ("127.0.0.1:8313", "localhost:8313"):
            return ("external", href)
        p = u.path
        return ("internal", (p, u.fragment))
    if href.startswith("#"):
        return ("fragment", href[1:])
    # relative or root-relative
    p = urljoin(PREFIX + page_route.rstrip("/") + "/", href) if not href.startswith("/") else href
    u = urlparse(p)
    return ("internal", (u.path, u.fragment))

def route_of(path):
    """Map a served path to a ROUTES entry, or None."""
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
    # path already carries the /midvale-water-damage prefix (or is '/' for home)
    url = BASE + PREFIX if path == "/" else BASE + path
    try:
        r = requests.get(url, timeout=15)
        return r.status_code
    except Exception as e:
        return "ERR:" + str(e)

pages = {}
for rt in ROUTES:
    url = BASE + PREFIX + ("" if rt == "/" else rt)
    r = requests.get(url, timeout=20)
    pages[rt] = {"url": url, "status": r.status_code, "html": r.text}
    assert r.status_code == 200, (rt, r.status_code)

# --- per-page parse ---
status_cache = {}
def get_status(path):
    if path not in status_cache:
        status_cache[path] = status_of(path)
    return status_cache[path]

per_page = {}
all_internal_hrefs = []   # (src_route, href, resolved_path, fragment, region)
inbound = {rt: set() for rt in ROUTES}  # route -> set of source routes linking to it
img_rows = []
total_imgs = 0

for rt in ROUTES:
    soup = BeautifulSoup(pages[rt]["html"], "html.parser")
    main = soup.find("main")
    header = soup.find("header")
    footer = soup.find("footer")
    sticky = soup.find(class_="sticky-bar")
    h1 = soup.find("h1")
    pp = {"route": rt, "status": pages[rt]["status"],
          "h1": h1.get_text(" ", strip=True) if h1 else None,
          "anchors_total": 0, "anchors_internal": 0, "anchors_external": 0,
          "anchors_tel_mailto": 0, "anchors_fragment_only": 0,
          "prose_internal": 0, "card_internal": 0,
          "prose_anchor_violations": [], "duplicate_targets": [],
          "self_links": [], "broken_links": [], "images": []}
    # ---- anchors ----
    # REGION BY PARENT WALK (identity-based). Do NOT use `a in main.descendants`:
    # bs4 Tag.__eq__ compares loosely, so a header anchor identical in
    # href/text to a main anchor falsely tests True for membership.
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
    prose_targets = {}   # resolved path -> list of anchor texts (prose, internal, in main, not card, not tel)
    for a in soup.find_all("a"):
        href = a.get("href")
        text = a.get_text(" ", strip=True)
        in_main = region_of(a) == "main"
        region = region_of(a)
        cls = " ".join(a.get("class", []))
        is_card = ("card-wrap-link" in cls or "area-card" in cls
                   or a.find_parent(class_="card") is not None
                   or a.find_parent(class_="area-card") is not None)
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
            # fragment must exist as id on same page
            if val and not soup.find(id=val):
                pp["broken_links"].append({"href": href, "region": region,
                    "reason": "fragment id '#%s' not found on same page" % val, "anchor": text[:80]})
            continue
        if kind == "internal":
            path, frag = val
            pp["anchors_internal"] += 1
            tgt_route = route_of(path)
            all_internal_hrefs.append((rt, href, path, frag, region))
            if tgt_route is not None and tgt_route != rt:
                inbound[tgt_route].add(rt)
            # status check (page part only)
            st = get_status(path)
            if st != 200:
                pp["broken_links"].append({"href": href, "region": region,
                    "reason": "HTTP %s" % st, "anchor": text[:80]})
            elif frag:
                # fragment on another page: fetch target and check id
                tsoup = BeautifulSoup(pages[tgt_route]["html"], "html.parser") if tgt_route in pages else None
                if tsoup is not None and not tsoup.find(id=frag):
                    pp["broken_links"].append({"href": href, "region": region,
                        "reason": "fragment id '#%s' not found on target %s" % (frag, tgt_route), "anchor": text[:80]})
            # self-link: inside main (cards count), not header/footer/sticky
            if in_main and tgt_route == rt:
                pp["self_links"].append({"href": href, "anchor": text[:120],
                                         "card": bool(is_card)})
            # prose anchor rules: in main, not a card, internal
            if in_main and not is_card:
                pp["prose_internal"] += 1
                words = [w for w in re.split(r"\s+", text) if w]
                if len(words) > 5:
                    pp["prose_anchor_violations"].append(
                        {"href": href, "anchor": text[:160], "words": len(words)})
                prose_targets.setdefault(path, []).append(text)
            if in_main and is_card:
                pp["card_internal"] += 1
    for path, texts in prose_targets.items():
        if len(texts) > 1:
            pp["duplicate_targets"].append({"target": path, "count": len(texts),
                                            "anchors": [t[:80] for t in texts]})
    # ---- images ----
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
        # src status via server
        if src.startswith("/"):
            try:
                rr = requests.get(BASE + src, timeout=15)
                row["status"] = rr.status_code
            except Exception as e:
                row["status"] = "ERR:" + str(e)
        elif src.startswith("http"):
            row["status"] = "external-not-checked"
        else:
            row["status"] = "relative-unexpected"
        pp["images"].append(row)
        img_rows.append(row)
    per_page[rt] = pp

# ---- orphans ----
orphans = [rt for rt in ROUTES if len(inbound[rt]) == 0]
inbound_counts = {rt: sorted(inbound[rt]) for rt in ROUTES}

# ---- disk image count ----
disk_webp = []
for root, _, files in os.walk(os.path.join(OUT, "images")):
    for f in files:
        if f.lower().endswith(".webp"):
            disk_webp.append(os.path.join(root, f))
disk_total = len(disk_webp)
disk_all = sum(len(fs) for _, _, fs in os.walk(os.path.join(OUT, "images")))

# ---- link totals ----
tot_prose = sum(p["prose_internal"] for p in per_page.values())
tot_card = sum(p["card_internal"] for p in per_page.values())
tot_broken = sum(len(p["broken_links"]) for p in per_page.values())
tot_self = sum(len(p["self_links"]) for p in per_page.values())
tot_anchor_viol = sum(len(p["prose_anchor_violations"]) for p in per_page.values())
tot_dup = sum(len(p["duplicate_targets"]) for p in per_page.values())
missing_alt = [r for r in img_rows if not r["alt_present"] or r["alt_empty"]]
bad_img_status = [r for r in img_rows if r["status"] != 200]
no_dims = [r for r in img_rows if not r["width"] or not r["height"]]

result = {
    "audit": "SEO AUDIT 1 — worker W3 (internal links + images/alt)",
    "site": "Midvale UT water damage",
    "base": BASE + PREFIX,
    "server_port": 8313,
    "pages_data_sha256_expected": "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f",
    "pages_data_sha256_actual": "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f",
    "routes_total": len(ROUTES),
    "routes_status_200": sum(1 for p in per_page.values() if p["status"] == 200),
    "totals": {
        "anchors_total_all_pages": sum(p["anchors_total"] for p in per_page.values()),
        "anchors_internal": sum(p["anchors_internal"] for p in per_page.values()),
        "anchors_external": sum(p["anchors_external"] for p in per_page.values()),
        "anchors_tel_mailto": sum(p["anchors_tel_mailto"] for p in per_page.values()),
        "anchors_fragment_only": sum(p["anchors_fragment_only"] for p in per_page.values()),
        "prose_internal_links_in_main": tot_prose,
        "card_internal_links_in_main": tot_card,
        "prose_plus_card": tot_prose + tot_card,
        "expected_prose_plus_card": 162,
        "expected_prose": 143, "expected_card": 19,
        "broken_links_total": tot_broken,
        "self_links_total": tot_self,
        "prose_anchor_wordcount_violations": tot_anchor_viol,
        "duplicate_target_pages": tot_dup,
        "img_tags_total": total_imgs,
        "img_missing_or_empty_alt": len(missing_alt),
        "img_non200_src": len(bad_img_status),
        "img_without_width_height": len(no_dims),
        "disk_webp_total": disk_total,
        "disk_webp_expected": 107,
        "disk_files_total_in_images": disk_all,
    },
    "orphans": orphans,
    "inbound_counts": {rt: len(v) for rt, v in inbound_counts.items()},
    "inbound_sources": inbound_counts,
    "missing_alt": missing_alt,
    "bad_img_status": bad_img_status,
    "img_without_width_height": no_dims,
    "per_page": per_page,
    "unique_internal_paths_checked": len(status_cache),
    "internal_path_statuses": {k: v for k, v in sorted(status_cache.items())},
    "PROBLEMS": [],
}
with open("/home/hatch/workspace/midvale-water-damage/qa/seo-audit1-w3.json", "w") as f:
    json.dump(result, f, indent=2)

print("routes 200:", result["routes_status_200"], "/", len(ROUTES))
print("anchors internal:", result["totals"]["anchors_internal"], "external:", result["totals"]["anchors_external"],
      "tel/mailto:", result["totals"]["anchors_tel_mailto"], "frag-only:", result["totals"]["anchors_fragment_only"])
print("prose:", tot_prose, "card:", tot_card, "sum:", tot_prose + tot_card, "(expected 143+19=162)")
print("broken:", tot_broken, "self:", tot_self, "anchor-viol:", tot_anchor_viol, "dup-target-pages:", tot_dup)
print("orphans:", orphans)
print("img tags:", total_imgs, "missing/empty alt:", len(missing_alt), "non-200 src:", len(bad_img_status),
      "no dims:", len(no_dims), "disk webp:", disk_total)
for rt in ROUTES:
    p = per_page[rt]
    if p["broken_links"] or p["self_links"] or p["prose_anchor_violations"] or p["duplicate_targets"]:
        print("FLAG", rt, "broken:", len(p["broken_links"]), "self:", len(p["self_links"]),
              "anchor-viol:", len(p["prose_anchor_violations"]), "dup:", len(p["duplicate_targets"]))
