# BATCH 2 OPTIMIZATION CYCLE 3 — FINDINGS (coordinator synthesis)

**VERDICT: CYCLE 3 CLOSED — READY. PROBLEMS 0 (P1 0 / P2 0 / P3 0) on the site.**
Independent re-verification by a fresh agent (`qa/FINDINGS-opt-cycle3-reverify-2026-11-14.md`)
closed READY with PROBLEMS 1 (P1 0 / P2 0 / P3 1) — the single P3 was a findings-text
correction (Maps note reason), NOT a site defect; it is fixed below (§5) and in §3's flag
count. All coordinator claims below are measured, not asserted; the re-verifier re-measured
them with its own scripts, several to the exact integer.

- Site: Midvale UT water damage, 31 routes, Next.js static export. Cycle 3 export: `out-cycle3/`
  (Pages subpath build, same base as `out-cycle2/`). LOCAL ONLY — no push/deploy/token/DNS.
  Live site untouched (still the Cycle 1 close build on Cloudflare Pages + GitHub Pages).
- Data gate: `lib/pages-data.json` sha256
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — UNCHANGED
  through the whole cycle (verified at build + at every check; any change would have been a STOP).
- Content 1001% verbatim. No word changed, nothing invented.

## 1. TWO-WIDTH MOBILE CROPS (the cycle's core work — CLOSED)

**Problem (measured, not assumed):** the Cycle 2 390-matched `-m` crop degrades across the
481–767px range — mean visible fraction **0.657** (per-width: 0.921 @481 / 0.767 @560 /
0.614 @640 / 0.527 @700 / 0.455 @767). The task's "56–74%" framing checks out as the
481–767 mean, but the per-width breakdown shows it is NOT uniform: the `-m` crop is still
excellent at 481 (0.921) and poor at 767 (0.455).

**Measurement first (real Chromium, `qa/opt3-measure-mid.py`, `qa/opt3-slots-mid.json`):**
hero-box aspect (w/h) across all 31 routes: @390 mean 0.403 (0.315–0.798) / @481 mean 0.548
(0.450–0.984) / @560 mean 0.698 (0.563–1.145) / @640 mean 0.877 (0.684–1.546) / @700 mean
1.019 (0.825–1.691) / @767 mean 1.172 (0.977–1.853). The box aspect grows fast with viewport
width because hero height is set by content (H1 + intro + buttons + trust chips), so short
pages (the 3 legal pages: box 489px tall) are already ~1.0 wide at 481.

**Design decision (data, not the naive scheme):** a blanket `-mid` source at `<=767px` would
REGRESS two widths — at 481 the mid crop shows 0.678 vs the `-m` crop's 0.921, and at 767
it shows 0.659 vs the landscape file's 0.782. The per-page scheme below never regresses any
page at any width: at every width each page serves the file with the best visible fraction
(visible = min(a,Ab)/max(a,Ab), object-fit: cover; ties prefer the wider file).
- **Mid crop:** fixed 3:4 (aspect 0.75), slice width round(1066×0.75) = 800px, file 800×1066,
  WebP q82. 0.75 is the geometric-mean optimum for the mid range (box aspects ~0.55→~1.0).
  Same photo as the hero, same x-offset as the Cycle 2 `-m` crop (`qa/opt2-crop-offsets.json`,
  incl. contact x0=120) — same subject centering. 28 files (not 31): the 3 legal pages never
  win with the mid crop (their boxes are already ~1.0 at 481; landscape beats mid everywhere
  above ~519), so they get no `-mid` file and no `-mid` source — no dead weight in the export.
- **Breakpoints per page (`lib/hero-crops.ts`, from the measured grid):** `-m` applies to mMax
  (475–575 by page); `-mid` applies to midMax (659–767, 28 pages; 11 pages keep it to 767);
  landscape above. Legal pages: mMax 534, midMax null — `-m` ≤534, landscape above.
- **Implementation (template chrome only):** `components/site.tsx` PhotoHero — two `<source>`
  elements with per-hero media queries from `lib/hero-crops.ts` (fallback mMax 480 / midMax 767
  if a slug is ever missing); `<img>` srcset 800w/1600w unchanged; same alt, same photo, no
  layout change. Verified in the built HTML: home shows `(max-width: 534px)` → `-m` +
  `(max-width: 744px)` → `-mid`; disclaimer shows only the `-m` source (≤534px), no `-mid`.

**Files:** 28 × `<slug>-mid.webp` (800×1066, WebP q82, bytes min 28,834 / max 117,684 /
mean 72,968; total 2,043,092 B). EXIF/XMP/IPTC/ICC/GPS/MakerNotes/IFD0 = 0 on all 28
(exiftool, per-file check). Export now holds 273 image files (107 main + 138 Cycle 2 variants
+ 28 mid). No new photos — crops of this site's own heroes, so the reuse question is inherited
from the already-cleared sources; the fresh-disk net was still run (§3).

## 2. PER-PAGE CROP ASPECT RE-CHECK (CLOSED — 0 fixes needed)

**Raw mid crops (viewed full-size, contact sheets `qa/opt3-mid-sheet1-4.png`): 28/28 PASS.**
Subject in frame, alt-exact on every crop: about (crew + house + truck), basement (worker +
pump), snowmelt (downspout + pooling), burst-pipe (spraying copper), can-mold (moldy wall +
hose), ceiling (sagging ceiling + bucket), commercial (restaurant + air mover), condo (2
workers + ladder + leak + bucket), contact (man on phone + 2 air movers — the x0=120 re-crop
carries over, crew fully in frame), cottonwood (snowy canyon + houses), crawl-space (worker +
headlamp), emergency (crew + hoses + pump), frozen-pipes (ice-crusted burst pipe), hardwood
(kitchen + mats), home (crew + extraction rig), magna (Main Street storefronts), contacts
(night emergency truck), mold (hazmat + containment), sewage (hazmat crew), south-salt-lake
(wet street + apartments), storm (flooded street), swamp-cooler (rooftop cooler + wet roof),
upstairs-unit (ceiling drip + sofa), water-damage-repair (empty room, wood floors),
water-heater (heater + leak), water-leak-detection (thermal camera), window-well (well +
inflow), winterize (snow-covered cooler). No offset shift needed anywhere.

**Rendered heroes (element screenshots, `qa/opt3-hero-shots.py`): 31/31 @390 + 31/31 @600 PASS.**
At 390 the `-m` crop still shows the right subject behind the shade on every page (contact
re-crop confirmed in render; legal pages' short heroes render fully covered — the white
blocks in the contact sheets are sheet-layout padding under shorter panels, confirmed by
viewing `privacy-policy.png` + `disclaimer.png` individually at full size). At 600 the `-mid`
crop shows the right subject on all 28 pages; the 3 legal pages show the wider landscape
file at 600, as designed (their midMax is null).

**Measured visible fraction (rendered boxes + serving-file aspects, `qa/opt3-verify-cycle3.py`):**
- @390: min 0.630 / max 1.000 / mean **0.749** — EXACTLY Cycle 2's numbers (0.630/1.000/0.749).
  No regression at 390.
- @600: min 0.788 / max 0.992 / mean **0.922** vs the Cycle 2 build's 0.525/0.774/0.671
  at the same width — mean +0.251 (+37% relative), worst page 0.525 → 0.788.
- Mean across 481–767 (modelled from measured boxes): -m 0.657 → per-page best-file scheme
  ~0.84 (the scheme picks the max of the three files at every width).

**Transfer (hero, real Chromium):** @390 1× mean 51,418 B (identical to Cycle 2 — the `-m`
files are untouched); @481 1× mean 52,134 B; @600 1× mean 68,989 B (mid files: taller crop,
more pixels — +17.5 KB vs the `-m` file at the same width, the honest price of +0.25 visible
fraction on the LCP image); @767 1× mean 56,177 B; @1440 1× mean 120,333 B (identical to
Cycle 2). The 11 pages that keep `-mid` to 767 pay up to a 1.92× upscale at 767 2× (800px
file in a 1534-device-px slot) — source-limited (a 0.75 slice of a 1600×1066 photo is at most
800px wide); photographic hero under a dark shade, accepted, recorded here.

## 3. REUSE NETS (fresh-disk reads at install time — CLEAR)

`qa/opt3-reuse.py` (adapted from the Cycle 2 re-verifier's scoped net) + resume runs
(`qa/opt3-reuse-resume.py`, `qa/opt3-reuse-upstairs.py` — the main run was killed at 23/28
by a VM replacement mid-scan; the 5 + 1 remaining targets were re-run fresh, same corpus).
28/28 mid targets vs a fresh-disk corpus of **2,998** other-site `*/public/images` files
(md5 + aHash8, Pool(4); aHash16 + viewed-pixel adjudication for aHash8 ≤ 12). Filename net
(Midvale hero slugs in the corpus): **0**. Logs: `qa/opt3-reuse.log`,
`qa/opt3-reuse-resume.log`, `qa/opt3-reuse-upstairs.log`; results `qa/opt3-reuse.json` (+
resume/upstairs), summary `qa/opt3-reuse-summary-main.json` /
`qa/opt3-reuse-summary-resume.json`.

- **md5 hits: 0/28.** No mid file is byte-identical to any photo on any other site.
- **aHash8 ≤ 12 flags: 11/28 targets flagged, 99 flag entries in the top-10-per-target
  lists my script stored** (`close[:10]` truncation — the re-verifier's full count is 834
  entries / 633 distinct photos; headline figures identical). Min aHash8 **4**
  (swamp-cooler vs Glenpool welcome sign), min aHash16 **33** (water-damage-repair vs Cape
  Coral area-ne). Same-photo band is aHash16 0–2/256; different-photo band is 25+/256 —
  every flag sits in the different band.
- **Viewed-pixel adjudication (9 distinct flagged photos, full-size side-by-side,
  `qa/adj-*.png`): ALL DIFFERENT.** Tulsa commercial drying equipment (office, blue air
  movers) vs about (crew + house at dusk); Biohazard front porch (green lawn, white house)
  vs snowmelt (snow piles + downspout); Plano mopping-tile-floor vs condo (workers + ladder
  + leak); Catoosa port wharf (tugboat + barge + crane) vs snowmelt; Cape Coral canal homes
  (palms + boat + mansions) vs snowmelt; Glenpool welcome sign (stone sign) vs swamp-cooler
  (rooftop unit); Cape Coral area-ne (waterway + skyline) vs water-damage-repair (empty
  room); Plano laundromat (washing machines) vs window-well (snowy well + inflow); Tulsa
  ceiling stain (peeling ceiling + floral wallpaper) vs water-damage-repair. The aHash8
  flags were coarse-hash collisions on dark/wet/outdoor scenes. The remaining unviewed
  flags all have aHash16 ≥ 33 (different band) and are weaker than the viewed ones.
- **Verdict: NETS CLEAR.** The mid crops are crops of this site's own already-cleared hero
  photos; nothing in them is reused from any past site.

## 4. VERIFICATION OF THE CYCLE 3 BUILD (coordinator, real Chromium, `qa/opt3-verify-cycle3.py` + `qa/opt3-scroll-check.py` + `qa/opt3-static.py`)

Served `out-cycle3/` (port 8326) vs Cycle 2 `out-cycle2/` (8325). 31 routes × 390/481/560/640/
700/767/800/1440 (1× + 2× where relevant), plus slow-scroll + targeted re-check.

- **Hero file selection: 0 mismatches** — all 31 routes × 13 viewport/DPR combos served exactly
  the file the per-page breakpoints predict (`-m` / `-mid` / `-800` / main 1600w).
- **H1: 31/31 = 1. Overflow: 0 @320 / @390 / @481 / @600 / @767 / @1440. Console errors: 0.**
  Failed responses (≥400) across all passes: 0.
- **Button 2: 31/31 @320 worst 552.19 px (condo, unchanged from Cycle 1/2) + 31/31 @390 worst
  773.06 px (condo, unchanged).** Headroom holds.
- **Cards/bodies after slow scroll:** 16/19 cards + 44/57 bodies on first pass (same lazy +
  fast-scroll artifact as Cycle 2); **targeted re-check with 2.5 s settle: 3/3 missing cards +
  13/13 missing bodies loaded, 0 failed** (`qa/opt3-scroll-recheck.json`) — all 107 images load.
  Cards @1440 1× all `-340`; bodies @1440 1× all `-400`; hero @800px viewport = `-800.webp`
  (mold-remediation, 56,492 B, unchanged).
- **Full regression (`qa/opt3-static.py`, same script lineage as the Cycle 2 re-verifier):**
  routes 31, sitemap 31 locs = routes exactly, H1 all 1, status 200, canonicals match Pages
  base; fullness 31/31 FULL (total main words 46,377 — identical to Cycle 2's count; thinnest
  disclaimer 309); verbatim 0 missing (3,331 doc segments, 2,900 unique + 92 trust chips + 31
  eyebrows); FAQ 142/142; tables 43/43; links 0 broken / 0 self-links / 0 orphans; schema 254
  blocks, 0 parse errors, contentUrls 107/107 (mid variants correctly NOT in schema — they are
  the same images at another crop, Cycle 2 precedent); localhost 1 (polyfills.js framework
  string only); double-slash 0; main imgs 135 (107 + 28 mid) + variants 138, 0 missing in
  export; dims verified (28× 800×1066 mid, 31× 1600×1066, 31× 800×533, 28× 533×1066 + 3×
  780×978 -m, 19× 340×192, 57× 400×225); sewage-3 sha + alt unchanged from Cycle 2.
- **Data gate:** sha `21c6e7f2…` verified at build, before checks, and after checks — unchanged.

## 5. DELIBERATELY LEFT (not problems)

- **Basement-flooding-cleanup-3 aerial stays — DO NOT TOUCH.** Still pending HIS call (generated
  image, honestly labelled, vs accept the aerial). Untouched this cycle (verified: file + sha
  unchanged, no edit to it or its alt).
- **Mold-remediation-2 (washed-out) + water-damage-repair-1 (near-white)** — still as Cycle 1
  left them (subject-correct, alt-exact, no better candidate found in prior searches).
- **480w mid variant (1× DPR):** at 481–600 1× the 800px mid file is oversized (~73 KB where
  a ~480px file would be ~40 KB). Same single-file trade Cycle 2 accepted for `-m` (780px
  file at 390 1×). A `480w` srcset candidate for the `-mid` source is a genuine Cycle 4 item
  (28 more files); not done here — the cycle's scope was the two-width crop itself.
- **1.92× upscale at 767 2×** for the 11 mid-to-767 pages (see §2) — source-limited, accepted.
- **Real LCP still unmeasured** — Chromium cannot reach live pages from this cell
  (ERR_TUNNEL_CONNECTION_FAILED; same as Cycles 1–2). The mobile-hero win is now twofold
  (Cycle 2: 135 KB → ~51 KB @390; Cycle 3: visible 0.671 → 0.922 @600 at ~69 KB). True
  real-user LCP needs an off-cell run or PageSpeed Insights (`qa/lcp-measure.py` is ready).
- **Footer Google Maps embed** — the iframe does not load in this VM's Chromium (zero
  google.com responses, empty iframe, requestfailed — the re-verifier proved curl DOES
  reach google.com and the embed URL, so the earlier "no google.com egress" reason was
  wrong; corrected here per P3-1). A real-network eyeball after push is still the remaining
  check. Same as Cycles 1–2. (Only the 3 location pages omit the embed, by template design.)
- **Carried from Cycles 1–2 (verbatim wins / accepted):** 12 over-cap anchors, breadcrumb
  double-link, single-item BreadcrumbList, breadcrumb 24px, repair-hero "Midvale home" alt on
  an Akron photo, card/body img attrs, picture breakpoint ≤700px is now per-page (475–767),
  mobile crop worst 63% @390 (condo, accepted in Cycle 2, unchanged).

## 6. FILES

- New images: `public/images/heroes/*-mid.webp` (28)
- Code: `lib/hero-crops.ts` (new, per-hero breakpoints), `components/site.tsx` (picture element
  only — two sources + slug lookup; no other change)
- Scripts + data: `qa/opt3-measure-mid.py`, `qa/opt3-slots-mid.json`, `qa/opt3-gen-mid.py`,
  `qa/opt3-variants.json`, `qa/opt3-mid-sheet1-4.png`, `qa/opt3-hero-shots.py`,
  `qa/opt3-hero-390/*.png` (31), `qa/opt3-hero-600/*.png` (31), `qa/opt3-hero-sheet-390-1/2.png`,
  `qa/opt3-hero-sheet-600-1/2.png`, `qa/opt3-hero-sheet-390-1a/1b.png`
- Verification: `qa/opt3-serve.py`, `qa/opt3-verify-cycle3.py`, `qa/opt3-verify-cycle3.json`,
  `qa/opt3-scroll-check.py`, `qa/opt3-scroll-check.json`, `qa/opt3-scroll-missing.json`,
  `qa/opt3-scroll-recheck.json`, `qa/opt3-static.py`, `qa/opt3-reuse.py`, `qa/opt3-reuse.log`,
  `qa/opt3-reuse.json`, `qa/opt3-reuse-resume.py`, `qa/opt3-reuse-resume.log`,
  `qa/opt3-reuse-resume.json`, `qa/opt3-reuse-upstairs.py`, `qa/opt3-reuse-upstairs.log`,
  `qa/opt3-reuse-upstairs.json`, `qa/opt3-reuse-summary-main.json`,
  `qa/opt3-reuse-summary-resume.json`, `qa/adj-*.png` (9 side-by-side adjudications)
- Export: `out-cycle3/` (Cycle 3 build; `out/` + `out-cycle2/` + `out-cloudflare/` untouched)
- Re-verification: `qa/FINDINGS-opt-cycle3-reverify-2026-11-14.md` (fresh agent — READY,
  PROBLEMS 1: P3-1 findings-text Maps reason only, fixed in §5; flag-count truncation noted
  in §3) + `qa/reverify3-*.py/json`, `qa/reverify3-adj/*.png` (11 adjudications),
  `qa/reverify3-maps.json`
- Review pack: `~/workspace/your_files/midvale-opt-cycle3-review.pdf` (62 pp, 62,405,165 B,
  pdfinfo-verified) + remote-storage link
  https://muse.ai/files/1300466579823511/2204282097172066/r1tlfx1f47xfzyi0xry7zf1a/midvale-opt-cycle3-review.pdf
  (expires 2026-11-16T10:04:12+00:00, HTTP 200 verified, full 62,405,165 bytes downloaded)
  + 62 PNGs in `~/workspace/your_files/midvale-opt-cycle3/` (129 MB). Manifest
  `qa/opt3-pack-manifest.json`: 62/62 full-page (0 stitched), brokenImgs 0, overflow 0,
  re-shoots 0. Note: the PDF is byte-identical in size to Cycle 2's (62,405,165 B) because
  the pack shoots only 1440 + 390, where the serving files are unchanged from Cycle 2 (the
  mid crops serve at 481–767) — the renders are pixel-identical at those widths, as designed.

## 7. WOULD ANOTHER CYCLE STILL FIND REAL IMPROVEMENTS?

Yes, small ones — the honest list for Cycle 4: (1) 480w mid variant for 1× DPR (~30 KB/page
saved at 481–600 1×); (2) re-run the Pexels search for basement-3 / mold-2 / repair-1
replacements (new uploads land constantly; Cycle 2's kill-list may not hold forever); (3) real
LCP via PageSpeed Insights once the Cycle 2/3 build is live (the lab numbers are all we can
do from this cell); (4) the footer Maps eyeball after push. Nothing here is a defect — the
site is READY FOR CYCLE 3 CLOSE as it stands.
