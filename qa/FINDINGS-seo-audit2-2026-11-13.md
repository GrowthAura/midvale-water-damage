# FINDINGS — Midvale UT Technical SEO Audit 2 (2026-11-13)

Coordinator: SEO audit 2 coordinator (STAGE 3 of the 6-hour watchdog chain; Stage 2 SEO audit 1 found 11 problems; fix 1 completed with PROBLEMS 0).
Method: my own fresh `npm run export` exit 0 (2026-11-13 ~10:52 PKT, with `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`, no trailing slash), served on the `/midvale-water-damage/` subpath (port 8342), homepage confirmed Midvale (H1 + phone (385) 337-3560). Data `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` verified unchanged before, during and after. Four parallel audit-only workers (W1 crawl/index/meta/headings, W2 schema, W3 links/images-alt, W4 performance/mobile); coordinator re-verified every key number from the raw files + fresh greps + JSON-LD re-parse + viewed the three disputed images full-size + one in-browser spot-check (Playwright, home @390 + emergency @320). No site source file was modified by any worker or by the coordinator. No push/deploy/token/DNS.

## VERDICT: SHIPPABLE — P1 0 / P2 0 / P3 5 (all minor)

Audit 1's blocking P1 (localhost base) is fixed and verified gone. All 11 audit-1 problems re-checked: 7 fixed, 2 verified non-issues, 2 carried as accepted tensions (verbatim wins). Three NEW P3s found (two alt-text mismatches, one duplicate noindex tag on 404.html). Nothing blocks a push; the 3 new P3s are quick fixes a fix coordinator can do (alt rewrites live in `lib/content.ts`, not in doc content; the 404 meta is framework output).

## AUDIT-1 RE-CHECK (all 11, fresh)

| Audit-1 item | Verdict | Evidence (coordinator-verified) |
|---|---|---|
| P1-1 localhost base | **FIXED** | 0 localhost in out/ HTML/XML/TXT; 1 occurrence total in out/ is the Next.js URL-parser polyfill chunk (`"localhost"===s.host`), framework code, not a site URL. Canonicals 31/31, og:url 31/31, sitemap 31 locs, robots Sitemap line, llms 31/31 — all on `https://growthaura.github.io/midvale-water-damage/`. Double-slash absolute URLs 0. |
| P2-1 Maps iframe lazy | **FIXED** | 29 `<iframe>` tags in out/ (28 routes + 404.html), all 29 carry `loading="lazy"`; 0 iframes on the 3 location pages. |
| P2-2 footer tap targets 26px | **FIXED** | Footer links min 48px on all 31 routes @320/390/1440 (W4 in-browser); coordinator spot-check home @390 footer min 48px. |
| P3-1 legal titles short | Carried, accepted tension | Disclaimer 10ch / Terms 12ch / Privacy 14ch — verbatim from the doc. Changing them breaks the verbatim rule. Observation only. |
| P3-2 location serviceType generic | **FIXED** | serviceType == page H1 on all 3 locations, verified by coordinator re-parse: cottonwood `24/7 Water Damage Restoration in Cottonwood Heights, UT 84121`, south-salt-lake `Emergency Water Damage Restoration in South Salt Lake, UT 84115`, magna `Local Water Damage Restoration in Magna, UT 84044`. |
| P3-3 homepage single-item BreadcrumbList | Carried (P3-4 below) | No truthful second item exists. |
| P3-4 breadcrumb Home href form | **Verified non-issue** | Schema Home item == homepage canonical exactly (`https://growthaura.github.io/midvale-water-damage/`). Visible href is Next's relative basePath form `/midvale-water-damage` — same resource. |
| P3-5 12 anchors over 5-word cap | Carried, accepted tension | Same 12 (9× "Water Heater & Appliance Leak Cleanup" 6w, 2× "Midvale Water & Sewer Emergency Contacts" 6w, 1× 8w homepage). All verbatim doc titles/anchors. |
| P3-6 homepage twice in `<main>` on 3 location pages | **Verified non-issue** | Both links are inside `<nav aria-label="Breadcrumb">` on all 3 location pages (Home → `/midvale-water-damage`, "Nearby Cities We Serve" → `/midvale-water-damage#areas`). Breadcrumb nav, not body copy. Body-copy duplicate targets 0 sitewide. |
| P3-7 menu 46x46 + header phone ~47px | **FIXED** | Menu button 48×48 @320/390 on all 31 routes; header phone 48px @390, 50.6px @1440 (hidden ≤360px by design). Coordinator spot-check home @390 menu 48×48. |
| P3-8 10 largest images 185–341 KB | **FIXED (8/10)** | All 8 re-encoded files byte-identical to fix-1 adopted q75 sizes; originals in `qa/img-opt/orig-backup/`; no banding/blocking/detail loss (W3 full-res per-channel RMS 2.85–5.08 vs backups). Largest now `body/magna-ut-1.webp` 282,352 B (was 340,588 B). Total image weight 11,694,402 B → 11,331,800 B. |

## PROBLEMS (new in audit 2 + carried)

### P3-1 — `out/404.html` carries the noindex meta tag twice (NEW, minor)
- Two `<meta name="robots" content="noindex"/>` tags in `<head>` (char 976, before `<title>`; char 1257, after it) — coordinator-confirmed by direct grep. The page IS correctly noindexed; this is a duplicate-tag nit, not an indexing leak. The duplication is also reflected twice in the RSC/flight payload. Fix: dedupe at the 404 template/framework level.

### P3-2 — Cottonwood card alt describes a different photo (NEW)
- `images/cards/cottonwood-heights-ut.webp` (homepage card): alt is "Bench homes below snowy Wasatch canyons in Cottonwood Heights, Utah" but the photo — viewed full-size by W3 AND by the coordinator — is a winding canyon highway through steep rocky autumn slopes: no homes, no snow. Alt appears copied from the hero's alt (the hero does show bench homes below snowy canyons). Photo itself is on-topic for the place; only the alt is factually wrong. Fix: rewrite the card alt to the actual scene, e.g. "Canyon highway through autumn slopes in Cottonwood Canyon, Utah" (alt text is not doc body copy).

### P3-3 — Basement-snowmelt hero alt mislocates the photo (NEW)
- `images/heroes/basement-flooding-spring-snowmelt-utah.webp` (hero of `/resources/basement-flooding-spring-snowmelt-utah`): alt is "Spring snowmelt water seeping across a Midvale basement floor" but the photo — viewed full-size by W3 AND by the coordinator — is an exterior shot: a downspout discharging meltwater onto wet ground at the house foundation base, snow piles, snowy mountains behind. No basement floor in frame. Topic fit is right (spring snowmelt threatening a basement); the literal alt is wrong about location. Fix: rewrite the alt, e.g. "Spring snowmelt water pooling at a Midvale home foundation as a downspout discharges".

### P3-4 — Homepage single-item BreadcrumbList, no visible breadcrumb nav (CARRIED from audit 1 P3-3)
- Homepage carries a one-item BreadcrumbList (Home) with no visible breadcrumb navigation. Invisible markup, harmless; no second truthful item exists.

### P3-5 — Homepage linked twice in `<main>` on the 3 location pages (CARRIED from audit 1 P3-6, observation only)
- Both links are breadcrumb nav targeting different anchors (see re-check table). Strict-reading flag only; no body-copy change.

## CLOSED — old design-round P3 superseded (coordinator-verified)
- **commercial-3 B&W photo:** does NOT apply to the current file. The coordinator viewed `public/images/body/commercial-water-damage-3.webp` full-size: it is a FULL-COLOUR photo (open office floor, wet floor, blue air movers + dehumidifier) matching its alt exactly, and no grayscale/filter rule touches it. Stage 1's UI/UX image swaps replaced the old B&W file (Stage 1 verification already noted "commercial-3 now COLOUR"). The old P3 is closed, not carried.

## PASSES (all measured fresh)
- **Crawlability:** robots.txt exact content `User-agent: * / Allow: / / Sitemap: https://growthaura.github.io/midvale-water-damage/sitemap.xml` (Allow present, no Host: line), HTTP 200; sitemap exactly 31 locs, date-only lastmod `2026-11-12`, 0 duplicates, all 200 via served subpath, homepage root `/` only, others no-slash; llms.txt lists all 31 routes on the Pages URL, HTTP 200.
- **Indexability:** meta robots `index, follow` on 31/31; canonical self-referential 31/31, 0 duplicate canonicals; URL form homepage `/` only, others no-slash (sitemap, llms, canonicals, og:url alike).
- **Meta:** title + description verbatim vs `pages-data.json` character-for-character on 31/31; title lengths 10–73ch, descriptions 47–138ch; 0 duplicate titles, 0 duplicate descriptions.
- **Headings:** exactly 1 H1 per page on 31/31, text matches the doc H1 every time; 0 skipped heading levels; H2 sequence matches doc blocks 31/31, H3 sequence 31/31 (406 H2 + 259 H3 rendered); no H4+.
- **Schema:** 80 JSON-LD blocks across 31 pages, 0 invalid JSON (coordinator re-parsed all 80); FAQPage 142/142 exact (coordinator: schema 142 = visible 142 in `#faq` sections on 28 pages = data 142; commercial FAQ item 5 exact only after stripping the doc's link annotation — same adjudicated non-issue as audit 1); BreadcrumbList on 31/31, positions 1..n sequential, names match visible breadcrumb; Service on exactly 19 pages, `name` == page H1 and `serviceType` == H1 on all 19; LocalBusiness (`HomeAndConstructionBusiness`) standalone on homepage (name "Water Damage Restoration Midvale UT", telephone +13853373560, areaServed 4 cities, openingHours Mo-Su 00:00-24:00) and as `provider` inside the 19 Service schemas (same name/telephone everywhere); 0 invented facts — 0 occurrences of aggregateRating/ratingValue/reviewCount/foundingDate/priceRange/price/streetAddress/hasCredential/award/sameAs in any block; 0 localhost in JSON-LD; all schema URLs on the Pages URL.
- **Links:** 1,063 internal anchors checked on the served site, 0 broken, 0 external; orphans 0 (inbound min 5, max 30 — identical to audit 1); body self-links 0; link count reconciles exactly: 143 `body-link` + 19 card links = 162; 33 in-main breadcrumb links classified separately.
- **Images/alt:** 107 webp on disk, 107 `<img>` tags, 0 missing/empty alt, 0 non-200 src, 0 missing width+height; W3 viewed 13 full-size (8 q75 + commercial-3 + 3 heroes + 1 body): 11 MATCH, 2 PARTIAL (the two alt P3s above — photos fine, alt wrong).
- **Mobile:** viewport meta correct 31/31; horizontal overflow 0 at 320 AND 390 AND 1440 on 31/31 (93 in-browser loads); body font 19px rendered on all 31 routes × 3 viewports; hero lead `p.intro` 19px on all 31 routes × 3 viewports (audit 1's "first paragraph 18px" was the eyebrow `p.eyebrow` — 14px @320, 18px @390/1440 — chrome, not body copy; fix 1's account confirmed by data); tap targets: footer min 48px, header nav 48px (58.6px with mobile menu opened), menu 48×48, header phone 48px @390 / 50.6px @1440 (hidden ≤360px by design); Button 2 visible at scroll-0 on 31/31 @320 (worst bottom 556.2px vs 568 fold — condo) AND @390 (worst 768.3px vs 844) — fix 1's numbers reproduce exactly; coordinator spot-check home @390 Button 2 bottom 536.9px, emergency @320 481.2px.
- **Performance (local, unthrottled loopback, cold cache, fresh context per load — LAB numbers, NOT field data):** FCP medians 612ms @320 / 628ms @390 / 736ms @1440; LCP medians 672ms @320 / 776ms @390 / 824ms @1440 (max 1,472ms, emergency-contacts @1440); CLS median 0 at all viewports (max 0.0013 @390); 0 console errors across all 93 loads; 0 failed requests apart from the Maps embed (sandbox-blocked google.com egress); LCP element identified, not invented: `IMG.hero-img` on 93/93 loads.
- **Maps:** 29 iframes, all `loading="lazy"`; embed itself does not load in this sandbox (google.com egress blocked) — environmental, needs a real-network eyeball after push (open since the fill round).

## OBSERVATIONS (not problems)
- **50/107 image files' pixel dims differ from their width/height attrs** (all heroes 1600×1066 files vs 1600×900 attrs; all cards 1200×675/800 vs 800×450) — not a defect: CSS crops into 16:9 boxes (`.hero-img`/`.card-img`/`.body-img` all `object-fit: cover` + `aspect-ratio 16/9` + `height: auto`), so nothing is squished.
- **404 noindex is correct** (see P3-1): the duplication is a nit; the page is noindexed as intended.
- **Local perf numbers are noisy;** LCP medians rose vs audit 1 (168–336ms) because W4 used fresh contexts per load (cold cache) while audit 1's W4 reused warmer contexts — methodology difference, not a regression. LCP max 1,472ms is the emergency-contacts page (no body images, heavy text) at 1440.
- **W4 recorded two exec failures (exit 1)** in its run; content not visible to the coordinator. The evidence JSON is complete (31 pages × 3 viewports, 93 loads) and the coordinator's own spot-check reproduces its headline numbers (footer 48px, menu 48×48, Button 2 bottoms, overflow 0, console 0), so there is no data gap — recorded here for honesty.

## WORKER ERRORS OWNED (all caught, fixed, re-run — not site defects)
- W1: first run double-counted FAQ questions as expected H3s (they are already h3 blocks in `pages-data.json`) and falsely flagged 28 pages. Fixed, re-ran clean (31/31 H2/H3 sequence match).
- W2: first run reported visible FAQs 136/142 (homepage FAQ `<section>` carries `class="section"` before `id="faq"`, missed by an exact-attribute regex) and 80 off-base schema URLs (counted the `https://schema.org` `@context` URI as a site URL). Fixed both, re-ran from scratch.
- W3: no script errors; audit-1 traps avoided by construction (no double-prefixing, identity-based parent-walk, URL-decoding).
- W4: no script errors in the final run (93/93 loads); see the two recorded exec failures in Observations.

## PER-PAGE TABLE (problem codes; P3-4/P3-5 are site-wide observations)

| Route | Problems |
|---|---|
| / | P3-2 (cottonwood card alt), P3-4 |
| /about | — |
| /contact | — |
| /emergency-water-extraction | — |
| /basement-flooding-cleanup | — |
| /window-well-flooding | — |
| /burst-pipe-water-damage | — |
| /sewage-backup-cleanup | — |
| /water-heater-leak-cleanup | — |
| /swamp-cooler-leak-water-damage | — |
| /ceiling-water-damage | — |
| /crawl-space-water-damage | — |
| /hardwood-floor-cabinet-drying | — |
| /condo-apartment-water-damage | — |
| /commercial-water-damage | — |
| /storm-flood-damage | — |
| /mold-remediation | — |
| /water-leak-detection | — |
| /water-damage-repair | — |
| /locations/cottonwood-heights-ut | P3-5 (observation) |
| /locations/south-salt-lake-ut | P3-5 (observation) |
| /locations/magna-ut | P3-5 (observation) |
| /midvale-water-sewer-emergency-contacts | — |
| /privacy-policy | — |
| /terms-of-use | — |
| /disclaimer | — |
| /resources/frozen-pipes-midvale | — |
| /resources/winterize-swamp-cooler-utah | — |
| /resources/upstairs-unit-leak-who-pays-utah | — |
| /resources/can-mold-grow-in-utah | — |
| /resources/basement-flooding-spring-snowmelt-utah | P3-3 (snowmelt hero alt) |
| out/404.html (not a route) | P3-1 (duplicate noindex) |

## EVIDENCE
- Worker evidence: `qa/seo-audit2-w1.json` (+ `qa/seo-audit2-w1.py`), `qa/seo-audit2-w2.json` (+ `qa/seo-audit2-w2.py`), `qa/seo-audit2-w3.json` (+ `qa/seo-audit2-w3.py`), `qa/seo-audit2-w4.json`.
- Coordinator spot-checks: data sha256 unchanged; localhost 0 in HTML/XML/TXT (1 polyfill-chunk string); double-slash 0; canonicals 31; sitemap 31 locs lastmod 2026-11-12; robots exact; llms 31; 404 noindex ×2 (chars 976 + 1257); JSON-LD re-parse 80 blocks / FAQ 142 / Service 19 / serviceType == H1 ×3 / localhost 0; visible FAQ h3 in `#faq` sections 142 on 28 pages; W3 totals re-read (1,063 anchors, 0 broken, 162 = 143+19, orphans [], 107 imgs, weight 11,331,800 B); W4 summary re-read (FCP/LCP/CLS medians, n=31 × 3 viewports); viewed full-size: commercial-3 (COLOUR — old B&W P3 closed), cottonwood card (autumn highway, no homes/snow — alt P3 confirmed), snowmelt hero (exterior downspout — alt P3 confirmed); Playwright spot-check home @390 (overflow 0, footer 48px, Button 2 536.9px, menu 48×48, intro 19px, eyebrow 18px, console 0) + emergency @320 (overflow 0, footer 48px, Button 2 481.2px).
- Next: fix coordinator for the 3 new P3s (2 alt rewrites + 404 meta dedup), then Stage 4 (advanced schema) per the watchdog chain. No push/deploy/token/DNS.
