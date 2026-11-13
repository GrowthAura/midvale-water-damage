# CYCLE 1 — SCHEMA RE-AUDIT — Midvale UT — 2026-11-13

Auditor: Cycle 1 schema re-auditor (audit-only — no site source file modified).
Scope: all JSON-LD in `out/` on the fresh export (exit 0,
`NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`, no trailing slash).
Data gate: `lib/pages-data.json` sha256
`21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — **MATCHES**,
audit proceeded.

## VERDICT: PROBLEMS 0 (P1 0 / P2 0 / P3 0)

Stage 4's 178 blocks re-verify clean from the raw files on the fresh export.
Honest-only trace: **0 invented facts**. Six further-advancement candidates
below (C-1 strongest, C-3 largest at 76 blocks). Live-validator confirmation
(Google Rich Results Test) still needs the live URL after push — no live
validator exists in this VM.

## 1. Counts (verified from raw files, not from Stage 4's report)

| Type (top-level) | Count | Expected |
|---|---|---|
| BreadcrumbList | 31 | 31 |
| FAQPage | 28 | 28 |
| WebPage | 31 | 31 |
| ImageObject | 31 | 31 |
| HowTo | 36 | 36 |
| Service | 19 | 19 |
| HomeAndConstructionBusiness | 1 | 1 |
| WebSite | 1 | 1 |
| **Total** | **178** | **178** |

Nested (not top-level): Question 142, Answer 142, HowToStep 233, ListItem 64,
SpeakableSpecification 31, City 23, PostalAddress 23, inline
HomeAndConstructionBusiness providers 19 (total 20 incl. standalone).
`404.html` carries 0 blocks (correct). Per-file counts match Stage 4's table
exactly (7 on `/`, 8 on `/water-leak-detection`, 3 on each legal page, etc.).

## 2. Validation

- **Parse errors: 0** — all 178 blocks parse as JSON.
- **Duplicate @id definitions: 1 id, 20 definitions — see OBS-1, not a problem.**
  `#business` is defined once fully on the homepage and 19× as inline
  `provider` objects inside Service blocks. The 19 inline objects are
  byte-identical strict subsets (same name/telephone/url, zero conflicting
  values). All other 177 defined @ids are defined exactly once. This is the
  standard cross-page pattern for one business described on many pages.
- **Unresolved @id refs: 0** — 113 pure `{"@id": …}` references, all resolve.
- **Forbidden / invented keys: 0** — scanned for aggregateRating, review,
  ratingValue, priceRange, sameAs, SearchAction, potentialAction,
  hasCredential, geo, openingHoursSpecification, founder, employee, price,
  offers, streetAddress, latitude/longitude, slogan: zero hits.
- **URL problems: 0** — 655 URL strings scanned: localhost 0, double-slash 0,
  doubled subpath 0, off-base 0. Only allowed off-base URLs: the `hasMap`
  Google Maps link (matches the footer's own maps link) and `schema.org`
  `@context` values.
- **contentUrl / image URLs: 31/31 curl 200 live** (Pages URLs,
  `images/heroes/*.webp`) **and 31/31 files exist locally** — the Stage 4 P1
  doubled-subpath fix is confirmed still fixed.
- **@context: 0 bad** — every block uses `https://schema.org`.
- **BreadcrumbList:** 64 items, positions sequential 31/31, all items on-base.
  The 3 fragment items (position 2 on location pages →
  `…/midvale-water-damage/#areas`) point at `id="areas"`, which exists on the
  homepage. Names match the visible breadcrumb text (verified on Magna).
- **Speakable:** 28 FAQ pages carry `["#faq .faq-item", ".hero .intro"]`,
  3 legal pages carry `[".hero .intro"]`. `#faq .faq-item` resolves on 28/28
  (`id="faq"` present); `.hero .intro` present on 31/31.
- **WebPage @id == url: 31/31.**
- **Stage 4 P3 fix confirmed:** 23/23 City nodes carry `address` as a
  `PostalAddress` with `addressRegion` + `postalCode`.

## 3. Honest-only trace (verbatim vs `lib/pages-data.json` + rendered HTML)

| Check | Result |
|---|---|
| WebPage name == metaTitle | 31/31 |
| WebPage description == metaDescription | 31/31 |
| WebPage url == canonical | 31/31 |
| Service name == h1, serviceType == h1 | 19/19 |
| Service description == intro verbatim | 19/19 |
| Service image @id-ref resolves to hero ImageObject | 19/19 |
| Service provider @id == #business | 19/19 |
| HowTo name == doc H2 | 36/36 |
| HowTo steps == visible `<ol>` items | 233/233 |
| HowTo step name is verbatim prefix of step text | 233/233 |
| FAQPage Q + A verbatim vs visible rendered text | 142/142 |
| ImageObject caption == hero `<img>` alt verbatim | 31/31 |
| Business telephone +13853373560 == doc (385) 337-3560 | ✓ |
| Business openingHours "Mo-Su 00:00-24:00" == doc 24/7 | ✓ (metaDescription + h1 both say 24/7) |
| areaServed ZIPs 84047 / 84121 / 84115 / 84044 | all 4 confirmed present in `frozen-doc.txt` |
| **Invented facts** | **0** |

Notes on the two apparent diffs found during tracing (both resolved, not defects):

1. **FAQ, `/commercial-water-damage`** — "Do you handle sewage in commercial
   buildings?": the doc answer ends `Sewage Backup Cleanup
   (/sewage-backup-cleanup/)`. The parenthetical is a link annotation, not
   prose. The visible HTML renders it as a real link with anchor text
   "Sewage Backup Cleanup", and the LD answer matches the visible rendered
   text exactly. Correct behaviour per the documented annotation-token rule.
2. **HowTo steps** — the first pass compared LD steps against ALL `<ol>`s
   including the breadcrumb `<ol>` inside `<nav class="breadcrumb">`, which
   inflated visible counts by 2–3 per page. Re-run excluding the breadcrumb
   nav: 233 LD steps == 233 visible content `<ol>` items, exact. Three
   remaining one-character diffs were an artifact of my own tag-stripper
   inserting a space before commas; raw HTML is
   `dried</strong><span>,` which renders as `dried,` — verified, all exact.

## 4. PROBLEMS

### P1 — 0
None.

### P2 — 0
None.

### P3 — 0
None.

### Observations (not problems — no fix required)

- **OBS-1 — `#business` @id defined 20×.** 1 full definition + 19 inline
  provider subsets with identical values, no conflicts. Standard cross-page
  pattern; recorded for transparency only.
- **OBS-2 — Fragment @ids without matching DOM ids.** `#breadcrumb`,
  `#hero-image`, `#service`, `#howto-0…N` have no matching `id="…"` element
  on any page (0/31); only `#faq` resolves (28/28). JSON-LD identifiers are
  valid without DOM ids. Optional polish only — see candidate C-5.
- **OBS-3 — Hero `<img>` width/height attributes vs true file size.** The
  hero `<img>` tags say `width="1600" height="900"`, but the actual hero
  files measure **1600×1066** (PIL read, 31/31 files). Not a JSON-LD defect
  (schema carries no dimensions yet), but any future ImageObject
  width/height MUST use measured 1600×1066, never the 1600×900 attributes.
  Flagged for the web/mobile stage.

## 5. Further advancement — honest candidates Stage 4 missed

### C-1 (strongest) — WebPage `mainEntity` linkage to the page's own nodes
Each WebPage currently links only `isPartOf` (→ WebSite), `breadcrumb`
(→ BreadcrumbList) and `primaryImageOfPage` (→ hero ImageObject). **114
defined @ids are never referenced** — the `#faq` (28), `#howto-N` (36) and
`#service` (19) ids exist solely as unlinked definitions, plus the page-URL
WebPage ids. The graph mechanism is proven on this site (113/113 existing
refs resolve), so adding `mainEntity` @id-references is zero-risk.
**Exact pages:** `mainEntity` → `#faq` on the 28 FAQ pages; → `#service` on
the 19 Service pages; → `#howto-N` on the 25 HowTo pages (36 nodes). Adds
zero new claims — pure references to already-defined, already-verified nodes.

### C-2 (moderate) — WebPage subtype refinement: AboutPage / ContactPage
Both routes currently use plain `WebPage` (31 WebPage blocks, 0 AboutPage /
0 ContactPage). `/about` and `/contact` are the site's About and Contact
pages by tab/route, so the schema.org subtypes describe page purpose, not
new facts. All values carry over unchanged.
**Exact pages:** `/about` → `AboutPage`, `/contact` → `ContactPage`.

### C-3 (strong, largest) — ImageObject blocks for the 76 non-hero images
107 `<img>` in `out/`; only the 31 heroes have ImageObject. The other 76:
**57 body images** (3 each on 19 service/location pages) + **19 card images**
on the homepage. Evidence it is truthful: all 76 have non-empty alt text
(76/76), all 76 files exist locally (76/76), 76 distinct files. Card files
(`images/cards/*.webp`) are distinct files from hero files with different
alts (spot-checked 3/3 — hero alt ≠ card alt for the same service), so
`caption` = alt verbatim and `contentUrl` = absolute single-prefix URL are
truthful per image, exactly as the hero ImageObjects already do. Each new
block needs its own @id (e.g. page URL + `#body-image-N` / `#card-image-N`).
**Exact pages:** 19 service/location pages × 3 body images = 57; homepage
× 19 card images = 19. **Total 76 new blocks.**

### C-4 (moderate) — width/height on the 31 hero ImageObjects
All 31 hero files measure exactly **1600×1066** (measured from the site's
own files). `ImageObject` supports `width`/`height`. **Must use measured
1600×1066** — the hero `<img>` width/height attributes (1600×900) contradict
the true file ratio (OBS-3) and must not be copied.
**Exact pages:** all 31 pages with a hero ImageObject.

### C-5 (low / optional polish) — DOM ids matching fragment @ids
Add `id="breadcrumb"`, `id="hero-image"`, `id="service"`, `id="howto-N"` to
the corresponding existing elements so the fragment identifiers literally
resolve (today 0/31 pages have them; only `#faq` resolves, 28/28). HTML-only
change; no schema values change. Value is cosmetic — identifiers are valid
without this.
**Exact pages:** all 31 routes (breadcrumb + hero-image), 19 Service pages
(#service), 25 HowTo pages (#howto-N).

### C-6 (weak — largely redundant) — ItemList of services on the homepage
Homepage cards link 19 services (verified in `out/index.html`). An
`ItemList` with item name (= service H1, already verified verbatim) + url
(= canonical service URL) would be truthful site chrome — but it would
duplicate information already carried by the 19 Service blocks + the
WebPage/Breadcrumb graph, so marginal gain. Listed for the coordinator's
call, not recommended as a priority.
**Exact pages:** `/` only.

## 6. Deliberately NOT added (would be invented — re-checked, still rejected)

| Rejected | Reason |
|---|---|
| SearchAction / `potentialAction` on WebSite | No search endpoint exists on the site |
| Reviews / ratings / aggregateRating | No reviews or ratings in the doc |
| priceRange / offers / price | No prices in the doc |
| sameAs (social profiles) | No social profiles in the doc |
| geo / GeoCoordinates, street address | No coordinates or street address in the doc |
| logo | No logo file exists — only `favicon.svg`, which is not a business logo |
| datePublished / dateModified | No publication date in the doc |
| HowTo totalTime / supply / tool | No durations, supplies or tools stated in the doc |
| founder / employee / credentials | None in the doc |

## 7. Honest limits

- **No live validator exists in this VM.** Google Rich Results Test /
  Schema.org validator need the live URL after push. Validation here = JSON
  parsing + schema.org conformance checks run locally (structure, @id graph,
  URL shapes, live curl of all 31 contentUrls, verbatim trace vs
  `lib/pages-data.json` and vs rendered HTML).
- Audit-only: no site source file was modified. Deliverables are this file
  and `qa/opt1-schema.json` (machine-readable counts, validation results,
  trace sample, candidates). Scratch scripts live in `/tmp`
  (`opt1-schema-audit.py`, `opt1-trace.py`, `opt1-contenturls.txt`,
  `opt1-curl.txt`); the curl log is session scratch, not a deliverable.

## Verdict restated

**PROBLEMS 0 (P1 0 / P2 0 / P3 0).** The 178-block schema is valid,
fully linked where it claims to be, URL-clean, and honest-only (0 invented
facts) on the fresh export. The honest way further is C-1 (link the graph
together), C-3 (76 body/card ImageObjects), C-2 (AboutPage/ContactPage) and
C-4 (measured 1600×1066 dimensions) — all evidenced above, none invented.
