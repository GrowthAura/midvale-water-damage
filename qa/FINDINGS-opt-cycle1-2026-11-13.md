# BATCH 2 OPTIMIZATION CYCLE 1 — FINDINGS (coordinator synthesis)

**VERDICT: CYCLE 1 CLOSED — PROBLEMS 0 on independent re-verification. READY FOR RE-PUSH (his word + token only).**

- Site: Midvale UT water damage, 31 routes, Next.js static export, live Pages URL https://growthaura.github.io/midvale-water-damage/
- Data gate: `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — UNCHANGED through the whole cycle (verified at every stage; any change would have been a STOP).
- Local only. No push/deploy/token/DNS. Content 1001% verbatim.

## 1. AUDITS (6 parallel workers, fresh export, all real Chromium where applicable)

**Consolidated audit verdict: PROBLEMS 40 (P1 3 / P2 22 / P3 15) + 6 schema advancement candidates.**

| Worker | File | Verdict |
|---|---|---|
| Images heroes+cards (50) | qa/opt1-images-heroes-cards.md | NOT READY — 29 (P1 3 / P2 20 / P3 6) |
| Images body (57) | qa/opt1-images-body.md | 4 (P1 0 / P2 1 systemic / P3 3) |
| Schema re-audit (178 blocks) | qa/opt1-schema.md | PROBLEMS 0 + 6 candidates |
| Technical SEO | qa/opt1-seo.md | READY — P1 0 / P2 0 / P3 3 carried |
| Content visibility | qa/opt1-content.md | PROBLEMS 0 |
| UI/UX A-to-Z | qa/opt1-uiux.md | 4 (P1 0 / P2 1 / P3 3) |

### P1 (3) — wrong hero photos, alt text factually false (coordinator viewed all 3 full-size, confirmed)
- `heroes/disclaimer.webp`: blurry office photo (laptop/calculator/card terminal); alt claimed a technician with a moisture meter. Nothing water-related.
- `heroes/upstairs-unit-leak-who-pays-utah.webp`: daylight bathroom flood; alt claimed water dripping from an apartment ceiling. No ceiling drip; wrong subject.
- `heroes/water-damage-repair.webp`: worker portrait; alt claimed a newly rebuilt room. No room visible.

### P2 (22)
- All 19 cards oversized: 1200px files vs 245×138 slots @1440 (3.5–4.9×).
- All 57 body images oversized: 1200×675 vs 400×225 slots (3.00× desktop / 3.51× mobile); no srcset.
- Mobile hero `object-fit: cover` crops the sides of wide scenes at 390px.
- Homepage cards repeat the title in plain body text at the end of every description (19 cards).

### P3 (15)
- Burst-pipe card alt (wall cavity, no ice) + cottonwood-3 body alt (rooftop view, no street) — alt-loose.
- 3 cards 1200×800 (3:2) in a 16:9 slot; hero `width/height` attrs 1600×900 vs files 1600×1066; no srcset on any image.
- Mold-remediation-2 washed-out; 4 generic-location body images; water-damage-repair-1 near-white-on-white.
- 12 over-cap verbatim anchors; breadcrumb double-link; single-item BreadcrumbList (all carried, verbatim wins).
- Logo link 43px; radio labels 32px; breadcrumb links 24px (all pass WCAG 24px minimum).

### Clean in audit (no action needed)
- Schema: 178 blocks exact, 0 parse errors, refs 113/113 resolve, 0 invented, contentUrl 31/31 200.
- SEO: robots/sitemap/llms/canonicals/meta/H1/links all clean; 0 malformed `tel:` links (checked after the Tulsa GSC note).
- Content: visible 50,213 / main 46,152 / unique 45,744 words; hidden words in `<main>`: **0**; FAQ 142/142 visible at load — **no accordion exists** (plain h3+p); verbatim 0 missing; thinnest page disclaimer 308 main words (FULL).
- UI/UX: overflow 0, console 0, Button 2 31/31 @320/@390, brokenImgs 0, body 19px, contrast 0 AA failures.

## 2. FIXES (all verified fresh by the independent re-verifier — PROBLEMS 0)

### Images — resize (F1, verified by recovery worker)
- 19 cards → 680×383: 1,489,472 → 633,910 B (−57.4%). 57 body → 800×450: 6,160,088 → 2,826,316 B (−54.1%).
- 76 files total: 7,649,560 → 3,460,226 B (−54.8%, saved 4,189,334 B). Dims exact, EXIF 0 on all 76, quality PASS (6 heaviest viewed full-size, no visible loss). Originals backed up in qa/opt1-images-backup/ (19+57, original dims).
- **Total site image weight: 11,243,230 B → 7,188,454 B (−36%).** srcset NOT added this round (template change, deferred — see §4).

### Images — 3 hero replacements + 1 body swap (F2, completed by recovery worker)
- disclaimer — GENERATED: technician kneeling, pin-type moisture meter on a stained/peeling wall, dark room. 1600×1066, 123,354 B. (Pexels had nothing fitting.)
- upstairs-unit-leak — GENERATED: water streaming from a brown-stained peeling ceiling into the furnished living room below. 1600×1066, 116,246 B. (Pexels had nothing fitting.)
- water-damage-repair — Pexels 40701216: renovated living room, hardwood floors, crown molding (Akron, OH). 1600×1066, 109,092 B.
- body/magna-ut-1 — SWAPPED: Pexels 5587966, aerial Utah home amid autumn trees (Woodland Hills, UT). 800×450. Alt updated to match.
- Coordinator viewed all 3 new heroes full-size: all alt-exact, on-topic, dark-series fit. Reuse nets CLEAR on a fresh-disk corpus (2,269 files, 34 sites; md5 + aHash; Pexels-ID grep 0). The one near flag (gen-disclaimer aHash8 4 vs Plano 3 wet-tile) was visually adjudicated full-size by both the recovery worker and the re-verifier — different subject, dark-tone coincidence, NOT a reuse. Generated images are labelled GENERATED in the findings — never claimed as real job photos; XMP stripped on install (raw generations in qa/gen/, do not install directly). Old heroes backed up in qa/opt1-hero-backup/.
- Alt rewrites (chrome, not doc content): cards/burst-pipe → "Split copper pipe spraying water inside an opened wall cavity with wet wooden studs"; body/cottonwood-3 → "Snowy city rooftops in the Salt Lake Valley with snow-capped mountains under low cloud".

### Schema — 178 → 254 blocks (F3)
- C-1 WebPage `mainEntity`: 83 pure @id refs (28 #faq + 19 #service + 36 #howto-N). C-2: /about → AboutPage, /contact → ContactPage. C-3: +76 ImageObjects (57 body + 19 cards; caption = alt verbatim). C-4: width/height 1600×1066 on 31 hero ImageObjects (PIL-measured). C-5: DOM ids #service (19/19), #howto-N (25/31 pages), #breadcrumb (30/31 — homepage has no breadcrumb nav, correct), #hero-image (31/31). C-6 ItemList SKIPPED (weak/redundant).
- Validation 48/48 PASS on the real compiled schema; re-verifier confirmed 254 exact, 107/107 contentUrls 200, 0 invented.

### UI/UX + CSS (F4)
- Card title echo fixed: anchor is now its own CTA line (copper-dark #9d5418 ~5.7:1 AA, 700 weight, 18px, → bound by nbsp, pinned to card bottom). All 19 CTA texts match the `anchor:` strings exactly — no word removed or reworded. Grid 4/4/4/4 unchanged.
- Logo link 43→48px; radio labels 32→48px (form still 6 fields + verbatim submit); breadcrumb 24px LEFT (accepted).
- Hero attrs 1600×900 → 1600×1066, 31/31.
- Regression owned + fixed: the 48px brand pushed Button 2 @320 to 568.2px (0.2px past the fold); the first compensation (hero padding) was measured not to move it and was reverted; the correct fix (header row-gap 24→8px at ≤360px only) restored Button 2 worst @320 to 552.2px (15.8px headroom), @390 = 773.1px.

### Interruptions (owned plainly)
- F1 (resize) + F2 (heroes) were INTERRUPTED by the runtime mid-work. Recovery: F1's resize was complete on disk (verified: 19/19 + 57/57 at target dims, backup complete); F2 had only backed up the 3 old heroes. A single recovery worker verified F1 + completed F2. No work was lost; no file was re-done blind.

## 3. INDEPENDENT RE-VERIFICATION (fresh agent, did not audit or fix)

qa/FINDINGS-opt-cycle1-reverify-2026-11-13.md — **PROBLEMS 0 (P1 0 / P2 0 / P3 0) — READY FOR CYCLE 1 CLOSE.**
- Resize exact (19×680×383, 57×800×450; 634 KB / 2.83 MB / 7.19 MB; EXIF 0 all 107; 6 heaviest viewed — sharp).
- 3 new heroes + magna swap viewed full-size, alt-exact; reuse re-run with the verifier's own script (2,268-file fresh-disk corpus): md5 0, Pexels-ID grep 0.
- Alt rewrites exact; old alts gone. Schema 254 exact, refs resolve, 107/107 contentUrls 200, honest trace 0 invented.
- Card CTA distinct (viewed @1440 + @390), 19/19 texts exact, grid 4/4/4/4; logo/radio 48px; hero attrs 1600×1066.
- Regression: fullness 31/31 FULL; verbatim 0 missing (3,040 segments); FAQ 142/142; tables 43/43; links 0 broken/orphans/self-links; paren 0; localhost 1 (polyfills.js framework string only); double-slash 0; sitemap 31/31 200; 404 noindex; 31/31 index,follow; Button 2 31/31 @320 (worst 552) + @390 (worst 773); overflow 0 (93 measurements); console 0 (93 loads); images 107/107 render; real clicks keep subpath; hidden words 0.

## 4. DELIBERATELY LEFT (not problems)

- **Mobile hero crop — known limitation, measured:** visible fraction @390 min 21.0% / max 53.2% / mean 26.9%; 28/31 pages ≤28.6%. No clean CSS fix exists (box is tall because content is tall; `contain` letterboxes; `object-position` can't widen the view; per-hero mobile crops = 31 new assets, out of scope). Mitigation: dark shade makes the photo an atmospheric backdrop; centre-weighted heroes survive the crop.
- **srcset — deferred:** "no srcset anywhere" stands as a P3. Resize to 2×-DPR slot widths achieves MEDIUM now; srcset is the next cycle's job (a parallel srcset job was observed in the dir during re-verification but landed no changes — no srcset attributes exist in the source).
- **Mold-remediation-2 washed-out** (subject correct, alt exact; no better fogging photo found in 2 searches) + **water-damage-repair-1 near-white-on-white** (on-topic; no better photo in this pass).
- **Breadcrumb links 24px** (accepted; pass WCAG 24px minimum). **12 over-cap verbatim anchors, breadcrumb double-link, single-item BreadcrumbList** (accepted tensions — verbatim wins).
- **Repair-hero alt says "Midvale home" for an Akron, Ohio stock photo** (alt kept verbatim per the fix brief; same framing as other stock heroes' "Midvale" alts — carried as an observation, not a defect).
- **Card `<img>` attrs 800×450 vs 680×383 files** (aspect ratios match, no distortion — observation only).
- **Maps embed** unconfirmable in this VM (no google.com egress) — needs a real-network eyeball after push. **LCP lab numbers** inflated during the audits by shared-cell CPU contention (FCP rose by the same factor, CLS 0, heroes byte-identical) — re-measure on a quiet cell / real hosting.

## 5. WOULD ANOTHER CYCLE STILL FIND IMPROVEMENTS? YES.

Cycle 2 would still have real work: (1) **srcset** — the deferred P3, biggest remaining image-weight win on mobile; (2) **per-hero mobile crops** (31 portrait crops) to fix the 21–28% visible-fraction limitation; (3) **LCP re-measure** on a quiet cell / real hosting; (4) the remaining generic-location P3s (2 aerial-suburb body images) if better Utah-plausible photos turn up; (5) a fresh full A-to-Z re-audit, which is the point of the cycles. Cycle 1 itself found nothing left un-fixed from its own audit — every P1/P2 it found is closed and re-verified.

## 6. FILES

- Audits: qa/opt1-images-heroes-cards.{json,md}, qa/opt1-images-body.{json,md}, qa/opt1-schema.{json,md}, qa/opt1-seo.{json,md}, qa/opt1-content.{json,md}, qa/opt1-uiux.{json,md} (+ qa/opt1-uiux/ screenshots)
- Fixes: qa/opt1-fix-resize.md, qa/opt1-fix-heroes.md (+ qa/opt1-hero-reuse.py/.json, qa/opt1-magna-reuse.py/.json, qa/gen/ raw generations), qa/opt1-fix-schema.md (+ qa/opt1-fix-schema-verify.json), qa/opt1-fix-uiux.md (+ qa/opt1-fix-baseline.json, qa/opt1-fix-after.json, qa/opt1-fix-uiux/before + after)
- Re-verification: qa/FINDINGS-opt-cycle1-reverify-2026-11-13.md (+ qa/reverify-*.json, qa/reverify-home-*.png)
- Backups: qa/opt1-images-backup/ (76 originals), qa/opt1-hero-backup/ (3 old heroes), qa/final5-fix/orig-backup/ (Stage 5 cards)
- Review pack: ~/workspace/your_files/midvale-opt-cycle1-review.pdf (fresh, 62 full-page shots — see Cycle 1 report)
