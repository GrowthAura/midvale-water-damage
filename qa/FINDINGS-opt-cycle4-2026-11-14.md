# BATCH 2 OPTIMIZATION CYCLE 4 — FINDINGS (coordinator synthesis)

**VERDICT: CYCLE 4 CLOSED — READY. PROBLEMS 0 on the site (P1 0 / P2 0 / P3 0).**
This close took a fix round to earn. The first independent re-verification found
the cycle **NOT READY — PROBLEMS 2 (P1 1 / P2 1)**: one installed photo was a
live reuse on another site, and the reuse net that had cleared it was run on a
corpus that missed the export directories. Both problems were fixed with a
corrected corpus, re-verified by a second fresh agent (READY, P1 0 / P2 0 /
P3 2 — one new P3 alt overclaim, fixed by the coordinator with a one-line alt
reword + fresh export; one carried action-weaker note), and the review pack was
refreshed for the two changed pages. Nothing below is asserted — every number
was measured by at least two independent agents, several to the exact integer.

- Site: Midvale UT water damage, 31 routes, Next.js static export. Cycle 4
  export: `out-cycle4/` (Pages subpath build). LOCAL ONLY — no push/deploy/
  token/DNS. Live site untouched (still the Cycle 1 close build on Cloudflare
  Pages + GitHub Pages).
- Data gate: `lib/pages-data.json` sha256
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — UNCHANGED
  through the whole cycle, the fix round, and the final alt fix (verified at
  every build and every check; any change would have been a STOP).
- Content 1001% verbatim. No word changed, nothing invented.

## 1. 600w MID VARIANT FOR 1× DPR (CLOSED — fully verified, untouched by the fix round)

**The design trap, measured not assumed:** Cycle 3's note suggested a "480w"
mid variant. With `sizes="100vw"` the browser picks the smallest srcset
candidate ≥ slot-width × DPR, so a literal 480w file would essentially NEVER
be selected in the 481–600 range — dead weight. Two candidates were generated
from the SAME 800×1066 mid crops (PIL Lanczos resize, WebP q82 — same photo,
same crop, same pixels) and measured per file (`qa/opt4-candidates.json`):
600w saves 29.9% mean (21,828 B/file), 700w only 14.6% (worst file 2%).
**Decision: 600w.**

- **New images (28):** `public/images/heroes/<slug>-mid600.webp` (600×800,
  WebP q82, total 1,431,902 B), EXIF 0 on all 28. One per mid page; the 3 legal
  pages (midMax null) get no variant, same as Cycle 3's mid rule.
- **Code (1 line, template chrome only):** `components/site.tsx` PhotoHero —
  the mid `<source>` srcset is now
  `…/<slug>-mid600.webp 600w, …/<slug>-mid.webp 800w` with `sizes="100vw"`.
  Breakpoints, `-m` source, `<img>` srcset, alts, layout untouched.
- **Verification (real Chromium, 496 probes, reproduced by TWO fresh
  agents to the byte):** hero file selection **0 mismatches** (31 routes × 16
  viewport/DPR combos); mid600 served @481 1/31, @560 19/31, @600 28/31; 2×
  unchanged. Hero transfer @600 1× all-31: **68,989 → 49,273 B**; mid-serving
  pages @481 94,602 → 62,722 B (−33.7%), @560 73,092 → 50,922 B (−30.3%),
  @600 73,268 → 51,439 B (−29.8%). @390/@767/@1440 identical to Cycle 3.
  Visible fraction **no regression:** @390 0.630/1.000/0.749 (0 per-page
  diffs); @600 0.788/0.991/0.922 (mean identical to Cycle 3).
- **Reuse net (item 1) — CLEAR in two corpora:** fresh-disk 2,998-file
  corpus (md5 0, min aHash16 33, 6 closest pairs adjudicated DIFFERENT by
  viewed pixels); re-verifier's 11,093-file corpus A (min a16 29, Lancaster
  desert — different) + 3,566-file corpus B (min a16 33 — exactly claimed).
  No flag in the same-photo band (0–2) or gray zone (13–24) in either corpus.
- **Deliberately left:** 700w candidates deleted (measurement manifest only);
  601–767 1× still serves the 800w `-mid` file (a second variant is a
  separate call); 1.92× upscale at 767 2× unchanged (source-limited, accepted
  in Cycle 3).

## 2. BODY PHOTOS — THE FALSE "NETS CLEAR", THE REUSE, AND THE FIX

### 2a. What item 2 did first (and why it was wrong)

Worker 2 replaced both washed-out body photos (report
`qa/opt4-p3-body-2026-11-14.md`): mold-remediation-2 → Pexels **4176541**
(worker fogging a furnished living room), water-damage-repair-1 → Pexels
**5493659** (worker on drywall stilts smoothing compound). Both 800×450 +
-400 variants, new alts, EXIF 0, backups in `qa/opt4-p3-backup/`. Its reuse
net claimed CLEAR on a fresh-disk **2,642-file corpus** (md5 0, Pexels-ID 0,
5 aHash flags adjudicated different). **That claim was FALSE.**

### 2b. Independent re-verification — NOT READY, PROBLEMS 2
(`qa/FINDINGS-opt-cycle4-reverify-2026-11-14.md`, fresh agent, own scripts)

- **P1-1 — mold-remediation-2 (4176541) is already live on Chesterfield.**
  Viewed-pixel-identical to Chesterfield's live
  `chesterfield-mold-remediation-mold-filtration-unit.webp`: aHash8 0 /
  aHash16 0, same centered 16:9 crop (800×450 vs 1200×675, different WebP
  encodes so md5 differs), rendered as a real `<img>` in
  `chesterfield-gh-pages/mold-remediation.html` (also in
  `chesterfield-water-damage/out/images/`), file mtime 2026-11-12 18:37 —
  two days before Midvale's install. The item-2 net missed it because its
  corpus did not include `chesterfield-gh-pages/images/` (or any gh-pages /
  export dir).
- **P2-1 — Pexels-ID filename net NOT clear for either photo.** Chesterfield
  holds raw candidate `qa-images-real/tmp-batch1/raw/mold-remediation-body1-4176541.jpg`
  (md5-identical to Elyria's candidate) and `qa/cand-dl/drywall-loop3/5493659.jpg`.
  By the item-2 worker's own stated rule (used to kill 5493667: "even a raw
  candidate file on another site counts"), 5493659 should also have been
  killed. No live install of 5493659 was found — only the candidate file.
- **Coordinator confirmation (own checks, before acting):** aHash8 0 /
  aHash16 0 recomputed with the coordinator's own code; the re-verifier's
  side-by-side adjudication PNG viewed full-size by the coordinator — same
  worker pose, sofa, cushions, throw, clothes rack, plant, fog. The P1 is
  real. The cycle was NOT closed as ready.

### 2c. Fix round — BOTH SLOTS REPLACED (`qa/opt4-fix-2026-11-14.md`)

Corrected corpus: **11,111 files** — `*/public/images`, `*/images`,
`*gh-pages*/images`, `*/out*/images`, `*/export*/images`, `*/dist*/images`,
`*/build*/images`, excluding every `*midvale*` path and temp copies. The
control proves the corrected net works: the bad mold install flags
Chesterfield live a16 0 in both runs.

- **Mold-remediation-2 → Pexels 4098781.** 800w sha `78f9d749…`
  (26,986 B), -400 sha `a517c214…` (10,704 B). Filename net 0 hits, log net
  0 hits, md5 0, min aHash16 40 (source) / 48 (install crop — different
  band); explicit pairs vs Biohazard's live file a16 93–153, vs Chesterfield
  4176541 a16 167. **The fix worker's first pick, 4098760, was KILLED by
  the corrected net** — source aHash8 0 / aHash16 0 vs Biohazard's live
  `technician-bathroom-disinfection-oklahoma.jpg`. Its filename/log nets
  were clear; only the 11,111-file hash corpus caught it. 4098781 (different
  room/action from the same shoot) passed everything.
- **Water-damage-repair-1 → Pexels 6474123.** 800w sha `d1fdf52d…`
  (9,302 B), -400 sha `06293b32…` (3,710 B). Filename 0 hits, log 0 hits,
  md5 0, install crop **0 flags ≤12**; explicit pairs vs Plano Blackland's
  live 6474308 a16 96–106 (same shoot, different photo — disclosed).
- Install spec both: 800×450 WebP q82 + 400×225 -400 variant, EXIF/XMP/
  IPTC/ICC 0. Bad installs overwritten, not preserved (shas recorded:
  mold 73a15608…, repair c6ece3c4…). Originals remain in
  `qa/opt4-p3-backup/` (unused — nothing was restored).
- **Export rebuilt fresh** (temp-copy build, `NEXT_PUBLIC_SITE_URL` Pages,
  rc=0, temp copy deleted). Export shas match `public/` exactly; new alts
  1× each, old alts 0; 28 mid600 files; sitemap base Pages (31 refs);
  localhost 0. Real Chromium at 1440 + 390: both slots H1 1, overflow 0,
  console 0, failed requests 0; served-bytes sha matches the installed
  -400 file at both widths; 800w files verified by direct curl (200, shas
  match). All 4 element screenshots viewed — correct new photos rendering.

### 2d. Fix re-verification — READY, P1 0 / P2 0 / P3 2
(`qa/FINDINGS-opt-cycle4-fix-reverify-2026-11-14.md`, second fresh agent,
own scripts, 10,231-file corrected corpus)

- **P1-1 CLOSED.** Installed shas match the fix claims exactly (800w
  78f9d749… / -400 a517c214…), in public/ and export and served bytes.
  Old bad shas 0× in the corpus and 0× in public/. New installs: md5 0,
  min aHash16 48 (source 40). **Control passes:** the verifier reconstructed
  the bad install from the documented source + crop band — byte-identical
  to the bad install (sha 73a15608…, 25,842 B) — and it flags Chesterfield
  live a8 0 / a16 0. **Kill evidence reproduced:** 4098760 source vs
  Biohazard live = a8 0 / a16 0. 4098781 vs Biohazard a16 153 (source) / 93
  (crop), vs Chesterfield a16 167 — different room/action confirmed by
  viewed pixels. Filename net 0 hits outside Midvale; log net 0 hits in
  all 8 sites' qa dirs.
- **P2-1 CLOSED.** Shas match exactly (800w d1fdf52d… / -400 06293b32…).
  Source 4 flags min a16 60 (exact match to the fix worker), installed
  files 0 flags, md5 0. Explicit pairs vs Plano Blackland live 6474308:
  a16 105–106 (source) / 96–97 (crop) — same shoot, different photo,
  confirmed visually. Alt accurate.
- **Regression (rebuilt export, fresh):** 31/31 routes 200, H1 31/31 = 1,
  overflow 0, console 0, images 107/107, schema 254 blocks / 0 errors /
  contentUrls 107/107, FAQ 142/142 (schema Question blocks), links
  0 broken / 0 self / 0 orphans, Button 2 31/31 @320 + @390, bogus URL →
  real 404, sitemap 31 locs, 28 mid600 files, localhost 0, double-slash 0,
  basement-3 sha 3c3282f4… unchanged, pages-data sha unchanged. Static
  verbatim 1,013/1,013 strings present. Both fixed slots render the new
  photos in place (verifier's own element screenshots, 1440 + 390).
- **P3-1 (NEW, fixed by the coordinator — see §3):** mold alt overclaimed
  for the crop.
- **P3-2 (carried, disclosed):** mold photo shows PPE furniture-handling,
  not active fogging — no clean fogging photo exists outside the two
  contaminated families (4176xx = the killed photo's own shoot; 40987xx =
  Biohazard-installed). Subject-correct, action-weaker.

## 3. P3-1 ALT FIX (coordinator, after the fix re-verification)

The fix re-verifier found the new mold alt — "…blue gloves lifting a sofa
cushion in a bright living room" — true of the *source* photo but not of
the installed 16:9 crop, which cuts at the worker's waist: no cushion and
no blue gloves are visible in the rendered image. The coordinator viewed
the installed crop full-size itself and confirmed: white suit, respirator,
safety goggles, leaning over, bright living room, large window, houseplant
— no gloves, no cushion in frame.

- **Fix:** one line in `lib/body-images.json` — alt reworded to
  "A worker in a white protective suit, respirator and safety goggles
  leaning over in a bright living room beside a large window" (describes
  exactly what the crop shows).
- **Export rebuilt fresh** (temp-copy build, rc=0, temp copy deleted;
  `out-cycle4/` replaced wholesale). Verified by the coordinator: new alt
  1× in `out-cycle4/mold-remediation.html`, old alt 0× in export and
  source, body shas still the fix ones (78f9d749… / d1fdf52d…), mid600 28,
  sitemap 31 refs, localhost 0, data sha unchanged, `lib/body-images.json`
  parses (19 routes). The pack PDF needed no refresh — alt text is invisible
  in screenshots, and the PNGs are unchanged.
- P3-1 is closed. P3-2 (action-weaker mold photo) is carried as a disclosed
  limitation, not a defect.

## 4. FULL REGRESSION (final export, worker 3 + fix re-verifier agree)

31/31 status 200, H1==1, 31/31 FULL (46,377 words, thinnest disclaimer
309w), verbatim 0 missing (3,331 segments), FAQ 142/142, tables 43/43,
links 0 broken / 0 self / 0 orphans (1,063 instances), Button 2 552.19px
@320 / 773.06px @390 (identical to Cycle 3), overflow 0 at 9 widths,
console/page errors 0, images 107/107 loaded @1440 and @390, schema 254
blocks with 0 parse errors, contentUrls 107/107 live 200, bogus URL →
real 404 (404.html carries the only noindex), sitemap 31 locs = routes,
localhost 1 (polyfills.js framework string only), double-slash 0, data sha
unchanged before AND after. Hero selection 0 mismatches (496 probes).
Basement-3 sha 3c3282f4… unchanged throughout.

## 5. REVIEW PACK — DELIVERED + REFRESHED

- **Current pack (refreshed after the fix):** 62/62 shots, all native
  full-page (0 stitched), 0 broken images, 0 overflow, 0 re-shoots.
  PDF: `~/workspace/your_files/midvale-opt-cycle4-review.pdf` (62 pp,
  **62,420,945 B**) + 62 PNGs in `~/workspace/your_files/midvale-opt-cycle4/`.
  Link (HTTP 200 verified by the coordinator, full bytes):
  https://muse.ai/files/1300466579823511/1612765630600675/caipdj6gusgkggomi5aawmpe/midvale-opt-cycle4-review.pdf
  — expires **2026-11-16T13:05:52Z** (48h). Manifest
  `qa/opt4-pack-manifest.json` (refresh block: old/new PDF shas, new
  link/expiry). The refresh re-shot ONLY the 4 affected shots
  (mold-remediation + water-damage-repair × 1440 + 390), verified the new
  photos in all 4 shots by viewed pixels + pixel-match, rebuilt the PDF
  with the original script — exactly pages 33, 34, 37, 38 differ, the other
  58 are render-identical. Old 4 PNGs + old PDF preserved as evidence in
  `qa/opt4-pack-superseded/`.
- **Superseded pack link (do NOT use):**
  https://muse.ai/files/1300466579823511/1503366738379999/rgh2ailqyu37e8ymq5ka8r8n/midvale-opt-cycle4-review.pdf
  (62,422,681 B, expires 2026-11-16T11:33:04Z) — shows the old reused /
  killed photos on the mold + repair pages.

## 6. STANDING LESSON — REUSE CORPORA MUST INCLUDE EXPORT DIRS

The item-2 worker's corpus (`public/images` + `images` globs only) missed
Chesterfield's live photo because it lives in `chesterfield-gh-pages/images/`.
**Every reuse net from now on must cover installed/exported files everywhere:**
`*/public/images`, `*/images`, `*gh-pages*/images`, `*/out*/images`,
`*/export*/images`, `*/dist*/images`, `*/build*/images` — plus the
Pexels-ID filename net across ALL of `~/workspace` (not just image dirs)
and the qa logs of all sites. A net that only covers source dirs is not a
net. The fix round's 11,111-file corpus and the fix re-verifier's
10,231-file corpus both caught the reuse immediately; the control (rebuild
the bad install, confirm a16 0 vs the live file) is now the required
proof that a corpus is actually working. This is the same class of error
as the Acworth leak-credit (stale manifest) — the corpus, not the photo,
was the failure.

## 7. DELIBERATELY LEFT (not problems)

- **Basement-flooding-cleanup-3 aerial stays — DO NOT TOUCH.** Still pending
  HIS call (generated image, honestly labelled, vs accept the aerial).
  Untouched this cycle (sha verified before/after every phase).
- **Mold photo action-weaker (P3-2):** PPE furniture-handling, not active
  fogging. No clean fogging photo exists outside the two contaminated
  families. Alt now describes exactly what the crop shows.
- **601–767 1× still serves the 800w `-mid` file** (a second variant is a
  separate call); 1.92× upscale at 767 2× (source-limited, accepted);
  real LCP still unmeasured (cell egress blocks live Chromium; Cycle 1's
  2.9–3.7s is lab noise, not proven — needs an off-cell run or PageSpeed
  Insights once live); footer Maps embed render unverified in this VM
  (curl reaches the embed URL; Chromium can't load the iframe here) —
  needs a real-network eyeball after push.
- Carried from Cycles 1–3: 12 over-cap anchors, single-item home
  breadcrumb, breadcrumb 24px, repair-hero Akron alt, mobile crop worst
  63% @390 (condo, accepted), mold-remediation-2's predecessor photos are
  gone from the site (bad installs overwritten, not preserved — shas
  recorded in §2c).

## 8. WOULD ANOTHER CYCLE STILL FIND REAL IMPROVEMENTS?

Yes, small ones: (1) a 700w mid variant for the 601–767 1× band (~10,668 B/
file mean — the Cycle 4 scope decision, deferred); (2) a fresh Pexels
search for a true fogging-action mold photo (only if a new clean upload
lands — the two known families are contaminated); (3) real LCP via
PageSpeed Insights once the Cycle 2/3/4 build is live; (4) the footer Maps
eyeball after push. Nothing here is a defect — the site is READY FOR
CYCLE 4 CLOSE as it stands. **Note for the parent:** the live site still
carries the Cycle 1 close build — Cycles 2, 3 and 4 are all local. A
re-push needs his word + token.

## 9. FILES

- This report: `qa/FINDINGS-opt-cycle4-2026-11-14.md`
- Item 1: `qa/opt4-mid480.md`, `qa/opt4-candidates.json`,
  `qa/opt4-reuse.py/.log/.json`, `qa/adj4-01..06.png`,
  `qa/opt4-verify-cycle4.py/.json/.log`
- Item 2 (first attempt, superseded): `qa/opt4-p3-body-2026-11-14.md`,
  `qa/opt4-p3-reuse.py/.json/.log`, `qa/opt4-p3-candidates/`,
  `qa/opt4-p3-backup/` (pre-Cycle-4 originals)
- Re-verification (NOT READY): `qa/FINDINGS-opt-cycle4-reverify-2026-11-14.md`,
  `qa/reverify4-*.py/.json`, `qa/reverify4-adj-*.png`,
  `qa/reverify4-slot-*.png`
- Fix round: `qa/opt4-fix-2026-11-14.md`, `qa/opt4-fix-reuse.json`,
  `qa/opt4-fix-reuse2.json`, `qa/opt4-fix-corpus-cache.json`,
  `qa/opt4-fix-render/opt4-fix-render.json`
- Fix re-verification (READY): `qa/FINDINGS-opt-cycle4-fix-reverify-2026-11-14.md`,
  `qa/reverify4fix-*.py/.json`
- Regression + pack: `qa/opt4-verify-cycle4.md`, `qa/opt4-final-static.json`,
  `qa/opt4-final-live.json`, `qa/opt4-final-body-*.png`,
  `qa/opt4-pack-shoot.py`, `qa/opt4-pack-pdf.py`, `qa/opt4-pack-manifest.json`,
  `qa/opt4-pack-refresh.py`, `qa/opt4-refresh-manifest.json`,
  `qa/opt4-pack-superseded/` (old 4 PNGs + old PDF + page hashes)
- Export: `out-cycle4/` (final; `out/` + `out-cycle2/` + `out-cycle3/` +
  `out-cloudflare/` untouched)
- Review pack: `~/workspace/your_files/midvale-opt-cycle4-review.pdf`
  (62 pp, 62,420,945 B) + 62 PNGs in
  `~/workspace/your_files/midvale-opt-cycle4/` + link above (expires
  2026-11-16T13:05:52Z)
