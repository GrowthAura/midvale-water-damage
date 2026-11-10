# FINDINGS — Midvale UT 10x PASS B: Technical SEO / Google (2026-11-10)

Role: PASS B, independent. Tested FRESH from the live local export
(`~/workspace/midvale-water-damage/out/`), never from the last report.
TEST ONLY — no site code, content, CSS, or image was edited.

Method: own fresh scripts (did not re-run `qa/hero-az-check.py`):
- `qa/10x/pass-b.py` — HTTP crawl on port 8332 (own extensionless-route
  mapping server; plain `http.server` 404s extensionless routes, so the
  mapping server is required), canonical/sitemap/robots/titles/H1/FAQ/
  og+twitter/links/contamination.
- `qa/10x/pass-b-browser.py` — Playwright headless Chromium (1440×900),
  H1 visibility + JSON-LD parse in a real render.
- Raw results: `qa/10x/pass-b.json`, `qa/10x/pass-b-browser.json`.
- Base URL in this build is the localhost placeholder `http://localhost:3000`
  (no real domain yet). All consistency checks are against THAT base; the
  placeholder itself is NOT flagged as a defect.

## VERDICT — PROBLEMS 0

Every numbered check below passed with positive counts (no vacuous "0" gates).

## 1. HTTP + slash form — 21/21

- HTTP 200 on all 21 routes, served from `out/` on port 8332.
- Slash probe: `/emergency-water-extraction/` → **404** (expected under
  `trailingSlash:false`; slash forms are never linked or canonicalised —
  recorded, NOT a defect). Homepage `/` → 200. `//` → 200 (server quirk,
  not a route).

## 2. Self-canonical — 21/21

- Exactly **1** canonical per page on all 21 pages (count set {1}).
- Every canonical == sitemap form against the placeholder base, including
  homepage keeping its trailing slash: `http://localhost:3000/`.
- All 20 inner pages: no trailing slash in canonical, matching sitemap.

## 3. Sitemap — 21 locs, lastmod REALLY present

- `sitemap.xml` HTTP 200, parses cleanly as XML.
- **21 locs**, exactly the 21 routes — 0 missing, 0 extra.
- **`<lastmod>2026-11-10</lastmod>` on ALL 21 locs** — date-only
  `YYYY-MM-DD`, verified in the BUILT file (this was the Round-2 false
  claim: the old sitemap had no lastmod at all; this time the built file
  was read directly — 21/21 present, 0 missing, single distinct value
  `2026-11-10`).
- No `<image:>` entries. No noindex URL inside (no page on the site is
  noindex except `404.html`, which is NOT in the sitemap — see O2).

## 4. robots.txt — PASS

- HTTP 200. Body, verbatim:
  `User-agent: *` / `Allow: /` / `Sitemap: http://localhost:3000/sitemap.xml`
- `Allow: /` present. **No `Host:` line.** Sitemap line present and
  consistent with the placeholder base.

## 5. Titles + meta descriptions — 21/21 unique, homepage verbatim

- Titles unique **21/21**; descriptions unique **21/21** (0 duplicates).
- Homepage title verbatim vs `frozen-doc.txt` line 2:
  `Water Damage Restoration Midvale UT | 24/7 Emergency Crew Dispatched Now`
  — **72 characters**, kept verbatim (over 60, NOT rewritten — his call).
- Homepage description verbatim vs doc line 3 (138 chars):
  `24/7 water damage restoration in Midvale, UT 84047. Extraction, drying,
  sewage and mold cleanup. Crew dispatched now. Call (385) 337-3560.`
- Inner titles all follow `<H1> | Water Damage Restoration Midvale UT`
  (69–85 chars). Full titles listed in `qa/10x/pass-b.json`.

## 6. H1 — exactly 1, visible, verbatim — 21/21

- DOM count: exactly **1** `<h1>` per page on all 21 pages.
- Real-browser render (Playwright, 1440×900): H1 visible on **21/21** —
  non-zero box (880px wide, 55–110px tall), `display` not none,
  `visibility` visible, opacity 1, colour `rgb(255, 255, 255)` on all 21,
  positioned y=192 (home) / y=240 (inner pages), in viewport.
- Homepage H1 verbatim vs doc: `24/7 Water Damage Restoration in Midvale, UT 84047`.
- Inner H1s are doc-derived (`<service anchor> in Midvale, UT`,
  `Water Damage Restoration <City>, UT`, guide H1 = its doc title) —
  see per-route table below. Source check: `app/[slug]/page.tsx:24`
  builds H1 as `` `${service.anchor} in Midvale, UT` `` from the doc
  service anchors.

## 7. FAQ — 6/6 visible = schema — PASS

- Homepage only (no other page carries FAQ schema — verified 0 elsewhere).
- FAQPage JSON-LD: **6** `mainEntity` entries, parses with 0 errors.
- Visible FAQ H3 questions: **6**, and the schema question list ==
  the visible H3 list, in the same order.
- All 6 accepted answers' text found in visible body text (first-60-chars
  match per answer).
- All JSON-LD blocks on all 21 pages parse with 0 errors (home: 4 blocks —
  HomeAndConstructionBusiness, FAQPage, WebSite, BreadcrumbList; services:
  Service + BreadcrumbList; guide: BreadcrumbList only).

## 8. og:image + twitter:image — own hero — 21/21

- `og:image` == the page's OWN hero URL on **21/21**; `twitter:image` ==
  the same on **21/21**; `twitter:card` == `summary_large_image` on 21/21.
- The hero `<img>` in the page body is that page's own hero file on 21/21
  (first hero img src checked per page).
- All 21 hero files exist on disk in `out/images/heroes/` (31–182 KB each).
  No hero is another page's file: e.g. home → `home.webp`, emergency →
  `emergency-water-extraction.webp`, Cottonwood → `cottonwood-heights-ut.webp`.

## 9. Links — 0 broken, 0 orphans, 0 self-links (body copy)

- Crawl: **21 distinct internal href paths** checked; every one resolves
  HTTP 200 (page routes) or exists on disk (assets: `/images/…`,
  `/_next/…`, `/favicon.svg`).
- **Broken links: 0. Orphan routes: 0** — all 21 routes reachable from the
  homepage crawl.
- **Self-links in body copy: 0.** Body copy was scoped by a parent-walk
  (inside `<main>`, excluding header/footer/nav/breadcrumb ancestors —
  see "Script errors owned" below for why the scoping matters).
- **One link per target per page in body copy: PASS**, with the documented
  exception: `/condo-apartment-water-damage` IS linked twice on the
  homepage (service card + insurance paragraph) — verified present exactly
  2×, kept as expected, NOT a defect.
- No page links to a route that does not exist (every internal href target
  is one of the 21 routes, a same-page `#fragment`, a `tel:` link, or an
  existing asset).
- Anchor word counts (body copy only): all body-copy anchors are 3–5 words
  EXCEPT 3 anchors, all doc-verbatim titles — NOT defects (rewriting them
  would break the verbatim rule, which outranks the anchor-length guideline):
  - `Mold Remediation` (2 words, `/mold-remediation`) — doc service name,
    `frozen-doc.txt:41-42`.
  - `Midvale Water & Sewer Emergency Contacts` (6 words) — doc guide title,
    `frozen-doc.txt:94`.
  - `Water Damage Restoration South Salt Lake` (6 words,
    `/locations/south-salt-lake-ut`) — doc area line, `frozen-doc.txt:98`.
  - Breadcrumb `Home` (1 word) and hub links (`See all Midvale services`,
    4 words) are navigation, exempt per the task.

## 10. Contamination sweep — 0

- Grepped whole `out/` + shipped source (`app/`, `lib/`, `components/`,
  `public/`, `next.config.mjs`) — including CSS comments, JS, schema,
  sitemap, robots — for: Tulsa, 918, Edmond, Plano, Pleasant Grove,
  Lancaster, Fort Myers, McDonough, Broken Arrow, Owasso, Naples,
  Tukwila, `918-395-9320`, `tulsawaterdamage`, Oklahoma, Texas.
  **0 hits.**
- "AI" word: whole-token match over all image filenames, all `<img>` srcs
  and alts on all 21 pages, and all image metadata (below). **0 hits.**
  (Substring matching would false-positive on `water-damage-rep**ai**r.webp` —
  not counted.)
- Image metadata (exiftool, all 40 files in `out/images/heroes/` +
  `out/images/cards/`): only File / RIFF / Composite tags (dimensions,
  WebP version). **No EXIF, no XMP, no GPS, no prompt, no Comment/
  Description/Artist/Software tags.** Full-tag grep for
  tulsa/918/edmond/plano/oklahoma/texas/ai/artificial/openai/midjourney/dall:
  **0 hits.**

## 11. Noindex — PASS

- Meta robots on all 21 routes: `index, follow` (single value site-wide).
- No noindex page is in the sitemap. The only noindex on the site is
  `out/404.html` (correct for an error page) — see O2 for a trivial
  duplicate-meta note on that file.

## Per-route table

| Route | 200 | Canonical | Title len | H1 | og:image (own hero) | Issues |
|---|---|---|---|---|---|---|
| / | 200 | http://localhost:3000/ | 72 | 24/7 Water Damage Restoration in Midvale, UT 84047 | /images/heroes/home.webp | — |
| /emergency-water-extraction | 200 | http://localhost:3000/emergency-water-extraction | 79 | Emergency Water Extraction in Midvale, UT | /images/heroes/emergency-water-extraction.webp | — |
| /basement-flooding-cleanup | 200 | http://localhost:3000/basement-flooding-cleanup | 78 | Basement Flooding Cleanup in Midvale, UT | /images/heroes/basement-flooding-cleanup.webp | — |
| /window-well-flooding | 200 | http://localhost:3000/window-well-flooding | 73 | Window Well Flooding in Midvale, UT | /images/heroes/window-well-flooding.webp | — |
| /burst-pipe-water-damage | 200 | http://localhost:3000/burst-pipe-water-damage | 76 | Burst Pipe Water Damage in Midvale, UT | /images/heroes/burst-pipe-water-damage.webp | — |
| /sewage-backup-cleanup | 200 | http://localhost:3000/sewage-backup-cleanup | 74 | Sewage Backup Cleanup in Midvale, UT | /images/heroes/sewage-backup-cleanup.webp | — |
| /water-heater-leak-cleanup | 200 | http://localhost:3000/water-heater-leak-cleanup | 78 | Water Heater Leak Cleanup in Midvale, UT | /images/heroes/water-heater-leak-cleanup.webp | — |
| /swamp-cooler-leak-water-damage | 200 | http://localhost:3000/swamp-cooler-leak-water-damage | 83 | Swamp Cooler Leak Water Damage in Midvale, UT | /images/heroes/swamp-cooler-leak-water-damage.webp | — |
| /ceiling-water-damage | 200 | http://localhost:3000/ceiling-water-damage | 73 | Ceiling Water Damage in Midvale, UT | /images/heroes/ceiling-water-damage.webp | — |
| /crawl-space-water-damage | 200 | http://localhost:3000/crawl-space-water-damage | 77 | Crawl Space Water Damage in Midvale, UT | /images/heroes/crawl-space-water-damage.webp | — |
| /hardwood-floor-cabinet-drying | 200 | http://localhost:3000/hardwood-floor-cabinet-drying | 84 | Hardwood Floor & Cabinet Drying in Midvale, UT | /images/heroes/hardwood-floor-cabinet-drying.webp | — |
| /condo-apartment-water-damage | 200 | http://localhost:3000/condo-apartment-water-damage | 83 | Condo & Apartment Water Damage in Midvale, UT | /images/heroes/condo-apartment-water-damage.webp | — |
| /commercial-water-damage | 200 | http://localhost:3000/commercial-water-damage | 76 | Commercial Water Damage in Midvale, UT | /images/heroes/commercial-water-damage.webp | — |
| /storm-flood-damage | 200 | http://localhost:3000/storm-flood-damage | 71 | Storm Water Damage in Midvale, UT | /images/heroes/storm-flood-damage.webp | — |
| /mold-remediation | 200 | http://localhost:3000/mold-remediation | 69 | Mold Remediation in Midvale, UT | /images/heroes/mold-remediation.webp | — |
| /water-leak-detection | 200 | http://localhost:3000/water-leak-detection | 73 | Water Leak Detection in Midvale, UT | /images/heroes/water-leak-detection.webp | — |
| /water-damage-repair | 200 | http://localhost:3000/water-damage-repair | 72 | Water Damage Repair in Midvale, UT | /images/heroes/water-damage-repair.webp | — |
| /midvale-water-sewer-emergency-contacts | 200 | http://localhost:3000/midvale-water-sewer-emergency-contacts | 78 | Midvale Water & Sewer Emergency Contacts | /images/heroes/midvale-water-sewer-emergency-contacts.webp | — |
| /locations/cottonwood-heights-ut | 200 | http://localhost:3000/locations/cottonwood-heights-ut | 85 | Water Damage Restoration Cottonwood Heights, UT | /images/heroes/cottonwood-heights-ut.webp | — |
| /locations/south-salt-lake-ut | 200 | http://localhost:3000/locations/south-salt-lake-ut | 82 | Water Damage Restoration South Salt Lake, UT | /images/heroes/south-salt-lake-ut.webp | — |
| /locations/magna-ut | 200 | http://localhost:3000/locations/magna-ut | 72 | Water Damage Restoration Magna, UT | /images/heroes/magna-ut.webp | — |

## Observations (NOT counted as problems — recorded for the parent)

- **O1 — Homepage `og:url` lacks the trailing slash.** Homepage canonical
  is `http://localhost:3000/` (correct, matches sitemap) but `og:url` is
  `http://localhost:3000` (no slash). All 20 inner pages have
  `og:url` == canonical exactly. The canonical tag — the authoritative
  signal — is correct on all 21 pages, so this is a cosmetic inconsistency
  (Next.js metadata normalises the root slash away; fixable with explicit
  tags, as was done for canonicals on the Chesterfield build), not a
  canonicalisation defect. Parent's call whether to fix.
- **O2 — `out/404.html` carries two `<meta name="robots">` tags:**
  `noindex` AND `index, follow`. The page is correctly absent from the
  sitemap and not linked anywhere; Google applies the most restrictive
  directive when robots tags conflict, so it stays non-indexed in practice.
  Trivial, error-page-only, not one of the 21 routes.

## Script errors owned (NOT site defects)

- **Run 1 of `pass-b.py` reported 21 false "duplicate body link" problems.**
  Root cause was MY script: "in body" was tested with
  `a in main.descendants`, which counted breadcrumb `Home` links and the
  `See all Midvale services` hub link (and, on the homepage, a footer link)
  as body copy. Fixed by replacing it with an explicit parent-walk that
  excludes header/footer/nav/breadcrumb ancestors. Re-ran fresh from the
  same export: **0 problems**. The site was never at fault; no defect was
  invented to show work.
- The anchor word-count notes in run 1 included 40 breadcrumb `Home`
  (1-word) hits — breadcrumb is exempt navigation, correctly excluded
  after the fix; the 3 remaining out-of-range anchors are the doc-verbatim
  titles listed in §9.

## Prior-round claims — re-verification

| Prior claim | This pass |
|---|---|
| 21/21 routes 200 | Confirmed 21/21 |
| Self-canonical = sitemap form | Confirmed 21/21, exactly 1/page |
| Sitemap 21 locs + date-only lastmod on every loc | Confirmed — built file read directly, 21/21 `<lastmod>2026-11-10</lastmod>` (Round 2's claim on this point was wrong; this one is verified against the built file) |
| robots Allow:/, no Host: | Confirmed |
| FAQ 6/6 = schema | Confirmed (schema Qs == visible H3s, answers in visible text) |
| og:image = own hero 21/21 | Confirmed (+ twitter:image 21/21) |
| 0 broken / orphan / self-links | Confirmed (21 internal paths, 0 broken, 0 orphans, 0 body self-links) |
| Contamination 0 | Confirmed (text + filenames + alt + image metadata) |

## PASS B — PROBLEMS: 0
