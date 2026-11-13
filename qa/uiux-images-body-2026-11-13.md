# Midvale UT — Body Images Audit (Stage 1 UI/UX round)

- **Date:** 2026-11-13
- **Scope:** `public/images/body/` — all 57 WebP body images, 19 routes × 3
- **Method:** every file viewed at full size (1200×675) with the file-read tool; judged on topic fit for its exact section (`lib/body-images.json` `afterH2` checked against the page's H2 order in `lib/pages-data.json`), place/service fit, display quality, legible text/branding, and duplicates (md5 + 16×16 aHash + visual check).
- **Local only — audit only. No files edited.**

## Verdict counts

| Verdict | Count |
|---|---|
| PASS | 42 |
| WEAK | 12 |
| REPLACE | 3 |
| **Total** | **57** |

## Verification checks (all done this round)

- **Manifest vs disk: 57/57.** `lib/body-images.json` lists 57 entries across 19 routes; all 57 files exist on disk, 0 files on disk unlisted, 0 duplicates in the manifest, every `afterH2` index in range for its page.
- **Duplicates: 0.** No md5 duplicates; no aHash (16×16) pair at Hamming ≤ 6; no visual duplicates. One near-twin noted below (same room, different angle — different photos, not a reuse).
- **"AI" in filenames: none.** No filename contains the word "AI" (the substring match `water-damage-repair-*` is the word "repair", not "AI").
- **EXIF on the 7 generated files: 0.** `exiftool` on all 7 shows only container/file fields (dimensions, VP8 version, dates, permissions) — no EXIF, XMP, GPS, author, or software tags.
- **Dimensions: all 1200×675.** File sizes 17–199 KB.
- **G1 q50–70 files re-judged fresh at full size:** `basement-flooding-cleanup-2.webp` (22 KB), `emergency-water-extraction-2.webp` (42 KB), `sewage-backup-cleanup-1.webp` (45 KB) — no visible compression artifacts, blocking, or banding at 1200×675. Low-detail subjects compress small legitimately. All three PASS on pixels (basement-2 is WEAK for topic reasons only, not quality).

## The 7 generated images (Stage 0) — judged as images, not by origin

All 7 PASS. None looks AI-generated or off-topic at full size: anatomy, hands, equipment, hoses, water, and reflections are coherent; no warped objects, no extra/missing fingers, no legible text, no watermark.

| File | Verdict | Note |
|---|---|---|
| `emergency-water-extraction-1.webp` | PASS | Truck-mounted extraction unit, hoses into house, worker extracting flooded living-room floor. Topic-perfect for "First 60 Minutes on Site". |
| `emergency-water-extraction-3.webp` | PASS | Worker lifting damp carpet, extractor on wet pad. Topic-perfect for "Can Wet Carpet and Pad Be Saved?". Minor note only: the wand tip reads slightly as spraying rather than extracting — ambiguous at a glance, not a defect. |
| `crawl-space-water-damage-1.webp` | PASS | Joists, damp dirt, puddle, flashlight beam. Topic-perfect for "Signs Your Crawl Space Is Wet". |
| `crawl-space-water-damage-2.webp` | PASS | White pipes under joists, drip and pool on dirt. Topic-perfect for "What Floods Midvale Crawl Spaces". |
| `water-heater-leak-cleanup-2.webp` | PASS | Man shutting off a valve, mop in hand, water across a basement floor. Topic-perfect for "Water Heater Flooded Basement: The First 15 Minutes". Head is cropped at the top edge (framing choice, not an artifact). |
| `south-salt-lake-ut-3.webp` | PASS | Technician in gloves/rubber boots extracting a flooded apartment bathroom floor. Topic-perfect for "Sewage Backup Cleanup South Salt Lake". |
| `commercial-water-damage-3.webp` | PASS | Open office, wet floor, blue air movers + dehumidifier. Topic-perfect for "Commercial Drying for Large Open Spaces". **Correction of a prior note:** the design round recorded this file as B&W/grayscale (REPLACE P3-1). The file on disk today is in FULL COLOUR (vivid blue air movers, green plants) — that prior REPLACE reason does not apply as seen. |

## Per-image table

Section = the H2 the image sits after (`afterH2` index → H2 text from `pages-data.json`).

| # | File | Route / section (H2) | Verdict | Reason |
|---|---|---|---|---|
| 1 | `basement-flooding-cleanup-1.webp` | /basement-flooding-cleanup — "Why does water come up through a Midvale basement floor with no leak?" | WEAK | Sharp, correct room type (finished basement bedroom, egress window), but bone-dry: no water, damp, or drying cue anywhere under a flooding-explainer H2. |
| 2 | `basement-flooding-cleanup-2.webp` | /basement-flooding-cleanup — "Basement Apartments and Rentals" | WEAK | Same dry finished basement room as #1, different angle (same photo series). Clean and sharp, no artifacts, but again zero water/damage cue, and a visitor who saw #1 will recognise the room. |
| 3 | `basement-flooding-cleanup-3.webp` | /basement-flooding-cleanup — "Basement Flooding Across Midvale Neighborhoods" | PASS | Sharp aerial of a leafy suburban neighbourhood; generic but right for a neighbourhoods section. |
| 4 | `burst-pipe-water-damage-1.webp` | /burst-pipe-water-damage — "Where do pipes freeze first in Midvale homes?" | WEAK | Snow-capped pipe outlet with icicle, sharp and wintry — but it reads as a downspout/gutter outlet, not a supply pipe that bursts. Frozen theme is right, subject is the wrong kind of pipe. |
| 5 | `burst-pipe-water-damage-2.webp` | /burst-pipe-water-damage — "Pipe Burst in Wall: Why Surface Drying Isn't Enough" | PASS | Peeling, water-damaged paint on a concrete wall — exactly the wall-damage evidence the section describes. Sharp, real. |
| 6 | `burst-pipe-water-damage-3.webp` | /burst-pipe-water-damage — "Our Broken Pipe Cleanup Midvale Utah Process" | REPLACE | Alt claims "worker's hands gripping a weathered metal pipe fitting" — the frame actually shows hands holding what reads as a white-painted wood/birch-bark plank; no pipe fitting is visible as the subject (one copper fitting is blurred in a corner). Does not show pipe repair at all. Replace with a real photo of hands/a wrench on a pipe fitting or a burst pipe being repaired. |
| 7 | `ceiling-water-damage-1.webp` | /ceiling-water-damage — "Ceiling Leak Midvale: The Most Common Sources" | PASS | Man sanding a green drywall ceiling with a power sander; sharp, real, clearly ceiling-repair work. |
| 8 | `ceiling-water-damage-2.webp` | /ceiling-water-damage — "How We Repair Ceiling Water Damage" | PASS | Gloved arm plastering the ceiling/wall corner with a trowel; sharp, real, on-task. |
| 9 | `ceiling-water-damage-3.webp` | /ceiling-water-damage — "Ceiling Leaks by Midvale Home Type" | PASS | Room under renovation, stepladder, drop cloths, curved ceiling detail; sharp, real. No leak visible, but on-theme for a repair page. |
| 10 | `commercial-water-damage-1.webp` | /commercial-water-damage — "Midvale Business Districts We Serve" | PASS | Glass office towers seen from above; sharp, real. Big-city scale, but a fair business-districts image. |
| 11 | `commercial-water-damage-2.webp` | /commercial-water-damage — "Office Flood Cleanup Midvale: Keeping Work Moving" | PASS | Bright open-plan office, people working at laptops; sharp, real. No water, but the section is about keeping work moving, so a working office fits. |
| 12 | `commercial-water-damage-3.webp` | /commercial-water-damage — "Commercial Drying for Large Open Spaces" | PASS | See generated-7 section above: full colour, wet office floor with air movers + dehumidifier, topic-perfect, no AI tells. |
| 13 | `condo-apartment-water-damage-1.webp` | /condo-apartment-water-damage — "Who pays when water leaks from an upstairs condo in Midvale?" | PASS | White-brick apartment building with black metal balconies; sharp, real, right building type. |
| 14 | `condo-apartment-water-damage-2.webp` | /condo-apartment-water-damage — "How We Handle Multi-Unit Water Damage" | PASS | Worker in hard hat, safety glasses, orange hi-vis holding a pipe wrench; sharp, real. (Tiny logo on the glasses lens is illegible at display size.) |
| 15 | `condo-apartment-water-damage-3.webp` | /condo-apartment-water-damage — "Most Common Leak Sources in Midvale Condos and Apartments" | PASS | Grey drain/waste pipes on an exterior wall; sharp, real, on-topic. Pipe mould marks are tiny/embossed, not legible branding. |
| 16 | `crawl-space-water-damage-1.webp` | /crawl-space-water-damage — "Signs Your Crawl Space Is Wet" | PASS | Generated; see above. |
| 17 | `crawl-space-water-damage-2.webp` | /crawl-space-water-damage — "What Floods Midvale Crawl Spaces" | PASS | Generated; see above. |
| 18 | `crawl-space-water-damage-3.webp` | /crawl-space-water-damage — "Crawl Space Vapor Barrier After Drying" | WEAK | Subject is literally correct (clear poly vapor-barrier sheeting) but the shot is an abstract, soft-focus close-up of plastic with no context — no crawl space, no installation, reads as a texture swatch. Replace with a photo of vapor barrier being installed/laid in a crawl space. |
| 19 | `emergency-water-extraction-1.webp` | /emergency-water-extraction — "What Happens in the First 60 Minutes on Site" | PASS | Generated; see above. |
| 20 | `emergency-water-extraction-2.webp` | /emergency-water-extraction — "Water Removal Midvale Jobs: The Equipment and When We Use It" | PASS | Yellow wet/dry vacuum in a room under renovation; sharp, real, the equipment is the subject. No visible brand. |
| 21 | `emergency-water-extraction-3.webp` | /emergency-water-extraction — "Can Wet Carpet and Pad Be Saved?" | PASS | Generated; see above. |
| 22 | `hardwood-floor-cabinet-drying-1.webp` | /hardwood-floor-cabinet-drying — "Can wet hardwood floors in Midvale be saved without tearing them out?" | PASS | Close-up of worn wood planks with peeling finish and nail holes; sharp, real, shows damaged wood. |
| 23 | `hardwood-floor-cabinet-drying-2.webp` | /hardwood-floor-cabinet-drying — "Cabinet Water Damage Drying Midvale: Keeping Counters in Place" | WEAK | Grey kitchen cabinets + wood countertop + sink are the right subject, but the toaster oven carries a legible "Panasonic" brand and a decorative plate behind it has legible Cyrillic text; the kitchen also reads European, not a Utah home. |
| 24 | `hardwood-floor-cabinet-drying-3.webp` | /hardwood-floor-cabinet-drying — "Why Utah's Dry Climate Changes How Floors Dry" | PASS | Sunlight across a herringbone parquet floor; sharp, real. Dry/sunny read suits the climate section. |
| 25 | `cottonwood-heights-ut-1.webp` | /locations/cottonwood-heights-ut — "Cottonwood Heights Water Risks, Season by Season" | PASS | Snow-covered Wasatch mountains in cloud above the valley; sharp, real, right place/season. (A tiny aircraft is visible mid-frame; trivial.) |
| 26 | `cottonwood-heights-ut-2.webp` | /locations/cottonwood-heights-ut — "Burst Pipe Repair Cottonwood Heights: Winter Damage" | PASS | Aerial Salt Lake City with snow-covered mountains behind; sharp, real, same valley/mountain backdrop. |
| 27 | `cottonwood-heights-ut-3.webp` | /locations/cottonwood-heights-ut — "What to Do First When Water Hits Your Cottonwood Heights Home" | PASS | Snowy city street with snow-capped mountains; sharp, real winter scene. Distant signage is illegible at display size. |
| 28 | `magna-ut-1.webp` | /locations/magna-ut — "Home Age and Pipe Material in Magna" | WEAK | Ranch-style home with porch among autumn trees is the right subject, but the file has baked-in BLACK PILLARBOX BARS left and right (a narrower photo padded to 1200×675) — visible at full size and at display size. Also reads more pine-forest/south-eastern than Utah. Replace with a native 16:9 shot of an older Magna home, or re-crop this one without bars if the source allows. |
| 29 | `magna-ut-2.webp` | /locations/magna-ut — "Areas We Cover in Magna" | REPLACE | The photo is of WABASHA, Minnesota, not Magna: a "WABASHA MAIN STREET" sign is legible centre-frame, plus a legible boutique sign ("On the river Boutique — Antiques, Gifts, Home Decor") and a "SCHOEN" sign. Wrong town, wrong state, legible business signage. Replace with a real photo of Magna Main Street or an older Magna home/street. |
| 30 | `magna-ut-3.webp` | /locations/magna-ut — "Crawl Spaces and Additions in Magna" | WEAK | Sharp, clean empty carpeted basement room — but (a) it is the same room/photo series as `basement-flooding-cleanup-1.webp` (same grey walls, carpet, egress window, white doors; different angle), and (b) it shows neither a crawl space nor an addition under a crawl-space H2. Replace with a crawl-space or home-addition photo in Magna. |
| 31 | `south-salt-lake-ut-1.webp` | /locations/south-salt-lake-ut — "Water Damage for Renters, Owners and Businesses" | PASS | Multi-storey apartment building with balconies; sharp, real, right building type for a renters/multi-unit page. |
| 32 | `south-salt-lake-ut-2.webp` | /locations/south-salt-lake-ut — "Problem-to-Service Guide for South Salt Lake" | WEAK | Warehouse shelving with pallets and roof tiles: industrial character suits South Salt Lake, but it illustrates neither a problem nor a service for a problem-to-service guide, and brand text ("NELSKAMP") is legible on the tile packaging. Replace with a photo of a South Salt Lake apartment/warehouse interior with water damage or drying equipment. |
| 33 | `south-salt-lake-ut-3.webp` | /locations/south-salt-lake-ut — "Sewage Backup Cleanup South Salt Lake" | PASS | Generated; see above. |
| 34 | `mold-remediation-1.webp` | /mold-remediation — "Signs You May Have Mold" | PASS | Green/black mold streaks across a white block wall; sharp, real, exactly the section's subject. |
| 35 | `mold-remediation-2.webp` | /mold-remediation — "Mold Removal Midvale: Our Remediation Process" | PASS | Worker in white protective suit, respirator, blue gloves fogging a room; sharp, real, on-task. |
| 36 | `mold-remediation-3.webp` | /mold-remediation — "Preventing Mold After a Leak" | PASS | Black mildew stains streaking down a light wall; sharp, real, unmistakably mold staining (tight/abstract framing, but the subject is clear). |
| 37 | `sewage-backup-cleanup-1.webp` | /sewage-backup-cleanup — "Why Sewage Is Dangerous" | PASS | Worker in white protective suit + blue gloves with a pump sprayer in a kitchen; sharp, real, PPE/disinfection reads correctly for a sewage-danger section. No compression artifacts at full size. |
| 38 | `sewage-backup-cleanup-2.webp` | /sewage-backup-cleanup — "Floor Drain Backup in Older Midvale Homes" | WEAK | A drain grate is on-topic for floor drains, but the cast markings "400 X 600" and "EN124 B125" are legible across the frame (metric size + European standard — a non-US grate), and leaves growing through it make it read as a neglected outdoor storm drain rather than a basement floor drain. Replace with a basement floor drain in a home. |
| 39 | `sewage-backup-cleanup-3.webp` | /sewage-backup-cleanup — "Sewage Backups by Midvale Property Type" | PASS | Aerial autumn suburban neighbourhood; sharp, real, fair for a property-types/neighbourhoods section. |
| 40 | `storm-flood-damage-1.webp` | /storm-flood-damage — "Why do Midvale streets and basements flood in summer storms?" | PASS | Flooded suburban street with standing water between bare trees; sharp, real, exactly on-topic. |
| 41 | `storm-flood-damage-2.webp` | /storm-flood-damage — "Where Storm Water Gets Into Midvale Homes" | PASS | Rainwater pouring off a corrugated roof edge in heavy rain; sharp, real, dramatic and on-topic. |
| 42 | `storm-flood-damage-3.webp` | /storm-flood-damage — "Storm Water Damage Across Midvale Neighborhoods" | PASS | Cars driving through a flooded road in the rain; sharp, real, on-topic. (Licence plate blurred/illegible.) |
| 43 | `swamp-cooler-leak-water-damage-1.webp` | /swamp-cooler-leak-water-damage — "Why is my swamp cooler leaking through the ceiling in Midvale?" | PASS | Dark water stains/mildew streaks down a white wall; sharp, real, shows leak staining (wall, not ceiling, but unmistakably leak damage). |
| 44 | `swamp-cooler-leak-water-damage-2.webp` | /swamp-cooler-leak-water-damage — "Which Midvale Homes Have Swamp Coolers" | WEAK | Sharp photo of newer grey two-storey suburban houses — but NO swamp cooler is visible on any roof or wall in the frame. Generic houses under a section about which homes have coolers. Replace with a Utah home showing a roof- or side-mounted evaporative cooler. |
| 45 | `swamp-cooler-leak-water-damage-3.webp` | /swamp-cooler-leak-water-damage — "Side-Mount and Window Coolers" | REPLACE | Its own alt says it: an apartment facade in BOISE, IDAHO with WINDOW AIR CONDITIONER units — not side-mount/window swamp (evaporative) coolers, and not Utah. Wrong equipment, wrong city. Replace with a real photo of a side-mount or window evaporative cooler on a Utah home. |
| 46 | `water-damage-repair-1.webp` | /water-damage-repair — "Drywall Water Damage Repair Midvale" | PASS | Gloved hand smoothing joint compound with a wide taping knife; sharp, real, exactly on-task. (Very high-key/white, but clean.) |
| 47 | `water-damage-repair-2.webp` | /water-damage-repair — "Basement Rebuild After Flood" | PASS | Worker kneeling to fit a dark wood laminate plank, mallet beside him; sharp, real, rebuild work. |
| 48 | `water-damage-repair-3.webp` | /water-damage-repair — "Choosing Materials That Handle Water Better" | PASS | Room mid-renovation, freshly painted walls, stepladder, floor protection, shop vacuum; sharp, real, on-theme for a rebuild page. |
| 49 | `water-heater-leak-cleanup-1.webp` | /water-heater-leak-cleanup — "The Appliances That Flood Midvale Homes Most" | WEAK | A washing machine + bathroom is arguably on-topic (appliances), but the "Indesit" brand on the washer is clearly legible, the water heater itself appears only as a reflection in the mirror cabinet, and the wall-hung toilet/concealed cistern reads European. Replace with a real photo of a tank water heater (and/or washer) in a US utility space, no legible brand. |
| 50 | `water-heater-leak-cleanup-2.webp` | /water-heater-leak-cleanup — "Water Heater Flooded Basement Midvale: The First 15 Minutes" | PASS | Generated; see above. |
| 51 | `water-heater-leak-cleanup-3.webp` | /water-heater-leak-cleanup — "Gas, Electric and Tankless: How Each One Fails" | PASS | White wall-mounted tankless water heater with pipes; sharp, real, the heater is the clear subject. (Small logo/display on the unit is illegible.) |
| 52 | `water-leak-detection-1.webp` | /water-leak-detection — "The Simple Meter Test" | PASS | Round water pressure gauge on a red pipe, psi/kPa; sharp, real, exactly the meter-test subject. Dial text ("WATER", numbers, small "CENTRAL" mark) is inherent to the instrument face. |
| 53 | `water-leak-detection-2.webp` | /water-leak-detection — "Leak Behind Wall: Where Midvale Leaks Hide" | PASS | Patch of plaster fallen from a blue painted wall exposing substrate; sharp, real, shows wall failure. (Bright-blue paint + outdoor look is slightly off for an interior leak, but the subject reads clearly.) |
| 54 | `water-leak-detection-3.webp` | /water-leak-detection — "What Happens After We Find the Leak" | PASS | Technician repairing an orange pump housing on a workbench covered with tools; sharp, real — repair-after-detection reads correctly for the section. |
| 55 | `window-well-flooding-1.webp` | /window-well-flooding — "Why do Midvale window wells fill with water and flood the basement?" | PASS | Rain-soaked suburban street seen through a window, American flag; sharp, real, wet-weather read with a through-window framing that suits the topic. |
| 56 | `window-well-flooding-2.webp` | /window-well-flooding — "Window Well Leak Into Basement Midvale: The Usual Causes" | PASS | Metal downspout dripping water onto a stone foundation wall; sharp, real. No window well in frame, but a downspout dumping at the foundation is exactly one of the causes the section covers. |
| 57 | `window-well-flooding-3.webp` | /window-well-flooding — "Window Well Problems by Midvale Home Type" | WEAK | Sharp photo of suburban houses under a cloudy sky — but no water, no window well, no basement cue anywhere in the frame. Pure generic houses under a flooding section. Replace with a photo of a window well (ideally with water) at a Midvale-style home. |

## REPLACE shortlist (3 — do first)

1. **`burst-pipe-water-damage-3.webp`** (/burst-pipe-water-damage, "Our Broken Pipe Cleanup Midvale Utah Process") — frame shows hands holding a white wood/bark plank, not a pipe fitting. Replace with: real photo of hands/a wrench on a pipe fitting or a burst pipe being repaired.
2. **`magna-ut-2.webp`** (/locations/magna-ut, "Areas We Cover in Magna") — photo is Wabasha, Minnesota ("WABASHA MAIN STREET" sign legible). Replace with: real photo of Magna Main Street or an older Magna home/street.
3. **`swamp-cooler-leak-water-damage-3.webp`** (/swamp-cooler-leak-water-damage, "Side-Mount and Window Coolers") — Boise, Idaho apartment with window AC units, not evaporative coolers. Replace with: real photo of a side-mount or window evaporative (swamp) cooler on a Utah home.

## WEAK shortlist (12 — replace when convenient, in priority order)

1. `magna-ut-3.webp` — finished basement room (twin of basement-1) under a crawl-space H2; needs a crawl-space/addition photo.
2. `magna-ut-1.webp` — baked-in black pillarbox bars; needs a native 16:9 older-Magna-home shot.
3. `basement-flooding-cleanup-1.webp` + `basement-flooding-cleanup-2.webp` — two dry finished rooms, same series; at least one should show water/drying (extraction, air movers, wet carpet).
4. `swamp-cooler-leak-water-damage-2.webp` — no cooler visible; needs a Utah home with a visible evaporative cooler.
5. `water-heater-leak-cleanup-1.webp` — legible "Indesit" brand, heater only in mirror reflection; needs a US utility-space water-heater photo, no brand.
6. `hardwood-floor-cabinet-drying-2.webp` — legible "Panasonic" brand + Cyrillic plate; needs a brand-free US kitchen-cabinet photo.
7. `south-salt-lake-ut-2.webp` — warehouse roof-tile stock, legible "NELSKAMP" packaging, illustrates no problem/service; needs a South Salt Lake interior with damage or drying equipment.
8. `sewage-backup-cleanup-2.webp` — legible metric/European cast marks ("400 X 600", "EN124 B125"), reads as an outdoor storm drain; needs a basement floor drain photo.
9. `burst-pipe-water-damage-1.webp` — reads as a downspout, not a burst supply pipe; needs a frozen/burst supply pipe photo.
10. `crawl-space-water-damage-3.webp` — abstract soft-focus plastic swatch; needs vapor barrier being installed in a crawl space.
11. `window-well-flooding-3.webp` — generic houses, no water/well cue; needs a window-well photo (ideally with water).

## Notes (not verdicts — for the record)

- **Prior B&W note on `commercial-water-damage-3.webp` is stale.** The design round recorded it as the only grayscale image sitewide (REPLACE P3-1). Viewed at full size today it is in full colour. No action needed on that ground.
- **`magna-ut-3.webp` vs `basement-flooding-cleanup-1.webp` twin confirmed visually:** different photos/angles of the same grey carpeted basement room (same egress window, doors, carpet). Not a duplicate file (md5/aHash differ), but a sharp-eyed visitor browsing both pages could notice.
- **Alt-text nits (manifest only, not image defects):** `ceiling-water-damage-1.webp` alt says "Man on a ladder" — no ladder is visible; `sewage-backup-cleanup-1.webp` alt says "spray bottle and a cleaning cloth" — the frame shows a pump sprayer and no cloth. Worth fixing the alts if the files are ever touched.
- **Inherent instrument text passed, not flagged:** gauge dial text on `water-leak-detection-1.webp`, pipe mould marks on `condo-apartment-water-damage-3.webp`, and the small illegible unit display on `water-heater-leak-cleanup-3.webp` are part of the objects photographed, not scene branding.
- **No errors encountered during the audit.** All 57 files opened and rendered; manifest, pages data, and EXIF checks all ran clean.
