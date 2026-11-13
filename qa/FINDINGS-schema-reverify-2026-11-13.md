# FINDINGS — Independent Schema RE-Verification, Midvale UT (Stage 4)

- **Date:** 2026-11-13 (re-verified ~11:40–12:05 PKT)
- **Verifier:** fresh independent schema re-verifier (Stage 4 of the 6-hour watchdog chain)
- **Scope:** `~/workspace/midvale-water-damage/`, LOCAL ONLY. No push/deploy/token/DNS, no source edits, no MEMORY.md / PROGRESS.md edits.
- **Method:** fresh export + fresh static parse of every `application/ld+json` block + fresh Playwright render of the served export + independent curl of every ImageObject contentUrl. Every key number re-measured from raw files / fresh greps by my own scripts (`qa/verify-schema-2026-11-13.py` — updated, see §3 — + `qa/verify-schema-render-2026-11-13.py`); raw results in `qa/verify-schema-2026-11-13.json` and `qa/verify-schema-render-2026-11-13.json`.
- **VERDICT: READY for Stage 5 — PROBLEMS 0 (P1 × 0, P2 × 0, P3 × 0).** Both fixes from the first verification are confirmed in the emitted export, not just in source. The P1 is closed (31/31 contentUrls return 200) and the P3 shape now passes the updated allowlist with 0 prop problems and 0 honest mismatches.

## 0. Export + data gate (PASS)

- Fresh export: `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage npm run export` (no trailing slash) — **exit 0**, 35/35 static pages.
- Data gate: `sha256 lib/pages-data.json` = `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — **exactly the claimed hash. PASS.**
- Served `out/` locally under `/midvale-water-damage/` (subpath-mapped server `qa/linkfix-serve.py` on 127.0.0.1:8322; plain `http.server` 404s extensionless Next routes). Served homepage confirmed Midvale: H1 `24/7 Water Damage Restoration in Midvale, UT 84047`, phone `(385) 337-3560`, homepage HTTP 200.

## 1. Block totals — claimed totals CONFIRMED (structure unchanged from first verification)

- **178 JSON-LD blocks total**: BreadcrumbList **31**, FAQPage **28**, WebPage **31**, ImageObject **31**, HowTo **36**, Service **19**, HomeAndConstructionBusiness **1**, WebSite **1**.
- Nested nodes: Question 142, Answer 142, HowToStep 233, ListItem 64, City 23, **PostalAddress 23** (new — was 0), SpeakableSpecification 31, HomeAndConstructionBusiness (nested provider) 19.
- 404 page: **0** ld+json blocks. Every block on all 31 routes + 404 parsed as JSON: **0 parse errors**.

### Per-page block table (route → counts by top-level @type)

BC=BreadcrumbList, FAQ=FAQPage, WP=WebPage, IMG=ImageObject, HowTo, Svc=Service, LB=HomeAndConstructionBusiness, WS=WebSite.

| route | blocks | BC | FAQ | WP | IMG | HowTo | Svc | LB | WS |
|---|---|---|---|---|---|---|---|---|---|
| / | 7 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |
| /404 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| /about | 5 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| /basement-flooding-cleanup | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /burst-pipe-water-damage | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /ceiling-water-damage | 7 | 1 | 1 | 1 | 1 | 2 | 1 | 0 | 0 |
| /commercial-water-damage | 7 | 1 | 1 | 1 | 1 | 2 | 1 | 0 | 0 |
| /condo-apartment-water-damage | 7 | 1 | 1 | 1 | 1 | 2 | 1 | 0 | 0 |
| /contact | 4 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| /crawl-space-water-damage | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /disclaimer | 3 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| /emergency-water-extraction | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /hardwood-floor-cabinet-drying | 7 | 1 | 1 | 1 | 1 | 2 | 1 | 0 | 0 |
| /locations/cottonwood-heights-ut | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /locations/magna-ut | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /locations/south-salt-lake-ut | 5 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 |
| /midvale-water-sewer-emergency-contacts | 6 | 1 | 1 | 1 | 1 | 2 | 0 | 0 | 0 |
| /mold-remediation | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /privacy-policy | 3 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| /resources/basement-flooding-spring-snowmelt-utah | 4 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| /resources/can-mold-grow-in-utah | 5 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| /resources/frozen-pipes-midvale | 6 | 1 | 1 | 1 | 1 | 2 | 0 | 0 | 0 |
| /resources/upstairs-unit-leak-who-pays-utah | 6 | 1 | 1 | 1 | 1 | 2 | 0 | 0 | 0 |
| /resources/winterize-swamp-cooler-utah | 5 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| /sewage-backup-cleanup | 7 | 1 | 1 | 1 | 1 | 2 | 1 | 0 | 0 |
| /storm-flood-damage | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /swamp-cooler-leak-water-damage | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /terms-of-use | 3 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| /water-damage-repair | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| /water-heater-leak-cleanup | 7 | 1 | 1 | 1 | 1 | 2 | 1 | 0 | 0 |
| /water-leak-detection | 8 | 1 | 1 | 1 | 1 | 3 | 1 | 0 | 0 |
| /window-well-flooding | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |

Table is byte-identical in structure to the first verification — the fixes changed values inside nodes, not block counts. Service = 19 routes exactly (16 service slugs + 3 location slugs). FAQPage = 28 (the 3 pages without FAQ are /disclaimer, /privacy-policy, /terms-of-use — matches data). HowTo = 36 blocks across 25 routes, 233 steps total.

## 2. P1 RE-CHECK — FIX 1 CONFIRMED CLOSED (was 31/31 contentUrl 404, now 31/31 200)

Measured three independent ways on the fresh export (not from source claims):

- (a) **curl of all 31 distinct ImageObject contentUrls against the served export: 31/31 → 200, 0 non-200.** Distinct URLs taken from the verifier JSON (`regression.image_content_urls`), each fetched as `http://127.0.0.1:8322` + the Pages path. Sample: homepage contentUrl is now `https://growthaura.github.io/midvale-water-damage/images/heroes/home.webp` (single prefix).
- (b) **Doubled subpath `midvale-water-damage/midvale-water-damage` in `out/`: 0 files** (grep over all of `out/`; also 0 of the 31 contentUrls contain the doubled segment). Was 31/31 doubled.
- (c) **File-existence check for all 31 hero files in `out/`: 31/31 exist** (resolved path under `out/images/heroes/*.webp`).
- Source read (not modified) confirms the one-line root-cause fix is in place: `lib/schema.ts` `heroImageObject()` now builds `contentUrl: SITE.base + hero.src` (comment updated: SITE.base already carries the subpath). The URL-shape rule in the verifier flags 0 problems, and the contentUrl-vs-hero-src honest check passes on all 31 pages (0 mismatches) — this time the check compares against the single-prefix form, not the tautological doubled form the first verifier had to correct in §8 of its own report.

## 3. P3 RE-CHECK — FIX 2 CONFIRMED: PostalAddress shape PASSES after the allowlist update

### What the emitted export actually contains (spot-checked from `out/`, not source)

- Service areaServed on `/emergency-water-extraction`: `{"@type": "City", "name": "Midvale", "address": {"@type": "PostalAddress", "addressRegion": "UT", "postalCode": "84047"}}`
- LocalBusiness areaServed on `/`: same shape for Midvale 84047, Cottonwood Heights 84121, South Salt Lake 84115, Magna 84044.
- Raw occurrence counts across all `out/*.html`: `"postalCode"` **23**, `"PostalAddress"` **23**, `"City"` **23** — every postalCode lives inside exactly one PostalAddress, one per City. Zero postalCode keys remain outside a PostalAddress node.
- The verifier's strict shape check counted **23 PostalAddress nodes** — 19 Service areaServed + 4 LocalBusiness areaServed — each with `addressRegion: "UT"` and the correct ZIP (4 distinct ZIPs: 84044, 84047, 84115, 84121). **0 prop problems, 0 honest mismatches** on these nodes after the allowlist update. The old P3 UNVERIFIED note is retired: the shape is now verified, not unverified.

### schema.org reasoning (why this shape is valid)

- `address` is a property of **Place** (schema.org/Place); **City is a Place subtype**, so `City.address` is a valid property use.
- `postalCode`'s schema.org domain is **PostalAddress** (schema.org/postalCode) — it does not belong directly on City, which is why the first verification flagged direct-on-City use as UNVERIFIED.
- `addressRegion`'s domain includes Place, so it is valid both on Place and inside PostalAddress; here it sits inside PostalAddress alongside postalCode, matching schema.org's own PostalAddress examples.
- Therefore `City → address: PostalAddress{addressRegion, postalCode}` is the schema.org-correct nesting, and the values are unchanged from before the fix (city names + ZIPs identical, verified against `lib/content.ts` LOCATIONS and the location pages' own data).

### Exact verifier-script edits (`qa/verify-schema-2026-11-13.py` only — check tooling, NOT site source)

1. **ALLOW — City:** `{"name", "addressRegion", "postalCode"}` → `{"name", "address", "addressRegion"}`. `postalCode` removed (domain is PostalAddress only); `address` added; `addressRegion` kept (valid Place property).
2. **ALLOW — new entry:** `"PostalAddress": {"streetAddress", "addressLocality", "addressRegion", "postalCode", "addressCountry", "postOfficeBoxNumber"}` (full standard PostalAddress property set; our nodes use addressRegion + postalCode).
3. **REQUIRED — new entry:** `"PostalAddress": ["addressRegion", "postalCode"]` (enforced by the generic required-property loop for every PostalAddress node).
4. **Replaced the old postalCode-on-City UNVERIFIED block** with a strict shape check (per block): (a) any `postalCode` key on a non-PostalAddress node is recorded as a PROP PROBLEM; (b) every City `address` must be a dict with `@type: PostalAddress`, else PROP PROBLEM; (c) every PostalAddress node is counted into `results["postal_address_nodes"]` with its addressRegion/postalCode. The old "UNVERIFIED, not a fail" recording is gone — the check now passes or fails outright.
5. **areaServed honest-check extractor (LocalBusiness):** `got_areas = {(a.get("name"), a.get("postalCode")) ...}` → reads postalCode from inside `address`: `{(a.get("name"), (a.get("address") or {}).get("postalCode")) ...}`. The old extractor would have returned `None` ZIPs after the fix and false-failed; the new one passes 4/4.
6. **New Service areaServed honest check** (the first verifier did not check Service areaServed values): for each of the 19 Service nodes, expected city/ZIP is Midvale/84047 on the 16 service pages and the page's own LOCATIONS city/ZIP (parsed from `lib/content.ts`: Cottonwood Heights 84121, South Salt Lake 84115, Magna 84044) on the 3 location pages; the check compares the full tuple `(City, name, PostalAddress, UT, ZIP)`. **19/19 pass.**
7. **Header docstring + summary print** updated to document edits 1–6 and to print the PostalAddress node count and its ZIP set.

No site source file was modified by the verifier; only `qa/verify-schema-2026-11-13.py` (check tooling) was edited, as the task authorized.

## 4. FULL RE-RUN of both verifier scripts (updated allowlist) — all gates green

Static script (`qa/verify-schema-2026-11-13.py`, fresh run on the new export):

| Check | Measured |
|---|---|
| Total blocks | **178** (BreadcrumbList 31, FAQPage 28, WebPage 31, ImageObject 31, HowTo 36, Service 19, HomeAndConstructionBusiness 1, WebSite 1) |
| Parse errors | **0** |
| Duplicate @ids (per page) | **0** |
| Unresolved @id refs | **0** (30 cross-page refs — all `WebPage.isPartOf → …/#website` on the 30 non-home pages, resolving to the homepage WebSite node; standard practice, not errors) |
| Forbidden keys | **0** occurrences of totalTime / supply / tool / priceRange / sameAs / reviews / aggregateRating / potentialAction / SearchAction |
| URL problems | **0** (0 localhost, 0 double-slash, 0 off-base, 0 doubled subpath) |
| Prop problems | **0** (incl. the new PostalAddress shape rules) |
| Unverified props | **0** (the City/postalCode UNVERIFIED is retired — see §3) |
| PostalAddress nodes | **23** (19 Service + 4 LocalBusiness) |
| Honest mismatches | **0** |
| localhost in out/ HTML/XML/TXT | **0 files** |
| Double-slash in out/ attrs | **0** |

Render script (`qa/verify-schema-render-2026-11-13.py`, Playwright against the served export): **0 console-error entries total** (see §7).

## 5. HONEST-ONLY re-check — 0 invented values (PASS)

- WebPage name/description = page metaTitle/metaDescription **verbatim on 31/31** (also equal to rendered `<title>` and meta description on 31/31).
- Service name/serviceType = page H1 verbatim, description = page intro verbatim (annotation-stripped) on **19/19**; Service areaServed city/ZIP **19/19** (new check, §3.6).
- HowTo name = preceding H2 verbatim on **36/36**; every HowToStep text = visible `ol` item text on **233/233** steps.
- ImageObject caption = hero `<img>` alt verbatim on **31/31**; contentUrl = hero src single-prefix form on **31/31** (now also 200 — §2).
- LocalBusiness: name = brand `Water Damage Restoration Midvale UT`, description = homepage metaDescription verbatim, telephone `+13853373560`, url = Pages base + `/`, areaServed = Midvale 84047 / Cottonwood Heights 84121 / South Salt Lake 84115 / Magna 84044 (all four match the location pages' own data ZIPs).
- hasMap `https://www.google.com/maps?q=Midvale,+UT+84047` = the site's own footer map embed query (same query, canonical form; verified against the rendered footer `<iframe>` src on the homepage).
- WebSite name = brand, url = Pages base + `/`, publisher = `#business` ref (defined on the same page).
- FAQPage == visible FAQ: **142/142** — every question and every answer matches the rendered `#faq .faq-item` h3 + p text and the data FAQs.
- BreadcrumbList == visible breadcrumb on **30/30** pages that render one; homepage has no visible breadcrumb nav by design and its schema BreadcrumbList is a single-item `["Home"]` (recorded, not a mismatch).
- SpeakableSpecification cssSelectors match ≥1 element in the rendered DOM on every page: `.hero .intro` **31/31** at both 320 and 390 (live Playwright check); `#faq .faq-item` matches on all 28 FAQ pages (142 items total live) and is absent only on the 3 no-FAQ pages, which correctly carry only `[".hero .intro"]`.

## 6. REGRESSION — the schema fixes broke nothing (all PASS)

Measured fresh on the new export (static parse + Playwright against the served export at 1440/390/320):

| Check | Measured |
|---|---|
| Fullness | **31/31 FULL** — data-derived expected-word multiset: **0 missing words on every page** (51,060 visible words total) |
| Verbatim | 0 missing (same multiset check; title/meta verbatim 31/31) |
| H1 | 1/page on 31/31 (static + live) |
| Title / meta description | verbatim vs data on 31/31 |
| Tables | **43/43** (data tables = rendered `<table>` count) |
| Links | total 1,344 anchors; body links (`.body-link`) **143**, image-card links **19** — matches the 143 + 19 expectation |
| Orphans | **[]** (every internal href target is one of the 31 routes) |
| Self-links | **0** body self-links |
| Broken links | **0** (every internal href resolves to a file in `out/`) |
| Visible paren ` (/` | **0 pages** |
| localhost in out/ HTML/XML/TXT | **0 files** |
| Double-slash in out/ attrs | **0** (href/src/content attributes) |
| Button 2 scroll-0 | **31/31 @390** (worst bottom 768.25px of 844px viewport) and **31/31 @320** (worst bottom 556.19px) |
| Overflow | **0px on 31/31 @320 and @390**; 0px on the 4 render pages @1440 too |
| Console errors (local) | **0** on all 31 pages @320/@390 and all render pages |
| 404 page | exactly 1 `noindex` meta (only file in `out/` containing `noindex`), **0** ld+json blocks |
| Robots | **31/31 pages exactly 1 `index, follow`** |

## 7. Render-check (real browser, served export)

Homepage + `/emergency-water-extraction` + `/burst-pipe-water-damage` + `/locations/cottonwood-heights-ut` viewed at 1440/390/320 — 12 screenshots in `qa/render-schema/` (regenerated this run). All 4 pages: styled hero, H1, both buttons, breadcrumb, trust chips render; overflow 0 at every width; console errors 0. Two screenshots viewed directly by the verifier: homepage @1440 (styled hero, H1, both buttons, trust line) and Cottonwood Heights @390 (styled, breadcrumb wraps, Button 2 fully visible at scroll-0). Live H1s confirmed: homepage `24/7 Water Damage Restoration in Midvale, UT 84047`; emergency `Rapid Emergency Water Extraction in Midvale, UT 84047`; burst pipe `Emergency Burst Pipe Water Damage Cleanup in Midvale, UT 84047`; Cottonwood Heights `24/7 Water Damage Restoration in Cottonwood Heights, UT 84121`. FAQ items live: 6 / 6 / 5 / 5 respectively.

## 8. PROBLEMS

### P1 × 0 · P2 × 0 · P3 × 0

- **P1-1 (first verification) — CLOSED.** ImageObject contentUrl double subpath: re-measured 31/31 curl 200, 0 doubled subpaths in `out/`, 31/31 hero files exist. No recurrence.
- **P3-1 (first verification) — CLOSED.** `postalCode` directly on City (23 instances, UNVERIFIED): all 23 now sit inside `address: PostalAddress`; the updated allowlist + strict shape check passes with 0 prop problems and 0 honest mismatches. Retired as UNVERIFIED — now verified.
- No new problems found in any gate. Nothing is left flagged, unverified, or deferred from this round.

## 9. Verifier's own errors — owned plainly

- **None this round.** Both verifier scripts ran clean on the first full pass after the allowlist edits (no crashes, no retries, no transient load failures — unlike the first verification, which needed a server swap and one page re-check). The serve used the persistent subpath-mapped server `qa/linkfix-serve.py` on port 8322 from the start.
- One caution carried from the first verification and re-applied here: the contentUrl-vs-hero check strips exactly one subpath from the rendered hero `src` before comparing (the rendered src already carries the subpath; `BASE + rendered src` would double-prefix and false-pass). The independent curl-200 + file-existence checks stand behind it either way.

## 10. Files produced (verification only — no site source file touched)

- `qa/FINDINGS-schema-reverify-2026-11-13.md` (this file)
- `qa/verify-schema-2026-11-13.py` — UPDATED (allowlist + PostalAddress shape check + areaServed extractor + new Service areaServed check; edits documented in §3) + `qa/verify-schema-2026-11-13.json` (re-run output)
- `qa/verify-schema-render-2026-11-13.py` (unchanged) + `qa/verify-schema-render-2026-11-13.json` (re-run output)
- `qa/render-schema/` — 12 regenerated screenshots (4 pages × 1440/390/320)
- Local serve log: `/tmp/midvale-reverify-serve.log` (ephemeral; server stopped after the run)
