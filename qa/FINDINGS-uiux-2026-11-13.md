# FINDINGS — Midvale UT Stage 1 UI/UX Round: INDEPENDENT VERIFICATION (2026-11-13)

**Verifier:** independent verifier (spawned ~10:02 PKT; did NOT do any Stage 1 fix).
**Method:** fresh export (`npm run export` exit 0, first attempt), served on
`/midvale-water-damage/` via `qa/linkfix-serve.py` port 8341. Served homepage
confirmed really Midvale before measuring: H1 `24/7 Water Damage Restoration
in Midvale, UT 84047`, phone `(385) 337-3560`. Data sha256 unchanged:
`21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`.
**Raw data:** `qa/uiux-verify-static-2026-11-13.json`,
`qa/uiux-faqld-2026-11-13.json`, `qa/uiux-verify-render-2026-11-13.json`,
`qa/uiux-adjudicate-2026-11-13.json`, `qa/uiux-images-all-2026-11-13.json`.
**Scripts (fresh, written for this verification):**
`qa/uiux-verify-static-2026-11-13.py` (reused intact from the interrupted
verifier — its JSON was empty, its results are mine, run fresh),
`qa/uiux-faqld-2026-11-13.py`, `qa/uiux-verify-render-2026-11-13.py`,
`qa/uiux-adjudicate-2026-11-13.py`, `qa/uiux-images-all-2026-11-13.py`,
`qa/build-review-pdf-uiux.py`.

## VERDICT: PROBLEMS 0 — READY FOR RE-PUSH

After adjudication, **P1 0 · P2 0 · P3 0**. The raw runs flagged 203 items
(30 static + 173 render); every one was traced to a verifier-script artifact
and re-measured clean — see "Script errors owned" below. Nothing was waived
on trust: each category got an independent re-probe with a corrected method.
The Stage 1 fixes all hold: 15 body swaps + 2 alt fixes, 9 hero/card swaps,
4 CSS fixes.

## PROBLEMS

None.

## 1. Static — fullness / verbatim / links / FAQ / tables (fresh export)

- Fullness **31/31 FULL** (0 EMPTY, 0 THIN). Verbatim: per-segment
  contiguous-subsequence check vs `lib/pages-data.json`, annotation tokens
  `(/.../)` stripped as link metadata — **0 segments missing**, 0 reordered.
- H1 **1/page on 31/31**, text matches data on all. Meta title + description
  verbatim on all 31.
- FAQ visible **142/142**, item counts match data per page; FAQPage JSON-LD
  **142/142** with Q/A text matching visible (independent raw-parse check —
  see script error #2).
- Tables **43/43**, counts match data per page.
- Links: body **143**, card **19** (total 162, per-route counts match the
  link inventory on all 31). Broken **0**, orphans **0**, body self-links
  **0**, visible `(/.../)` path text **0** (rendered DOM + out/ HTML).
- Images: **107 files** in out/ (31 heroes + 57 body + 19 cards),
  **107 distinct srcs** in `<main>`, 0 srcs missing on disk, 0 imgs missing alt.

## 2. Render — Playwright Chromium, 31 routes x 1440/390/320

- Button 2 visible at scroll-0 on **31/31 @320 AND 31/31 @390**. Worst
  bottom **554px @320x568** (`/condo-apartment-water-damage`, 14px headroom —
  holds, see OBS-4) and **767px @390x844** (same route). Buttons exactly
  equal size on all routes/viewports. H1 visible on all; H1 30px @320 ≥ H2
  28px on 31/31 (hierarchy fix holds).
- Overflow **0** at 320/390/1440 on all routes. Console errors **0**.
  Failed requests **0 local, 0 Maps** this run (no Maps request observed;
  the known VM-no-route-to-google.com limit stands as OBS-5).
- Homepage service-card grid @1440: **16 cards, 4 cols, rows 4/4/4/4**,
  247px cards, image height 138px uniform. No orphan row.
- Table scroll cue @390: correct on every `.table-wrap` — opacity 1 at
  scroll 0 on overflowing tables, 0 at max scroll (re-probed with a wait),
  0 on fitting tables.
- Contact form: **6 fields** (Name, Phone, Address or ZIP, What happened,
  Is the water still running? Yes/No/Not sure, Best time to call), submit
  verbatim `[Send My Request]`, honest no-send notice present.
- Real clicks, subpath kept on all: homepage card → emergency page (correct
  H1), body link → hardwood page (correct H1), logo → home, footer link →
  about (correct H1), mobile menu @390 opens (3 links) and navigates home.
- Images in rendered DOM: **107/107 render** after a proper slow scroll,
  0 failed requests (definitive re-check — see script error #1).

## 3. Images — judged by viewed pixels (full size)

**REPLACE 3/3 PASS:**
- `burst-pipe-water-damage-3.webp` — gloved hands, pipe wrench on a burst
  copper fitting with brass valve, water dripping. A pipe, not a plank.
  (Nit: tiny illegible maker stamp on the valve.)
- `magna-ut-2.webp` — older Utah main street, brick/wood storefronts with
  awnings, pickups, foothills and mountains. **No legible signage anywhere —
  Wabasha is gone.**
- `swamp-cooler-leak-water-damage-3.webp` — wall-mounted louvered
  evaporative cooler on a stucco house, water dripping from the drain,
  desert + red-rock mesa behind. A swamp cooler, not a window AC.

**WEAK 9/9 sampled PASS:** `hardwood-2` (brand-free US kitchen, Panasonic
gone; dry room, see OBS-2), `water-heater-1` (tank heater + washer/dryer,
puddle at base), `south-salt-lake-2` (moldy wall, worker with moisture
meter, 2 blue air movers + dehumidifier), `burst-pipe-1` (frozen burst
copper supply pipe, icicles, water spray — not a downspout), `magna-1`
(no pillarbox bars; generic leafy suburb, see OBS-1), `magna-3` (old white
clapboard house + new wood-frame addition under construction),
`sewage-2` (floor drain in wet concrete, mop + bucket; EN124 marks gone),
`swamp-cooler-2` (Utah ranch house, large rooftop evaporative cooler,
arid foothills), `window-well-3` (corrugated well filled with rainwater).

**Generated fills 4/7 sampled PASS:** `commercial-3` (COLOUR wet office,
5 blue air movers + dehumidifier — the old B&W P3 is resolved),
`emergency-1` (truck-mounted extraction unit, hoses into house, crew on a
flooded living-room floor), `crawl-space-1` (dark crawl space, joists,
piers, standing water), `water-heater-2` (worker at a heater in a flooded
basement, mop in hand). The other 3 fills were verified in Stage 0
(PROBLEMS 0) and render in this build (107/107).

**Heroes/cards 2/9 sampled PASS:** `heroes/water-damage-repair.webp`
(worker in hard hat + respirator fitting trim; blank wall left for the
headline; trowel hand slightly cut at bottom edge — worker's own nit),
`cards/burst-pipe-water-damage.webp` (burst copper pipe in an opened wall,
water spraying — unmistakably burst pipe, not frozen-pipes).

**Metadata:** EXIF/XMP/ICC **0 on all 24 swapped files** (raw-byte scan).
Alt fixes render correctly: `ceiling-1` now "A man sanding a green drywall
ceiling with a power sander" (was "ladder"); `sewage-1` now "A worker in a
white protective suit and blue gloves holding a pump sprayer in a kitchen"
(was "spray bottle + cloth").

**Reuse note (honest limit):** I did NOT re-run the full-corpus hash DB —
the fix workers' manifests record md5 0 vs the complete live-image set and
aHash adjudications (body manifest + heroes/cards manifest on disk). My
independent check was full-size pixel viewing of 15 body + 2 hero/card
images: none matches any image I know from a past site, and the site's own
107 files are distinct srcs. The full-corpus DB run's VM failure was
already honestly reported by the body worker.

## Script errors owned (all 203 raw flags were these — none was a site defect)

1. **My render script's scroll vs `scroll-behavior: smooth`** (globals.css
   line 21): 60ms-step `scrollTo` calls animated and lagged, so the
   viewport never reached the bottom of long pages before the script
   scrolled back to top — lazy images there never loaded. **48 false P1
   "broken images"**. Adjudicated: multi-pass scroll until scrollHeight
   stable + 2s wait on all 31 routes → **107/107 render, 0 failed
   requests** (`qa/uiux-images-all-2026-11-13.py`). The static check also
   proved all 107 files exist on disk, and the first run itself recorded
   0 failed requests.
2. **Static script's `main_text_of()` decomposes `<script>` in `<main>`**
   before the FAQ JSON-LD check: the FAQPage block lives inside `<main>`,
   so the check saw 0. **29 false P1s.** Adjudicated: independent
   raw-regex parse (no decompose) → **FAQPage 142/142, 0 problems**
   (`qa/uiux-faqld-2026-11-13.py`).
3. **Static script's broken-link check misclassifies basepath+anchor
   links** (`/midvale-water-damage#areas`): **3 false P1s.** The target
   `id="areas"` exists on the homepage; these are valid anchor links
   (same artifact the 10x verifier owned).
4. **My render script's table-cue check read `::after` opacity
   immediately** after setting `scrollLeft` — container queries
   (`scroll-state`) update asynchronously. **31 false P2s.** Adjudicated:
   500ms wait + rAF → cue 1 at scroll 0, 0 at max scroll, 0 on fitting
   tables (`qa/uiux-adjudicate-2026-11-13.py`).
5. **My render script's body-text sampler included chrome elements:**
   `p.eyebrow` (18px desktop, 14px @≤360px by design) and breadcrumb
   `<li>` (18px). **93 false P3s.** All actual body copy (intro, section
   p, card p, page-body p, list li) is **19px** on every sampled
   page/viewport.
6. **My render script counted radio inputs as separate fields:** the
   "water still running" question is 3 radio inputs = 1 field. **1 false
   P2.** Form is 6 fields as specified.

## Observations (NOT problems — no action required unless he wants it)

1. `magna-ut-1.webp` reads as a generic leafy suburb (lush trees/lawn,
   no Utah cues) — weakest place-fit of the 3 Magna images; not wrong,
   just generic.
2. `hardwood-floor-cabinet-drying-2.webp` shows a dry kitchen (no water or
   drying visible) — it is the room being dried, so acceptable.
3. Hero eyebrow is 14px @≤360px (18px above that) — known, load-bearing
   for Button 2, accepted in the design round.
4. Button 2 headroom @320 is 14px on the condo page (554px vs 568px
   fold). Holds, but any future change adding ~14px above the buttons at
   ≤360px on that page would break it.
5. Footer Google Maps embed: 0 failed requests / 0 console errors this
   run (no Maps request observed) — still needs a real-network eyeball
   after push (known VM limit).
6. Repair hero: trowel hand slightly cut at the bottom edge (worker's own
   noted nit).
7. `water-heater-2`: worker's face partially cut at the top edge —
   framing nit only.

## Per-page table (fresh export; btn2 = Button 2 bottom px at scroll-0)

| route | FULL | H1 | FAQ | tbl | links b+c | btn2@320 | btn2@390 | imgs |
|---|---|---|---|---|---|---|---|---|
| / | FULL | 1 | 6/6 | 1 | 1+19 | 443 | 535 | 20 |
| /about | FULL | 1 | 5/5 | 1 | 16+0 | 455 | 651 | 1 |
| /contact | FULL | 1 | 5/5 | 2 | 1+0 | 455 | 621 | 1 |
| /emergency-water-extraction | FULL | 1 | 6/6 | 2 | 7+0 | 479 | 651 | 4 |
| /basement-flooding-cleanup | FULL | 1 | 5/5 | 1 | 5+0 | 517 | 694 | 4 |
| /window-well-flooding | FULL | 1 | 5/5 | 1 | 2+0 | 479 | 651 | 4 |
| /burst-pipe-water-damage | FULL | 1 | 5/5 | 2 | 5+0 | 517 | 694 | 4 |
| /sewage-backup-cleanup | FULL | 1 | 5/5 | 2 | 3+0 | 479 | 651 | 4 |
| /water-heater-leak-cleanup | FULL | 1 | 5/5 | 1 | 7+0 | 517 | 694 | 4 |
| /swamp-cooler-leak-water-damage | FULL | 1 | 5/5 | 3 | 2+0 | 517 | 694 | 4 |
| /ceiling-water-damage | FULL | 1 | 5/5 | 1 | 6+0 | 479 | 694 | 4 |
| /crawl-space-water-damage | FULL | 1 | 5/5 | 1 | 3+0 | 517 | 694 | 4 |
| /hardwood-floor-cabinet-drying | FULL | 1 | 5/5 | 2 | 4+0 | 479 | 694 | 4 |
| /condo-apartment-water-damage | FULL | 1 | 5/5 | 2 | 4+0 | 554 | 767 | 4 |
| /commercial-water-damage | FULL | 1 | 5/5 | 1 | 4+0 | 479 | 694 | 4 |
| /storm-flood-damage | FULL | 1 | 5/5 | 2 | 5+0 | 517 | 694 | 4 |
| /mold-remediation | FULL | 1 | 5/5 | 1 | 7+0 | 442 | 651 | 4 |
| /water-leak-detection | FULL | 1 | 5/5 | 1 | 6+0 | 517 | 736 | 4 |
| /water-damage-repair | FULL | 1 | 5/5 | 2 | 6+0 | 479 | 694 | 4 |
| /locations/cottonwood-heights-ut | FULL | 1 | 5/5 | 1 | 8+0 | 517 | 694 | 4 |
| /locations/south-salt-lake-ut | FULL | 1 | 5/5 | 2 | 13+0 | 517 | 736 | 4 |
| /locations/magna-ut | FULL | 1 | 5/5 | 2 | 9+0 | 479 | 694 | 4 |
| /midvale-water-sewer-emergency-contacts | FULL | 1 | 5/5 | 1 | 3+0 | 442 | 651 | 1 |
| /privacy-policy | FULL | 1 | 0/0 | 0 | 0+0 | 367 | 499 | 1 |
| /terms-of-use | FULL | 1 | 0/0 | 0 | 0+0 | 367 | 499 | 1 |
| /disclaimer | FULL | 1 | 0/0 | 0 | 0+0 | 367 | 499 | 1 |
| /resources/frozen-pipes-midvale | FULL | 1 | 5/5 | 1 | 3+0 | 530 | 663 | 1 |
| /resources/winterize-swamp-cooler-utah | FULL | 1 | 5/5 | 1 | 3+0 | 479 | 694 | 1 |
| /resources/upstairs-unit-leak-who-pays-utah | FULL | 1 | 5/5 | 1 | 2+0 | 517 | 736 | 1 |
| /resources/can-mold-grow-in-utah | FULL | 1 | 5/5 | 3 | 4+0 | 479 | 694 | 1 |
| /resources/basement-flooding-spring-snowmelt-utah | FULL | 1 | 5/5 | 2 | 4+0 | 517 | 767 | 1 |

## Deliverables

- Review pack regenerated: `~/workspace/your_files/midvale-design-review.pdf`
  (31 pp, 5.9 MB, desktop 1440 + mobile 390 per route, from the 62 fresh
  screenshots in `qa/uiux-render/` taken on THIS build).
- Raw JSONs: `qa/uiux-verify-static-2026-11-13.json`,
  `qa/uiux-faqld-2026-11-13.json`, `qa/uiux-verify-render-2026-11-13.json`,
  `qa/uiux-adjudicate-2026-11-13.json`, `qa/uiux-images-all-2026-11-13.json`.

## Readiness

**PROBLEMS 0 — READY FOR RE-PUSH.** The Stage 1 fixes hold on a fresh
export under independent re-measurement. No push/deploy/token/DNS touched
by this verifier. Still open (his call / later): OBS-1/OBS-2 polish,
OBS-4 thin Button 2 headroom on the condo page, OBS-5 Maps embed
real-network eyeball after push.
