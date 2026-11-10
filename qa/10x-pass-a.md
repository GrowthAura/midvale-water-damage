# FINDINGS — PASS A: VISUAL / UI / UX — Midvale UT (10x testing)
Date: 2026-11-10 ~21:30 PKT. Tester: PASS A (independent, fresh from the live local export).
Method: served `out/` on 127.0.0.1:8331 (own mapping server, extensionless routes);
Python Playwright + headless Chromium. Scrolled each page before capture so lazy
images loaded; waited for `naturalWidth > 0`. NO site code/content/CSS/images edited.

## VERDICT — PASS A — PROBLEMS: 1

One real, reproduced defect (P1 below): at **320px** first paint the sticky mobile
call bar covers hero Button 2 on 15 of 21 pages. Everything else checked passes,
including the 390px first-paint bar rule, which is clean on 21/21.

## COUNTS (all measured fresh, this run)

| What | Count |
|---|---|
| Pages | 21/21 (status 200) |
| Screenshots taken | 84 (21 desktop-1440 full + 21 mobile-390 top + 21 mobile-390 full + 21 mobile-320 top) |
| Screenshots viewed by pixels | 84/84 (home mobile-390 full read as 3 segments; +2 zoom crops: home hero, home footer) |
| Sections checked | homepage 14 sections (hero, causes, 16 service cards, neighborhoods, why, process 1–6, category table, cost, insurance, 30-min, areas, FAQ 6, final CTA, footer) + every service/location/guide page (hero, H2 body, buttons, footer) |
| Overflow (scrollWidth − clientWidth) | 0 on 21/21 at 1440, 390 AND 320 |
| Body font (computed) | 18px on 21/21 |
| H1 | exactly 1/page, visible, white, on 21/21 |
| Hero order (breadcrumb → eyebrow → H1 → intro → 2 buttons → trust chips) | 21/21 |
| Hero buttons equal | 322×56px desktop, 342×56px mobile, on 21/21 |
| Hero images loaded | 21/21, natural 1600×1066, rendered 1440×504–633 |
| All images loaded | 40/40 (21 heroes + 19 cards), 0 unloaded |
| Image repeats (md5) | 0 across the site; max file 186KB (cottonwood hero); total 3.8MB |
| Homepage card images (desktop) | 19 cards, all 337×189 rendered = 16:9, height measured, not width-only |
| H2 vs H3 colour | distinct: H2 rgb(14,59,56) pine, H3 rgb(21,82,76) pine-2, on all pages that have them |
| Sticky bar vs hero buttons, 390px first paint | NO overlap on 21/21 (worst button bottom 694px < bar top 781px, viewport 844) |
| Tap targets (hero buttons) | 56px tall, ≥44px, on 21/21 at desktop + mobile |
| CLS | NOT measured by this pass (no claim made) |

## PROBLEM

### P1 — Sticky call bar covers hero Button 2 at 320px first paint (15/21 pages)
- **Reproduction:** viewport 320×700, load page, do NOT scroll. The fixed
  `.sticky-bar` (top 637px, height 63px) sits on top of the hero buttons.
- **Evidence (measurements + pixels):**
  - Worst tier — Button 2 FULLY hidden, Button 1 only a ~19px orange sliver visible
    (Button 2 bottom 746px vs bar top 637px = 109px hidden): `swamp-cooler-leak-water-damage-mobile320-top.png`,
    `hardwood-floor-cabinet-drying-mobile320-top.png`, `condo-apartment-water-damage-mobile320-top.png`,
    `midvale-water-sewer-emergency-contacts-mobile320-top.png`, `cottonwood-heights-ut-mobile320-top.png`,
    `south-salt-lake-ut-mobile320-top.png` (6 pages).
  - Button 2 fully hidden, Button 1 fully visible (66–78px hidden):
    `emergency-water-extraction-mobile320-top.png`, `basement-flooding-cleanup-mobile320-top.png`,
    `magna-ut-mobile320-top.png` (3 pages; Button 2 bottom 703–715px).
  - Button 2 partly covered — only a "Request Emergency" sliver shows (36px hidden,
    Button 2 bottom 673px): `home-mobile320-top.png`, `burst-pipe-water-damage-mobile320-top.png`,
    `sewage-backup-cleanup-mobile320-top.png`, `water-heater-leak-cleanup-mobile320-top.png`,
    `crawl-space-water-damage-mobile320-top.png`, `commercial-water-damage-mobile320-top.png` (6 pages).
  - Clean at 320 (6 pages): window-well, ceiling, storm, mold, leak-detection,
    water-damage-repair — Button 2 bottom ≤636px. Note window-well/ceiling pass by
    1px only, so the margin is razor-thin even where it passes.
- **Why it is real:** seen in the actual first-paint pixels on all 15 screenshots
  (not inferred from numbers); a 320px-wide phone user cannot see or tap Button 2
  without scrolling, and on the 6 worst pages cannot see Button 1 properly either.
  The 700px test height is generous — real 320px phones (viewport ~568px tall)
  would be worse. Same defect class as Chesterfield D1, which was at 390px; here
  390px is clean and the failure moved to 320px because the hero stacks taller there.
- **Scope note:** the task's bar rule names 390px, where this site PASSES 21/21.
  P1 is filed under "any other visual defect you genuinely see" — it is genuine,
  reproduced, and user-facing on small phones.

## PER-PAGE TABLE

| Page | Widths viewed | Verdict | Issues |
|---|---|---|---|
| home (/) | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 sliver, 36px hidden). Otherwise clean. |
| emergency-water-extraction | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 fully hidden, 78px). Otherwise clean. |
| basement-flooding-cleanup | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 fully hidden, 78px). Otherwise clean. |
| window-well-flooding | 1440 full, 390 top+full, 320 top | PASS | None. Hero photo (snowy window well) reads at mobile crop. |
| burst-pipe-water-damage | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 sliver, 36px). Otherwise clean. |
| sewage-backup-cleanup | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 sliver, 36px). Otherwise clean. |
| water-heater-leak-cleanup | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 sliver, 36px). Otherwise clean. |
| swamp-cooler-leak-water-damage | 1440 full, 390 top+full, 320 top | ISSUE | P1 worst tier (320: Button 2 fully hidden + Button 1 sliver, 109px). |
| ceiling-water-damage | 1440 full, 390 top+full, 320 top | PASS | None (320 passes by 1px). |
| crawl-space-water-damage | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 sliver, 36px). Otherwise clean. |
| hardwood-floor-cabinet-drying | 1440 full, 390 top+full, 320 top | ISSUE | P1 worst tier (320: Button 2 fully hidden + Button 1 sliver, 109px). |
| condo-apartment-water-damage | 1440 full, 390 top+full, 320 top | ISSUE | P1 worst tier (320: Button 2 fully hidden + Button 1 sliver, 109px). |
| commercial-water-damage | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 sliver, 36px). Otherwise clean. |
| storm-flood-damage | 1440 full, 390 top+full, 320 top | PASS | None. |
| mold-remediation | 1440 full, 390 top+full, 320 top | PASS | None. |
| water-leak-detection | 1440 full, 390 top+full, 320 top | PASS | None. |
| water-damage-repair | 1440 full, 390 top+full, 320 top | PASS | None. |
| midvale-water-sewer-emergency-contacts | 1440 full, 390 top+full, 320 top | ISSUE | P1 worst tier (320: Button 2 fully hidden + Button 1 sliver, 109px). |
| locations/cottonwood-heights-ut | 1440 full, 390 top+full, 320 top | ISSUE | P1 worst tier (320: Button 2 fully hidden + Button 1 sliver, 109px). |
| locations/south-salt-lake-ut | 1440 full, 390 top+full, 320 top | ISSUE | P1 worst tier (320: Button 2 fully hidden + Button 1 sliver, 109px). |
| locations/magna-ut | 1440 full, 390 top+full, 320 top | ISSUE | P1 (320: Button 2 fully hidden, 66px). Otherwise clean. |

## WHAT PASSED (verified, not trusted from the last round)

- **Heroes:** every hero photo reads as a real scene at desktop zoom and mobile:
  home = extraction crew + truck hoses at dusk; emergency = hi-vis crew + hoses;
  basement = worker + pump; window-well = snowy well; burst-pipe = spraying pipe in
  wall cavity; sewage = PPE/hazmat crew; water-heater = tank + pipes; swamp-cooler =
  rooftop unit on wet shingles; ceiling = stained ceiling + icicles; crawl-space =
  worker + headlamp; hardwood = drying mats on wood floor; condo = moisture meter in
  wet hallway; commercial = restaurant + air mover/dehumidifier; storm = flooded
  street at dusk; mold = PPE worker in containment; leak-detection = thermal camera
  (orange/blue heat pattern, no legible text); repair = rebuilt room interior;
  contacts = utility truck at night; Cottonwood = snowy bench homes below canyons;
  South Salt Lake = apartments + warehouses, wet street; Magna = older Main Street
  at dusk. Topic fit and place fit good on all 21. All heroes are dark by design;
  the homepage hero's left ~60% is near-black gradient, but the photo is genuinely
  legible on the right half — NOT dead black, not flagged as a defect.
- **Homepage sections (desktop + mobile):** causes, 16 service cards (1-col stack on
  mobile, all images 16:9, no repeats), neighborhood cards, why-bullets, process
  steps 1–6, category table, cost list, insurance, 30-min list, 3 area cards,
  FAQ 6/6, final CTA (buttons stacked + equal on mobile), footer 4-col → 1-col.
  Spacing balanced, no cramped/flat/ugly section, no text overflow, no orphan text.
- **Service/location/guide pages:** thin by design (hero + H2 + link + buttons) —
  known, not a defect. H2 pine + copper bar reads clearly against H3 pine-2.
- **Header/footer:** clean at all widths; header wraps to brand + call button at
  320 with no overflow; footer links all visible, no clipping.
- **390px first paint:** both hero buttons fully visible above the sticky bar on
  21/21 (measured + seen in pixels).

## NOTES — checked, NOT defects (do not re-flag)

1. **Footer map blank in sandbox (KNOWN caveat, noted once):** the Google Maps
   iframe renders blank here because google.com is unreachable in this sandbox.
   Markup verified correct: `<iframe title="Map: Midvale, UT 84047"
   src="https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed">`
   in the footer of home + all service/guide pages. Area pages have no map by
   design. The blank iframe leaves a large empty dark-green gap above the footer
   columns in sandbox screenshots — that gap is the map box, not a layout bug.
2. **Category table at 390px** shows its 3rd column cut off until swiped — verified
   the table sits in `.table-wrap` with `overflow-x: auto` (scrollW 377 > clientW
   342), so the column is reachable by horizontal swipe; document overflow is 0.
   Standard responsive-table behaviour, not a defect.
3. **Sticky bar appearing mid-page in full-page screenshots** (e.g. across the
   hero intro in `home-mobile390-full.png`) is a capture artifact of fixed
   elements in full-page shots. The true first-paint tops are the valid evidence
   for the bar, and they are clean at 390px.
4. **Contacts page note box** ("the full emergency-contact list ... is not in the
   source document yet") is an honest pending-content placeholder, renders cleanly
   at desktop + mobile. Content gap, not a visual defect.
5. **Breadcrumb wraps to 2 lines** at 390/320 on long page names (e.g. swamp-cooler,
   hardwood, contacts, location pages). Normal wrap, reads fine, no overflow.

## SCRIPT ERRORS (mine, NOT site defects)

1. First run died on the home mobile full-page screenshot: Playwright capture
   limit at `device_scale_factor=2`. Fixed to 1x, re-ran from scratch — 84/84
   screenshots produced.
2. A `pkill -f server.py` once matched my own shell (exit 15); the test server
   was then stopped cleanly by PID. No site impact.

## FILES

- Findings: `~/workspace/midvale-water-damage/qa/10x-pass-a.md` (this file)
- Screenshots (84): `~/workspace/midvale-water-damage/qa/10x/pass-a/<slug>-{desktop1440-full,mobile390-top,mobile390-full,mobile320-top}.png`
  (home mobile full also split as `home-mobile390-full-seg1/2/3.png` because the
  single file exceeded the image-reader size limit)
- Measurements: `~/workspace/midvale-water-damage/qa/10x/pass-a/measurements.json`
- Runner + server: `~/workspace/midvale-water-damage/qa/10x/pass-a/shot.py`, `server.py`
  (server on port 8331 stopped after the run; no site files touched)

## PASS A — PROBLEMS: 1
