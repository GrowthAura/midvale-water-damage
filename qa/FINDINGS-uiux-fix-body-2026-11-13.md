# FINDINGS — Body image fix, Stage 1 UI/UX round — 2026-11-13

Scope: fix list in `qa/uiux-images-body-2026-11-13.md`. Work only in `public/images/body/` + `lib/body-images.json` (alts only). Local only; no push/deploy.

## Result: 15/15 replaced, 0 unfilled, + 2 alt fixes

| File | Old verdict | New source | Viewed verdict |
|---|---|---|---|
| basement-flooding-cleanup-1.webp | WEAK (dry room) | generated | ACCEPT — flooded bedroom, standing water, extraction + air movers |
| basement-flooding-cleanup-2.webp | WEAK (dry room) | generated | ACCEPT — wet carpet peeled back, soaked pad, air movers + dehumidifier |
| burst-pipe-water-damage-1.webp | WEAK (downspout) | generated | ACCEPT — frozen burst copper supply pipe, split, icicles, spray |
| burst-pipe-water-damage-3.webp | REPLACE (wood plank) | generated | ACCEPT — gloved hands, wrench on burst copper fitting, brass valve |
| crawl-space-water-damage-3.webp | WEAK (abstract plastic) | generated | ACCEPT — worker unrolling white vapor barrier under joists |
| hardwood-floor-cabinet-drying-2.webp | WEAK (Panasonic + Cyrillic) | Pexels 4030055 | ACCEPT — brand-free US kitchen, white cabinets, wood floor |
| magna-ut-1.webp | WEAK (pillarbox bars) | Pexels 29350636 re-crop | ACCEPT — same photo, native 16:9 crop, no bars |
| magna-ut-2.webp | REPLACE (Wabasha, MN) | generated | ACCEPT — older Utah main street, no legible signage |
| magna-ut-3.webp | WEAK (basement twin) | Pexels 33954649 | ACCEPT — old clapboard house + new wood-frame addition |
| south-salt-lake-ut-2.webp | WEAK (NELSKAMP tiles) | generated | ACCEPT — apartment, water-stained wall, moisture meter, drying gear |
| sewage-backup-cleanup-2.webp | WEAK (storm drain) | generated | ACCEPT — basement floor drain, mop + bucket, water heater |
| swamp-cooler-leak-water-damage-2.webp | WEAK (no cooler) | generated | ACCEPT — ranch house, roof-mounted evaporative cooler |
| swamp-cooler-leak-water-damage-3.webp | REPLACE (Boise window AC) | generated | ACCEPT — side-mount evaporative cooler, water dripping |
| water-heater-leak-cleanup-1.webp | WEAK (Indesit/mirror) | generated | ACCEPT — tank water heater + washer/dryer, puddle, no brands |
| window-well-flooding-3.webp | WEAK (generic houses) | generated | ACCEPT — corrugated window well full of rainwater |

Alt fixes (manifest only, frames verified at full size):
- `ceiling-water-damage-1`: "Man on a ladder…" → "A man sanding a green drywall ceiling with a power sander" (no ladder visible).
- `sewage-backup-cleanup-1`: "spray bottle and a cleaning cloth" → "holding a pump sprayer" (pump sprayer, no cloth).

Per-file detail (old/new md5, aHash, alt, viewed verdict): `qa/images-uiux-fix-body.json`.

## Sourcing
- Real Pexels first. No fitting real photo existed for 12 slots after full searches (basement, crawl space, swamp cooler, window well: only derelict rooms / street floods / AC condensers / window AC units; burst-pipe / water-heater / sewage / magna-2 candidates all viewed and rejected — live on other sites, wrong place, legible brands, wrong subject). Those 12 are generated (novel pixels, viewed at full size, metadata stripped, never claimed as real job photos, no "AI" word anywhere).
- 3 slots real Pexels: 4030055 (hardwood-2), 33954649 (magna-3), 29350636 (magna-1 re-crop of the file's own source).

## Checks (all pass)
- All 15: 1200×675 WebP q82, 0 EXIF/XMP (raw-byte scan), atomic rename via `os.replace` from staged temp names, 0 temp leftovers.
- md5 vs 9,437 live past-site image files (public/images, images, assets/images, out): **0 matches**.
- 16×16 aHash (≤8) vs 3,641 unique live past-site images: **0 matches**.
- Pexels IDs 4030055 / 33954649: 0 hits in all logs + workspace filename search. 29350636: only Midvale's own log.
- Local duplicate check vs all current Midvale body images: 0 matches.
- `lib/pages-data.json` sha256 unchanged: `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`.
- 16 alt updates applied in `lib/body-images.json`; manifest re-read, 0 mismatches.

## Environment notes (owning them plainly)
- The full-corpus hash DB (28,421 files) did NOT complete: VM load ~9.7 (other agents' Playwright work), `/dev/shm` exhaustion broke `multiprocessing.Pool` creation, and `/tmp` writes intermittently failed with EPERM (two background jobs died at the finish line). Reuse checks were re-run against the complete **live-image** set (9,437 files — every image that can actually appear on a site) instead, with md5 via `md5sum` and aHash single-threaded in the foreground. That is the check the numbers above rest on.
- One earlier foreground run reported "0 hits" with an empty aHash dict because paths in `/tmp/live-md5.txt` are workspace-relative (`./…`) and the script ran from `~` — every open failed silently. Caught by the "ahash computed: 0" line, paths fixed, re-run properly (3,641 hashed). The void run is not counted anywhere above.
- magna-ut-1 is 340,588 bytes (detailed trees at q82) vs 62–199 KB for the others; spec is q82, kept as-is.

## Open / not done here
- Nothing unfilled. No live push (local only per task).
