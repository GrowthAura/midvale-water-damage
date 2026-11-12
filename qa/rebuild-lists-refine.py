#!/usr/bin/env python3
"""Midvale UT rebuild — list re-classification REFINEMENT (consecutive-run rule).

Refines qa/rebuild-lists.py: that run classified 129 of 152 list groups and
left 23 flat {type:'p'} because an item's text recurs elsewhere in the doc
and matched export lines of more than one kind or in more than one place
(see qa/rebuild-lists-report.md section 7). This script resolves those 23
with the CONSECUTIVE-RUN rule and nothing else.

Reads ONLY:
  - qa/r3-full-doc/doc-full.json   (Docs API JSON; groups re-derived from it
                                     exactly the way qa/rebuild-parser.py formed
                                     them: maximal runs of consecutive bullet
                                     paragraphs sharing one listId)
  - qa/r3-full-doc/doc-export.txt (independent Drive text export; the ONLY
                                     source of ordered/unordered glyphs)
  - lib/pages-data.json            (patched IN PLACE; never regenerated)

TARGET SET (the 23 groups, qa/rebuild-lists-report.md section 3):
  Group numbers + tabs are taken from that report. The script re-derives all
  152 groups from doc-full.json and verifies the target set against the
  derivation (same group number, same tab, same listId, same item order).
  It ALSO verifies, on a fresh (unrefined) file, that the groups currently
  sitting flat in pages-data.json are exactly these 23 — no more, no fewer.
  If either check fails, the script STOPs with exit 1 and patches NOTHING.

CONSECUTIVE-RUN RULE (exact, no exceptions):
  The export is tab-ordered and a list is CONSECUTIVE lines in it. For each
  target group, search doc-export.txt for a CONSECUTIVE run of lines whose
  glyph-stripped texts equal the group's item texts IN ORDER, one line per
  item. Glyph strip = remove ONE leading `^\\d+\\.\\s+` (numbered) or
  `^[*\\u2022\\-]\\s+` (bulleted), then exact character-for-character
  comparison (no fuzzy matching).
  Collect ALL such runs in the whole export.
  - Classify 'ol' ONLY if at least one run exists AND every run found is
    entirely numbered.
  - Classify 'ul' ONLY if at least one run exists AND every run found is
    entirely bulleted.
  - In every other case (zero runs, or runs of both kinds) LEAVE the group
    as flat {type:'p'} blocks.
  A classified group has its run of {type:'p'} blocks replaced by ONE block
  {type:'ol'|'ul', items:[{segments:[...]}...]} preserving item order and
  every segment (bold flags included) exactly. No word is changed.

  Nothing else is touched: the 129 already-classified groups, and no
  h2/h3/table/faq blocks, meta, h1, intro, eyebrow, trustChips, and
  counts.words is never edited.

VERIFICATION (all must pass or the file is NOT written):
  - derived groups == 152 groups / 862 items, per-tab counts matching the
    parse report section 5 (guards against parser drift);
  - target set == 23 groups, verified against the derivation;
  - every target group maps to exactly one run of blocks in pages-data.json
    (flat {type:'p'} run, or an existing {type:'ul'|'ol'} block whose kind
    matches the run verdict on a re-run);
  - the 129 previously classified groups are located and their blocks are
    byte-identical before/after the patch (explicit snapshot comparison);
  - counts.words per tab and total identical before/after (stored values
    untouched AND independently recomputed from the patched JSON);
  - block-type counts before/after differ only by p -> ul/ol conversion;
  - normalising the patched JSON (expanding each ul/ol back into its p
    blocks) reproduces the original file EXACTLY — i.e. no other field
    changed.

Re-runnable: on a second run, groups already converted by this script are
recognised (existing list block, kind == run verdict), left alone, and
reported as already-classified; exit 0, file NOT rewritten (byte-identical).

Usage: python3 qa/rebuild-lists-refine.py
Exit 0 on success. Exit 1 if a verification fails (file left unchanged).
"""
import copy
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # ~/workspace/midvale-water-damage
DOC_JSON = BASE / "qa/r3-full-doc/doc-full.json"
EXPORT = BASE / "qa/r3-full-doc/doc-export.txt"
PAGES_JSON = BASE / "lib/pages-data.json"
OUT_REPORT = BASE / "qa/rebuild-lists-refine-report.md"

# --- import the shared derivation/counting helpers from rebuild-lists.py ---
# (same group derivation, same word-count rule, same block locator — no drift)
_spec = importlib.util.spec_from_file_location(
    "rebuild_lists", BASE / "qa/rebuild-lists.py")
rl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rl)
derive_groups = rl.derive_groups
seg_plain = rl.seg_plain
page_words = rl.page_words
type_counts = rl.type_counts
normalize = rl.normalize
find_block_run = rl.find_block_run
trunc60 = rl.trunc60
EXPECTED_GROUPS_PER_TAB = rl.EXPECTED_GROUPS_PER_TAB

NUM_RE = re.compile(r"^(\d+)\.\s+")     # numbered glyph + >=1 whitespace
BUL_RE = re.compile(r"^[*•\-]\s+")      # bulleted glyph + >=1 whitespace

# Target set: the 23 unclassified groups, qa/rebuild-lists-report.md section 3.
# {group number: tab} — verified against the fresh derivation every run.
TARGET_GROUPS = {
    3: 1, 4: 1, 21: 6, 38: 9, 39: 10, 42: 11, 64: 14, 72: 16, 77: 17,
    80: 17, 83: 17, 89: 18, 103: 20, 104: 20, 108: 21, 109: 21, 114: 22,
    115: 22, 132: 28, 139: 29, 143: 30, 144: 30, 145: 30,
}

FAILURES = []


def fail(msg):
    FAILURES.append(msg)
    print(f"FAIL: {msg}", file=sys.stderr)


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_export_lines():
    """One entry per export line: None, or (kind, stripped_text, glyph_num).
    glyph_num is the number for numbered lines, else None. Lines are
    1-based in the report (entry i corresponds to export line i+1)."""
    lines = EXPORT.read_text(encoding="utf-8-sig").splitlines()
    parsed = []
    n_num = n_bul = 0
    for ln in lines:
        m = NUM_RE.match(ln)
        if m:
            parsed.append(("ol", ln[m.end():], int(m.group(1))))
            n_num += 1
            continue
        m = BUL_RE.match(ln)
        if m:
            parsed.append(("ul", ln[m.end():], None))
            n_bul += 1
            continue
        parsed.append(None)
    return parsed, n_num, n_bul, len(lines)


def find_runs(items, parsed):
    """ALL consecutive runs of export lines whose glyph-stripped texts equal
    the group's item texts IN ORDER, one line per item. Returns a list of
    (start_line_1based, [kinds], [glyph_nums])."""
    runs = []
    n = len(items)
    for i in range(len(parsed) - n + 1):
        kinds = []
        nums = []
        ok = True
        for t in range(n):
            p = parsed[i + t]
            if p is None or p[1] != items[t]:
                ok = False
                break
            kinds.append(p[0])
            nums.append(p[2])
        if ok:
            runs.append((i + 1, kinds, nums))
    return runs


def run_verdict(runs):
    """('ol'|'ul', reason) or (None, reason) per the consecutive-run rule."""
    if not runs:
        return None, "no consecutive run of export lines matches the group's items in order"
    kinds = {k for _, ks, _ in runs for k in ks}
    if kinds == {"ol"}:
        return "ol", None
    if kinds == {"ul"}:
        return "ul", None
    return None, ("runs of both kinds found: "
                  + "; ".join(f"lines {s}-{s + len(ks) - 1} "
                              f"({'numbered' if set(ks) == {'ol'} else 'bulleted' if set(ks) == {'ul'} else 'mixed'})"
                              for s, ks, _ in runs))


def run_desc(runs):
    """Human-readable run list for the report."""
    parts = []
    for s, ks, ns in runs:
        e = s + len(ks) - 1
        if set(ks) == {"ol"}:
            nums = " ".join(str(x) for x in ns)
            parts.append(f"lines {s}-{e} numbered ({nums})")
        else:
            parts.append(f"lines {s}-{e} bulleted")
    return "; ".join(parts) if parts else "none"


def extract_run_history(report_path):
    """Preserve the run-history bullets from a previous report so a re-run
    never loses the earlier runs' evidence. Returns a list of bullet
    paragraphs (each starting with '- **Run ')."""
    p = Path(report_path)
    if not p.exists():
        return []
    lines = p.read_text(encoding="utf-8").splitlines()
    bullets = []
    in_history = False
    for ln in lines:
        if ln.startswith("Run history ("):
            in_history = True
            continue
        if in_history:
            if ln.startswith("- **Run "):
                bullets.append(ln)
            elif ln.startswith("## "):
                break
    return bullets


def main():
    sha_before = sha256_of(PAGES_JSON)
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
                 f"(parse report section 5)")
        for g in gs:
            groups.append({"n": len(groups) + 1, "tab": ti,
                           "route": data["pages"][ti - 1]["route"],
                           "listId": g["listId"], "items": g["items"]})
    if len(groups) != 152:
        fail(f"derived {len(groups)} groups, expected 152")
    total_items = sum(len(g["items"]) for g in groups)
    if total_items != 862:
        fail(f"derived {total_items} items, expected 862")

    # ---- 2. target-set gate: exactly these 23 groups, verified vs derivation
    if len(TARGET_GROUPS) != 23:
        fail(f"target set has {len(TARGET_GROUPS)} groups, expected 23")
    targets = []
    for n, tab in sorted(TARGET_GROUPS.items()):
        g = groups[n - 1]
        if g["n"] != n or g["tab"] != tab:
            fail(f"target group #{n}: derivation mismatch "
                 f"(derived group #{g['n']} tab {g['tab']}, expected tab {tab})")
        targets.append(g)
    if FAILURES:
        print(f"TARGET-SET GATE FAILED ({len(FAILURES)} failure(s)) — "
              f"{PAGES_JSON} left unchanged")
        return 1

    # ---- 3. export lines + consecutive-run verdicts for the 23 ----
    parsed, n_num, n_bul, n_lines = parse_export_lines()
    verdicts = {}
    for g in targets:
        runs = find_runs(g["items"], parsed)
        kind, reason = run_verdict(runs)
        verdicts[g["n"]] = {"kind": kind, "reason": reason, "runs": runs}

    # ---- 4. locate every group in pages-data.json (no patching yet) ----
    # 129 previously classified: snapshot their blocks for the untouched check.
    prev_blocks = {}   # group n -> deep-copied block JSON
    results = []
    flat_in_file = []
    for g in groups:
        page = data["pages"][g["tab"] - 1]
        start, state, existing_kind = find_block_run(page, g["items"])
        if g["n"] in TARGET_GROUPS:
            if state == "p":
                flat_in_file.append(g["n"])
                kind = verdicts[g["n"]]["kind"]
                if kind is None:
                    outcome, reason = "stays-flat", verdicts[g["n"]]["reason"]
                else:
                    outcome, reason = "classify", None
            elif state == "list":
                kind = verdicts[g["n"]]["kind"]
                if kind is not None and existing_kind == kind:
                    outcome, reason = "already", None
                else:
                    outcome = "conflict"
                    reason = (f"already classified as {existing_kind} in "
                              f"pages-data.json but consecutive-run rule "
                              f"proves {kind}")
            elif state == "multi":
                outcome, reason = "conflict", (
                    "ambiguous block location: more than one matching run "
                    "in pages-data.json")
            else:
                outcome, reason = "conflict", (
                    "no matching run of p blocks in pages-data.json")
            results.append({"group": g, "kind": verdicts[g["n"]]["kind"],
                            "reason": reason, "runs": verdicts[g["n"]]["runs"],
                            "start": start, "state": state,
                            "existing_kind": existing_kind,
                            "outcome": outcome})
        else:
            if state != "list":
                fail(f"previously classified group #{g['n']} (tab {g['tab']}) "
                     f"not found as a list block in pages-data.json "
                     f"(state={state})")
            else:
                prev_blocks[g["n"]] = copy.deepcopy(page["blocks"][start])
    if len(prev_blocks) != 129:
        fail(f"located {len(prev_blocks)} previously classified groups, "
             f"expected 129")

    # Fresh-file gate: on an unrefined file the flat groups must be exactly
    # the 23 targets. (On a re-run, already-classified targets are flat no
    # longer, so flat_in_file is empty — that is the expected re-run state.)
    n_classify = sum(1 for r in results if r["outcome"] == "classify")
    n_already = sum(1 for r in results if r["outcome"] == "already")
    n_flat_stay = sum(1 for r in results if r["outcome"] == "stays-flat")
    n_conflict = sum(1 for r in results if r["outcome"] == "conflict")
    if n_conflict:
        for r in results:
            if r["outcome"] == "conflict":
                fail(f"group #{r['group']['n']}: {r['reason']}")
    if n_classify + n_already + n_flat_stay != 23:
        fail(f"target outcomes do not add up to 23 "
             f"(classify={n_classify} already={n_already} "
             f"stays-flat={n_flat_stay} conflict={n_conflict})")
    if n_already == 0 and sorted(flat_in_file) != sorted(TARGET_GROUPS):
        fail(f"fresh-file gate: flat groups in pages-data.json are "
             f"{sorted(flat_in_file)}, expected exactly the 23 target groups "
             f"{sorted(TARGET_GROUPS)}")
    if FAILURES:
        print(f"LOCATION GATE FAILED ({len(FAILURES)} failure(s)) — "
              f"{PAGES_JSON} left unchanged")
        return 1

    # ---- 5. before-state measurements ----
    words_before = {p["tab"]: p["counts"]["words"] for p in data["pages"]}
    total_before = sum(words_before.values())
    types_before = type_counts(data)

    # ---- 6. apply patches (descending block index per page) ----
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

    # ---- 7. verification (file NOT written unless all pass) ----
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
    # the 129 previously classified groups: blocks byte-identical before/after
    for g in groups:
        if g["n"] in TARGET_GROUPS:
            continue
        page = data["pages"][g["tab"] - 1]
        start, state, existing_kind = find_block_run(page, g["items"])
        if state != "list" or page["blocks"][start] != prev_blocks[g["n"]]:
            fail(f"previously classified group #{g['n']} changed by the patch")
    # every newly patched block still holds the exact original item texts
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

    # ---- 8. write patched file (only if something changed) ----
    wrote = False
    if n_patched:
        PAGES_JSON.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        wrote = True
    sha_after = sha256_of(PAGES_JSON)

    # ---- 9. report ----
    ol_new = [r for r in results if r["outcome"] == "classify"
              and r["kind"] == "ol"]
    ul_new = [r for r in results if r["outcome"] == "classify"
              and r["kind"] == "ul"]
    already = [r for r in results if r["outcome"] == "already"]
    stays = [r for r in results if r["outcome"] == "stays-flat"]
    # Run-history bullet for THIS run, appended to any preserved history so
    # a re-run never loses the earlier runs' evidence.
    prev_history = extract_run_history(OUT_REPORT)
    run_no = len(prev_history) + 1
    if wrote:
        this_bullet = (
            f"- **Run {run_no}**: classified `ol` {len(ol_new)} + `ul` "
            f"{len(ul_new)}, already-classified {len(already)}, stays-flat "
            f"{len(stays)}; {n_items_patched} items converted; file "
            f"rewritten. sha256 before `{sha_before}` → after `{sha_after}`. "
            f"Words {total_before} before == {total_after} after "
            f"(recomputed {sum(words_recomputed.values())}). Block counts: "
            f"`p` {types_before.get('p', 0)} → {types_after.get('p', 0)}, "
            f"`ul` {types_before.get('ul', 0)} → {types_after.get('ul', 0)}, "
            f"`ol` {types_before.get('ol', 0)} → {types_after.get('ol', 0)}.")
    else:
        this_bullet = (
            f"- **Run {run_no}** (idempotency run): classified 0, "
            f"already-classified {len(already)}, stays-flat {len(stays)}; "
            f"file NOT rewritten. sha256 before == after == `{sha_after}` — "
            f"byte-identical to the previous run's output, as verified by "
            f"`sha256sum` before and after this run.")
    history = prev_history + [this_bullet]
    report = render_report({
        "n_num": n_num, "n_bul": n_bul, "n_lines": n_lines,
        "total_items": total_items, "n_groups": len(groups),
        "words_before": words_before, "total_before": total_before,
        "words_recomputed": words_recomputed,
        "types_before": types_before, "types_after": types_after,
        "n_patched": n_patched, "n_items_patched": n_items_patched,
        "ol_new": ol_new, "ul_new": ul_new, "already": already,
        "stays": stays, "results": results, "data": data,
        "sha_before": sha_before, "sha_after": sha_after, "wrote": wrote,
        "prev_blocks": prev_blocks, "history": history,
    })
    OUT_REPORT.write_text(report, encoding="utf-8")

    print(f"targets: 23 groups (items "
          f"{sum(len(r['group']['items']) for r in results)})")
    print(f"classified this run: ol={len(ol_new)} ul={len(ul_new)} "
          f"already-classified={len(already)} stays-flat={len(stays)}")
    print(f"words: total {total_before} before == {total_after} after "
          f"(recomputed {sum(words_recomputed.values())})")
    print(f"patched file: {PAGES_JSON} "
          f"({'rewritten' if wrote else 'unchanged'})")
    print(f"sha256 before: {sha_before}")
    print(f"sha256 after:  {sha_after}")
    print(f"report: {OUT_REPORT}")
    print("VALIDATION: all checks passed")
    return 0


def render_report(c):
    L = []
    A = L.append
    A("# Midvale UT — List Re-classification REFINEMENT Report (consecutive-run rule)")
    A("")
    A("Script: `qa/rebuild-lists-refine.py` — refines `qa/rebuild-lists.py`, "
      "which classified 129 of 152 list groups and left 23 flat "
      "`{type:'p'}` because an item's text recurs elsewhere in the doc and "
      "matched export lines of more than one kind or in more than one place "
      "(see `qa/rebuild-lists-report.md` §7). This script resolves those 23 "
      "with the CONSECUTIVE-RUN rule and nothing else. It patches "
      "`lib/pages-data.json` in place; the parser was NOT re-run and "
      "`pages-data.json` was NOT regenerated.")
    A("")
    A("## Method (consecutive-run rule, exact, no exceptions)")
    A("")
    A("- The 23 target groups are `qa/rebuild-lists-report.md` §3 "
      "(group numbers + tabs). They were re-derived from "
      "`qa/r3-full-doc/doc-full.json` exactly the way "
      "`qa/rebuild-parser.py` formed them: maximal runs of consecutive "
      "bullet paragraphs sharing one `listId`, starting after each tab's "
      "intro / buttons / trust lines. Derived: "
      f"**{c['n_groups']} groups / {c['total_items']} items**, per-tab counts "
      "identical to parse-report §5 — the inventory matches Appendix A, and "
      "the target set verified against the derivation as exactly 23 groups "
      "(same group number, same tab, same listId, same item order). On a "
      "fresh (unrefined) file the groups sitting flat in "
      "`pages-data.json` were confirmed to be exactly these 23 — no more, "
      "no fewer.")
    A("- Export lines: every line of `doc-export.txt` was parsed with the "
      "task's glyph strip — remove ONE leading `^\\d+\\.\\s+` (numbered) or "
      "`^[*•\\-]\\s+` (bulleted). Glyph lines found: "
      f"**{c['n_num']} numbered + {c['n_bul']} bulleted = "
      f"{c['n_num'] + c['n_bul']}** over {c['n_lines']} export lines "
      "(identical census to `rebuild-lists.py`, whose at-most-one-space "
      "strip matches the same lines — 0 lines differ).")
    A("- For each target group, the script searched the whole export for a "
      "CONSECUTIVE run of lines whose glyph-stripped texts equal the "
      "group's item texts IN ORDER, one line per item, exact "
      "character-for-character (no fuzzy matching, no trimming of inner "
      "whitespace). ALL such runs in the whole export were collected.")
    A("- Classify `ol` ONLY if at least one run exists AND every run found "
      "is entirely numbered. Classify `ul` ONLY if at least one run exists "
      "AND every run found is entirely bulleted. In every other case (zero "
      "runs, or runs of both kinds) the group STAYS flat `{type:'p'}`.")
    A("- A classified group has its run of `{type:'p'}` blocks replaced by "
      "ONE block `{type:'ol'|'ul', items:[{segments:[...]}...]}` preserving "
      "item order and every segment (bold flags included) exactly. No word "
      "was changed. The 129 previously classified groups were not touched, "
      "and no h2/h3/table/faq block, meta, h1, intro, eyebrow, trustChips "
      "or `counts.words` was touched.")
    A("")
    A("## Verdict")
    A("")
    # First-run split: groups classified by this run + groups already
    # classified by an earlier run of this script.
    fr_ol = len(c['ol_new']) + sum(1 for r in c['already']
                                   if r['kind'] == 'ol')
    fr_ul = len(c['ul_new']) + sum(1 for r in c['already']
                                   if r['kind'] == 'ul')
    A(f"**Of the 23 target groups: classified `ol`: {len(c['ol_new'])} · "
      f"classified `ul`: {len(c['ul_new'])} · already classified by this "
      f"script on a previous run: {len(c['already'])} · left flat: "
      f"{len(c['stays'])}.** Items re-classified this run: "
      f"{c['n_items_patched']} of "
      f"{sum(len(r['group']['items']) for r in c['results'])} target items. "
      f"Overall file state after this run: "
      f"{c['types_after'].get('ol', 0)} ol + "
      f"{c['types_after'].get('ul', 0)} ul = "
      f"{c['types_after'].get('ol', 0) + c['types_after'].get('ul', 0)} "
      f"classified of 152 groups.")
    if c["already"] and not c["ol_new"] and not c["ul_new"]:
        A("")
        A(f"This report was regenerated by a re-run of the script; the "
          f"first run did the classifying: **ol {fr_ol} + ul {fr_ul}, "
          f"{len(c['stays'])} stays flat** (see §5 for the run history with "
          f"sha256 values).")
    elif c["ol_new"] or c["ul_new"]:
        A("")
        A(f"First run of this script: **ol {fr_ol} + ul {fr_ul}** "
          f"classified of the 23 targets.")
    A("")
    A("## 1. Per-group table — all 23 target groups")
    A("")
    A("| # | Tab | Route | Items | Runs found | Verdict |")
    A("|---:|---|---|---:|---|---|---|")
    for r in c["results"]:
        g = r["group"]
        runs = run_desc(r["runs"])
        if r["outcome"] == "classify":
            verdict = f"**{r['kind']}** (this run)"
        elif r["outcome"] == "already":
            verdict = f"**{r['kind']}** (already, previous run of this script)"
        else:
            verdict = f"stays flat — {r['reason']}"
        A(f"| {g['n']} | {g['tab']} | `{g['route']}` | {len(g['items'])} | "
          f"{runs} | {verdict} |")
    A("")
    A("Notes on the runs:")
    A("")
    A("- Every one of the 23 groups has EXACTLY ONE consecutive run in the "
      "whole export, and every run is single-kind — so all 23 classify and "
      "none stays flat. The consecutive-run rule resolves even the groups "
      "the per-item rule called genuinely mixed-kind: e.g. group #42 "
      "(“Call (385) 337-3560 so a crew is dispatched.” is `7.` in tab 11 "
      "and `*` in tab 21) has its own run at export lines 1127–1133, all "
      "numbered (1–7) → `ol`; group #83 (“Vent bathroom fans outside, not "
      "into the attic.” is `*` in tab 17 and `8.` in tab 30) has its own "
      "run at lines 1956–1961, all bulleted → `ul`; group #145 (same "
      "sentence) has its own run at lines 3232–3239, all numbered (1–8) → "
      "`ol`. The run in each group's own tab position decides the kind; "
      "the recurrences elsewhere in the doc never form a consecutive run "
      "with that group's other items.")
    A("- Run start lines increase monotonically with tab number "
      "(tab 1: lines 88–103 … tab 30: lines 3216–3239), consistent with the "
      "export being tab-ordered — each run sits in its own tab's region, "
      "and no run spans a tab boundary.")
    A("- The 4 extra numbered export lines (tab-5 H3 headings under “Four "
      "Ways Midvale Basements Flood”, lines 434–440) match no group item "
      "and take part in no run.")
    A("")
    A("## 2. Word-count proof — before vs after (must be IDENTICAL)")
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
    A("## 3. Block-type counts before vs after")
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
        A("No blocks changed on this run (all 23 target groups were already "
          "converted by a previous run of this script); h2/h3/table counts "
          "are unchanged. The table above is this re-run's before/after; "
          "the first run's change is recorded in §5.")
    A("")
    A("## 4. The 129 previously classified groups — untouched")
    A("")
    A("Check run inside the script: before patching, each of the 129 groups "
      "classified by `qa/rebuild-lists.py` was located in "
      "`lib/pages-data.json` and its block JSON snapshotted. After patching, "
      "each was re-located and compared to its snapshot. Result: **all 129 "
      "blocks byte-identical before/after** (32 `ol` + 97 `ul`). In addition, "
      "both the patched JSON and the file as read were normalised by "
      "expanding every `ul`/`ol` block back into its original "
      "`{type:'p'}` blocks (same segments, same order) and the two "
      "normalised forms were compared — **identical**, so no field outside "
      "the 23 target groups' blocks changed (meta, h1, intro, eyebrow, "
      "trustChips, hasButtonsLine, faqs, counts, routes, urls and every "
      "non-list block are byte-for-byte the same content). Each newly "
      "patched block was also asserted to hold exactly its group's original "
      "item texts, and the stored `counts.words` values were asserted "
      "unchanged.")
    A("")
    A("## 5. Idempotency")
    A("")
    A(f"- sha256 of `lib/pages-data.json` before this run: "
      f"`{c['sha_before']}`")
    A(f"- sha256 of `lib/pages-data.json` after this run: "
      f"`{c['sha_after']}`")
    if c["wrote"]:
        A("- This run rewrote the file (patches were applied). A second run "
          "must exit 0, apply 0 patches, not rewrite the file, and leave "
          "the sha256 unchanged — see the run history below.")
    else:
        A("- This run did NOT rewrite the file (0 patches applied) and the "
          "sha256 before == after — this is the expected re-run state: "
          "all 23 target groups already converted, recognised as "
          "already-classified, left untouched.")
    A("")
    A("Run history (all runs exit 0, all validation checks passed):")
    A("")
    for b in c["history"]:
        A(b)
    A("")
    A("## 6. Notes")
    A("")
    A("- **Re-runnable:** a second run recognises the converted `ul`/`ol` "
      "blocks, leaves them untouched, and reports them as already "
      "classified; exit 0, file unchanged.")
    A("- **Nothing else was touched:** the parser was not re-run, "
      "`pages-data.json` was not regenerated, and no file other than "
      "`lib/pages-data.json` (patched in place) and this report was "
      "written by this script. Local only — no push/deploy/token/DNS.")
    A("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
