# STAGE 4 — ADVANCED SCHEMA — FINDINGS 2026-11-13

## VERDICT: PROBLEMS 0 — READY FOR STAGE 5 (final web + mobile friendly check)

- Coordinator: Stage 4 Advanced Schema coordinator (6-hour watchdog chain, Stage 4 of 5).
- Baseline before this round: 80 JSON-LD blocks (LocalBusiness + FAQPage + WebSite + BreadcrumbList on home; Service + BreadcrumbList + FAQPage on DocPages). All valid, 0 invented facts (SEO audits 1+2).
- After this round: **178 JSON-LD blocks**, 0 parse errors, 0 invalid, 0 invented values.
- Data gate: `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — UNCHANGED through implementation, verification, fix and re-verification (checked 4×).
- No push/deploy/token/DNS. Local only.

## 1. What was added / changed per page (honest-only, nothing invented)

New shared helpers in `lib/schema.ts` (`BUSINESS_ID` = base + `/#business`,
`WEBSITE_ID` = base + `/#website`, `pageUrl()`, `heroImageObject()`,
`webPageLd()`, `howToFromBlocks()`). Wire-in: `components/doc-page.tsx` +
`app/page.tsx`. No visible rendering changed (schema `<script>` blocks only).

### New entities (99 blocks)
| Entity | Count | Source (verbatim / site chrome) |
|---|---|---|
| WebPage | 31 (every route) | name = metaTitle, description = metaDescription, url = canonical; isPartOf → WebSite @id; breadcrumb → BreadcrumbList @id; primaryImageOfPage → hero ImageObject @id; speakable cssSelector `["#faq .faq-item", ".hero .intro"]` on FAQ pages, `[".hero .intro"]` elsewhere (the site's own classes) |
| ImageObject (hero) | 31 | contentUrl = absolute single-prefix hero URL; caption = hero alt verbatim; representativeOfPage: true |
| HowTo | 36 (25 pages) | name = preceding H2 verbatim; steps = the page's `<ol>` items verbatim (annotation tokens ` (/path/)` stripped, anchor phrases kept as plain text — same rule as FAQ schema answers); bold lead = step name; NO totalTime/supply/tool |

### Upgrades to existing entities
| Entity | Change |
|---|---|
| LocalBusiness (home) | + `@id` #business, + `description` = metaDescription verbatim, + `hasMap` = the site's own footer map query (`https://www.google.com/maps?q=Midvale,+UT+84047`) |
| WebSite (home) | + `@id` #website, + `publisher` → #business @id-ref, + `inLanguage: "en-US"` |
| FAQPage (28) | + `@id` (page URL + `#faq`) |
| BreadcrumbList (31) | + `@id` (page URL + `#breadcrumb`) |
| Service (19) | + `@id` (page URL + `#service`), + `description` = page intro verbatim, + `image` → hero ImageObject @id-ref, provider + `@id` #business (inline name/telephone/url kept) |
| Service + LocalBusiness areaServed (23 City nodes) | addressRegion + postalCode wrapped into `address: { "@type": "PostalAddress", ... }` (Place.address; City is a Place subtype); values identical |

### Deliberately NOT added (would be invented)
totalTime, supply, tool, priceRange, sameAs, reviews, ratings, aggregateRating,
SearchAction/potentialAction, credentials, addresses, founder/employee.
No `potentialAction` (no site search). No `sameAs` (no social profiles in doc).

### Per-page block table (final build)
| Blocks | Routes |
|---|---|
| 7 | `/` (LocalBusiness, FAQPage, WebSite, BreadcrumbList, WebPage, ImageObject, HowTo×1) |
| 8 | `/water-leak-detection` (HowTo×3) |
| 7 | `/ceiling-water-damage`, `/commercial-water-damage`, `/condo-apartment-water-damage`, `/hardwood-floor-cabinet-drying`, `/sewage-backup-cleanup`, `/water-heater-leak-cleanup` (HowTo×2 each) |
| 6 | `/basement-flooding-cleanup`, `/burst-pipe-water-damage`, `/crawl-space-water-damage`, `/emergency-water-extraction`, `/locations/cottonwood-heights-ut`, `/locations/magna-ut`, `/mold-remediation`, `/storm-flood-damage`, `/swamp-cooler-leak-water-damage`, `/water-damage-repair`, `/window-well-flooding` (Service + HowTo×1); `/midvale-water-sewer-emergency-contacts`, `/resources/frozen-pipes-midvale`, `/resources/upstairs-unit-leak-who-pays-utah` (no Service, HowTo×2) |
| 5 | `/about` (HowTo×1), `/locations/south-salt-lake-ut` (Service, 0 HowTo), `/resources/can-mold-grow-in-utah`, `/resources/winterize-swamp-cooler-utah` (HowTo×1) |
| 4 | `/contact`, `/resources/basement-flooding-spring-snowmelt-utah` (0 HowTo) |
| 3 | `/disclaimer`, `/privacy-policy`, `/terms-of-use` (Breadcrumb + WebPage + ImageObject only; no FAQ) |
| 0 | `404.html` (correctly carries no ld+json) |

Totals: BreadcrumbList 31, FAQPage 28, WebPage 31, ImageObject 31,
HowTo 36, Service 19, HomeAndConstructionBusiness 20 (1 standalone +
19 inline Service providers), WebSite 1, PostalAddress 23. Grand total **178**.

### Count correction (coordinator-verified from data)
The design brief expected 179 (DocPage +96 incl. 36 HowTo). Actual is 178:
DocPage routes hold **35** ol blocks; the 36th ol is the homepage's own
(route `/` in pages-data), already emitted as the homepage HowTo from
PROCESS. The implementation worker implemented the spec as written rather
than inventing a 36th DocPage HowTo. **178 is the correct total.**

## 2. Independent verification (first pass) — VERDICT: NOT READY
File: `qa/FINDINGS-schema-verify-2026-11-13.md`
(verifier scripts `qa/verify-schema-2026-11-13.py` +
`qa/verify-schema-render-2026-11-13.py`, 12 screenshots in `qa/render-schema/`).

- **P1-1 (31 instances, one root cause): every ImageObject contentUrl 404.**
  `heroImageObject()` built `SITE.base + ASSET_PREFIX + hero.src`, but
  SITE.base already contains `/midvale-water-damage` → doubled subpath in
  every contentUrl. Measured 3 ways: URL-shape 31/31, curl 31/31 → 404,
  file-existence 31/31 missing. og:image/twitter:image + rendered hero
  `<img>` already used the correct single-prefix form. Coordinator confirmed
  from raw files (sample contentUrl doubled, 62 doubled occurrences in out/,
  `lib/schema.ts:28` root cause).
- **P3 (UNVERIFIED, not a fail): `postalCode` directly on City nodes**
  (19× Service + 4× LocalBusiness). schema.org examples place postalCode
  inside PostalAddress; no live validator in VM. Values all correct.
- Everything else clean: totals exactly 178, parse errors 0, duplicate @ids 0,
  unresolved refs 0, forbidden keys 0; honest-only 0 invented (WebPage
  31/31, Service 19/19, HowTo names 36/36, steps == visible `<ol>` 233/233,
  FAQPage == visible FAQ 142/142, captions 31/31, hasMap correct);
  regression green (fullness 31/31 FULL, H1 1/page, tables 43/43, links
  143+19, Button 2 31/31 @320/@390, overflow 0, console 0).
- Verifier owned its errors (§8): first contentUrl check false-passed
  (tautological comparison — caught by the independent curl-200 check);
  plain http.server 404s extensionless routes (server artifacts, re-ran with
  the mapping server); one transient ERR_INSUFFICIENT_RESOURCES @320
  re-checked OK; two parser artifacts fixed, re-run clean.

## 3. Fixes applied
- FIX 1 (P1, one line): `lib/schema.ts` contentUrl → `SITE.base + hero.src`
  (unused ASSET_PREFIX import removed; comment records the single-prefix rule).
- FIX 2 (P3): PostalAddress wrap on all 23 City areaServed nodes
  (doc-page.tsx service + location variants; app/page.tsx 4 LocalBusiness
  cities); values identical.
- Fix worker re-verified on a fresh export (exit 0, subpath-mapped serve,
  both verifier scripts re-run): contentUrl 31/31 curl 200, doubled subpath 0,
  totals 178, localhost 0, data hash unchanged, fullness 31/31 FULL,
  verbatim 0 missing, links 162, Button 2 31/31 @320/@390, overflow 0,
  console 0.
- Fix worker flagged (correctly, did not edit the verifier scripts): the
  verifier's static script still flagged 23 PROP PROBLEMS + 1 HONEST
  MISMATCH + 23 UNVERIFIED because its allowlist was written against the OLD
  shape (City: name/addressRegion/postalCode) and its extractor read
  top-level postalCode.

## 4. Fresh independent re-verification — VERDICT: READY FOR STAGE 5
File: `qa/FINDINGS-schema-reverify-2026-11-13.md`

- **PROBLEMS: 0** (P1 0, P2 0, P3 0).
- FIX 1 CLOSED: contentUrl **31/31 → 200**, doubled subpath 0, all 31 hero
  files exist.
- FIX 2 CLOSED: PostalAddress shape PASSES after the allowlist update
  (City allowlist + `address`, new PostalAddress entry with
  REQUIRED addressRegion+postalCode, areaServed extractor reads postalCode
  from inside `address`; reasoning + exact edits documented in the
  re-verification findings §3). Script shows **0 PROP PROBLEMS and
  0 HONEST MISMATCHES** on these nodes (Service areaServed 19/19 incl. a new
  value check vs LOCATIONS city/ZIPs; LocalBusiness 4/4). Raw counts:
  `"postalCode"` 23 = `"PostalAddress"` 23 = `"City"` 23.
- Full re-run: 178 blocks, parse errors 0, duplicate @ids 0, unresolved refs 0
  (30 cross-page `#website` refs, standard), forbidden keys 0, localhost 0,
  double-slash 0.
- Honest-only: WebPage 31/31, Service 19/19, HowTo names 36/36, steps 233/233,
  FAQPage == visible FAQ 142/142, captions 31/31, hasMap correct.
  **0 invented values.**
- Regression: fullness 31/31 FULL (0 missing words, 51,060 visible words),
  verbatim 0 missing, H1 1/page, title/meta verbatim, tables 43/43, links 162
  (143 body + 19 card), orphans/self-links/broken 0, visible paren 0,
  Button 2 31/31 @320 (worst 556.19px) AND @390 (worst 768.25px), overflow 0,
  console 0, 404 exactly 1 noindex with 0 ld+json, 31/31 `index, follow`.
- Render-check: homepage + 2 service + 1 location pages in Chromium
  @1440/390/320 — styled, H1s correct, Button 2 visible, 0 overflow,
  0 console errors; 12 screenshots in `qa/render-schema/`.

## 5. Coordinator's own spot-checks (final build, before sign-off)
- Data sha256 unchanged; ld+json blocks 178; doubled subpath 0; localhost 0.
- Per-type counts match exactly (incl. HomeAndConstructionBusiness 20 =
  1 standalone + 19 inline providers; PostalAddress 23).
- **contentUrl: 31 checked by my own curl against the subpath-mapped server,
  0 failures.**
- Findings files on disk: verify (17,974 B) + re-verify (18,379 B).

## 6. Open / not defects
- Maps embed still sandbox-blocked in this VM (environmental) — needs a
  real-network eyeball after push (carried from earlier stages).
- Homepage single-item BreadcrumbList + 12 over-cap verbatim anchors +
  short legal titles remain accepted tensions from SEO audits (verbatim wins).
- No live validator exists in this VM; conformance was checked against
  schema.org property rules + required-property checks + DOM/URL liveness.
  Google Rich Results Test on the live URL after push is the final external
  confirmation.
- No review-pack regen in this stage (schema-only change, no visible change).

## 7. Next
Stage 5 (final 1001% web + mobile friendly check) starts next per the
watchdog chain. No push until his word + token.
