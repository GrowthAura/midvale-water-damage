# Cycle 1 — Images Audit: Heroes + Cards — Midvale UT

- **Date:** 2026-11-13 (Batch 2 optimization, Cycle 1)
- **Scope:** all 50 hero + card images — `public/images/heroes/*.webp` (31) + `public/images/cards/*.webp` (19)
- **Audit only.** No site source file or image was modified.
- **Method:** PIL pixel dims + file size; `exiftool -json -G` metadata on all 50 files; Playwright Chromium real render of the fresh `out/` export served locally at `http://127.0.0.1:8391/midvale-water-damage/` (copy of `qa/linkfix-serve.py`, port 8391 — port 8347 was already in use by another worker); hero `<img>` box measured on each of the 31 hero pages + card `<img>` boxes on the homepage, at 1440 and 390 viewport widths; **every image viewed full-size** and judged against its page's area/place/service + its alt text (alt taken from `out/*.html`); all 50 images used exactly once, 0 unused, 0 missing.
- **Per-file table:** `qa/opt1-images-heroes-cards.json`

## Verdict

**NOT READY — 29 PROBLEMS (P1 3 / P2 20 / P3 6).**

Relevance is otherwise strong: 47/50 images pass relevance, 47/50 alts are exact. The failures are concentrated and specific: 3 hero photos are wrong for their alt/page, and all 19 cards are far larger than their display slots.

## Totals

| | Count | Size |
|---|---|---|
| Heroes (31) | 31 × 1600×1066 | 3,509.6 KB |
| Cards (19) | 16 × 1200×675, 3 × 1200×800 | 1,454.5 KB |
| **All 50** | | **4,964.1 KB** |

- **Largest files:** `heroes/basement-flooding-spring-snowmelt-utah.webp` 210.2 KB · `heroes/cottonwood-heights-ut.webp` 182.1 KB · `cards/cottonwood-heights-ut.webp` 170.2 KB · `heroes/magna-ut.webp` 159.5 KB · `heroes/frozen-pipes-midvale.webp` 155.1 KB · `heroes/can-mold-grow-in-utah.webp` 145.2 KB · `heroes/about.webp` 138.4 KB · `heroes/swamp-cooler-leak-water-damage.webp` 136.8 KB · `heroes/basement-flooding-cleanup.webp` 136.4 KB · `heroes/burst-pipe-water-damage.webp` 133.3 KB
- **Metadata:** EXIF / XMP / IPTC / ICC = **0 tags on all 50 files** (verified via `exiftool -json -G`; only File/RIFF/Composite structural tags present). PASS.
- **Loading:** all 50 images return 200 and render. The `loaded: false` readings for below-fold lazy cards at first paint are expected `loading="lazy"` behaviour, not broken images — after a full scroll, all 20 homepage images load at both 1440 and 390 (verified separately).
- **No `srcset` on any of the 50 `<img>` tags** — one file serves every viewport (see P3-5).

## P1 — Wrong-topic / wrong-alt photos (3)

### P1-1 — `heroes/disclaimer.webp` — /disclaimer
- 1600×1066, 33.5 KB. Slot 1440×414 / 390×489.
- **What it shows:** a blurry stock office photo — white laptop, calculator, card payment terminal on a desk.
- **Alt claims:** "Technician inspecting a water-damaged wall with a moisture meter in a dark room" — no technician, no wall, no moisture meter, nothing water-related in the frame.
- **Why P1:** the only image in the set that is not water-damage related at all; alt text is factually false. Needs a replacement photo (or an honest alt if the photo stays — but the photo is off-topic for this site).

### P1-2 — `heroes/upstairs-unit-leak-who-pays-utah.webp` — /resources/upstairs-unit-leak-who-pays-utah
- 1600×1066, 85.5 KB. Slot 1440×566 / 390×1016.
- **What it shows:** a bright daylight bathroom with water on the floor and towels (tub/toilet-overflow look). A real stock photo — breaks the dark generated-series style of the rest of the site.
- **Alt claims:** "Water dripping from an apartment ceiling into the unit below in Midvale" — there is **no ceiling drip, no upstairs source, no ceiling** in the frame.
- **Why P1:** does not illustrate the page subject at all (ceiling leak from the upstairs unit — compare `heroes/condo-apartment-water-damage.webp`, which shows exactly that). Needs a replacement photo showing water coming through a ceiling.

### P1-3 — `heroes/water-damage-repair.webp` — /water-damage-repair
- 1600×1066, 97.1 KB. Slot 1440×661 / 390×1133.
- **What it shows:** a close-up portrait of a worker in a hard hat + respirator holding a piece of trim. A real stock photo — breaks the dark generated-series style.
- **Alt claims:** "Newly rebuilt room in a Midvale home, fresh drywall and trim" — no rebuilt room is visible.
- **Why P1:** alt describes content that is not in the photo. Needs a replacement photo of a finished/rebuilt room (or an alt rewrite to describe the worker — but the alt as written is false).
- **Note:** the CARD for this same page (`cards/water-damage-repair.webp`, fresh drywall + new white trim being finished) matches its own alt exactly — only the hero mismatches.

## P2 — Oversized / heavy for the slot (20)

### P2-1..19 — ALL 19 card images are 3.5–4.9× wider than their display slot
- **Files:** 1200 px wide (16 × 1200×675, 3 × 1200×800). **Measured slots:** service cards 245×138 @1440 and 340×191 @390; location cards (Cottonwood Heights, Magna, South Salt Lake) 337×189 @1440 and 340×191 @390.
- **Ratios:** 1200/245 = **4.9×** @1440 (service cards); 1200/337 = 3.6× @1440 (location cards); 1200/340 = **3.5×** @390 (all cards).
- **Weight:** cards total 1,454.5 KB on the homepage. Heaviest for their tiny slots: `cards/cottonwood-heights-ut.webp` 170.2 KB, `cards/burst-pipe-water-damage.webp` 123.8 KB, `cards/window-well-flooding.webp` 119.5 KB, `cards/magna-ut.webp` 117.0 KB, `cards/storm-flood-damage.webp` 101.1 KB. (No card exceeds the 200 KB absolute threshold, but every card is oversized against its 245–340 px slot.)
- **Fix direction (for the fixer, not done here):** resize cards to ~680 px wide (2× the largest slot, 340 px @390) — a single file serves both widths; ~490 px would cover the 245 px desktop slot alone. Expect the 19-card homepage payload to drop from ~1,455 KB to roughly ~400–600 KB.
- **Full list:** `cards/basement-flooding-cleanup, burst-pipe-water-damage, ceiling-water-damage, commercial-water-damage, condo-apartment-water-damage, cottonwood-heights-ut, crawl-space-water-damage, emergency-water-extraction, hardwood-floor-cabinet-drying, magna-ut, mold-remediation, sewage-backup-cleanup, south-salt-lake-ut, storm-flood-damage, swamp-cooler-leak-water-damage, water-damage-repair, water-heater-leak-cleanup, water-leak-detection, window-well-flooding` (all `.webp`).

### P2-20 — Mobile hero crop: at 390 px only ~24% of each hero's width is visible
- **Measured:** hero `<img>` is `position: absolute; inset: 0; width/height: 100%; object-fit: cover` inside a content-height hero section. At 1440 the box is 1440×414–748 (height varies by page content); at 390 the box is 390×489–1239 (e.g. `/basement-flooding-cleanup` 390×1198, `/condo-apartment-water-damage` 390×1239).
- **Math:** at 390×1198 the 1600×1066 file scales to ~1798×1198 and is cropped to the centre 390 px — about **76% of the image width is cropped away** on mobile (object-position `center 35%`).
- **Impact:** heroes whose subject spans the frame lose their sides on phones — worst affected are the wide scenes `heroes/about.webp`, `heroes/home.webp`, `heroes/magna-ut.webp`, `heroes/cottonwood-heights-ut.webp`, `heroes/south-salt-lake-ut.webp` (crew/truck/street subjects at the edges). Centre-weighted heroes (burst pipe, frozen pipe, mold) survive the crop. This is a CSS/layout issue, not a wrong photo — recorded here because it changes what the hero photo actually shows on mobile. Fix direction: cap the mobile hero height or use a mobile-cropped variant; do not just swap photos.
- **Heroes are NOT oversized:** 1600 px file vs 1440 px slot = 1.11× @1440, and every hero is under the 300 KB threshold (max 210.2 KB). No P2 for heroes on size/weight.

## P3 — Minor (6)

### P3-1 — `cards/burst-pipe-water-damage.webp` — alt wording imprecise
- Photo shows a burst copper pipe spraying inside an **opened wall cavity** (studs, torn drywall). Alt says "Burst frozen pipe joint with ice and water spraying in a **dark crawl space**" — it is not a crawl space, and no ice is visible. Topic is right; the alt's setting/detail is wrong. Fix: rewrite alt to describe the wall cavity, or swap the photo for a crawl-space burst pipe.

### P3-2 — 3 cards are 1200×800 (3:2) displayed in a 16:9 slot (vertical crop)
- `cards/swamp-cooler-leak-water-damage.webp` (79.3 KB), `cards/water-heater-leak-cleanup.webp` (48.5 KB), `cards/water-leak-detection.webp` (42.2 KB). `.card-img` is `aspect-ratio: 16/9; object-fit: cover`, so top/bottom is cropped. Subjects are centred so nothing essential is lost — cosmetic only. Fix: re-crop to 16:9 at resize time.

### P3-3 — Hero `width`/`height` attributes mismatch the file (all 31 heroes, one markup line)
- `components/site.tsx:63` emits `width={1600} height={900}` (16:9) but every hero file is 1600×1066 (3:2). CSS (`position: absolute; inset: 0; width/height: 100%`) overrides the box in practice, so no visible layout shift was measured — but the reserved aspect ratio is factually wrong. Fix: `height={1066}`.

### P3-4 — No `srcset` on any of the 50 images
- One file serves 390–1440 px. Mobile (390 px slot) downloads the same 1600 px heroes (~4.1× oversampling) and 1200 px cards. A 800 px hero variant + the resized cards would cut mobile bytes substantially. (Counts once here, not per file.)

### P3-5 — `heroes/crawl-space-water-damage.webp` reads taller than a typical crawl space
- The photo is a dark under-house dirt space with joists and matches its alt; it just reads more like a low basement than a tight crawl space. No action needed — recorded so the pass is honest.

### P3-6 — Style break on the 3 stock-photo heroes
- `heroes/disclaimer.webp`, `heroes/upstairs-unit-leak-who-pays-utah.webp`, `heroes/water-damage-repair.webp` are bright real stock photos; the other 28 heroes are a consistent dark generated series. The two P1 replacements (P1-2, P1-3) should match the dark series style. (The disclaimer photo is P1-1 on content, not just style.)

**P3 count:** P3-1 burst-pipe alt (1) + P3-2 three 3:2 cards (1) + P3-3 hero attr mismatch (1) + P3-4 no srcset (1) + P3-5 crawl-space tall-read, no action (1) + P3-6 style break (1) = 6.

## What passed (for the record)

- **Relevance 47/50:** every service/location/resource hero and every card except the 3 P1s matches its page and alt on viewed pixels. No wrong-country / wrong-place photo found. The 3 location heroes/cards are Utah-plausible: Cottonwood Heights (snowy Wasatch canyon + bench homes; card is a real autumn canyon-highway photo, plausibly Big Cottonwood Canyon), Magna (historic brick Main Street), South Salt Lake (apartments + warehouses). `cards/south-salt-lake-ut.webp` and `cards/magna-ut.webp` are crops of their own page heroes — same page, same subject, fine.
- **Alts 47/50 exact:** only the 3 P1 heroes have false alts, plus the 1 P3 imprecise card alt.
- **Metadata 50/50 clean:** 0 EXIF/XMP/ICC tags.
- **No oversized heroes:** 1.11× width @1440, all < 300 KB.
- **No broken images:** all 50 return 200 and render at both widths.

## Method notes / caveats (owned plainly)

- Port 8347 was already bound by another worker's instance of the same serve script, so this audit served on port **8391** (same script, same `out/`). No re-export was run.
- The first `exiftool` loop (100 separate invocations) was slow (~3 min) — replaced by a single `exiftool -json -G` pass over all 50 files; the 0-tag verdict comes from the parsed JSON, not the slow loop.
- Card `loaded: false` at first paint for below-fold cards is lazy loading, verified by a full-scroll re-check (all 20 homepage images loaded at 1440 and 390).
- Hero slot heights vary by page (414–748 @1440) because the hero section height is content-driven; the numbers in the JSON are the measured `<img>` boxes per page, not a single assumed size.
