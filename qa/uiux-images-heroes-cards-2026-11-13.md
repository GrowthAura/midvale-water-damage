# Midvale UT — Image Audit: Heroes + Cards (Stage 1 UI/UX round)

- **Date:** 2026-11-13
- **Auditor:** image auditor (Stage 1 UI/UX round)
- **Scope:** `public/images/heroes/` (31 files, one per route) + `public/images/cards/` (19 files)
- **Method:** every file viewed at full size with the file-read tool — NOT judged from filenames, dimensions, or thumbnails. No file edits made (audit only).
- **Design rule confirmed from code:** `lib/content.ts` (line ~383) states cards are intentionally "different scene from the hero" — so a card is judged on **same topic, different scene**, not on being the same file as the hero. All 19 cards match their linked page's topic; 0 cards point at the wrong page.
- **Exact duplicates:** none — all 50 files have distinct content (no byte-identical pair). Near-duplicates are motif/scene repeats, listed below.

## Counts

| Set | Total | PASS | WEAK | REPLACE |
|---|---|---|---|---|
| Heroes | 31 | 26 | 5 | 0 |
| Cards | 19 | 15 | 4 | 0 |
| **Total** | **50** | **41** | **9** | **0** |

No image is wrong-topic, broken, or watermarked enough to earn REPLACE. All 9 WEAKs are specific, fixable swaps — each names the replacement shot needed.

## Heroes — per-image table

| File | Route | Verdict | Reason |
|---|---|---|---|
| `heroes/home.webp` | `/` | PASS | Crew extracting flood water in a living room, Wasatch-style mountains through the windows. Strong topic + Utah place fit. Minor: extraction machine looks slightly fantastical and faces are soft (AI sheen), but it reads clearly as real restoration work. |
| `heroes/about.webp` | `/about/` | PASS | Crew + unbranded service truck outside a mountain-town home at dusk. Good team/about fit, Utah mountains in background. No legible branding/text. |
| `heroes/contact.webp` | `/contact/` | PASS | Technician on the phone among air movers on a wet floor, furniture in protective plastic. Excellent contact-page fit — the call + the job in one frame. |
| `heroes/emergency-water-extraction.webp` | `/emergency-water-extraction/` | PASS | Crew running a truck-mounted extractor in a flooded basement/garage. Exact topic, dramatic, sharp. |
| `heroes/water-damage-repair.webp` | `/water-damage-repair/` | WEAK | Pretty but off-topic: an empty, already-finished room with one work light and a mountain view. No repair work, no damage, no crew — reads as an empty-room real-estate photo, not a repair page. (Its own card image, fresh drywall mud + trim, shows the repair better than this hero does.) |
| `heroes/basement-flooding-cleanup.webp` | `/basement-flooding-cleanup/` | WEAK | Flooded wood-panel basement, worker lifting soaked carpet — strong scene, but a visible logic error: the pump on the right is discharging a jet of water back onto the already-flooded floor it is supposed to be pumping out. Noticeable on a full-size look. |
| `heroes/burst-pipe-water-damage.webp` | `/burst-pipe-water-damage/` | PASS | Split copper pipe spraying water inside an opened, wet wall cavity. Exact topic, sharp, no text. |
| `heroes/ceiling-water-damage.webp` | `/ceiling-water-damage/` | PASS | Sagging, stained ceiling dripping into a bucket, snowy icicles outside the window (Utah winter). Exact topic + place cue. |
| `heroes/commercial-water-damage.webp` | `/commercial-water-damage/` | PASS | Restaurant dining room, chairs up on tables, air movers + dehumidifier on wet carpet, mountain prints on the wall. Unmistakably commercial. |
| `heroes/condo-apartment-water-damage.webp` | `/condo-apartment-water-damage/` | PASS | Apartment hallway with multiple unit doors, ceiling leak pouring into a bucket, two techs with a moisture meter. Exact condo/apartment context. |
| `heroes/cottonwood-heights-ut.webp` | `/locations/cottonwood-heights-ut/` | PASS | Snowy mountain-neighbourhood street, homes, wet road, steep snowy canyon behind. Strong Utah/foothills place fit for an area page. (Canyon is generic-alpine rather than identifiably Cottonwood Heights, but plausible.) |
| `heroes/crawl-space-water-damage.webp` | `/crawl-space-water-damage/` | PASS | Technician with headlamp in a muddy crawl space under wet joists, dripping water, cobwebs. Exact topic. |
| `heroes/frozen-pipes-midvale.webp` | `/resources/frozen-pipes-midvale/` | PASS | Burst copper pipe encased in ice in a crawl space. Unmistakable frozen-pipe topic. Note: the fern-like ice crystals are oversized/stylised (AI sheen) — reads fine at hero size, slightly exaggerated up close. |
| `heroes/hardwood-floor-cabinet-drying.webp` | `/hardwood-floor-cabinet-drying/` | PASS | Kitchen with cupped wet hardwood, air movers aimed at cabinets/floor, drying mats. Exact topic, every element correct. |
| `heroes/magna-ut.webp` | `/locations/magna-ut/` | PASS | Wet old-brick main street, storefronts, mountains behind. Fits Magna's historic mining-town character. Minor: the vintage pickup is an anachronism; harmless. |
| `heroes/midvale-water-sewer-emergency-contacts.webp` | `/resources/midvale-water-sewer-emergency-contacts/` | PASS | Utility truck at night on a wet street, open manhole, cones, mountains. Exact sewer-emergency topic. (Plate is illegible gibberish — not readable, not a defect.) |
| `heroes/mold-remediation.webp` | `/mold-remediation/` | PASS | Worker in Tyvek + respirator scraping a mouldy wall inside poly containment, air scrubber present. Exact topic. |
| `heroes/privacy-policy.webp` | `/privacy-policy/` | PASS | Desk with file folder, blank papers, closed laptop, lamp. Neutral documents image, correct register for a legal page. No legible text. |
| `heroes/sewage-backup-cleanup.webp` | `/sewage-backup-cleanup/` | PASS | Three workers in PPE/respirators cleaning a filthy tiled bathroom floor (spray, brush, vacuum hose). Exact topic. |
| `heroes/south-salt-lake-ut.webp` | `/locations/south-salt-lake-ut/` | PASS | Wet street at dusk, apartment blocks on one side, warehouses/industrial on the other — matches South Salt Lake's genuinely mixed residential/industrial character. Good place fit. |
| `heroes/storm-flood-damage.webp` | `/storm-flood-damage/` | PASS | Flood water rushing into a garage from a storm street, car headlights, desert scrub + mountains. Exact Utah storm-flood scene. |
| `heroes/swamp-cooler-leak-water-damage.webp` | `/swamp-cooler-leak-water-damage/` | PASS | Rooftop evaporative cooler on a wet shingle roof above rotted, water-damaged eaves/insulation. Exact Utah swamp-cooler topic. |
| `heroes/upstairs-unit-leak-who-pays-utah.webp` | `/resources/upstairs-unit-leak-who-pays-utah/` | WEAK | Near-duplicate motif of the ceiling hero: cracked ceiling dripping into a bucket in an empty room. Same "ceiling drip + bucket" composition as `heroes/ceiling-water-damage.webp`, only the window view differs. A resource page about an upstairs-unit leak needs a distinct angle (e.g. the upstairs bathroom source, or a two-storey/apartment context). |
| `heroes/water-heater-leak-cleanup.webp` | `/water-heater-leak-cleanup/` | PASS | Corroded water heater with dripping pipes and a puddle. Exact topic. Minor: pipe routing is slightly fantastical up close. |
| `heroes/water-leak-detection.webp` | `/water-leak-detection/` | PASS | Technician with thermal-imaging camera + moisture probe on a wet wall. Exact topic. |
| `heroes/window-well-flooding.webp` | `/window-well-flooding/` | PASS | Meltwater pouring from a flooded window well through a basement window into a bedroom, snow outside. Exact topic, very clear. |
| `heroes/winterize-swamp-cooler-utah.webp` | `/resources/winterize-swamp-cooler-utah/` | PASS | Snow-covered covered evaporative cooler on a snowy roof, valley/mountains behind. Exact winterisation topic. |
| `heroes/basement-flooding-spring-snowmelt-utah.webp` | `/resources/basement-flooding-spring-snowmelt-utah/` | WEAK | Near-duplicate motif of the window-well hero: meltwater streaming in through a basement window with snow outside and puddles on a concrete floor. Same "water pouring through basement window, snow outside" scene as `heroes/window-well-flooding.webp`, only the room differs (bare basement vs bedroom). Needs a distinct snowmelt angle (e.g. snowmelt pooling against the foundation outside, or a sump pump handling meltwater). |
| `heroes/can-mold-grow-in-utah.webp` | `/resources/can-mold-grow-in-utah/` | PASS | Flashlight beam on a mould-spotted wall corner, vacuum hose in frame. Exact mould topic for the question page. |
| `heroes/disclaimer.webp` | `/disclaimer/` | WEAK | Shows a technician moisture-testing a damp wall — an inspection photo on a legal page. It is not wrong for the business, but it says nothing about a disclaimer; the privacy/terms pages use neutral documents imagery, and this one should too. |
| `heroes/terms-of-use.webp` | `/terms-of-use/` | PASS | Stack of blank papers, glasses, pen on a desk by a window. Neutral documents image, correct register for a legal page. |

## Cards — per-image table

Cards are designed (per `lib/content.ts`) to be a **different scene from the hero, same topic**. "Match" below means: same service/area as its linked page's hero, different scene.

| File | Linked page | Verdict | Reason |
|---|---|---|---|
| `cards/basement-flooding-cleanup.webp` | `/basement-flooding-cleanup/` | PASS | Soaked carpet peeled back over a muddy floor. Same topic as hero, different scene. Matches its alt text. |
| `cards/burst-pipe-water-damage.webp` | `/burst-pipe-water-damage/` | WEAK | Shows a **frozen** burst pipe (ice crystals, water spraying) in a crawl space — visually near-duplicates the **frozen-pipes hero** (`heroes/frozen-pipes-midvale.webp`: ice-covered burst copper pipe). A visitor scanning cards will read this as the frozen-pipes page, not burst-pipe. Needs a non-frozen burst pipe (e.g. the hero's opened-wall split copper pipe from another angle). |
| `cards/ceiling-water-damage.webp` | `/ceiling-water-damage/` | PASS | Brown water stain spreading across a ceiling with a drip forming. Same topic, different scene from hero. |
| `cards/commercial-water-damage.webp` | `/commercial-water-damage/` | PASS | Office with air movers + dehumidifier on wet carpet tiles. Commercial setting, different scene from the hero's restaurant. |
| `cards/condo-apartment-water-damage.webp` | `/condo-apartment-water-damage/` | PASS | Water dripping from a ceiling light fixture into a bucket — apartment-specific (electrical hazard) and distinct from the hero's hallway scene. Note: this is the site's third "drip into a bucket" image (with the ceiling + upstairs heroes) — acceptable here because the light-fixture detail makes it distinct, but no fourth bucket shot should be added anywhere. |
| `cards/cottonwood-heights-ut.webp` | `/locations/cottonwood-heights-ut/` | WEAK | Near-duplicate of its own hero: same snowy canyon + snow-covered bench homes, only from an overlook with a bench instead of street level. Card and hero read as the same photo at card size. Needs a different Cottonwood Heights angle (street-level homes, foothill trailhead, or the mouth of Big Cottonwood Canyon). |
| `cards/crawl-space-water-damage.webp` | `/crawl-space-water-damage/` | PASS | Wet floor joists + standing water in a dark dirt crawl space. Same topic, different scene from hero (no technician). |
| `cards/emergency-water-extraction.webp` | `/emergency-water-extraction/` | PASS | Submersible pump + extraction hose in standing water. Same topic, different scene from hero (no crew/truck). |
| `cards/hardwood-floor-cabinet-drying.webp` | `/hardwood-floor-cabinet-drying/` | PASS | Cupped wet hardwood with a drying mat + hose, cabinets behind. Matches its alt text exactly; different scene from hero. |
| `cards/magna-ut.webp` | `/locations/magna-ut/` | WEAK | Near-duplicate of its own hero: same wet brick main street with storefronts and a snowy mountain behind, only a wider/straighter view. Card and hero read as the same photo at card size. Needs a different Magna angle (residential street of mine-era homes, or Oquirrh foothills view). |
| `cards/mold-remediation.webp` | `/mold-remediation/` | PASS | HEPA air scrubber with ducting into poly containment. Same topic, different scene from hero. Note: no mould is visible in the card itself (equipment only) — acceptable for a card, as the alt text describes the equipment. |
| `cards/sewage-backup-cleanup.webp` | `/sewage-backup-cleanup/` | PASS | Floor drain with sewage backup water, worker in PPE with sprayer. Same topic, different scene from hero's bathroom. |
| `cards/south-salt-lake-ut.webp` | `/locations/south-salt-lake-ut/` | WEAK | Near-duplicate of its own hero: same apartments-on-one-side / warehouses-on-the-other wet street, same dusk composition. Card and hero read as the same photo at card size. Needs a different South Salt Lake angle (TRAX corridor, State Street, or an industrial-yard close-up). |
| `cards/storm-flood-damage.webp` | `/storm-flood-damage/` | PASS | Sandbags + sump pump in a muddy garage flood, rain outside. Same topic, different scene from hero. |
| `cards/swamp-cooler-leak-water-damage.webp` | `/swamp-cooler-leak-water-damage/` | PASS | Overflowing swamp-cooler drain pan spilling onto a wet roof. Matches its alt text exactly; different scene from hero. |
| `cards/water-damage-repair.webp` | `/water-damage-repair/` | PASS | Fresh drywall mud + new white trim, trowel, work lamp — actual repair work in progress. Same topic, different scene from hero, and stronger on topic than its own hero. |
| `cards/water-heater-leak-cleanup.webp` | `/water-heater-leak-cleanup/` | PASS | Corroded valve dripping onto a wet concrete floor. Same topic, tighter scene than the hero's full tank. |
| `cards/water-leak-detection.webp` | `/water-leak-detection/` | PASS | Moisture meter + thermal camera against a wet wall. Same topic, different scene from hero (no technician). |
| `cards/window-well-flooding.webp` | `/window-well-flooding/` | PASS | Corrugated window well half-full of icy snowmelt water with leaves. Matches its alt text exactly; exterior scene vs the hero's interior view. |

## Cross-image duplication notes

- **No exact duplicates.** All 50 files are distinct images.
- **Near-duplicate pairs (the WEAKs above):**
  1. `heroes/ceiling-water-damage.webp` ↔ `heroes/upstairs-unit-leak-who-pays-utah.webp` — same ceiling-drip-into-bucket motif.
  2. `heroes/window-well-flooding.webp` ↔ `heroes/basement-flooding-spring-snowmelt-utah.webp` — same water-through-basement-window + snow motif.
  3. `heroes/frozen-pipes-midvale.webp` ↔ `cards/burst-pipe-water-damage.webp` — same ice-covered burst copper pipe motif (cross-page confusion, not just repetition).
  4. `heroes/cottonwood-heights-ut.webp` ↔ `cards/cottonwood-heights-ut.webp` — same snowy-canyon-over-homes scene.
  5. `heroes/magna-ut.webp` ↔ `cards/magna-ut.webp` — same wet brick main street scene.
  6. `heroes/south-salt-lake-ut.webp` ↔ `cards/south-salt-lake-ut.webp` — same apartments-vs-warehouses wet street scene.
- **Motif overuse (not a per-image fail, but a site-wide note):** three images use the "drip into a bucket" composition (ceiling hero, upstairs hero, condo card). The condo card escapes a WEAK only because its ceiling-light-fixture detail makes it distinct. No further bucket shots should be added.
- **Site-wide look:** all 50 images share one consistent cinematic, dusk-lit, AI-generated/created look (soft faces in the home hero, oversized ice crystals in the frozen-pipes hero, a fantastical extraction machine in the home hero, the pump-logic error in the basement hero). None is presented as a real job photo in the audit's remit to judge, but per the user's rule created images are only for slots where no real photo of that exact place/service exists — the 5 area/legal images and the 3 area cards are the ones a real Utah photo could most credibly replace later. No image carries a legible watermark, logo, or readable branding.

## REPLACE shortlist

**None.** 0 images earn REPLACE — nothing is wrong-topic, broken, watermarked, or unusable. The 9 WEAKs below are the full fix list; each is a swap to a specified replacement shot, in priority order:

1. **Hero — `water-damage-repair.webp`:** replace with a real repair-action photo — worker trowelling fresh drywall mud / fitting new trim (the current card image's subject, shot wider, would work as the hero).
2. **Hero — `upstairs-unit-leak-who-pays-utah.webp`:** replace with a distinct upstairs-leak angle — water source in an upstairs bathroom, or a two-storey/apartment exterior establishing the upstairs/downstairs relationship.
3. **Hero — `basement-flooding-spring-snowmelt-utah.webp`:** replace with a distinct snowmelt angle — meltwater pooling against the foundation outside, or a sump pump discharging meltwater.
4. **Hero — `basement-flooding-cleanup.webp`:** replace with a corrected version of the same scene — pump discharging **out** (hose leading away/out a window or door), worker lifting soaked carpet.
5. **Hero — `disclaimer.webp`:** replace with a neutral documents/office image in the same register as the privacy-policy and terms heroes (desk, papers, laptop — no people, no damage).
6. **Card — `burst-pipe-water-damage.webp`:** replace with a non-frozen burst pipe — split copper in an opened wall from a different angle than the hero.
7. **Card — `cottonwood-heights-ut.webp`:** replace with a different Cottonwood Heights angle — street-level homes, foothill trailhead, or the mouth of Big Cottonwood Canyon.
8. **Card — `magna-ut.webp`:** replace with a different Magna angle — residential street of mine-era homes, or an Oquirrh foothills view.
9. **Card — `south-salt-lake-ut.webp`:** replace with a different South Salt Lake angle — TRAX corridor, State Street, or an industrial-yard close-up.

## Aside (not an image verdict)

`lib/content.ts` line ~383 still says "21 heroes, 0 repeats" but the heroes folder now holds 31 files (10 added later: about, contact, disclaimer, privacy-policy, terms-of-use, basement-flooding-spring-snowmelt-utah, can-mold-grow-in-utah, frozen-pipes-midvale, upstairs-unit-leak-who-pays-utah, winterize-swamp-cooler-utah). Stale comment only — no image impact, flagged so the coordinator can correct it in passing.
