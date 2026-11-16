# Agent B image fix — Midvale UT (10x nav-footer round, 2026-11-16)

## FINAL STATUS (2026-11-16 ~02:30 PKT): 2 of 4 replaced + hero recompressed; 2 mold slots UNFIXABLE from Pexels (old files restored byte-identical)
- `lib/pages-data.json` sha256: `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` (verified unchanged throughout — last check after mold restore).
- Old files backed up to `qa/10x-nav-footer-2026-11-16/replaced/` (8 files: 4 base + 4 `-400` variants).
- Uncommitted 4-file diff saved to `qa/10x-nav-footer-2026-11-16/uncommitted-4files.diff` (145 lines, app/not-found.tsx, components/site.tsx, lib/content.ts, lib/links.tsx) — must be preserved across the Cloudflare temp-edit build.
- All 4 slots are 800x450 (16:9) base + 400w variant. Slot renders 400x225 @1440.
- Pexels search pages return 403 from VM curl (known); searches read via browser fetch route; downloads via images.pexels.com CDN work from VM.

## Per-file results

### SLOT 1 — /emergency-water-extraction slot 2 (afterH2 2, sticky) — REPLACED
- OLD: `public/images/body/emergency-water-extraction-2.webp` (+ `-400`), Pexels **5691510**, alt "A yellow wet/dry vacuum standing on a wooden floor in a room under renovation." BANNED — same photo live on Chesterfield emergency-water-extraction.html AND Tulsa Repair service-area pages. Deleted from `public/images/body/` (backup in `qa/.../replaced/`).
- NEW: `public/images/body/water-extraction-yellow-wet-dry-vacuum.webp` (800x450, 21,352 B) + `water-extraction-yellow-wet-dry-vacuum-400.webp` (400x225, 8,672 B), VP8-only chunks (metadata stripped). Pexels **6196579**. Source: https://images.pexels.com/photos/6196579/pexels-photo-6196579.jpeg (photo page: pexels.com/photo/6196579 — slug TBD). Crop: portrait 1200x1800, band y200–875 (first crop y150–825 cut the hose off; re-cropped and re-viewed).
- Viewed: yellow wet/dry vac body + corrugated hose on a sunlit tiled floor; US home interior; no legible brand. New alt: "A yellow wet/dry vacuum with a hose on a sunlit tiled floor." (in `lib/body-images.json`).
- Reuse net (final, fresh disk reads on installed file): md5 0 hits; **0** a8<=12 flags; closest cross-site a16 **68** (Plano `wet-attic-reinsulate-split-480.webp`, clearly different); own-site closest a16 82; filename scan `*6196579*` 0 hits anywhere in ~/workspace; ID in 0 corpus paths. CLEAN.

### SLOT 2 — /mold-remediation slot 1 (afterH2 1, split) — UNFIXABLE from Pexels (old file restored)
- OLD: `public/images/body/mold-remediation-1.webp` (+ `-400`), Pexels **17401392**, alt "Green and black mold streaks across a white painted block wall". BANNED — same photo live on Boynton Beach mold-after-leak / ac-leak pages.
- RESTORED byte-identical from `qa/.../replaced/`: base sha256 `fe5f076f615f50af393f5766a01be81039515c2dc65bdaf617d708876b490dfd`, -400 sha256 `6359285936410bbc6a03e424ed09fd340280956ce39405254878c5c91d4c713e`. `lib/body-images.json` entry reverted to the original src + alt (no net diff vs HEAD for this slot).
- Why unfixable: 9 Pexels searches run ("mold on wall", "black mold", "mold on drywall", "mildew", "mold removal", "black mould", "mold in bathroom", "mold on wall" variants). Every genuinely moldy-interior-wall photo on Pexels found is already used somewhere in the portfolio: 17401392 (Boynton), 7434331 (Lancaster), 9127236 (Plano — round-1 pick, rejected a8 1/a16 24, pixel-identical), 7506161 (Midvale's own swamp-cooler-1 — round-1 pick, rejected a8 0/a16 7–8, pixel-identical), 18063447 (Plano `indoor-mold-18063447.webp`, a16 2/a8 1). All other clean candidates viewed and rejected as NOT mold: peeling paint (36251228, 30397827), exterior lichen/moss (6141203, 7599719), stone/grunge textures (7597726, 36251226, 15220749, 12425952), COVID-fumigation PPE shots (4176xxx series — avoided entirely; 4176541 is the bad Cycle-4 photo itself), abandoned EU bathrooms, generic cleaning. The 2 work-shot candidates (6474117, 5499416) were also rejected by the net (same photo as biohazard-cleanup-oklahoma / Chesterfield mold-drywall-removal). No fitting fresh photo exists on Pexels. USER'S CALL: non-Pexels source, real job photos, or accept the reuse.

### SLOT 3 — /mold-remediation slot 3 (afterH2 13, split) — UNFIXABLE from Pexels (old file restored)
- OLD: `public/images/body/mold-remediation-3.webp` (+ `-400`), Pexels **7434331**, alt "Black mildew stains streaking down a light-coloured wall". BANNED — same photo live on Lancaster mold-removal pages; also in Lancaster's img-scout pool.
- RESTORED byte-identical from `qa/.../replaced/`: base sha256 `e639c308e3d9a0d44fe3216b800454a0a721e75839f953809b83117352b5be84`, -400 sha256 `b57f04a5b0d8c6b023a8dc7e438d3c1f08d29a4e4c161884709966bcc29aa575`. `lib/body-images.json` entry reverted to the original src + alt (no net diff vs HEAD for this slot).
- Why unfixable: same 9 searches as slot 2 — same exhausted pool (see slot 2). No fitting fresh mold-streak wall photo exists on Pexels. USER'S CALL: non-Pexels source, real job photos, or accept the reuse.

### SLOT 4 — /ceiling-water-damage slot 3 (afterH2 7, split) — REPLACED
- OLD: `public/images/body/ceiling-water-damage-3.webp` (+ `-400`), Pexels **36035072**, alt "Room under renovation with a stepladder, drop cloths on the floor and a curved ceiling detail". BANNED — same photo live on Boynton Beach repair-rebuild page. Deleted from `public/images/body/` (backup in `qa/.../replaced/`).
- NEW: `public/images/body/ceiling-water-damage-renovation-stepladder.webp` (800x450, 31,960 B) + `ceiling-water-damage-renovation-stepladder-400.webp` (400x225, 12,850 B), VP8-only chunks (metadata stripped). Pexels **7217923**. Source: https://images.pexels.com/photos/7217923/pexels-photo-7217923.jpeg (photo page: pexels.com/photo/7217923 — slug TBD).
- Viewed: paint-splattered wooden stepladder + drop cloths + paint tray/can, white walls, wood floor; US home interior; no legible brand. New alt: "A paint-splattered wooden stepladder beside drop cloths, a paint tray and a paint can on a wooden floor in a room under renovation." (in `lib/body-images.json`).
- Reuse net (final, fresh disk reads on installed file): md5 0 hits; closest cross-site a16 **61** (Tulsa `carpet-pad-removal-480.webp`, clearly different); 0 flags a8<=12 with a16<=40; own-site closest a16 76; filename scan 0 hits; rg content grep 0 hits. CLEAN.

### HERO — recompressed (same photo, same filename)
- `public/images/heroes/basement-flooding-spring-snowmelt-utah.webp`: 215,212 B -> **198,260 B** (q68, 1600x1066, VP8-only, EXIF-stripped). Viewed original vs q68 full-size — no visible loss.
- Reuse net after recompression: md5 0 hits; closest a16 **0** entries are ALL Midvale's own export dirs (`midvale-cloudflare-pages/`, `midvale-gh-pages/`, `tmp-midvale-c4b-build/` — corpus leaked Midvale's own exports; same photo, same site, expected); **closest NON-Midvale hero match: none in top-5; 0 non-Midvale flags with a16<=40**. CLEAN (no cross-site reuse introduced).

## Round-1 rejections (reuse net + full-size viewed-pixel adjudication — all CONFIRMED same photo)
- **3616735 (ext)**: a8 0 / a16 0 vs Chesterfield `chesterfield-flooded-basement-cleanup-basement-drying-setup.webp` (viewed pixel-identical); Plano live `wet-dry-vacuum-3616735.webp` (filename = ID). DELETED.
- **9127236 (mold-1)**: a8 1 / a16 24 vs Plano `mold-wall-9127236.webp` (viewed pixel-identical crack + green streaks); also in Lancaster img-scout pool. DELETED.
- **7506161 (mold-3)**: a8 0 / a16 7–8 vs Midvale's OWN `swamp-cooler-leak-water-damage-1.webp` (viewed pixel-identical — 7506161 was already installed on this site as swamp-cooler-1); also in Lancaster img-scout pool. DELETED.
- **CONTROL PASSED** (final run): recon file a8 0 / a16 0 vs Chesterfield live 4176541 file. Fresh CDN 4176541 download flags a8 8 / a16 33 (Chesterfield install is a crop of the full photo; recon = the actual rebuilt install, 0/0).

## Other pre-check rejections (hash/ID net, before install)
- **38325 (ext)**: a16 0 / a8 0 vs Plano `wet-vacuum-carpet-38325.webp` (ID in filename).
- **18063447 (mold backup)**: a16 2 / a8 1 vs Plano `indoor-mold-18063447.webp` (ID in filename).
- **6474117 (mold work shot)**: a16 0 / a8 0 vs biohazard-cleanup-oklahoma technician photo + Plano `respirator-containment-6474117.webp`.
- **5499416 (mold work shot)**: a16 12 / a8 2 vs Chesterfield `chesterfield-mold-remediation-mold-drywall-removal.webp` — viewed side-by-side: SAME PHOTO (same worker, blue respirator + goggles, red spray gun, same pose; Chesterfield's is a wider crop).
- **3616746 (ext backup, same shoot as banned 3616735)**: closest a16 25 / a8 4 vs Tulsa `bixby-ok-red-clay-soil-road.jpg` — viewed: a red dirt road, hash coincidence; substantively hash-clean but same shoot/room/vac as banned 3616735 — held as backup only, not used.
- Pixel-rejected (no mold visible / wrong subject / wrong country): 15220749, 12425952, 7597726, 36251228, 30397827, 6141203, 36251226, 15798786, 3616739, 7937304, 30482688, 36035073 (same shoot as banned 36035072), all 5691xxx series (same series as banned 5691510), 6196579's siblings 6195xxx red-coveralls shots (Acworth uses red-coveralls photos; avoid).
- rg content grep for the 4 round-1 IDs across ~/workspace *.json/*.md returned 0 hits — the logs don't carry these IDs; the FILENAME scan + hash net caught them. Both nets mandatory.
- **PROCESS LESSON (mine)**: round-1 picks were chosen from search titles + viewed pixels WITHOUT nets first; the nets then killed 3/4 after install. Round 2: ID grep + hash pre-check on EVERY candidate BEFORE install.

## Corpus note
- `qa/10x-nav-footer-2026-11-16/agent-B-corpus-hashes.jsonl` (12,211 files; 12,210 usable — 1 None-hash entry). It leaked Midvale's own export dirs (`midvale-cloudflare-pages/`, `midvale-gh-pages/`, `tmp-midvale-c4b-build/`) because they don't contain the string `midvale-water-damage`, so the exclusion missed them — closest matches against those dirs are the site's own files, not cross-site reuse. Adjudicate cross-site matches only on non-Midvale paths.

## Git state (uncommitted, nothing committed)
- `M lib/body-images.json` — 4 lines (ext src+alt, ceiling src+alt; mold entries = original, no net diff).
- `M public/images/heroes/basement-flooding-spring-snowmelt-utah.webp` — recompressed.
- `D` old ext-2 + ceil-3 (base + -400). `??` new yellow-vac + stepladder (base + -400).
- Mold files: NOT in git status (restored byte-identical to HEAD).
- Pre-existing uncommitted: `M app/not-found.tsx, components/site.tsx, lib/content.ts, lib/links.tsx` (P3 console-404 fix + comment fixes) — preserved in `qa/.../uncommitted-4files.diff`.

## VERIFICATION — DONE (2026-11-16 ~03:00 PKT)
### Rebuilds (both exit 0)
- Pages build (`NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage/`, basePath /midvale-water-damage, output `out/`): exit 0, log `qa/.../pages-build.log`.
- Cloudflare build (`NEXT_PUBLIC_SITE_URL=https://www.waterdamagerestorationmidvale.us`, no basePath, output `out-cloudflare/`): exit 0, log `qa/.../cf-build.log`. Temp edits applied + restored; `next.config.mjs` verified == Pages config after; `lib/content.ts` uncommitted hunk re-applied from saved diff (verified byte-identical: `git diff -- lib/content.ts` shows only the original comment fix). Full uncommitted diff intact (43 insertions / 30 deletions across the same 5 files). Nothing committed, no token used, nothing pushed/deployed.
- `lib/pages-data.json` sha256 still `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` (checked after both builds).

### Route + file checks (verify-export.py; logs `qa/.../verify-pages.log`, `verify-cf.log`)
- Pages: **31/31 routes 200 + H1==1, 0 FAILs**. CF: **31/31 routes 200 + H1==1, 0 FAILs**.
- New files 200 in both exports (base + -400 for both replacements; recompressed hero 200). Old body files 404 in both exports (0 exact `images/body/...` refs, 0 stale files on disk in either export — the two homepage grep hits were the card image `images/cards/ceiling-water-damage-340.webp`, a substring false positive). Restored mold files 200 in both exports. Slot HTML references correct on all 3 routes in both exports.

### Real-browser render (Playwright, headless Chromium, Pages server 8908; scripts `qa/.../render-check.py`, `slot-check.py`)
- All 3 routes: H1==1, scrollW == clientW (no horizontal overflow) at 1440 and 390, **0 console errors** on every route/width.
- Slot loads (after scrollIntoView — all body images are `loading="lazy"`, so below-fold slots only load on scroll; this is by design, not a defect): ext yellow-vac 400x225 @1440 / 351x197 @390; ceiling stepladder 400x225 / 351x197; mold-1 + mold-3 (restored) 400x225 / 351x197 — all `complete: True`, currentSrc = the -400 variant, 0 failed/4xx requests.
- Viewed screenshots (`qa/.../shots/agent-B-render/slot-*.png`): yellow wet/dry vac + hose renders beside "Water Removal Midvale Jobs" (1440 + 390); paint-splattered stepladder + drop cloths renders beside "Ceiling Leaks by Midvale Home Type" (1440 + 390). Both correct slots, no overflow, no broken images.

## Still to do
- NOTHING on my side. Tree is ready for the independent re-verifier. Open user calls: the 2 mold slots (non-Pexels source / real job photos / accept the reuse of 17401392 + 7434331).
