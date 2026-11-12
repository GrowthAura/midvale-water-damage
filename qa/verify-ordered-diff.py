#!/usr/bin/env python3
"""Ordered verbatim diff: expected content token sequence (from pages-data.json,
in document order) vs actual <main> visible token sequence (from built HTML).
Uses difflib to pinpoint exactly which sentences are missing/changed.
Reads only; writes qa/verify-ordered-diff.json.
"""
import json, re, os, difflib
from bs4 import BeautifulSoup
from collections import Counter

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
DATA = json.load(open(os.path.join(ROOT, "lib/pages-data.json")))
TOKEN_RE = re.compile(r"[a-z0-9]+(?:/[a-z0-9]+)*")

def toks(text):
    return TOKEN_RE.findall((text or "").lower())

def expected_seq(p):
    """Ordered list of (label, tokens) segments in document order."""
    segs = []
    if p.get("eyebrow"):
        segs.append(("eyebrow", toks(p["eyebrow"])))
    segs.append(("h1", toks(p["h1"])))
    segs.append(("intro", toks(p["intro"])))
    for i, ch in enumerate(p.get("trustChips") or []):
        segs.append((f"trustChip{i}", toks(ch)))
    for bi, b in enumerate(p["blocks"]):
        t = b["type"]
        if t in ("h2", "h3"):
            segs.append((f"block{bi}:{t}", toks(b["text"])))
        elif t == "p":
            segs.append((f"block{bi}:p", toks("".join(s["t"] for s in b["segments"]))))
        elif t in ("ul", "ol"):
            for ii, it in enumerate(b["items"]):
                segs.append((f"block{bi}:{t}[{ii}]", toks("".join(s["t"] for s in it["segments"]))))
        elif t == "table":
            segs.append((f"block{bi}:table-headers", toks(" ".join(b["headers"]))))
            for ri, r in enumerate(b["rows"]):
                segs.append((f"block{bi}:table-row{ri}", toks(" ".join(r))))
    for fi, f in enumerate(p["faqs"]):
        segs.append((f"faq{fi}:q", toks(f["q"])))
        segs.append((f"faq{fi}:a", toks(f["a"])))
    return segs

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
    segs = expected_seq(p)
    exp_flat = [t for _, ts in segs for t in ts]
    # segment boundaries in the flat expected sequence
    bounds = []
    pos = 0
    for label, ts in segs:
        bounds.append((label, pos, pos + len(ts)))
        pos += len(ts)
    sm = difflib.SequenceMatcher(a=exp_flat, b=actual, autojunk=False)
    # tokens in expected that are NOT matched (deletions)
    matched_exp = set()
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("equal",):
            matched_exp.update(range(i1, i2))
    # per-segment missing counts
    seg_missing = []
    for label, s, e in bounds:
        miss = sum(1 for i in range(s, e) if i not in matched_exp)
        if miss:
            seg_missing.append({"seg": label, "missing": miss, "total": e - s,
                                "text": " ".join(exp_flat[s:e])[:160]})
    # contiguous missing runs (for readable reporting)
    runs = []
    cur = None
    for i in range(len(exp_flat)):
        if i not in matched_exp:
            if cur is None:
                cur = [i, i]
            else:
                cur[1] = i
        else:
            if cur is not None:
                runs.append(tuple(cur))
                cur = None
    if cur is not None:
        runs.append(tuple(cur))
    run_texts = []
    for s, e in runs:
        if e - s + 1 >= 3:  # only runs of 3+ tokens
            run_texts.append({"tokens": e - s + 1, "text": " ".join(exp_flat[s:e + 1])[:220]})
    report[route] = {
        "expected_tokens": len(exp_flat),
        "actual_tokens": len(actual),
        "missing_tokens": len(exp_flat) - len(matched_exp),
        "seg_missing": seg_missing,
        "missing_runs_3plus": run_texts,
    }
    print(f"{route}: exp={len(exp_flat)} act={len(actual)} missing={len(exp_flat)-len(matched_exp)} segs_with_missing={len(seg_missing)} runs3+={len(run_texts)}")

json.dump(report, open(os.path.join(ROOT, "qa", "verify-ordered-diff.json"), "w"), indent=1)
print("---- detail: missing runs per page ----")
for route, r in report.items():
    if r["missing_runs_3plus"]:
        print(f"== {route} ==")
        for run in r["missing_runs_3plus"]:
            print(f"  [{run['tokens']} tok] {run['text']}")
