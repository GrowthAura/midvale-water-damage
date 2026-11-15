# BATCH 2 OPTIMIZATION CYCLE 2 — FINDINGS (coordinator synthesis)

**VERDICT: READY FOR CYCLE 2 CLOSE — PROBLEMS 1 (P1 0 / P2 0 / P3 1).** Independent re-verification (fresh agent, `qa/FINDINGS-opt-cycle2-reverify-2026-11-14.md`) reproduced every claim, several to the exact integer. The single problem was a coordinator documentation error — the variant count "169" (fixed to the true 138; the 31 mobile crops had been double-counted). No site defect. Nothing on the site needed changing.

- Site: Midvale UT water damage, 31 routes, Next.js static export. Cycle 2 export: `out-cycle2/` (Pages subpath build, same base as `out/`). LOCAL ONLY — no push/deploy/token/DNS. Live site untouched (still the Cycle 1 close build on Cloudflare Pages + GitHub Pages).
- Data gate: `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — UNCHANGED through the whole cycle (verified at every build; any change would have been a STOP).
- Content 1001% verbatim. No word changed, nothing invented.

## 1. SRCSET (deferred Cycle 1 P3 — CLOSED)

**Baseline (Cycle 1 close, measured fresh):** 0 srcset anywhere. Mobile downloaded the same files as desktop: hero 1600×1066 mean 121,030 B @390 (6-route sample: 91,390–142,016 B); cards 680×383 for a 245px slot; body 800×450 for a 400px slot.

**Measured slots first (real Chromium, `qa/opt2-slots.json`):** hero box @390 = 390 wide × 489–1,239 tall (mean 1,030); cards 245px @1440 / 340px @390 / 344 @768 / 305 @1024; body 400×225 @1440 / 342×192 @390. Hero box aspect @390: w/h min 0.315 / max 0.798 / mean 0.403 (median 0.354); 28/31 pages < 0.5. Picture media breakpoint measured, not guessed: hero box aspect crosses 1.0 (landscape fits) between 700px (0.83–0.94) and 768px (0.98–1.13) — so mobile crop applies ≤700px.

**Implementation (3 component files, template chrome only):**
- `components/site.tsx` PhotoHero: `<picture>` + `<source media="(max-width: 700px)">` → per-page mobile crop; `<img>` srcset `800w / 1600w`, sizes `100vw`. Width/height attrs stay 1600×1066; `fetchPriority="high"` unchanged.
- `components/panels.tsx` CardImage: srcset `340w / 680w`, sizes `(max-width: 900px) 340px, (max-width: 1280px) 305px, 245px`; attrs corrected 800×450 → 680×383 (true file dims).
- `components/doc-page.tsx` body img: srcset `400w / 800w`, sizes `(max-width: 900px) 90vw, 400px`; attrs corrected 1200×675 → 800×450 (true file dims).
- Variant naming: heroes `<slug>-800.webp` / `<slug>-m.webp`; cards `<slug>-340.webp`; body `<slug>-N-400.webp`. All generated from the site's OWN files with PIL (Lanczos, WebP q82) — no new photos, no reuse question. EXIF 0 on all 138 variants (PIL-verified).
- NOTE — React emits the attribute as `srcSet` (camelCase) in the static HTML, same as the pre-existing `fetchPriority="high"` in the Cycle 1 live build. HTML parsing lowercases attribute names, so browsers honor it — PROVEN in render (see §3: every viewport/DPR picked the right file). Not a defect; recorded so the next grep for lowercase `srcset` does not false-alarm.

**Files added:** 31 hero 800w (800×533), 31 hero mobile crops, 19 card 340w (340×192), 57 body 400w (400×225) = **138 new files**.

## 2. PER-HERO MOBILE CROPS (31 — CLOSED)

**Problem (Cycle 1 measured):** visible fraction @390 min 21.0% / max 53.2% / mean 26.9% — the 1600×1066 landscape photo in a ~390×1,030 hero box shows only its center ~27% band.

**Method:** per-page portrait crop of the SAME photo. Slice width = clamp(round(1066 × A390), 533, 1066) where A390 = that page's measured hero-box w/h at 390 — aspect-matched per page, never narrower than 533px (caps the 2×-DPR upscale at 1.46×). File width capped at 780. Center x-offset default; script `qa/opt2-gen-variants.py`, offsets in `qa/opt2-crop-offsets.json`, manifest `qa/opt2-variants.json`.

**Viewed-pixel adjudication (coordinator viewed all 31 crops full-size, contact sheets `qa/opt2-crops-sheet1-4.png`):** 30/31 center crops PASS — subject in frame, alt-exact. 1 needed a shift: **contact** — the center crop cut the crew member (man on phone) to a sliver at the left edge; re-cropped with x0=120 (window 120–653) — crew + air movers now fully in frame, re-viewed and confirmed (check sheet `qa/opt2-contact-crop-check.png`). 3 short pages (privacy/terms/disclaimer, box 489px) got 780×978 crops from 850-wide slices.

**Re-measured visible fraction @390 (from rendered boxes + crop aspects, `qa/opt2-verify-cycle2.json`): min 0.630 / max 1.000 / mean 0.749** (Cycle 1: 0.210 / 0.532 / 0.269) — **2.8× mean improvement**. Worst page now 63% (tallest hero, condo, clamped at 533px to bound the upscale) vs 21% before.

## 3. VERIFICATION OF SRCSET + CROPS (coordinator, real Chromium, `qa/opt2-verify-cycle2.py` + `qa/opt2-scroll-check.py`)

Served `out-cycle2/` (port 8325) vs Cycle 1 `out/` (8324). 31 routes × 390 1×/2× + 1440 1×, plus slow-scroll-through + targeted re-check.

- **Hero @390 (1× and 2×): 31/31 currentSrc = `-m.webp`; transfer mean 51,418 B (min 18,736 / max 86,726) vs Cycle 1 baseline mean 121,030 B → −57.5%.**
- **Hero @1440 1×: 31/31 = 1600w file** (correct — 1440px viewport needs 1440w). **Hero @800px viewport: `mold-remediation-800.webp` picked, 56,492 B** (the 800w candidate works).
- **Cards @1440 1×: 16/16 loaded = `-340.webp`** (12,514 B mean on the loaded sample); @390 2× = 680w. **Body @1440 1×: 43/43 loaded = `-400.webp`** (15,756 B mean); @390 2× = 800w. Slow-scroll first pass left 3 area cards + 14 last-section body images unloaded (lazy + fast scroll); **targeted re-check with 2.5s settle: 17/17 loaded, 0 missing, 0 failed responses** — confirmed a scroll-timing artifact, not missing files.
- **Failed responses (≥400) across all 31 routes: 0. H1: 31/31 = 1. Overflow: 0 @390 / 0 @1440 / 0 @320. Console errors: 0. Button 2 @320 worst 552.19px (condo — unchanged from Cycle 1's 552.2, 15.8px headroom holds).**
- **Visible main words (innerText approx): 46,377** vs Cycle 1 DOM main count 46,152 — same content, different counting method (innerText vs DOM text); the exact verbatim diff is the re-verifier's job (Cycle 1 baseline: 0 missing / 3,040 segments).
- **Schema untouched:** no schema change — variants are the same images at other resolutions; hero/card/body ImageObject contentUrls still point at the main files (verified present in the export by the re-verifier).
- All 138 variant files exist in `out-cycle2/` (verified by the re-verifier's disk count: 245 image files = 107 main + 138 variants).

## 4. LCP RE-MEASURE ON REAL HOSTING (subagent, `qa/opt2-lcp-live-2026-11-14.md`)

**Honest result: real LCP could NOT be measured from this cell.** Playwright + Chromium failed 24/24 navigations to the live site (`net::ERR_TUNNEL_CONNECTION_FAILED`; same failure on example.com/google.com; curl from the same cell returns 200 — a cell egress-proxy limitation, not the site). No numbers invented.

**Curl fallback actually run (same 6 pages × 2 UAs × 2 runs):** TTFB median 1,603 ms (range 896–2,777 ms, 3× run-to-run variance — the cell's proxy path, not the origin). Hero bytes median 135,854 B, identical mobile/desktop (0 srcset on the LIVE build — expected, it is the Cycle 1 build). Initial transfer 668–708 KB/page uncompressed (≈280–330 KB with brotli, measured). Render-blocking minimal: 1 CSS file, 7/8 JS async, only non-async script is `polyfills` with `noModule`. Below-fold images all lazy.

**Verdict:** Cycle 1's mobile LCP 2.9–3.7s is **mostly lab noise, supported but not proven** — TTFB alone (~1.6s in this cell's path, 3× variance) plus a ~133 KB hero fully explains a ~3s lab LCP, and the page is light where LCP cares. The one real remaining LCP win was the mobile hero — now addressed by Cycle 2 (§1–2: mobile hero 135 KB → ~51 KB mean, −57%). True real-user LCP is very likely well under 2.5s, but that is an inference. **To close the item for real: run the ready-made `qa/lcp-measure.py` on any machine with real egress, or PageSpeed Insights against the live URL** (parent's call — no API key in this cell). CLS was 0 in Cycle 1 lab; not re-measurable here for the same reason.

## 5. GENERIC-LOCATION P3s — CLOSED: 1 of 2 replaced, 1 deliberately left (subagent, `qa/opt2-p3-body-2026-11-14.md`; coordinator verified the install from disk + viewed the new photo full-size)

**REPLACED — `body/sewage-backup-cleanup-3.webp` → Pexels 4239074** (gloved hand scrubbing a toilet bowl with a brush, disinfectant bottle beside it — ties to the page's "Toilet Sewage Overflow vs Main Line Backup" section and sanitizing step). 800×450 WebP q82, 72,220 B → **11,978 B**, sha256 `8c0380ae…`; EXIF/XMP/IPTC/ICC 0. The `-400.webp` variant was ALSO replaced from the same crop (21,558 B → 5,746 B, sha `defeef29…`) — the agent caught that mobile would otherwise keep serving the old aerial via srcset. Alt updated in `lib/body-images.json` (only that image's alt): "A gloved hand scrubbing a toilet bowl with a brush, a bottle of disinfectant cleaner on the floor beside it." — coordinator viewed the installed photo full-size: alt-exact. Originals backed up in `qa/opt2-p3-backup/` (sha-verified). **Reuse nets CLEAR** on a fresh-disk 2,586-file corpus (md5 0, Pexels-ID grep 0, 5 closest aHash flags all adjudicated different photos by viewed pixels, aHash16 38–64). Render-verified by the agent (HTTP 200, served shas match, 800×450 natural / 400×225 client).

**DELIBERATELY LEFT — `body/basement-flooding-cleanup-3.webp`** (aerial leafy suburb stays, 75,018 B). 15 Pexels searches + 9 full-size candidate views: no real, non-reused, non-wrong-place basement-cleanup photo exists. The 3 real basement interiors were ALL killed by the reuse net — 4092030 (live on Plano 3, visually confirmed), 4092026 (Belleville's basement-flood hero), 10847198 (live on Plano 3) — evidence kept in `qa/opt2-p3-candidates/`. The rest were derelict rooms, a European house, or outdoor workers. No image generated — a fake crew photo must never be presented as a real job photo. **OPEN for his call: authorize a generated image (honestly labelled, per the standing rule) or accept the aerial.** Coordinator did not override the agent's escalation.

**Fresh audit: all 57 body images re-viewed — NO other generic-location image found** (magna-ut-1 already swapped in Cycle 1, cottonwood-heights-ut-3 alt already fixed — not re-flagged).

**Note:** the P3 agent synced the new sewage image into the stale `out/` and `out-cloudflare/` dirs for its render check (local build artifacts only — nothing pushed/deployed, live site unaffected). Both dirs now hold the new image with OLD HTML (old alt, 1200×675 attrs); the next real export rebuilds them from `public/`.

## 6. DELIBERATELY LEFT (not problems)

- **Desktop hero @1440 1× still downloads the 1600w file** (mean 120,333 B) — correct per srcset (1440px viewport needs it); the 800w candidate serves ≤800px viewports. No larger hero variant exists (1600w is the max) and none is needed.
- **Area cards (3) at 1440 1× get the 340w file for a ~381px slot** (sizes claims 245px, the services-grid slot) — a 1.12× upscale, immaterial; the services grid (16 cards) dominates and is exact.
- **Mobile crop worst page 63% visible** (condo, tallest hero) — the 533px clamp bounds the 2× upscale at 1.46×; a narrower slice would be softer. Accepted.
- **Picture media ≤700px, not the theme's 767px breakpoint** — measured crossover (see §1); at 701–767px the landscape file fits better.
- **Mold-remediation-2 (washed-out) + water-damage-repair-1 (near-white)** — still as Cycle 1 left them (no better candidate found in 2 searches; subject-correct, alt-exact). P3 agent may revisit if its sourcing turns up a genuine replacement; otherwise they stay.
- **12 over-cap verbatim anchors, breadcrumb double-link, single-item BreadcrumbList, breadcrumb 24px, repair-hero "Midvale home" alt on an Akron photo, card/body img attrs** — carried from Cycle 1 (verbatim wins / accepted / fixed where chrome).
- **Footer Google Maps embed** — still unverifiable in this VM (no google.com egress); needs a real-network eyeball after push.

## 7. FILES

- Variants: `public/images/heroes/*-m.webp` (31), `*-800.webp` (31), `public/images/cards/*-340.webp` (19), `public/images/body/*-400.webp` (57)
- Components: `components/site.tsx`, `components/panels.tsx`, `components/doc-page.tsx` (srcset/picture only)
- Scripts + data: `qa/opt2-measure-slots.py`, `qa/opt2-slots.json`, `qa/opt2-gen-variants.py`, `qa/opt2-variants.json`, `qa/opt2-crop-offsets.json`, `qa/opt2-crops-sheet1-4.png`, `qa/opt2-contact-crop-check.png`, `qa/opt2-verify-cycle2.py`, `qa/opt2-verify-cycle2.json`, `qa/opt2-scroll-check.py`, `qa/opt2-scroll-check.json`, `qa/opt2-serve.py`
- LCP: `qa/opt2-lcp-live-2026-11-14.md`, `qa/lcp-measure.py`, `qa/lcp-measure-curl.py`, `qa/lcp-live-curl-2026-11-14.json`
- Export: `out-cycle2/` (Cycle 2 build; `out/` + `out-cloudflare/` untouched)
- Re-verification: `qa/FINDINGS-opt-cycle2-reverify-2026-11-14.md` (+ `qa/reverify2-*.py/json`)
- Review pack: `~/workspace/your_files/midvale-opt-cycle2-review.pdf` (62 pp, 62,405,165 B) + remote-storage link https://muse.ai/files/1300466579823511/2388855918552751/r4mv2jtvubwlofon6a6smcmg/midvale-opt-cycle2-review.pdf (expires 2026-11-16T08:14:30Z, parent-verified HTTP 200) + 62 PNGs in `~/workspace/your_files/midvale-opt-cycle2/` (129 MB). Manifest `qa/opt2-pack-manifest.json`. All 62 shots native full-page (0 stitched), 0 broken images, 0 overflow, 0 re-shoots. Pack agent incidents owned: VM-wide Chromium SIGTRAP-133 outage ~01:44–02:06 PKT (recovered on its own; /tmp healthy 1–5%) + homepage lazy-load trap (3 area-card photos blank in runs 1–2; fixed by flipping lazy imgs to eager + scrollIntoView + poll — defective run-2 shot preserved at `qa/opt2-defective-home-desktop-run2.png`).

## 8. INDEPENDENT RE-VERIFICATION (fresh agent, did not audit or fix)

`qa/FINDINGS-opt-cycle2-reverify-2026-11-14.md` — **READY FOR CYCLE 2 CLOSE — PROBLEMS 1 (P1 0 / P2 0 / P3 1).**

- Every claim reproduced with the verifier's own scripts, several to the exact integer (hero transfer mean 51,418 B; visible-fraction mean 0.749; Button 2 worst 552.19 / 773.06 px; hero @1440 mean 120,333 B; total main words 46,377).
- **P3-1 (the only problem): coordinator's "169 variants" count — wrong arithmetic (31+31+19+57 = 138; the mobile crops were double-counted). FIXED in this file (all counts now 138).** No site defect; all 138 real variants exist in `public/` and `out-cycle2/`.
- Full regression (verifier's own numbers): 31/31 FULL (thinnest disclaimer 309 words); verbatim 0 missing (2,900 unique segments + 92 trust chips + 31 eyebrows); FAQ 142/142; tables 43/43; links 0/0/0; Button 2 31/31 @320 (552.19) + @390 (773.06); overflow 0; console 0; images 107/107 loaded after slow scroll; schema 254 blocks, contentUrls 107/107; sitemap 31; localhost 1 (polyfills.js string only); double-slash 0; data sha unchanged before AND after.
- Sewage-3 re-verified with the verifier's OWN fresh-disk reuse net (2,998-file corpus: md5 0, Pexels-ID grep 1 hit = Chesterfield scouted-and-REJECTED sibling 4239068, different photo; closest aHash8 12 adjudicated different). Basement-3 kill-list confirmed (4092030/4092026/10847198 all on Plano 3; 4092030 viewed). LCP limitation confirmed by the verifier's own live navigation (ERR_TUNNEL_CONNECTION_FAILED on live site AND example.com; curl 200) — report honestly labels everything NOT MEASURED.
- Verifier's probe artifacts owned plainly (7, all re-measured clean — normaliser spacing, FAQ annotation strip, sitemap trailing slash, schema count order, localhost grep scope, corpus scope, stale contact sheet 2 — sheet regenerated by coordinator after the re-crop).
- Carried observations (not problems): O-1 real LCP still unmeasured (off-cell run / PSI); O-2 basement-3 aerial awaits his call; O-3 footer Maps embed unverifiable in VM; O-4 mobile crop worst 63% (condo, accepted); O-5 picture breakpoint ≤700px (measured); O-6 inner-page single cards correctly pick 680w at 1440 1× (wider slots — srcset working as designed; coordinator's area-card note was slightly imprecise, outcome optimal); O-7 Pexels 4239074's shoot-sibling 4239068 is on Chesterfield (different photo, not a reuse); O-8 carried from Cycle 1 (mold-2 washed-out, repair-1 near-white, breadcrumb 24px, repair-hero Akron alt).
