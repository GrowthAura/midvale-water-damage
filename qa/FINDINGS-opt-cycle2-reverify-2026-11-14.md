# CYCLE 2 INDEPENDENT RE-VERIFICATION — Midvale UT — 2026-11-14

**Verifier:** independent re-verifier (did NOT audit or fix anything in Cycle 2).
Fresh reads only — coordinator claims were re-measured, not trusted.
**Scope:** `~/workspace/midvale-water-damage/`, final export `out-cycle2/`
served on `/midvale-water-damage/` (port 8325, `qa/opt2-serve.py`).
LOCAL ONLY — no push/deploy/DNS/token. No site file modified (only `qa/` writes).
**Data gate:** `lib/pages-data.json` sha256
`21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` —
**MATCHES, verified before AND after all checks.**

## VERDICT: READY FOR CYCLE 2 CLOSE — PROBLEMS 1 (P1 0 / P2 0 / P3 1)

Every Cycle 2 claim reproduced independently with my own scripts and my own
measurements — several to the exact integer the coordinator reported
(hero transfer mean 51,418 B, visible-fraction mean 0.749, Button 2 worst
552.19 / 773.06 px, hero @1440 mean 120,333 B, total main words 46,377).
The single problem is a **documentation error in the coordinator's findings
text** (variant count 169 vs the true 138) — not a site defect: all 138 real
variant files exist in `public/` and in `out-cycle2/`.

## 1. PER-CLAIM TABLE

| # | Claim (coordinator) | My measurement | Result |
|---|---|---|---|
| 1a | Hero @390 1×/2×: 31/31 `-m.webp`, transfer mean ~51 KB (was ~121 KB) | 31/31 `-m.webp` at 1× AND 2×; transfer **min 18,736 / max 86,726 / mean 51,418 B** (identical to claimed) | **PASS** |
| 1b | Hero @800px picks 800w | 31/31 `-800.webp`; mean 49,259 B | **PASS** |
| 1c | Hero @1440 1×: 1600w file | 31/31 1600w main file; mean **120,333 B** (identical to claimed); @1440 2× also 1600w (max available, correct) | **PASS** |
| 1d | Cards @1440 1× all `-340`; body @1440 1× all `-400` | Homepage 19/19 cards `-340`; all 57 body images `-400` (after slow scroll); card `-340` mean 11,923 B, body `-400` mean 16,103 B | **PASS** |
| 1e | Cards/body @390 2× pick 680w/800w | Cards 680w main, bodies 800w main — DPR switching works | **PASS** |
| 1f | React `srcSet` camelCase honored by browser | DOM `srcset` attr present (`800w, 1600w`); every viewport/DPR selected the correct file (transfer sizes prove it); `<picture>` source `media="(max-width: 700px)"` present | **PASS** |
| 1g | 0 failed responses | 0 failed (≥400) + 0 console errors across all 7 render passes (390 1×/2×, 800, 1440 1×/2×, 320/390 Button 2) | **PASS** |
| 2a | Visible fraction @390 min 0.63 / max 1.00 / mean 0.749 (was 0.210/0.532/0.269) | Re-measured from rendered hero boxes + actual crop dims: **min 0.630 / max 1.000 / mean 0.749**; worst = condo (box 390×1239, crop 533×1066) | **PASS** |
| 2b | All 31 mobile crops: subject in frame, alt-exact | All 31 viewed (4 contact sheets + full-size: contact, condo, about). Subjects in frame. Contact re-crop x0=120 confirmed: crew member (man on phone) + 2 air movers fully in frame. Condo: both workers + ladder + leak + bucket fully in frame. About: 2 crew complete (3rd worker's edge sliver at far right only) | **PASS** |
| 3a | Sewage-3 → Pexels 4239074, 800×450, alt updated | File sha `8c0380ae…` (matches claim), 800×450, 11,978 B; `-400` variant sha `defeef29…`, 400×225; alt in `lib/body-images.json` + export HTML verbatim as claimed; srcset wires the `-400` variant; EXIF 0 both files | **PASS** |
| 3b | Installed sewage photo alt-exact + 101% relevant (viewed full-size by me) | Gloved (yellow) hand scrubbing a toilet bowl with a brush; green disinfectant bottle with red cap on the floor beside it — alt-exact, real photo, 101% relevant to the sewage/sanitizing section | **PASS** |
| 3c | Reuse nets CLEAR (fresh disk, my own run — not trusted from `qa/opt2-p3-reuse.json`) | Corpus 2,998 files (`*/public/images`): md5 **0 hits** both files; filename net **0**; Pexels-ID grep: 1 mention outside Midvale = Chesterfield scouted-and-REJECTED (same-shoot sibling 4239068, different photo — not a reuse); closest aHash8 = 12, aHash16 58 → viewed: Plano 3 rooftop water-tank photo, **DIFFERENT** | **PASS** |
| 3d | Basement-3 deliberately left; kill-list claims plausible (4092030 on Plano 3) | 4092030, 4092026, 10847198 all present on Plano 3 as `crawl-space-<id>.webp` (+variants); 4092030 viewed by me: real unfinished-basement interior (joists, water heater, concrete floor) | **PASS** |
| 4 | Real LCP could NOT be measured from this cell (Chromium 24/24 ERR_TUNNEL_CONNECTION_FAILED); curl fallback honestly labelled | My own live navigation: **ERR_TUNNEL_CONNECTION_FAILED** for the live site AND example.com; curl 200 both (TTFB 2.73 s live / 2.30 s example — proxy path). The LCP report labels every LCP/FCP/CLS cell NOT MEASURED and the "well under 2.5 s" as an inference, not a measurement | **PASS** (limitation real, labelling honest) |
| 5 | Full regression on `out-cycle2/` | See §2 — all gates pass | **PASS** |

## 2. FULL REGRESSION (my own scripts, `qa/reverify2-static.py` + `qa/reverify2-render.py`)

| Check | Result |
|---|---|
| Routes 200 + H1==1 | **31/31** at 390/800/1440 (1×/2×) and 320 |
| Fullness | **31/31 FULL** — visible main words (script-excluded) total **46,377**; thinnest disclaimer **309** words (Cycle 1 baseline 308) |
| Verbatim | **0 missing** — 3,331 doc segments (2,900 unique: h1/intro/blocks/list items/table headers+cells/FAQ q+a, link annotations stripped) + 92 trust chips + 31 eyebrows, all present in visible main text |
| FAQ | **142/142** questions + answers visible at load; 28 FAQPage blocks in schema |
| Tables | **43/43** rendered |
| Links | **0 broken, 0 orphans, 0 body self-links** (every internal href resolves; every route linked from somewhere) |
| Button 2 | **31/31 @320 worst 552.19 px** (condo) ≤ 568 gate; **31/31 @390 worst 773.06 px** (condo) ≤ 844 gate |
| Overflow | **0 @320 / @390 / @1440** (all passes) |
| Console / failed | **0 console errors, 0 failed responses** (all 7 render passes) |
| Images | **107/107 main + 138/138 variants exist** in `out-cycle2/`; after slow scroll + settle, **107/107 images loaded** (0 unloaded, 0 failed). Initial-load probes show only above-fold lazy images — slow scroll required, as in Cycle 1 |
| Schema | **254 blocks**, 0 parse errors. Types: BreadcrumbList 31, FAQPage 28, WebPage 29, AboutPage 1, ContactPage 1, ImageObject 107, HowTo 36, Service 19, HomeAndConstructionBusiness 1, WebSite 1. contentUrl **107/107** present locally |
| Sitemap / canonicals / robots | Sitemap **31 locs** = routes exactly; canonicals all match the Pages base (`https://growthaura.github.io/midvale-water-damage/`, home with trailing slash); robots `Allow: /` + Pages sitemap |
| localhost / double-slash | localhost **1** — inside `polyfills-*.js` framework string only (same as Cycle 1, non-defect); double-slash **0** |
| 404 | Returns **404**; exactly 1 noindex page (`404.html`) |
| EXIF | **0** on all 138 variants + both sewage files (exiftool EXIF/XMP/IPTC/ICC/MakerNotes/GPS/IFD0) |
| Data gate | sha `21c6e7f2…` verified before AND after all checks — still matching |

## 3. PROBLEMS

### P3-1 — Coordinator's "169 variants" count is wrong (documentation only, NOT a site defect)
- The findings claim "all 169 variant files exist in `out-cycle2/`" and
  "31+31+19+57 = 169 variants total". The arithmetic is wrong:
  31 hero-800w + 31 mobile crops + 19 card-340w + 57 body-400w = **138**.
  The 169 figure adds the 31 mobile crops a second time.
- Disk truth (my count): `public/images` = 245 files = 107 main + **138 variants**;
  `out-cycle2/images` = 245 files, identical set; 0 missing.
  `qa/opt2-variants.json` manifests only heroes (31) + cards (19) — body
  variants are not manifested there, but disk is authoritative.
- **Fix:** correct the count to 138 in the Cycle 2 findings. No site change needed.

## 4. MY OWN PROBE ARTIFACTS (owned plainly, not site defects)

1. **Verbatim "9 missing segments" (first run)** — my `norm()` did not collapse
   the space BeautifulSoup inserts before punctuation at element boundaries
   (`"side , closer"` vs `"side, closer"`). All 9 were bold-lead list items.
   Fixed the normaliser + confirmed each item in the rendered `<li>` text:
   **0 missing**.
2. **FAQ answer 141/142 (first run)** — my per-route check matched the raw
   answer including its `(/sewage-backup-cleanup/)` link annotation; the
   rendered answer has the annotation as a real link. Stripping annotations
   first: **142/142**.
3. **Sitemap/canonical "mismatch" (first run)** — my expected homepage URL
   omitted the trailing slash; the sitemap/canonical form
   `.../midvale-water-damage/` is correct. Fixed expectation: **31/31**.
4. **Schema "0 blocks" (second run)** — I decomposed `<script>` tags from
   `<main>` before counting JSON-LD (the blocks live inside `<main>`).
   Reordered: count schema first, then decompose. **254 blocks**.
5. **localhost "0" (first run)** — my grep excluded `*.js`; including it finds
   the 1 known polyfills.js framework string. **localhost 1 (non-defect)**.
6. **Reuse net v1 killed, v2 too slow** — my first corpus walked all of
   `~/workspace` (114,010 image files, mostly QA screenshots/exports) and
   would have taken hours. Killed it; re-ran scoped to `*/public/images`
   (2,998 files, parallel) — the corpus that decides the reuse question.
7. **Contact sheet staleness** — `qa/opt2-crops-sheet2.png` (22:38) predates the
   contact re-crop (22:40); its contact panel still shows the old center crop
   with the crew member cut off. The installed `contact-m.webp` (sha-identical
   in `public/` and `out-cycle2/`) is the fixed crop — verified full-size by me.

## 5. CARRIED OBSERVATIONS (not problems)

- **O-1 Real LCP still unmeasured** — needs a machine with real egress
  (`qa/lcp-measure.py` is ready) or PageSpeed Insights against the live URL.
  The mobile-hero win (−57% bytes) is real and measured locally; the
  "well under 2.5 s" real-user figure remains an inference.
- **O-2 Basement-flooding-cleanup-3 aerial stays** — no clean replacement exists;
  his call (generated image, honestly labelled, or accept the aerial).
- **O-3 Footer Google Maps embed** — unverifiable in this VM (no google.com
  egress); needs a real-network eyeball after push. Same as Cycle 1.
- **O-4 Mobile crop worst 63% (condo)** — the 533 px clamp bounds the 2×
  upscale at 1.46×; accepted, as the coordinator recorded.
- **O-5 Picture breakpoint ≤700 px, not the theme's 767 px** — measured
  crossover; at 701–767 px the landscape file fits better. Accepted.
- **O-6 Inner-page single cards pick the 680w file at 1440 1×** (19 instances)
  — correct srcset behaviour: those slots are wider than the homepage's
  245 px services-grid slot, so the browser rightly takes the larger
  candidate. The coordinator's note about area cards is slightly imprecise;
  the rendered outcome is optimal.
- **O-7 Same-shoot note (not a reuse):** Pexels 4239074's shoot-sibling
  4239068 is installed on Chesterfield (different photo, different ID).
  No action — different photo, different site.
- **O-8 Carried from Cycle 1:** mold-remediation-2 (washed-out) +
  water-damage-repair-1 (near-white) unchanged; breadcrumb 24 px accepted;
  repair-hero alt "Midvale home" on an Akron photo (stock attribution).

## 6. EVIDENCE FILES (all under `~/workspace/midvale-water-damage/qa/`)

- `reverify2-static.py` / `reverify2-static.json` — routes, H1, fullness,
  verbatim (2,900 unique segments + chips + eyebrows), FAQ, tables, links,
  schema counts, contentUrls, sitemap/canonicals/robots, localhost,
  double-slash, image files + dims, sewage shas + alt
- `reverify2-render.py` / `reverify2-render-{390-1x,390-2x,800-1x,1440-1x,1440-2x,320-b2,390-b2}.json`
  — per-route render: hero/card/body currentSrc + transferSize, hero box,
  overflow, console, failed responses, H1, Button 2, slow-scroll image load
- `reverify2-reuse3.py` / `reverify2-reuse3.log` / `reverify2-reuse.json` —
  fresh-disk reuse net, 2,998-file corpus (md5 0, filename 0, aHash8 closest 12)
- `FINDINGS-opt-cycle2-reverify-2026-11-14.md` (this file)

## VERDICT RESTATED

**PROBLEMS 1 — READY FOR CYCLE 2 CLOSE.** Srcset proven by real renders at
5 viewport/DPR combinations (hero @390 mean 51,418 B, −57.5% vs Cycle 1;
visible fraction 0.630/1.000/0.749; `srcSet` honored); all 31 mobile crops
subject-in-frame with the contact re-crop confirmed; sewage P3 installed
alt-exact and 101% relevant with reuse nets clear on my own fresh-disk run;
LCP limitation confirmed real and honestly labelled; full regression clean
(31/31 FULL, verbatim 0, FAQ 142/142, tables 43/43, links 0/0/0, Button 2
31/31 @320/@390, overflow 0, console 0, images 107/107, schema 254, data sha
unchanged). The one P3 is a count typo in the coordinator's findings text
(169 vs the true 138 variants) — correct the text; nothing on the site
needs changing.
