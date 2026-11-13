# Cycle 1 Optimization — Body Images Audit (Midvale UT)

**Scope:** all 57 body images — `public/images/body/*.webp`, 19 routes × 3, manifest `lib/body-images.json`.
**Date:** 2026-11-13. **Method:** served fresh `out/` via `qa/linkfix-serve.py` copy on port 8341 under `/midvale-water-damage/`; Playwright/Chromium real render at 1440 and 390; every one of the 57 files viewed full-size; dims/KB via PIL; EXIF/XMP/IPTC via PIL + `exiftool` batch. **Audit only — no site file or image was modified.**

## Verdict

**PROBLEMS: 4 total — P1 0, P2 1 (systemic, 57 files), P3 3 (6 files).**
Relevance is otherwise clean: **56/57 alt-exact, 1 alt-loose, 0 alt-mismatch, 0 wrong-topic / wrong-place / wrong-country.** Metadata is clean: **EXIF 0, XMP 0, IPTC 0, ICC 0 on all 57 files** (exiftool batch confirms). All 57 files exist in `out/images/body/` and return HTTP 200 from the local server.

## P2 — Systemic: all 57 files oversized for their slot (no srcset)

- Every body `<img class="body-img">` renders **400×225 @1440** and **342×192 @390** (figure is the same size; uniform across all 19 routes).
- Every file is **1200×675** — **3.00× the 1440 slot width, 3.51× the 390 slot width**. Even against a 2×-DPR ideal (800×450) it is still 1.50×.
- **No `srcset` anywhere** on the body pages (`grep -c srcset` = 0), so a 390px phone downloads the same full 1200px file as desktop.
- **Fix (for Stage 2):** resize to the slot — 800×450 covers 2× DPR at the 400px slot (or serve 400w/800w srcset); recompress to medium. Expected saving is large: the set is 6,015.4 KB for what is, on screen, 57 × 400×225 images.
- Note on measurement: `naturalWidth=0` on some below-fold images at measure time is `loading="lazy"`, not breakage — all 57 verified HTTP 200 + present in `out/`.

## P3 — Relevance / quality (minor)

### P3-1 — `body/mold-remediation-2.webp` — very washed-out (KNOWN Stage 5 P3, re-confirmed fresh)
Worker in white PPE suit, respirator and blue gloves with a fogging hose — alt-exact, on-topic. The frame is heavily hazed white. The haze is partly the fogging treatment itself and the subject stays legible, so this stays **P3 cosmetic, not escalated**. Per the task brief I only re-flag if I find a genuinely better candidate — I did not find one; no replacement proposed.

### P3-2 — Generic location imagery, not verifiably the named place (4 files, alt-accurate)
- `body/basement-flooding-cleanup-3.webp` (171.9 KB) — aerial leafy suburb; could be anywhere, not verifiably Midvale.
- `body/sewage-backup-cleanup-3.webp` (177.6 KB) — aerial autumn suburb + cul-de-sac; same.
- `body/magna-ut-1.webp` (275.7 KB) — ranch home + porch matches its alt, but lush green, crepe-myrtle, SE-US look; not verifiably Magna UT / Utah foothills.
- `body/cottonwood-heights-ut-3.webp` (110.6 KB) — snowy SLC valley + mountains is plausible, but the alt says "snowy city street" while the image is a rooftop/cityscape view with no street clearly visible (alt-loose, the only one of 57).

### P3-3 — `body/water-damage-repair-1.webp` (17.0 KB) — near-white-on-white
Gloved hand smoothing joint compound with a taping knife matches the alt, but white compound on a white wall makes the subject barely visible at the 400px slot.

## Totals

| Metric | Value |
|---|---|
| Files audited | 57 (19 routes × 3) |
| Total weight | **6,015.4 KB** (avg 105.5 KB/file; avg **316.6 KB/page** of body images alone) |
| Files >150 KB | 15 · >100 KB: 28 · <50 KB: 9 |
| Largest files | magna-ut-1 275.7 · storm-flood-damage-1 180.7 · window-well-flooding-3 178.2 · sewage-backup-cleanup-3 177.6 · mold-remediation-3 175.1 KB |
| Heaviest page | /locations/magna-ut — 589.8 KB (3 images) |
| Lightest page | /ceiling-water-damage — 88.1 KB |
| File dimensions | 1200×675 on all 57 |
| Rendered slot | 400×225 @1440 · 342×192 @390 (all 57) |
| Alt verdicts | exact 56 · loose 1 (cottonwood-heights-ut-3) · mismatch 0 |
| Relevance | pass 51 · P3 6 · wrong-topic/wrong-place/wrong-country 0 |
| Metadata | EXIF 0 · XMP 0 · IPTC 0 · ICC 0 (all 57) |
| Served | 57/57 HTTP 200, present in out/images/body/ |

## Per-page body-image weight (KB)

| Route | KB | Route | KB |
|---|---|---|---|
| /locations/magna-ut | 589.8 | /water-heater-leak-cleanup | 315.2 |
| /swamp-cooler-leak-water-damage | 417.2 | /crawl-space-water-damage | 311.3 |
| /storm-flood-damage | 407.7 | /water-leak-detection | 301.5 |
| /window-well-flooding | 389.6 | /sewage-backup-cleanup | 289.2 |
| /burst-pipe-water-damage | 365.1 | /hardwood-floor-cabinet-drying | 283.2 |
| /basement-flooding-cleanup | 364.8 | /emergency-water-extraction | 257.7 |
| /mold-remediation | 356.8 | /locations/south-salt-lake-ut | 256.6 |
| /locations/cottonwood-heights-ut | 350.6 | /condo-apartment-water-damage | 216.0 |
| /commercial-water-damage | 333.6 | /water-damage-repair | 121.4 |
| | | /ceiling-water-damage | 88.1 |

## Per-file table

Full per-file record (dims, KB, slot 1440/390, oversized?, relevance, alt verdict, EXIF): `qa/opt1-images-body.json`.

Relevance notes (all other 51 files: viewed full-size, image matches alt + page service/area — PASS):
- basement-1/2: flooded basement + extraction crew, air movers — exact. burst-1: frozen split copper pipe, icicles — exact. burst-2: peeling water-damaged paint — exact. burst-3: wrench on burst copper fitting, brass valve — exact.
- ceiling-1/2/3: sanding green drywall ceiling / trowel at ceiling corner / renovation room with stepladder + curved ceiling — exact.
- commercial-1/2/3: glass office towers / open-plan office / wet office floor with air movers + dehumidifier — exact.
- condo-1/2/3: white-brick apartment + balconies / worker in hard hat + hi-vis with wrench / grey drain pipes on exterior wall — exact.
- crawl-1/2/3: joists + damp dirt + puddle by flashlight / white pipes dripping + pooling / worker unrolling vapor barrier — exact.
- emergency-1/2/3: truck-mounted extraction + hoses / yellow wet-dry vac / carpet extraction under lifted carpet — exact.
- hardwood-1/2/3: worn planks + peeling finish / bright kitchen, white cabinets + dark wood floor / sunlit herringbone parquet — exact.
- cottonwood-1/2: snow-covered Wasatch above SLC valley / aerial SLC + snow mountains — exact.
- magna-2/3: older main street, pickups, dry foothills + mountains / white clapboard house + new wood-frame addition — exact.
- mold-1/3: green-black mold on white block wall / black mildew streaks down light wall — exact.
- sewage-1/2: PPE worker + pump sprayer in kitchen / floor drain + mop/bucket + water heater — exact.
- south-salt-lake-1/2/3: apartment building + balconies / moisture-meter check of stained wall with air movers / technician extracting flooded bathroom floor — exact.
- storm-1/2/3: flooded suburban street / rain off corrugated roof edge / cars in flooded road — exact.
- swamp-1/2/3: mildew streaks on white wall / ranch house + roof evaporative cooler + foothills / side-mount cooler dripping on stucco wall — exact.
- repair-2/3: laminate plank fitting + mallet / renovated room, stepladder, floor protection, shop vac — exact.
- heater-1/2/3: tank heater + copper pipes + washer/dryer + puddle / man shutting valve with mop in flooded basement / wall-mounted tankless heater, blue-brick walls — exact.
- leak-1/2/3: pressure gauge on red pipe, psi/kPa / fallen plaster on blue wall / technician repairing orange pump housing on workbench — exact.
- window-1/2/3: rainy street + American flag through window / downspout dripping on stone foundation / corrugated window well full of rainwater — exact.

## Method notes / honest limits

- First Playwright run returned 0 images because the serve script 404s on trailing-slash route URLs (flat `.html` files); re-ran with no-trailing-slash URLs and got 3/3 on all 19 routes at both viewports. This was my measurement error, caught and corrected — slot numbers above are from the corrected run.
- "Not verifiably the place" (P3-2) is a judgement call on generic stock, not proof of a wrong place: none of the four shows a recognisably wrong city/country, and all four alts are accurate. Only the alt-loose wording on cottonwood-3 is a concrete text-vs-image gap.
- Location identity (e.g. whether the Wasatch/SLC aerials are truly Salt Lake) cannot be proven from pixels alone; verdicts rest on visual plausibility + alt accuracy.
