#!/usr/bin/env python3
"""Segment-level verbatim check: every unique doc segment must appear verbatim
(normalised) in the VISIBLE main text (scripts/styles stripped). Writes qa/reverify-segments.json."""
import json, re, html
from pathlib import Path

ROOT = Path.home() / "workspace/midvale-water-damage"
OUT = ROOT / "out"
data = json.loads((ROOT / "lib/pages-data.json").read_text())
pages = data["pages"]

def norm(s):
    s = html.unescape(str(s)).lower()
    s = re.sub(r"\([^)]*?/[^)]*?\)", " ", s)  # strip link annotations (/path/)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def route_file(r): return OUT / "index.html" if r == "/" else OUT / (r.strip("/") + ".html")

def visible_main_text(raw):
    m = re.search(r"<main[^>]*>(.*?)</main>", raw, re.S)
    h = m.group(1) if m else ""
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return norm(t)

problems = []
res = {}
total_segs = 0; total_missing = 0
for p in pages:
    route = p["route"]; raw = route_file(route).read_text()
    vis = visible_main_text(raw)
    segs = []  # (kind, text)
    segs.append(("h1", p.get("h1", "")))
    segs.append(("intro", p.get("intro", "")))
    for b in p.get("blocks", []):
        if b.get("type") in ("h2", "h3"):
            segs.append((b["type"], b.get("text", "")))
        elif b.get("type") == "p":
            for s in b.get("segments", []):
                segs.append(("p", s.get("t", "") if isinstance(s, dict) else str(s)))
        elif b.get("type") in ("ul", "ol"):
            for it in b.get("items", []):
                if isinstance(it, dict):
                    segs.append((b["type"], " ".join(s.get("t","") for s in it.get("segments", []))))
                else:
                    segs.append((b["type"], str(it)))
        elif b.get("type") == "table":
            for hcell in b.get("headers", []): segs.append(("th", hcell))
            for row in b.get("rows", []):
                for c in row: segs.append(("td", c))
    for f in p.get("faqs", []):
        segs.append(("faq-q", f.get("q", "")))
        segs.append(("faq-a", f.get("a", "")))
    # dedupe by normalised text (FAQ content also appears as blocks)
    seen = {}
    for kind, t in segs:
        n = norm(t)
        if len(n) < 3: continue
        seen.setdefault(n, kind)
    missing = []
    for n, kind in seen.items():
        if n not in vis:
            missing.append((kind, n[:120]))
    total_segs += len(seen); total_missing += len(missing)
    res[route] = {"segments_unique": len(seen), "missing": len(missing),
                  "missing_sample": missing[:6],
                  "visible_main_words": len(vis.split())}
    if missing:
        problems.append({"severity": "P1", "check": "verbatim-segment", "page": route,
                         "detail": f"{len(missing)} segments missing: {missing[:3]}"})
out = {"per_page": res, "total_segments": total_segs, "total_missing": total_missing,
       "problems": problems}
(ROOT / "qa/reverify-segments.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1)[:4000])
print("TOTAL segments:", total_segs, "missing:", total_missing)
