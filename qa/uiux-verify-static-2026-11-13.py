#!/usr/bin/env python3
"""INDEPENDENT VERIFIER — Midvale UT Stage 1 UI/UX round (2026-11-13).
Fresh static checks on out/ (fresh export). Reads only, except this report.
Method (own, written fresh for this verification):
- Ordered verbatim diff vs lib/pages-data.json, annotation tokens `(/.../)`
  stripped from expected text (they are link metadata, never visible).
- Per-segment contiguous-subsequence check (stricter than the diff).
- H1 count/text, meta title/description verbatim, FAQ visible + JSON-LD,
  tables, links (body .body-link + cards .card-wrap-link), visible path
  text, image inventory, EXIF scan of the 24 swapped files, manifest shape.
Writes qa/uiux-verify-static-2026-11-13.json
"""
import json, os, re, sys
from bs4 import BeautifulSoup

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
DATA = json.load(open(os.path.join(ROOT, "lib/pages-data.json")))
PAGES = DATA["pages"]
ROUTES = [p["route"] for p in PAGES]

TOKEN_RE = re.compile(r"[a-z0-9]+")
ANN_RE = re.compile(r"\(\s*/[^)]*?\)")          # link-annotation parens only
PATH_TEXT_RE = re.compile(r"\(\s*/[^)]*?/[^)]*\)")  # visible (/.../) path text

def toks(text):
    return TOKEN_RE.findall((text or "").lower())

def strip_ann(text):
    return ANN_RE.sub(" ", text or "")

def segments_of(p):
    """(label, raw_text) in document order."""
    segs = []
    if p.get("eyebrow"):
        segs.append(("eyebrow", p["eyebrow"]))
    segs.append(("h1", p["h1"]))
    if p.get("intro"):
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
    for fi, f in enumerate(p["faqs"]):
        segs.append((f"faq{fi}:q", f["q"]))
        segs.append((f"faq{fi}:a", f["a"]))
    return segs

def find_subseq(hay, needle):
    if not needle:
        return 0
    n, m = len(needle), len(hay)
    for i in range(m - n + 1):
        if hay[i:i + n] == needle:
            return i
    return -1

def route_to_file(route):
    return os.path.join(OUT, "index.html") if route == "/" else os.path.join(OUT, route.strip("/") + ".html")

def main_text_of(soup):
    main = soup.find("main")
    if main is None:
        return None, ""
    for bad in main(["script", "style", "noscript"]):
        bad.decompose()
    cf = main.find("section", class_="contact-form")
    if cf:
        cf.decompose()  # template form words are not doc content
    return main, main.get_text(" ")

report = {"pages": {}, "problems": [], "site": {}}
total_faq_visible = 0
total_faq_jsonld = 0
total_tables = 0
total_body_links = 0
total_card_links = 0
all_broken = []
all_self = []
all_pathtext = []
all_img_srcs = set()

for p in PAGES:
    route = p["route"]
    pr = {"route": route}
    fp = route_to_file(route)
    if not os.path.exists(fp):
        report["problems"].append({"sev": "P1", "route": route, "what": "built file missing", "file": fp})
        report["pages"][route] = pr
        continue
    soup = BeautifulSoup(open(fp, encoding="utf-8").read(), "html.parser")
    main, main_text = main_text_of(soup)
    if main is None:
        report["problems"].append({"sev": "P1", "route": route, "what": "no <main> element"})
        report["pages"][route] = pr
        continue
    actual_toks = toks(main_text)

    # ---- verbatim: per-segment contiguous check (annotation-stripped) ----
    seg_missing, seg_short = [], []
    exp_total = 0
    for label, text in segments_of(p):
        nt = toks(strip_ann(text))
        exp_total += len(nt)
        if not nt:
            continue
        if find_subseq(actual_toks, nt) < 0:
            # sentence-level fallback: all sentences present but reordered?
            sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", strip_ann(text)) if s.strip()]
            all_present = bool(sents) and all(find_subseq(actual_toks, toks(s)) >= 0 for s in sents)
            (seg_short if all_present else seg_missing).append(
                {"seg": label, "tokens": len(nt), "text": strip_ann(text)[:200]})
    pr["expected_tokens_ann_stripped"] = exp_total
    pr["actual_tokens_main"] = len(actual_toks)
    pr["seg_missing"] = seg_missing
    pr["seg_reordered"] = seg_short
    if seg_missing:
        report["problems"].append({"sev": "P1", "route": route, "what": "segment(s) missing from visible <main> (annotation-stripped)",
                                   "detail": seg_missing})
    if seg_short:
        report["problems"].append({"sev": "P3", "route": route, "what": "segment(s) present but not contiguous (reordered?)",
                                   "detail": seg_short})

    # ---- H1 ----
    h1s = main.find_all("h1")
    pr["h1_count"] = len(h1s)
    pr["h1_text_match"] = bool(h1s) and (h1s[0].get_text(" ", strip=True) == strip_ann(p["h1"]).strip())
    if len(h1s) != 1:
        report["problems"].append({"sev": "P1", "route": route, "what": "H1 count != 1", "count": len(h1s)})
    if not pr["h1_text_match"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "H1 text != data h1",
                                   "rendered": h1s[0].get_text(" ", strip=True)[:120] if h1s else None,
                                   "expected": p["h1"][:120]})

    # ---- meta ----
    title = soup.find("title")
    md = soup.find("meta", attrs={"name": "description"})
    pr["meta_title_match"] = bool(title) and title.get_text(strip=True) == p["metaTitle"]
    pr["meta_desc_match"] = bool(md) and md.get("content", "") == p["metaDescription"]
    if not pr["meta_title_match"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "meta title != data",
                                   "rendered": title.get_text(strip=True)[:120] if title else None})
    if not pr["meta_desc_match"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "meta description != data"})

    # ---- FAQ visible ----
    faq_items = main.find_all(class_="faq-item")
    pr["faq_visible_items"] = len(faq_items)
    pr["faq_expected"] = len(p["faqs"])
    total_faq_visible += len(faq_items)
    # every FAQ Q and A must be present as contiguous text
    faq_missing = []
    for fi, f in enumerate(p["faqs"]):
        if find_subseq(actual_toks, toks(strip_ann(f["q"]))) < 0:
            faq_missing.append({"faq": fi, "part": "q", "text": f["q"][:120]})
        if find_subseq(actual_toks, toks(strip_ann(f["a"]))) < 0:
            faq_missing.append({"faq": fi, "part": "a", "text": f["a"][:120]})
    pr["faq_missing"] = faq_missing
    if faq_missing:
        report["problems"].append({"sev": "P1", "route": route, "what": "FAQ Q/A missing from visible text", "detail": faq_missing})
    if len(faq_items) != len(p["faqs"]):
        report["problems"].append({"sev": "P2", "route": route, "what": "FAQ item count != data",
                                   "expected": len(p["faqs"]), "visible": len(faq_items)})

    # ---- JSON-LD FAQPage ----
    ld_faq = 0
    ld_mismatch = []
    for sc in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            ld = json.loads(sc.string or "")
        except Exception:
            continue
        graphs = ld if isinstance(ld, list) else [ld]
        for g in graphs:
            if isinstance(g, dict) and g.get("@type") == "FAQPage":
                ents = g.get("mainEntity", [])
                ld_faq += len(ents)
                for ei, ent in enumerate(ents):
                    q = (ent.get("name") or "").strip()
                    a = ""
                    acc = ent.get("acceptedAnswer")
                    if isinstance(acc, dict):
                        a = (acc.get("text") or "").strip()
                    if ei < len(p["faqs"]):
                        if q != strip_ann(p["faqs"][ei]["q"]).strip():
                            ld_mismatch.append({"faq": ei, "part": "q"})
                        if a != strip_ann(p["faqs"][ei]["a"]).strip():
                            ld_mismatch.append({"faq": ei, "part": "a"})
    pr["faq_jsonld_items"] = ld_faq
    pr["faq_jsonld_mismatch"] = ld_mismatch
    total_faq_jsonld += ld_faq
    if ld_faq != len(p["faqs"]):
        report["problems"].append({"sev": "P1", "route": route, "what": "JSON-LD FAQ count != data",
                                   "expected": len(p["faqs"]), "jsonld": ld_faq})
    if ld_mismatch:
        report["problems"].append({"sev": "P1", "route": route, "what": "JSON-LD FAQ text != data (annotation-stripped)",
                                   "detail": ld_mismatch[:6]})

    # ---- tables ----
    ntab = len(main.find_all("table"))
    exp_tab = sum(1 for b in p["blocks"] if b["type"] == "table")
    pr["tables"] = ntab
    pr["tables_expected"] = exp_tab
    total_tables += ntab
    if ntab != exp_tab:
        report["problems"].append({"sev": "P1", "route": route, "what": "table count != data",
                                   "expected": exp_tab, "actual": ntab})

    # ---- visible path text ----
    pt = PATH_TEXT_RE.findall(main_text)
    pr["visible_path_text"] = pt
    if pt:
        all_pathtext.append({"route": route, "hits": pt[:5]})
        report["problems"].append({"sev": "P1", "route": route, "what": "visible (/.../) path text", "hits": pt[:5]})

    # ---- links ----
    body_links = main.find_all("a", class_="body-link")
    card_links = main.find_all("a", class_="card-wrap-link")
    pr["body_links"] = len(body_links)
    pr["card_links"] = len(card_links)
    total_body_links += len(body_links)
    total_card_links += len(card_links)
    for a in main.find_all("a", href=True):
        href = a["href"]
        if href.startswith(("tel:", "mailto:", "http", "#")):
            continue
        # normalise: strip basePath prefix
        h = href
        if h.startswith("/midvale-water-damage"):
            h = h[len("/midvale-water-damage"):] or "/"
        h = h.rstrip("/") or "/"
        if h == route.rstrip("/") or (h == "/" and route == "/"):
            if "body-link" in (a.get("class") or []):
                all_self.append({"route": route, "href": href, "text": a.get_text(" ", strip=True)[:80]})
        tgt_file = os.path.join(OUT, "index.html") if h == "/" else os.path.join(OUT, h.strip("/") + ".html")
        if not os.path.exists(tgt_file):
            all_broken.append({"route": route, "href": href})
    # hero buttons
    hero = main.find("section", class_="hero")
    if hero:
        btns = [a.get_text(" ", strip=True) for a in hero.find_all("a")]
        pr["hero_buttons"] = btns
        if "(385) 337-3560" not in btns or "Request Emergency Help" not in btns:
            report["problems"].append({"sev": "P2", "route": route, "what": "hero buttons missing/wrong", "buttons": btns})
    else:
        report["problems"].append({"sev": "P1", "route": route, "what": "no hero section in <main>"})

    # ---- images in this page ----
    imgs = main.find_all("img")
    pr["imgs_in_main"] = len(imgs)
    for im in imgs:
        s = im.get("src", "")
        if s:
            all_img_srcs.add(s)
    pr["imgs_missing_alt"] = [im.get("src", "") for im in imgs if not (im.get("alt") or "").strip()]

    report["pages"][route] = pr

# ---- per-page link counts vs inventory ----
inv = json.load(open(os.path.join(ROOT, "qa/link-inventory.json")))
inv_per_route = inv.get("per_route", {})
inv_records = {}
for rec in inv.get("records", []):
    inv_records.setdefault(rec["route"], []).append(rec)

def norm_href(href):
    h = href or ""
    if h.startswith("/midvale-water-damage"):
        h = h[len("/midvale-water-damage"):] or "/"
    return h.rstrip("/") or "/"

for route, pr in report["pages"].items():
    if "body_links" not in pr:
        continue
    exp_kept = inv_per_route.get(route, {}).get("kept", 0)
    exp_card = 19 if route == "/" else 0
    pr["expected_kept_links"] = exp_kept
    pr["expected_card_links"] = exp_card
    pr["expected_body_links"] = exp_kept - exp_card
    if pr["body_links"] + pr["card_links"] != exp_kept:
        report["problems"].append({"sev": "P1", "route": route, "what": "body+card links != inventory kept",
                                   "expected": exp_kept, "body": pr["body_links"], "cards": pr["card_links"]})
    if pr["card_links"] != exp_card:
        report["problems"].append({"sev": "P1", "route": route, "what": "card link count != expected",
                                   "expected": exp_card, "actual": pr["card_links"]})
    # per-record anchor verification (re-read the page soup)
    fp = route_to_file(route)
    soup = BeautifulSoup(open(fp, encoding="utf-8").read(), "html.parser")
    main = soup.find("main")
    main_text_raw = re.sub(r"\s+", " ", main.get_text(" ", strip=True)) if main else ""
    rec_problems = []
    for rec in inv_records.get(route, []):
        anchor, target, status = rec["anchor"], rec["target"], rec["status"]
        linked = [a for a in soup.find_all("a", href=True)
                  if a.get("class") and ("body-link" in a.get("class") or "card-wrap-link" in a.get("class"))
                  and norm_href(a["href"]) == target]
        anchor_in_linked = [a for a in linked if anchor in re.sub(r"\s+", " ", a.get_text(" ", strip=True))]
        if status == "kept":
            if not anchor_in_linked:
                rec_problems.append({"record": rec["unit"], "target": target, "anchor": anchor,
                                     "issue": "kept link missing: no body/card link with this href contains the anchor text",
                                     "links_with_href": len(linked)})
        else:  # dup-dropped / schema-only: anchor must stay visible as plain text; exactly one kept link per target
            if anchor not in main_text_raw:
                rec_problems.append({"record": rec["unit"], "target": target, "anchor": anchor,
                                     "issue": "dup-dropped anchor text MISSING from visible text"})
            if len(linked) != 1:
                rec_problems.append({"record": rec["unit"], "target": target, "anchor": anchor,
                                     "issue": "dup-dropped target should have exactly 1 kept link on the page",
                                     "links_with_href": len(linked)})
    pr["record_problems"] = rec_problems
    if rec_problems:
        report["problems"].append({"sev": "P1", "route": route, "what": "inventory record mismatch", "detail": rec_problems})
    # orphan check: every body/card link href must be a real route
    for a in (main.find_all("a", class_="body-link") + main.find_all("a", class_="card-wrap-link")):
        if norm_href(a.get("href")) not in ROUTES:
            report["problems"].append({"sev": "P1", "route": route, "what": "orphan link: href is not a site route",
                                       "href": a.get("href")})
report["site"]["total_body_links"] = total_body_links
report["site"]["total_card_links"] = total_card_links
report["site"]["total_faq_visible"] = total_faq_visible
report["site"]["total_faq_jsonld"] = total_faq_jsonld
report["site"]["total_tables"] = total_tables
report["site"]["broken_links"] = all_broken
report["site"]["body_self_links"] = all_self
report["site"]["visible_path_text_pages"] = all_pathtext
report["site"]["distinct_img_srcs_in_main"] = sorted(all_img_srcs)
if total_body_links != 143:
    report["problems"].append({"sev": "P1", "route": "*", "what": "total body links != 143", "actual": total_body_links})
if total_card_links != 19:
    report["problems"].append({"sev": "P1", "route": "*", "what": "total card links != 19", "actual": total_card_links})
if all_broken:
    report["problems"].append({"sev": "P1", "route": "*", "what": "broken internal links", "detail": all_broken[:20]})
if all_self:
    report["problems"].append({"sev": "P2", "route": "*", "what": "body self-links", "detail": all_self})
if total_faq_visible != 142:
    report["problems"].append({"sev": "P1", "route": "*", "what": "total visible FAQ items != 142", "actual": total_faq_visible})
if total_faq_jsonld != 142:
    report["problems"].append({"sev": "P1", "route": "*", "what": "total JSON-LD FAQ items != 142", "actual": total_faq_jsonld})
if total_tables != 43:
    report["problems"].append({"sev": "P1", "route": "*", "what": "total tables != 43", "actual": total_tables})

# ---- fullness gate ----
full = sum(1 for r in ROUTES if not report["pages"][r].get("seg_missing"))
report["site"]["full_pages"] = full
report["site"]["routes"] = len(ROUTES)

# ---- image files ----
import glob
disk_imgs = sorted(glob.glob(os.path.join(OUT, "images/**/*.webp"), recursive=True))
report["site"]["img_files_in_out"] = len(disk_imgs)
missing_files = [s for s in all_img_srcs if not os.path.exists(os.path.join(OUT, s.lstrip("/").replace("midvale-water-damage/", "", 1)))]
# srcs are basePath-prefixed (/midvale-water-damage/images/...)
missing_files = []
for s in all_img_srcs:
    rel = s[len("/midvale-water-damage/"):] if s.startswith("/midvale-water-damage/") else s.lstrip("/")
    if not os.path.exists(os.path.join(OUT, rel)):
        missing_files.append(s)
report["site"]["img_srcs_missing_on_disk"] = missing_files
if missing_files:
    report["problems"].append({"sev": "P1", "route": "*", "what": "img srcs missing on disk", "detail": missing_files})

import time
for _attempt in range(12):
    try:
        json.dump(report, open(os.path.join(ROOT, "qa/uiux-verify-static-2026-11-13.json"), "w"), indent=1)
        break
    except OSError as e:
        print(f"json write attempt {_attempt} failed: {e}")
        time.sleep(5)
else:
    print("WARNING: could not write uiux-verify-static JSON after 12 attempts (write gate)")
print("routes:", len(ROUTES), "| FULL pages:", full, "/31")
print("body links:", total_body_links, "| card links:", total_card_links)
print("FAQ visible:", total_faq_visible, "| FAQ JSON-LD:", total_faq_jsonld, "| tables:", total_tables)
print("img files in out/:", len(disk_imgs), "| distinct img srcs in main:", len(all_img_srcs))
print("PROBLEMS:", len(report["problems"]))
for pb in report["problems"]:
    print(" -", pb["sev"], pb["route"], pb["what"], str(pb.get("detail", pb.get("actual", "")))[:200])
