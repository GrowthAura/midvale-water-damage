# INDEPENDENT RE-VERIFICATION — Batch 2 Optimization Cycle 4 — Midvale UT
**Date:** 2026-11-14 · **Verifier:** fresh subagent (did not trust coordinator/worker claims; own scripts, own measurements) · **Build dir:** `~/workspace/midvale-water-damage/` · **Export verified:** `out-cycle4/` (mtime 2026-11-14 10:47:59, untouched during this verification; 0 files changed after 11:10)

## VERDICT: NOT READY — PROBLEMS 2 (P1 1 / P2 1 / P3 0)

- **P1-1 — mold-remediation-2 is a reuse: the "new" Pexels 4176541 photo is already installed on Chesterfield.** Viewed-pixel-identical to Chesterfield's live `chesterfield-mold-remediation-mold-filtration-unit.webp` (aHash8 0 / aHash16 0, same centered 16:9 crop), rendered as a real `<img>` in `chesterfield-gh-pages/mold-remediation.html`, file mtime 2026-11-12 18:37 — two days before Midvale's install (2026-11-14 10:33). The P3 reuse net missed it (corpus did not include Chesterfield's gh-pages export). Item 2's "nets CLEAR" claim is FALSE. The photo must be replaced again (or the slot left honestly empty).
- **P2-1 — Pexels-ID net for both installed photos is NOT clear.** Chesterfield holds raw candidate `qa-images-real/tmp-batch1/raw/mold-remediation-body1-4176541.jpg` (md5-identical to Elyria's `qa/design-A-work/cand/4176541.jpg`) and `qa/cand-dl/drywall-loop3/5493659.jpg`. The P3 report claimed "no file named *4176541* / *5493659* anywhere in ~/workspace" — false on both IDs. By the worker's own stated rule (used to kill 5493667: "even a raw candidate file on another site counts"), 5493659 should also have been killed; 4176541 is already a P1 for the live-install reason above. At minimum the ID-net claim must be corrected and the 5493659 install re-decided by the parent.
- Everything else in Cycle 4 reproduces exactly (see below). Item 1 (600w mid variant) is fully verified; the regression is clean.

## 0. FRESHNESS GATE (checked first — PASS, so verification proceeded)

| Check | Claimed | Measured |
|---|---|---|
| `lib/pages-data.json` sha256 | `21c6e7f2…d638f` | `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — match |
| `-mid600.webp` public / export | 28 / 28 | 28 / 28, all 600×800, EXIF 0 on all 28 |
| `-mid.webp` public / export | 28 / 28 | 28 / 28, all 800×1066 |
| Export image files | 301 | 301 webp + 1 svg = 302 files (coordinator's "302" counts the favicon) |
| Body shas public = export = claimed | 73a15608… / c6ece3c4… + -400 variants | all match; basement-flooding-cleanup-3 `3c3282f4…` unchanged |
| New alts in export HTML | "fogging a living room" + "drywall stilts" | present in `mold-remediation.html` + `water-damage-repair.html`; old alts 0 hits anywhere |
| New alts in `lib/body-images.json` | — | lines 231 + 305, exact text as claimed |
| `components/site.tsx` mid srcset | 1 line | exactly 1 line (line 99): `…-mid600.webp 600w, …-mid.webp 800w`, `sizes="100vw"` |
| Sitemap | base `https://growthaura.github.io/midvale-water-damage`, 31 locs, 0 localhost | 31 locs, base OK, 0 localhost in sitemap + 0 in any HTML |
| Double-slash | 0 | 0 |
| Backups `qa/opt4-p3-backup/` (4 files) | old shas 309a0270… / 3f03341a… / 65505557… / 33a94112… | all 4 match, byte sizes 11708 / 4632 / 7106 / 2664 |
| mid600 export-vs-public sha | identical | 0 mismatches |
| Body install dims / EXIF | 800×450 + 400×225, EXIF 0 | 800×450 (25,842 B / 20,254 B), 400×225 (9,522 B / 7,838 B), EXIF 0 on all 4 |
| `candidates.json` bytes (600/800/700) | 600: min 19,804 / max 83,236 / mean 51,139 / total 1,431,902; 800: 28,834 / 117,684 / 72,968 / 2,043,092; 700 total 1,744,378 | reproduced to the byte from disk; 700 files on disk 0 (deleted as claimed) |

## 1. ITEM 1 — 600w MID VARIANT — VERIFIED

- **Selection, 496 probes (31 routes × 16 viewport/DPR combos, real Chromium): 0 mismatches** vs breakpoints + srcset rule. Counts reproduce exactly: @481 1× mid600 1/31; @560 1× 19/31; @600 1× 28/31 (3 legal on `-800`); @640 1× `-mid` 28 + `-800` 3; @481 2× `-m` 30 + `-mid` 1; @600 2× `-mid` 28 + main 3; @767 2× `-mid` 11 + main 20.
- **Hero transfer (real Chromium transferSize, C3 baseline served from `out-cycle3/`):**

  | width 1× | mid n | C3 mean | C4 mean | delta |
  |---|---|---|---|---|
  | @481 | 1 | 94,602 | 62,722 | −33.7% |
  | @560 | 19 | 73,092 | 50,922 | −30.3% |
  | @600 | 28 | 73,268 | 51,439 | −29.8% |
  | @600 ALL 31 | — | **68,989** | **49,273** | −19,716 B |

  All-31 means: @481 52,134 → 51,106; @560 63,268 → 49,680. Unchanged as designed: @390 51,418; @640 68,989; @767 56,177; @1440 120,333. Every number matches the claim to the byte.
- **Visible fraction:** @390 min/max/mean **0.630 / 1.000 / 0.749**; @600 **0.788 / 0.991 / 0.922** — exact matches.
- **Reuse net (item 1) — CLEAR in both of my corpora.** My own implementation reproduces the coordinator's hash values exactly on their closest pair (repair-mid600 vs Cape Coral area-ne: a8 5 / a16 33). Clean rerun (`qa/reverify4-reuse2.py`, all `*midvale*` paths excluded): corpus B (coordinator-style, 3,566 files) total flags 723, **min a16 = 33 — exactly the claimed 33**; corpus A (installed/exported incl. gh-pages/out dirs, 11,093 files) total flags 2,562, min a16 = 29 (repair-mid600 vs Lancaster `...-93536-sec2.webp`, a8 8 / a16 29 — still different-band; flag counts are higher in A because export dirs multiply near-identical files). md5 0 for all 28 in both corpora. **No mid600 flag in the same-photo band (0–2) or gray zone (13–24) in either corpus.** All 6 claimed closest pairs re-adjudicated by MY OWN full-size viewed pixels — **ALL DIFFERENT** (empty room vs waterway+skyline; snowy window well vs laundromat; empty room vs peeling ceiling+floral wallpaper; empty room vs industrial tanks; downspout+snowmelt vs tugboat+barge+crane; rooftop swamp cooler vs Glenpool welcome sign), plus the corpus-A closest pair (a16 29: empty room vs desert Joshua-tree landscape — also DIFFERENT). Contact sheets: `qa/reverify4-adj-mid600-1..7.png`.

## 2. ITEM 2 — BODY PHOTOS — ONE P1 REUSE, ONE CLEAN-ISH

- **mold-remediation-2 → Pexels 4176541: REUSE — P1.** See verdict. Evidence:
  - Installed file vs Chesterfield live file: aHash8 0 / aHash16 0 (my own code); md5 differs (different WebP encode/size: 800×450 vs 1200×675) — same pixels, same centered 16:9 crop.
  - Viewed pixels (side-by-side `qa/reverify4-adj-mold-vs-chesterfield.png`): identical — same worker pose, same beige sofa/cushions/checkered throw, same clothes rack with orange/grey garments, same plant, same fog pattern.
  - Chesterfield live use: `<img src="/chesterfield-water-damage/images/chesterfield-mold-remediation-mold-filtration-unit.webp" alt="Worker in a protective suit fogging a living room with a fumigation machine" width="1200" height="675">` in `chesterfield-gh-pages/mold-remediation.html`; also present in `chesterfield-water-damage/out/images/`. File mtime 2026-11-12 18:37, predates Midvale install 2026-11-14 10:33. Chesterfield had it first.
  - Chesterfield's raw source `qa-images-real/tmp-batch1/raw/mold-remediation-body1-4176541.jpg` (2026-11-10) is md5-identical to Elyria's candidate `qa/design-A-work/cand/4176541.jpg`.
  - Why the P3 net missed it: its corpus (2,642 files, `public/images` + `images` globs) did not include `chesterfield-gh-pages/images/` (or other gh-pages export dirs). My round-1 corpus (3,974 files, incl. gh-pages/images) found it immediately.
- **water-damage-repair-1 → Pexels 5493659: no live install found.** md5 0; only aHash8 ≤12 flag is Cape Coral `svc-commercial.jpg` (a8 11 / a16 53) — re-adjudicated by MY OWN full-size viewed pixels: **DIFFERENT** (interior drywall worker on stilts vs brick-and-glass office exterior; `qa/reverify4-adj-5493659-vs-capecoral.png`). The full source frame shows the stilts clearly, so the new alt ("standing on drywall stilts") describes the photo accurately even though the 16:9 crop cuts the stilts off — not a defect.
  - BUT the Pexels-ID net is not clear (P2-1): Chesterfield holds `qa/cand-dl/drywall-loop3/5493659.jpg` (2026-11-13, different md5 — different download params, same Pexels ID). Under the worker's own 5493667 precedent this is a kill; the parent must decide whether the qa-candidate rule stands. If it stands, this install also fails.
  - The P3 claim "no `photos/5493659` URL in the main qa logs (8 sites)" reproduces for TEXT logs (bounded grep: only hit is Midvale's own P3 report). The failure is the FILENAME net, not the log net. Same for 4176541.
- **Both slots render:** my own screenshots `qa/reverify4-slot-mold-1440/390.png` + `qa/reverify4-slot-repair-1440/390.png` show the new photos in their slots at both widths; served shas match (800w 73a15608… / c6ece3c4…; -400 variants serve at 1440/390 as designed, slot 400px wide). EXIF 0 on all 4 installed files. Backups verified (§0).
- **24 candidates / dead-candidate evidence spot-checked:** 6474308 IS listed in `plano-blackland-restoration/IMAGES.md:11` as their `--drywall-work` image (kill reproduces); `acworth-water-damage/qa/r3-new-images/5493667.jpg` exists (kill reproduces); `belleville-water-damage/qa/c-work/raw/6474308.jpg` also exists.

## 3. FULL REGRESSION (served `out-cycle4/` locally, real Chromium)

| Check | Measured |
|---|---|
| Routes / sitemap | 31 routes, 31 locs = routes, 0 localhost |
| H1 | 31/31 = 1 (@390) |
| Fullness (main innerText words) | 31/31 FULL, total **46,377** — exact match to Cycle 3 |
| Verbatim vs `lib/pages-data.json` | **0 missing** (all content strings incl. h1/intro/blocks/tables/FAQs; 9 initial hits were link-annotation artifacts — "Label (/route/)" renders as a link; label text + href both verified present) |
| FAQ | **142/142**, per-page counts match pages-data exactly |
| Tables | **43/43** |
| Links (rendered DOM, 1,063 internal instances, 31 unique targets) | **0 broken, 0 self-links in main, 0 orphans** |
| Button 2 ("Request Emergency Help") | 31/31 @320 (worst bottom **552px**, `/condo-apartment-water-damage`) + 31/31 @390 (worst **773px**, `/resources/basement-flooding-spring-snowmelt-utah`); none hidden, none missing; no sticky call bar exists on this site (no `callbar`/`call-bar` element in HTML or `site.tsx`) |
| Overflow | 0 @320/@390/@481/@560/@600/@640/@767/@800/@1440 |
| Console errors / pageerrors / failed responses | 0 / 0 / 0 (all 16 combos) |
| Images | **107/107 loaded** (slow-scroll probe: 0 unloaded; my first fast-scroll probe showed 14 lazy images unloaded — probe artifact, not broken images: all 14 load on scrollIntoView, 0 failed responses, files valid WebP on disk) |
| Schema | **254 blocks, 0 parse errors, contentUrls 107/107**; FAQPage on 28 routes (31 − 3 legal) |
| Bogus URL | `/this-page-does-not-exist-xyz` → **HTTP 404**, 335 B, not homepage (109,770 B); `out-cycle4/404.html` exists (12,528 B, "Page Not Found") |
| Hero selection | 0 mismatches (496 probes, §1) |

## 4. REVIEW PACK — PRESENT

`~/workspace/your_files/midvale-opt-cycle4-review.pdf` — 62 pages, 62,422,681 B, valid %PDF-1.7. 62 PNGs in `~/workspace/your_files/midvale-opt-cycle4/` — all 62 manifest shot files present. Manifest `qa/opt4-pack-manifest.json`: 62 shots, all `fullpage` method, brokenImgs 0, overflow 0. (Pack produced by a parallel agent; I did not shoot it. I verified existence/counts/validity only.)

## 5. INCIDENTS IN MY OWN RUN (owned)

- My first reuse script's corpus was contaminated by `tmp-midvale-c4b-build/public/images` (a parallel agent's temp copy of Midvale itself): every mid600 showed md5=1 + a16=0 self-hits. Caught from the hit paths, discarded, re-ran clean excluding every `*midvale*` path. The contamination is what surfaced the Chesterfield hit in the first place (corpus included gh-pages/images).
- My first reuse script's unbounded `grep -rl` over 8 qa dirs (~14.4 GB of pack binaries) stalled the run; killed the grep child by PID (43288) and re-did the log net bounded to text files only.
- My first lazy-image probe scrolled too fast (60 ms steps) and falsely showed 14 images unloaded; re-probed with slow scroll + scrollIntoView: 107/107 loaded. Fast-scroll numbers are not load failures.
- One `pkill -f` with my own command string in it killed my own shell (known trap); server was stopped by PID afterwards. No site files touched at any point — read-only throughout; no edits, no rebuild, no push/deploy/DNS/token.

## 6. CLEAN REUSE TOTALS (reuse2, `qa/reverify4-reuse2.json`)

Corpus A = 11,093 installed/exported files (public/images, images, out*, gh-pages, export/dist/build; no qa/candidates/tmp/node_modules; no Midvale paths). Corpus B = 3,566 (coordinator-style `*/public/images` + `*/images`, no Midvale paths). md5 = 0 for every target in both corpora.

| Target | A flags (a8≤12) | A min a16 | B flags | B min a16 |
|---|---|---|---|---|
| 28 × -mid600 (total) | 2,562 | **29** (repair vs Lancaster desert, different) | 723 | **33** (claimed 33 — exact) |
| mold-remediation-2 install | 2 | **0** — Chesterfield live file, twice (gh-pages + out) | 1 | **0** |
| water-damage-repair-1 install | 4 | 64 (same Tulsa carpet-machine photo ×4 dirs) | 0 | — |
| Pexels 4176541 source | 2 | 33 (Chesterfield file ×2) | 1 | 33 |
| Pexels 5493659 source | 4 | 53 (Cape Coral commercial; Lancaster; Belleville sump ×2) | 1 | 53 |

No mid600 flag in the same-photo band (0–2) or gray zone (13–24) in either corpus. The only a16 ≤ 24 hit anywhere in the clean run is the mold install vs Chesterfield (a16 0 — the P1).

## FILES (my own scripts + logs)

- `qa/reverify4-freshness.py` + `qa/reverify4-freshness.json`
- `qa/reverify4-reuse.py` + `qa/reverify4-reuse.json` (ROUND 1 — CONTAMINATED by tmp-midvale copy; do not use its flag counts; its Chesterfield hit is real and was re-confirmed clean)
- `qa/reverify4-reuse2.py` + `qa/reverify4-reuse2.log` + `qa/reverify4-reuse2.json` (clean; authoritative)
- `qa/reverify4-serve.py` (my server), `qa/reverify4-render.py` + `qa/reverify4-render.json` + `qa/reverify4-render.log`
- `qa/reverify4-verbatim-links.py` + `qa/reverify4-verbatim-links.json`
- `qa/reverify4-images.py` + `qa/reverify4-images.json` (fast scroll — superseded), `qa/reverify4-images2.py` (probe), `qa/reverify4-images3.py` + `qa/reverify4-images3.json` (slow scroll — authoritative)
- `qa/reverify4-slot-mold-1440.png`, `qa/reverify4-slot-mold-390.png`, `qa/reverify4-slot-repair-1440.png`, `qa/reverify4-slot-repair-390.png`
- `qa/reverify4-adj-mold-vs-chesterfield.png`, `qa/reverify4-adj-5493659-vs-capecoral.png`, `qa/reverify4-adj-4176541src-vs-install.png`, `qa/reverify4-adj-mid600-1..7.png`
