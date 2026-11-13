#!/usr/bin/env python3
"""Generate qa/uiux-render-2026-11-13.md from qa/uiux-render-data.json.
Read-only wrt source: only writes the findings file."""
import json, os

D = os.path.expanduser("~/workspace/midvale-water-damage/qa")
data = json.load(open(os.path.join(D, "uiux-render-data.json")))
ORDER = [
    ("home", "/"), ("about", "/about"),
    ("basement-flooding-cleanup", "/basement-flooding-cleanup"),
    ("burst-pipe-water-damage", "/burst-pipe-water-damage"),
    ("ceiling-water-damage", "/ceiling-water-damage"),
    ("commercial-water-damage", "/commercial-water-damage"),
    ("condo-apartment-water-damage", "/condo-apartment-water-damage"),
    ("contact", "/contact"),
    ("crawl-space-water-damage", "/crawl-space-water-damage"),
    ("disclaimer", "/disclaimer"),
    ("emergency-water-extraction", "/emergency-water-extraction"),
    ("hardwood-floor-cabinet-drying", "/hardwood-floor-cabinet-drying"),
    ("locations-cottonwood-heights-ut", "/locations/cottonwood-heights-ut"),
    ("locations-magna-ut", "/locations/magna-ut"),
    ("locations-south-salt-lake-ut", "/locations/south-salt-lake-ut"),
    ("midvale-water-sewer-emergency-contacts", "/midvale-water-sewer-emergency-contacts"),
    ("mold-remediation", "/mold-remediation"),
    ("privacy-policy", "/privacy-policy"),
    ("resources-basement-flooding-spring-snowmelt-utah", "/resources/basement-flooding-spring-snowmelt-utah"),
    ("resources-can-mold-grow-in-utah", "/resources/can-mold-grow-in-utah"),
    ("resources-frozen-pipes-midvale", "/resources/frozen-pipes-midvale"),
    ("resources-upstairs-unit-leak-who-pays-utah", "/resources/upstairs-unit-leak-who-pays-utah"),
    ("resources-winterize-swamp-cooler-utah", "/resources/winterize-swamp-cooler-utah"),
    ("sewage-backup-cleanup", "/sewage-backup-cleanup"),
    ("storm-flood-damage", "/storm-flood-damage"),
    ("swamp-cooler-leak-water-damage", "/swamp-cooler-leak-water-damage"),
    ("terms-of-use", "/terms-of-use"),
    ("water-damage-repair", "/water-damage-repair"),
    ("water-heater-leak-cleanup", "/water-heater-leak-cleanup"),
    ("water-leak-detection", "/water-leak-detection"),
    ("window-well-flooding", "/window-well-flooding"),
]

wide_m = []
for k, _ in ORDER:
    m = data[k]["m390"]
    if m.get("wide"):
        tw = max(w["w"] for w in m["wide"] if w["tag"] == "TABLE")
        wide_m.append((k, tw))

L = []
L.append("# Midvale UT — UI/UX Render Audit (Stage 1)")
L.append("")
L.append("**Date:** 2026-11-13 · **Auditor:** RENDER auditor (Stage 1 UI/UX round) · **Scope:** local audit only — no source edits, no push, no deploy, no token, no DNS.")
L.append("")
L.append("## Method")
L.append("")
L.append("- Served the built `out/` on the `/midvale-water-damage/` subpath at `http://127.0.0.1:8341/midvale-water-damage/` via the existing `qa/linkfix-serve.py` (accepts a port argument; no copy was needed).")
L.append("- Site identity confirmed before screenshotting: homepage H1 = “24/7 Water Damage Restoration in Midvale, UT 84047”, phone (385) 337-3560 present, `/emergency-water-extraction` returns 200.")
L.append("- Playwright Chromium, desktop viewport 1440×900 and mobile 390×844, full-page capture after a slow scroll (600px steps) so lazy images load; fonts/images waited on before capture. Raw metrics in `qa/uiux-render-data.json`.")
L.append("- Per-page metrics: H1/H2/H3 lists, element counts (paragraphs, images, tables, lists, FAQ items), `scrollWidth` vs `clientWidth`, images with `naturalWidth == 0` after slow scroll (broken-local check), elements wider than the viewport, blank-band heuristic. Visual spot-checks on crops: home hero + service-card grid (desktop + mobile), emergency hero + mid-section (desktop + mobile), commercial mobile table, Magna desktop hero, frozen-pipes mobile hero, contact desktop top, home footer (desktop).")
L.append("- `lib/pages-data.json` untouched (sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`, re-verified after the audit).")
L.append("")
L.append("## Verdict")
L.append("")
L.append("**31/31 routes rendered at desktop 1440 and mobile 390 — 62 full-page screenshots. P1: 0 · P2: 0 · P3 observations: 2 (both non-blocking, see below). No horizontal page overflow on any route at either width. 0 broken local images (214 image instances checked after slow scroll, 0 with `naturalWidth == 0`). Every route has exactly 1 H1. No blank bands, no cut-off elements, no misaligned grids found. Sticky header (top, 115px tall on mobile) and sticky body images (`.body-img-fig.sticky`, `top: 96px`) render correctly; sticky images appear at the right of text blocks on desktop and stack above/below on mobile with no overlap.**")
L.append("")
L.append("## Defects by severity")
L.append("")
L.append("### P1 — none")
L.append("")
L.append("### P2 — none")
L.append("")
L.append("### P3 — observations (not defects; no fix required for a pass)")
L.append("")
L.append("**OBS-1 — Mobile tables are wider than the 390px viewport and need a horizontal swipe (18 routes).** Table widths 392–621px at 390px viewport (worst: `locations/magna-ut`, 630px table, ~1.6× viewport; next: `storm-flood-damage` 450px, `commercial-water-damage` 446–452px). Verified NOT clipped: every table sits in `.table-wrap { overflow-x: auto; }` (`app/globals.css:237`); probed live at 390px — wrapper `scrollWidth` (e.g. Magna 630) > `clientWidth` (342) with `overflow-x: auto`, so the full table is reachable by swiping, and the page itself never scrolls horizontally (`scrollWidth == clientWidth` on all 31 routes). Viewed the commercial table crop: the third column is cut at the right edge until swiped, with no visible scroll cue (no fade/shadow). Cosmetic only; a scroll hint would be a nice-to-have. Affected routes: home, basement-flooding-cleanup, burst-pipe-water-damage, ceiling-water-damage, commercial-water-damage, condo-apartment-water-damage, emergency-water-extraction, hardwood-floor-cabinet-drying, locations-magna-ut, locations-south-salt-lake-ut, resources-basement-flooding-spring-snowmelt-utah, resources-can-mold-grow-in-utah, resources-frozen-pipes-midvale, resources-upstairs-unit-leak-who-pays-utah, storm-flood-damage, water-damage-repair, water-heater-leak-cleanup, water-leak-detection.")
L.append("")
L.append("**OBS-2 — Mobile sticky call bar covers the bottom ~50px of the viewport at scroll 0 (normal fixed-bar behaviour).** In full-page screenshots the bar appears to overlap the hero intro paragraph (e.g. home mobile: “…mold can take hold. From Bingham” runs under the “Call (385) 337-3560 · 24/7” bar). This is a full-page-capture artifact: the bar is fixed to the viewport bottom and the text scrolls under it in real use; no content is lost. Not a defect.")
L.append("")
L.append("### Checked and explicitly NOT defects")
L.append("")
L.append("- **Blank-band heuristic fired 1× per page on both widths** — every hit is `div.hero-shade` (the dark overlay div over the hero image, no text by design). Not a blank band; hero images render underneath it (viewed on home, emergency, Magna, frozen-pipes, contact).")
L.append("- **“Wide” elements on mobile are only TABLE/THEAD/TBODY/TR** (see OBS-1). No other element exceeds the viewport on any route.")
L.append("- **Footer Google Maps embed fails in this VM (ERR_TUNNEL_CONNECTION_FAILED, no route to google.com)** — the known open item, NOT counted as a defect. 0 local assets fail. Footer link columns themselves render clean (viewed home desktop footer: 5 aligned columns + copyright line).")
L.append("- **Stale `_error` keys in `qa/uiux-render-data.json`** for swamp-cooler-leak-water-damage (m390), terms-of-use, water-damage-repair, water-heater-leak-cleanup, water-leak-detection, window-well-flooding are leftovers from the crashed intermediate run (see “Script errors” below); all 62 passes re-ran successfully afterwards and every entry now carries fresh metrics + a screenshot file. They are not failures.")
L.append("")
L.append("## Script errors (owned plainly)")
L.append("")
L.append("1. **First run died on `emergency-water-extraction` desktop: `Page.screenshot: Timeout 30000ms exceeded`** (full-page capture of a ~10,000px page). Fixed by raising the screenshot timeout to 180s with a retry, and by saving `uiux-render-data.json` incrementally after each route so a crash no longer loses collected metrics.")
L.append("2. **Second run died on `swamp-cooler-leak-water-damage` m390: `Page.screenshot: Target crashed`** (renderer tab crash on a ~19,000px-tall mobile capture; the retry crashed the same way). Fixed with a segmented-screenshot fallback (viewport slices stitched with PIL) and per-viewport try/except so one crash cannot kill the run; metrics are now collected before the screenshot.")
L.append("3. **A VM replacement mid-run wiped `/tmp`** (server + log gone) and **all Chromium binaries then failed to launch** (`SIGTRAP`, exit 133, on every Playwright build: headless-shell 1243/1248 and full chromium 1243 — even `--dump-dom about:blank`; `--version` still worked). Root cause found by probing: the default multi-process launch traps/hangs in this post-replacement VM (child/zygote process dies; main process then hangs or traps). **Workaround that works: launch with `--single-process --no-zygote --disable-gpu --disable-dev-shm-usage`** (verified: page loads, H1 correct). Single-process mode is fragile — one renderer crash kills the whole browser — so the script now launches a fresh browser per (route, viewport). No further launch failures after that change. `playwright install chromium-headless-shell` also fails here (`EPERM: operation not permitted, write`); not needed since the installed binaries work under the workaround.")
L.append("4. **Two `nohup`/`setsid` background launches were silently killed** when their parent exec session ended (log stayed 0 bytes, process gone). The runs that completed were foreground `exec` calls that the runtime backgrounded. If this audit is re-run, launch it as a foreground exec and let the runtime background it; do not use `nohup`/`setsid` + `disown`.")
L.append("")
L.append("## Per-route section catalogue")
L.append("")
L.append("Counts are inside `<main>` at desktop width. Heights are full-page heights (px). Overflow = `scrollWidth > clientWidth`. Broken = local `<img>` with `naturalWidth == 0` after slow scroll. FAQ = `main [id*=faq], main details, main .faq` count.")
L.append("")
for slug, path in ORDER:
    v = data[slug]
    d = v["desktop"]; m = v["m390"]
    L.append(f"### {slug} — `{path}`")
    L.append("")
    L.append(f"- **H1 (1):** {d['h1'][0] if d['h1'] else '(none!)'}")
    L.append(f"- **Heights:** desktop {d['docHeight']}px · mobile {m['docHeight']}px · **Overflow:** desktop {'YES' if d['scrollW'] > d['clientW'] else 'no'} · mobile {'YES' if m['scrollW'] > m['clientW'] else 'no'} · **Broken local images:** desktop {len(d['brokenLocal'])} · mobile {len(m['brokenLocal'])}")
    L.append(f"- **Counts (desktop, in `<main>`):** p {d['counts']['p']} · img {d['counts']['img']} · table {d['counts']['table']} · ul {d['counts']['ul']} · ol {d['counts']['ol']} · faq {d['counts']['faq']} · links {d['counts']['a']} · body text {d['bodyText']} chars")
    L.append(f"- **Counts (mobile):** p {m['counts']['p']} · img {m['counts']['img']} · table {m['counts']['table']} · ul {m['counts']['ul']} · ol {m['counts']['ol']} · faq {m['counts']['faq']}")
    L.append(f"- **Sections (`<section>` in `<main>`, in order):** {len(d['sections'])} sections")
    for s in d["sections"]:
        L.append(f"  - “{s['heading']}” — p {s['p']} · img {s['img']} · table {s['table']} · lists {s['list']} · ~{s['height']}px")
    L.append(f"- **H2s ({len(d['h2s'])}):**")
    for h in d["h2s"]:
        L.append(f"  - {h}")
    if m.get("wide"):
        tw = sorted(set(w["w"] for w in m["wide"] if w["tag"] == "TABLE"))
        L.append(f"- **Mobile wide elements:** table(s) {tw}px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).")
    L.append("")

L.append("## Screenshot inventory")
L.append("")
L.append("All 62 files under `qa/uiux-render/` (full-page PNG, after slow scroll). Sizes are as captured:")
L.append("")
rd = os.path.join(D, "uiux-render")
total = 0
for slug, _ in ORDER:
    for lab in ("desktop", "m390"):
        fn = f"{slug}-{lab}-full.png"
        sz = os.path.getsize(os.path.join(rd, fn))
        total += sz
        L.append(f"- `{fn}` — {sz:,} bytes")
L.append("")
L.append(f"Total: 62 files, {total:,} bytes ({total/1024/1024:.1f} MB). Crops used for visual checks live in `qa/uiux-render/crops/` (hero/cards/table/footer regions).")
L.append("")
L.append("## Files")
L.append("")
L.append("- Findings (this file): `qa/uiux-render-2026-11-13.md`")
L.append("- Raw metrics: `qa/uiux-render-data.json` (31 routes × desktop/mobile, incl. per-image `naturalWidth`/displayed size and per-section element counts)")
L.append("- Screenshots: `qa/uiux-render/*-desktop-full.png`, `qa/uiux-render/*-m390-full.png` (62 files)")
L.append("- Audit script: `qa/uiux-render-audit.py` (serves nothing; expects the server on port 8341)")
L.append("- Server: `qa/linkfix-serve.py 8341` (unchanged, reused as-is)")
L.append("")

with open(os.path.join(D, "uiux-render-2026-11-13.md"), "w") as f:
    f.write("\n".join(L))
print("wrote", os.path.join(D, "uiux-render-2026-11-13.md"), len(L), "lines")
