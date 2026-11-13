# FINDINGS — Independent Schema Verification, Midvale UT (Stage 4)

- **Date:** 2026-11-13 (verified ~11:30–12:00 PKT)
- **Verifier:** independent schema verifier (Stage 4 of the 6-hour watchdog chain)
- **Scope:** `~/workspace/midvale-water-damage/`, LOCAL ONLY. No push/deploy/token/DNS, no source edits, no MEMORY.md / PROGRESS.md edits.
- **Method:** fresh export + fresh static parse of every `application/ld+json` block + fresh Playwright render of the served export. Every key number re-measured from raw files / fresh greps by my own scripts (`qa/verify-schema-2026-11-13.py`, `qa/verify-schema-render-2026-11-13.py`); raw results in `qa/verify-schema-2026-11-13.json` and `qa/verify-schema-render-2026-11-13.json`.
- **VERDICT: NOT READY for Stage 5 — 1 P1 defect (one root cause, all 31 pages).** Everything else verified clean; the fix is one line and re-verification is cheap.

## 0. Export + data gate (PASS)

- Fresh export: `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage npm run export` (no trailing slash) — **exit 0**, 35/35 static pages.
- Data gate: `sha256 lib/pages-data.json` = `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — **exactly the claimed hash. PASS.**
- Served `out/` locally under `/midvale-water-damage/` (extensionless-mapping server on 127.0.0.1:8322; plain `http.server` 404s extensionless Next routes, so it was replaced — see §8). Served homepage confirmed Midvale: H1 `24/7 Water Damage Restoration in Midvale, UT 84047`, phone `(385) 337-3560`, hero image 200.

## 1. Block totals — claimed totals CONFIRMED (structure, not validity)

- **178 JSON-LD blocks total** (claimed 178 — match): BreadcrumbList **31**, FAQPage **28**, WebPage **31**, ImageObject **31**, HowTo **36**, Service **19**, HomeAndConstructionBusiness **1**, WebSite **1**.
- Nested nodes: Question 142, Answer 142, HowToStep 233, ListItem 64, City 23, SpeakableSpecification 31, HomeAndConstructionBusiness (nested provider) 19.
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

Service = 19 routes exactly (16 service slugs + 3 location slugs — list verified against the table). FAQPage = 28 (the 3 pages without FAQ are /disclaimer, /privacy-policy, /terms-of-use — matches data, which has 0 FAQs there). HowTo = 36 blocks across 25 routes = the 36 `ol` blocks in the data, 233 steps total.

## 2. JSON-LD validation (PASS except the P1 URL defect in §6)

- Parse: **0 errors** on 178 blocks.
- Duplicate `@id` on the same page: **0** (checked per page).
- `@id` references: **0 unresolved**. **30 cross-page refs** — all are `WebPage.isPartOf → https://growthaura.github.io/midvale-water-damage/#website` on the 30 non-home pages, resolving to the WebSite node defined on the homepage. Recorded as observations per brief, **not errors** (standard JSON-LD practice; the homepage is the canonical home of that node). All other refs resolve on the same page (`#breadcrumb`, `#hero-image`, `#faq`, `#service`, `#howto-N`; Service `provider`/`image` are inline definitions, not dangling refs).
- Forbidden keys in any schema block: **0** occurrences of `totalTime` / `supply` / `tool` / `priceRange` / `sameAs` / `reviews` / `aggregateRating` / `potentialAction` / `SearchAction` (JSON-key search over all 178 blocks).

## 3. schema.org conformance

- Property allowlist check over every node of every used @type (WebPage, ImageObject, HowTo, HowToStep, FAQPage, Question, Answer, BreadcrumbList, ListItem, Service, HomeAndConstructionBusiness, WebSite, SpeakableSpecification, City): **0 invalid properties, 0 missing required properties**.
- Required-property spot results: FAQPage mainEntity = Question with name + acceptedAnswer Answer.text on all 28 pages; HowTo name + step[] with text on all 36; BreadcrumbList itemListElement with position/name/item on all 31; ImageObject contentUrl present on all 31 (but see P1 — the value is a 404); Service name/description present on all 19.
- URL shape (all other URLs): absolute on the Pages base, **0 localhost, 0 double-slash** in schema URLs — except the P1 below.
- **UNVERIFIED (1 pattern, 23 instances — NOT counted as a PROBLEM): `postalCode` used directly on a `City` node** — 19× Service `areaServed` + 4× LocalBusiness `areaServed`. schema.org's own `postalCode` examples place it inside `PostalAddress` (checked against schema.org/postalCode today); `addressRegion` IS a valid Place property, `postalCode`'s domain is PostalAddress. No live validator exists in this VM to confirm whether Google flags direct-on-City use, so per brief this is flagged UNVERIFIED rather than passed or failed. Suggested hardening (optional, same fix round): wrap as `address: {"@type": "PostalAddress", "addressLocality": <city>, "addressRegion": "UT", "postalCode": <zip>}`. Values themselves (city names + ZIPs) are all correct against the data.
- Other properties checked and accepted from schema.org knowledge: `representativeOfPage` (ImageObject), `speakable` + `breadcrumb` + `primaryImageOfPage` + `isPartOf` (WebPage), `hasMap` + `openingHours: "Mo-Su 00:00-24:00"` (LocalBusiness — the 24/7 encoding is sourced: doc H1 + meta both say "24/7"), `serviceType` / `provider` / `areaServed` (Service), `cssSelector` (SpeakableSpecification), `inLanguage: "en-US"`.

## 4. Honest-only (PASS except P1)

Every new string traced to doc/site source; **0 invented values** found:

- WebPage name/description = page metaTitle/metaDescription **verbatim on 31/31** (also equal to rendered `<title>` and meta description on 31/31).
- Service name/serviceType = page H1 verbatim, description = page intro verbatim (annotation-stripped) on **19/19**.
- HowTo name = preceding H2 verbatim on **36/36** (homepage HowTo name `How Our Water Mitigation Midvale 84047 Process Works` independently confirmed equal to the H2 immediately preceding `ol.steps`); every HowToStep text = visible `ol` item text with ` (/path/)` tokens stripped, anchor phrases kept as plain text, on **233/233** steps.
- ImageObject caption = hero `<img>` alt verbatim on **31/31**.
- LocalBusiness: name = brand `Water Damage Restoration Midvale UT`, description = homepage metaDescription verbatim, telephone `+13853373560`, url = Pages base + `/`, areaServed = Midvale 84047 / Cottonwood Heights 84121 / South Salt Lake 84115 / Magna 84044 (all four match the location pages' own data ZIPs).
- hasMap `https://www.google.com/maps?q=Midvale,+UT+84047` = the site's own footer map embed query (`https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed` — same query, canonical form). Verified against the rendered footer `<iframe>` src on the homepage.
- WebSite name = brand, url = Pages base + `/`, publisher = `#business` ref (defined on the same page).

## 5. SCHEMA == VISIBLE (PASS except P1 contentUrl)

- FAQPage mainEntity == visible FAQ Q&A: **142/142** — every question and every answer matches the rendered `#faq .faq-item` h3 + p text (answers compared after the same ` (/path/)` strip the renderer applies) and the data FAQs.
- HowTo steps == rendered `<ol>` items 1:1: **all 36 HowTo blocks, 233/233 steps**.
- BreadcrumbList == visible breadcrumb: **30/30 pages that render a breadcrumb** (names + positions + item URLs). Homepage has no visible breadcrumb nav by design; its schema BreadcrumbList is a single-item `["Home"]` — recorded, not a mismatch.
- SpeakableSpecification cssSelectors match ≥1 element in the rendered DOM on **every page**: `.hero .intro` matches 31/31 (live Playwright check: 31/31, 0 pages with 0 matches); `#faq .faq-item` matches on all 28 FAQ pages and is absent (0) only on the 3 no-FAQ pages, which correctly carry only `[".hero .intro"]` in their speakable selector list.
- ImageObject contentUrl returns 200 from the served export: **0/31 — FAIL, see P1.** The correct single-prefix URLs all return 200 (homepage hero checked directly: 200; all 31 hero files exist in `out/images/heroes/`).

## 6. PROBLEMS

### P1-1 — ImageObject.contentUrl double subpath prefix on ALL 31 pages (one root cause)

- **What:** every `ImageObject.contentUrl` is `https://growthaura.github.io/midvale-water-damage/midvale-water-damage/images/heroes/<slug>.webp` — the `/midvale-water-damage` subpath appears twice. E.g. homepage: schema says `…/midvale-water-damage/midvale-water-damage/images/heroes/home.webp`; the real file is at `…/midvale-water-damage/images/heroes/home.webp`.
- **Measured three independent ways:** (a) URL-shape check flags the repeated subpath on **31/31** contentUrls; (b) curl of all 31 schema contentUrls against the served export: **31/31 → 404**; (c) file-existence check of the resolved path inside `out/`: **31/31 missing**. The correct single-prefix URL returns 200.
- **Root cause (code, read not modified):** `lib/schema.ts` `heroImageObject()` builds `contentUrl: SITE.base + ASSET_PREFIX + hero.src`. `SITE.base` already IS the full Pages URL including the subpath (`https://growthaura.github.io/midvale-water-damage`), and `hero.src` is `/images/heroes/….webp`, so adding `ASSET_PREFIX` (`/midvale-water-damage`) duplicates it. The helper's comment assumes SITE.base is a bare domain — it is not.
- **Proof the rest of the site does it right:** `og:image` and `twitter:image` on the homepage are the correct single-prefix form (`https://growthaura.github.io/midvale-water-damage/images/heroes/home.webp`) — built as `SITE.base + HERO_IMAGE.home.src` in `app/page.tsx`. The rendered hero `<img src>` is likewise correct single-prefix.
- **Fix (for the schema worker, one line in `lib/schema.ts`):** `contentUrl: SITE.base + hero.src` (drop `ASSET_PREFIX`). No other schema URL is affected — WebPage url, breadcrumb items, Service url, LocalBusiness url, hasMap were all checked clean. After the fix: re-export, re-run this verifier's contentUrl checks (URL-shape + curl-200 + file-exists), and re-verify the full gate.
- **Impact:** `contentUrl` is a required ImageObject property; a 404 image URL makes all 31 ImageObject nodes (and the WebPage `primaryImageOfPage` links pointing at them) invalid for rich-result use. This is the only thing standing between the schema round and Stage 5.

### P3-1 — UNVERIFIED: `postalCode` directly on `City` (23 instances)

- See §3. Not a fail, not invented, values correct. Optional hardening in the same fix round; re-verify with the same allowlist if changed. If left as-is, note it as a known UNVERIFIED in the Stage 5 handoff.

### PROBLEMS count: P1 × 1 (31 instances, 1 root cause) · P2 × 0 · P3 × 1 (UNVERIFIED note)

## 7. Regression — schema change broke nothing (all PASS)

Measured fresh on the new export (static parse + Playwright against the served export at 1440/390/320):

| Check | Measured |
|---|---|
| Fullness | 31/31 FULL — data-derived expected-word multiset: **0 missing words on every page** (51,060 visible words total) |
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
| Button 2 scroll-0 | **31/31 @390** (worst bottom 768.25px of 844px viewport) and **31/31 @320** (worst bottom 556.19px; see §8 for the one retry) |
| Overflow | **0px on 31/31 @320 and @390**; 0px on the 4 render pages @1440 too |
| Console errors (local) | **0** on all 31 pages @320/@390 and all render pages |
| 404 page | exactly 1 `noindex` meta, **0** ld+json blocks |
| Robots | **31/31 pages exactly 1 `index, follow`** |
| Render-check (real browser) | homepage + `/emergency-water-extraction` + `/burst-pipe-water-damage` + `/locations/cottonwood-heights-ut` viewed at 1440/390/320 — styled hero, H1, both buttons, breadcrumb, trust chips all render; screenshots in `qa/render-schema/` (12 PNGs). Mobile location page: breadcrumb wraps, Button 2 fully visible at scroll-0. |

## 8. Verifier's own errors — owned plainly

1. **First static run crashed twice on my script bugs** (dict built from 3-tuples; `None` eyebrow in one data page). Both fixed in `qa/verify-schema-2026-11-13.py`; no results were claimed from the crashed runs.
2. **My first-pass ImageObject.contentUrl check was constructed wrong and FALSE-PASSED.** I compared the schema URL to `BASE + rendered <img> src`; the rendered src already contains the subpath, so that comparison tautologically reproduced the doubled URL. The defect was caught by the independent curl-200 check (31/31 404), not by that check. I fixed the checker (strip one subpath from the rendered src + add a file-existence check + add a repeated-subpath URL-shape rule) and re-ran: it now flags the defect three ways (31 URL problems + 62 honest mismatches = 31 contentUrl-vs-hero + 31 file-missing, one root cause). The numbers in this report are from the corrected re-run.
3. **First render run used a plain `python3 -m http.server`, which 404s extensionless Next routes** — every doc page "failed" (H1 `Error response`, no hero, console 404s) because of my server, not the site. Re-ran with an extensionless-mapping server (`/tmp/midvale-serve/serve.py`, since removed) and all those failures disappeared. The plain server also served the homepage fine, which is why it looked plausible at first.
4. **One transient load failure in the long render loop:** `/water-leak-detection` @320 failed once with `net::ERR_INSUFFICIENT_RESOURCES` (resource exhaustion from 62 sequential page loads in one browser). Re-checked alone in a fresh browser: Button 2 bottom 518.69px ≤ 844, overflow 0, H1 1, FAQ 5, `.hero .intro` 1, console 0 — **pass**. Not a site defect.
5. **Two of my first five "honest mismatches" were my own parser artifacts**, found and fixed before final numbers: my content.ts FAQ/PROCESS regex didn't handle multi-line objects (homepage FAQ parsed as 0), and `get_text(" ")` inserted a space before commas at inline-node boundaries (3 HowTo "mismatches" were `dried , such` artifacts). Fixed to multi-line regexes and `get_text("")` (true textContent); re-run shows 0 mismatches on those checks.

## 9. Files produced (verification only — no site source file touched)

- `qa/FINDINGS-schema-verify-2026-11-13.md` (this file)
- `qa/verify-schema-2026-11-13.py` + `qa/verify-schema-2026-11-13.json` (static checks)
- `qa/verify-schema-render-2026-11-13.py` + `qa/verify-schema-render-2026-11-13.json` (render checks)
- `qa/render-schema/` — 12 screenshots (4 pages × 1440/390/320)

Local test servers (127.0.0.1:8321/8322) started for this verification have been stopped. Other pre-existing QA servers in the VM were left untouched.

## 10. Recommended next step

Schema worker: one-line fix in `lib/schema.ts` (`contentUrl: SITE.base + hero.src`), optionally the PostalAddress wrap for `postalCode` (P3-1). Then re-export and re-run this verifier's two scripts — the contentUrl gate now fails loudly three ways if the fix is wrong. **Stage 5 should start only after a re-verification shows P1-1 closed (31/31 contentUrls 200) with no other gate regressed.**
