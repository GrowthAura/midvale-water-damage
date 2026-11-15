# BATCH 2 OPTIMIZATION CYCLE 3 — INDEPENDENT RE-VERIFICATION (fresh agent)

**VERDICT: READY — PROBLEMS 1 (P1 0 / P2 0 / P3 1).** The single P3 is a wording
correction in the coordinator's findings note (Maps "no egress" reason), NOT a
site defect. Nothing blocks Cycle 3 close. No site file was modified; all
re-verification work lives under `qa/reverify3-*`.

- Site: Midvale UT water damage, 31 routes, Next.js static export. Cycle 3
  export `out-cycle3/` served on port 8326 (`qa/opt3-serve.py`); Cycle 2
  baseline `out-cycle2/` on 8325 (`qa/opt2-serve.py`). Both servers started by
  me, killed by PID afterwards (verified stopped). LOCAL ONLY.
- Data gate: `lib/pages-data.json` sha256
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — verified
  at start AND at end (after every check). MATCH both times. Content untouched.
- Method: my own fresh scripts, written from scratch (not the coordinator's):
  `qa/reverify3-static.py` → `reverify3-static.json`,
  `qa/reverify3-hero.py` → `reverify3-hero.json` (403 probes: 31 routes × 13
  viewport/DPR combos, real Chromium),
  `qa/reverify3-hero-shots.py` (retake, see probe artifacts),
  `qa/reverify3-scroll.py` → `reverify3-scroll.json`,
  `qa/reverify3-reuse.py` → `reverify3-reuse.json`,
  `qa/reverify3-maps.py` → `reverify3-maps.json`,
  `qa/reverify3-adj/adj-*.png` (11 side-by-side adjudications).

## PROBLEMS

### P3-1 — Coordinator's Maps note states the wrong reason (findings text only, not a site defect)
- `qa/FINDINGS-opt-cycle3-2026-11-14.md` §5: "Footer Google Maps embed — still
  unverifiable in this VM (no google.com egress)". The "no google.com egress"
  reason is wrong: from this VM, `curl https://www.google.com/` → 200, and the
  exact footer embed URL
  `https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed` → 301 →
  200 with real embed HTML (`#mapDiv`, final URL
  `https://www.google.com/maps/embed?origin=mfe&pb=…Midvale,+UT+84047`).
- What IS real: Chromium in this VM cannot load the iframe — my
  `reverify3-maps.py` run recorded ZERO google.com responses, iframe
  `innerLen 0`, and the scroll check logged the embed URL in `requestfailed`
  on 26 routes. So the in-browser map render remains unverified in this VM,
  but for a browser-network reason, not "no egress".
- Evidence: `qa/reverify3-maps.json`; curl transcript in this file's §5.
- Fix: correct the note's reason at the next findings touch; no site change.

## PER-CLAIM VERIFICATION TABLE (coordinator claim vs MY measurement)

| # | Coordinator claim | My measurement | Result |
|---|---|---|---|
| 1a | 28 `-mid.webp` files, 800×1066, WebP q82, in `public/images/heroes/` | 28 files; PIL: all 800×1066 WebP; bytes min 28,834 / max 117,684 / mean 72,968 / total 2,043,092 | CONFIRMED (byte-for-byte the stated min/max/mean/total) |
| 1a | Hero serves exactly the predicted file at 390/481/560/640/700/767/800/1440, 1×+2×, 31 routes | 403 probes, 0 mismatches vs `lib/hero-crops.ts` parsed by my own regex | CONFIRMED |
| 1a | Two `<source>` in `components/site.tsx` + img srcset 800w/1600w | Code read: 2 sources (`-m` to mMax, `-mid` to midMax, null-guarded) + img srcset `…-800.webp 800w, …webp 1600w`; built HTML: 28 routes have 2 sources, 3 legal have 1; media values match `hero-crops.ts` exactly on all 31 routes (0 mismatches); mMax 475–575, midMax 659–767 | CONFIRMED |
| 1b | Visible fraction @390 0.630/1.000/0.749; @600 0.788/0.992/0.922 (vs C2 @600 0.525/0.774/0.671) | From MY hero-box + natural-size measurements: C3 @390 0.630/1.000/0.749; C3 @600 0.788/0.992/0.922; C2 baseline (probed on 8325 myself) @600 0.525/0.774/0.671. Worst page both builds: winterize @600 (0.525 → 0.788). Per-width C3 means: 0.921 @481, 0.869 @560, 0.928 @640, 0.818 @700, 0.763 @767; mean across 481–767 = 0.87 (coordinator modelled ~0.84 — mine measures slightly better) | CONFIRMED (exact on the two headline widths) |
| 1c | Hero transfer means @390 51,418 B; @600 68,989 B; @1440 120,333 B | My transferSize means: @390 51,418; @481 52,134; @600 68,989; @767 56,177; @1440 120,333 | CONFIRMED (exact, all five widths incl. the two not in my task list) |
| 1d | All 28 mid crops viewed full-size — subject in frame, alt-exact | Viewed all 4 coordinator contact sheets + 4 files full-size myself (contact: man on phone + 2 air movers, crew fully in frame; condo: 2 workers + ladder + leak + bucket; snowmelt: downspout + pooling + snow; swamp-cooler: rooftop cooler + wet roof) — all PASS. Rendered heroes viewed by me @390 (home, contact, condo, disclaimer) and @600 (home, contact, condo, disclaimer): correct subject behind shade on every one; legal pages show landscape at 600 as designed | CONFIRMED |
| 1e | EXIF 0 on all 28 mid files (exiftool) | **Method substitution (owned): exiftool is NOT installed in this VM.** I used PIL `getexif()` (0 items) + raw WebP RIFF chunk parse (single `VP8 ` chunk) + byte scan for Exif/XMP/ICC/GPS/MakerNote markers — 0 hits on all 28 | CONFIRMED by substitute method (see probe artifacts) |
| 1f | 3 legal pages: no `-mid` file, no `-mid` source in built HTML | `disclaimer`/`privacy-policy`/`terms-of-use`: no `-mid.webp` on disk; built HTML has exactly 1 source (`-m` only, ≤534px); `midMax: null` only for these 3 in `hero-crops.ts` | CONFIRMED |
| 2 | `basement-flooding-cleanup-3.webp` deliberately untouched (aerial leafy suburb) | sha256 `3c3282f4…` identical across `public/`, `out-cycle2/`, `out-cycle3/`, `out/`; mtime 2026-11-13 14:56 (pre-Cycle 3); `<img>` tag byte-identical between cycle2/cycle3 HTML incl. alt "An aerial view of a leafy suburban neighborhood with detached houses along curving streets." | CONFIRMED |
| 3 | Reuse nets: md5 0/28; 11/28 targets aHash8≤12; min aHash8 4; min aHash16 33; 9 adjudications DIFFERENT | MY net (fresh disk, bigger corpus — see §reuse): md5 0/28; 11/28 targets flagged (same 11); min aHash8 4 (swamp-cooler vs Glenpool welcome sign — same pair); min aHash16 33 (water-damage-repair vs Cape Coral area-ne — same pair); MY 11 lowest-aHash16 pairs adjudicated full-size side-by-side — ALL DIFFERENT | CONFIRMED (see reuse § for the entry-count footnote) |
| 4 | Full regression (see table below) | All numbers reproduced exactly (see regression table) | CONFIRMED |
| 5 | Deliberately left: mold-2 washed-out + repair-1 near-white unchanged; no 480w mid variant; Maps unverifiable in VM | mold-remediation-2 + water-damage-repair-1 sha256 identical across public/cycle2/cycle3 (309a0270… / 65505557…); no `-mid-480` file anywhere, no 480w mid srcset; Maps: browser render unverifiable in VM — TRUE, but reason corrected (P3-1) | CONFIRMED except Maps reason (P3-1) |

## FULL REGRESSION (my own scripts, `out-cycle3/`)

| Check | Coordinator | Mine | Result |
|---|---|---|---|
| Routes 200 + H1==1 | 31/31 | 31/31 (status 200 all; H1==1 all; also H1==1 in every hero-probe combo) | PASS |
| Fullness (main words) | 31/31 FULL, total 46,377, thinnest disclaimer 309 | 31/31 FULL, total 46,377, thinnest (309, `/disclaimer`) | PASS exact |
| Verbatim vs `lib/pages-data.json` | 0 missing (3,331 segments) | 0 missing (my segment set incl. h1/intro/eyebrow/chips/blocks/tables/FAQ — BS-space + annotation normalised) | PASS |
| FAQ | 142/142 | 142/142 questions visible, 142/142 answers visible | PASS |
| Tables | 43/43 | 43 rendered / 43 expected | PASS |
| Links | 0 broken / 0 orphans / 0 body self-links | 0 broken / 0 orphans / 0 body self-links | PASS |
| Button 2 | 31/31 @320 worst 552.19px (condo); @390 773.06px (condo) | @320 worst 552.1875 (condo); @390 worst 773.0625 (condo); overflow 0 @320/@390 | PASS exact |
| Overflow | 0 @320/@390/@1440 (also @481/@600/@767) | 0 @320/@390/@481/@600/@767/@1440 | PASS |
| Console errors | 0 | 0 across all 403 route-combos (console error + pageerror listeners) | PASS |
| Failed responses | 0 | 0 failed asset/font/image responses; only failure observed anywhere is the Maps embed iframe in Chromium (VM-network artifact, P3-1) | PASS |
| Images after slow scroll | 107/107 | 107/107 main imgs loaded on FIRST pass (slow scroll + 2.5 s settle); 0 bad; no re-check needed | PASS |
| Images in export | 107 main + 138 variants + 28 mid = 273 | 273 image files in export; 273 referenced images, 0 missing; 19× `-340` cards, 57× `-400` bodies, 28× `-mid`, 31× `-800`, 31× main | PASS |
| Schema | 254 blocks, 0 parse errors, contentUrls 107/107 | 254 blocks, 0 parse errors, contentUrls 107 | PASS |
| Sitemap | 31 locs = routes | 31 locs, set-equal to routes (homepage trailing slash included) | PASS |
| Canonicals | Pages base `https://growthaura.github.io/midvale-water-damage/` | All 31 canonicals match exactly (incl. homepage trailing slash) | PASS |
| localhost | 1 (polyfills.js string only) | 1 hit, in polyfills.js framework string | PASS |
| Double-slash | 0 | 0 | PASS |
| 404 | bogus URL → 404, exactly 1 noindex | Bogus URL → HTTP 404 (verified by curl); `404.html` → 200 with exactly 1 `noindex` robots meta | PASS |
| Dims | 28× 800×1066 mid; 31× 1600×1066; 31× 800×533; 28× 533×1066 + 3× 780×978 `-m`; 19× 340×192; 57× 400×225 | All confirmed from disk with PIL | PASS |
| Extra: mold hero @800 1× | `-800.webp`, 56,492 B | `mold-remediation-800.webp`, transferSize 56,492 | PASS exact |
| Extra: 767 2× upscale | 11 pages keep `-mid` to 767, up to 1.92× upscale | Exactly 11 pages serve `-mid` at 767 2×; box 767 CSS px = 1,534 device px vs 800 px file = 1.92× | PASS (disclosed, accepted) |

## REUSE NET (my own run, `qa/reverify3-reuse.py` → `reverify3-reuse.json`)

- Corpus: **3,386** other-site `*/public/images` files (14 dirs incl. nested
  `…/site/public/images`, `…/publish-src2/…`, `…/repo/…`, `elyria-deploy-snapshot`;
  larger than the coordinator's 2,998 — strictly stronger net). Fresh-disk reads.
  My aHash is a from-scratch PIL/numpy implementation (imagehash is not
  installed); cross-checked on the two anchor pairs — it reproduces the
  coordinator's distances exactly (Glenpool a8=4; area-ne a16=33).
- **md5 hits: 0/28.** No mid file is byte-identical to any photo on any other site.
- **aHash8 ≤ 12 flags: 11/28 targets** (same 11 as coordinator), **834 flag
  entries** (633 distinct photo-keys after stripping size suffixes). The
  coordinator's "99 flag entries" is NOT a miscount of the same thing — their
  script stores only `close[:10]` per target (top 10 closest), so 99 is the
  truncated count; my 834 is the full count. No contradiction; the headline
  figures (11 targets, min a8 4, min a16 33) reproduce exactly.
- **Min aHash8: 4** (swamp-cooler vs Glenpool welcome sign). **Min aHash16: 33**
  (water-damage-repair vs Cape Coral area-ne). Same-photo band is aHash16
  0–2/256; different band 25+/256 — every flag sits in the different band.
- **Filename net (anchored, my fix — see artifacts): 136 hits.** These are
  generic service-slug collisions on other sites (e.g. Belleville's
  `burst-pipe-water-damage.webp`, `home.webp`, `mold-remediation.webp`). **0 of
  the 136 are aHash-flagged for their matching target** — same slug, different
  photo. Not reuse.
- **Viewed-pixel adjudication — MY 11 lowest-aHash16 pairs, full-size
  side-by-side (`qa/reverify3-adj/adj-*.png`): ALL DIFFERENT.**
  - about vs Elyria rental-blog hero (a8 12 / a16 76): crew+house at dusk vs daylight apartment block.
  - snowmelt vs Catoosa port wharf (11/42): downspout+snow vs tugboat+barge+crane.
  - commercial vs Plano mopping-tile-floor (9/64): restaurant+air movers vs mop+bucket close-up.
  - cottonwood vs Catoosa Blue Whale (9/47): snowy canyon+houses vs giant blue whale slide.
  - south-salt-lake vs Coweta aerial (11/53): wet dusk street+apartments vs green daylight suburb aerial.
  - storm vs Boynton wet tile floor (12/70): flooded night street+garage vs bright living room+air mover.
  - swamp-cooler vs Tulsa pipe geyser (8/38): rooftop cooler+wet roof vs street water-main burst.
  - upstairs-unit vs Boynton storm roof leak interior (12/74): **closest call — same
    scene type** (ceiling leak + sofa + bucket), but visibly different photos:
    different ceiling-damage pattern, grey 2-seater vs beige sofa, different
    room/window/palms, different bucket position. aHash16 74 = different band.
  - water-damage-repair vs Cape Coral area-ne (6/33): empty room/wood floors vs waterway+skyline.
  - window-well vs Collinsville Caney River banks (9/34): snowy well+inflow vs green river.
  - winterize vs N. Tulsa Greenwood Memorial Park (12/85): snow-covered cooler cover vs street+monument.
- **Verdict: NETS CLEAR.** Nothing in the 28 mid crops is reused from any past site.

## PROBE ARTIFACTS (owned plainly — all caught by my own sanity checks, all fixed, nothing hidden)

1. **Reuse script v1 — shadowed `ahash` def.** My edit added a new PIL/numpy
   `ahash` but left the old `imagehash`-based def below it, which overwrote the
   new one; `imagehash` is not installed, so every call returned None and the
   run reported "aHash8 computed: 0 / flags 0". Caught by the 0-count sanity
   check; deleted the stale def, fixed the corpus scope and filename net, and
   re-ran the whole net clean. The v1 md5 result (0 hits) was unaffected, but
   the full net was re-run anyway — the numbers in this file are from the
   clean re-run only.
2. **Reuse v1 filename net — substring false positives.** Plain `slug in
   basename` matching gave 413 hits (slug `home` matching
   `oklahoma-home-front-porch.jpg`, etc.). Fixed to anchored matching
   (basename equals slug, or starts with `slug + '-'`); clean re-run: 136
   anchored hits, 0 hash-flagged for their matching target.
3. **Hero screenshots v1 — trailing-slash 404s.** My first screenshot loop
   hardcoded trailing-slash routes (`/contact/`); the local python server 404s
   those for a flat `.html` export (sitemap locs are no-slash). All 14
   first-attempt shots were identical 404 pages. Retaken with no-slash routes
   (`qa/reverify3-hero-shots.py`); all 14 return 200. The hero-probe numbers
   were never affected (that script used sitemap routes).
4. **Scroll-check `requestfailed` handler missed 2 routes.** The Maps-embed
   failure was logged on 26 routes but not on `/disclaimer` and
   `/privacy-policy` — a handler-timing artifact (evaluate racing navigation).
   Grep is authoritative: the embed iframe IS present in their HTML (29/32
   html files contain it; only the 3 location pages lack it by design).
5. **EXIF method substitution.** `exiftool` is not installed in this VM, so the
   coordinator's exact tool could not be re-run. Substitute: PIL `getexif()` +
   raw WebP RIFF chunk parse + byte scan for Exif/XMP/ICC/GPS/MakerNote
   markers — 0 on all 28. The check itself is complete; only the tool differs.
6. **Coordinator "99 flag entries" is a top-10 truncation** (their script stores
   `close[:10]` per target). My full count is 834 entries. Headline figures
   agree; the summary number understates raw flag volume.

## CARRIED OBSERVATIONS (not problems)

- 1.92× upscale at 767 2× for the 11 mid-to-767 pages — source-limited, disclosed by coordinator, confirmed by me. Accepted.
- No 480w mid variant for 1× DPR at 481–600 — genuine Cycle 4 item, disclosed. Not done this cycle by design.
- Mold-remediation-2 (washed-out) + water-damage-repair-1 (near-white) still as Cycle 1 left them; shas unchanged (see claim 5). Still pending his call / a better candidate.
- Basement-flooding-cleanup-3 aerial still pending his call; untouched (see claim 2).
- Real LCP still unmeasured (Chromium cannot reach live pages from this cell); lab hero-transfer numbers are the available proxy. Same as Cycles 1–2.
- Footer Maps embed: endpoint answers 200 via curl, but the iframe does not load in this VM's Chromium (requestfailed, empty iframe) — a real-network eyeball after push is still the remaining check. Only the 3 location pages omit the embed (by template design, not a defect).
- Carried from Cycles 1–2 (unchanged, not re-litigated): 12 over-cap anchors, breadcrumb double-link, single-item BreadcrumbList, breadcrumb 24px, repair-hero "Midvale home" alt on an Akron photo, card/body img attrs, mobile crop worst 63% @390 (condo, accepted in Cycle 2, unchanged).

## FILES (mine)

- `qa/reverify3-static.py` / `qa/reverify3-static.json`
- `qa/reverify3-hero.py` / `qa/reverify3-hero.json`
- `qa/reverify3-hero-shots.py` / `qa/reverify3-hero-390/*.png` / `qa/reverify3-hero-600/*.png` (7 routes each, retaken)
- `qa/reverify3-scroll.py` / `qa/reverify3-scroll.json`
- `qa/reverify3-reuse.py` / `qa/reverify3-reuse.json`
- `qa/reverify3-maps.py` / `qa/reverify3-maps.json`
- `qa/reverify3-adj/adj-*.png` (11 side-by-side adjudications)
- `qa/FINDINGS-opt-cycle3-reverify-2026-11-14.md` (this file)
