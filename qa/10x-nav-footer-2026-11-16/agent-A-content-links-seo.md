# Agent A — Content + Links + SEO — Midvale UT 10x round (nav/footer)
Date: 2026-11-16 ~05:38–06:00 PKT. Checker: Agent A (read-only; no push/deploy/token, no site edits).
Data fingerprint: `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — verified unchanged before and after all checks.
Scope checked: `out/` (Pages build, basePath `/midvale-water-damage`, served http://127.0.0.1:8908) + `out-cloudflare/` (root-relative, served http://127.0.0.1:8909) + LIVE https://growthaura.github.io/midvale-water-damage/ + LIVE https://midvale-water-damage.pages.dev (curl only).

## OVERALL VERDICT: READY — P1 0 / P2 0 / P3 0 (content/links/SEO scope)

Every check below was measured, not assumed. Two apparent mismatches found mid-run were both checker artifacts, verified and documented in place (canonical trailing slash; homepage link class) — neither is a site defect.

## 1. VERBATIM — PASS
- `qa/reverify-segments.py` on `out/`: **3,040 unique segments, 0 missing** (all 31 pages 0 missing; per-page JSON in `qa/reverify-segments.json`, re-run this round).
- Same script adapted for `out-cloudflare/` (`/tmp/reverify-segments-cf.py`): **3,040 segments, 0 missing**.
- Word diff: rendered visible `<main>` words **47,090** vs doc **47,188** = **−98 (−0.21%)**. Reconciled: 165 `(/path/)` annotation tokens are stripped from visible text by design (renderer rule, `lib/links.tsx`), while rendered chrome words (eyebrow, trust chips, hero/CTA button text, breadcrumb labels, contact-form labels) add words back. No content loss — the 3,040/3,040 segment check is the binding proof.
- H1 text on all 31 pages == data `h1` verbatim (both builds). Meta descriptions == data on all 31 pages (both builds).

## 2. FAQ — PASS, 142/142
- Schema: 28 FAQPage blocks (31 pages − 3 legal pages with 0 FAQs); every `mainEntity` Q and A matches data Q/A exactly after normalisation (stripAnnotations applied to answers in schema, same as visible): **142 schema-ok / 0 bad**, both builds.
- Visible: every FAQ Q and A found verbatim in the page's visible `<main>` text: **142 visible-ok / 0 bad**, both builds.

## 3. TABLES — PASS, 43/43
- Data table blocks: 43. Rendered `<table>` tags: **43** (both builds). Every header + cell present verbatim in its page's table text: **735/735 cells, 0 bad**, both builds.

## 4. LINKS — PASS (positive checks, no vacuous gates)
- Crawl: 1,437 `<a>` hrefs total across the 31 pages per build. Unique internal route targets: **151**, all resolve **200** on both local servers (8908 Pages, 8909 CF). Unique asset targets (img/link/script src): **120**, all 200 local, both builds.
- Live (curl): all 31 unique route targets resolve **200** on both live hosts. Live per-route: 31/31 200 + H1==1 on pages.dev; 30/31 direct-200 + homepage 301→200 on gh-pages (see note N1).
- Orphans: **0** — every route has ≥1 inbound link from another page (header/footer/nav counted out of the self-link rule but inbound accounting excludes self-links).
- Self-links in body copy: **0** `body-link` self-links; **0** `<a>` inside `<main>` (breadcrumb nav stripped out, exempt) pointing at its own route — both builds. Renderer drops self-links to plain text by design; 0 self-dropped annotations exist in the data anyway.
- Expected doc links: 164 `(/path/)` annotations in data → **162 kept + 2 dup-dropped** (home 1, `/water-heater-leak-cleanup` 1; first-occurrence-wins rule) + **0 self-dropped**. Rendered kept links present: **162/162** — 143 as `body-link` + 19 on the homepage as whole-card `card-wrap-link` (see note N2). Verified per link: target href correct AND the full expected anchor phrase is contained in the link's text.
- `(385) 468-6600` (guide page `/midvale-water-sewer-emergency-contacts`): renders as plain text `<td><span>(385) 468-6600</span></td>` in both the static HTML and the RSC payload; **no `tel:` link** wraps it. Only `tel:` href on that page is `tel:+13853373560` (business phone). NOT flagged — doc-verbatim county dispatch info, as instructed.
- Other non-business numbers are all doc-verbatim and plain text (no `tel:`): guide-page tables — Midvalley Sewer District 801-255-7321, Midvale City Public Works 801-567-7235, Cottonwood Improvement District 801-943-7671, Sandy Suburban Improvement District 801-561-7662 (also 801-255-7321 / 801-567-7235 on `/contact`). All four confirmed present in `lib/pages-data.json`. Only `tel:` anywhere on the site is `tel:+13853373560`.

## 5. H1 / TITLES / META / CANONICAL / OG / TWITTER — PASS
- H1 == 1 on **31/31 pages per build** and **31/31 live** (both hosts; gh-pages home after following its 301).
- Titles: 31 unique, all == data `metaTitle`. Meta descriptions: 31 unique, all == data. No duplicates.
- Canonical == og:url == sitemap loc on **every page, both builds and live**. Canonical form is **no-slash** (`…/about`, home `…/`), matching the sitemap exactly. (My checker's first pass expected a trailing slash and flagged 30/page — that expectation was wrong; the site's canonical/og/sitemap forms are mutually consistent, so this is NOT a defect.)
- og:title / twitter:title == metaTitle on all pages after HTML-entity unescaping (5 titles contain `&`, rendered as `&amp;` in attributes — correct escaping, not a mismatch). og:description == metaDescription; og:image present with correct per-build base on all pages.
- `localhost`: **0** refs in either build. `growthaura.github.io`: **0** in CF build. `www.waterdamagerestorationmidvale.us`: **0** in Pages build. No basePath `/midvale-water-damage` hrefs in CF build.

## 6. ROBOTS / SITEMAP / LLMS — PASS
- Robots meta: legal 3 (`/privacy-policy`, `/terms-of-use`, `/disclaimer`) = `noindex, follow`; other 28 = `index, follow` — both builds, and spot-checked live on both hosts (all 3 legal + `/mold-remediation`).
- Sitemap: **31 locs** per build and live on both hosts; covers all 31 routes exactly; lastmod date-only `2026-11-12` on all 31; **no image entries**; correct base per build; includes the 3 noindex legal URLs (owner call, not flagged).
- robots.txt: `User-Agent: *` + `Allow: /` + correct `Sitemap:` line per build, **no `Host:` line** — both builds and live on both hosts.
- llms.txt: **31 URLs** per build and live, correct base per build.

## 7. OLD-SITE TRACES — PASS, 0
- Grep over served `.html` (both builds) + full-body curl of all 31 live pages on both hosts + the `.txt` flight payloads: **0 hits** for Tulsa / 918 / (918) 578-1166 / Plano / Chesterfield / Apopka / Elyria / Belleville / Acworth / San Bruno / Pleasant Grove / Lancaster / Fort Myers / Naples / McDonough / Boynton / Broken Arrow / Cape Coral / Georgia / Florida / Oklahoma / Ohio / Pennsylvania / California / `localhost`.
- Only external domains in served HTML are the two own bases (growthaura.github.io in `out/`, www.waterdamagerestorationmidvale.us in `out-cloudflare/`). Schema-only `hasMap: https://www.google.com/maps?q=Midvale,+UT+84047` exists in LocalBusiness JSON-LD (not a rendered link, no fake address).

## 8. SCHEMA — PASS
- JSON-LD blocks: **254 per build** (matches the ~254 expectation). Types per build: HomeAndConstructionBusiness 1, FAQPage 28, WebSite 1, BreadcrumbList 31, WebPage 29, AboutPage 1, ContactPage 1, Service 19, HowTo 36, ImageObject 107. (WebPage 29 + AboutPage 1 + ContactPage 1 = 31; FAQPage 28 = 31 − 3 legal pages.)
- LocalBusiness (HomeAndConstructionBusiness, home page): telephone `+13853373560`; areaServed Midvale UT 84047, Cottonwood Heights 84121, South Salt Lake 84115, Magna 84044; no street address invented.
- **No `logo` key anywhere** in either build — no fake image/logo.
- ImageObject: 107 unique `contentUrl`s; **all resolve to real files** in `out/images/` and `out-cloudflare/images/` (0 missing, both builds).
- BreadcrumbList present on 31/31 pages with per-build correct base URLs.

## NOTES (not defects — do not re-flag)
- **N1** — gh-pages homepage bare URL `https://growthaura.github.io/midvale-water-damage` (no trailing slash) returns **301 → `…/midvale-water-damage/`** which returns 200, H1==1, correct title + canonical. Standard GitHub Pages directory redirect; the crawl's single "301" row was a curl-without-`-L` artifact.
- **N2** — Homepage's 19 service/location doc links render as whole-card links (`<a class="card-wrap-link">` wrapping H3 + paragraph) rather than `body-link`. Each link's target is correct and the full doc anchor phrase is inside the link text (verified per link, all 20 home links incl. the 1 body-link). Present and correct; class differs by design.
- **N3** — Settled owner calls, not flagged: www returns 000 (nameservers change in the morning; verified `curl … 000`); sitemap keeps the 3 noindex legal URLs; 72-char homepage meta title verbatim; basement-3 aerial photo; footer map removed / footer no longer 4-column.
- **N4** — Sitemap lastmod is uniformly `2026-11-12` on all 31 URLs (date-only ✓). Not flagged: no content change requiring a bump is in this round's scope.

## DEFECT LIST
None. P1 0 / P2 0 / P3 0.

## HOW TO REPRODUCE
- Verbatim: `python3 qa/reverify-segments.py` → `TOTAL segments: 3040 missing: 0`; CF variant `/tmp/reverify-segments-cf.py` → same.
- File checks: `/tmp/agentA_check.py` → full results `/tmp/agentA_results.json`.
- Link crawl + live: `/tmp/agentA_crawl.py` → full results `/tmp/agentA_crawl.json` (local 151 route + 120 asset targets 200; live 31 route targets 200 both hosts).
