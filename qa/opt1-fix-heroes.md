# F2 Hero Replacements — Cycle 1 Image Recovery (Batch 2)

**Date:** 2026-11-13 ~21:05 PKT | **Worker:** Cycle 1 image recovery (finishing interrupted F2 worker)
**Scope:** 3 hero replacements in `public/images/heroes/` + 2 alt rewrites + 1 opportunistic body swap. All 3 hero alts KEPT verbatim (lib/content.ts untouched for heroes). Local only — no push/export.

## Pre-state (verified at start of this job)

- `qa/opt1-hero-backup/` holds the 3 old heroes; current files were byte-identical to backups (sha256-verified) — old wrong photos still in place. Backup shas: disclaimer `12748157…`, upstairs `b45712bc…`, water-damage-repair `e5860e27…`.

## Pexels sourcing (done first, per task)

- Direct Pexels search-page fetch from the VM returns **403** (`qa/pexels-search.py` fails) — same block noted on other chains. Search pages were instead read via the browser fetch route, which works.
- Queries run (5 hero queries + 1 opportunistic): `moisture meter water damage`, `water damage inspection`, `ceiling water leak`, `water damage ceiling`, `leaking ceiling`, `newly renovated living room`, `utah house mountains`.
- **Slot 1 (disclaimer): NO fitting Pexels photo.** Results were utility-meter close-ups, an abandoned-building man with flashlight in Vorkuta, Russia (wrong place), and a senior inspecting a bathroom (no moisture meter, no water-damaged wall). The image-search CLI's technician-with-meter hits are other companies' website images (floodpro.us, restoreadvisor.com, etc.) — not freely licensed stock, NOT used.
- **Slot 2 (upstairs-unit): NO fitting Pexels photo.** Three queries returned only dripping faucets/pipes (outdoor), abstract water drops, and abandoned-building decay. No photo of water dripping from an apartment ceiling into the unit below exists in the Pexels pools searched.
- **Slot 3 (water-damage-repair): FIT FOUND on Pexels** — see below.
- Per task, slots 1–2 were therefore GENERATED (photographic style, metadata stripped, never to be claimed as real job photos).

## Slot 1 — heroes/disclaimer.webp — GENERATED (no Pexels fit)

| | |
|---|---|
| Old | Blurry office photo: laptop, calculator, card terminal (viewed full-size) |
| New | AI-generated photograph: technician kneeling in a dark room, pin-type moisture meter pressed against a severely water-damaged wall (brown stains, peeling paint), wet floor, tool belt |
| Alt (kept) | "Technician inspecting a water-damaged wall with a moisture meter in a dark room" — matches the new photo exactly |
| Source | Generated with media.generate_image, photographic style; generation file `qa/gen/media-generation-midvale-hero-disclaimer-gen-0-e2aacd2f-2c2b-44f1-b3bd-6b96e82f8247.webp` (1920x1280, XMP present in the raw generation — stripped on install) |
| Install | 1600x1066 WebP q82, 123,354 B (old 34,340 B). sha256 new `3443f783e195fd84227c9360d9ad364eb257a24efdfc91e68d0c21b723cf1914` |
| Honesty note | GENERATED image — not a real job photo; do not present it as one |

## Slot 2 — heroes/upstairs-unit-leak-who-pays-utah.webp — GENERATED (no Pexels fit)

| | |
|---|---|
| Old | Daylight bathroom flood with mold stains (viewed full-size) — a bathroom flood, not a ceiling leak into the unit below |
| New | AI-generated photograph: water streaming/dripping from a large brown-stained, peeling ceiling into the furnished living room below (sofa and coffee table getting wet), daylight through windows |
| Alt (kept) | "Water dripping from an apartment ceiling into the unit below in Midvale" — matches the new photo exactly |
| Source | Generated with media.generate_image, photographic style; generation file `qa/gen/media-generation-midvale-hero-upstairs-gen-0-24cf23d1-a513-4d89-8127-f1575efadbf6.webp` (1920x1280, XMP present in the raw generation — stripped on install) |
| Install | 1600x1066 WebP q82, 116,246 B (old 87,580 B). sha256 new `b52193f61644b13b6327c4b71c4531435d75864768fb8498e702cc87eae793c9` |
| Honesty note | GENERATED image — not a real job photo; do not present it as one |

## Slot 3 — heroes/water-damage-repair.webp — PEXELS 40701216

| | |
|---|---|
| Old | Worker portrait (viewed — not a rebuilt room) |
| New | Pexels photo 40701216, "Renovated living room with hardwood floors and crown molding in Akron, Ohio home", by Josh (PleaseLinkToOurWebsite), taken Mar 24, 2026 in Akron, Ohio, USA, 8262x5506. Page: https://www.pexels.com/photo/bright-renovated-living-room-in-akron-home-40701216/ |
| Alt (kept) | "Newly rebuilt room in a Midvale home, fresh drywall and trim" — photo shows a renovated living room with fresh light-gray walls, white crown-molding trim, hardwood floors; matches |
| Install | 1600x1066 WebP q82 from the Pexels CDN original, 109,092 B (old 99,430 B). sha256 new `b4d6e0703ef73a567d211795ceb637de34867d10f6f291d0ac2490600f2ce219` |
| Honesty note | Real Pexels stock photo (Akron, Ohio home, not a Midvale job photo); alt kept per task |

## Reuse checks (fresh disk reads — never a stale manifest)

- **Method:** `qa/opt1-hero-reuse.py` — corpus = every image under `public/images/` + `images/` in 34 site dirs, read fresh from disk at run time: **2,269 files**. Nets: md5 exact + 8x8 aHash + 16x16 aHash. Hash nets are supporting evidence only; any aHash8 ≤ 8 flag gets full-size visual adjudication. Results in `qa/opt1-hero-reuse.json`.
- **Pexels-ID grep:** `40701216` — 0 hits in all `*/qa/IMAGE-LOG*.md` + `CARD-IMAGE-LOG*.md` files across the workspace.
- **40701216:** md5 hits 0. Closest aHash8 = 12 (Plano 3 laundry-room, Tulsa Claremore images), aHash16 = 58–75 — above the flag band, clearly different photos. **CLEAR.**
- **gen-disclaimer:** md5 hits 0. Closest aHash8 = 4 (Plano 3 `wet-tile-9376351.webp`, aHash16 = 43) — inside the ≤8 flag band, so **visually adjudicated full-size**: the Plano 3 file is a black-and-white photo of wet patterned floor tiles with a palm-frond shadow — a completely different subject from the generated technician-with-meter image. The aHash8 similarity is a dark-tone coincidence. **VERDICT: DIFFERENT, not a reuse. CLEAR.**
- **gen-upstairs:** md5 hits 0. Closest aHash8 = 10 (Plano 3 plumber-work), aHash16 = 61 — above the flag band, clearly different. **CLEAR.**
- **All 3 new heroes: reuse nets CLEAR. No live-site reuse.**

## Metadata (exiftool, installed files)

- EXIF 0, XMP 0, ICC profile 0 on all 3 installed heroes (per-file scan). The 2 raw generations carried XMP; the install re-save (PIL, no exif/icc/xmp passed) stripped it — verified 0 after install. The Pexels JPEG carried EXIF; likewise stripped on convert.

## Verification of installed files (all 3 viewed full-size after install)

- disclaimer: technician + moisture meter + stained wall + dark room — alt match PASS, no conversion loss.
- upstairs-unit: ceiling stain + dripping water + furnished room below — alt match PASS, no conversion loss.
- water-damage-repair: renovated room, fresh walls, crown-molding trim, hardwood floors — alt match PASS, no conversion loss.
- Dims: 3/3 exactly 1600x1066.

## Alt rewrites (Job 3 — chrome, not doc content; photos viewed full-size first)

1. **cards/burst-pipe-water-damage** (`lib/content.ts:438`):
   - OLD: "Burst frozen pipe joint with ice and water spraying in a dark crawl space"
   - NEW: "Split copper pipe spraying water inside an opened wall cavity with wet wooden studs"
   - Reason: photo is a split copper pipe spraying water inside an opened wall cavity with wet studs and torn drywall — no ice, no crawl space. (Hero alt at :402 already says "Split copper pipe spraying water inside a dark wall cavity" — consistent.)
2. **body/cottonwood-heights-ut-3** (`lib/body-images.json`):
   - OLD: "A snowy city street in Salt Lake City with snow-capped mountains in the background"
   - NEW: "Snowy city rooftops in the Salt Lake Valley with snow-capped mountains under low cloud"
   - Reason: photo is an elevated/rooftop view over snowy city rooftops with snow-capped mountains under low cloud — no street visible.
   - `lib/body-images.json` re-validated as JSON after edit (19 pages). Hero alts in `lib/content.ts` unchanged.

## Opportunistic swaps

- **magna-ut-1 body — SWAPPED.** Old: gray ranch with porch among trees — generic SE-US look (crepe myrtles, pines, no mountains). New: Pexels **5587966**, "Charming suburban home surrounded by vibrant fall foliage in Woodland Hills, Utah" by Get Lost Mike, Woodland Hills, UT, 3172x1784 — aerial drone shot of a Utah home amid red/orange maples, blue spruce and pines. Clearly better place-fit for the Magna, UT page. Installed at 800x450 WebP q82, 145,698 B (old 138,482 B). Alt rewritten: "Aerial view of a Utah home surrounded by vibrant autumn trees" (old: "A ranch-style home with a front porch among trees in autumn"). Reuse: Pexels-ID grep 0 hits; fresh-disk net `qa/opt1-magna-reuse.py` (same 2,269-file corpus): md5 hits 0, closest aHash8 = 16 (Plano 3 crawl-space, Tulsa Bixby corridor), aHash16 = 88–89 — far above flag band, clearly different. **CLEAR.** EXIF/XMP/ICC 0 after install. Installed file viewed full-size — matches new alt. NOTE: this swap postdates the F1 resize verification, so `qa/opt1-fix-resize.md` totals are pre-swap for this one file (+7,216 B vs its verified row; dims unchanged 800x450).
- **water-damage-repair-1 body — LEFT AS-IS.** Viewed full-size: gloved hand smoothing white plaster/compound with a trowel on a wall — near-white-on-white as flagged, but on-topic (repair finishing). No clearly better photo turned up in this sourcing pass.
- **mold-remediation-2 body — LEFT AS-IS** per task (washed-out, no swap attempted).

## Unfilled slots

- **None.** All 3 hero slots filled (1 Pexels + 2 generated). No slot left on an old wrong photo.

## Files written / changed this job

- `qa/opt1-fix-heroes.md` (this file), `qa/opt1-hero-reuse.py`, `qa/opt1-hero-reuse.json`, `qa/opt1-magna-reuse.py`, `qa/opt1-magna-reuse.json`
- Installed: `public/images/heroes/disclaimer.webp`, `public/images/heroes/upstairs-unit-leak-who-pays-utah.webp`, `public/images/heroes/water-damage-repair.webp`, `public/images/body/magna-ut-1.webp`
- Edited: `lib/content.ts` (1 card alt), `lib/body-images.json` (2 body alts)
- Generation sources kept: `qa/gen/media-generation-midvale-hero-*-gen-0-*.webp` (raw generations, XMP intact — do not install directly)
- NOT done: `npm run export` (coordinator's single fresh export), no push/deploy/token/DNS.

## Verdict

**F2 HEROES COMPLETE — 3/3 replaced and verified.** Pexels 1, generated 2 (honestly labelled), reuse nets clear on a fresh 2,269-file corpus with one visual adjudication (different), metadata 0, dims 1600x1066, alts match. Plus 2 required alt rewrites and 1 opportunistic body swap (Magna), all verified.
