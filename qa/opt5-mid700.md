# CYCLE 5 ITEM 1 — 700w MID VARIANT FOR 1× DPR (601–767px) — FINDINGS

**VERDICT: DONE + VERIFIED. 0 problems.** Real Chromium, locally served
`out-cycle5/` vs Cycle 4 baseline `out-cycle4/`. LOCAL ONLY — no push/deploy/
token/DNS. Live site untouched (still the Cycle 1 close build).

- Site: Midvale UT water damage, 31 routes, Next.js static export.
  Cycle 5 export: `out-cycle5/` (fresh temp-copy build, Pages subpath base).
- Data gate: `lib/pages-data.json` sha256
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` —
  UNCHANGED at every check (start, after install, after code edit, after
  build, after all verification). Any mismatch would have been a STOP; none
  occurred.
- `public/images/body/basement-flooding-cleanup-3.webp` sha256
  `3c3282f408f855f6fda99c8553102957a4177e30fe4fa6bfb5c7a91c20e1d68f` —
  UNCHANGED, untouched (pending his call).
- Content 1001% verbatim. No word changed, nothing invented. Visible main
  words total 46,377 — identical to Cycle 4.

## 1. WHAT CHANGED

- **New images (28):** `public/images/heroes/<slug>-mid700.webp`
  (700×933, WebP q82 method=6, total **1,744,378 B**), regenerated from the
  SAME Cycle 3 `-mid` crops (`<slug>-mid.webp`, 800×1066) with PIL Lanczos
  resize — same photo, same crop, same pixels; no re-crop from originals.
  One per mid page; the 3 legal pages (disclaimer, privacy-policy,
  terms-of-use — midMax null in `lib/hero-crops.ts`) get no variant, same
  as the Cycle 3/4 rule.
- **Comparison vs Cycle 4's measured manifest (`qa/opt4-candidates.json`
  ["700"]): byte-identical on all 28 files (delta 0 on every file, total
  delta 0).** Mean 62,299 B, total 1,744,378 B — exactly Cycle 4's measured
  numbers. No deviation to explain: the same resize (Lanczos, q82,
  method=6) from the same source files reproduces the same bytes.
  Saving vs the 800w `-mid` file: **298,714 B total, 10,668 B/file mean
  (14.6%)**; worst file cottonwood-heights-ut saves only 1,878 B (1.9%).
- **Code (1 line, template chrome only):** `components/site.tsx` PhotoHero —
  the mid `<source>` srcset is now
  `…/<slug>-mid600.webp 600w, …/<slug>-mid700.webp 700w, …/<slug>-mid.webp 800w`
  with `sizes="100vw"`. Breakpoints (`lib/hero-crops.ts`), the `-m` source,
  the `<img>` srcset, alts, layout: ALL untouched. (`variantSrc` is a plain
  `.webp` suffix replace, so `-mid700` resolves exactly like `-mid600`.)
- **EXIF: 0 on all 28** — raw RIFF/WebP chunk scan: every file carries only
  a `VP8 ` chunk (no EXIF / XMP / ICCP chunks), PIL `getexif()` empty,
  `info` keys only `background`/`loop`. NOTE: exiftool itself was
  unavailable in this VM at build time (apt lock held by process 806, and
  the package was not in the lists); the chunk scan + `getexif()` is the
  verification, and PIL-saved WebP carries no EXIF by construction.
- **Untouched:** `out/`, `out-cycle2/`, `out-cycle3/`, `out-cycle4/`,
  `out-cloudflare/` — verified 0 `-mid700.webp` files in any of them.

### Per-file bytes (700w vs 800w `-mid`)

| slug | 800w | 700w | saving |
|---|---|---|---|
| about | 77872 | 64682 | 13190 |
| basement-flooding-cleanup | 65344 | 54010 | 11334 |
| basement-flooding-spring-snowmelt-utah | 117684 | 102076 | 15608 |
| burst-pipe-water-damage | 88924 | 77634 | 11290 |
| can-mold-grow-in-utah | 94302 | 77262 | 17040 |
| ceiling-water-damage | 52896 | 43416 | 9480 |
| commercial-water-damage | 72466 | 60546 | 11920 |
| condo-apartment-water-damage | 69634 | 59372 | 10262 |
| contact | 41680 | 33892 | 7788 |
| cottonwood-heights-ut | 100686 | 98808 | 1878 |
| crawl-space-water-damage | 83532 | 72058 | 11474 |
| emergency-water-extraction | 88146 | 77706 | 10440 |
| frozen-pipes-midvale | 95756 | 77196 | 18560 |
| hardwood-floor-cabinet-drying | 66872 | 55348 | 11524 |
| home | 76576 | 66702 | 9874 |
| magna-ut | 86652 | 75952 | 10700 |
| midvale-water-sewer-emergency-contacts | 58258 | 48042 | 10216 |
| mold-remediation | 84038 | 74146 | 9892 |
| sewage-backup-cleanup | 85362 | 76438 | 8924 |
| south-salt-lake-ut | 72874 | 60674 | 12200 |
| storm-flood-damage | 76022 | 65838 | 10184 |
| swamp-cooler-leak-water-damage | 80932 | 68920 | 12012 |
| upstairs-unit-leak-who-pays-utah | 68324 | 57270 | 11054 |
| water-damage-repair | 46828 | 36474 | 10354 |
| water-heater-leak-cleanup | 39538 | 32806 | 6732 |
| water-leak-detection | 28834 | 22868 | 5966 |
| window-well-flooding | 72320 | 63874 | 8446 |
| winterize-swamp-cooler-utah | 50740 | 40368 | 10372 |
| **TOTAL (28)** | **2,043,092** | **1,744,378** | **298,714** |

## 2. REUSE NET — CLEAR (corrected corpus + control proof)

`qa/opt5-reuse.py` (same corrected-corpus construction as
`qa/opt4-fix-reuse.py`), log `qa/opt5-reuse.log`, results
`qa/opt5-reuse.json`. Run BEFORE the build, so no temp-copy contamination.

- **Corpus: 11,161 files, fresh disk read** — `*/public/images`,
  `*/images`, `*gh-pages*/images`, `*/out*/images`, `*/export*/images`,
  `*/dist*/images`, `*/build*/images` across `~/workspace`, excluding
  every `*midvale*` path and every qa/candidates/raw/tmp/design dir.
  Composition: public/images 3,386; out* 3,534; gh-pages 789; export* 33;
  other-images 3,419. The Chesterfield live file (the control target) is
  confirmed IN the corpus.
- **md5 hits: 0/28.** No variant is byte-identical to any photo on any
  other site.
- **Filename net (Midvale slugs in corpus): 0.** No corpus file carries a
  Midvale-specific slug.
- **aHash8 ≤ 12 flags: 2,516 entries** (untruncated count — Cycle 4's
  opt4-reuse stored only the top 10 per target, so its "99" is not
  comparable; the count is also inflated by duplicate copies of the same
  photo in public + out + thumbs). **Minimum aHash16 over ALL flagged
  entries = 29** — every flag sits in the different-photo band (same-photo
  0–2, gray zone 13–24, different 25+). Zero flags in the same band, zero
  in the gray zone. CORRECTION: the log's DONE line says
  "min_aHash16_overall=33" — that number was computed over the per-target
  closest-5 lists only and is wrong; the true min recomputed from the full
  flagged lists in `qa/opt5-reuse.json` is **29**. The verdict does not
  change (29 is still decisively in the different band).
- **Viewed-pixel adjudication (6 closest distinct pairs, `qa/adj5-01..06.png`,
  viewed full-size): ALL DIFFERENT.**
  - adj5-01: water-damage-repair (empty room, wood floors) vs Lancaster
    desert rocks + Joshua trees, a16=29.
  - adj5-02: water-damage-repair vs Lancaster barren brown hills, a16=32.
  - adj5-03: window-well-flooding (snowy well + inflow) vs Naples blank
    ceiling-corner thumb (144×144), a16=33.
  - adj5-04: water-damage-repair vs Cape Coral area-ne (waterway +
    skyline), a16=33 — same pair Cycle 4 already adjudicated DIFFERENT.
  - adj5-05: window-well-flooding vs Collinsville Caney River green banks,
    a16=34.
  - adj5-06: window-well-flooding vs Plano laundromat washing machines,
    a16=35.
  Coarse-hash collisions on bright-top/dark-bottom scenes, as in Cycles
  3–4. The remaining 2,510 flag entries are all weaker (aHash16 ≥ 35)
  than the viewed ones.
- **CONTROL — PASSES.** The reconstructed Cycle 4 bad mold install
  (`qa/reverify4fix-bad-mold-recon.webp`, sha256 verified
  `73a156085b8ff5118dec2ffaf6c1d42dc34afbe82f7a7c2246b3df6c1953522a`,
  25,842 B) flags the Chesterfield live file
  `chesterfield-gh-pages/images/chesterfield-mold-remediation-mold-filtration-unit.webp`
  **aHash8 0 / aHash16 0** (md5 differs — different WebP encodes, expected).
  The corpus catches exactly the reuse the Cycle 4 item-2 net missed.
- **Pexels-ID filename net (all of `~/workspace`, 187,639 filenames,
  `qa/opt5-pexels-filename-net.json`):** dead IDs 4176541 (4 files),
  5493659 (3), 5493667 (5), 6474308 (2), 4092030 (24), 4092026 (25),
  10847198 (8), 4098760 (3). Every hit is a pre-existing file on another
  site (raw candidates in qa dirs, or Plano's own installed crawl-space
  photos for 4092030/4092026/10847198) or Midvale's own qa evidence files
  — **none is a Midvale install, none involves the new mid700 files**
  (which carry no Pexels ID in their filenames; they are downscales of
  Midvale's own heroes). "mid700" appears in NO other site's qa dir. Other
  sites' qa logs mention "midvale-water-damage" only as corpus references
  in reuse-net logs, never as an install.
- **Verdict: NET CLEAR.** The variants are downscales of this site's own
  already-cleared mid crops; nothing is reused from any past site.

## 3. BUILD

`qa/opt5-build.sh` (temp-copy method, same as Cycle 4): rsync excluding
`.next`/`out*`/`node_modules`/`.git`/`qa` → `/tmp/midvale-build-c5`,
symlink node_modules, `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`
(no trailing slash) `npm run build`, rc=0. Log `qa/opt5-build.log`.
`out-cycle5/` replaced wholesale (417 files vs Cycle 4's 389 — +28 exactly).
Temp copy deleted (verified gone). Export checks: 28× `-mid700.webp`,
28× `-mid600.webp`, 28× `-mid.webp`; sitemap 31 locs, Pages base, 0
localhost anywhere in the export; exactly 28 HTML files reference `mid700`
(the 28 mid pages; legal pages 0); home HTML carries the 3-candidate
srcset verbatim (`…-mid600.webp 600w, …-mid700.webp 700w, …-mid.webp 800w`).

## 4. VERIFICATION (real Chromium, `qa/opt5-verify-cycle5.py` + `qa/opt5-serve.py`)

Served `out-cycle5/` (port 8328) vs Cycle 4 `out-cycle4/` (port 8327).
31 routes × 390/481/560/600/601/640/700/701/767/1440 (1× + 2×) =
**620 probes**, 0 error probes, plus 310 Cycle 4 baseline probes (1×, all
10 widths). Raw data: `qa/opt5-verify-cycle5.json`, log
`qa/opt5-verify-cycle5.log`.

- **Hero file selection: 0 mismatches** — every route × every viewport/DPR
  combo served exactly the file the breakpoints + 3-candidate srcset rule
  predict (`-m` / `-mid600` / `-mid700` / `-mid` / `-800` / main 1600w).
- **Selection matrix (1×):** `-mid700` served @601 **28/31** (all mid
  pages), @640 **28/31**, @700 **26/31** (can-mold-grow-in-utah midMax 680
  and winterize-swamp-cooler-utah midMax 659 serve the landscape `-800`
  at 700, as designed); @701 **0/31** (the 800w `-mid` serves again,
  25 mid pages + 3 legal on `-800`). **2× unchanged in kind:** @601-2×
  28× `-mid`, @600-2× 28× `-mid`, @767-2× 11× `-mid` + 20× main — the
  700w is never selected at 2× (need 1202–1534 > 700), exactly as designed.
- **Hero transfer, before → after (real Chromium, transferSize):**

  | width 1× | mid-serving pages | C4 mean | C5 mean | delta |
  |---|---|---|---|---|
  | @601 | n=28 | 73,268 B | 62,599 B | **−10,669 B (−14.6%)** |
  | @640 | n=28 | 73,268 B | 62,599 B | **−10,669 B (−14.6%)** |
  | @700 | n=26 | 73,302 B | 62,867 B | **−10,435 B (−14.2%)** |
  | @701 | n=25 | 73,892 B | 73,892 B | 0 B |
  | @767 | n=11 | 71,257 B | 71,257 B | 0 B |

  All-31 means: @601 68,989 → 59,353 B (−9,636 B); @640 same; @700
  67,382 → 58,630 B (−8,752 B). The @601/@640 mid-page saving (10,669 B)
  matches the file-byte prediction (10,668 B) to within 1 byte. The @700
  saving is smaller (10,435 B) because the 26-page set excludes
  can-mold-grow-in-utah (saving 17,040 B) and winterize-swamp-cooler-utah
  (10,372 B): (298,714 − 17,040 − 10,372)/26 = 10,435 B exactly.
  Unchanged as designed: @390 mean 51,418 B (delta 0), @481 51,106 B
  (delta 0), @560 49,680 B (delta 0), @600 49,273 B (delta 0), @767
  56,177 B (delta 0), @1440 120,333 B (delta 0).
- **Visible fraction — NO regression:** @390 min/max/mean **0.630 / 1.000 /
  0.749** — 0 per-page diffs vs Cycle 4 on all 31 pages. @600 **0.788 /
  0.991 / 0.922** — 0 per-page diffs vs Cycle 4. @700 (new width)
  **0.708 / 0.909 / 0.818**. (700×933 is aspect 0.75027 vs 800×1066's
  0.75047 — the 0.0002 aspect difference moves no page's fraction by even
  0.001 at the measured widths.)
- **H1: 31/31 = 1. Overflow: 0 at all 10 widths (1×). Console errors: 0.
  Failed responses / pageerrors (all 20 combos): 0.** No error probes.
- **Export contents:** 417 files; sitemap 31 locs Pages base; 0 localhost.

## 5. DELIBERATELY LEFT (not problems)

- **601–767 1× now serves the 700w file; 701–767 still serves the 800w
  `-mid`** (701 > 700) — by design, the srcset picks the smallest candidate
  ≥ slot width. A 750w variant would be a further separate call.
- **1.92× upscale at 767 2×** for the 11 mid-to-767 pages — unchanged,
  source-limited, accepted in Cycle 3.
- **Real LCP not measured, footer Maps not checked** — per task (needs the
  live push / real network). Not attempted.
- **Regression / re-verification / pack** — not this item's scope; other
  agents do those after this build.

## 6. FILES

- New images: `public/images/heroes/*-mid700.webp` (28)
- Code: `components/site.tsx` (mid `<source>` srcset only — 1 line)
- Scripts + data: `qa/opt5-gen-mid700.py`, `qa/opt5-candidates.json`,
  `qa/opt5-reuse.py`, `qa/opt5-reuse.log`, `qa/opt5-reuse.json`,
  `qa/opt5-pexels-filename-net.json`, `qa/adj5-01..06.png`,
  `qa/opt5-build.sh`, `qa/opt5-build.log`, `qa/opt5-serve.py`,
  `qa/opt5-verify-cycle5.py`, `qa/opt5-verify-cycle5.json`,
  `qa/opt5-verify-cycle5.log`
- Export: `out-cycle5/` (Cycle 5 build; `out/` + `out-cycle2/` +
  `out-cycle3/` + `out-cycle4/` + `out-cloudflare/` untouched — verified:
  no mid700 files in any of them). Temp build copy
  `/tmp/midvale-build-c5` deleted after the copy.
- No push/deploy/token/DNS. Live site still the Cycle 1 close build until he
  orders a re-push with his word + token.
