#!/usr/bin/env python3
"""CYCLE 1 INDEPENDENT RE-VERIFIER — static pass, Midvale UT.
Fresh reads only. Writes qa/reverify-static.json."""
import json, re, html, hashlib, urllib.request, urllib.error, os, subprocess
from collections import Counter
from pathlib import Path
from PIL import Image

ROOT = Path.home() / "workspace/midvale-water-damage"
OUT = ROOT / "out"
PUB = ROOT / "public"
BASE = "http://127.0.0.1:8410/midvale-water-damage"
SITE = "https://growthaura.github.io/midvale-water-damage"
EXPECTED_SHA = "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f"
problems = []
def add(sev, check, page, detail):
    problems.append({"severity": sev, "check": check, "page": page, "detail": detail})

sha = hashlib.sha256((ROOT/"lib/pages-data.json").read_bytes()).hexdigest()
assert sha == EXPECTED_SHA, f"DATA HASH MISMATCH {sha}"
data = json.loads((ROOT/"lib/pages-data.json").read_text())
pages = data["pages"]
assert len(pages) == 31

def route_file(r): return OUT/"index.html" if r=="/" else OUT/(r.strip("/")+".html")
def route_url(r): return SITE+"/" if r=="/" else SITE+r.rstrip("/")
def served(r): return BASE+"/" if r=="/" else BASE+r.rstrip("/")
def http_status(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as resp: return resp.status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return f"ERR:{e}"

def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s))
def norm_tokens(text):
    return re.findall(r"[a-z0-9']+", text.lower())

# ---------- IMAGES: PIL dims + weights + exiftool ----------
img = {}
heroes = sorted((PUB/"images/heroes").glob("*.webp"))
cards = sorted((PUB/"images/cards").glob("*.webp"))
body = sorted((PUB/"images/body").glob("*.webp"))
img["counts"] = {"heroes": len(heroes), "cards": len(cards), "body": len(body), "total": len(heroes)+len(cards)+len(body)}
img["weights"] = {"heroes": sum(f.stat().st_size for f in heroes),
                  "cards": sum(f.stat().st_size for f in cards),
                  "body": sum(f.stat().st_size for f in body)}
img["weights"]["total"] = sum(img["weights"].values())
def dims(files):
    out = {}
    for f in files:
        with Image.open(f) as im: out[f.name] = list(im.size)
    return out
img["hero_dims"] = dims(heroes)
img["card_dims"] = dims(cards)
img["body_dims"] = dims(body)
img["hero_dims_bad"] = {k:v for k,v in img["hero_dims"].items() if v != [1600,1066]}
img["card_dims_bad"] = {k:v for k,v in img["card_dims"].items() if v != [680,383]}
img["body_dims_bad"] = {k:v for k,v in img["body_dims"].items() if v != [800,450]}
if img["hero_dims_bad"]: add("P1","images-heroes-dims","-",str(img["hero_dims_bad"]))
if img["card_dims_bad"]: add("P1","images-cards-dims","-",str(img["card_dims_bad"]))
if img["body_dims_bad"]: add("P1","images-body-dims","-",str(img["body_dims_bad"]))
# exiftool over all 107 — only EXIF / XMP / ICC groups count as metadata
allimgs = heroes+cards+body
r = subprocess.run(["exiftool","-G","-j"]+[str(f) for f in allimgs], capture_output=True, text=True)
meta = {}
try:
    ej = json.loads(r.stdout)
    for e in ej:
        name = os.path.basename(e.get("SourceFile","?"))
        bad = [k for k in e.keys() if k.split(":")[0] in ("EXIF","XMP","ICC_Profile","IFD0","ExifIFD","GPS","MakerNotes","PrintIM") ]
        meta[name] = bad
except Exception as ex:
    meta = {"_parse_error": str(ex)}
img["metadata_leftover"] = {k:v for k,v in meta.items() if v}
if img["metadata_leftover"]: add("P2","images-metadata","-",str(img["metadata_leftover"])[:500])
# ---------- alt rewrites ----------
content_ts = (ROOT/"lib/content.ts").read_text()
body_imgs = json.loads((ROOT/"lib/body-images.json").read_text())
img["alt_burst_card"] = re.search(r"burst-pipe-water-damage.*?alt:\s*\"([^\"]+)\"", content_ts, re.S)
# find card alt near burst pipe: search all alt strings containing 'copper'
img["alt_burst_card_new"] = "Split copper pipe spraying water inside an opened wall cavity with wet wooden studs" in content_ts
img["alt_burst_card_old_gone"] = "Burst frozen pipe joint with ice and water spraying in a dark crawl space" not in content_ts
# body cottonwood-heights-ut-3 alt
b3 = None
for route, entries in (body_imgs.items() if isinstance(body_imgs, dict) else []):
    for e in entries:
        if isinstance(e, dict) and "cottonwood-heights-ut-3" in str(e.get("src",""))+str(e.get("file","")):
            b3 = e
img["body_images_keys"] = list(body_imgs.keys())[:5] if isinstance(body_imgs, dict) else type(body_imgs).__name__
img["cottonwood3_entry"] = b3
raw_bi = (ROOT/"lib/body-images.json").read_text()
img["alt_cotton_new"] = "Snowy city rooftops in the Salt Lake Valley with snow-capped mountains under low cloud" in raw_bi
img["alt_cotton_old_gone"] = "A snowy city street in Salt Lake City with snow-capped mountains in the background" not in raw_bi
if not img["alt_burst_card_new"]: add("P1","alt-burst-card","-","new card alt not found in lib/content.ts")
if not img["alt_cotton_new"]: add("P1","alt-cotton3","-","new cottonwood-3 alt not found in lib/body-images.json")
# new hero shas
img["new_hero_sha"] = {n: hashlib.sha256((PUB/f"images/heroes/{n}").read_bytes()).hexdigest()[:12] for n in ["disclaimer.webp","upstairs-unit-leak-who-pays-utah.webp","water-damage-repair.webp"]}
img["magna1_sha"] = hashlib.sha256((PUB/"images/body/magna-ut-1.webp").read_bytes()).hexdigest()[:12]
img["magna1_size"] = (PUB/"images/body/magna-ut-1.webp").stat().st_size

# ---------- per-page static ----------
per = {}
schema_counts = Counter()
schema_parse_err = 0
all_contenturls = []
id_refs_unresolved = []
for p in pages:
    route = p["route"]; f = route_file(route)
    raw = f.read_text()
    d = {}
    # robots meta
    m = re.search(r'<meta name="robots" content="([^"]+)"', raw)
    d["robots"] = m.group(1) if m else None
    # canonical / og
    cm = re.search(r'<link rel="canonical" href="([^"]+)"', raw)
    d["canonical"] = cm.group(1) if cm else None
    d["canonical_ok"] = d["canonical"] == route_url(route)
    # H1
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    d["h1_count"] = len(h1s)
    d["h1_text"] = strip_tags(h1s[0]).strip() if h1s else None
    d["h1_ok"] = d["h1_text"] == p["h1"] if h1s else False
    # hero img attrs
    hm = re.search(r'<img[^>]*id="hero-image"[^>]*>', raw)
    if not hm: hm = re.search(r'<img[^>]*class="hero-img"[^>]*>', raw)
    d["hero_img_tag"] = bool(hm)
    if hm:
        tag = hm.group(0)
        d["hero_width"] = re.search(r'width="(\d+)"', tag).group(1) if re.search(r'width="(\d+)"', tag) else None
        d["hero_height"] = re.search(r'height="(\d+)"', tag).group(1) if re.search(r'height="(\d+)"', tag) else None
        am = re.search(r'alt="([^"]*)"', tag); d["hero_alt"] = am.group(1) if am else None
        sm = re.search(r'src="([^"]+)"', tag); d["hero_src"] = sm.group(1) if sm else None
    d["has_breadcrumb_id"] = 'id="breadcrumb"' in raw
    d["has_hero_id"] = 'id="hero-image"' in raw
    d["has_service_id"] = 'id="service"' in raw
    d["howto_ids"] = sorted(set(re.findall(r'id="(howto-\d+)"', raw)))
    # JSON-LD
    blocks = []
    for jm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            blocks.append(json.loads(jm.group(1)))
        except Exception as e:
            schema_parse_err += 1
            add("P1","schema-parse",route,str(e)[:200])
    d["ld_blocks"] = len(blocks)
    types = []
    def walk(o):
        if isinstance(o, dict):
            if "@type" in o: types.append(o["@type"])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for b in blocks: walk(b)
    d["ld_types"] = Counter(types)
    for t in types: schema_counts[t] += 1
    # collect @ids defined and refs
    defined = set(); refs = set()
    def walk2(o):
        if isinstance(o, dict):
            if "@id" in o and isinstance(o["@id"], str):
                if len(o) == 1: refs.add(o["@id"])
                else: defined.add(o["@id"])
            for v in o.values(): walk2(v)
        elif isinstance(o, list):
            for v in o: walk2(v)
    for b in blocks: walk2(b)
    d["defined_ids"] = sorted(defined); d["ref_ids"] = sorted(refs)
    d["unresolved_refs"] = sorted(r for r in refs if r not in defined)
    if d["unresolved_refs"]:
        id_refs_unresolved.append((route, d["unresolved_refs"]))
        add("P1","schema-id-refs",route,str(d["unresolved_refs"]))
    for b in blocks:
        def walk3(o):
            if isinstance(o, dict):
                if o.get("@type") == "ImageObject" and "contentUrl" in o:
                    all_contenturls.append(o["contentUrl"])
                for v in o.values(): walk3(v)
            elif isinstance(o, list):
                for v in o: walk3(v)
        walk3(b)
    # main text / fullness / hidden
    mm = re.search(r"<main[^>]*>(.*?)</main>", raw, re.S)
    main_html = mm.group(1) if mm else ""
    main_text = strip_tags(main_html)
    d["main_words"] = len(norm_tokens(main_text))
    d["doc_words"] = p["counts"]["words"]
    # hidden words: elements with display:none / hidden attr / visibility:hidden inside main
    hidden = 0
    for hm2 in re.finditer(r'<[^>]+(?:style="[^"]*(?:display:\s*none|visibility:\s*hidden)[^"]*"| hidden)[^>]*>(.*?)</', main_html, re.S|re.I):
        hidden += len(norm_tokens(strip_tags(hm2.group(1))))
    d["hidden_words_est"] = hidden
    d["faq_visible"] = len(re.findall(r"<h3[^>]*>.*?</h3>", main_html, re.S))
    d["localhost"] = raw.count("localhost")
    d["double_slash_bad"] = len(re.findall(r'https?://growthaura\.github\.io//|(?<!:)//midvale-water-damage', raw))
    # links
    hrefs = re.findall(r'href="([^"]+)"', raw)
    d["href_count"] = len(hrefs)
    per[route] = d
    if d["robots"] != "index, follow": add("P1","robots-meta",route,str(d["robots"]))
    if not d["canonical_ok"]: add("P1","canonical",route,str(d["canonical"]))
    if d["h1_count"] != 1 or not d["h1_ok"]: add("P1","h1",route,f"count={d['h1_count']} ok={d['h1_ok']}")
    if d["hero_width"] != "1600" or d["hero_height"] != "1066": add("P1","hero-attrs",route,f"{d.get('hero_width')}x{d.get('hero_height')}")
    if not d["has_hero_id"]: add("P1","dom-hero-id",route,"missing #hero-image")

# site-wide @id resolution: #website is defined only on homepage
_all_defined = set()
for _v in per.values(): _all_defined.update(_v["defined_ids"])
_still_unresolved = [(r, sorted(x for x in v["ref_ids"] if x not in _all_defined)) for r, v in per.items()]
_still_unresolved = [(r, u) for r, u in _still_unresolved if u]
schema_unresolved_sitewide = _still_unresolved
# drop the per-page P1s for refs that resolve site-wide
problems[:] = [pr for pr in problems if not (pr["check"]=="schema-id-refs" and pr["detail"].strip("[]'") in str(_all_defined))]
if _still_unresolved: add("P1","schema-id-refs-sitewide","-",str(_still_unresolved))
schema = {"per_type": dict(schema_counts), "total_blocks": sum(schema_counts.values()),
          "parse_errors": schema_parse_err, "contenturls_total": len(all_contenturls),
          "contenturls_unique": len(set(all_contenturls)),
          "unresolved_refs": id_refs_unresolved}
# top-level @type counts (one per JSON-LD block)
_top = Counter()
for _p in pages:
    _raw = route_file(_p["route"]).read_text()
    for _jm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', _raw, re.S):
        try: _b = json.loads(_jm.group(1))
        except Exception: continue
        _items = _b if isinstance(_b, list) else [_b]
        for _it in _items:
            if isinstance(_it, dict) and "@type" in _it: _top[_it["@type"]] += 1
schema["top_level_types"] = dict(_top)
schema["top_level_total"] = sum(_top.values())
schema["unresolved_sitewide"] = schema_unresolved_sitewide
# contentUrl curl via local server (map SITE -> BASE)
cu_status = {}
for u in sorted(set(all_contenturls)):
    local = u.replace(SITE, BASE)
    cu_status[u] = http_status(local)
schema["contenturl_non200"] = {u:s for u,s in cu_status.items() if s != 200}
if schema["contenturl_non200"]: add("P1","schema-contenturl","-",str(schema["contenturl_non200"])[:500])
# hero ImageObject dims
hero_dims_schema = {}
for p in pages:
    raw = route_file(p["route"]).read_text()
    for jm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try: b = json.loads(jm.group(1))
        except Exception: continue
        def w(o):
            if isinstance(o, dict):
                if o.get("@type")=="ImageObject" and o.get("representativeOfPage"):
                    hero_dims_schema[p["route"]] = (o.get("width"), o.get("height"))
                for v in o.values(): w(v)
            elif isinstance(o, list):
                for v in o: w(v)
        w(b)
schema["hero_dims_schema"] = {k:list(v) for k,v in hero_dims_schema.items()}
schema["hero_dims_schema_bad"] = {k:v for k,v in hero_dims_schema.items() if v != (1600,1066)}
if schema["hero_dims_schema_bad"]: add("P1","schema-hero-dims","-",str(schema["hero_dims_schema_bad"]))

# ---------- sitemap / robots / 404 / global greps ----------
sm_raw = (OUT/"sitemap.xml").read_text()
locs = re.findall(r"<loc>(.*?)</loc>", sm_raw)
sm = {"loc_count": len(locs), "set_ok": sorted(set(locs))==sorted(route_url(p["route"]) for p in pages),
      "missing": sorted(set(route_url(p["route"]) for p in pages)-set(locs)),
      "extra": sorted(set(locs)-set(route_url(p["route"]) for p in pages))}
sm_status = {}
for loc in locs:
    path = loc[len(SITE):] or "/"
    sm_status[loc] = http_status(BASE+path)
sm["non200"] = {u:s for u,s in sm_status.items() if s!=200}
if sm["loc_count"]!=31 or not sm["set_ok"] or sm["non200"]: add("P1","sitemap","-",str(sm)[:400])
robots = (OUT/"robots.txt").read_text()
glob = {}
all_out = ""
for f in OUT.rglob("*"):
    if f.is_file() and f.suffix in (".html",".txt",".xml",".css",".js"):
        try: all_out += f.read_text(errors="ignore")
        except Exception: pass
glob["visible_paren"] = len(re.findall(r"\([^)]*?/[^)]*?\)", all_out))  # rough; refined below
glob["localhost_total"] = all_out.count("localhost")
glob["double_slash"] = len(re.findall(r"(?<!:)//midvale-water-damage", all_out))
glob["404_status"] = http_status(BASE+"/definitely-not-a-page-xyz")
# 404 page robots
nf = (OUT/"404.html").read_text()
glob["404_robots"] = re.search(r'<meta name="robots" content="([^"]+)"', nf).group(1) if re.search(r'<meta name="robots" content="([^"]+)"', nf) else None
if glob["404_robots"] != "noindex": add("P2","404-noindex","-",str(glob["404_robots"]))
if glob["404_status"] != 404: add("P2","404-status","-",str(glob["404_status"]))

# ---------- verbatim + fullness (token multiset, doc segments) ----------
def doc_tokens(p):
    toks = []
    toks += norm_tokens(p.get("h1","") or "")
    toks += norm_tokens(p.get("intro","") or "")
    def nt(s):
        return norm_tokens(re.sub(r"\(/[^)]*\)", " ", str(s)))
    for b in p.get("blocks", []):
        if isinstance(b, dict):
            if "text" in b: toks += nt(b["text"])
            for seg in b.get("segments", []):
                if isinstance(seg, dict): toks += nt(seg.get("t",""))
                elif isinstance(seg, str): toks += nt(seg)
            for row in b.get("rows", []) or []:
                for c in row: toks += nt(str(c))
            for cell in b.get("cells", []) or []: toks += nt(str(cell))
    for f in p.get("faqs", []):
        toks += nt(f.get("q","")); toks += nt(f.get("a",""))
    return toks
verb = {}
for p in pages:
    route = p["route"]; raw = route_file(route).read_text()
    mm = re.search(r"<main[^>]*>(.*?)</main>", raw, re.S)
    main_text = strip_tags(mm.group(1)) if mm else ""
    # remove template chrome? count missing doc tokens in main text multiset
    from collections import Counter as C
    doc = C(doc_tokens(p)); vis = C(norm_tokens(main_text))
    missing = sum((doc-vis).values())
    verb[route] = {"doc_tokens": sum(doc.values()), "main_words": len(vis), "missing_tokens": missing,
                   "missing_sample": list((doc-vis).elements())[:10]}
    if missing: add("P1","verbatim",route,f"missing {missing} tokens e.g. {verb[route]['missing_sample']}")
    # fullness: main words vs doc words (doc counts.words is content words)
    if len(vis) < 100: add("P1","fullness",route,f"main words {len(vis)}")

# FAQ counts
faq_total = sum(len(p.get("faqs",[])) for p in pages)
faq_schema_q = sum(per[r]["ld_types"].get("Question",0) for r in per)
verb["faq_total_doc"] = faq_total; verb["faq_schema_questions"] = faq_schema_q
tables_doc = sum(p["counts"].get("tables",0) for p in pages)

out = {"data_sha_ok": True, "images": img, "per_page": per, "schema": schema,
       "sitemap": sm, "robots_txt": robots, "global": glob, "verbatim": verb,
       "faq_total_doc": faq_total, "faq_schema_q": faq_schema_q, "tables_doc": tables_doc,
       "problems": problems}
(ROOT/"qa/reverify-static.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({"problems": problems, "schema": schema, "img_counts": img["counts"],
  "weights": img["weights"], "hero_bad": img["hero_dims_bad"], "card_bad": img["card_dims_bad"],
  "body_bad": img["body_dims_bad"], "meta_leftover": img["metadata_leftover"],
  "sitemap": sm, "global": glob, "faq": (faq_total, faq_schema_q), "tables_doc": tables_doc,
  "missing_total": sum(v.get("missing_tokens",0) for v in verb.values() if isinstance(v, dict)),
  "main_words_min": min(v["main_words"] for v in verb.values() if isinstance(v, dict)),
  "breadcrumb_ids": sum(1 for v in per.values() if v["has_breadcrumb_id"]),
  "hero_ids": sum(1 for v in per.values() if v["has_hero_id"]),
  "service_ids": sum(1 for v in per.values() if v["has_service_id"]),
  "alt_burst_new": img["alt_burst_card_new"], "alt_cotton_new": img["alt_cotton_new"],
  "cotton3": b3}, indent=1, default=str))
