# FINDINGS — Independent 10x UI/UX testing, Midvale design round

**Date:** 2026-11-13 ~03:30–04:30 PKT (scheduled 2-hour-mark round)
**Build tested:** `out/` timestamped 2026-11-12 21:59:41 UTC (02:59 PKT); no source file newer than `out/` — design NOT mid-edit, final design build.
**Served:** `qa/linkfix-serve.py` on 127.0.0.1:8325 under `/midvale-water-damage/`; identity verified (homepage title "Water Damage Restoration Midvale UT | 24/7 Emergency Crew Dispatched Now", H1 "24/7 Water Damage Restoration in Midvale, UT 84047"). Server left running on port 8325.
**Method:** fresh Playwright (Chromium) pass, 31 routes × viewports 1440/390/320; fresh screenshots (never reused prior rounds' as evidence); independent static pass (verbatim multiset vs `lib/pages-data.json`, link crawl, orphans, self-links, sitemap, assets); full scroll-through image re-check; real-click navigation with proper waits; all 101 images judged by viewed pixels (heroes, cards, body files + in-context renders).
**Scope:** VERIFY ONLY. No site source file modified, no rebuild, no push/deploy/GitHub/token, no MEMORY.md edit.

## VERDICT — READY FOR RE-PUSH

**PROBLEMS: P1 0 · P2 0 · P3 1 (non-blocking polish, see P3-1).**

The design round verifies clean on every gate I measured fresh. The single P3 is one black-and-white body photo among 101 colour images — a polish swap the user can take or leave; it does not block the re-push. Everything else the coordinator claimed (PROBLEMS 0) held up under fresh eyes, with two of my own first-pass flags turning out to be my own script artifacts (owned below in §Methodology notes), not site defects.

## PROBLEMS

### P3-1 — commercial-water-damage-3.webp is black-and-white (only B&W photo on the site)
- **Page:** `/commercial-water-damage` (split image after H2, "Commercial Drying for Large Open Spaces" section area; file `public/images/body/commercial-water-damage-3.webp`, 17,748 bytes).
- **Evidence:** measured mean saturation 0.000 (truly grayscale) — confirmed by viewed pixels: concrete commercial interior, wet floor, no colour. It is the ONLY grayscale image among 101 site images (31 heroes + 19 cards + 51 body, all colour). In context (`commercial-sec1-live.png`, `test-fpl-sec2.png`) it reads as a mistake next to its colour siblings.
- **Topic fit is fine** (commercial interior, wet floor) — the issue is treatment consistency only.
- **Fix:** replace with a colour commercial-interior photo (same slot, same 1200×675). Non-blocking: his call.

## Marginal images — verdicts (all judged by viewed pixels)

| Image | Verdict | Reason |
|---|---|---|
| `commercial-water-damage-3.webp` (B&W) | **REPLACE** (P3-1) | Only grayscale image sitewide; topic fine, treatment inconsistent. |
| `basement-flooding-cleanup-1.webp` + `-2.webp` (dry finished rooms) | KEEP | Clean empty basement bedrooms, correct room type for the page. No water/drying cues — a wet/drying shot would sell the service harder, but nothing is wrong. Optional swap, his call. |
| `burst-pipe-water-damage-1.webp` (snow-capped pipe outlet/downspout + icicle) | KEEP | Frozen exterior pipe outlet in deep snow — on-topic for frozen/burst pipes. It is a downspout/outlet rather than a burst interior pipe, but the freeze story is exactly the page's story. |
| `sewage-backup-cleanup-2.webp` (drain grate, "400 X 600" / "EN124 B125" stamps legible) | KEEP | Stamps are small generic product markings on the grate, not place-identifying text or branding. Harmless. |
| G1 files at q50–70 (smallest: `basement-flooding-cleanup-2.webp` 22 KB, `emergency-water-extraction-2.webp` 42 KB, `sewage-backup-cleanup-1.webp` 45 KB) | KEEP | No visible compression artifacts at display size (400/342 px) or at full 1200×675 (checked `basement-flooding-cleanup-2.webp` full-size: smooth gradients, no blocking/banding). Low-detail subjects compress small legitimately. Exact encode quality is not recoverable from the file and does not matter — pixels are clean. |
| `magna-ut-3.webp` vs `basement-flooding-cleanup-1.webp` (look like twins) | KEEP (note) | Different photos, not a reuse: md5 differ, aHash8 12/64, aHash16 52/256, MAD 21.93 (same-photo ≈ 0–2/256, 0.5–3). Full-size side-by-side (`/tmp/magna-vs-basement.png`) confirms different shots/angles of a similar grey basement room (same photo series). A sharp-eyed visitor could notice the resemblance — optional variety swap, his call. |

## Observations (NOT problems — no action required unless he wants it)

- **O1 — Footer map is a 320 px empty dark band when Google Maps cannot load.** The footer opens with a `.footer-map` iframe (`https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed`, 320 px tall, no `loading="lazy"`). In this sandbox every page load logs `ERR_TUNNEL_CONNECTION_FAILED` for it (sandbox proxy blocks external network — same known limit as prior rounds), so the band renders empty dark green. On a normal connection it shows the Midvale map. **Map tiles NOT VERIFIED** (cannot be verified from this sandbox). Optional robustness: lazy-load the iframe and/or a static fallback behind it.
- **O2 — Eyebrow is 14 px at ≤360 px.** The ONLY sub-18 px text anywhere: the hero eyebrow `<p>` (e.g. "WATER DAMAGE RESTORATION • MIDVALE, UTAH") measures 14 px at 320 px viewport on all 31 pages. Body copy is 18 px everywhere else. This is the known, accepted design-round trade-off (load-bearing for Button 2 visibility at 320 px) — recorded here for completeness, not a defect.
- **O3 — Sticky-pin travel varies with section length (by design).** All 18 sticky figures pin at exactly `top: 96px` (`position: sticky`). Pin travel = parent section height − 225 px: 43 px (`magna-ut-3`, 431-char section) to 1,120 px (`water-heater-leak-cleanup-1`, 1,763-char section); median ≈ 500 px. Short sections pin briefly because there is little text to sit beside — correct sticky behaviour, not a malfunction.
- **O4 — Heroes/cards are AI-generated-style images (pre-existing).** All 31 heroes + 19 cards are dramatic, dark, on-topic generated scenes (no foreign text, no legible branding; checked at full size). Topic/place fit is good throughout (Wasatch/snow for Cottonwood, Main Street dusk for Magna, wet industrial street for South Salt Lake). "Real job photos vs generated images" remains the standing open item from Round 1 — not a design-round defect.
- **O5 — 6 honestly-empty image slots (as briefed, not defects):** emergency 1+3, crawl-space 1+2, water-heater 2, south-salt-lake 3. No slot renders broken; empty slots simply have no `<img>`.
- **O6 — Header nav carries 3 links + logo + tel (no /about link in header).** By design; About/Contact/legal are in the footer (27 links/page). Orphans 0 — every route is reachable.
- **O7 — Contact form has 6 fields, no email — exactly per the doc.** Doc Tab 3 "Request Form Fields" lists Name / Phone number / Address or ZIP code / What happened / Is the water still running? (Yes/No/Not sure) / Best time to call — no email field exists in the doc, so none is rendered. Submit "[Send My Request]" is verbatim doc text. Submit shows the honest "Thanks, this preview form doesn't send. Please call (385) 337-3560…" message, no fake POST (verified live: URL unchanged after submit).

## Pass evidence (fresh measurements)

- **Routes / sitemap:** 31/31 routes 200 via served subpath; sitemap 31 `<loc>`, exactly the 31 data routes; title + meta description verbatim 31/31; H1 exactly 1/page with exact doc text 31/31.
- **Verbatim:** missing words **0 on all 31 pages** (annotation-adjusted multiset: eyebrow+H1+intro+trustChips+blocks minus link-annotation path tokens). Extra words 749 sitewide (~24/page) are chrome only — verified samples: phone digits, "Request Emergency Help", button labels, form labels, breadcrumb/FAQ overlap. FAQ visible = data 142/142; tables 43/43 cell counts match.
- **Links:** 0 broken internal links; 0 orphans (every route reachable from homepage or another page); 0 body self-links; 0 missing referenced assets (incl. `_next` chunks, after URL-decoding `%5Bslug%5D` paths); 0 paren-path `(/.../)` leaks in visible main text.
- **Overflow:** 0 px at 320, 390 and 1440 on all 31 routes.
- **Button 2 (`.hero .btn-help`, "Request Emergency Help"):** fully visible at scroll-0 on 31/31 at 320 AND 390 AND 1440; worst bottom margin 70.8 px @320, 77.2 px @390; hit-test confirms not covered by anything; sticky call bar is `bar-hidden` at scroll-0 (appears on scroll past ~900–1500 px, hides again at top — verified live).
- **Header/footer:** 0 em dashes, 0 en dashes in header, footer and main visible text on all 31 pages (contact-form dashes fixed, confirmed).
- **Underlines:** 0 violations among internal links (computed `text-decoration-line`); the only borders are the designed 2 px full borders on the four tel: `.btn` buttons per page.
- **Type:** body copy computed 18 px (min = median = 18) at 1440/390 on all pages; H2 32 px, H3 24 px.
- **Contrast (computed, effective background):** worst heading ratio sitewide **8.96:1** (H3 pine-2 on white); H2 pine 12.34:1 on white, 10.57:1 on tint — all AAA, nothing below AA 4.5:1.
- **Images:** 101 total (31 heroes + 19 cards + 51 body). After full scroll-through + targeted scroll-into-view, **0 broken**; all `object-fit: cover`, 0 real distortion (display-vs-natural aspect deltas are cover-crops, not stretches). Layout verified live: desktop 2-col grid `632px + 400px` (text | image), mobile stacked image-above-text full width (342 px @390), sticky pins at 96 px. Homepage cards: 3-col grid, 19/19 16:9, equal.
- **Console / network:** 0 console errors, 0 page errors, 0 failed LOCAL requests on all 31 routes × 3 viewports. Sole failed request is the external Google Maps embed (sandbox-blocked, see O1).
- **Real-click navigation (with `wait_for_url`, not racy reads):** home card → `/emergency-water-extraction` (H1 correct, styled 44 px); body link → `/hardwood-floor-cabinet-drying` (H1 correct); footer link → `/locations/cottonwood-heights-ut` (H1 correct). Subpath `/midvale-water-damage/` kept on every click; pages render styled.
- **Mobile menu:** hamburger opens at 390, panel 201 px with Home / Emergency Water Extraction / Sewage Backup Cleanup.
- **Footer:** 5-column grid, 27 links/page, no dashes, no underlines, white on pine, bottom line "Water Damage Restoration Midvale UT · Midvale, UT 84047 · (385) 337-3560".

## Per-page table

| Route | H1 | Overflow 320/390/1440 | Button 2 @320 (margin) | Button 2 @390 (margin) | Verbatim missing | Images | Links |
|---|---|---|---|---|---|---|---|
| `/` | OK | 0/0/0 | OK (171px) | OK (309px) | 0 | 20 (hero+19 cards), 0 broken* | OK |
| `/about` | OK | 0/0/0 | OK (155px) | OK (193px) | 0 | 1 (hero), 0 broken | OK |
| `/contact` | OK | 0/0/0 | OK (155px) | OK (223px) | 0 | 1 (hero), 0 broken | OK |
| `/emergency-water-extraction` | OK | 0/0/0 | OK (131px) | OK (193px) | 0 | 2 (hero+1 body), 0 broken | OK |
| `/basement-flooding-cleanup` | OK | 0/0/0 | OK (131px) | OK (150px) | 0 | 4 (hero+3 body), 0 broken | OK |
| `/window-well-flooding` | OK | 0/0/0 | OK (131px) | OK (193px) | 0 | 4, 0 broken | OK |
| `/burst-pipe-water-damage` | OK | 0/0/0 | OK (101px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/sewage-backup-cleanup` | OK | 0/0/0 | OK (131px) | OK (193px) | 0 | 4, 0 broken | OK |
| `/water-heater-leak-cleanup` | OK | 0/0/0 | OK (101px) | OK (150px) | 0 | 3 (hero+2 body), 0 broken | OK |
| `/swamp-cooler-leak-water-damage` | OK | 0/0/0 | OK (101px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/ceiling-water-damage` | OK | 0/0/0 | OK (131px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/crawl-space-water-damage` | OK | 0/0/0 | OK (101px) | OK (150px) | 0 | 2 (hero+1 body), 0 broken | OK |
| `/hardwood-floor-cabinet-drying` | OK | 0/0/0 | OK (131px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/condo-apartment-water-damage` | OK | 0/0/0 | OK (71px) | OK (77px) | 0 | 4, 0 broken | OK |
| `/commercial-water-damage` | OK | 0/0/0 | OK (101px) | OK (150px) | 0 | 4, 0 broken — incl. P3-1 B&W | OK |
| `/storm-flood-damage` | OK | 0/0/0 | OK (131px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/mold-remediation` | OK | 0/0/0 | OK (131px) | OK (193px) | 0 | 4, 0 broken | OK |
| `/water-leak-detection` | OK | 0/0/0 | OK (101px) | OK (108px) | 0 | 4, 0 broken | OK |
| `/water-damage-repair` | OK | 0/0/0 | OK (131px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/locations/cottonwood-heights-ut` | OK | 0/0/0 | OK (101px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/locations/south-salt-lake-ut` | OK | 0/0/0 | OK (101px) | OK (108px) | 0 | 3 (hero+2 body), 0 broken | OK |
| `/locations/magna-ut` | OK | 0/0/0 | OK (131px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/midvale-water-sewer-emergency-contacts` | OK | 0/0/0 | OK (131px) | OK (193px) | 0 | 1 (hero), 0 broken | OK |
| `/privacy-policy` | OK | 0/0/0 | OK (191px) | OK (345px) | 0 | 1 (hero), 0 broken | OK |
| `/terms-of-use` | OK | 0/0/0 | OK (191px) | OK (345px) | 0 | 1 (hero), 0 broken | OK |
| `/disclaimer` | OK | 0/0/0 | OK (191px) | OK (345px) | 0 | 1 (hero), 0 broken | OK |
| `/resources/frozen-pipes-midvale` | OK | 0/0/0 | OK (125px) | OK (181px) | 0 | 1 (hero), 0 broken | OK |
| `/resources/winterize-swamp-cooler-utah` | OK | 0/0/0 | OK (131px) | OK (150px) | 0 | 4, 0 broken | OK |
| `/resources/upstairs-unit-leak-who-pays-utah` | OK | 0/0/0 | OK (101px) | OK (108px) | 0 | 1 (hero), 0 broken | OK |
| `/resources/can-mold-grow-in-utah` | OK | 0/0/0 | OK (101px) | OK (150px) | 0 | 1 (hero), 0 broken | OK |
| `/resources/basement-flooding-spring-snowmelt-utah` | OK | 0/0/0 | OK (71px) | OK (77px) | 0 | 1 (hero), 0 broken | OK |

\* Homepage "broken" in the raw scroll-through JSON was 3 lazy location cards that had not yet loaded during the scripted fast scroll; targeted `scrollIntoView` + 2 s wait proves all three load (`complete: true`, natural 1200×675), and `location-cards-check.png` shows the Magna card rendered. 0 genuinely broken images sitewide.

## Methodology notes — my own script errors, owned plainly

1. **Static script v1 false positives (fixed, re-ran clean).** First run flagged 65 "problems": `/midvale-water-damage#faq` / `#services` / `#areas` were mis-classified as unprefixed root-relative links (they ARE base-path-prefixed anchor links to the homepage; targets `#faq`/`#services`/`#areas` all exist on the homepage), and `_next/static/chunks/app/%5Bslug%5D/page-*.js` was reported missing because the path was not URL-decoded (`%5B` = `[`). Both fixed in the script; re-run: PROBLEMS 0, broken links 0, missing assets 0. The first run's output is superseded — do not trust it.
2. **"Broken images" in the first render pass were lazy-load timing, not broken images.** `loading="lazy"` images below the fold report `naturalWidth 0` until scrolled into view. Re-checked with a full scroll-through + targeted `scrollIntoView` on every flagged file: all load (1200×675). The only files that stayed "broken" after the fast scroll were the deepest-below-fold ones (3 homepage location cards, several `*-3` body images at 390) — all proven to load on scroll-into-view.
3. **First full-page screenshots lied about the body-image layout.** Captures taken at scroll-0 (before lazy images loaded) render unloaded lazy images as absent and reflow the text full-width — a Chromium fullPage-capture artifact, proven by reproduction: same capture after a scroll-through shows the correct 2-col layout with images. The live DOM geometry (grid `632px + 400px`, figure x=856 w=400) and scrolled screenshots (`commercial-sec1-live.png`, `test-fpl-sec1/2.png`) are the true evidence. All `*-full-loaded.png` re-shoots were taken after scroll-through and show the real layout.
4. **Click-test v1 raced client-side navigation.** It read `page.url` before Next.js client-side routing updated history, recording the old URL next to the new H1. Re-ran with `wait_for_url`: all three clicks land on the correct subpath URL with the correct H1.
5. **A "missing email field" expectation was wrong, not the site.** I briefly expected 7 contact fields incl. email (an Acworth spec). Midvale's doc Tab 3 lists 6 fields, no email — the form matches the doc exactly. No defect.

## Files produced (all under `qa/10x-design/`)

- `FINDINGS-10x-design-2026-11-13.md` — this file.
- `10x-design-render.json` — per-route × viewport measurements (H1, overflow, Button 2, fonts, contrast, dashes, underlines, images, console/failed).
- `10x-design-static.json` — verbatim multiset, links, orphans, self-links, sitemap, assets (re-run after the v1 fix).
- `10x-design-images.json` — post-scroll image states + proper-wait click test.
- `10x-design-verify.py`, `10x-design-static.py`, `10x-design-recheck.py`, `10x-design-reshoot.py` — the fresh scripts used (test-only).
- Screenshots: `*-1440-top.png`, `*-390-top.png`, `*-320-top.png` (31 each); `*-390-full-loaded.png` (31, post-scroll); `*-1440-full-loaded.png` (home, emergency, commercial, about); `sheet-desktop-tops.png`, `sheet-mobile-tops.png`, `sheet-320-tops.png`, `sheet-heroes.png`, `sheet-cards.png`, `sheet-body-1..5.png` (contact sheets used for the viewed-pixels review); `commercial-sec1-live.png`, `test-fpl-sec1.png`, `test-fpl-sec2.png`, `basement-390-loaded-sec1.png`, `commercial-390-loaded-sec1.png`, `home-cards-crop.png`, `location-cards-check.png`, `mobile-menu-open.png`, `mobile-sticky-bar.png`, `contact-form-sent.png`.
- Note: the first-pass `*-390-full.png` / `*-1440-full.png` files are UNRELIABLE for body-image sections (see methodology note 3) — use the `*-loaded.png` versions instead.

## Not verified (stated limits)

- Footer Google Maps tiles (sandbox blocks external network; iframe URL + 320 px box verified, tiles not).
- LCP numbers in headless shell (not measured; FCP/CLS not claimed).
- Live GitHub Pages behaviour (local subpath mirror only; no push/deploy was done or attempted).
