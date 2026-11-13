# FINDINGS — Midvale UT Design Round (2026-11-13)

Coordinator: design coordinator (spawned 2026-11-13 ~02:08 PKT).
Order: user 2026-11-13 ~01:30 PKT — every service + location page 4–5 relevant
images (text/image containers, sticky beside long paragraphs), beautiful
header/footer, NO em/en dashes in header/footer, NO underline under internal
links anywhere, beautiful H2/H3 colouring, body text ≥18px, service + location
pages 10x better. Deadline ~04:30 PKT; independent 10x UI/UX testing ~03:30 PKT.
Local only. Re-push only on his word + token (parent pushes).

## STEP 0 — doc freshness (DONE ~02:15 PKT)
Live doc re-fetched with includeTabsContent=true (`/tmp/midvale-doc-fresh.json` —
note: /tmp was later wiped by a VM replacement; the check itself is recorded
here and in PROGRESS.md): 31 tabs, 47,188 total words — EXACT match to the
frozen read (per-tab counts = data counts + ~45–49 for URL/meta/H1/buttons
lines). **Doc UNCHANGED.** Built on `lib/pages-data.json` (sha256 unchanged).

## Workers (5, all DONE and verified by coordinator against files)
- G1 images (emergency, basement, window-well, burst-pipe, sewage): 13/15.
- G2 images (water-heater, swamp-cooler, ceiling, crawl-space, hardwood): 12/15.
- G3 images (condo, commercial, storm, mold, leak-detection): 15/15.
- G4 images (water-damage-repair + 3 locations): 11/12.
- D design/CSS (renderer, header/footer, H2/H3, dashes, underlines, body 18px):
  DONE; findings `qa/FINDINGS-design-css-2026-11-13.md`.

## Images — 51 new body images, 19 pages (57 slots, 6 empty)
All real Pexels photos, judged by VIEWED pixels, 1200×675 WebP q82 (except
3 G1 files at q50–q70, noted below), 0 EXIF, no "AI" in filename/alt/metadata.
Reuse checks: md5 vs 50 existing, dup md5 across body dir, aHash16 >8,
Pexels-ID workspace checks. Manifests `qa/images-design-g1.json` … `g4.json`,
merged contract `lib/body-images.json`.

Per-page totals (hero + body):
- 4 images (hero + 3): basement, window-well, burst-pipe, sewage,
  swamp-cooler, ceiling, hardwood, condo, commercial, storm, mold,
  leak-detection, water-damage-repair, cottonwood-heights, magna (15 pages)
- 3 images (hero + 2): water-heater, south-salt-lake (2 pages)
- 2 images (hero + 1): emergency-water-extraction, crawl-space (2 pages)

Per-page body slots (afterH2 = 0-based H2 index; layout split|sticky):
- /emergency-water-extraction: 1 — slot 2 sticky (extraction-2). Slots 1+3 EMPTY.
- /basement-flooding-cleanup: 3 — 0 sticky, 6 split, 7 split.
- /window-well-flooding: 3 — 0 sticky, 2 split, 8 split.
- /burst-pipe-water-damage: 3 — 0 sticky, 4 split, 6 split (slot 3 REPLACED, see below).
- /sewage-backup-cleanup: 3 — 3 split, 6 sticky, 10 split.
- /water-heater-leak-cleanup: 2 — 1 sticky, 7 split. Slot 2 EMPTY.
- /swamp-cooler-leak-water-damage: 3 — 0 sticky, 6 split, 8 split.
- /ceiling-water-damage: 3 — 2 sticky, 4 split, 7 split.
- /crawl-space-water-damage: 1 — slot 3 split. Slots 1+2 EMPTY.
- /hardwood-floor-cabinet-drying: 3 — 0 split, 4 split, 9 sticky.
- /condo-apartment-water-damage: 3 — 0 split, 7 split, 10 split.
- /commercial-water-damage: 3 — 1 split, 3 split, 10 split.
- /storm-flood-damage: 3 — 0 split, 2 sticky, 9 split.
- /mold-remediation: 3 — 1 split, 4 sticky, 13 split.
- /water-leak-detection: 3 — 2 split, 4 sticky, 8 split.
- /water-damage-repair: 3 — 2 split, 5 sticky, 10 split.
- /locations/cottonwood-heights-ut: 3 — 1 sticky, 3 split, 8 split.
- /locations/south-salt-lake-ut: 2 — 1 sticky, 2 split. Slot 3 EMPTY.
- /locations/magna-ut: 3 — 1 split, 5 split, 11 sticky.
Total body images rendered (design-CSS verifier, desktop): 51. Grid sections: 51.

### Empty slots (honest, never forced)
- emergency-water-extraction slots 1 (standing water) + 3 (wet carpet): every
  fitting Pexels candidate is live on another site (Plano 3, Lancaster,
  Owasso, Littleton, Belleville) or is a wrong-context photo (aerial floods,
  domestic vacuums, branded uniforms). Coordinator re-tried 3 fresh queries;
  the only new wet-carpet candidate (14675105, pro steam-cleaning a rug) was
  REJECTED for legible logos on the worker's vest.
- crawl-space slots 1+2: no fitting under-house photo on Pexels.
- water-heater slot 2 (laundry): no fitting photo.
- south-salt-lake slot 3 (Older Homes, Older Pipes): no fitting clean photo.

### Reuse catch — G1 burst-pipe-3 REPLACED by coordinator (2026-11-13 ~03:00 PKT)
- G1 adopted Pexels 16509869 (gloved hands tightening a pipe fitting) claiming
  "candidate-only". G4's deep checks flagged it: the photo IS live on
  Belleville as its burst-pipe hero. Coordinator verified independently:
  aHash16 distance **0** vs Belleville's
  `site/public/images/heroes/burst-pipe-water-damage.webp` (different md5 =
  different crop/encode, same photo). **Confirmed cross-site reuse.**
- Replacement: Pexels **35072812** (hands gripping a weathered metal pipe
  fitting during repair), viewed at full size, fits slot 3's section
  "Our Broken Pipe Cleanup Midvale Utah Process" (afterH2 6). Processed
  1200×675 WebP q82, 58KB, 0 EXIF, md5 4b1e376f87fd4cf5410c721f9beba4c5.
  aHash16 vs Belleville hero = 129; 0 reuse hits vs all Midvale images.
- 35072812 trace note (checked, NOT a reuse): the ID appears in PG
  `past_pexels_ids.json` + `banned_ids.json` and in a Lancaster harvest file.
  Those lists are corpus aggregates that include harvest/candidate IDs. The
  Acworth corpus manifest attributes this ID SOLELY to the Lancaster harvest
  file (`harvest-plumber.html`, a Pexels search-results list, alt "Craftsman
  skillfully repairing machinery with tools"), and a full-workspace filename
  search found ZERO image files named *35072812* in any site tree (15 site
  trees scanned + full-workspace find). Candidate-only, not live anywhere.

### Weak / marginal images (flagged honestly for the 10x testing round)
- commercial-3: B&W flooded corridor — marginal topic fit.
- basement 1–3: dry finished rooms — weak relevance (no water visible).
- burst-pipe-1: downspout-style pipe (not a burst pipe).
- sewage-2: drain grate with cast markings.
- 3 G1 files at reduced quality q50–q70 (burst-pipe-1, sewage-1, sewage-3).
- 9551366 (G2): candidate-only, not a reuse (verified: no .webp filename hits
  workspace-wide; only an Elyria manifest mention).

## Design changes (worker D + coordinator wiring pass)
- H2-section grid renderer (`components/doc-page.tsx`): text | image split
  containers; `sticky` figures use position:sticky top 96px beside long
  sections; reads `lib/body-images.json`, graceful when absent. No content
  words touched (data sha256 unchanged, word-diff 0).
- Header/footer polish: spacing, alignment, typography, contrast. 0 em/en
  dashes in header/footer visible text (checked on the built homepage text).
- NO underline on ANY internal link: 1,313 links checked in the render
  verifier; the only flagged items are tel: `.btn` buttons whose 2px solid
  BORDER is a button treatment (text-decoration: none). Built CSS
  `text-decoration:underline` = 0.
- H2/H3 colouring: H2 pine `#0e3b38` (rgb 14,59,56) + copper bar; H3 pine-2
  `#15524c` (rgb 21,82,76). Consistent on all 31 pages. Contrast worst
  5.65:1 (AA), body 12.82:1 (AAA).
- Body text 18px minimum: desktop small-count = 0 on every page. The ONLY
  <18px text is the hero eyebrow at 14px @≤360px (load-bearing for Button 2
  visibility; heading/eyebrow sizes unchanged per the order).
- Contact-form em dashes FIXED by coordinator (2 lines,
  `components/contact-form.tsx`): notice chrome "— calling is faster" and
  "Thanks — this preview form" now use commas. These are template chrome, not
  verbatim tab text (the doc has 0 dashes).
- Files changed (design round): globals.css, doc-page.tsx, not-found.tsx,
  page.tsx, contact-form.tsx (2 dashes), lib/body-images.json (new),
  public/images/body/ (51 new files), qa/ manifests + findings. Nothing else.

## Verification — fresh, on the final build (export exit 0, served on the
## /midvale-water-damage/ subpath locally)
### 1. Static — qa/verify-linkfix.py (run 2, on the design build): PROBLEMS 0
- pages 31, problems 0. Fullness 31/31 FULL (0 EMPTY, 0 THIN).
- Verbatim: missing words total 0; extra 749 (annotation tokens 552
  subtracted + heading labels + trust badges/form chrome — same explained
  scale as the linkfix round). FAQ data 142 = ld 142. Tables 43/43.
- Links: body 143 + card 19 = 162 kept. Orphans []. Self-links [].
- Visible `(/.../)` in out/ html/txt/xml/css = 0 (7 js/webp hits are Next.js
  chunk regexes + binary WebP bytes, not visible text).
- H1/title/meta True on 31/31. Footer navs: Services 8, Nearby cities 3,
  About and resources 10, Help 4.
### 2. Design/CSS render — qa/verify-design-css.py (run 2): PROBLEMS 0
- Overflow 0 (all 31 × 3 viewports). H1 1/page. Button 2 visible scroll-0
  31/31 @320 AND @390 (worst bottom 497.2px vs 568 fold @320). Buttons equal.
- Underline: 0 real violations (see tel-button note above).
- Header dashes 0, footer dashes 0, paren paths 0. H2/H3 colours consistent.
- Body imgs 51 rendered, grid sections 51. Contact form present (9 fields
  incl. submit). Console errors 0, failed requests 0. Footer links 27/page.
- Adjudicated non-defects: (a) the script's `orphans` list is a subpath-prefix
  artifact — it normalises `/midvale-water-damage/...` hrefs against the
  bare route set; the authoritative static check says orphans []. (b) The
  script's `small_text` is only the eyebrow 14px @m320 (see above).
### 3. Render + real-click — qa/verify-linkfix-render.py (run 2): PROBLEMS 0
- All 31 routes × 3 viewports: paren 0, overflow 0, console 0, failed 0,
  Button 2 visible True everywhere.
- Cards 19/19: equal widths, image ratio 1.778 (16:9), deco none, nested_a 1.
- Real clicks 7/7 land on the right pages with the right H1s (card, logo,
  body link, inner body link, footer, header, breadcrumb). Two show
  `subpath_kept: false` (logo->home, breadcrumb->home) — the URL is the bare
  subpath root `.../midvale-water-damage` without a trailing slash, so the
  script's `"/midvale-water-damage/" in url` string check misses; the H1s
  prove the landing is correct. Checker artifact, not a navigation failure.
- Mobile menu: opens (flex|main-nav open|aria:true), scroll lock works
  (body overflow hidden|fixed). The script's click on
  `#main-nav a[href*='burst-pipe-water-damage']` timed out — because the nav
  contains NO such link: #main-nav has exactly 3 links (Home, Emergency
  Water Extraction, Sewage Backup Cleanup) BY DESIGN on desktop AND mobile
  (same element; verified in `components/site.tsx` and in a live desktop
  probe). Full navigation lives in the footer (27 links) + homepage cards +
  body links. Verifier expectation error, not a site defect; pre-existing,
  not introduced by this round.
- Location-card images show natural [0,0] at scroll-0: lazy-load, below the
  fold — not a defect.

## Visual spot-checks (coordinator, viewed pixels)
- Burst-pipe desktop: header clean, hero with equal buttons, H2 pine + copper
  bar, split text|image section rendering. Emergency mobile @390: header
  stacks cleanly, equal full-width buttons, no overflow, no dashes.
- Replacement burst-pipe-3 crop (1200×675): hands on weathered pipe fitting,
  no legible brand text in the crop.

## Review pack
`~/workspace/your_files/midvale-design-review.pdf` — 31 pages (desktop +
mobile-390 per route, labelled headers), 5.9 MB, built from the fresh render
screenshots of this build (`qa/build-review-pdf-design.py`).

## PROBLEMS: 0 — READY FOR RE-PUSH (parent pushes with the token)
The design round + the link-fix ride together in the same push (link-fix was
verified PROBLEMS 0 and is included in this build). Local only until his word.

## Open / honest gaps (for the parent + the 10x testing round)
- 6 empty image slots (listed above) — emergency (2) is the most visible.
- Marginal/weak images listed above — 10x testing to adjudicate; replace any
  it fails, then re-verify before the push if time allows.
- Pre-existing, unchanged by this round: P3 locations-hub trailing comma
  (doc-driven, his call); 5 flagged image slots awaiting real job photos;
  LCP + footer map tiles re-measure on real hosting.
- Script/ops notes: /tmp was wiped by a VM replacement mid-round
  (previews + `/tmp/linkfix-serve.py` lost); serve script recreated and a
  persistent copy saved at `qa/linkfix-serve.py`. The background 35072812
  workspace grep took ~5.5 min (full-tree grep is slow — use targeted scans).
- The 10x UI/UX testing round (~03:30 PKT) runs on this build; its findings
  are to be fixed before the ~04:30 PKT deadline.
