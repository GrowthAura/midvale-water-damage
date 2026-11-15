# CYCLE 4 — FINAL INDEPENDENT VERIFICATION + FRESH REVIEW PACK — 2026-11-14

**VERDICT: READY FOR CYCLE 4 CLOSE — PROBLEMS 0 (P1 0 / P2 0 / P3 0).**

Independent final-phase verifier (fresh agent; did not do the Cycle 4 items).
Verified the coordinator's fresh export `out-cycle4/` with my own scripts —
nothing rebuilt, nothing in `out/`, `out-cycle2/`, `out-cycle3/` or
`out-cloudflare/` touched. LOCAL ONLY — no push/deploy/token/DNS.

- Scripts (mine, fresh): `qa/opt4-final-static.py` → `qa/opt4-final-static.json`;
  `qa/opt4-final-live.py` → `qa/opt4-final-live.json`;
  `qa/opt4-nat-recheck.py`, `qa/opt4-nat-test2.py` (artifact adjudication);
  `qa/opt4-pack-shoot.py` → `qa/opt4-pack/` + `qa/opt4-pack-manifest.json`;
  `qa/opt4-pack-pdf.py` → `~/workspace/your_files/midvale-opt-cycle4-review.pdf`.
- Cycle 4 item evidence re-checked, not trusted: `qa/opt4-mid480.md`,
  `qa/opt4-p3-body-2026-11-14.md`, `qa/opt4-verify-cycle4.json`.

## 1. EXPORT VERIFIED BEFORE ANY PROBING (disk)

- `out-cycle4/`: **301 webp files** (28 × `-mid600.webp` 600×800, 28 × `-mid.webp`
  800×1066, 28 × `-m.webp` 533×1066, 31 × main 1600×1066, 31 × `-800.webp`
  800×533, 3 × 780×978 legal `-m`, 19 cards 680×383 + 19 `-340.webp` 340×192,
  57 body 800×450 + 57 `-400.webp` 400×225). Every `public/images` file present
  in the export, 0 missing.
- `lib/pages-data.json` sha256
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` —
  **unchanged before AND after** every phase.
- Sitemap: **31 locs = 31 routes exactly**, base
  `https://growthaura.github.io/midvale-water-damage`, 0 localhost in
  sitemap/HTML. `localhost` count **1** — `polyfills-42372ed130431b0a.js`
  framework string only. Double-slash **0**. `mid600` referenced in 28 HTML
  files (the 28 mid pages; 3 legal pages 0).
- New body photos, public + export, 800w and -400w: shas **all match** the
  claimed new files (mold `73a15608…` / `82389941…`; repair `c6ece3c4…` /
  `060cf540…`), dims exact (800×450 / 400×225), bytes 25,842/9,522 and
  20,254/7,838, EXIF/XMP/ICC **0 on all 4** (exiftool).
- New alts exact in `lib/body-images.json` and in built HTML (4 occurrences
  each); old alts **0** anywhere in the export.
- `basement-flooding-cleanup-3.webp` sha `3c3282f4…` — **untouched**, public ==
  export == claimed.

## 2. FULL REGRESSION (static + real Chromium, served `out-cycle4/`)

| Check | Result |
|---|---|
| Routes status 200 | 31/31 |
| H1 exactly 1 | 31/31 |
| Fullness (main words) | 31/31 FULL — total **46,377**, thinnest disclaimer **309w** |
| Verbatim (doc segments) | **0 missing** — 3,331 segments, 2,900 unique |
| FAQ visible (Q + A) | **142/142** |
| Tables rendered | **43/43** |
| Links | **0 broken / 0 self-links / 0 orphans** |
| Button 2 | 31/31 @320 (worst **552.19px**, condo, headroom 15.81 vs 568 fold) + @390 (worst **773.06px**, headroom 70.94 vs 844) — identical to Cycle 3 |
| Overflow | **0** @320/@390/@481/@560/@600/@640/@767/@800/@1440 (worst 0px) |
| Console errors / pageerrors / failed responses | **0** (all 16 viewport/DPR combos) |
| Images loaded | **107/107** @1440 and **107/107** @390 (slow scroll + lazy→eager + poll; 0 failed) |
| Schema blocks | **254**, parse errors **0** — BreadcrumbList 31, FAQPage 28, WebPage 29, AboutPage 1, ContactPage 1, ImageObject 107, HowTo 36, Service 19, HomeAndConstructionBusiness 1, WebSite 1 |
| Schema contentUrls | **107/107** exist locally; **107/107 live 200** via served URLs |
| Canonicals | 31/31 exact; robots all `index, follow` |
| Bogus URL | real **404** status (no soft-404); `404.html` carries `noindex` (only noindex page) |
| Visible paren annotations | 1 — `/contact` "(Yes / No / Not sure)", form copy, adjudicated Cycle 1 |

## 3. CYCLE 4 CLAIMS RE-MEASURED (my own probes, 31 routes × 8 widths × 1×/2× = 496 probes)

### Item 1 — 600w mid variant
- **Hero file selection: 0 mismatches** vs per-page breakpoints + the
  `600w/800w` mid srcset rule, all 496 probes.
- `mid600` served at 1×: **@481 1/31, @560 19/31, @600 28/31** — exactly as claimed.
- Hero transfer, Cycle 3 baseline vs Cycle 4 (real Chromium `transferSize`, 1×):

  | width | mid-serving pages | C3 mean | C4 mean | delta |
  |---|---|---|---|---|
  | @481 | n=1 | 94,602 B | 62,722 B | **−31,880 B (−33.7%)** |
  | @560 | n=19 | 73,092 B | 50,922 B | **−22,170 B (−30.3%)** |
  | @600 | n=28 | 73,268 B | 51,439 B | **−21,829 B (−29.8%)** |

  All-31 means: @481 52,134 → 51,106 B; @560 63,268 → 49,680 B;
  **@600 68,989 → 49,273 B (−19,716 B)** — the claimed mean 49,273 B
  reproduced exactly. Unchanged as designed: @390 51,418 B (identical),
  @767 56,177 B (identical), @1440 120,333 B (identical), @640 68,989 B
  (800w `-mid` serves, same as Cycle 3's @600).
- **Visible fraction — no regression:** @390 **0.630 / 1.000 / 0.749** —
  0 per-page diffs vs Cycle 3. @600 **0.788 / 0.991 / 0.922** — mean identical
  to Cycle 3's 0.922; 21 pages move by exactly ±0.001 (pure aspect arithmetic:
  600×800 is exactly 0.75, 800×1066 is 0.75047 — not a visible change).
  Same crop, same pixels, same box.

### Item 2 — two body photos replaced
- Both render in their slots at desktop 1440 and mobile 390 — element
  screenshots viewed (`qa/opt4-final-body-*.png`): mold = worker in white
  protective suit fogging a furnished living room (sofa + clothes rack);
  repair = worker in hard hat + respirator on drywall stilts smoothing joint
  compound with a trowel. **Alt-exact in the live DOM at both widths.**
- `currentSrc` is the `-400.webp` variant at both widths (slot 400px @1440,
  342px @390 — srcset working as designed); `srcset` is
  `<img>-400.webp 400w, <img>.webp 800w` on both pages.
- **Served shas match the new files** for both 800w and -400w, fetched from
  the live-served export at both widths (8/8 checks).
- Slot boxes: 400×225 @1440, 342×192 @390. Natural dims 400×225 @1440
  (see §5 for the 390 `naturalWidth` artifact — not a defect).

## 4. FRESH REVIEW PACK (this cycle, never recycled)

- **62/62 shots** (31 routes × desktop 1440 + mobile 390), **all native
  full-page, 0 stitched**, 0 broken images, 0 overflow, **0 re-shoots**,
  0 errors. All first-attempt.
- PNGs: `~/workspace/your_files/midvale-opt-cycle4/` — 62 files, 129 MB.
- PDF: `~/workspace/your_files/midvale-opt-cycle4-review.pdf` — **62 pp,
  62,422,681 bytes**, pdfinfo-verified (62 pages). Slightly larger than
  Cycle 3's 62,405,165 B — the two new body photos, as expected for a fresh
  pack (mid600 serves only at 481–767, so 1440/390 renders are otherwise
  pixel-identical by design).
- Remote-storage link:
  **https://muse.ai/files/1300466579823511/1503366738379999/rgh2ailqyu37e8ymq5ka8r8n/midvale-opt-cycle4-review.pdf**
  — expires **2026-11-16T11:33:04Z** (48h). Verified: HTTP 200, full
  62,422,681 bytes downloaded, sha256 matches the local file, 62 pages.
- Manifest: `qa/opt4-pack-manifest.json` (shots, brokenImgs, overflow,
  re-shoots, stitched count 0). Pack serves the verified `out-cycle4/`.
- Home desktop shot spot-viewed: labelled header, styled hero, both buttons,
  service cards with photos rendering.

## 5. INCIDENTS + PROBE ARTIFACTS (owned, adjudicated)

1. **First pack-shoot attempt killed by a service restart** after 5 shots
   (6 files on disk, server dead, log lost with the shell). Re-ran the shoot
   from scratch — clean 62/62, 0 re-shoots. No stale or partial shots in the
   pack.
2. **`naturalWidth` 351×197 at 390px viewport** (both new body photos):
   reproduced, then proven a **site-wide Chromium headless-shell artifact,
   not a defect in these files** — the untouched `sewage-backup-cleanup-1/2/3`
   `-400.webp` images report the identical 351×197 at 390; the same file
   loaded directly decodes 400×225 at both 390 and 1440; card images at 390
   report their true file dims (340×192). The served-bytes sha check (8/8)
   is the authoritative proof the right files serve.
3. **Bogus-URL response body is the Python server's default 404 page**
   (local-server artifact, not the site's `404.html` — on Pages hosting,
   `404.html` serves). Status 404 is real; `404.html` itself carries the
   `noindex` meta.

## 6. DELIBERATELY LEFT (not problems)

- Real LCP not measured (needs the live push / real network — cell egress).
- Footer Maps render not checked (needs the live push).
- 601–767px 1× still serves the 800w `-mid` file (a 700w third variant is a
  separate call, out of this item's scope).
- 1.92× upscale at 767 2× for the 11 mid-to-767 pages — source-limited,
  accepted in Cycle 3.
- `body/basement-flooding-cleanup-3.webp` aerial — untouched, his call.
- Carried from prior cycles: mobile hero crop is a backdrop (visible fraction
  is the measured 0.749 mean), breadcrumb 24px accepted, footer Maps
  unverifiable in this VM.

## 7. FILES

- Findings: this file (`qa/opt4-verify-cycle4.md`)
- Data: `qa/opt4-final-static.json`, `qa/opt4-final-live.json`,
  `qa/opt4-final-body-*.png` (4 slot screenshots)
- Pack: `qa/opt4-pack/` (62 PNGs) + `qa/opt4-pack-manifest.json` +
  `~/workspace/your_files/midvale-opt-cycle4/` (62 PNGs) +
  `~/workspace/your_files/midvale-opt-cycle4-review.pdf`
- Scripts: `qa/opt4-final-static.py`, `qa/opt4-final-live.py`,
  `qa/opt4-nat-recheck.py`, `qa/opt4-nat-test2.py`, `qa/opt4-pack-shoot.py`,
  `qa/opt4-pack-pdf.py`, `qa/opt4-pack-shoot.log`, `qa/opt4-pack-pdf.log`
- No push/deploy/token/DNS. Live site still the Cycle 1 close build until he
  orders a re-push with his word + token.
