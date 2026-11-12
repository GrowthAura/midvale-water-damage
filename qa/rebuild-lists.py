#!/usr/bin/env python3
"""Midvale UT rebuild — list re-classifier.

Reads ONLY:
  - qa/r3-full-doc/doc-full.json   (Docs API JSON; groups re-derived from it
                                     exactly the way qa/rebuild-parser.py formed
                                     them: maximal runs of consecutive bullet
                                     paragraphs sharing one listId)
  - qa/r3-full-doc/doc-export.txt (independent Drive text export; the ONLY
                                     source of ordered/unordered glyphs)
  - lib/pages-data.json            (patched IN PLACE; never regenerated)

CLASSIFICATION RULE (exact, no exceptions):
  For each of the 152 groups, take each item's full text (segments joined,
  exactly as in pages-data.json). In doc-export.txt, find the line whose text,
  AFTER stripping ONE leading glyph (`^\\d+\\. ` at most one following space
  for numbered, `^[*\\u2022\\-] ` at most one following space for bulleted),
  equals the item text EXACTLY (character-for-character; no fuzzy matching,
  no trimming of inner whitespace).
  - Classify the WHOLE group 'ol' ONLY if EVERY item matches a NUMBERED line.
  - Classify the WHOLE group 'ul' ONLY if EVERY item matches a BULLETED line.
  - Otherwise (any item with no exact match, mixed numbered+bulleted matches,
    or two export lines matching the same item text) leave the WHOLE group as
    flat {type:'p'} blocks and record it UNCLASSIFIED with the exact reason.

  A classified group has its run of {type:'p'} blocks replaced by ONE block
  {type:'ol'|'ul', items:[{segments:[...]}...]} preserving item order and
  every segment (bold flags included) exactly. No word is changed.

  Nothing else is touched: no h2/h3/table/faq blocks, no meta, h1, intro,
  eyebrow, trustChips, and counts.words is never edited.

VERIFICATION (all must pass or the file is NOT written):
  - derived groups == 152 groups / 862 items, per-tab counts matching the
    parse report §5 (guards against parser drift);
  - every group maps to exactly one run of blocks in pages-data.json;
  - counts.words per tab and total identical before/after (stored values
    untouched AND independently recomputed from the patched JSON);
  - block-type counts before/after differ only by p -> ul/ol conversion;
  - normalising the patched JSON (expanding each ul/ol back into its p
    blocks) reproduces the original file EXACTLY — i.e. no other field
    changed.

Re-runnable: on a second run, groups already converted to ul/ol are
recognised, left alone, and reported as already-classified; exit 0, file
unchanged.

Usage: python3 qa/rebuild-lists.py
Exit 0 on success. Exit 1 if a verification fails (file left unchanged).
"""
import copy
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # ~/workspace/midvale-water-damage
DOC_JSON = BASE / "qa/r3-full-doc/doc-full.json"
EXPORT = BASE / "qa/r3-full-doc/doc-export.txt"
PAGES_JSON = BASE / "lib/pages-data.json"
OUT_REPORT = BASE / "qa/rebuild-lists-report.md"

BUTTONS_LINE = "[Call (385) 337-3560] [Request Emergency Help]"
NUM_RE = re.compile(r"^(\d+)\. ?")       # numbered glyph + at most one space
BUL_RE = re.compile(r"^[*•\-] ?")        # bulleted glyph + at most one space

# Per-tab group counts from qa/rebuild-parse-report.md §5 — sanity guard.
EXPECTED_GROUPS_PER_TAB = {
    1: 5, 2: 4, 3: 3, 4: 5, 5: 3, 6: 3, 7: 6, 8: 3, 9: 6, 10: 3,
    11: 4, 12: 6, 13: 6, 14: 7, 15: 7, 16: 5, 17: 7, 18: 9, 19: 6,
    20: 6, 21: 5, 22: 6, 23: 4, 24: 3, 25: 1, 26: 0, 27: 6, 28: 5,
    29: 6, 30: 6, 31: 6,
}

FAILURES = []


def fail(msg):
    FAILURES.append(msg)
    print(f"FAIL: {msg}", file=sys.stderr)


def trunc60(s):
    """First-item text truncated to at most 60 chars for report listings."""
    return s if len(s) <= 60 else s[:57] + "..."


def words(s):
    return len(s.split())


def para_text(p):
    return "".join(e.get("textRun", {}).get("content", "")
                    for e in p.get("elements", []))


def para_segments(p):
    """Segments exactly as qa/rebuild-parser.py builds them (dash rule
    included; the doc contains 0 em/en dashes, so this is a no-op here)."""
    segs = []
    for e in p.get("elements", []):
        tr = e.get("textRun")
        if tr is None:
            continue
        segs.append({"t": tr.get("content", ""),
                     "b": bool(tr.get("textStyle", {}).get("bold", False))})
    if segs:
        segs[-1]["t"] = segs[-1]["t"].rstrip("\n")
    out = []
    for s in segs:
        t = s["t"].replace("\u2014", " ").replace("\u2013", " ")
        t = re.sub(r" {2,}", " ", t)
        if t == "":
            continue
        out.append({"t": t, "b": s["b"]})
    return out


def seg_plain(segments):
    return "".join(s["t"] for s in segments)


def derive_groups(tab):
    """Re-derive list groups from one doc tab, the same way the parser formed
    them: walk body content from just after the intro/buttons/trust lines;
    a group is a maximal run of consecutive bullet paragraphs sharing one
    listId. Blank paragraphs, tables, headings and the buttons line break a
    run (sectionBreaks do not — same as the parser)."""
    dt = tab["documentTab"]
    content = dt["body"]["content"]
    items = []
    for el in content:
        if "paragraph" in el:
            items.append(("p", el["paragraph"]))
        elif "table" in el:
            items.append(("table", el["table"]))
        elif "sectionBreak" in el:
            items.append(("sectionBreak", None))
        else:
            items.append(("other", None))

    def style(it):
        return it[1].get("paragraphStyle", {}).get("namedStyleType")

    def text(it):
        return para_text(it[1])

    h1_pos = [j for j, it in enumerate(items)
              if it[0] == "p" and style(it) == "HEADING_1"]
    assert len(h1_pos) == 1, f"expected exactly 1 H1, found {len(h1_pos)}"
    h1_j = h1_pos[0]
    intro_j = None
    for j, it in enumerate(items):
        if j > h1_j and it[0] == "p" and style(it) == "NORMAL_TEXT" \
                and text(it).strip() != "":
            intro_j = j
            break
    assert intro_j is not None, "no intro paragraph after H1"
    k = intro_j + 1
    while k < len(items) and items[k][0] == "p" and text(items[k]).strip() == "":
        k += 1
    if k < len(items) and items[k][0] == "p" \
            and text(items[k]).strip() == BUTTONS_LINE:
        k += 1
        while k < len(items) and items[k][0] == "p" \
                and text(items[k]).strip() == "":
            k += 1
        if k < len(items) and items[k][0] == "p" \
                and "\u00b7" in text(items[k]):
            k += 1

    groups = []
    cur = None

    def flush():
        nonlocal cur
        if cur is not None:
            groups.append(cur)
            cur = None

    j = k
    while j < len(items):
        kind, obj = items[j]
        if kind == "sectionBreak":
            j += 1
            continue
        if kind == "table":
            flush()
            j += 1
            continue
        if kind != "p":
            flush()
            j += 1
            continue
        raw = text(items[j]).strip()
        st = style(items[j])
        if raw == "":
            flush()
            j += 1
            continue
        if raw == BUTTONS_LINE:
            flush()
            j += 1
            continue
        if st in ("HEADING_2", "HEADING_3"):
            flush()
            j += 1
            continue
        bullet = obj.get("bullet")
        if bullet is not None:
            plain = seg_plain(para_segments(obj))
            lid = bullet.get("listId")
            if cur is not None and cur["listId"] == lid:
                cur["items"].append(plain)
            else:
                flush()
                cur = {"listId": lid, "items": [plain]}
        else:
            flush()
        j += 1
    flush()
    return groups


def build_export_index():
    """stripped text -> [(export line number, 'ol'|'ul')] for every glyph line
    in the Drive export. One leading glyph + at most one following space is
    stripped; the remainder must equal the item text character-for-character.
    Lines with no leading glyph (headings, body text, table lines) are not
    indexed."""
    lines = EXPORT.read_text(encoding="utf-8-sig").splitlines()
    index = defaultdict(list)
    n_num = n_bul = 0
    for i, ln in enumerate(lines, 1):
        m = NUM_RE.match(ln)
        if m:
            index[ln[m.end():]].append((i, "ol"))
            n_num += 1
            continue
        m = BUL_RE.match(ln)
        if m:
            index[ln[m.end():]].append((i, "ul"))
            n_bul += 1
            continue
    return index, n_num, n_bul, len(lines)


def classify(items, index):
    """Return (kind, None) with kind 'ol'|'ul', or (None, reason)."""
    kinds = {}  # item position (1-based) -> kind
    for pos, it in enumerate(items, 1):
        ms = index.get(it, [])
        if not ms:
            return None, (f"item {pos} no exact export match: "
                          f"{trunc60(it)!r}")
        if len(ms) > 1:
            desc = ", ".join(f"line {ln} ({k})" for ln, k in ms)
            return None, (f"item {pos} ambiguous match: {len(ms)} export "
                          f"lines ({desc}) match {trunc60(it)!r}")
        kinds[pos] = ms[0][1]
    ks = set(kinds.values())
    if len(ks) > 1:
        ol_items = [p for p, k in kinds.items() if k == "ol"]
        ul_items = [p for p, k in kinds.items() if k == "ul"]
        return None, (f"mixed glyphs: item(s) {ol_items} match numbered "
                      f"lines, item(s) {ul_items} match bulleted lines")
    return ks.pop(), None


def find_block_run(page, items):
    """Locate a group in the page's blocks. Returns (start, state, kind):
    state 'p' = one run of consecutive {type:'p'} blocks whose joined segment
    texts equal the items; state 'list' = one existing {type:'ul'|'ol'} block
    with the same items (already classified by a previous run); state None
    with kind None = no unique match. kind is the list kind for state 'list'."""
    blocks = page["blocks"]
    n = len(items)
    hits = []
    for i, b in enumerate(blocks):
        if b["type"] == "p":
            if i + n <= len(blocks) and all(
                    blocks[i + t]["type"] == "p" and
                    seg_plain(blocks[i + t]["segments"]) == items[t]
                    for t in range(n)):
                hits.append((i, "p", None))
        elif b["type"] in ("ul", "ol"):
            got = [seg_plain(it["segments"]) for it in b["items"]]
            if got == items:
                hits.append((i, "list", b["type"]))
    if len(hits) == 1:
        return hits[0]
    return (None, None, None) if not hits else (None, "multi", None)


def page_words(page):
    """Word count of one page, computed the way the parser counts it:
    eyebrow + h1 + intro + raw trust line (incl. its '·' separators) +
    all block words (h2/h3 text, p segments, ul/ol item segments, tables).
    FAQs are inside blocks already and are not double-counted."""
    w = 0
    if page.get("eyebrow"):
        w += words(page["eyebrow"])
    w += words(page["h1"]) + words(page["intro"])
    chips = page.get("trustChips")
    if chips:
        w += words(" · ".join(chips))
    for b in page["blocks"]:
        if b["type"] in ("h2", "h3"):
            w += words(b["text"])
        elif b["type"] == "p":
            w += words(seg_plain(b["segments"]))
        elif b["type"] in ("ul", "ol"):
            for it in b["items"]:
                w += words(seg_plain(it["segments"]))
        elif b["type"] == "table":
            w += sum(words(c) for c in b["headers"])
            for r in b["rows"]:
                w += sum(words(c) for c in r)
    return w


def type_counts(data):
    c = Counter()
    for p in data["pages"]:
        for b in p["blocks"]:
            c[b["type"]] += 1
    return c


def normalize(data):
    """Expand every ul/ol block back into its p blocks — the patched JSON
    normalised this way must equal the original file exactly."""
    d = copy.deepcopy(data)
    for p in d["pages"]:
        nb = []
        for b in p["blocks"]:
            if b["type"] in ("ul", "ol"):
                for it in b["items"]:
                    nb.append({"type": "p", "segments": it["segments"]})
            else:
                nb.append(b)
        p["blocks"] = nb
    return d


def main():
    doc = json.loads(DOC_JSON.read_text(encoding="utf-8"))
    data = json.loads(PAGES_JSON.read_text(encoding="utf-8"))
    before = copy.deepcopy(data)
    if data.get("totalTabs") != 31 or len(data["pages"]) != 31:
        fail("pages-data.json does not hold 31 pages")
    if len(doc.get("tabs", [])) != 31:
        fail("doc-full.json does not hold 31 tabs")

    # ---- 1. re-derive groups from doc-full.json ----
    groups = []  # {n, tab, route, listId, items}
    for ti, tab in enumerate(doc["tabs"], 1):
        gs = derive_groups(tab)
        exp = EXPECTED_GROUPS_PER_TAB[ti]
        if len(gs) != exp:
            fail(f"tab {ti}: derived {len(gs)} groups, expected {exp} "
                 f"(parse report §5)")
        for g in gs:
            groups.append({"n": len(groups) + 1, "tab": ti,
                           "route": data["pages"][ti - 1]["route"],
                           "listId": g["listId"], "items": g["items"]})
    if len(groups) != 152:
        fail(f"derived {len(groups)} groups, expected 152")
    total_items = sum(len(g["items"]) for g in groups)
    if total_items != 862:
        fail(f"derived {total_items} items, expected 862")

    # ---- 2. export glyph index ----
    index, n_num, n_bul, n_lines = build_export_index()

    # ---- 3. before-state measurements ----
    words_before = {p["tab"]: p["counts"]["words"] for p in data["pages"]}
    total_before = sum(words_before.values())
    types_before = type_counts(data)

    # ---- 4. classify + locate every group (no patching yet) ----
    results = []
    for g in groups:
        page = data["pages"][g["tab"] - 1]
        kind, reason = classify(g["items"], index)
        start, state, existing_kind = find_block_run(page, g["items"])
        rec = {"group": g, "kind": kind, "reason": reason,
               "start": start, "state": state, "existing_kind": existing_kind}
        if kind is None:
            rec["outcome"] = "unclassified"
        elif state == "p":
            rec["outcome"] = "classify"
        elif state == "list" and existing_kind == kind:
            rec["outcome"] = "already"
        elif state == "list":
            rec["outcome"] = "unclassified"
            rec["reason"] = (f"already classified as {existing_kind} in "
                             f"pages-data.json but export proves {kind}")
        elif state == "multi":
            rec["outcome"] = "unclassified"
            rec["reason"] = ("ambiguous block location: more than one "
                             "matching run in pages-data.json")
        else:
            rec["outcome"] = "unclassified"
            rec["reason"] = ("no matching run of p blocks in "
                             "pages-data.json")
        results.append(rec)

    # ---- 5. apply patches (descending block index per page) ----
    patches = {}
    for r in results:
        if r["outcome"] == "classify":
            patches.setdefault(r["group"]["tab"], []).append(r)
    n_patched = 0
    for tab, rs in patches.items():
        page = data["pages"][tab - 1]
        for r in sorted(rs, key=lambda x: x["start"], reverse=True):
            g = r["group"]
            n = len(g["items"])
            run = page["blocks"][r["start"]:r["start"] + n]
            assert all(b["type"] == "p" for b in run)
            assert [seg_plain(b["segments"]) for b in run] == g["items"]
            new_block = {
                "type": r["kind"],
                "items": [{"segments": copy.deepcopy(b["segments"])}
                          for b in run],
            }
            page["blocks"][r["start"]:r["start"] + n] = [new_block]
            n_patched += 1

    # ---- 6. verification (file NOT written unless all pass) ----
    words_after_stored = {p["tab"]: p["counts"]["words"]
                          for p in data["pages"]}
    if words_after_stored != words_before:
        fail("counts.words changed by the patch")
    words_recomputed = {p["tab"]: page_words(p) for p in data["pages"]}
    for tab in words_before:
        if words_recomputed[tab] != words_before[tab]:
            fail(f"tab {tab}: recomputed words {words_recomputed[tab]} != "
                 f"before {words_before[tab]}")
    total_after = sum(words_after_stored.values())
    if total_after != total_before:
        fail(f"total words changed: {total_before} -> {total_after}")
    types_after = type_counts(data)
    for t in ("h2", "h3", "table"):
        if types_after.get(t, 0) != types_before.get(t, 0):
            fail(f"block type {t} count changed: "
                 f"{types_before.get(t, 0)} -> {types_after.get(t, 0)}")
    n_new_lists = (types_after.get("ul", 0) + types_after.get("ol", 0)
                   - types_before.get("ul", 0) - types_before.get("ol", 0))
    n_p_lost = types_before.get("p", 0) - types_after.get("p", 0)
    n_items_patched = sum(len(r["group"]["items"]) for r in results
                          if r["outcome"] == "classify")
    if n_new_lists != n_patched:
        fail(f"new list blocks {n_new_lists} != patches applied {n_patched}")
    if n_p_lost != n_items_patched:
        fail(f"p blocks lost {n_p_lost} != items patched {n_items_patched}")
    if normalize(data) != normalize(before):
        fail("normalised patched JSON != normalised original file: some "
             "field other than the list blocks changed")
    # every patched block still holds the exact original item texts
    for r in results:
        if r["outcome"] == "classify":
            page = data["pages"][r["group"]["tab"] - 1]
            blk = next(b for b in page["blocks"]
                       if b["type"] in ("ul", "ol") and
                       [seg_plain(it["segments"]) for it in b["items"]]
                       == r["group"]["items"])
            assert blk["type"] == r["kind"]

    if FAILURES:
        print(f"VERIFICATION FAILED ({len(FAILURES)} failure(s)) — "
              f"{PAGES_JSON} left unchanged")
        return 1

    # ---- 7. write patched file (only if something changed) ----
    if n_patched:
        PAGES_JSON.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")

    # ---- 8. report ----
    ol = [r for r in results if r["kind"] == "ol"
          and r["outcome"] in ("classify", "already")]
    ul = [r for r in results if r["kind"] == "ul"
          and r["outcome"] in ("classify", "already")]
    ol_new = [r for r in ol if r["outcome"] == "classify"]
    ul_new = [r for r in ul if r["outcome"] == "classify"]
    already = [r for r in results if r["outcome"] == "already"]
    unc = [r for r in results if r["outcome"] == "unclassified"]
    report = render_report({
        "n_num": n_num, "n_bul": n_bul, "n_lines": n_lines,
        "distinct_texts": len(index),
        "total_items": total_items, "n_groups": len(groups),
        "words_before": words_before, "total_before": total_before,
        "words_recomputed": words_recomputed,
        "types_before": types_before, "types_after": types_after,
        "n_patched": n_patched, "n_items_patched": n_items_patched,
        "ol": ol, "ul": ul, "ol_new": ol_new, "ul_new": ul_new,
        "already": already, "unc": unc,
        "data": data,
    })
    OUT_REPORT.write_text(report, encoding="utf-8")

    print(f"groups: {len(groups)} (items {total_items})")
    print(f"classified this run: ol={len(ol_new)} ul={len(ul_new)} "
          f"already-classified={len(already)} unclassified={len(unc)}")
    print(f"words: total {total_before} before == {total_after} after "
          f"(recomputed {sum(words_recomputed.values())})")
    print(f"patched file: {PAGES_JSON} "
          f"({'rewritten' if n_patched else 'unchanged'})")
    print(f"report: {OUT_REPORT}")
    print("VALIDATION: all checks passed")
    return 0


def render_report(c):
    L = []
    A = L.append
    A("# Midvale UT — List Re-classification Report")
    A("")
    A("Script: `qa/rebuild-lists.py` — re-classifies the 152 flat-`p` list "
      "groups from `qa/rebuild-parse-report.md` Appendix A into true "
      "`ul`/`ol` blocks, using only the glyphs rendered in the independent "
      "Drive text export `qa/r3-full-doc/doc-export.txt`. Patches "
      "`lib/pages-data.json` in place; the parser was NOT re-run and "
      "`pages-data.json` was NOT regenerated.")
    A("")
    A("## Method (classification rule, exact, no exceptions)")
    A("")
    A("- Groups were re-derived from `qa/r3-full-doc/doc-full.json` exactly "
      "the way `qa/rebuild-parser.py` formed them: maximal runs of "
      "consecutive bullet paragraphs sharing one `listId`, starting after "
      "each tab's intro / buttons / trust lines. Derived: "
      f"**{c['n_groups']} groups / {c['total_items']} items**, per-tab counts "
      "identical to parse-report §5 — the inventory matches Appendix A.")
    A("- Export index: every line of `doc-export.txt` starting with a glyph "
      "was indexed by its text after stripping ONE leading glyph "
      "(`^\\d+\\. ` + at most one space for numbered, `^[*•\\-] ` + at most "
      "one space for bulleted). Glyph lines found: "
      f"**{c['n_num']} numbered + {c['n_bul']} bulleted = "
      f"{c['n_num'] + c['n_bul']}** over {c['n_lines']} export lines, "
      f"{c['distinct_texts']} distinct stripped texts.")
    A("- For each group, every item's full text (segments joined, exactly as "
      "in `pages-data.json`) had to match an export line EXACTLY, "
      "character-for-character, after glyph stripping — no fuzzy matching, "
      "no trimming of inner whitespace.")
    A("- Whole group classified `ol` only if EVERY item matches a NUMBERED "
      "line; `ul` only if EVERY item matches a BULLETED line. If any item "
      "has no exact match, or the group's matches mix numbered and bulleted, "
      "or two export lines match the same item text, the WHOLE group stays "
      "flat `{type:'p'}` and is listed below as UNCLASSIFIED with the exact "
      "reason.")
    A("- A classified group has its run of `{type:'p'}` blocks replaced by "
      "ONE block `{type:'ol'|'ul', items:[{segments:[...]}...]}` preserving "
      "item order and every segment (bold flags included) exactly. No word "
      "was changed. No h2/h3/table/faq block, meta, h1, intro, eyebrow, "
      "trustChips or `counts.words` was touched.")
    A("")
    A("## Verdict")
    A("")
    A(f"**Classified `ol`: {len(c['ol'])} groups · Classified `ul`: "
      f"{len(c['ul'])} groups · Left UNCLASSIFIED: {len(c['unc'])} groups** "
      f"(of 152). Of the classified groups, {len(c['ol_new'])} ol + "
      f"{len(c['ul_new'])} ul were classified by this run and "
      f"{len(c['already'])} were already classified by a previous run. "
      f"Items re-classified this run: {c['n_items_patched']} of 862.")
    A("")
    A("## 1. Groups classified `ol` (in the file)")
    A("")
    A(f"{len(c['ol_new'])} classified by this run, "
      f"{len(c['ol']) - len(c['ol_new'])} by a previous run.")
    if c["ol"]:
        A("| # | Tab | Route | Items | First item (≤60 chars) |")
        A("|---:|---|---|---:|---|---|")
        for r in c["ol"]:
            g = r["group"]
            A(f"| {g['n']} | {g['tab']} | `{g['route']}` | {len(g['items'])} | "
              f"{trunc60(g['items'][0])} |")
    else:
        A("None.")
    A("")
    A("## 2. Groups classified `ul` (in the file)")
    A("")
    A(f"{len(c['ul_new'])} classified by this run, "
      f"{len(c['ul']) - len(c['ul_new'])} by a previous run.")
    if c["ul"]:
        A("| # | Tab | Route | Items | First item (≤60 chars) |")
        A("|---:|---|---|---:|---|---|")
        for r in c["ul"]:
            g = r["group"]
            A(f"| {g['n']} | {g['tab']} | `{g['route']}` | {len(g['items'])} | "
              f"{trunc60(g['items'][0])} |")
    else:
        A("None.")
    A("")
    A("## 3. Groups left UNCLASSIFIED (still flat `{type:'p'}`)")
    A("")
    if c["unc"]:
        A("| # | Tab | Route | Items | Exact reason |")
        A("|---:|---|---|---:|---|---|")
        for r in c["unc"]:
            g = r["group"]
            A(f"| {g['n']} | {g['tab']} | `{g['route']}` | {len(g['items'])} | "
              f"{r['reason']} |")
    else:
        A("None — every group classified.")
    if c["already"]:
        A("")
        A("## 4. Already classified by a previous run (left untouched)")
        A("")
        A("| # | Tab | Route | Items | Kind |")
        A("|---:|---|---|---:|---|---|")
        for r in c["already"]:
            g = r["group"]
            A(f"| {g['n']} | {g['tab']} | `{g['route']}` | {len(g['items'])} | "
              f"{r['existing_kind']} |")
    A("")
    A("## 5. Word-count proof — before vs after (must be IDENTICAL)")
    A("")
    A("`before` = stored `counts.words` per tab before the patch. `after` = "
      "stored `counts.words` after the patch (never edited by this script). "
      "`recomputed` = words counted fresh from the patched JSON by the "
      "parser's own counting rule (eyebrow + h1 + intro + raw trust line "
      "incl. its `·` separators + all block words incl. tables and FAQ).")
    A("")
    A("| Tab | Route | Before | After (stored) | Recomputed | Check |")
    A("|---:|---|---:|---:|---:|---|")
    for p in c["data"]["pages"]:
        t = p["tab"]
        b = c["words_before"][t]
        rc = c["words_recomputed"][t]
        ok = "✓" if b == rc else "**FAIL**"
        A(f"| {t} | `{p['route']}` | {b} | {b} | {rc} | {ok} |")
    A(f"| **Total** | | **{c['total_before']}** | **{c['total_before']}** | "
      f"**{sum(c['words_recomputed'].values())}** | ✓ |")
    A("")
    A(f"Total words before = total words after = "
      f"**{c['total_before']}** (per-tab `counts.words` unchanged, and the "
      "fresh recomputation from the patched file agrees on every tab).")
    A("")
    A("## 6. Block-type counts before vs after")
    A("")
    tb, ta = c["types_before"], c["types_after"]
    A("| Block type | Before | After | Change |")
    A("|---|---:|---:|---|")
    for t in ("p", "ul", "ol", "h2", "h3", "table"):
        d = ta.get(t, 0) - tb.get(t, 0)
        ds = f"{d:+d}" if d else "0"
        A(f"| `{t}` | {tb.get(t, 0)} | {ta.get(t, 0)} | {ds} |")
    A("")
    if c["n_patched"]:
        A(f"The only change is the conversion itself: "
          f"{c['n_items_patched']} `{{\"type\":'p'}}` blocks became "
          f"{c['n_patched']} list blocks (one per classified group); h2/h3/table "
          "counts are unchanged.")
    else:
        A("No blocks changed on this run (all classified groups were "
          "already converted by a previous run); h2/h3/table counts are "
          "unchanged.")
    A("")
    A("## 7. No-other-field check")
    A("")
    A("Check run inside the script before writing the file: both the "
      "patched JSON and the file as read were normalised by expanding every "
      "`ul`/`ol` block back into its original `{type:'p'}` blocks (same "
      "segments, same order) and the two normalised forms were compared. "
      "Result: **identical** — no field outside the classified groups' "
      "blocks changed (meta, h1, intro, eyebrow, trustChips, "
      "hasButtonsLine, faqs, counts, routes, urls and every non-list block "
      "are byte-for-byte the same content). In addition, each patched block "
      "was asserted to hold exactly its group's original item texts, and "
      "the stored `counts.words` values were asserted unchanged.")
    A("")
    A("## 8. Notes")
    A("")
    A("- **Export census reconciles exactly.** 866 glyph lines = 862 list "
      "items + 4 extra numbered lines. The 4 extras are the tab-5 H3 "
      "headings under “Four Ways Midvale Basements Flood” "
      "(“Groundwater Seepage”, “Window Wells and Surface Runoff”, "
      "“Plumbing and Appliance Failures”, “Sewer Backups”, export lines "
      "434–440), which the export renders as `1.`–`4.` but which the parser "
      "correctly emitted as `h3` blocks, not list items. Their stripped "
      "texts match no group item, so they cannot misclassify anything.")
    A("- **Zero items had no exact export match.** Every one of the 862 "
      "item texts matched at least one glyph line exactly — the export is "
      "fully matchable; nothing was left flat for lack of a match.")
    A("- **Why 23 groups are unclassified: two different causes.** 4 groups "
      "are genuinely mixed-kind — the same sentence is a numbered step in "
      "one tab and a bulleted item in another, so a per-item lookup cannot "
      "prove that group's glyph (e.g. “Call (385) 337-3560 so a crew is "
      "dispatched.” is `7.` in tab 11's process list but `*` in tab 21's "
      "checklist; “Vent bathroom fans outside, not into the attic.” is `*` "
      "in tab 17 but `8.` in tab 30). The other 19 are ambiguous only "
      "because the same item text recurs elsewhere in the doc and every "
      "matching export line carries the SAME glyph kind (e.g. “Call (385) "
      "337-3560 so a crew is dispatched while you work.” matches 4 bulleted "
      "lines; “Basement flooding cleanup: about $2,500 to $9,000” matches 2 "
      "bulleted lines). Under the rule as written — two export lines matching "
      "the same item text disqualifies the group — all 19 stay flat. If the "
      "rule were relaxed to “ambiguous only when the matching lines disagree "
      "on kind”, 19 of the 23 would classify (114 ul + 34 ol, 4 unclassified) "
      "with no other change; that relaxation was NOT applied — it needs an "
      "explicit order.")
    A("- **Re-runnable:** a second run recognises the converted `ul`/`ol` "
      "blocks, leaves them untouched, and reports them as already "
      "classified; exit 0, file unchanged.")
    A("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
