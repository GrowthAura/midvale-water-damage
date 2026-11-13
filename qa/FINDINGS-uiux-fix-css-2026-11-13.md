# Midvale UT — Stage 1 UI/UX CSS Fixes: Verification Findings

**Date:** 2026-11-13 · **Worker:** CSS FIX worker (Stage 1 UI/UX round)
**Scope:** local only — no push, no deploy, no token, no DNS, no MEMORY.md edits.
**Files touched (only):** `app/globals.css` (3 CSS fixes + comment updates),
`lib/content.ts` (1 stale comment). `lib/pages-data.json` untouched,
no image file touched, no other chat.
**Method:** `npm run export`, served `out/` on `/midvale-water-damage/` at
`http://127.0.0.1:8345/midvale-water-damage/` (`qa/linkfix-serve.py 8345`;
the port-8341 server was left alone). Playwright Chromium 153
(`--single-process --no-zygote --disable-gpu --disable-dev-shm-usage`,
fresh browser per route/viewport — see "Script errors"). Site identity
confirmed before measuring: H1 `24/7 Water Damage Restoration in Midvale,
UT 84047`, phone `(385) 337-3560`, HTTP 200.
**Raw data:** `qa/uiux-fix-css-verify-2026-11-13.json` (31 routes × 320x568 /
320x844 / 390x844 / 1440 + table inventory + Magna fade probe),
`qa/uiux-fix-textcheck-2026-11-13.json` (no-word-change check).
**Scripts:** `qa/uiux-fix-css-verify-2026-11-13.py`,
`/tmp/uiux_fix_shots.py`, `/tmp/uiux_fix_textcheck.py`,
`/tmp/scroll_probe.py`, `/tmp/scroll_probe2.py`, `/tmp/scrolltest.html`.
**Screenshots:** `qa/uiux-fix-magna-table-390.png`,
`qa/uiux-fix-home-cards-1440.png`, `qa/uiux-fix-home-cards-390.png`,
`qa/uiux-fix-hero-320-worst.png`.

## Verdict: all 4 fixes VERIFIED — 0 reverted, 0 open

| # | Fix | Outcome |
|---|-----|---------|
| 1 | H1 hierarchy at 320px (H1 24px < H2 28px) | **FIXED and KEPT** — H1 30px ≥ H2 28px on 31/31 @320; Button 2 hard constraint holds on 31/31 (worst 554.2px ≤ 568px, 13.8px headroom — thin, see note) |
| 2 | Home service-card grid orphan (16 cards, 3 cols → 1-card last row) | **FIXED** — 4 cols ≥1280px, 4 rows × 4, no orphan; equal heights per row; areas grid untouched |
| 3 | Mobile table scroll cue (no visual cue for 3rd column) | **FIXED** — pure-CSS right-edge fade, on only while the table overflows and more content lies right; off at max scroll and on fitting tables |
| 4 | Stale comment in `lib/content.ts` ("21 heroes") | **FIXED** — now "31 heroes" (folder holds 31 files, verified) |

## Fix 1 — H1 hierarchy at 320px: FIXED and KEPT (no revert needed)

**What changed** (`app/globals.css`, `@media (max-width: 360px)` block only —
nothing changes at 390px or desktop):
- `h1 { font-size: 24px; }` → `30px` (≥ H2's 28px at this width).
- Compensation at the same width only, paid out of the hero stack above the
  buttons: hero top padding 16px → 8px (`.hero` and `.hero-photo`),
  breadcrumb margin-bottom 10px → 6px, eyebrow margin-bottom 4px → 2px,
  `.hero-buttons` margin-top 8px → 4px — 18px saved in total.
- The stale P2-2 comment ("worst Button 2 bottom 493px") updated to the new
  measured 554.2px. (Production build strips CSS comments — verified 0
  comment strings in `out/_next/static/css/*.css` — so the comment edit
  cannot change the built output.)

**Measurements (before → after, from `qa/uiux-css-2026-11-13.md` + this run):**

| Metric | Before | After |
|---|---|---|
| H1 size @320 | 24px (H2 28px — inversion) | **30px** on 31/31, H2 28px on 31/31 — hierarchy restored (H3 24px; the 3 legal pages have no H3) |
| H1 size @390 / @1440 | 34px / 44px | 34px / 44px — unchanged |
| Button 2 bottom @320x568, worst | 497.2px (condo + spring-snowmelt; 70.8px headroom) | **554.2px** (`/condo-apartment-water-damage`, H1 6 lines; next: frozen-pipes 530.4px, then three routes at 516.7px) — **0 routes > 568px** |
| Button 2 visible scroll-0 @320x568 | 31/31 | 31/31 |
| Button 2 visible scroll-0 @320x844 | 31/31 | 31/31 |
| Button 2 visible scroll-0 @390x844 | 31/31 (worst 766.8px) | 31/31 (worst 766.8px — **unchanged**) |
| Button sizes @320, worst route | 272×48 both | 272×48 both (Button 1 bottom 490.2, Button 2 bottom 554.2 — still exactly equal) |

**Headroom note (owned plainly):** the 18px compensation did not fully cover
the H1 growth on the longest H1s — condo's H1 is 6 lines at 30px, so its
Button 2 moved +57.0px (497.2 → 554.2). The hard constraint (≤568px) still
holds on all 31 routes, but headroom is now **13.8px** on the worst route,
down from 70.8px. The measurement is deterministic in this Chromium
(system fonts, no webfont variance), and the value was re-measured on the
final build — but any future change that adds even ~14px above the buttons
at ≤360px on the condo page would break it. No revert was needed: the
constraint holds, so per the task the fix stays.

**Visual check:** `qa/uiux-fix-hero-320-worst.png` (condo @320x568) — H1
reads clearly larger than section headings, both buttons fully visible at
scroll-0, breadcrumb truncated to one line, eyebrow 2 lines. Clean.

## Fix 2 — Home service-card grid orphan: FIXED

**What changed** (`app/globals.css`, appended at end of file):
```css
@media (min-width: 1280px) {
  #services .card-grid { grid-template-columns: repeat(4, 1fr); }
}
```
Scoped to `#services` so the 3 location cards keep their clean single row
of 3 (they are a separate `.card-grid` in `#areas`).

**Measurements (before → after):**

| Metric | Before | After |
|---|---|---|
| Service grid @1440 | 3 cols, 16 cards, rows 3/3/3/3/3/1 — last row 1 card alone (480.8px tall) | **4 cols, 16 cards, rows 4/4/4/4 — no orphan** |
| Row heights @1440 (per row, equal within row) | 545.5 / 513.1 / 483.1 / 513.2 / 513.1 / 445.1* | **620.8 / 558.5 / 618.5 / 526.2** (one height value per row) |
| Card width @1440 | ~354px | 247px each, all rows |
| Card image height @1440 | 177px | 137.8px, uniform (16:9, `object-fit: cover`, no distortion) |
| Location cards (`#areas`) @1440 | 3 cols × 3, heights 445.1 | **unchanged**: 3 cols × 3, heights 445.1, widths 338.7, img 189.4 |
| Homepage overflow @320 / @390 / @1440 | 0 | 0 |

\* baseline row heights from the audit; the 445.1 row was the location cards.
**Visual check:** `qa/uiux-fix-home-cards-1440.png` — 4-column first row,
equal heights, images fit. `qa/uiux-fix-home-cards-390.png` — homepage
clean at 390 (single-column cards, image fits, no overflow; the sticky call
bar at the bottom is the normal fixed-bar behaviour). Grid rules at ≤900px
(2 cols) and ≤600px (1 col) are untouched by the new ≥1280px rule.

## Fix 3 — Mobile table scroll cue: FIXED

**What changed** (`app/globals.css`, `.table-wrap`): pure CSS, no added text,
no added words, no markup change. The wrapper is now `display: flex` with
`container-type: scroll-state`; the table is `flex: 0 0 auto`; a `::after`
is a sticky flex item (`position: sticky; right: 0; flex: 0 0 56px;
margin-left: -56px; align-self: stretch; pointer-events: none`) pinned to
the visible right edge, carrying a two-layer fade — a white fade (reads over
the dark pine header row) over a pine-tinted shadow (reads over white/mist
rows). `@container scroll-state(scrollable: right)` switches it on only
when the wrapper can still scroll right; base opacity is 0. Fallback: on
browsers without scroll-state queries the cue simply never shows and tables
stay swipeable exactly as before.
**Mechanism proven before landing** (Chromium 153, `CSS.supports
('container-type','scroll-state') === true`): on a scratch replica
(`/tmp/scrolltest.html`, `scroll_probe2.py`), the fade's opacity was 1 at
scroll 0, 1 mid-scroll, 0 at max scroll, and 0 on a fitting table; the
screenshot showed the fade pinned at the visible right edge while scrolling.
(First probe read 1 at max scroll — a timing artifact: the query updates
asynchronously after scrolling; the re-probe with a 500ms settle showed the
correct 0.)

**Measurements on the real site @390 (worst case Magna, table 630px in a
342px box, max scroll 288):**

| State | `::after` opacity |
|---|---|
| Scroll 0 (more content right) | **1** |
| Mid-scroll (100px) | **1** |
| Max scroll (288px, nothing more right) | **0** |

All-route inventory @390 (43 `.table-wrap` instances across 31 routes):
**32 overflowing tables — fade ON at scroll-0 on 32/32; 11 fitting tables —
fade OFF on 11/11.** The negative-margin flex item adds no scrollable
overflow of its own (Magna `scrollWidth` still 630 = table width).
**Visual check:** `qa/uiux-fix-magna-table-390.png` — the third column
("Supply pi…") fades into the gradient at the right edge across the dark
header row and the body rows; the cue is clearly perceivable.

## Fix 4 — Stale comment in `lib/content.ts`: FIXED

Line ~383: `// image per page (21 heroes, 0 repeats)` → `(31 heroes,
0 repeats)`. Number only; the "19 cards" figure in the same comment is
still correct (16 service + 3 location cards) and was left alone.
Verified: `public/images/heroes/` holds **31 files**.

## Guards — all verified on the final build

| Guard | Result |
|---|---|
| Overflow | **0 on 31/31 @320, 31/31 @390, 31/31 @1440** (`scrollWidth − innerWidth`) |
| Button 2 scroll-0 | 31/31 @320x568 (worst 554.2 ≤ 568), 31/31 @320x844, 31/31 @390x844 |
| Contrast | **0 pairs below AA @1440**; worst ratio **5.65:1** (white on copper-dark `#9d5418`, header phone / Button 1 / sticky bar; and copper on white brand line) — unchanged from baseline |
| H1 count | **1 per page on 31/31 at 320, 390 and 1440** |
| Data hash | `lib/pages-data.json` sha256 **21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f** — unchanged |
| Content words | **0 changed.** Proof: new build's `<main>` `innerText` length matches the pre-fix render audit's recorded `bodyText` on **31/31 routes**; H1 strings 31/31 identical, H2 lists 31/31 identical, titles 31/31 identical (`qa/uiux-fix-textcheck-2026-11-13.json`). All 32 `out/*.html` hashes changed after the export, but only because the CSS asset filename hash changed (`e5629849076b4e10.css` → `03d0702a217810f6.css`) plus the build ID — the rendered words are proven identical by the text check above. Source diff confirms only `globals.css` + one comment in `content.ts` changed. |
| FAQ | Untouched — static Q&A by design (accepted, not a defect). |
| Footer Maps embed | Untouched — VM tunnel failure is environmental, not a defect. |

## Script errors (owned plainly)

1. **First verification run died mid-1440-pass** (`TargetClosedError`:
   browser closed) — single-process mode is fragile; one renderer crash
   kills the whole browser, and the JSON was only saved at the end, so the
   320/390 measurements were lost. Rewrote the script: fresh browser per
   (route, viewport), retry once, incremental save after every route.
2. **Screenshots step in the rewritten run also hit a browser close** —
   the Magna table screenshot had already saved; retook the other two
   (`/tmp/uiux_fix_shots.py`, fresh browser per shot). All 3 screenshots
   exist and were viewed.
3. **First scroll-state probe misread max-scroll opacity as 1** — the
   query updates asynchronously after scrolling; re-probe with a 500ms
   settle showed the correct 0 (see Fix 3).

## Files

- Findings (this file): `qa/FINDINGS-uiux-fix-css-2026-11-13.md`
- Raw verification data: `qa/uiux-fix-css-verify-2026-11-13.json`
- No-word-change data: `qa/uiux-fix-textcheck-2026-11-13.json`
- Script: `qa/uiux-fix-css-verify-2026-11-13.py`
- Screenshots: `qa/uiux-fix-magna-table-390.png`,
  `qa/uiux-fix-home-cards-1440.png`, `qa/uiux-fix-home-cards-390.png`,
  `qa/uiux-fix-hero-320-worst.png`
- Served for verification on port 8345 (stopped after the run); the
  port-8341 server was not touched.
