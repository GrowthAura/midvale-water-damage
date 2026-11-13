# F1 Resize Verification — Cycle 1 Image Recovery (Batch 2)

**Date:** 2026-11-13 ~20:40 PKT | **Worker:** Cycle 1 image recovery (finishing interrupted F1 worker)
**Scope:** all 19 card images + all 57 body images in `public/images/`. Heroes NOT resized by this fix (1600x1066, untouched).

## Method
- Before = `qa/opt1-images-backup/cards/` (19 files) + `qa/opt1-images-backup/body/` (57 files) — the F1 worker's own pre-resize backup, read fresh from disk.
- After = current `public/images/cards/` + `public/images/body/`, read fresh from disk.
- Dimensions confirmed with PIL on every file (76/76). Metadata checked with exiftool per file: EXIF + XMP + ICC_PROFILE (76/76).
- Quality: 6 heaviest after-files viewed full-size (see below).

## Totals
| Set | Files | Before | After | Saved |
|---|---|---|---|---|
| Cards (680x383) | 19 | 1454.6 KB | 619.1 KB | 835.5 KB (57.4%) |
| Body (800x450) | 57 | 6015.7 KB | 2760.1 KB | 3255.6 KB (54.1%) |
| **TOTAL** | **76** | **7470.3 KB** | **3379.1 KB** | **4091.1 KB (54.8%)** |

## Dimensions (PIL, 76/76)
- Cards: 19/19 exactly 680x383 (backup originals were 1200x675 / 1200x800).
- Body: 57/57 exactly 800x450 (backup originals all 1200x675).
- 0 dimension mismatches.

## Metadata (exiftool, 76/76)
- EXIF 0, XMP 0, ICC profile 0 on all 76 current files (per-file scan, no hits).

## Quality — full-size views (6 heaviest after-files)
| File | After | Viewed verdict |
|---|---|---|
| body/magna-ut-1.webp | 138.5 KB | Sharp; house, porch, trees, lawn all clean, no blocking or smearing |
| body/mold-remediation-3.webp | 95.3 KB | Sharp; mold staining detail intact, no visible loss |
| body/window-well-flooding-3.webp | 90.2 KB | Sharp; corrugated metal, water droplets, mud all clean |
| body/storm-flood-damage-1.webp | 89.3 KB | Sharp; flooded street, tree reflections clean |
| body/swamp-cooler-leak-water-damage-2.webp | 88.6 KB | Sharp; house, roof cooler, desert hills clean |
| body/cottonwood-heights-ut-2.webp | 85.6 KB | Sharp; aerial city + snow mountains clean |

**Quality verdict: PASS — no visible quality loss in any of the 6 heaviest files viewed full-size.**
Largest single saving: body/magna-ut-1.webp 282,352 -> 138,482 B (-51.0%). No file grew; every file is smaller than its backup.

## Per-file before/after
| File | Before (B) | Before dims | After (B) | After dims | Change |
|---|---|---|---|---|---|
| cards/basement-flooding-cleanup.webp | 85614 | 1200x675 | 36828 | 680x383 | -57.0% |
| cards/burst-pipe-water-damage.webp | 126742 | 1200x675 | 52878 | 680x383 | -58.3% |
| cards/ceiling-water-damage.webp | 28798 | 1200x675 | 13632 | 680x383 | -52.7% |
| cards/commercial-water-damage.webp | 47330 | 1200x675 | 18780 | 680x383 | -60.3% |
| cards/condo-apartment-water-damage.webp | 36132 | 1200x675 | 16224 | 680x383 | -55.1% |
| cards/cottonwood-heights-ut.webp | 174328 | 1200x675 | 72522 | 680x383 | -58.4% |
| cards/crawl-space-water-damage.webp | 99886 | 1200x675 | 40418 | 680x383 | -59.5% |
| cards/emergency-water-extraction.webp | 64750 | 1200x675 | 31114 | 680x383 | -51.9% |
| cards/hardwood-floor-cabinet-drying.webp | 52188 | 1200x675 | 24102 | 680x383 | -53.8% |
| cards/magna-ut.webp | 119830 | 1200x675 | 47324 | 680x383 | -60.5% |
| cards/mold-remediation.webp | 50338 | 1200x675 | 22768 | 680x383 | -54.8% |
| cards/sewage-backup-cleanup.webp | 75256 | 1200x675 | 34790 | 680x383 | -53.8% |
| cards/south-salt-lake-ut.webp | 75946 | 1200x675 | 29172 | 680x383 | -61.6% |
| cards/storm-flood-damage.webp | 103488 | 1200x675 | 44550 | 680x383 | -57.0% |
| cards/swamp-cooler-leak-water-damage.webp | 81220 | 1200x800 | 35278 | 680x383 | -56.6% |
| cards/water-damage-repair.webp | 52342 | 1200x675 | 22938 | 680x383 | -56.2% |
| cards/water-heater-leak-cleanup.webp | 49694 | 1200x800 | 19896 | 680x383 | -60.0% |
| cards/water-leak-detection.webp | 43180 | 1200x800 | 16846 | 680x383 | -61.0% |
| cards/window-well-flooding.webp | 122410 | 1200x675 | 53850 | 680x383 | -56.0% |
| body/basement-flooding-cleanup-1.webp | 73304 | 1200x675 | 36462 | 800x450 | -50.3% |
| body/basement-flooding-cleanup-2.webp | 124220 | 1200x675 | 57956 | 800x450 | -53.3% |
| body/basement-flooding-cleanup-3.webp | 176048 | 1200x675 | 75018 | 800x450 | -57.4% |
| body/burst-pipe-water-damage-1.webp | 142722 | 1200x675 | 70152 | 800x450 | -50.8% |
| body/burst-pipe-water-damage-2.webp | 168234 | 1200x675 | 61604 | 800x450 | -63.4% |
| body/burst-pipe-water-damage-3.webp | 62846 | 1200x675 | 32662 | 800x450 | -48.0% |
| body/ceiling-water-damage-1.webp | 31686 | 1200x675 | 14054 | 800x450 | -55.6% |
| body/ceiling-water-damage-2.webp | 17884 | 1200x675 | 7628 | 800x450 | -57.3% |
| body/ceiling-water-damage-3.webp | 40630 | 1200x675 | 18564 | 800x450 | -54.3% |
| body/commercial-water-damage-1.webp | 156612 | 1200x675 | 80694 | 800x450 | -48.5% |
| body/commercial-water-damage-2.webp | 62268 | 1200x675 | 29340 | 800x450 | -52.9% |
| body/commercial-water-damage-3.webp | 122818 | 1200x675 | 61396 | 800x450 | -50.0% |
| body/condo-apartment-water-damage-1.webp | 93548 | 1200x675 | 30458 | 800x450 | -67.4% |
| body/condo-apartment-water-damage-2.webp | 55432 | 1200x675 | 23634 | 800x450 | -57.4% |
| body/condo-apartment-water-damage-3.webp | 72234 | 1200x675 | 25876 | 800x450 | -64.2% |
| body/cottonwood-heights-ut-1.webp | 96800 | 1200x675 | 39034 | 800x450 | -59.7% |
| body/cottonwood-heights-ut-2.webp | 149004 | 1200x675 | 85596 | 800x450 | -42.6% |
| body/cottonwood-heights-ut-3.webp | 113292 | 1200x675 | 47248 | 800x450 | -58.3% |
| body/crawl-space-water-damage-1.webp | 130854 | 1200x675 | 57568 | 800x450 | -56.0% |
| body/crawl-space-water-damage-2.webp | 90868 | 1200x675 | 41244 | 800x450 | -54.6% |
| body/crawl-space-water-damage-3.webp | 97084 | 1200x675 | 48478 | 800x450 | -50.1% |
| body/emergency-water-extraction-1.webp | 122270 | 1200x675 | 59898 | 800x450 | -51.0% |
| body/emergency-water-extraction-2.webp | 41996 | 1200x675 | 17620 | 800x450 | -58.0% |
| body/emergency-water-extraction-3.webp | 99630 | 1200x675 | 47186 | 800x450 | -52.6% |
| body/hardwood-floor-cabinet-drying-1.webp | 167522 | 1200x675 | 61118 | 800x450 | -63.5% |
| body/hardwood-floor-cabinet-drying-2.webp | 85948 | 1200x675 | 40268 | 800x450 | -53.1% |
| body/hardwood-floor-cabinet-drying-3.webp | 36528 | 1200x675 | 15776 | 800x450 | -56.8% |
| body/magna-ut-1.webp | 282352 | 1200x675 | 138482 | 800x450 | -51.0% |
| body/magna-ut-2.webp | 150756 | 1200x675 | 67560 | 800x450 | -55.2% |
| body/magna-ut-3.webp | 170946 | 1200x675 | 74062 | 800x450 | -56.7% |
| body/mold-remediation-1.webp | 157214 | 1200x675 | 83490 | 800x450 | -46.9% |
| body/mold-remediation-2.webp | 28910 | 1200x675 | 11708 | 800x450 | -59.5% |
| body/mold-remediation-3.webp | 179332 | 1200x675 | 95264 | 800x450 | -46.9% |
| body/sewage-backup-cleanup-1.webp | 44776 | 1200x675 | 20798 | 800x450 | -53.6% |
| body/sewage-backup-cleanup-2.webp | 69494 | 1200x675 | 35944 | 800x450 | -48.3% |
| body/sewage-backup-cleanup-3.webp | 181866 | 1200x675 | 72220 | 800x450 | -60.3% |
| body/south-salt-lake-ut-1.webp | 108834 | 1200x675 | 53034 | 800x450 | -51.3% |
| body/south-salt-lake-ut-2.webp | 102594 | 1200x675 | 48094 | 800x450 | -53.1% |
| body/south-salt-lake-ut-3.webp | 51328 | 1200x675 | 26064 | 800x450 | -49.2% |
| body/storm-flood-damage-1.webp | 185028 | 1200x675 | 89322 | 800x450 | -51.7% |
| body/storm-flood-damage-2.webp | 54058 | 1200x675 | 21996 | 800x450 | -59.3% |
| body/storm-flood-damage-3.webp | 178376 | 1200x675 | 74544 | 800x450 | -58.2% |
| body/swamp-cooler-leak-water-damage-1.webp | 133062 | 1200x675 | 60240 | 800x450 | -54.7% |
| body/swamp-cooler-leak-water-damage-2.webp | 160428 | 1200x675 | 88620 | 800x450 | -44.8% |
| body/swamp-cooler-leak-water-damage-3.webp | 133710 | 1200x675 | 61326 | 800x450 | -54.1% |
| body/water-damage-repair-1.webp | 17396 | 1200x675 | 7106 | 800x450 | -59.2% |
| body/water-damage-repair-2.webp | 59422 | 1200x675 | 23838 | 800x450 | -59.9% |
| body/water-damage-repair-3.webp | 47496 | 1200x675 | 16028 | 800x450 | -66.3% |
| body/water-heater-leak-cleanup-1.webp | 71862 | 1200x675 | 32860 | 800x450 | -54.3% |
| body/water-heater-leak-cleanup-2.webp | 86122 | 1200x675 | 43322 | 800x450 | -49.7% |
| body/water-heater-leak-cleanup-3.webp | 164728 | 1200x675 | 55822 | 800x450 | -66.1% |
| body/water-leak-detection-1.webp | 65958 | 1200x675 | 30960 | 800x450 | -53.1% |
| body/water-leak-detection-2.webp | 157424 | 1200x675 | 76634 | 800x450 | -51.3% |
| body/water-leak-detection-3.webp | 85384 | 1200x675 | 39702 | 800x450 | -53.5% |
| body/window-well-flooding-1.webp | 99032 | 1200x675 | 42332 | 800x450 | -57.3% |
| body/window-well-flooding-2.webp | 117484 | 1200x675 | 58258 | 800x450 | -50.4% |
| body/window-well-flooding-3.webp | 182434 | 1200x675 | 90154 | 800x450 | -50.6% |

## Verdict
**F1 RESIZE VERIFIED COMPLETE — PASS.** 76/76 dims exact, 76/76 metadata clean, weight 7,649,560 B -> 3,460,226 B (-54.8%), quality PASS on full-size views.

## Addendum (post-verification swap, ~21:05 PKT)

body/magna-ut-1.webp was opportunistically replaced AFTER this verification by Pexels 5587966 (Utah aerial, see qa/opt1-fix-heroes.md): same 800x450 dims, 145,698 B (was 138,482 B, +7,216 B). The totals above are therefore pre-swap for that one file; all other 75 rows stand as verified.
