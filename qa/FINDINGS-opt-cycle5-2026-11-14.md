# BATCH 2 OPTIMIZATION CYCLE 5 — FINDINGS (coordinator synthesis)

**VERDICT: CYCLE 5 CLOSED — READY. PROBLEMS 0 on the site (P1 0 / P2 0 / P3 0).**
No fix round was needed: the first independent re-verification closed READY
with every builder claim reproduced exactly or confirmed, and the fresh pack
was shot from the same frozen export. Nothing below is asserted — every
number was measured by at least two independent agents, several to the
exact integer, and the coordinator spot-verified the deliverables on disk
(pack PDF bytes + link HTTP 200, findings files, export, gates).

- Site: Midvale UT water damage, 31 routes, Next.js static export. Cycle 5
  export: `out-cycle5/` (Pages subpath build, 417 files vs Cycle 4's 389,
  +28 exactly). LOCAL ONLY — no push/deploy/token/DNS. Live site untouched
  (still the Cycle 1 close build on Cloudflare Pages + GitHub Pages).
- Data gate: `lib/pages-data.json` sha256
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` —
  UNCHANGED through the whole cycle (verified at every build and every
  check, and by the coordinator after close; any change would have been a
  STOP).
- Content 1001% verbatim. No word changed, nothing invented.

## 1. 700w MID VARIANT FOR 601–767 1× (CLOSED — fully verified)

**Design, measured not assumed:** with `sizes="100vw"` the browser picks
the smallest srcset candidate ≥ slot-width × DPR. At 601–700 1× the old
ladder (600w, 800w) served the 800w file (600 < slot); a 700w candidate
fills exactly that band. At 701–767 1× the 800w file still serves (700 <
slot); at 2× the 800w file still serves (no candidate ≥ slot × 2). So the
700w file's only job is 601–700 1× — Cycle 4 had already measured it
(`qa/opt4-candidates.json`: 700×933, mean 62,299 B, saving 10,668 B/file)
and deleted the files after measurement. This cycle installed them.

- **New images (28):** `public/images/heroes/<slug>-mid700.webp` (700×933,
  WebP q82 method=6, PIL Lanczos downscales of the Cycle 3 `-mid` crops —
  same photo, same crop, same pixels; no re-crop from originals). Total
  **1,744,378 B, mean 62,299 B — byte-identical to Cycle 4's measured
  manifest on all 28 files (delta 0 per file, total delta 0).** Saving vs
  the 800w `-mid`: **298,714 B total, 10,668 B/file mean (14.6%)**; worst
  file cottonwood-heights-ut saves only 1,878 B (1.9%). One per mid page;
  the 3 legal pages (disclaimer, privacy-policy, terms-of-use — midMax
  null) get no variant, same as Cycles 3/4.
- **EXIF 0 on all 28** — builder verified by raw WebP chunk scan (only
  `VP8` chunks) + `getexif()` empty (exiftool was unavailable: apt lock
  held by another process — documented, not hidden); the re-verifier ran
  real exiftool on all 28: EXIF/XMP/IPTC/GPS/ICC all 0. PIL-saved WebP
  carries no EXIF by construction; both checks agree.
- **Code (1 line, template chrome only):** `components/site.tsx` PhotoHero
  — the mid `<source>` srcset is now
  `…/<slug>-mid600.webp 600w, …/<slug>-mid700.webp 700w, …/<slug>-mid.webp 800w`
  with `sizes="100vw"`. Breakpoints (`lib/hero-crops.ts`), the `-m` source,
  the `<img>` srcset (800w/1600w), alts, layout: ALL untouched. Re-verifier:
  after normalising only the mid700 entry + rebuild chunk hashes, C4 vs C5
  HTML is identical on all 32 files; alts identical (107); mid700 vs `-mid`
  same-photo check a16 max 7 across all 28.
- **Build:** fresh `out-cycle5/` (temp-copy method,
  `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`,
  rc=0; temp copy deleted). Sitemap 31 locs Pages base, 0 localhost, 28
  HTML files reference `mid700`. `out/`, `out-cycle2/`, `out-cycle3/`,
  `out-cycle4/`, `out-cloudflare/` untouched (0 mid700 files in any).

## 2. REUSE NETS — CLEAR, WITH CONTROL PROOF (two independent corpora)

- **Builder (qa/opt5-reuse.py): 11,161-file fresh-disk corpus** covering
  `*/public/images`, `*/images`, `*gh-pages*/images`, `*/out*/images`,
  `*/export*/images`, `*/dist*/images`, `*/build*/images`, excluding every
  `*midvale*` path and qa/candidate/raw/tmp dirs. Chesterfield live file
  confirmed in corpus. md5 hits 0/28; Midvale-slug filename hits 0; min
  aHash16 over all 2,516 aHash8≤12 flags = **29** (all in the different-photo
  band; zero in same-photo 0–2 or gray zone 13–24). **Correction recorded
  by the builder:** the reuse log's DONE line says min a16 = 33, but that
  was computed over per-target closest-5 lists only — the true min from the
  full flagged lists is 29. The 2,516 count is untruncated (Cycle 4 stored
  only top-10/target) and inflated by duplicate copies of the same photo in
  public + out + thumbs. 6 closest pairs adjudicated DIFFERENT by full-size
  viewed pixels (`qa/adj5-01..06.png`): repair vs Lancaster desert (a16 29),
  repair vs Lancaster hills (32), window-well vs Naples blank-ceiling thumb
  (33), repair vs Cape Coral waterway (33, same pair Cycle 4 cleared),
  window-well vs Collinsville river banks (34), window-well vs Plano
  laundromat (35).
- **Re-verifier (own scripts): 11,499-file fresh-disk corpus** — a superset
  of the builder's (public/images 3,386; out* 3,534; gh-pages-any 789;
  build* 72; other 3,718). md5 hits 0/28. aHash8≤12 flags: 2,634 entries,
  **true min a16 = 29 (exactly the builder's corrected number).** All 22
  distinct pairs with a16 ≤ 40 viewed full-size (`qa/reverify5-adj-01..22.png`)
  — **all DIFFERENT** (including the a16=29 minimum: empty room vs
  Lancaster desert rocks). The remaining 512 distinct pairs sit at a16 ≥ 41,
  in the different band — not individually viewed, further into the band
  than every viewed pair (stated as scope, not hidden).
- **Pexels-ID filename net** over 187,639 (builder) / 188,632 (verifier)
  filenames across ALL of `~/workspace`: dead-ID hits are all pre-existing
  files on other sites (raw candidates, or Plano's own installed crawl-space
  photos) or Midvale's own qa evidence — none is a Midvale install, none
  touches mid700. "mid700" appears in no other site's qa. 4098781/6474123
  (Cycle 4 fixes) zero outside Midvale.
- **CONTROL PASSES in both runs:** reconstructed Cycle 4 bad mold install
  (sha verified `73a15608…`, 25,842 B) flags Chesterfield live **aHash8 0 /
  aHash16 0** — the corpus catches exactly the reuse the old net missed.
  Verifier note: its own rebuild from source + crop band did not reproduce
  the documented bytes (24,344 B vs 25,842 B — encoder settings not fully
  documented) but still flags Chesterfield 0/0, so the control stands.

## 3. VERIFICATION (real Chromium, out-cycle5 vs out-cycle4)

- **Hero selection: 0 mismatches across 620 probes** (31 routes × 10 widths
  × 1×/2×, incl. 481/560/600/601/640/700/701/767 at both DPRs; verifier
  ran 620 C5 + 310 C4 probes). mid700 served @601 28/31, @640 28/31, @700
  26/31 (can-mold midMax 680 + winterize midMax 659 correctly serve `-800`
  at 700); @701 0/31 (800w `-mid` resumes); never at 2×.
- **Transfer @601–700 1×:** mid-serving pages @601 **73,268 → 62,599 B
  (−10,669 B, −14.6%)**, matching the 10,668 B file-byte prediction to 1 B;
  @640 identical; @700 −10,435 B (−14.2%, n=26 — exactly
  (298,714−17,040−10,372)/26, the two excluded pages' savings).
  @390/@481/@560/@600/@701/@767/@1440 delta **0 B**.
- **Visible fraction, no regression:** @390 **0.630/1.000/0.749** (0
  per-page diffs vs Cycle 4 on all 31); @600 **0.788/0.991/0.922** (0
  per-page diffs); @700 new **0.708/0.909/0.818** (5 pages −0.001 from the
  0.0002 aspect difference — rounding, not a regression).
- **0 failed requests, 0 console errors, H1 31/31 = 1, overflow 0 at all
  widths.** Words 46,377, identical.

## 4. FULL REGRESSION (final export, builder + re-verifier agree)

31/31 status 200, H1==1, 31/31 FULL (46,377 words, thinnest disclaimer
309w), verbatim 0 missing (3,331 segments), FAQ 142/142, tables 43/43,
links 0 broken / 0 self / 0 orphans (1,063 instances), Button 2 552.19px
@320 / 773.06px @390 (identical to Cycles 3–4, reproduced exactly),
overflow 0 at 10 widths 1×/2×, console/page errors 0, images 107/107
loaded @1440 and @390, schema 254 blocks with 0 parse errors, contentUrls
107/107 live 200, bogus URL → real 404 (404.html carries the only noindex),
sitemap 31 locs = routes, localhost 1 (polyfills.js framework string only),
double-slash 0, data sha unchanged before AND after. Basement-3 sha
`3c3282f4…` unchanged throughout (coordinator-verified after close:
`3c3282f408f855f6fda99c8553102957a4177e30fe4fa6bfb5c7a91c20e1d68f`).

## 5. REVIEW PACK — DELIVERED

- **Pack:** 62/62 shots, all native full-page (0 stitched), 0 broken images,
  0 overflow, 0 re-shoots, from the frozen `out-cycle5/`. PDF:
  `~/workspace/your_files/midvale-opt-cycle5-review.pdf` (62 pp,
  **62,420,945 B**, sha256
  `f91106a0afcea6afc8ca4d2a1abf78af99c2ece8454283352544a6e5ebdaacb8`)
  + 62 PNGs in `~/workspace/your_files/midvale-opt-cycle5/` (129 MB).
  Link (HTTP 200 verified by the pack agent with a full-bytes download,
  and re-verified by the coordinator):
  https://muse.ai/files/1300466579823511/1109724241878648/aga3mbv3w6aricm20a41hknb/midvale-opt-cycle5-review.pdf
  — expires **2026-11-16T14:36:22Z** (48h). Manifest
  `qa/opt5-pack-manifest.json`. Tallest shot: `01-home-mobile.png` at
  27,287 px. /tmp 1% at start; Chromium profile under `qa/tmp-chrome/`;
  upload succeeded first attempt. The PDF is the same byte size as Cycle
  4's (62,420,945 B) because the pack shoots only 1440 + 390, where the
  serving files are unchanged from Cycle 4 (mid700 serves at 601–700) —
  renders are pixel-identical at those widths, as designed.
- **Honest notes from the agents (recorded, not hidden):** the re-verifier's
  own scripts had 3 bugs, all caught and re-run (reuse corpus v1 missed
  subdirs, 9,442 → fixed 11,499; baseline loop indentation bug lost the
  first C4 baseline, re-ran 310 probes; first Button-2 selector was wrong,
  27,797px artifact — re-measured properly). Two recorded exec failures in
  the builder's run (exit 1) and several in the verifier's (SIGTERM 15s
  from its own server cleanup + output-drain timeouts) did not affect the
  deliverables — all three agents completed and their claims were
  reproduced independently.

## 6. DELIBERATELY LEFT (not problems)

- **Basement-flooding-cleanup-3 aerial stays — DO NOT TOUCH.** Still pending
  HIS call (generated image, honestly labelled, vs accept the aerial).
  Untouched this cycle (sha verified before/after every phase).
- **701–767 1× still serves the 800w `-mid` file** (by design — a 750w
  variant would save ~5% on a 67px band; not a real item, see §7).
- **1.92× upscale at 767 2×** (source-limited, accepted Cycle 3); mold photo
  action-weaker (P3-2 carried from Cycle 4 — no clean fogging photo exists
  outside the two contaminated families; no search run this cycle, per
  brief); real LCP still unmeasured (cell egress blocks live Chromium;
  Cycle 1's 2.9–3.7s is lab noise, not proven — needs an off-cell run or
  PageSpeed Insights once live); footer Maps embed render unverified in
  this VM (curl reaches the embed URL; Chromium can't load the iframe here)
  — needs a real-network eyeball after push.
- Carried from Cycles 1–4: 12 over-cap anchors, single-item home breadcrumb,
  breadcrumb 24px, repair-hero Akron alt, mobile crop worst 63% @390
  (condo, accepted).

## 7. WOULD ANOTHER CYCLE STILL FIND REAL IMPROVEMENTS?

**No — not as a local-only cycle.** The image ladder is now complete
(600/700/800w mid + 800/1600w landscape + 400/800w body + 340/680w cards,
all slot-fit, all srcset'd); the only remaining named items all depend on
things outside this cycle's reach: (1) real LCP via PageSpeed Insights once
the Cycle 2–5 build is LIVE (needs his word + token for the re-push);
(2) the footer Maps eyeball after push (real network); (3) a true
fogging-action mold photo, only if a new clean upload lands (the two known
families are contaminated); (4) basement-3, on HIS call (generated image vs
accept the aerial). A Cycle 6 run today would re-measure the same numbers
and find nothing new — the honest recommendation is to stop the local-only
cycle chain here and resume it after the push (for LCP + Maps) or after his
basement-3 call. **Note for the parent:** the live site still carries the
Cycle 1 close build — Cycles 2, 3, 4 and 5 are all local. A re-push needs
his word + token.

## 8. FILES

- This report: `qa/FINDINGS-opt-cycle5-2026-11-14.md`
- Item 1: `qa/opt5-mid700.md`, `qa/opt5-candidates.json`,
  `qa/opt5-gen-mid700.py`, `qa/opt5-reuse.py/.log/.json`,
  `qa/opt5-pexels-filename-net.json`, `qa/adj5-01..06.png`,
  `qa/opt5-build.sh/.log`, `qa/opt5-serve.py`,
  `qa/opt5-verify-cycle5.py/.json/.log`
- Re-verification: `qa/FINDINGS-opt-cycle5-reverify-2026-11-14.md`,
  `qa/reverify5-*` (scripts, JSONs, logs, 22 adjudication PNGs)
- Pack: `qa/opt5-pack-shoot.py`, `qa/opt5-serve.py`, `qa/opt5-pack-pdf.py`,
  `qa/opt5-pack-manifest.json`, `qa/opt5-pack-shoot.log`
- Export: `out-cycle5/` (final; `out/` + `out-cycle2/` + `out-cycle3/` +
  `out-cycle4/` + `out-cloudflare/` untouched)
- Review pack: `~/workspace/your_files/midvale-opt-cycle5-review.pdf`
  (62 pp, 62,420,945 B) + 62 PNGs in
  `~/workspace/your_files/midvale-opt-cycle5/` + link above (expires
  2026-11-16T14:36:22Z)
