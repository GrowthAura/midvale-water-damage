# STAGE 5 — FINAL 1001% WEB + MOBILE FRIENDLY CHECK — FINDINGS

**Coordinator:** Stage 5 final friendly check coordinator (STAGE 5, FINAL, of the 6-hour watchdog chain; Stages 0–4 complete).
**Date:** 2026-11-13 ~12:10 PKT.
**Build:** fresh `npm run export` exit 0, `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage` (no trailing slash), served on `http://127.0.0.1:8350/midvale-water-damage/`. Data sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` verified unchanged before and after.
**Method:** four parallel workers (W1 static, W2 desktop render 1440, W3 mobile render 390/320, W4 real-clicks + speed + image spot-check), all in real Chromium (Playwright) unless stated. I re-verified every key number myself from the raw JSONs, fresh greps, and by viewing images/screenshots full-size. No source file modified. No push/deploy/token/DNS.

## VERDICT: NOT READY FOR RE-PUSH — P1 0 / P2 2 / P3 5

Two real P2s block the push: two location card photos do not match their alt text (false descriptions for screen readers and image search). Both are one-photo swaps — the matching heroes already exist and match their alts exactly. Everything else passes. The chain is NOT done until the 2 P2s are fixed and re-verified fresh.

## PROBLEMS

### P2-1 — cards/south-salt-lake-ut.webp alt mismatch (card photo is wrong, alt is right)
- Card alt (lib/content.ts): "Apartment blocks and warehouse buildings in South Salt Lake, Utah".
- Photo actually shows: a UTA TRAX Blue Line light-rail train at a snowy station. No apartments, no warehouses.
- Verified by W4 (viewed full-size) and by me (viewed full-size + read the source alt).
- The hero for the same page (heroes/south-salt-lake-ut.webp) shows apartments + warehouses at dusk and matches ITS alt exactly (W4 diagnostic view).
- Fix: swap the card photo for a crop of the matching hero (keeps the alt truthful; also closes the standing "card ≠ hero" item). Rewriting the card alt to describe a train is the weaker alternative — the card should show the place.

### P2-2 — cards/magna-ut.webp alt mismatch (card photo is wrong, alt is right)
- Card alt (lib/content.ts): "Older brick homes and storefronts on historic Main Street in Magna, Utah".
- Photo actually shows: newer suburban brick homes + white fence, snowy Oquirrh mountains behind. No storefronts, no Main Street.
- Verified by W4 (viewed full-size) and by me (viewed full-size + read the source alt).
- The hero for the same page (heroes/magna-ut.webp) shows older brick storefronts + homes on a wet Main Street at dusk and matches ITS alt exactly (W4 diagnostic view).
- Fix: same as P2-1 — swap the card photo for a crop of the matching hero.

### P3-1 — body/mold-remediation-2.webp very washed-out (cosmetic)
- Worker in white suit fogging a misty room; mean saturation 0.047, near-white fog. Alt + topic pass; the photo is on-topic but the worker is barely distinguishable from the white haze.
- Verified by me (viewed full-size — foggy white room, correct subject, low contrast).
- Fix: swap only if a stronger fogging photo is available; never force a wrong photo.

### P3-2 — Mobile LCP 2.9–3.7 s in lab (throttled)
- Desktop LCP 0.9–2.6 s; mobile LCP 2,928–3,668 ms (CPU ×4 + Fast 3G emulation); CLS 0 on all 12 measured rows.
- LCP element is `IMG.hero-img` on every page/viewport; on desktop FCP == LCP, i.e. the 1600×1066 hero gates first paint.
- Lab numbers only (served from 127.0.0.1 on this VM) — re-measure on real hosting. Not a blocker.

### P3-3 — Header nav carries only 3 links (observation)
- Home + Emergency Water Extraction + Sewage Backup Cleanup on all viewports (verified in the live DOM).
- Nothing is stranded (cards/footer/body links cover the rest). Observation only.

### P3-4 — Weakest contrast 5.65:1 (observation, passes AA)
- Burnt-orange text — brand-city "Midvale, UT" (18px), header phone link, hero phone-button text — 5.65:1 vs backgrounds (opacity-aware audit, 4 pages).
- Passes WCAG AA for normal text (4.5:1); it is the floor of the site. No fix required. (The per-route sampler, not opacity-aware, showed ≥10.85:1.)

### P3-5 — Google Maps embed unconfirmable in this sandbox (environmental)
- Footer Maps iframe (`google.com/maps?q=Midvale,+UT+84047&output=embed`, present on all 31 pages) fails to load here on 15/31 desktop routes — the sandbox has no route to google.com. Not a site defect. Map tiles need a real-network eyeball after push (same open item as every prior round).

## WHAT PASSED (all measured fresh this round)

### Static (W1) — PROBLEMS 0, all 11 checks pass
- Fullness 31/31 FULL (46,379 main words / 51,060 visible words). Thinnest: /disclaimer 309 main words; homepage 2,097; max service page 1,842.
- Verbatim: 2,980 segments, 0 missing / 0 reordered after annotation-normalization. Raw pass showed 165 "missing" — all 165 are doc link annotations, reconciled exactly: 143 body-links + 22 plain-text dedupes (homepage 20: 19 covered by card-wrap links + 1 body-link target; water-heater 1 + commercial 1: same route annotated twice, linked once per the one-link-per-target rule). 0 annotation targets unlinked; 0 body-link routes not from a data annotation.
- FAQ: 142 visible Q&A; FAQPage schema == visible on all 28 FAQ pages (count + question + answer text).
- Tables: 43/43. Links: 162 (143 body + 19 card-wrap), all 31 internal targets curl 200, 0 orphans, 0 self-links in body copy.
- Visible parenthetical path annotations `(/.../)`: 0. `http://localhost:3000`: 0 in HTML/XML/TXT and 0 in `_next` JS chunks (no framework-code hit at all this build). Double-slash absolute URLs: 0.
- robots.txt: `Allow: /`, no `Host:` line, Sitemap line on the Pages URL. sitemap.xml: 31 locs, date-only lastmod `2026-11-12`, all 31 curl 200.
- Robots meta: 404.html exactly 1 (`noindex`); each of the 31 pages exactly 1 (`index, follow`).
- JSON-LD: 178 blocks, exact per-type counts (BreadcrumbList 31, FAQPage 28, WebPage 31, ImageObject 31, HowTo 36, Service 19, HomeAndConstructionBusiness 1, WebSite 1). 0 parse errors. ImageObject contentUrl 31/31 curl 200, no doubled subpath. 0 localhost / 0 double-slash inside schema. (404.html has 0 JSON-LD blocks.)

### Desktop render 1440×900 (W2) — P1 0, P2 0
- H1 31/31 exactly 1 and visible; titles unique and correct.
- Buttons exactly equal 322×56 on all 31 routes (hero pair). Button 2 bottom worst 662.7px (condo), all fully above the 900px fold at scroll-0.
- Overflow 0 on all 31; console errors 0; page errors 0; failed local requests 0.
- Images 107/107 rendered (20 home + 64 service + 12 locations + 11 others).
- Tap targets: 0 below 48px (header nav min 48px, footer links min 48px).
- Body font 19px on all 31 routes (3 samples/page). Eyebrow 18px at desktop (label, not body copy).
- Scope note: "Request Emergency Help" does NOT live inside `<header>` — the header holds only the phone link (167×50.6). The Button 1/Button 2 pair is the hero pair (`.hero-buttons`), present above the fold at scroll-0 on every route (a second identical pair sits in the final CTA at page bottom).

### Mobile render 390×844 + 320×568 (W3) — PROBLEMS 0
- H1 31/31 × 2 widths, exactly 1 and visible. Styled render confirmed visually (home @390 and condo @320 screenshots viewed).
- Button 2 fully visible at scroll-0: 31/31 @390 (worst 768.2px) and 31/31 @320 (worst 556.2px, condo — 11.8px headroom, passes but thin; see observation (a) below).
- Overflow 0/31 at both widths; console errors 0; failed local requests 0; Google Maps env fails 0 (no failed Maps requests observed at all on mobile runs).
- Images 107/107 rendered after scroll-through, 0 broken.
- Tap targets: 0 below 48px at either width (footer links min 48px, header phone 48px @390, menu button 48px @both).
- Tables: 43 wrappers per width; 31 overflowing @390, 36 @320, across 24 routes (brief said 18 — measured 24). All 67 overflowing wrappers: scroll cue opacity 1, swipe verified (scrollLeft moves). 0 cue missing, 0 not swipeable.
- Body copy 19px on 31/31 (10–43 paragraphs sampled per page, all 19px). Eyebrow 18px @390 / 14px @320 — the known accepted ≤360px trade-off, not flagged.
- Mobile menu 3/3 PASS (home, emergency-water-extraction, mold-remediation @390) — opens, 3/3 links visible, body locks (position:fixed, top −600px, scroll attempt doesn't move it), closes cleanly, scroll restores to 600.

### Real-click navigation (W4) — 7/7 PASS
| # | Click | Result |
|---|---|---|
| A1 | Homepage service card (Emergency Water Extraction) | → /emergency-water-extraction, correct H1, subpath kept, 200 |
| A2 | Footer location link "Water Damage Restoration Cottonwood Heights" | → /locations/cottonwood-heights-ut, correct H1, subpath kept, 200 |
| A3 | Breadcrumb "Home" on service page | → /, correct H1, subpath kept, 200 |
| A4 | Mobile menu (390px) → "Sewage Backup Cleanup" | → /sewage-backup-cleanup, correct H1, subpath kept, 200 |
| A5 | Footer "About" link | → /about, correct H1, subpath kept, 200 |
| A6 | Body-copy link "Water Leak Detection" in a `<p>` on burst-pipe page | → /water-leak-detection, correct H1, subpath kept, 200 |
| A7 | Sticky call-bar phone link | href `tel:+13853373560` verified; no navigation (headless Chromium has no tel: handler — not a defect) |

### Speed (W4) — lab numbers, NOT field data
Method: PerformanceObserver injected pre-load, 3 runs/page/viewport, medians. Desktop 1440: CPU ×4, no network throttle. Mobile 390: CPU ×4 + Fast 3G (1.6 Mbps down / 750 kbps up, 150 ms RTT). Served from 127.0.0.1.

| Page | Desktop FCP/LCP | Mobile FCP/LCP | CLS | LCP element |
|---|---|---|---|---|
| Homepage | 920 / 920 ms | 1,936 / 2,928 ms | 0 | IMG.hero-img |
| Emergency Water Extraction | 1,796 / 1,796 ms | 1,892 / 3,080 ms | 0 | IMG.hero-img |
| Burst Pipe Water Damage | 2,600 / 2,600 ms | 2,192 / 3,520 ms | 0 | IMG.hero-img |
| Mold Remediation | 2,380 / 2,380 ms | 2,000 / 3,384 ms | 0 | IMG.hero-img |
| Location: Cottonwood Heights | 1,436 / 1,436 ms | 1,188 / 3,668 ms | 0 | IMG.hero-img |
| Resource: Frozen Pipes | 2,168 / 2,168 ms | 1,592 / 3,088 ms | 0 | IMG.hero-img |

CLS 0 on all 12 rows. LCP is the hero image on every page/viewport.

### Image spot-check by viewed pixels (W4) — 12/12 viewed full-size
10/12 alt-exact + topic-fit. The 2 failures are P2-1/P2-2 above. The other 10:
- heroes/basement-flooding-spring-snowmelt-utah.webp — downspout discharging onto a puddle at a foundation, melting snow piles, snowy hills. Alt EXACT (the fixed alt is correct).
- cards/cottonwood-heights-ut.webp — winding canyon highway, steep rocky autumn slopes. Alt EXACT (the fixed alt is correct).
- heroes/commercial-water-damage.webp — dark restaurant after hours, wet floor, 2 yellow air movers + dehumidifier. **Colour confirmed** (mean saturation 0.38) — not B&W. The old B&W P3 stays closed.
- heroes/burst-pipe-water-damage.webp — split copper pipe spraying water in a dark wall cavity. Alt exact.
- heroes/sewage-backup-cleanup.webp — 3 workers in PPE cleaning a filthy tiled bathroom floor. Alt yes (staged/illustration-style look; topic + alt pass).
- heroes/storm-flood-damage.webp — storm runoff flooding a garage at night. Alt exact.
- body/burst-pipe-water-damage-1.webp — frozen copper pipe split open, frost + icicles. Alt exact.
- body/mold-remediation-2.webp — worker in white suit fogging a misty room. Alt yes, topic yes — very washed-out (P3-1).
- body/water-heater-leak-cleanup-1.webp — tall white tank heater + copper pipes, puddle at base. Alt exact.
- heroes/can-mold-grow-in-utah.webp — flashlight on black mold on damp drywall. Alt yes, exact fit.
- Diagnostic extra: heroes/south-salt-lake-ut.webp and heroes/magna-ut.webp both match their alts exactly — the alt text is correct and only the two CARD files are the wrong photos.

## OBSERVATIONS (not problems)
- (a) Button 2 headroom at 320 is only 11.8px on the worst route (condo, 556.2px vs 568px fold) — watch item for any future hero change.
- (b) Header phone is hidden at 320 — deliberate, documented in `globals.css` `@media (max-width:360px)` (header 136→110px so Button 2 clears the fold; hero Button 1 + sticky bar still call).
- (c) On 27 inner pages at 320, the breadcrumb title SPAN's layout box extends past the viewport (up to 879px) but is clipped by its parent LI with ellipsis — the designed ≤360px breadcrumb truncation; the 320 screenshot shows "Home / 24/7 Condo, Townho…" truncated cleanly, overflow 0.
- (d) /disclaimer is the thinnest page at 309 main words — passes the FULL gate (≥300).
- (e) Eyebrow 14px @≤360px — known accepted trade-off (load-bearing for Button 2).
- (f) Accepted tensions carried (unchanged): single-item homepage BreadcrumbList; 12 over-cap verbatim anchors; short legal titles (verbatim wins).

## PER-PAGE TABLE (fresh this round)

B2 bottoms are at scroll-0; folds: 900 @1440, 844 @390, 568 @320. Overflow = document scrollWidth vs viewport. Images = rendered/total at desktop.

| Route | Main words | B2 1440 | B2 390 | B2 320 | Overflow | Console | Images |
|---|---|---|---|---|---|---|---|
| / | 2097 | 559.1 | 536.9 | 444.6 | 0 | 0 | 20/20 |
| /about | 931 | 575.4 | 652.7 | 457.4 | 0 | 0 | 1/1 |
| /basement-flooding-cleanup | 1676 | 575.4 | 695.2 | 518.7 | 0 | 0 | 4/4 |
| /burst-pipe-water-damage | 1842 | 575.4 | 695.2 | 518.7 | 0 | 0 | 4/4 |
| /ceiling-water-damage | 1615 | 575.4 | 695.2 | 481.2 | 0 | 0 | 4/4 |
| /commercial-water-damage | 1668 | 575.4 | 695.2 | 481.2 | 0 | 0 | 4/4 |
| /condo-apartment-water-damage | 1729 | 662.7 | 768.2 | 556.2 | 0 | 0 | 4/4 |
| /contact | 751 | 543.1 | 622.1 | 457.4 | 0 | 0 | 1/1 |
| /crawl-space-water-damage | 1635 | 575.4 | 695.2 | 518.7 | 0 | 0 | 4/4 |
| /disclaimer | 309 | 423.5 | 500.5 | 368.7 | 0 | 0 | 1/1 |
| /emergency-water-extraction | 1776 | 607.7 | 652.7 | 481.2 | 0 | 0 | 4/4 |
| /hardwood-floor-cabinet-drying | 1759 | 575.4 | 695.2 | 481.2 | 0 | 0 | 4/4 |
| /locations/cottonwood-heights-ut | 1746 | 575.4 | 695.2 | 518.7 | 0 | 0 | 4/4 |
| /locations/magna-ut | 1805 | 607.7 | 695.2 | 481.2 | 0 | 0 | 4/4 |
| /locations/south-salt-lake-ut | 1823 | 575.4 | 737.7 | 518.7 | 0 | 0 | 4/4 |
| /midvale-water-sewer-emergency-contacts | 1251 | 543.1 | 652.7 | 443.7 | 0 | 0 | 1/1 |
| /mold-remediation | 1684 | 575.4 | 652.7 | 443.7 | 0 | 0 | 4/4 |
| /privacy-policy | 524 | 423.5 | 500.5 | 368.7 | 0 | 0 | 1/1 |
| /resources/basement-flooding-spring-snowmelt-utah | 1468 | 598.1 | 768.2 | 518.7 | 0 | 0 | 1/1 |
| /resources/can-mold-grow-in-utah | 1449 | 543.1 | 695.2 | 481.2 | 0 | 0 | 1/1 |
| /resources/frozen-pipes-midvale | 1656 | 575.4 | 664.6 | 532.4 | 0 | 0 | 1/1 |
| /resources/upstairs-unit-leak-who-pays-utah | 1517 | 575.4 | 737.7 | 518.7 | 0 | 0 | 1/1 |
| /resources/winterize-swamp-cooler-utah | 1503 | 543.1 | 695.2 | 481.2 | 0 | 0 | 1/1 |
| /sewage-backup-cleanup | 1715 | 575.4 | 652.7 | 481.2 | 0 | 0 | 4/4 |
| /storm-flood-damage | 1625 | 607.7 | 695.2 | 481.2 | 0 | 0 | 4/4 |
| /swamp-cooler-leak-water-damage | 1631 | 575.4 | 695.2 | 518.7 | 0 | 0 | 4/4 |
| /terms-of-use | 470 | 423.5 | 500.5 | 368.7 | 0 | 0 | 1/1 |
| /water-damage-repair | 1531 | 575.4 | 695.2 | 518.7 | 0 | 0 | 4/4 |
| /water-heater-leak-cleanup | 1693 | 575.4 | 695.2 | 518.7 | 0 | 0 | 4/4 |
| /water-leak-detection | 1737 | 575.4 | 737.7 | 518.7 | 0 | 0 | 1/1 |
| /window-well-flooding | 1763 | 575.4 | 652.7 | 481.2 | 0 | 0 | 4/4 |

## COORDINATOR SPOT-CHECKS (my own, not the workers')
- Fresh export exit 0; data sha256 unchanged; 0 localhost in out/; 0 double-slash absolute URLs.
- W1: re-grepped localhost 0, double-slash 0, robots (Allow: / + no Host: + Pages-URL Sitemap), sitemap 31 locs, 404 exactly 1 noindex, home index,follow, JSON-LD 178 blocks, visible paren 0.
- W2: re-aggregated qa/final5-render-desktop.json — 31 routes, B2 worst 662.7 (condo), buttons 322×56 equal, overflow 0, console 0, failed local 0, images 107/107, H1 1/page, tap_small none, body font 19px everywhere. Viewed the stitched full-page homepage screenshot (1440×12062): styled throughout, no blank areas, all images rendered; the two wrong card photos visible in "Nearby Cities" (TRAX train / subdivision) — confirms P2-1/P2-2 in the live render.
- W4: viewed cards/south-salt-lake-ut.webp (TRAX train — confirms P2-1) and cards/magna-ut.webp (newer subdivision, no Main Street — confirms P2-2) full-size; read the card alts in lib/content.ts (451 area: south-salt-lake "Apartment blocks and warehouse buildings", magna "Older brick homes and storefronts on historic Main Street"); viewed body/mold-remediation-2.webp (foggy white — confirms P3-1).
- W3: re-aggregated qa/final5-render-mobile.json — B2 worst 768.25 @390 / 556.19 @320 (condo), B2 visible 31/31 both widths, H1 1+visible 31/31 both widths, overflow none. Read the adjudication file: menu 3/3 pass:true with scrollLocked:true + scroll restored to 600. Viewed the condo @320 screenshot myself: both buttons fully visible at scroll-0, breadcrumb truncated cleanly.

## WORKER ARTIFACTS ADJUDICATED (not defects)
- W1: two checker bugs, both caught by its own output and fixed before concluding — (1) fullness step decomposed `<script>` tags from shared soup objects, so JSON-LD/FAQ-schema checks first saw 0 scripts; (2) annotation anchor-text extractor over-captured whole table rows/sentences, misclassifying 14 body-links. Re-ran clean; annotation reconciliation verified exactly (143/22 split, 3 duplicate-annotation cases confirmed by hand).
- W2: run 1 measured the wrong buttons (header has no help button) + counted lazy below-fold images as broken; run 2 browser died mid-run (Chromium target crash); run 3 (fresh browser per route) completed 31/31. The 6 "broken" images were re-verified with a slow scroll — all load (lazy-load timing, not defects). Home + hardwood full-page captures crashed twice each (Page.captureScreenshot on ~10–12k px pages) — worked around with segmented captures stitched with PIL; both PNGs are full-page.
- W3: run 1 crashed (headless-shell SIGILL/CFI) — switched to full Chromium + crash-resume; adjudication v1 crashed (Target crashed) — rewrote with fresh browser per route + retries. Run-1 totals held four measurement artifacts, all re-measured: (i) 138 "broken" images were lazy below-fold at scroll-0 — 107/107 after scroll-through; (ii) font sample included .eyebrow — body copy is 19px everywhere; (iii) menu scroll-lock assertion was wrong (position:fixed makes scrollY read 0 by design) — corrected check passes 3/3 (adjudication file shows pass:true, scrollLocked:true); (iv) swipe results index-misaligned on mixed pages — re-measured per-wrapper, all swipe. Raw run-1 data preserved untouched in the JSON.
- W4: first A4 selector assumed a mold-remediation menu link (menu has only 3 links) — fixed to a real menu link, re-ran. First A6 selector was a loose static-HTML regex — corrected with a live-DOM probe to a genuine `<p>`-wrapped body link. One transient Chromium "Target crashed" on a re-run — completed cleanly on retry, environment flake.

## FILES
- qa/FINDINGS-final-friendly-2026-11-13.md (this file)
- qa/final5-static.json + qa/final5-static.py (W1)
- qa/final5-render-desktop.json + qa/final5-desktop-render.py + qa/final5-followup.py (W2); screenshots qa/render-final5/desktop/ (31 PNGs, incl. stitched full-page home + hardwood)
- qa/final5-render-mobile.json + qa/final5-render-mobile-adjudication.json (W3); screenshots qa/render-final5/mobile390/ + qa/render-final5/mobile320/ (34 PNGs each)
- qa/final5-clicks-speed.json + qa/final5-run.py (W4); image screenshots qa/final5-img-01…12.png (+ 2 diagnostic hero shots)
- Server log: /tmp/final5-serve.log (port 8350, subpath mirror)

## CHAIN STATUS
- Stage 5 verdict: NOT READY FOR RE-PUSH (P2 ×2). The 2 P2s are one-photo swaps each (card → matching hero crop). A fix agent should swap them (or, weaker, rewrite the two card alts), then a fresh targeted re-verification (both cards viewed full-size in the rendered homepage + location pages, alt match, regression spot-check) must confirm PROBLEMS 0.
- P3s: P3-1 cosmetic (swap only if a stronger fogging photo exists); P3-2 lab speed (re-measure on real hosting); P3-3/P3-4/P3-5 observations, no action.
- After the P2 fix + re-verification: the whole 6-hour watchdog chain is DONE and the build is ready for re-push — on his word + token only. No push made. Local only.
