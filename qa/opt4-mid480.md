# CYCLE 4 ITEM 1 — 600w MID VARIANT FOR 1× DPR (481–600px) — FINDINGS

**VERDICT: DONE + VERIFIED. 0 problems.** Real Chromium, locally served
`out-cycle4/` vs Cycle 3 baseline `out-cycle3/`. LOCAL ONLY — no push/deploy/
token/DNS. Live site untouched.

- Site: Midvale UT water damage, 31 routes, Next.js static export.
  Cycle 4 export: `out-cycle4/` (fresh build, Pages subpath base).
- Data gate: `lib/pages-data.json` sha256
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` —
  UNCHANGED at every check (start, after install, after build, after all
  verification). Any mismatch would have been a STOP; none occurred.
- Content 1001% verbatim. No word changed, nothing invented. Visible main
  words total 46,377 — identical to Cycle 3.

## 1. THE DESIGN TRAP — MEASURED, NOT ASSUMED

Cycle 3's note suggested a "480w" mid variant. With `sizes="100vw"` the
browser picks the smallest srcset candidate ≥ slot-width × DPR, so a literal
480w file would essentially NEVER be selected in the 481–600 range (slot
481–600 CSS px at 1×) — dead weight. Two candidates were generated from the
SAME 800×1066 mid crops (PIL Lanczos resize, WebP q82 method=6 — same photo,
same crop, same pixels; no re-crop from originals) and measured per file
(`qa/opt4-candidates.json`):

| variant | dims | bytes min / max / mean | total | saving vs 800w |
|---|---|---|---|---|
| `-mid` (Cycle 3, current) | 800×1066 | 28,834 / 117,684 / 72,968 | 2,043,092 | — |
| `-mid600` (**installed**) | 600×800 | 19,804 / 83,236 / **51,139** | 1,431,902 | **611,190 B total, 21,828 B/file, 29.9%** |
| `-mid700` (rejected) | 700×933 | 22,868 / 102,076 / 62,299 | 1,744,378 | 298,714 B total, 10,668 B/file, 14.6% |

- **Decision: 600w.** It is selected across the ENTIRE named 481–600 range
  at 1× (600 ≥ slot, smallest candidate ≥ slot) and saves 2× what 700w saves
  there (mean 21,828 B vs 10,668 B per file). 700w's only advantage is extra
  coverage at 601–700, outside the named range, and its worst file saves only
  2% (ratio 0.98) — near-dead weight on some pages. 600×800 is also exactly
  3:4 (aspect 0.75), while 700×933 is 0.75027.
- 700w files were generated for measurement only, then DELETED (scratch dir
  removed; only the measurement manifest `qa/opt4-candidates.json` kept).
  Nothing dead-weight was installed.

## 2. WHAT CHANGED

- **New images (28):** `public/images/heroes/<slug>-mid600.webp`
  (600×800, WebP q82, total 1,431,902 B). One per mid page; the 3 legal pages
  (midMax null) get no variant, same as Cycle 3's mid rule.
- **Code (1 line, template chrome only):** `components/site.tsx` PhotoHero —
  the mid `<source>` srcset is now
  `…/<slug>-mid600.webp 600w, …/<slug>-mid.webp 800w` with `sizes="100vw"`.
  Breakpoints untouched, the `-m` source untouched, the `<img>` srcset
  (800w/1600w) untouched, alts untouched, layout untouched.
- **EXIF: 0 on all 28** — exiftool per-file check (EXIF/XMP/IPTC/ICC/GPS/
  MakerNotes/IFD0 tag values = 0 on every file). NOTE: exiftool was absent
  from this VM (`/usr/bin/exiftool` missing); installed via apt
  (`libimage-exiftool-perl`) for this check. PIL-saved WebP carries no EXIF
  by construction; the exiftool run is the verification.
- **Untouched:** `public/images/body/basement-flooding-cleanup-3.webp`
  sha `3c3282f4…` verified before and after; all `-m` / `-mid` / body / card
  files untouched; `lib/hero-crops.ts` untouched.

## 3. VERIFICATION (real Chromium, `qa/opt4-verify-cycle4.py` + `qa/opt4-serve.py`)

Served `out-cycle4/` (port 8327) vs Cycle 3 `out-cycle3/` (port 8326).
31 routes × 390/481/560/600/640/767/800/1440 (1× + 2×) = **496 probes**,
0 error probes. Raw data: `qa/opt4-verify-cycle4.json`.

- **Hero file selection: 0 mismatches** — every route × every viewport/DPR
  combo served exactly the file the breakpoints + srcset rule predict
  (`-m` / `-mid600` / `-mid` / `-800` / main 1600w).
- **Selection matrix (1×):** `-mid600` served @481 **1/31** (only
  can-mold-grow-in-utah, mMax 475), @560 **19/31**, @600 **28/31** (all mid
  pages; the 3 legal pages serve `-800`). @640+ the 800w `-mid` serves again
  (640 > 600), exactly as designed. **2× unchanged:** @481-2× 30× `-m` +
  1× `-mid`; @600-2× 28× `-mid` + 3× main; @767-2× 11× `-mid` + 20× main.
- **Hero transfer, before → after (real Chromium, transferSize):**

  | width 1× | mid-serving pages | C3 mean | C4 mean | delta |
  |---|---|---|---|---|
  | @481 | n=1 | 94,602 B | 62,722 B | **−31,880 B (−33.7%)** |
  | @560 | n=19 | 73,092 B | 50,922 B | **−22,170 B (−30.3%)** |
  | @600 | n=28 | 73,268 B | 51,439 B | **−21,829 B (−29.8%)** |

  All-31 means: @481 52,134 → 51,106 B; @560 63,268 → 49,680 B;
  @600 68,989 → 49,273 B (−19,716 B). The @600 mid-page saving (21,829 B)
  matches the file-byte prediction (21,828 B) to within 1 byte.
  Unchanged as designed: @390 mean 51,418 B (identical to Cycle 3),
  @767 56,177 B (identical), @1440 120,333 B (identical), @640 68,989 B
  (800w mid serves, same as Cycle 3's @600).
- **Visible fraction — NO regression:** @390 min/max/mean **0.630 / 1.000 /
  0.749** — 0 per-page diffs vs Cycle 3. @600 **0.788 / 0.991 / 0.922** —
  mean identical to Cycle 3's 0.922, min identical 0.788. 21 pages move by
  exactly ±0.001 (e.g. home 0.967 → 0.966, repair 0.992 → 0.991): pure
  aspect arithmetic — 600×800 is exactly 0.75 while 800×1066 is 0.75047 —
  not a visible change. Same crop, same pixels, same box.
- **H1: 31/31 = 1. Overflow: 0 @390/@481/@560/@600/@640/@767/@800/@1440.
  Console errors: 0. Failed responses / pageerrors (all 16 combos): 0.**
- **Export contents:** `out-cycle4/` holds 28× `-mid600.webp`, 28× `-mid`,
  31 routes in sitemap, 0 `localhost:3000` in sitemap or any HTML, exactly
  28 HTML files reference `mid600` (the 28 mid pages; legal pages 0).
  Image files in export: 302 vs Cycle 3's 274 (+28, exactly the variants).

## 4. REUSE NET (fresh-disk read — CLEAR)

`qa/opt4-reuse.py` (same lineage as `qa/opt3-reuse.py`: corpus =
`*/public/images` of other site build dirs, md5 + aHash8, aHash16 for
aHash8 ≤ 12; one change: corpus md5/aHash8 computed ONCE and reused for all
28 targets instead of re-reading ~3,000 files per target — same comparison
math, ~28× less I/O; results written after each target, resume-safe).
Log `qa/opt4-reuse.log`, results `qa/opt4-reuse.json`.

- Corpus: **2,998** other-site files (fresh disk read). Filename net
  (Midvale slugs in corpus): **0**.
- **md5 hits: 0/28.** No variant is byte-identical to any photo on any
  other site.
- **aHash8 ≤ 12 flags: 99 entries** (top-10/target lists) across 11 targets,
  90 distinct corpus photos. **Min aHash16 = 33; all 99 flags have aHash16
  ≥ 33** — every flag sits in the different-photo band (same-photo 0–2,
  different 25+). Zero flags in the gray zone (13–24), zero in the same band.
- **Viewed-pixel adjudication (6 closest pairs, `qa/adj4-*.png`, viewed
  full-size): ALL DIFFERENT.** water-damage-repair (empty room, wood floors)
  vs Cape Coral area-ne (waterway + skyline) a16=33; window-well (snowy well
  + inflow) vs Plano laundromat (washing machines) a16=35; repair vs Tulsa
  ceiling stain (peeling ceiling + floral wallpaper) a16=38; repair vs West
  Tulsa industrial tanks a16=41; snowmelt (downspout + pooling) vs Catoosa
  port wharf (tugboat + barge + crane) a16=43; swamp-cooler (rooftop cooler
  + wet roof) vs Glenpool welcome sign (stone sign) a16=44. Coarse-hash
  collisions on dark/wet/outdoor scenes, as in Cycle 3. The remaining 93
  flag entries are all weaker (aHash16 ≥ 44) than the viewed ones.
- **Verdict: NET CLEAR.** The variants are downscales of this site's own
  already-cleared mid crops; nothing is reused from any past site.

## 5. INCIDENTS (owned, fixed in-round)

1. **First export built with localhost base (caught, rebuilt).** The temp-copy
   build ran WITHOUT `NEXT_PUBLIC_SITE_URL`, so `lib/content.ts:32` defaulted
   to `http://localhost:3000` — sitemap/canonicals/og/schema all localhost
   (the P1-1 root cause from the site's history). Caught because the
   verifier's new sitemap-base assertion failed and the route diff showed
   localhost URLs; the run's probes errored instead of silently passing.
   Rebuilt with `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/
   midvale-water-damage` (no trailing slash, Cycle 3's exact invocation);
   `out-cycle4/` replaced wholesale; re-verified 0 localhost in sitemap/HTML.
   The bad export was never served beyond my own crashed verify run.
   Lesson recorded in the verify script: it now asserts the sitemap base
   before probing.
2. **First verify run crashed in the baseline pass (data lost, re-run).**
   The baseline loop had no try/except, so one bad probe (the localhost
   routes 404ing, `.hero-photo` null) killed the script AFTER all 16 C4
   combos — and the JSON was only written at the end, so the C4 data was
   lost too. Hardened the script (baseline try/except, null-hero guard in
   `probe()`, JSON dumped after every combo) and re-ran clean: 496 probes,
   0 errors. The re-run's numbers above are the ones reported.
3. **My own `pkill -f` matched my own shell once** while stopping a test
   server (pattern contained the serve-script path) — killed the diagnostic
   shell, no harm; server checks were re-done properly.

## 6. DELIBERATELY LEFT (not problems)

- **601–767 1× still serves the 800w `-mid` file.** A second variant (700w)
  would save ~10,668 B/file mean there, but the task scoped ONE variant for
  the named 481–600 range; adding a third candidate per hero (28 more files)
  for the 601–700 band is a separate call, not this item.
- **1.92× upscale at 767 2×** for the 11 mid-to-767 pages — unchanged,
  source-limited, accepted in Cycle 3.
- **Real LCP not measured, footer Maps not checked** — per task (needs the
  live push / real network). Not attempted.
- **700w candidate files deleted;** only `qa/opt4-candidates.json` (byte
  measurements) kept.

## 7. FILES

- New images: `public/images/heroes/*-mid600.webp` (28)
- Code: `components/site.tsx` (mid `<source>` srcset only — 1 line)
- Scripts + data: `qa/opt4-candidates.json`, `qa/opt4-reuse.py`,
  `qa/opt4-reuse.log`, `qa/opt4-reuse.json`, `qa/adj4-01..06.png`,
  `qa/opt4-serve.py`, `qa/opt4-verify-cycle4.py`,
  `qa/opt4-verify-cycle4.json`, `qa/opt4-verify-cycle4.log`
- Export: `out-cycle4/` (Cycle 4 build; `out/` + `out-cycle2/` +
  `out-cycle3/` + `out-cloudflare/` untouched — verified: no mid600 files in
  `out-cycle3/`, sizes unchanged). Temp build copy
  `~/workspace/tmp-midvale-c4-build/` deleted after the copy.
- No push/deploy/token/DNS. Live site still the Cycle 1 close build until he
  orders a re-push with his word + token.
