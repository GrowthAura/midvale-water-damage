# Agent B — Images: evidence (10x nav-footer round, 2026-11-16)

Coordinator's synthesis of Agent B (killed by VM restart 2026-11-16 01:05 PKT),
Agent B-finish (killed by VM restart/drain 2026-11-16 01:58 PKT), and my own
full-size viewed-pixel adjudication of every flagged pair. No `agent-B-images.md`
was written by either agent — this file is the record.

## Verdict: NOT READY — P1 × 4 reused images (see §3)

- Inventory / slot-fit / metadata: PASS (see §1)
- Reuse net: CONTROL PASSED, md5 cross-site 0 — but **4 served body images are the
  SAME photo as another live site**, confirmed by viewed pixels (see §3)
- Key images viewed: PASS (see §5)
- 38 reprobe "404"s: checker bug, all resolve (see §6)
- Hero aspect flags (67): expected cover behaviour, subjects visible (see §7)

## 1. Inventory (Agent B, `agent-B-inventory.json`)

- File counts identical across trees: public 329 / out 329 / out-cloudflare 329.
  md5 mismatch across trees: 0. Extra/missing in either export: 0.
- Slots present: body-base 57 + body-400 57, card-base 19 + card-340 19,
  hero-base 31 + hero-800 31 + hero-m 31, hero-mid/mid600/mid700 28 each.
- Total image bytes 16,596,174 (~16.6 MB / 329 files).
- Metadata: 0 hits across all 329 files — no EXIF/XMP/ICC chunks, no PIL EXIF/ICC
  (webp chunk + VP8X-flag scan, `agent-B-inventory.py`).
- Overweight (>200 KB soft cap): 1 file — `heroes/basement-flooding-spring-snowmelt-utah.webp`,
  215,212 B, 1600×1066. **P3** (carried to the fix agent for recompression).
- basement-3 (`body/basement-flooding-cleanup-3.webp`, the aerial photo — owner's call
  still open): sha256 `3c3282f408f8…` — **unchanged**.

## 2. Reuse net (Agent B-finish, `agent-B-reuse.json`, `agent-B-corpus-hashes.jsonl`)

- Corpus: **12,211 files hashed** (md5 + aHash8 + aHash16), including export dirs
  (`*gh-pages*/images`, `*/out*/images`, `*/export*/images`) plus a Pexels-ID
  filename net across `~/workspace` (see §4).
- Targets: 107 served images (329 served files incl. variants).
- **CONTROL PASSED** (required proof the corpus works): the bad Cycle-4 mold install
  (Pexels 4176541) was rebuilt and flags a8 = 0 / a16 = 0 vs the Chesterfield live
  file `chesterfield-gh-pages/images/chesterfield-mold-remediation-mold-filtration-unit.webp`
  (recon sha256 matches expected `73a15608…`).
- md5 hits: 329 — **0 cross-site** (all hits are Midvale's own copies in
  `midvale-gh-pages/`, `midvale-cloudflare-pages/`, `tmp-midvale-c4b-build/`).
- aHash8 ≤ 12 flags: 6,610 (mostly self-matches + noise). a16 ≤ 28 true cross-site
  pairs: 62 — **every one adjudicated by full-size viewed pixels** (§3).
- `mold-remediation-2` check: current file sha = expected Pexels 4098781 sha
  (`78f9d749…`) — correct file installed, no Cycle-4 leak repeat.
- `repair-1` cross-check vs Apopka `process-8-repairs-apopka.jpg`: a8 19 / a16 76–79 —
  different photos.
- Card-vs-own-hero (Stage-5 crops): south-salt-lake-ut a8 6 / a16 29, magna-ut a8 6 /
  a16 29 — consistent with center crops of their own heroes (§5).

## 3. Adjudication of the 62 a16 ≤ 28 pairs (coordinator, viewed pixels)

Side-by-side shots: `shots/agent-B-adj-01.png` … `agent-B-adj-62.png`.
Method per the standing rule: hashes are supporting evidence only; the viewed
pixels decide. Aspect-matched MAD (same photo ≈0.5–3, different 15+) used as
supporting evidence on the remainder.

### CONFIRMED REUSE — P1 × 4 files

| # | Midvale file (served) | a8/a16 | Same photo live on | Proof |
|---|---|---|---|---|
| 1 | `body/emergency-water-extraction-2.webp` (/emergency-water-extraction slot 2, Pexels 5691510) | 0/0 | Chesterfield `chesterfield-emergency-water-extraction-kitchen-floor-wand.webp`, referenced by `chesterfield-gh-pages/emergency-water-extraction.html` | adj-01: identical room, green walls, same yellow wet-vac in the same position; framing differs (ours tighter crop) |
| 1b | same file | 3/6 | Tulsa Repair `services-water-mitigation-tulsa-water-damage-repair.webp` (site/out + gh-pages-staging service-area pages) | adj-03: same wet-vac photo, wider crop + blue water-drop watermark |
| 2 | `body/mold-remediation-3.webp` (/mold-remediation slot 3, Pexels 7434331) | 0/1 | Lancaster `mold-removal-lancaster-ca-sec1.webp`, referenced by `out/mold-removal-lancaster-ca/index.html` | adj-02: identical black-mold wall texture, same stain shapes throughout |
| 3 | `body/ceiling-water-damage-3.webp` (/ceiling-water-damage slot 3, Pexels 36035072) | 6/20 | Boynton Beach `room-renovation-tiles-1200.jpg` (+600w), referenced by `publish-pages/repair-rebuild/index.html` | adj-23: same renovation room — ladder, table, tile strips, ceiling curve, floor sheeting all identical; MAD 9.73 on the 600w variant |
| 4 | `body/mold-remediation-1.webp` (/mold-remediation slot 1, Pexels 17401392) | 7/28 | Boynton Beach `mold-wall-growth-1200.jpg` (+600w), referenced by `publish-pages/mold-after-leak/index.html` + `ac-leak/index.html` | adj-60: same moldy white block wall — identical mold bands, stain pattern, crack; MAD 15.52 on the 600w variant |

Notes:
- All 4 files exist in BOTH exports (`out/` + `out-cloudflare/`) and are referenced
  by served Midvale HTML (`emergency-water-extraction.html`, `mold-remediation.html`,
  `ceiling-water-damage.html`, `index.html`).
- a16 = 28 for #4 proves the Cycle-4 lesson again: heavy crops push same-photo pairs
  to a16 17–37 — a <25 hash threshold alone would have MISSED it. Visual adjudication
  caught it.
- #1 is the same stock photo live on THREE sites (Midvale + Chesterfield + Tulsa Repair).

### FALSE POSITIVES — 58 pairs, all refuted by viewed pixels

- adj-04 (a16 9): `cottonwood-heights-ut-3` (snowy SLC valley) vs Tulsa EMD
  `bixby-ok-desktop-crop-bottom.png` — the corpus file is a QA page screenshot
  (footer + area cards), not a photo. Same pattern for all 7 screenshot pairs
  (a16 9/19/25/27) — aHash noise from large pale areas. Not a reuse.
- adj-11 (a16 13): `cottonwood-heights-ut-1` (snowy Wasatch) vs Lancaster
  `93536-sec2` (Joshua-tree desert) — different place, different photo.
- adj-12 (a16 14): `cottonwood-heights-ut-3` vs Plano3 `texas-home-33404353`
  (house-framing construction site) — different photo.
- adj-14 (a16 16): `cottonwood-heights-ut-3` vs Tulsa `burst-pipe-geyser`
  (street water geyser) — different photo.
- Remaining 27 distinct non-screenshot pairs: aspect-matched MAD 28.6–92.4
  (different-photo band), subjects manifestly different (snowy valley vs ceiling
  stain / street / tanks / desert / construction). No further same-photo candidate.

## 4. Pexels-ID filename net (coordinator, 2026-11-16 ~07:05 PKT)

Midvale IDs from `qa/images-design-g*.json` / `qa/images-fill.json`:
- 5691510 (emergency-water-extraction-2): no filename/log hits outside Midvale
  (counterparts renamed — visual + a16 evidence stands).
- 7434331 (mold-remediation-3): `sb-cand/px-7434331.jpg` (unserved San Bruno
  candidate) + Lancaster `work/img-scout/{harvest,pool,pool_audit}.json`,
  `work/qa3-polish-log.md`, `work/qa3-image-manifest.md` — **corroborates** the
  Lancaster reuse (same Pexels ID in Lancaster's pool).
- 36035072 (ceiling-water-damage-3): no hits outside Midvale (Boynton renamed it).
- 17401392 (mold-remediation-1): Lancaster `work/img-scout/{harvest,pool,pool_audit}.json`,
  `work/qa3-staging/harvest-mold-rem.json` + Boynton `BOYNTON-FIX2-AUDIT.md` —
  **corroborates** the Boynton reuse.

## 5. Key images viewed (coordinator, full-size shots in `shots/`)

- Cycle-1 new heroes (3): `heroes/disclaimer.webp` (worker with moisture meter on
  peeling water-stained wall — topical, no brands) PASS;
  `heroes/upstairs-unit-leak-who-pays-utah.webp` (ceiling leak dripping onto sofa —
  perfectly topical) PASS; `heroes/water-damage-repair.webp` (clean restored US home
  interior, wood floors — no damage visible, fits a repair page) PASS.
- `body/mold-remediation-2.webp` (PPE worker + respirator, topical, no brands) PASS.
- `body/sewage-backup-cleanup-3.webp` (Pexels 4239074 — gloved hand plunging a toilet,
  topical, no brands) PASS.
- Stage-5 card crops: `cards/south-salt-lake-ut.webp` + `cards/magna-ut.webp` are
  proper center crops of their own heroes (wet dusk streets, Wasatch/mountains) PASS.
- `body/basement-flooding-cleanup-3.webp` (aerial) viewed; sha unchanged (§1).

## 6. The 38 reprobe "404"s — checker bug, resolved

`agent-B-reprobe-resolution.json` (38/38): `file_out` true, `file_cf` true,
`http_correct` 200, `http_double_prefix` 404. The original reprobe built the URL as
PAGES-base + src where src already contains the `/midvale-water-damage/` basePath
prefix — double prefix → 404. All 38 files exist and resolve 200 at the correct URL.
`agent-B-cf-resolution.json` (16/16): all spot-checked images 200 on the Cloudflare build.

## 7. Hero aspect flags (67) — expected behaviour, not defects

All 67 flags are hero images. The hero is an `object-fit:cover` background filling a
variable-height section, so file aspect ≠ box aspect by design (dev range 14.22–131.36%
in the original render probe). What matters is subject visibility: 21 hero renders
measured (`agent-B-view-hero2.json`: 12 @1440, 9 @390; box 1440×414.5 @1440, natural
1600×1066), subjects visible in the renders viewed. Cycles 2/3 already measured visible
fraction @390 (mean 0.749). No hero is broken, cropped blind, or subject-less.

## 8. What the fix agent must do (spawned 2026-11-16 ~07:15 PKT)

Replace the 4 files in §3 with fresh Pexels photos (new IDs, new filenames, 800w +
400w variants, metadata-stripped, alts rewritten to match the new photos), recompress
the 215 KB hero to ≤200 KB, rebuild BOTH exports, re-verify (31/31 + the 4 slots at
1440/390 + reuse net on the 4 new files). Report: `qa/10x-nav-footer-2026-11-16/agent-B-fix.md`.
If no fitting fresh photo exists for a slot, leave the old file and report it as
unfixable — never force a wrong photo.
