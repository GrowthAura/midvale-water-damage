#!/usr/bin/env python3
"""Independent FAQPage JSON-LD check (fresh, 2026-11-13 Stage 1 verifier).
Parses RAW html with regex — no BeautifulSoup decompose — so scripts inside
<main> are not destroyed. Compares FAQPage mainEntity count + Q/A text
against lib/pages-data.json (annotation-stripped).
Writes qa/uiux-faqld-2026-11-13.json
"""
import json, os, re

ROOT = os.path.expanduser("~/workspace/midvale-water-damage")
OUT = os.path.join(ROOT, "out")
DATA = json.load(open(os.path.join(ROOT, "lib/pages-data.json")))
ANN_RE = re.compile(r"\(\s*/[^)]*?\)")

def strip_ann(t):
    return ANN_RE.sub(" ", t or "").strip()

def route_to_file(route):
    return os.path.join(OUT, "index.html") if route == "/" else os.path.join(OUT, route.strip("/") + ".html")

report = {"pages": {}, "problems": [], "site": {"total_faq_jsonld": 0, "total_expected": 0}}
for p in DATA["pages"]:
    route = p["route"]
    html = open(route_to_file(route), encoding="utf-8").read()
    pr = {"expected": len(p["faqs"]), "jsonld": 0, "mismatch": []}
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            ld = json.loads(m.group(1))
        except Exception as e:
            pr["mismatch"].append({"parse_fail": str(e)[:100]})
            continue
        graphs = ld if isinstance(ld, list) else [ld]
        for g in graphs:
            if isinstance(g, dict) and g.get("@type") == "FAQPage":
                ents = g.get("mainEntity", [])
                pr["jsonld"] += len(ents)
                for ei, ent in enumerate(ents):
                    q = (ent.get("name") or "").strip()
                    acc = ent.get("acceptedAnswer")
                    a = (acc.get("text") or "").strip() if isinstance(acc, dict) else ""
                    if ei < len(p["faqs"]):
                        if q != strip_ann(p["faqs"][ei]["q"]):
                            pr["mismatch"].append({"faq": ei, "part": "q"})
                        if a != strip_ann(p["faqs"][ei]["a"]):
                            pr["mismatch"].append({"faq": ei, "part": "a"})
    report["site"]["total_faq_jsonld"] += pr["jsonld"]
    report["site"]["total_expected"] += pr["expected"]
    if pr["jsonld"] != pr["expected"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "FAQPage count != data",
                                   "expected": pr["expected"], "jsonld": pr["jsonld"]})
    if pr["mismatch"]:
        report["problems"].append({"sev": "P1", "route": route, "what": "FAQPage text mismatch",
                                   "detail": pr["mismatch"][:6]})
    report["pages"][route] = pr

json.dump(report, open(os.path.join(ROOT, "qa/uiux-faqld-2026-11-13.json"), "w"), indent=1)
print("FAQPage total:", report["site"]["total_faq_jsonld"], "| expected:", report["site"]["total_expected"])
print("PROBLEMS:", len(report["problems"]))
for pb in report["problems"]:
    print(" -", pb["sev"], pb["route"], pb["what"], str(pb.get("detail", ""))[:200])
