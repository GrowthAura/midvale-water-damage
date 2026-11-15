# CYCLE 5 — INDEPENDENT RE-VERIFICATION (fresh agent, own scripts)

**VERDICT: READY. PROBLEMS 0 (P1 0 / P2 0 / P3 0).**

Cycle 5 (28 × `<slug>-mid700.webp`, 700×933, WebP q82, for the 601–767 1× band)
is verified end-to-end with my own code and measurements. Every builder claim
I was asked to reproduce either reproduced exactly or is confirmed with a
stated method difference. Nothing was fixed, nothing was changed in the site:
read-only verification, local only — no push, no deploy, no DNS, no token.

- Site: Midvale UT water damage, 31 routes, Next.js static export.
  Cycle 5 export: `out-cycle5/` (417 files, Pages subpath build).
  Baseline: Cycle 4 export `out-cycle4/` (389 files).
- Data gate: `lib/pages-data.json` sha256
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` —
  MATCH before and after every phase of this verification. No STOP triggered.
- `public/images/body/basement-flooding-cleanup-3.webp` sha256
  `3c3282f408f855f6fda99c8553102957a4177e30fe4fa6bfb5c7a91c20e1d68f` —
  UNCHANGED in public/ and in the export. Untouched.
- Content 1001% verbatim. No word changed, nothing invented.

## 0. MY OWN ERRORS, CAUGHT AND RE-RUN (recorded, not hidden)

Three of my own scripts had bugs; each was fixed and the affected phase
re-run from scratch. None of them touched the site.

1. **Reuse corpus v1** (9,442 files) counted image files only when the walked
   directory itself was named `images`, so subdirs (`images/heroes/`,
   `images/body/`) and whole-tree gh-pages files were missed. Killed,
   rebuilt as the union (any file under an `images` dir OR any file under a
   `gh-pages` path OR any file under an out/export/dist/build path component),
   re-ran: **11,499 files**. The final corpus is a superset of the builder's
   11,161 (buckets match exactly: public/images 3,386; out\* 3,534;
   gh-pages-any 789).
2. **Baseline loop indentation bug** in `qa/reverify5-verify.py`: `base[r] = m`
   sat outside the route loop, so each Cycle 4 baseline dict kept only the
   last route and the summary crashed (KeyError '/'). C5 data, button2 and
   imgprobe from that run were intact. Re-ran the 310 baseline probes only
   with `qa/reverify5-baseline.py` (indentation fixed) and merged them.
3. **Button 2 first selector was wrong**: a document-wide
   `/Call|Get Help|Request/i` filter on `a,button` picked a far-down element
   (bottom 27,797px). The correct target is the second hero button
   (`.hero-buttons a:nth-child(2)`, "Request Emergency Help"). Re-measured
   properly in `qa/reverify5-imgprobe.py`: worst **552.19px @320** /
   **773.06px @390** — exact reproduction of Cycles 1–4.

## 1. INSTALL — VERIFIED

- **28 mid700 files in `public/images/heroes/` and 28 in
  `out-cycle5/images/heroes/`, byte-identical (sha256 compared per file).**
  All 700×933 (PIL). Total 1,744,378 B — byte-for-byte equal to Cycle 4's
  measured manifest `qa/opt4-candidates.json` ["700"] on all 28 files
  (delta 0 per file). Saving vs the 800w `-mid` file: 298,714 B total,
  10,668 B/file mean.
- **Legal pages have none:** disclaimer, privacy-policy, terms-of-use — no
  `-mid700.webp` in public/ or export. Same 28-file set as mid600/mid.
- **No mid700 files** in `out/`, `out-cycle2/`, `out-cycle3/`, `out-cycle4/`,
  `out-cloudflare/` (0 each).
- **Export webp total 329** (Cycle 4: 301; +28 exactly). All 329 public
  images present in the export, **0 sha mismatches public vs export**.
  Dims: 700×933 ×28, 600×800 ×28, 800×1066 ×28, 1600×1066 ×31, plus the
  unchanged body/sec dims (400×225 ×57, 800×450 ×57, 340×192 ×19, 680×383
  ×19, 800×533 ×31, 533×1066 ×28, 780×978 ×3).
- **mid700 = same photo, same crop as `-mid`:** aHash16 vs the 800×1066
  `-mid` source is 0–7 across all 28 (worst basement-flooding-cleanup a16 7,
  a8 0); a8 max 2. Downscale only, no re-crop.
- **Code — exactly the claimed 1 line:** `components/site.tsx` PhotoHero
  mid `<source>` srcset is verbatim
  `…/<slug>-mid600.webp 600w, …/<slug>-mid700.webp 700w, …/<slug>-mid.webp 800w`
  with `sizes="100vw"` on all 28 mid pages (exact-string match per page in
  the export; 0 problems). The `-m` source, the `<img>` srcset
  (`-800.webp 800w, <main> 1600w`), alts and layout are untouched:
  after normalising only the mid700 srcset entry and the fresh-build JS
  chunk hashes, **out-cycle4 vs out-cycle5 HTML is identical on all 32 files**
  (the only remaining diff is the `main-app-<hash>.js` filename, a normal
  rebuild hash). Alt attribute sets are identical C4 vs C5 (107 distinct).
  `lib/hero-crops.ts` breakpoints match `qa/opt3-variants.json` exactly on
  all 31 slugs (0 mismatches) — including can-mold-grow-in-utah midMax 680
  and winterize-swamp-cooler-utah midMax 659.
- **Cycle-4 body installs untouched:** mold-remediation-2 800w
  `78f9d749…` / -400 `a517c214…` and water-damage-repair-1 800w `d1fdf52d…` /
  -400 `06293b32…` — all four full shas match in public/ AND export.
  Mold alt in HTML: 4 (same as Cycle 4).

## 2. REUSE NETS — CLEAR (corrected corpus + control proof)

`qa/reverify5-reuse.py` (own code), log `qa/reverify5-reuse-run.log`,
results `qa/reverify5-reuse.json`, corpus hashes
`qa/reverify5-corpus-hashes.json`.

- **Corpus: 11,499 files, fresh disk read** — `*/public/images`,
  `*/images`, `*gh-pages*/images`, `*/out*/images`, `*/export*/images`,
  `*/dist*/images`, `*/build*/images` across `~/workspace` (union
  construction, §0.1), excluding every `*midvale*` path and temp copies
  (node_modules / .next / tmp / tmp-chrome / __pycache__). Composition:
  public/images 3,386; out\* 3,534; gh-pages-any 789; build\* 72;
  other-images 3,718. 0 hash errors. The Chesterfield live file is confirmed
  IN the corpus.
- **md5 hits: 0/28.** No variant is byte-identical to any photo on any
  other site.
- **aHash8 ≤ 12 flags: 2,634 entries** (untruncated count; builder: 2,516
  on a slightly smaller corpus — the difference is corpus size, not a new
  signal). **TRUE min aHash16 over ALL flagged entries = 29** — exactly the
  builder's corrected true min (29). Zero flags in the same-photo band
  (0–2), zero in the gray zone (13–24). Distinct flag photos (by md5): 534.
- **Viewed-pixel adjudication — all 22 distinct pairs with a16 ≤ 40,
  full-size side-by-sides `qa/reverify5-adj-01..22.png`, ALL DIFFERENT:**
  - adj-01 (a16 29, the true minimum): water-damage-repair (empty room,
    wood floors, stairs) vs Lancaster desert rocks + Joshua trees.
  - adj-02 (a16 32): same empty room vs Lancaster barren brown hills.
  - adj-03 (a16 33): window-well-flooding (snowy well + inflow) vs Naples
    blank ceiling-corner thumb (144×144).
  - adj-04 (a16 33): empty room vs Cape Coral area-ne (waterway + skyline)
    — same pair Cycle 4 already adjudicated DIFFERENT.
  - adj-05 (a16 34): snowy well vs Collinsville Caney River green banks.
  - adj-06 (a16 35): snowy well vs Plano laundromat washing machines.
  - adj-07/08/09 (a16 35): empty room vs Tulsa roof-ceiling water stain
    (480w / 800w / full variants of one photo).
  - adj-10 (a16 35): snowy well vs Caney River thumb.
  - adj-11/22 (a16 38/40): empty room vs Tulsa ceiling-drywall stain
    (peeling paint + floral wallpaper; full + thumb).
  - adj-12/13 (a16 38): swamp-cooler roof unit vs Tulsa burst-pipe
    street geyser (full + thumb).
  - adj-14–20 (a16 39): empty room vs Tulsa Day-1 page-bottom screenshot
    crops (Bixby / Broken Arrow / Catoosa / Collinsville / Glenpool /
    Kellyville / Oologah — blank card areas + footer, which is why the
    coarse hash collides).
  - adj-21 (a16 39): empty room vs Pleasant Grove privacy-policy section
    photo (hands signing a clipboard).
  Coarse-hash collisions on bright-top/dark-bottom scenes and near-blank
  screenshots, as in Cycles 3–4. The remaining 512 distinct flag photos
  sit at a16 ≥ 41 — further into the different band than every viewed pair;
  the full list is in `qa/reverify5-reuse.json` (`distinct_flags_sorted`).
  Scope stated plainly: I viewed all 22 distinct pairs with a16 ≤ 40
  full-size; the 512 weaker pairs (a16 ≥ 41) were not individually viewed —
  they are weaker than every viewed pair and sit 16+ points inside the
  different band, so no same-photo candidate can hide among them by the
  validated band rule (same 0–2, gray 13–24, different 25+).
- **CONTROL — PASSES.** The documented bad mold install
  (`qa/reverify4fix-bad-mold-recon.webp`, sha256 verified
  `73a156085b8ff5118dec2ffaf6c1d42dc34afbe82f7a7c2246b3df6c1953522a`,
  25,842 B) flags the Chesterfield live file **aHash8 0 / aHash16 0** in
  BOTH copies (`chesterfield-gh-pages/images/…` and
  `chesterfield-water-damage/out/images/…`). My own independent rebuild
  from the documented source + crop band (`qa/opt4-p3-candidates/4176541.jpg`,
  band y0=63..738 → 800×450 WebP q82) did NOT reproduce the documented
  bytes (24,344 B, sha `454d8994…` — the exact encoder settings the fix
  worker used are not fully documented) but it also flags Chesterfield live
  **a8 0 / a16 0**. The corpus catches exactly the reuse the Cycle 4
  item-2 net missed. The net is not void.
- **Pexels-ID filename net (all of `~/workspace`, 188,632 filenames,
  `qa/reverify5-pexels-filename-net.json`):** dead IDs 4176541 (4 files),
  5493659 (3), 5493667 (5), 6474308 (2), 4092030 (24), 4092026 (25),
  10847198 (8), 4098760 (3) — every hit is a pre-existing file on another
  site (raw candidates in qa dirs, or Plano's own installed crawl-space
  photos for 4092030/4092026/10847198) or Midvale's own qa evidence files;
  **none is a Midvale install, none involves the new mid700 files**
  (slug-named, no Pexels ID). New-install IDs 4098781 (3) and 6474123 (3):
  0 hits outside Midvale. "mid700" appears in 58 filenames workspace-wide,
  **0 outside Midvale**. The qa-log grep for the dead/new IDs across other
  sites' qa dirs returns only candidate/kill references in reuse-net logs
  and findings — no other site claims any of these IDs as an install.
- **Verdict: NET CLEAR.** The variants are downscales of this site's own
  already-cleared mid crops; nothing is reused from any past site.

## 3. EXIF — 0 ON ALL 28 (real exiftool this time)

The builder could not run exiftool (apt lock); it is available in this VM
now (`/usr/bin/exiftool` 12.76) and I ran it on all 28 files
(`qa/reverify5-exif.json`): **EXIF 0, XMP 0, IPTC 0, GPS 0, ICC 0 on every
file** — raw chunk scan agrees (VP8 only). The Cycle-4 body files are also
EXIF-empty (4/4). No metadata of any kind rides the new images.

## 4. HERO SELECTION + TRANSFER + VISIBLE FRACTION (real Chromium)

`qa/reverify5-verify.py` + `qa/reverify5-baseline.py`, served `out-cycle5/`
(port 8332/8333) vs `out-cycle4/` (port 8331). 620 C5 probes + 310 C4
baseline probes, 0 error probes. Raw data: `qa/reverify5-verify.json`.

- **Hero file selection: 0 mismatches** — every route × every viewport/DPR
  combo served exactly the file the breakpoints + 3-candidate srcset rule
  predict (`-m` / `-mid600` / `-mid700` / `-mid` / `-800` / main 1600w).
- **Selection matrix (1×):** `-mid700` served @601 **28/31**, @640 **28/31**,
  @700 **26/31** (can-mold-grow-in-utah midMax 680 and
  winterize-swamp-cooler-utah midMax 659 serve the landscape `-800` at 700,
  as designed); @701 **0/31**; @481 1/31 mid600 (can-mold only, mMax 475);
  @560 19/31 mid600; @600 28/31 mid600. **2× unchanged in kind:** @601-2×
  28× `-mid`, @600-2× 28× `-mid`, @700-2× 26× `-mid`, @767-2× 11× `-mid` +
  20× main — the 700w is never selected at 2× (need 1202–1534 > 700),
  exactly as designed. @390/1440 all `-m` / main respectively.
- **Hero transfer, before → after (real Chromium, transferSize):**

  | width 1× | mid-serving pages | C4 mean | C5 mean | delta |
  |---|---|---|---|---|
  | @390 | — | 51,418 B | 51,418 B | 0 B |
  | @481 | n=1 | 62,722 B | 62,722 B | 0 B |
  | @560 | n=19 | 50,922 B | 50,922 B | 0 B |
  | @600 | n=28 | 51,439 B | 51,439 B | 0 B |
  | @601 | n=28 | 73,268 B | 62,599 B | **−10,669 B (−14.6%)** |
  | @640 | n=28 | 73,268 B | 62,599 B | **−10,669 B (−14.6%)** |
  | @700 | n=26 | 73,302 B | 62,867 B | **−10,435 B (−14.2%)** |
  | @701 | n=25 | 73,892 B | 73,892 B | 0 B |
  | @767 | n=11 | 71,257 B | 71,257 B | 0 B |
  | @1440 | — | 120,333 B | 120,333 B | 0 B |

  All-31 means: @601 68,989 → 59,353 B (−9,636 B); @640 same; @700
  67,382 → 58,630 B (−8,752 B). The @601/@640 mid-page saving (10,669 B)
  matches the file-byte prediction (10,668 B) to within 1 byte; the @700
  saving is smaller exactly as the builder's arithmetic predicts
  ((298,714 − 17,040 − 10,372)/26 = 10,435 B). Every number in this table
  reproduces the builder's to the byte.
- **Visible fraction — NO regression:** @390 min/max/mean **0.630 / 1.000 /
  0.749** — 0 per-page diffs vs Cycle 4 on all 31 pages. @600 **0.788 /
  0.991 / 0.922** — 0 per-page diffs vs Cycle 4. @700 (new width)
  **0.708 / 0.909 / 0.818** (builder: same). Note: my @700 C5-vs-C4
  comparison shows 5 pages at −0.001 (contact, water-heater-leak-cleanup,
  crawl-space-water-damage, south-salt-lake-ut,
  midvale-water-sewer-emergency-contacts) — that is the 0.0002 aspect
  difference between 700×933 (0.75027) and 800×1066 (0.75047) rounding at
  the third decimal; the mean is unchanged (0.818) and no page moves by
  more than 0.001. Not a regression.
- **H1: 31/31 = 1 in every one of the 620 probe combos. Overflow: 0 in all
  620 combos (1× and 2×, all 10 widths). Console errors: 0 in all combos.
  Failed responses / pageerrors (all combos): 0.**

## 5. FULL REGRESSION on out-cycle5/

Static half `qa/reverify5-static.py` → `qa/reverify5-static.json`;
render half `qa/reverify5-verify.py` + `qa/reverify5-imgprobe.py` →
`qa/reverify5-verify.json` + `qa/reverify5-imgprobe.json`.

- 31/31 routes 200 + H1 exactly 1 (static + all 620 Chromium combos).
- 31/31 FULL: **46,377 main words** (rendered total equals static total
  on every route; thinnest disclaimer **309w**). Rendered words per route
  match the static count exactly on all 31 routes.
- Verbatim **0 missing** — segment check re-run from
  `lib/pages-data.json`: 3,331 segments, 2,900 unique, 0 missing.
- FAQ **142/142** questions and 142/142 answers visible in main text.
  (FAQ markup is not `<details>` — `details` count 0 is expected; the
  Cycle 4 fix re-verifier recorded the same 0.)
- Tables **43/43** rendered vs expected.
- Links **0 broken / 0 self / 0 orphans** (1,063 internal instances).
- Button 2 **31/31 @320 (worst 552.19px, condo-apartment-water-damage) +
  31/31 @390 (worst 773.06px, condo)** — exact reproduction of Cycles
  1–4 to the hundredth; gates 568 / 844 hold.
- Overflow **0** at 1280 + 390 and at all 10 measured widths, 1× and 2×.
- Console/page errors **0**; failed responses **0**.
- Images **107/107 loaded @1440 and 107/107 @390** with a proper slow
  scroll (300px/150ms + 2.5s wait); 0 broken. (My first fast-scroll pass
  showed 87/107 — the known lazy-load artifact the Cycle 4 fix
  re-verifier also hit and resolved the same way; the slow scroll loads
  all 107.)
- Schema **254 blocks, 0 parse errors** (HomeAndConstructionBusiness 1,
  FAQPage 28, WebSite 1, BreadcrumbList 31, WebPage 29, ImageObject 107,
  HowTo 36, AboutPage 1, ContactPage 1, Service 19); contentUrls **107/107
  return HTTP 200** (checked live against the local server, not just file
  existence).
- Sitemap **31 locs = routes**, Pages base, 0 localhost in sitemap;
  canonicals 31/31 correct.
- localhost **1** in the export — the known `polyfills.js` framework
  string only. Double-slash **0**.
- Bogus URL → **HTTP 404** (not 200, no soft-404); `404.html` carries
  `robots noindex`, H1 "Page Not Found", no canonical. (The local
  test server returns its own generic 404 body for unknown paths, so the
  `noindex` is verified on `404.html` itself — the same limitation and
  the same result as Cycle 4's own static check.)
- One visible parenthetical `(Yes / No / Not sure)` on /contact — a form
  label, identical to Cycle 4, not a doc annotation.
- Robots: `Allow: /`, sitemap URL on the Pages base.

## 6. GATES

- `lib/pages-data.json` sha256 = `21c6e7f2…d638f` — MATCH before and after.
  No P1 STOP.
- `public/images/body/basement-flooding-cleanup-3.webp` sha =
  `3c3282f4…e1d68f` — UNCHANGED in public/ and export.
- Content 1001% verbatim (46,377 words, 0 missing segments).

## 7. DELIBERATELY LEFT (not problems — carried from Cycle 5 / earlier)

- 701–767 1× still serves the 800w `-mid` (701 > 700) — by design; a
  750w variant would be a further separate call.
- 1.92× upscale at 767 2× for the 11 mid-to-767 pages — unchanged,
  source-limited, accepted in Cycle 3.
- Real LCP not measured, footer Maps not checked — per task (needs the
  live push / real network). Not attempted.
- Review pack refresh — not this item's scope.

## 8. FILES (all under ~/workspace/midvale-water-damage/qa/)

- This report: `qa/FINDINGS-opt-cycle5-reverify-2026-11-14.md`
- `qa/reverify5_hashutil.py` — md5 + aHash8/aHash16 helpers
- `qa/reverify5-reuse.py` + `qa/reverify5-reuse.log` +
  `qa/reverify5-reuse-run.log` + `qa/reverify5-reuse.json` +
  `qa/reverify5-corpus-hashes.json` — corrected-corpus reuse net (11,499)
- `qa/reverify5-adjudicate.py` + `qa/reverify5-adj-01..22.png` +
  `qa/reverify5-adjudication.json` — viewed-pixel adjudications
- `qa/reverify5-pexels-filename-net.json` — filename net (188,632 names)
- `qa/reverify5-exif.json` — exiftool results, 28/28 clean
- `qa/reverify5-mid700-vs-mid.json` — mid700 vs -mid same-photo check
- `qa/reverify5-serve.py` — subpath test server
- `qa/reverify5-static.py` + `qa/reverify5-static.json` — static regression
- `qa/reverify5-verify.py` + `qa/reverify5-verify.json` +
  `qa/reverify5-verify-run.log` — Chromium hero/transfer/fraction probes
- `qa/reverify5-baseline.py` + `qa/reverify5-baseline-run.log` — C4
  baseline re-run (indentation-bug fix)
- `qa/reverify5-imgprobe.py` + `qa/reverify5-imgprobe.json` +
  `qa/reverify5-imgprobe-run.log` — slow-scroll images + proper Button 2
- No push/deploy/token/DNS. Live site still the Cycle 1 close build until
  he orders a re-push with his word + token.
