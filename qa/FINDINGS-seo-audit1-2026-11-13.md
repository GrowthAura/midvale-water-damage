# FINDINGS — Midvale UT Technical SEO Audit 1 (2026-11-13)

Coordinator: SEO audit 1 coordinator (STAGE 2 of the 6-hour watchdog chain; Stage 0 photo-fill + 19px and Stage 1 UI/UX both completed PROBLEMS 0).
Method: fresh `npm run export` exit 0 (2026-11-13 ~10:24 PKT), served on the `/midvale-water-damage/` subpath, homepage confirmed Midvale (H1 + phone (385) 337-3560). Data `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` verified unchanged before and after. Four parallel audit-only workers (W1 crawl/index/meta/headings, W2 schema, W3 links/images-alt, W4 performance/mobile); coordinator re-verified every key number from the raw files + fresh greps + one in-browser spot-check (Playwright, home @390 + emergency @320). No site source file was modified by any worker or by the coordinator. No push/deploy/token/DNS.

## VERDICT: NOT SHIPPABLE AS-IS — P1 1 / P2 2 / P3 8 (total 11)

One root-cause P1 blocks any push: the `http://localhost:3000` base baked into schema + canonicals + sitemap + robots + llms. Everything else passes. A fix coordinator follows this audit; it does NOT fix anything itself.

## PROBLEMS

### P1-1 — localhost base site-wide (ONE root cause, counted once here; W1 had it as P2 x2, W2 as P1 x31)
- Schema JSON-LD: `http://localhost:3000` on **all 31 pages, 104 occurrences** (homepage 3, service pages 4, location pages 5, all others 2).
- Canonicals: **31/31** use the localhost base (self-referential, but to localhost).
- Sitemap: all **31 locs** localhost base.
- robots.txt Sitemap line: `http://localhost:3000/sitemap.xml` (a dead URL for any crawler if deployed as-is).
- llms.txt: all **31 URLs** localhost base.
- Root cause: `lib/content.ts:28` defaults the site base to `http://localhost:3000` and the export was built without `NEXT_PUBLIC_SITE_URL`. The gh-pages procedure is now "copy out/ as-is, NO rewriting" (publish_prefix.py guard refuses on basePath builds), so these localhost URLs would go **live** on any push.
- Fix: rebuild/export with `NEXT_PUBLIC_SITE_URL` set to the live URL — the GitHub Pages URL `https://growthaura.github.io/midvale-water-damage/` or the real domain once given — then re-verify schema/canonical/sitemap/robots/llms URLs. This is the known placeholder from the first push, not a surprise; it becomes a live defect the moment a push ships without the swap.

### P2-1 — Google Maps iframe loads eagerly on 28/31 routes
- The footer map iframe (`<iframe title="Map: Midvale, UT 84047" src="https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed" …>`) has no `loading="lazy"`, yet the map sits below the fold — every page view pays for the third-party embed.
- Affects 28 routes: all except the 3 location pages, which carry **no map iframe at all**.
- Correction to W4's count: W4 said 29/31 — the 29th match was `out/404.html` (which also carries the iframe), not a route. Coordinator-verified: 28 routes.
- Fix: add `loading="lazy"` to the iframe.

### P2-2 — Footer tap targets 26px tall on all 31 pages
- 25 of 30 header/footer targets per page are under 48px in height (measured in-browser @390: e.g. About 53.9x26, Privacy Policy 119.9x26, footer phone link 131.1x26; coordinator spot-check confirmed min footer height 26px).
- Mitigating facts, honestly recorded: ~16–17px gaps between links, no overlap, and all pass WCAG 2.2 AA's 24x24 minimum — hence P2, not P1.
- Fix: increase footer link padding/line-height to reach 48px height.

### P3-1 — Legal page titles short, verbatim (observation, not a fix)
- `/disclaimer` "Disclaimer" (10ch), `/terms-of-use` "Terms of Use" (12ch), `/privacy-policy` "Privacy Policy" (14ch); Terms description is 47ch. All MATCH `pages-data.json` exactly — changing them would break the verbatim rule. Coordinator decision, not a fix.

### P3-2 — Location pages' Service `serviceType` is generic (3 pages)
- `/locations/cottonwood-heights-ut`, `/locations/magna-ut`, `/locations/south-salt-lake-ut`: `serviceType` is "Water Damage Restoration" instead of the page-specific H1. Service `name` itself matches H1 exactly; truthful, just less specific.

### P3-3 — Homepage single-item BreadcrumbList, no visible breadcrumb nav
- Homepage carries a one-item BreadcrumbList (Home) with no visible breadcrumb navigation. Invisible markup, harmless.

### P3-4 — Breadcrumb Home href form (site-wide, confirm after the localhost fix)
- Visible breadcrumb Home link is `href="/midvale-water-damage"` (no trailing slash) while the schema Home item is absolute — confirm the URL form matches the visible href/canonical once P1-1 is fixed.

### P3-5 — 12 body-copy anchors over the 5-word cap (11 x 6 words, 1 x 8)
- "Water Heater & Appliance Leak Cleanup" (6 words) on 9 pages: /about, /basement-flooding-cleanup, /condo-apartment-water-damage, /crawl-space-water-damage, /emergency-water-extraction, /hardwood-floor-cabinet-drying, /water-leak-detection, /locations/south-salt-lake-ut, /resources/upstairs-unit-leak-who-pays-utah.
- "Midvale Water & Sewer Emergency Contacts" (6 words) on 2 pages: /contact, /resources/basement-flooding-spring-snowmelt-utah.
- Homepage "the Midvale Water & Sewer Emergency Contacts page" (8 words).
- All are verbatim doc titles/phrases (link-annotation anchors) — shortening them trades against the verbatim rule. Coordinator decision.

### P3-6 — Homepage linked twice in `<main>` on the 3 location pages
- Breadcrumb "Home" (→ `/midvale-water-damage`) + "Nearby Cities We Serve" (→ `/midvale-water-damage#areas`). Both are breadcrumb nav, not body copy, and target different anchors — strict-reading flag only.

### P3-7 — Header Menu button 46x46, header phone link ~47px tall (1–2px under 48px)
- Measured in-browser @390 on the homepage (coordinator spot-check confirmed: menu 46x46, header tel 151x47). All 31 pages.

### P3-8 — 10 largest images 185–341 KB (optimization only)
- Largest: `images/body/magna-ut-1.webp` 340,588 B; then `images/heroes/basement-flooding-spring-snowmelt-utah.webp` 276,840 B; `images/cards/cottonwood-heights-ut.webp` 217,136 B. Total images 11,694,402 B (107 webp). Lazy loading works (homepage loads 4/20 images at scroll-0, 391,606 B of 1,738,482 B inventory) — no per-page load problem observed.

## PASSES (all measured fresh)
- **Crawlability:** robots.txt exact content `User-agent: * / Allow: / / Sitemap: http://localhost:3000/sitemap.xml` (Allow present, no Host: line); sitemap exactly 31 locs, date-only lastmod `2026-11-12`, 0 duplicates, all 200, homepage root `/` only, others no-slash; llms.txt lists all 31 routes; 120 distinct local CSS/JS/image refs checked via server — 0 non-200.
- **Indexability:** meta robots `index, follow` on 31/31; canonical self-referential 31/31, 0 duplicate canonicals; URL form homepage `/` only, others no-slash.
- **Meta:** title + description verbatim vs `pages-data.json` character-for-character on 31/31; title lengths 10–73ch, descriptions 47–138ch; 0 duplicate titles, 0 duplicate descriptions.
- **Headings:** exactly 1 H1 per page on 31/31, text matches the doc H1 every time; 0 skipped heading levels; 0 H2 mismatches, 0 H3 mismatches vs doc blocks; no H4+.
- **Schema:** 80 JSON-LD blocks across 31 pages, 0 invalid JSON; FAQPage 142/142 exact (schema = visible = data, 28 pages with FAQs); BreadcrumbList on 31/31, positions 1..n sequential, names match the visible breadcrumb; Service on exactly 19 pages (16 services + 3 locations), `name` == page H1 on all 19; LocalBusiness (`HomeAndConstructionBusiness`) standalone on homepage (name "Water Damage Restoration Midvale UT", telephone +13853373560, areaServed 4 cities, openingHours Mo-Su 00:00-24:00 = the data's 24/7) and as `provider` inside the 19 Service schemas (same name/telephone everywhere); 0 invented facts — zero occurrences of aggregateRating/ratingValue/reviewCount/foundingDate/priceRange/price/streetAddress/hasCredential/award/sameAs in any block; all areaServed cities/ZIPs (84047/84121/84115/84044) trace to the data; no schema contradicts visible content.
- **Links:** 1,063 internal links checked on the served site, 0 broken; orphans 0 (every route has ≥5 inbound internal links); body self-links 0; link count reconciles exactly: 143 `body-link` + 19 card links = 162.
- **Images/alt:** 107 webp on disk, 107 `<img>` tags, 0 missing/empty alt, 0 non-200 src; all carry width+height (heroes 1600x900, body 1200x675, cards 800x450); 12/12 images viewed full-size match their alt text and fit their section topic (W3's sample: 6 heroes, 5 body, 1 location body).
- **Mobile:** viewport meta correct 31/31; horizontal overflow 0 at 320 AND 390 on 31/31 (in-browser scrollWidth vs innerWidth); body font 19px rendered (first/hero paragraph 18px — see Observations); tap targets measured (see P2-2/P3-7).
- **Performance (local, unthrottled loopback, 1.5 vCPU / 6 GB VM, cold cache, 2 runs each — NOISY, not field data):** FCP/LCP medians 168–336ms across 7 pages x 2 viewports; CLS 0.0 on all 14 measurements; 0 console errors, 0 failed requests apart from the Maps embed (sandbox-blocked, see Observations); render-blocking: exactly one stylesheet, 13,339 B; all JS async; 0 @font-face (system stack).

## OBSERVATIONS (not problems — no action required unless the parent wants it)
- **404 noindex is correct:** the single `noindex` hit in the build is `out/404.html`, which correctly carries `<meta name="robots" content="noindex"/>`. W1's "no noindex anywhere" wording is corrected — all 31 content routes are `index, follow`.
- **HomeAndConstructionBusiness on 20 pages, not homepage-only:** W2's wording corrected — the type appears standalone on the homepage AND as `provider` inside the 19 Service schemas (same name/telephone everywhere). Consistent, not a defect.
- **Hero lead paragraph renders 18px while body is 19px** (measured on the homepage @390; body font 19px, first `<main>` paragraph 18px). Check whether intended — Stage 0 set body text to 19px minimum.
- **Maps embed unverifiable live from this VM:** the Google Maps iframe request fails here with `ERR_TUNNEL_CONNECTION_FAILED` (sandbox blocks google.com egress). Environmental, not a site defect — needs a real-network eyeball after push (open since the fill round).
- **Local perf numbers are noisy; LCP element identity was not captured** (reported as unidentified by W4, not invented). LCP ≈ FCP on most pages, consistent with hero text/image painting at first paint.

## WORKER ERRORS OWNED (all caught, fixed, re-run — not site defects)
- W1: first run reported 59 false P1s — resource checker double-prefixed the subpath (404ing every ref) and checked `<a href>` + `#fragment` hrefs as resources; H3 comparison double-counted FAQ questions (FAQ questions already sit in `blocks` as h3). Fixed, re-ran clean.
- W2: first pass flagged 8 false positives — raw `&amp;` vs schema `&` in breadcrumb comparison (fixed with `html.unescape`); commercial FAQ item 5 "mismatch" was the link annotation rendering as an anchor in visible text and plain text in schema (exact match). Fixed, re-ran clean.
- W3: first run double-prefixed the subpath in the status check (all 1,063 links falsely broken); bs4 `Tag.__eq__` loose comparison falsely classified header nav "Home" as in-main, inflating prose links to 206 and fabricating 30 duplicate-target pages. Fixed with an identity-based parent-walk, re-ran clean (prose 176, 3 real duplicate pages).
- W4: first run used trailing-slash URLs, which the local serve script 404s for flat `.html` exports — 30 inner pages were measured as the server 404 page (impossible numbers, e.g. FCP ~30ms, no viewport meta). Caught, re-ran with the sitemap's no-slash URLs.

## PER-PAGE TABLE (problem codes; P3-4 breadcrumb-href form applies site-wide to all pages with a visible breadcrumb; P3-8 image weights is site-wide)

| Route | Problems |
|---|---|
| / | P1-1, P2-1, P2-2, P3-3, P3-5 (8w anchor), P3-7 |
| /about | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /contact | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /emergency-water-extraction | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /basement-flooding-cleanup | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /window-well-flooding | P1-1, P2-1, P2-2, P3-7 |
| /burst-pipe-water-damage | P1-1, P2-1, P2-2, P3-7 |
| /sewage-backup-cleanup | P1-1, P2-1, P2-2, P3-7 |
| /water-heater-leak-cleanup | P1-1, P2-1, P2-2, P3-7 |
| /swamp-cooler-leak-water-damage | P1-1, P2-1, P2-2, P3-7 |
| /ceiling-water-damage | P1-1, P2-1, P2-2, P3-7 |
| /crawl-space-water-damage | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /hardwood-floor-cabinet-drying | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /condo-apartment-water-damage | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /commercial-water-damage | P1-1, P2-1, P2-2, P3-7 |
| /storm-flood-damage | P1-1, P2-1, P2-2, P3-7 |
| /mold-remediation | P1-1, P2-1, P2-2, P3-7 |
| /water-leak-detection | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /water-damage-repair | P1-1, P2-1, P2-2, P3-7 |
| /locations/cottonwood-heights-ut | P1-1, P2-2, P3-2, P3-6, P3-7 (no Maps iframe) |
| /locations/south-salt-lake-ut | P1-1, P2-2, P3-2, P3-5, P3-6, P3-7 (no Maps iframe) |
| /locations/magna-ut | P1-1, P2-2, P3-2, P3-6, P3-7 (no Maps iframe) |
| /midvale-water-sewer-emergency-contacts | P1-1, P2-1, P2-2, P3-7 |
| /privacy-policy | P1-1, P2-1, P2-2, P3-1, P3-7 |
| /terms-of-use | P1-1, P2-1, P2-2, P3-1, P3-7 |
| /disclaimer | P1-1, P2-1, P2-2, P3-1, P3-7 |
| /resources/frozen-pipes-midvale | P1-1, P2-1, P2-2, P3-7 |
| /resources/winterize-swamp-cooler-utah | P1-1, P2-1, P2-2, P3-7 |
| /resources/upstairs-unit-leak-who-pays-utah | P1-1, P2-1, P2-2, P3-5, P3-7 |
| /resources/can-mold-grow-in-utah | P1-1, P2-1, P2-2, P3-7 |
| /resources/basement-flooding-spring-snowmelt-utah | P1-1, P2-1, P2-2, P3-5, P3-7 |

## EVIDENCE
- Worker evidence: `qa/seo-audit1-w1.json` (+ `qa/seo-audit1-w1.py`), `qa/seo-audit1-w2.json`, `qa/seo-audit1-w3.json` (+ `qa/w3-crawl.py`), `qa/seo-audit1-w4.json`.
- Coordinator spot-checks: robots/sitemap/llms/canonicals/H1/noindex greps; JSON-LD localhost count (104/31), FAQPage 142, Service 19, forbidden-claim grep 0; link counts 143+19=162, img 107/107 alt 0 missing, over-cap anchors 12, card anchors 19; Maps iframe 28 routes (404 corrected); in-browser Playwright spot-check (home @390: overflow 0, footer min height 26px, menu 46x46, header tel 151x47, body 19px, first paragraph 18px; emergency @320: overflow 0, console 0).
- Next: fix coordinator (P1-1 base swap needs the live-URL decision; P2-1 lazy Maps; P2-2 footer tap targets; P3s as listed), then SEO audit 2 (fresh + independent re-check) per the watchdog chain.
