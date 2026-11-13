#!/usr/bin/env python3
"""INDEPENDENT link-fix verification for Midvale (2026-11-13).
TEST ONLY — reads lib/pages-data.json, qa/link-inventory.json, out/**.
Writes qa/verify-linkfix-static.json. Does NOT modify any site source file.
Verb accounting (LINKFIX): ` (/path/)` tokens are link metadata, NOT
content words. Expected visible tokens = data content tokens MINUS the
path tokens of every VISIBLE annotation on that route (inventory records
minus the 1 schema-only duplicate, which lives only in the faqs array
that expected_tokens() already excludes). Anchor words stay visible.
Segment check strips ` (/path/)` from expected segments before the
contiguous-subsequence search.
"""
import json, re, os, hashlib
from collections import Counter
from bs4 import BeautifulSoup

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
DATA = json.load(open(os.path.join(ROOT, "lib", "pages-data.json")))
PAGES = DATA["pages"]
INV = json.load(open(os.path.join(ROOT, "qa", "link-inventory.json")))
TOKEN_RE = re.compile(r"[a-z0-9]+")
PAREN_RE = re.compile(r" \(/[^)]*\)")
PAREN_ANY_RE = re.compile(r"\(/[^)]+/\)")
BASE = "/midvale-water-damage"

def toks(text):
    return TOKEN_RE.findall((text or "").lower())

def counter_of(texts):
    c = Counter()
    for t in texts:
        c.update(toks(t))
    return c

def strip_parens(text):
    return PAREN_RE.sub("", text or "")

def expected_tokens(p):
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
    return counter_of(parts)

def route_to_file(route):
    return os.path.join(OUT, "index.html") if route == "/" else os.path.join(OUT, route.strip("/") + ".html")

def visible_text(elem):
    for bad in elem(["script", "style", "noscript"]):
        bad.decompose()
    return elem.get_text(" ")

def norm_href(href):
    """Strip basePath prefix; return (target_route_or_None, kind)."""
    if href == BASE or href == BASE + "/" or href.startswith(BASE + "#") or href.startswith(BASE + "?"):
        return "/", "internal"
    if href.startswith(BASE + "/"):
        t = href[len(BASE):].split("#")[0].split("?")[0] or "/"
        return t, "internal"
    if href.startswith("/"):
        return href.split("#")[0].split("?")[0] or "/", "UNPREFIXED"
    if href.startswith(("http", "tel:", "mailto:", "#")):
        return None, "external-or-anchor"
    return href, "other"

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

# ---- annotation path tokens per route (visible records only) ----
path_tokens = {}   # route -> Counter of path tokens to subtract
inv_records = {}   # route -> [records]
for rec in INV["records"]:
    if "SCHEMA-ONLY" in rec.get("unit", ""):
        continue
    r = rec["route"]
    path_tokens.setdefault(r, Counter()).update(toks(rec["target"]))
    inv_records.setdefault(r, []).append(rec)
# sanity: visible annotation counts per route vs inventory per_route table
inv_per_route = INV["per_route"]

report = {"pages": {}, "site": {}, "problems": []}
data_sha = hashlib.sha256(open(os.path.join(ROOT, "lib", "pages-data.json"), "rb").read()).hexdigest()
report["site"]["pages_data_sha256"] = data_sha
if data_sha != "21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f":
    report["problems"].append({"sev": "P1", "what": "pages-data.json sha256 CHANGED vs rebuild-verified value", "sha": data_sha})

total_body_links = 0
total_card_links = 0
link_graph = {}
all_routes = set(p["route"] for p in PAGES)

for p in PAGES:
    route = p["route"]
    fpath = route_to_file(route)
    pr = {"route": route}
    html = open(fpath, encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    main_text_raw = main.get_text(" ") if main else ""

    # ---- Gate 1 static: paren pattern in visible main text ----
    pr["paren_in_main_visible_text"] = len(PAREN_ANY_RE.findall(main_text_raw))
    if pr["paren_in_main_visible_text"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "paren-path pattern in MAIN visible text",
                                    "count": pr["paren_in_main_visible_text"],
                                    "samples": PAREN_ANY_RE.findall(main_text_raw)[:3]})

    # ---- title / meta / h1 ----
    title = soup.title.get_text(strip=True) if soup.title else None
    pr["title_ok"] = (title == p["metaTitle"])
    md = soup.find("meta", attrs={"name": "description"})
    md_val = md["content"] if md and md.has_attr("content") else None
    pr["meta_ok"] = (md_val == p["metaDescription"])
    if not pr["title_ok"]:
        report["problems"].append({"sev": "P2", "route": route, "what": "title mismatch", "expected": p["metaTitle"], "actual": title})
    if not pr["meta_ok"]:
        report["problems"].append({"sev": "P2", "route": route, "what": "meta description mismatch", "expected": p["metaDescription"], "actual": md_val})
    h1s = main.find_all("h1") if main else []
    pr["h1_count"] = len(h1s)
    pr["h1_ok"] = (len(h1s) == 1 and h1s[0].get_text(" ", strip=True) == p["h1"])
    if not pr["h1_ok"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "H1 count/text wrong",
                                    "count": len(h1s), "expected": p["h1"],
                                    "actual": h1s[0].get_text(" ", strip=True) if h1s else None})

    # ---- tables ----
    data_tables = [b for b in p["blocks"] if b["type"] == "table"]
    rendered_tables = main.find_all("table") if main else []
    pr["tables_data"] = len(data_tables)
    pr["tables_rendered"] = len(rendered_tables)
    tc_mismatch = []
    for i, tb in enumerate(data_tables):
        if i >= len(rendered_tables):
            tc_mismatch.append(f"table {i} not rendered")
            continue
        cells = [c.get_text(" ", strip=True) for c in rendered_tables[i].find_all(["th", "td"])]
        # LINKFIX: table cells render via splitAnnotated — the ` (/path/)`
        # metadata is stripped; compare against stripped expected cells.
        exp_cells = [strip_parens(c) for c in list(tb["headers"]) + [c for r in tb["rows"] for c in r]]
        if cells != exp_cells:
            tc_mismatch.append({"table": i, "expected": exp_cells, "actual": cells})
    pr["table_cell_mismatch"] = tc_mismatch
    if tc_mismatch:
        report["problems"].append({"sev": "P1", "route": route, "what": "table content mismatch", "detail": tc_mismatch})

    # ---- FAQ schema vs visible (stripped answers) ----
    faq_visible = {}
    faq_sec = soup.find("section", id="faq")
    if faq_sec:
        for h in faq_sec.find_all("h3"):
            q = h.get_text(" ", strip=True)
            ans_parts = []
            for sib in h.next_siblings:
                if getattr(sib, "name", None) == "h3":
                    break
                if hasattr(sib, "get_text"):
                    ans_parts.append(sib.get_text(" ", strip=True))
            faq_visible[q] = " ".join(ans_parts).strip()
    ld_faq = []
    ld_parse_errors = 0
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(sc.string)
        except Exception:
            ld_parse_errors += 1
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
    pr["faq_data_count"] = len(p["faqs"])
    pr["faq_ld_count"] = len(ld_faq)
    pr["faq_visible_count"] = len(faq_visible)
    pr["ld_parse_errors"] = ld_parse_errors
    faq_mismatch = []
    for f in p["faqs"]:
        q, a = f["q"], f["a"]
        exp_a_toks = toks(strip_parens(a))
        hit = [x for x in ld_faq if x[0] == q]
        if not hit:
            faq_mismatch.append({"q": q, "issue": "not in FAQPage schema"})
        else:
            if toks(hit[0][1]) != exp_a_toks:
                faq_mismatch.append({"q": q, "issue": "schema answer != stripped data answer"})
            if PAREN_ANY_RE.search(hit[0][1] or ""):
                faq_mismatch.append({"q": q, "issue": "schema answer still contains paren-path"})
        vis = faq_visible.get(q)
        if vis is None:
            faq_mismatch.append({"q": q, "issue": "question not visible in #faq section"})
        elif toks(vis) != exp_a_toks:
            faq_mismatch.append({"q": q, "issue": "visible answer != stripped data answer"})
        if vis and PAREN_ANY_RE.search(vis):
            faq_mismatch.append({"q": q, "issue": "visible answer still contains paren-path"})
    pr["faq_mismatch"] = faq_mismatch
    if faq_mismatch:
        report["problems"].append({"sev": "P1", "route": route, "what": "FAQ schema/visible mismatch", "detail": faq_mismatch})
    if ld_parse_errors:
        report["problems"].append({"sev": "P2", "route": route, "what": "JSON-LD parse error(s)", "count": ld_parse_errors})

    # ---- verbatim multiset (annotation-adjusted) ----
    main_tokens = counter_of([visible_text(main)]) if main else Counter()
    expected = expected_tokens(p)
    expected_visible = expected - path_tokens.get(route, Counter())
    missing = expected_visible - main_tokens
    extra = main_tokens - expected_visible
    pr["main_words"] = sum(main_tokens.values())
    pr["expected_words_raw"] = sum(expected.values())
    pr["annotation_path_tokens_subtracted"] = sum(path_tokens.get(route, Counter()).values())
    pr["expected_words_visible"] = sum(expected_visible.values())
    pr["missing_words"] = sum(missing.values())
    pr["extra_words"] = sum(extra.values())
    pr["missing_detail"] = dict(missing.most_common(40))
    pr["extra_detail"] = dict(extra.most_common(40))
    pr["fullness"] = "FULL" if pr["main_words"] >= 300 else ("THIN" if pr["main_words"] >= 100 else "EMPTY")
    if pr["fullness"] != "FULL":
        report["problems"].append({"sev": "P1", "route": route, "what": f"fullness gate {pr['fullness']}", "main_words": pr["main_words"]})
    if missing:
        report["problems"].append({"sev": "P1", "route": route, "what": "content words missing from render (annotation-adjusted)",
                                    "count": sum(missing.values()), "sample": dict(missing.most_common(20))})

    # ---- segment-level verbatim (annotations stripped from expected) ----
    actual_toks = toks(main.get_text(" ")) if main else []
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
    for fi, f in enumerate(p["faqs"]):
        segs.append((f"faq{fi}:q", f["q"]))
        segs.append((f"faq{fi}:a", f["a"]))
    seg_missing = []
    seg_reordered = []
    for label, text in segs:
        nt = toks(strip_parens(text))
        if find_subseq(actual_toks, nt) >= 0:
            continue
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", strip_parens(text)) if s.strip()]
        all_present = bool(sents) and all(find_subseq(actual_toks, toks(s)) >= 0 for s in sents)
        if all_present:
            seg_reordered.append({"seg": label, "kind": "reordered (all sentences present)", "tokens": len(nt), "text": text[:200]})
        else:
            miss_sents = [s[:160] for s in sents if find_subseq(actual_toks, toks(s)) < 0][:4]
            seg_missing.append({"seg": label, "tokens": len(nt), "missing_sentences": miss_sents, "text": text[:240]})
    pr["segments"] = len(segs)
    pr["seg_missing"] = seg_missing
    pr["seg_reordered"] = seg_reordered
    if seg_missing:
        report["problems"].append({"sev": "P1", "route": route, "what": "segment(s) missing from render (annotation-stripped)",
                                    "detail": seg_missing})
    if seg_reordered:
        report["problems"].append({"sev": "P3", "route": route, "what": "segment(s) reordered (all sentences present, not contiguous)",
                                    "detail": seg_reordered})

    # ---- links ----
    body_links = soup.find_all("a", class_="body-link")
    card_links = soup.find_all("a", class_="card-wrap-link")
    pr["body_link_count"] = len(body_links)
    pr["card_link_count"] = len(card_links)
    total_body_links += len(body_links)
    total_card_links += len(card_links)
    page_targets = set()
    broken = []
    self_links_body = []
    unprefixed = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        tgt, kind = norm_href(href)
        if kind == "UNPREFIXED":
            unprefixed.append(href)
        if tgt is None:
            continue
        page_targets.add(tgt)
        inside_main = main and a in main.find_all("a")
        inside_nav = a.find_parent("nav") is not None
        if inside_main and not inside_nav and tgt == route:
            # body self-link: exclude breadcrumb (inside nav) and card links are not self here
            self_links_body.append({"href": href, "text": a.get_text(" ", strip=True)[:80],
                                    "class": a.get("class")})
        if kind == "internal":
            fp = os.path.join(OUT, "index.html") if tgt == "/" else os.path.join(OUT, tgt.strip("/") + ".html")
            if not os.path.exists(fp):
                broken.append(tgt)
    pr["self_links_body"] = self_links_body
    pr["broken_internal_links"] = sorted(set(broken))
    pr["unprefixed_hrefs"] = sorted(set(unprefixed))
    if self_links_body:
        report["problems"].append({"sev": "P2", "route": route, "what": "body self-link(s)", "detail": self_links_body})
    if broken:
        report["problems"].append({"sev": "P1", "route": route, "what": "broken internal link(s)", "detail": sorted(set(broken))})
    if unprefixed:
        report["problems"].append({"sev": "P1", "route": route, "what": "unprefixed root-relative href(s)", "detail": sorted(set(unprefixed))})
    link_graph[route] = page_targets

    # ---- per-record anchor verification ----
    rec_problems = []
    for rec in inv_records.get(route, []):
        anchor = rec["anchor"]
        target = rec["target"]
        status = rec["status"]
        # candidate links: body-link or card-wrap-link with this href
        linked = [a for a in soup.find_all("a", href=True)
                  if a.get("class") and ("body-link" in a.get("class") or "card-wrap-link" in a.get("class"))
                  and norm_href(a["href"])[0] == target]
        anchor_in_linked = [a for a in linked
                            if anchor in re.sub(r"\s+", " ", a.get_text(" ", strip=True))]
        if status == "kept":
            if not anchor_in_linked:
                rec_problems.append({"record": rec["unit"], "target": target, "anchor": anchor,
                                     "issue": "kept link missing: no body/card link with this href contains the anchor text",
                                     "links_with_href": len(linked)})
        else:  # dup-dropped
            # NOTE: the kept link for the same target legitimately contains
            # the same anchor text, so a site-wide "is the anchor linked"
            # test cannot distinguish the two occurrences. The dup occurrence
            # itself is checked by the targeted plain_text_check() below
            # (finds the exact <p>/<li> by its distinctive surrounding
            # text and asserts no body-link inside it). Here only check the
            # anchor text still appears as visible plain text.
            if anchor not in re.sub(r"\s+", " ", main_text_raw):
                rec_problems.append({"record": rec["unit"], "target": target, "anchor": anchor,
                                     "issue": "dup-dropped anchor text MISSING from visible text"})
    pr["record_problems"] = rec_problems
    if rec_problems:
        report["problems"].append({"sev": "P1", "route": route, "what": "inventory record mismatch", "detail": rec_problems})

    # ---- per-page link counts vs inventory ----
    exp_kept = inv_per_route.get(route, {}).get("kept", 0)
    exp_card = 19 if route == "/" else 0
    exp_body = exp_kept - exp_card
    pr["expected_body_links"] = exp_body
    pr["expected_card_links"] = exp_card
    if len(body_links) != exp_body:
        report["problems"].append({"sev": "P1", "route": route, "what": "body-link count != inventory kept-minus-cards",
                                    "expected": exp_body, "actual": len(body_links)})
    if len(card_links) != exp_card:
        report["problems"].append({"sev": "P1", "route": route, "what": "card-wrap-link count != expected",
                                    "expected": exp_card, "actual": len(card_links)})

    # ---- hero buttons ----
    hero = main.find("section", class_="hero") if main else None
    if hero:
        btns = [a.get_text(" ", strip=True) for a in hero.find_all("a") if a.find_parent("nav") is None]
        pr["hero_buttons"] = btns
        if "(385) 337-3560" not in btns or "Request Emergency Help" not in btns:
            report["problems"].append({"sev": "P2", "route": route, "what": "hero buttons missing/wrong", "buttons": btns})
    else:
        report["problems"].append({"sev": "P1", "route": route, "what": "no hero section in main"})

    report["pages"][route] = pr

# ---- homepage cards (Gate 4) ----
home = BeautifulSoup(open(route_to_file("/"), encoding="utf-8").read(), "html.parser")
cards = home.find_all("article", class_="card")
report["site"]["homepage_cards"] = len(cards)
card_problems = []
for i, c in enumerate(cards):
    links = c.find_all("a")
    if len(links) != 1:
        card_problems.append({"card": i, "issue": f"{len(links)} <a> elements (expected exactly 1)"})
        continue
    a = links[0]
    if "card-wrap-link" not in (a.get("class") or []):
        card_problems.append({"card": i, "issue": "single link is not .card-wrap-link", "class": a.get("class")})
    if not a.find("img"):
        card_problems.append({"card": i, "issue": "no <img> inside card link"})
    if not (a.find("h3") or a.find("strong")):
        card_problems.append({"card": i, "issue": "no <h3>/<strong> inside card link"})
    if not a.find("p"):
        card_problems.append({"card": i, "issue": "no <p> summary inside card link"})
    nested = a.find_all("a")
    if nested:
        card_problems.append({"card": i, "issue": "nested <a> inside card link"})
report["site"]["card_problems"] = card_problems
if len(cards) != 19:
    report["problems"].append({"sev": "P1", "what": "homepage card count != 19", "actual": len(cards)})
if card_problems:
    report["problems"].append({"sev": "P1", "what": "homepage card structure problem(s)", "detail": card_problems})

# ---- dup-dropped targeted checks (Gate 3) ----
def plain_text_check(route, distinctive, label):
    soup = BeautifulSoup(open(route_to_file(route), encoding="utf-8").read(), "html.parser")
    main = soup.find("main")
    hit = None
    for el in main.find_all(["p", "li"]):
        if distinctive in el.get_text(" ", strip=True):
            hit = el
            break
    if hit is None:
        report["problems"].append({"sev": "P1", "route": route, "what": f"dup-drop context not found: {label}"})
        return
    if hit.find("a", class_="body-link"):
        report["problems"].append({"sev": "P1", "route": route, "what": f"dup-dropped anchor IS a body-link: {label}"})
    else:
        report["site"].setdefault("dup_drop_plain_ok", []).append(label)

plain_text_check("/", "If water came from an upstairs unit", "homepage Condo sentence")
plain_text_check("/water-heater-leak-cleanup", "Hardwood boards cupping at the edges", "water-heater blocks[36] ul[1]")

# ---- orphans (whole-page link graph incl. header/footer) ----
linked_to = Counter()
for src, tgts in link_graph.items():
    for t in tgts:
        if t != src:
            linked_to[t] += 1
orphans = [r for r in all_routes if linked_to.get(r, 0) == 0]
report["site"]["orphans"] = orphans
report["site"]["linked_to_counts"] = {r: linked_to.get(r, 0) for r in sorted(all_routes)}
if orphans:
    report["problems"].append({"sev": "P2", "what": "orphan route(s)", "routes": orphans})

# ---- footer links ----
footer = home.find("footer")
foot_navs = {}
if footer:
    for nav in footer.find_all("nav"):
        label = nav.get("aria-label")
        foot_navs[label] = [(a.get_text(" ", strip=True), a.get("href")) for a in nav.find_all("a", href=True)]
report["site"]["footer_navs"] = {k: len(v) for k, v in foot_navs.items()}
about_res = foot_navs.get("About and resources", [])
if len(about_res) != 10:
    report["problems"].append({"sev": "P2", "what": "footer About & Resources link count != 10", "actual": len(about_res), "links": about_res})
else:
    exp_footer = ["/about", "/contact", "/privacy-policy", "/terms-of-use", "/disclaimer",
                  "/resources/frozen-pipes-midvale", "/resources/winterize-swamp-cooler-utah",
                  "/resources/upstairs-unit-leak-who-pays-utah", "/resources/can-mold-grow-in-utah",
                  "/resources/basement-flooding-spring-snowmelt-utah"]
    got = [norm_href(h)[0] for _, h in about_res]
    if got != exp_footer:
        report["problems"].append({"sev": "P2", "what": "footer About & Resources hrefs differ", "expected": exp_footer, "actual": got})

# ---- Gate 1 static: paren pattern across out/ files ----
paren_hits = []
for dp, _, fns in os.walk(OUT):
    for fn in fns:
        pth = os.path.join(dp, fn)
        rel = os.path.relpath(pth, OUT)
        if fn.endswith((".html", ".txt", ".xml", ".css")):
            txt = open(pth, encoding="utf-8", errors="ignore").read()
            for m in PAREN_ANY_RE.finditer(txt):
                paren_hits.append({"file": rel, "match": m.group(0)[:80],
                                   "context": txt[max(0, m.start()-60):m.end()+60].replace("\n", " ")})
        elif fn.endswith(".js"):
            data = open(pth, "rb").read()
            # search raw bytes for the pattern
            for m in re.finditer(rb"\(/[^)]+/\)", data):
                paren_hits.append({"file": rel, "match": m.group(0)[:80].decode("utf-8", "ignore"),
                                   "context": data[max(0, m.start()-80):m.end()+80].decode("utf-8", "ignore")})
        elif fn.endswith(".webp"):
            data = open(pth, "rb").read()
            for m in re.finditer(rb"\(/[^)]+/\)", data):
                paren_hits.append({"file": rel, "match": m.group(0)[:80].decode("utf-8", "ignore"),
                                   "context": "BINARY webp bytes"})
report["site"]["paren_pattern_hits_out"] = paren_hits
html_txt_xml_css_hits = [h for h in paren_hits if h["file"].endswith((".html", ".txt", ".xml", ".css"))]
if html_txt_xml_css_hits:
    report["problems"].append({"sev": "P1", "what": "paren-path pattern in out/ HTML/TXT/XML/CSS", "detail": html_txt_xml_css_hits})
report["site"]["paren_js_webp_hits"] = [h for h in paren_hits if not h["file"].endswith((".html", ".txt", ".xml", ".css"))]

# ---- totals ----
report["site"]["total_body_links"] = total_body_links
report["site"]["total_card_links"] = total_card_links
report["site"]["total_kept_links"] = total_body_links + total_card_links
report["site"]["expected_total_kept"] = INV["totals"]["kept_links"]
report["site"]["expected_body"] = 143
report["site"]["expected_card"] = 19
if total_body_links != 143:
    report["problems"].append({"sev": "P1", "what": "total body-link count != 143", "actual": total_body_links})
if total_card_links != 19:
    report["problems"].append({"sev": "P1", "what": "total card-wrap-link count != 19", "actual": total_card_links})
report["site"]["total_missing_words"] = sum(pr["missing_words"] for pr in report["pages"].values())
report["site"]["total_extra_words"] = sum(pr["extra_words"] for pr in report["pages"].values())
report["site"]["total_main_words"] = sum(pr["main_words"] for pr in report["pages"].values())
report["site"]["total_expected_visible_words"] = sum(pr["expected_words_visible"] for pr in report["pages"].values())
report["site"]["total_annotation_path_tokens"] = sum(pr["annotation_path_tokens_subtracted"] for pr in report["pages"].values())
report["site"]["total_faq_data"] = sum(pr["faq_data_count"] for pr in report["pages"].values())
report["site"]["total_faq_ld"] = sum(pr["faq_ld_count"] for pr in report["pages"].values())
report["site"]["total_tables_data"] = sum(pr["tables_data"] for pr in report["pages"].values())
report["site"]["total_tables_rendered"] = sum(pr["tables_rendered"] for pr in report["pages"].values())
report["site"]["fullness"] = {r: pr["fullness"] for r, pr in report["pages"].items()}

# ---- sitemap / robots / llms ----
sm = open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", sm)
report["site"]["sitemap_locs"] = len(locs)
report["site"]["sitemap_lastmods"] = sorted(set(lastmods))
exp_locs = {"http://localhost:3000" + ("/" if r == "/" else r) for r in all_routes}
if set(locs) != exp_locs:
    report["problems"].append({"sev": "P1", "what": "sitemap loc set != 31 routes", "missing": sorted(exp_locs - set(locs)), "extra": sorted(set(locs) - exp_locs)})
robots = open(os.path.join(OUT, "robots.txt"), encoding="utf-8").read()
if "Host:" in robots:
    report["problems"].append({"sev": "P2", "what": "robots.txt contains Host: line"})
if "Allow: /" not in robots:
    report["problems"].append({"sev": "P2", "what": "robots.txt missing Allow: /"})
llms = open(os.path.join(OUT, "llms.txt"), encoding="utf-8").read()
llms_urls = [l.strip() for l in llms.splitlines() if l.strip().startswith("http")]
report["site"]["llms_url_count"] = len(llms_urls)
if set(llms_urls) != exp_locs:
    report["problems"].append({"sev": "P2", "what": "llms.txt URL set != 31 routes", "missing": sorted(exp_locs - set(llms_urls)), "extra": sorted(set(llms_urls) - exp_locs)})

# ---- grep gates on built HTML ----
double_slash = 0
unpref = 0
for dp, _, fns in os.walk(OUT):
    for fn in fns:
        if not fn.endswith(".html"):
            continue
        h = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
        double_slash += h.count("//midvale-water-damage")
        for m in re.finditer(r'(?:href|src)="(/[^"]*)"', h):
            if not m.group(1).startswith("/midvale-water-damage"):
                unpref += 1
report["site"]["grep_double_slash"] = double_slash
report["site"]["grep_unprefixed_href_src"] = unpref
if double_slash:
    report["problems"].append({"sev": "P1", "what": "double-slash prefix in built HTML", "count": double_slash})
if unpref:
    report["problems"].append({"sev": "P1", "what": "unprefixed root-relative href/src in built HTML", "count": unpref})

json.dump(report, open(os.path.join(ROOT, "qa", "verify-linkfix-static.json"), "w"), indent=1)
print(f"pages: {len(report['pages'])}  problems: {len(report['problems'])}")
for prob in report["problems"]:
    print(" -", prob["sev"], prob.get("route", ""), prob["what"], str(prob.get("detail", prob.get("sample", prob.get("actual", ""))))[:200])
print(f"body-links={total_body_links} card-links={total_card_links} kept-total={total_body_links + total_card_links}")
print(f"missing words total={report['site']['total_missing_words']} extra={report['site']['total_extra_words']} main={report['site']['total_main_words']} expected-visible={report['site']['total_expected_visible_words']} path-tokens-subtracted={report['site']['total_annotation_path_tokens']}")
print(f"FAQ data={report['site']['total_faq_data']} ld={report['site']['total_faq_ld']} tables={report['site']['total_tables_data']}/{report['site']['total_tables_rendered']}")
print(f"orphans={orphans} footer-navs={report['site']['footer_navs']}")
print(f"paren hits in out/: html/txt/xml/css={len(html_txt_xml_css_hits)} js/webp={len(report['site']['paren_js_webp_hits'])}")
for h in report["site"]["paren_js_webp_hits"]:
    print("   JS/WEBP:", h["file"], repr(h["match"]), "|", h["context"][:160])
print("--- per page ---")
for r, pr in report["pages"].items():
    print(f"{r}: main={pr['main_words']} expVis={pr['expected_words_visible']} miss={pr['missing_words']} extra={pr['extra_words']} full={pr['fullness']} body={pr['body_link_count']}/{pr['expected_body_links']} card={pr['card_link_count']}/{pr['expected_card_links']} segMiss={len(pr['seg_missing'])} segReord={len(pr['seg_reordered'])} faq={pr['faq_ld_count']}/{pr['faq_data_count']} h1={pr['h1_ok']} title={pr['title_ok']} meta={pr['meta_ok']}")
