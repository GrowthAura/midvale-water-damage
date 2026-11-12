#!/usr/bin/env python3
"""Segment-level verbatim check: every content segment from pages-data.json
(eyebrow, h1, intro, trust chips, each block, each table cell-row, each FAQ q/a)
must appear as a contiguous token subsequence in the page's <main> visible text.
Reports exactly which segments are absent or partial, with the break point.
Reads only; writes qa/verify-segments.json.
"""
import json, re, os
from bs4 import BeautifulSoup

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
DATA = json.load(open(os.path.join(ROOT, "lib/pages-data.json")))
TOKEN_RE = re.compile(r"[a-z0-9]+")

def toks(text):
    return TOKEN_RE.findall((text or "").lower())

def find_subseq(hay, needle):
    """Return start index of needle in hay, or -1. Empty needle -> 0."""
    n, m = len(hay), len(needle)
    if m == 0:
        return 0
    if m > n:
        return -1
    # naive with early exit; sequences are short
    first = needle[0]
    for i in range(n - m + 1):
        if hay[i] == first and hay[i:i + m] == needle:
            return i
    return -1

def longest_prefix_match(hay, needle):
    """Longest prefix of needle found as contiguous subsequence in hay."""
    best = 0
    for L in range(len(needle), 0, -1):
        if find_subseq(hay, needle[:L]) >= 0:
            return L
    return 0

def route_to_file(route):
    return os.path.join(OUT, "index.html") if route == "/" else os.path.join(OUT, route.strip("/") + ".html")

report = {}
for p in DATA["pages"]:
    route = p["route"]
    soup = BeautifulSoup(open(route_to_file(route), encoding="utf-8").read(), "html.parser")
    main = soup.find("main")
    for bad in main(["script", "style", "noscript"]):
        bad.decompose()
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
    for fi, f in enumerate(p["faqs"]):
        segs.append((f"faq{fi}:q", f["q"]))
        segs.append((f"faq{fi}:a", f["a"]))
    missing = []
    partial = []
    for label, text in segs:
        nt = toks(text)
        if find_subseq(actual, nt) >= 0:
            continue
        # try sentence-level: split into sentences, check each
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        sent_results = []
        all_present = True
        for s in sents:
            st = toks(s)
            present = find_subseq(actual, st) >= 0
            sent_results.append((s[:110], present, len(st)))
            if not present:
                all_present = False
        if all_present and sents:
            # whole segment not contiguous but every sentence present -> reordering only
            partial.append({"seg": label, "kind": "reordered (all sentences present, not contiguous)",
                            "tokens": len(nt), "text": text[:200]})
        else:
            miss_sents = [s for s, pr, _ in sent_results if not pr]
            missing.append({"seg": label, "tokens": len(nt),
                            "missing_sentences": miss_sents[:4],
                            "present_prefix_tokens": longest_prefix_match(actual, nt),
                            "text": text[:240]})
    report[route] = {
        "segments": len(segs),
        "missing_segments": len(missing),
        "partial_reordered": len(partial),
        "missing": missing,
        "partial": partial,
    }
    print(f"{route}: segs={len(segs)} missing={len(missing)} reordered={len(partial)}")

json.dump(report, open(os.path.join(ROOT, "qa", "verify-segments.json"), "w"), indent=1)
print("---- MISSING SEGMENTS ----")
for route, r in report.items():
    for m in r["missing"]:
        print(f"== {route} :: {m['seg']} ({m['tokens']} tok, prefix-match {m['present_prefix_tokens']}) ==")
        print("   TEXT:", m["text"][:200])
        for s in m["missing_sentences"]:
            print("   MISSING SENT:", s[:200])
    for pt in r["partial"]:
        print(f"-- {route} :: {pt['seg']} REORDERED ({pt['tokens']} tok): {pt['text'][:160]}")
