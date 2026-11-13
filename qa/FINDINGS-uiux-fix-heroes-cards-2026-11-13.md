# Midvale UT — Heroes + Cards Image Fix (Stage 1 UI/UX round)

- **Date:** 2026-11-13
- **Worker:** image fix worker (heroes + cards)
- **Fix list source:** `qa/uiux-images-heroes-cards-2026-11-13.md` (9 WEAKs, 0 REPLACE)
- **Result: 9/9 replaced, 0 unfilled.**
- **Scope kept:** ONLY `public/images/heroes/` and `public/images/cards/` touched. `lib/pages-data.json` sha256 verified unchanged after install: `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`.
- **Detail record:** `qa/images-uiux-fix-heroes-cards.json` (per-file source, checks, viewed verdict).

## Per-file outcome

| File | Source | What changed |
|---|---|---|
| `heroes/water-damage-repair.webp` | Pexels 5493667 | Worker in hard hat + respirator fitting new trim, trowel in hand (portrait cropped to 1600x1066). Repair action replaces the empty finished room. Minor nit: lower trowel hand slightly cut at bottom edge. |
| `heroes/upstairs-unit-leak-who-pays-utah.webp` | Generated | Upstairs bathroom, water pooling on tile from toilet base, damp wall, towels. Distinct source angle; bucket motif gone. No fitting real photo on Pexels (faucet drips only). |
| `heroes/basement-flooding-spring-snowmelt-utah.webp` | Generated | Meltwater pooling against the concrete foundation outside, dirty snow banks, downspout dripping, snowy foothills. No fitting real photo on Pexels (icicles / vintage garden pumps only). |
| `heroes/basement-flooding-cleanup.webp` | Generated (edit of existing hero) | Same wood-panel flooded basement, worker lifting soaked carpet; pump hose now leads up and OUT through the basement window, jet spraying outside. NOTE: the generator rebuilt the scene rather than pixel-preserving the original; composition is equivalent and the logic error is fixed. |
| `heroes/disclaimer.webp` | Pexels 8297022 | Neutral desk: laptop (blank screen), calculator, folders, papers; no people, no legible text — same register as privacy/terms heroes. Rejected: 5520296 (legible CONTRACT text), 8036339 (legible manuscript), 8927688 (legible 1040 + euro note), 8296951 (Cyrillic keyboard). |
| `cards/burst-pipe-water-damage.webp` | Generated | Split copper pipe in opened wall cavity spraying water, wet studs, torn drywall, zero ice. No fitting real photo on Pexels (outdoor dripping taps only). |
| `cards/cottonwood-heights-ut.webp` | Pexels 34409157 | Big Cottonwood Canyon winding road, autumn foliage, rocky cliffs; photo location metadata is Cottonwood Heights, Utah. Distinct from the snowy-street hero. |
| `cards/magna-ut.webp` | Pexels 15811732 | Residential street of brick homes, snowy Oquirrh foothills at sunrise. Distinct from the main-street storefront hero. |
| `cards/south-salt-lake-ut.webp` | Pexels 20890902 | UTA TRAX Blue Line train on a snowy street. Distinct from the hero; the only legible text is the train's own "BLUE LINE" sign + UTA livery (the place cue itself). |

## Checks (all 9)

- **Dimensions/format:** heroes 1600x1066, cards 1200x675, WebP q82 — verified on installed files.
- **Metadata:** 0 EXIF/XMP/ICC on every file (single VP8 chunk verified). No "AI" word in any filename/alt/metadata. Generated images are not presented as real job photos.
- **Reuse — md5:** 0 exact matches vs this site (107 files) and vs 5,510 past-site image files.
- **Reuse — 16x16 aHash:** min distances 37–85/256 past-site, 58–99/256 this-site, except two sub-25 values adjudicated DIFFERENT by full-size view: Magna card 18 vs Plano3 `texas-home-33404353` (house under wood-frame construction on a dirt lot) and 23 vs this-site `body/cottonwood-heights-ut-3` (grey overcast cityscape with church + scaffolding). Both are shared sky/ground banding at 16x16, not same content.
- **Pexels IDs:** all 5 used IDs checked free against 491 IDs grepped from past-site logs; one drywall candidate (6474308) was found USED and not taken.
- **Viewed:** every replacement viewed at full size (source + final processed file) before install — topic/place fit, no legible text/branding/logos (except the TRAX livery noted above), no AI tells that break the scene.
- **Install:** processed to temp file, copied to `<target>.new-tmp`, atomic `os.replace`, md5 re-verified after install, no temp files left.

## Notes / honest caveats

- The basement-cleanup "edit" is a regenerated equivalent scene, not the original pixels with only the hose changed — the generator rebuilt the room. The brief's elements (wood-panel basement, worker + carpet, pump discharging out) are all present and the logic error is gone.
- The repair hero's lower trowel hand is slightly cut at the bottom edge of the crop; the trim-fitting action still reads clearly.
- Pexels photo pages were reached via search (pexels.com main site is blocked from curl in this VM; images.pexels.com CDN downloads fine). No Pexels API key exists here; IDs were taken from search-result pages.
