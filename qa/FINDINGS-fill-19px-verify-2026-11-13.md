# FINDINGS — Midvale fill + 19px round, independent verification

**Date:** 2026-11-13 (PKT, overnight run). **Verifier:** independent; nothing from either worker taken on trust — every number below was re-measured fresh by my own scripts on a fresh export I ran myself.
**Scope:** local only. No push, deploy, token, DNS, or MEMORY.md edits. No site source, CSS, or manifest file was modified. (No fix was needed — see broken-image adjudication.)

## Verdict

**PROBLEMS 0 — build is READY for re-push.** One P3 environment note (footer Google Maps embed fails only inside this VM, which has no route to google.com) and two non-problem notes (eyebrow/breadcrumb chrome below 19px; my own script error, recovered). Details below.

## PROBLEMS

### P1 — none
### P2 — none
### P3 — 1 (environment, not a site defect, not a blocker)

- **P3-1 — Footer Google Maps embed fails in this VM only.** 56 failed requests in the render run, all the identical URL `https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed`, all `net::ERR_TUNNEL_CONNECTION_FAILED` (28 pages x 2 widths; the 3 `/locations/*` pages carry no map embed, hence 0 there). Zero local-asset failures, zero console errors, zero page errors. The embed URL is a standard Google Maps embed, unchanged by this round; the VM simply has no egress route to google.com. Needs a real-network eyeball check on the live site after push, not a code fix.

## How verification was done

- Fresh `npm run export` by me (TMPDIR pointed at `qa/tmpdir`): **exit 0**. Log: `qa/export-verify-2026-11-13.log`. Served `out/` under `/midvale-water-damage/` locally; homepage identity confirmed first: H1 `24/7 Water Damage Restoration in Midvale, UT 84047`, phone `(385) 337-3560` present.
- Static script `qa/verify-fill-19px.py` → `qa/verify-fill-19px-static.json` (0 problems). Render script `qa/verify-fill-19px-render.py` → `qa/verify-fill-19px-render.json` (31/31 pages x 1440/390/320, full-scroll image forcing). Adjudication script `qa/adjudicate-brokenimgs.py` → `qa/brokenimgs-adjudication.json`. Click/form follow-up `qa/verify-fill-19px-clicks-form.py` (see own-error note). Review pack `qa/build-review-pdf-fill19px.py` → `~/workspace/your_files/midvale-design-review.pdf` (31 pp, 5.9 MB) from 62 fresh viewport screenshots in `qa/render-fill19px/`.
- **Own script error, owned plainly:** the render script crashed AFTER all 31 per-page measurements (incremental JSON saved) with a JS syntax error in my click-navigation evaluate string (one stray paren). Clicks + contact form were re-run cleanly in a separate follow-up script and merged into the same render JSON. No per-page result was re-used from any worker.

## Gate results (fresh measurements)

| Gate | Result |
|---|---|
| pages-data.json sha256 | `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — MATCHES expected `21c6e7f2…d638f` |
| Fullness | 31/31 FULL (main words per page below; 0 EMPTY, 0 THIN) |
| Verbatim (annotation-adjusted) | 0 missing words site-wide; extra words 749 total = header/footer/nav/CTA chrome only |
| H1 | exactly 1 per page, text verbatim, 31/31 |
| Meta title / description | verbatim 31/31 |
| FAQ | 142/142 data, 142/142 visible, 142/142 in JSON-LD; 0 mismatches |
| Tables | 43/43 rendered, all cells exact |
| Links | 162 total = 143 body + 19 card; 0 broken, 0 orphans (min inbound 1), 0 body self-links, 0 unprefixed hrefs, 0 inventory-record mismatches |
| Visible `(/.../)` path text | 0 in rendered MAIN on all pages; 0 in out/ HTML files |
| Images, static | 19 service/location pages = exactly 4 each (hero + 3 body, matching manifest); homepage 20 (hero + 19 cards); other 11 pages 1 (hero); 0 img files missing from out/, 0 missing alt |
| Images, render | all pages' totals match static; see broken-image adjudication for the lazy-load flags (0 genuinely broken) |
| Manifest | 19 routes x 3 body images = 57 |
| 7 new images | all 1200x675 WebP, 0 EXIF, no "AI" in filename/alt/metadata (PIL + exiftool) |
| 19px body copy | body 19px on 31/31; every content p/li/td/th, card p, FAQ answer p and form input 19px at 1440/390/320; headings unchanged h1 44/34/24, h2 32/28, h3 24 (3 legal pages have no h3 in data: privacy-policy, terms-of-use, disclaimer) |
| Button 2 "Request Emergency Help" scroll-0 | 31/31 @320 (worst bottom 497.2px of 844) and 31/31 @390 (worst 766.8px of 844) |
| Overflow | 0 @320, 0 @390, 0 @1440 on all 31 pages |
| Console errors / page errors | 0 / 0 |
| Failed requests | 56, all the external Google Maps embed (P3-1, VM egress); 0 local assets |
| Real-click navigation | 6/6 clicks kept the `/midvale-water-damage/` subpath (5 homepage card links + 1 inner body link), each landing on the correct H1 |
| Contact form | 6 logical fields (Name, Phone number, Address or ZIP code, What happened, Is the water still running? Yes/No/Not sure, Best time to call) = 8 input elements incl. 3 radios; all inputs 19px; submit `[Send My Request]` verbatim from doc data; honest non-send notice present |

## Broken-image adjudication (shoot log vs reality)

The cancelled full-page screenshot run left `qa/fullpage-shoot.log` flagging brokenImgs=3 (homepage desktop), 5 (homepage m390), 2 (basement m390) across the 5/31 routes it shot. My fresh render run flagged MORE, not fewer: 19 images @1440 and 23 @390 across 17 routes — every single one `loading=lazy`, nearly all the lowest body image on its page (`*-3.webp`, a few `*-2.webp`), and the homepage's last 4 card images. No local image URL ever produced a failed request in either run.

Re-check (`qa/adjudicate-brokenimgs.py`, slow 400px/300ms scroll + `scrollIntoView` per flagged image + 2s wait, 1440px):

- **27 flagged srcs re-checked, 0 still broken.** Every flagged image reached `naturalWidth: 1200`, `complete: true`.
- **Network:** 84 image requests tracked across the 17 pages, **all HTTP 200**, 0 failed, 0 non-200.
- **Files:** all 27 flagged files curl **200** from the local server; out/ bytes identical to public/ bytes (sha256 match) for all 27.
- **Verdict: lazy-load counting artifact, not broken images.** The fast-scroll measurement (700px steps, 110ms) outran lazy-load triggering for the lowest images; the counts also varied run-to-run and width-to-width (shoot log: home m390 = 5; my run: home m390 = 0), which a genuinely missing file could not do. **No fix made, no re-export needed on this account.**

## New-image spot checks (viewed at full size)

| File | Viewed verdict |
|---|---|
| commercial-water-damage-3.webp (overwritten, colour) | PASS — large open office floor, wet floor, several blue air movers + dehumidifier; exact match to its alt |
| crawl-space-water-damage-1.webp | PASS — dark crawl space, wooden joists, damp dirt ground, puddle lit by flashlight; exact match to its alt |
| emergency-water-extraction-1.webp | PASS — truck-mounted extraction unit, hoses into a house, worker extracting water from a flooded living-room floor; exact match to its alt |
| emergency-water-extraction-3, crawl-space-water-damage-2, water-heater-leak-cleanup-2, south-salt-lake-ut-3 | not individually full-size viewed; all 1200x675 WebP, 0 EXIF, alts topical, all render naturalWidth 1200 in the adjudication/render runs |

## Notes (not problems)

- **Sub-19px elements found by the full scan (93 hits across 31 pages x 3 widths) are navigation/label chrome, not body copy:** the hero eyebrow kicker `p.eyebrow` (18px @1440/390, 14px @320) and breadcrumb `li` items (18px, e.g. "Home"). Both are deliberate pre-existing CSS (`.eyebrow`, `.breadcrumb li`), untouched by the 19px round, which scoped to body copy. Every content p/li/td/th, card paragraph, FAQ answer and form input measures 19px. Listed here so the parent can judge; not counted as a problem.
- `/tmp` was 25% used at start (not 100% as reported earlier); `TMPDIR` was still pointed at `qa/tmpdir` for all runs and Chromium launched with `--disable-dev-shm-usage` throughout. The other worker's `/tmp/pg-mech-test` was not touched.
- Extra words 749 site-wide are chrome (header/nav/footer/CTA/buttons), not invented content — missing words 0 is the verbatim gate and it passes.

## Per-page table

| Route | Main words | Missing | Fullness | Imgs static | Imgs render | Btn2 bottom 320 / 390 (px) | 19px body |
|---|---:|---:|---|---:|---:|---:|---|
| / | 2115 | 0 | FULL | 20 | 20 | 396.6 / 535.5 | body 19px, h1 44px/h2 32px/h3 24px |
| /about | 945 | 0 | FULL | 1 | 1 | 413.4 / 651.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /contact | 764 | 0 | FULL | 1 | 1 | 413.4 / 620.7 | body 19px, h1 44px/h2 32px/h3 24px |
| /emergency-water-extraction | 1797 | 0 | FULL | 4 | 4 | 437.2 / 651.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /basement-flooding-cleanup | 1702 | 0 | FULL | 4 | 4 | 437.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /window-well-flooding | 1782 | 0 | FULL | 4 | 4 | 437.2 / 651.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /burst-pipe-water-damage | 1868 | 0 | FULL | 4 | 4 | 467.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /sewage-backup-cleanup | 1737 | 0 | FULL | 4 | 4 | 437.2 / 651.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /water-heater-leak-cleanup | 1706 | 0 | FULL | 4 | 4 | 467.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /swamp-cooler-leak-water-damage | 1650 | 0 | FULL | 4 | 4 | 467.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /ceiling-water-damage | 1636 | 0 | FULL | 4 | 4 | 437.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /crawl-space-water-damage | 1654 | 0 | FULL | 4 | 4 | 467.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /hardwood-floor-cabinet-drying | 1777 | 0 | FULL | 4 | 4 | 437.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /condo-apartment-water-damage | 1774 | 0 | FULL | 4 | 4 | 497.2 / 766.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /commercial-water-damage | 1700 | 0 | FULL | 4 | 4 | 467.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /storm-flood-damage | 1645 | 0 | FULL | 4 | 4 | 437.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /mold-remediation | 1714 | 0 | FULL | 4 | 4 | 437.2 / 651.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /water-leak-detection | 1756 | 0 | FULL | 4 | 4 | 467.2 / 736.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /water-damage-repair | 1555 | 0 | FULL | 4 | 4 | 437.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /locations/cottonwood-heights-ut | 1766 | 0 | FULL | 4 | 4 | 467.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /locations/south-salt-lake-ut | 1860 | 0 | FULL | 4 | 4 | 467.2 / 736.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /locations/magna-ut | 1833 | 0 | FULL | 4 | 4 | 437.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /midvale-water-sewer-emergency-contacts | 1278 | 0 | FULL | 1 | 1 | 437.2 / 651.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /privacy-policy | 528 | 0 | FULL | 1 | 1 | 377.2 / 499.1 | body 19px, h1 44px/h2 32px/h3 None |
| /terms-of-use | 476 | 0 | FULL | 1 | 1 | 377.2 / 499.1 | body 19px, h1 44px/h2 32px/h3 None |
| /disclaimer | 312 | 0 | FULL | 1 | 1 | 377.2 / 499.1 | body 19px, h1 44px/h2 32px/h3 None |
| /resources/frozen-pipes-midvale | 1686 | 0 | FULL | 1 | 1 | 443.4 / 663.2 | body 19px, h1 44px/h2 32px/h3 24px |
| /resources/winterize-swamp-cooler-utah | 1534 | 0 | FULL | 1 | 1 | 437.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /resources/upstairs-unit-leak-who-pays-utah | 1571 | 0 | FULL | 1 | 1 | 467.2 / 736.3 | body 19px, h1 44px/h2 32px/h3 24px |
| /resources/can-mold-grow-in-utah | 1485 | 0 | FULL | 1 | 1 | 467.2 / 693.8 | body 19px, h1 44px/h2 32px/h3 24px |
| /resources/basement-flooding-spring-snowmelt-utah | 1488 | 0 | FULL | 1 | 1 | 497.2 / 766.8 | body 19px, h1 44px/h2 32px/h3 24px |

Button-2 worst bottoms: 497.2px @320 (condo-apartment-water-damage, resources/basement-flooding-spring-snowmelt-utah) and 766.8px @390 (same two pages) — both inside the 844px viewport. Overflow 0 and console 0 on every row above.

## Deliverables

- Review pack: `~/workspace/your_files/midvale-design-review.pdf` (31 pages, 5.9 MB; desktop 1440 + mobile 390 per route, labelled) — built from 62 fresh screenshots in `qa/render-fill19px/` taken from THIS export.
- This file: `qa/FINDINGS-fill-19px-verify-2026-11-13.md`.
- Evidence JSONs: `qa/verify-fill-19px-static.json`, `qa/verify-fill-19px-render.json` (incl. clicks + contact form), `qa/brokenimgs-adjudication.json`; logs `qa/export-verify-2026-11-13.log`, `qa/verify-fill-19px-render.log`; scripts `qa/verify-fill-19px.py`, `qa/verify-fill-19px-render.py`, `qa/verify-fill-19px-clicks-form.py`, `qa/adjudicate-brokenimgs.py`, `qa/build-review-pdf-fill19px.py`.
