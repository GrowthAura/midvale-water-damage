# Midvale UT — Water Damage Restoration — PROGRESS

- City: Midvale, UT 84047. Phone ONLY (385) 337-3560. Brand as in doc: "Water Damage Restoration Midvale UT".
- Stack: Next.js 14 (14.2.35, patched 14.x) static export (`out/`), App Router, TypeScript. LOCAL ONLY.
- Theme: locked Theme v2 (2026-11-04) — Tulsa EMD skeleton ONLY (section order/structure). ALL code written fresh for Midvale; zero Tulsa repo files copied. Fresh palette documented below. Zero raster images — branded SVG/CSS panels only (see Images).
- Source: Google Doc "Midvale UT" 1ZmyWIOGUbUoaM-LRuffoWeO9xmojFAQLLaJDlYhRaDQ. `doc-raw.json` + `extracted.txt` untouched. NOTE: the text extract MISSED the doc's 4-row water-category table (header + Category 1/2/3) — found in `doc-raw.json`, included verbatim on the homepage.
- Routes: 21 total = homepage `/` + 16 services + 1 guide + 3 locations (all no-slash except homepage).

## Palette (fresh for Midvale — NOT Tulsa v3 navy/emerald-gold)
- Pine `--pine: #0e3b38` (primary dark), `--pine-2: #15524c`, ink `#1b2a28`
- Copper `--copper: #c26a24` (call CTA solid), `--copper-dark: #9d5418`
- Sand `--sand: #f6f1e7`, mist `--mist: #e8efec`, line `#d9e2dd`, white `#ffffff`
- Buttons: Button 1 "(385) 337-3560" solid copper; Button 2 "Request Emergency Help" solid pine — SAME height, padding, font-size, font-weight (equal size/prominence/visibility).

## Images
- ZERO raster images on the site (0 files in `public/` except `favicon.svg` + `robots.txt`). No photo from any past site, no stock photo, no AI-generated photo. Hero + all 16 service cards + 3 area cards use fresh inline SVG/CSS branded panels (Wasatch mountain motif, per-service glyph). This is the sanctioned fallback: no fitting real/stock photo was supplied, and forcing a filler photo is a blunder. GAP NAMED: if real Midvale job photos arrive, panels can be swapped per slot.
- Favicon: fresh-drawn classic drop SVG in Midvale pine/copper (same classic drop *style*, fresh draw, new file).

## OPEN (do not guess — listed, not built)
1. DOMAIN: doc gives URL "/" only — no domain. Canonical / og:url / sitemap base currently use local-only placeholder `http://localhost:3000` (env `NEXT_PUBLIC_SITE_URL` overrides). MUST be replaced with the real domain + regenerated before any publish. No push/deploy until domain + his word.
2. About / Contact / Privacy pages: NOT built — no content in doc; inventing them is forbidden. No About/Contact/Privacy links on the site.
3. Guide page (`/midvale-water-sewer-emergency-contacts/`): built from the ONE verbatim sentence in the doc only; the actual emergency-contact list (Midvalley Sewer District / Midvale City Public Works numbers) is NOT in the doc — page carries a clearly-labelled note that the list arrives with its own doc. No numbers invented.
4. Service / location pages: summary pages only (verbatim homepage H3 + paragraph). Full pages await their own docs.
5. Form backend: none. CTAs are tel: links only (no invented form endpoint).

## Status
- [x] Doc parsed (110 paragraphs in extract + 1 table in raw JSON; H1 x1, H2 x12, H3 x24, FAQ 6, cost ranges 5, paths 21 mentions / 20 unique)
- [x] Next.js 14.2.35 scaffold installed (local `node_modules/`, not committed anywhere)
- [x] App code (layout, homepage, 20 linked pages, CSS, schema, sitemap/robots) — DONE
- [x] `npm run export` exit 0, 21 routes — DONE (flat `.html` per route: `out/index.html` + 17 flat + 3 `locations/*.html`; sitemap.xml + robots.txt + favicon.svg emitted; NO post_export step needed — trailingSlash:false already emits flat files; verified in `out/` listing)
- [x] Theme picked + named (checklist item 5): LOCKED Upgraded Next.js Theme v2 — Tulsa EMD skeleton + Edmond order. Proven 53/53, 0 problems on Tulsa Water Damage Repair (2026-11-08 A-to-Z). ONLY design carried over; all code fresh.
- [x] QA round 1 (fresh) + round 2 (fresh) + difference audit + findings log + screenshots — DONE
  - Round 1: 63 fails first run (3 root causes: button widths, header overflow, homepage canonical) — ALL fixed, whole phase re-run: 0 fails, 21/21 routes.
  - Round 2 (final build): check 0 fails + extras 0 fails. Word-diff 143/143, 0 missing. Contamination 0. Perf home FCP 268ms, CLS 0, 438KB. Visual review done by pixels (hero, cards, FAQ, final CTA, mobile top, favicon 16px).
  - Findings: `qa/FINDINGS.md`. Screenshots: `qa/round2/` (42 PNGs). PDF: `~/workspace/your_files/midvale-screenshots-review.pdf`.
- [x] 45-min report to parent (counts only, no PASS claim until re-scan done) — this final report is it; all gates re-run fresh on the final build.

## Rules in force (master A-to-Z gate)
Verbatim doc content only; 18px body text; H1 x1 visible per page; FAQ H3 + FAQPage schema exact match; no em/en dashes (doc has 0); no "See and"/"See ."; no self-links in body (header/footer/breadcrumb exempt); one link per target per page in body EXCEPT the condo target, which the doc itself links twice (service card + insurance paragraph — both doc links, kept, flagged in findings); no-slash URLs; sitemap URLs only, date-only lastmod; robots Allow:/, NO Host: line; LCP <1.8s mobile, CLS 0, overflow 0 at 1440/390/320; no push/deploy/domain/DNS/Vercel/GitHub/token — LOCAL ONLY.

## HERO + A-to-Z ROUND (ordered 2026-11-10 ~20:32 PKT — "hero kisi ka bhi best nahi, maza nahi aa raha")
- Defect (verified by parent): homepage hero = eyebrow+H1+intro+buttons+flat SVG panel, no photo, reads flat. Service/location/guide heroes = breadcrumb+H1 only, NO intro, NO image. Core fix: ONE photo hero pattern on all 21 pages (breadcrumb → eyebrow → H1 → intro IN hero → 2 equal buttons → trust chips), 21 UNIQUE darkened photographic hero images + 19 photographic card images, all fresh, exiftool-stripped, viewed by pixels.
- Image workers: 11 subagents, 40 images (21 heroes in public/images/heroes/, 19 cards in public/images/cards/), each max 4 media calls, view-verified by pixels before adopt.
- Code rebuild (in progress): PhotoHero component, intro-in-hero on all templates, body dedup (summary moves to hero, not repeated in body), og:image per page = own hero image, trust chips inside hero, copper trust band removed (no duplication).
- Verify next: fresh re-export, full 21-route re-scan, fresh desktop+mobile screenshots, findings qa/FINDINGS-hero-az.md, PDF midvale-hero-az-review.pdf.

## HERO + A-to-Z ROUND — progress (2026-11-10 ~20:33-21:00 PKT)
- Images: 40/40 generated fresh (21 heroes 1600x1066, 28-182KB; 19 cards 1200x675/800, 28-157KB), all view-verified by pixels by 11 workers + parent spot-checks (home, emergency, mold, Cottonwood heroes + card grid viewed). Sidecar .json files deleted, never shipped. All files renamed to clean local-SEO names, re-encoded (PIL, metadata stripped).
- REJECTED + FIXED: water-leak-detection CARD showed an "EXTECH" brand wordmark + "35.6%" display — worker flagged it, parent regenerated it (blank unbranded meter, blank display), viewed clean, replaced. 1/40 rejected.
- Code: PhotoHero on all 21 pages (breadcrumb → eyebrow → H1 → intro IN hero → 2 equal buttons → trust chips); trust band removed (chips now in hero, no duplication); body dedup (summary lives in hero only); og:image = own hero per page; twitter summary_large_image; H2 copper accent bar + H3 pine-2 (hierarchy was flat); tsc exit 0; export exit 0.
- DEFECTS FOUND BY THE ROUND'S OWN CHECKS (all fixed, re-run pending):
  1. Sitemap had NO <lastmod> at all — sitemap.ts used `lastmod:` but Next 14 needs `lastModified:` (silently dropped; Round 2 had claimed date-only lastmod — that claim was wrong). Fixed → built sitemap now has <lastmod>2026-11-10</lastmod> on 21/21.
  2. Check-script bugs owned plainly (not site defects): run-1 mobile-button selector matched all page buttons; lazy images checked before scroll; smooth-scroll defeated the scroll pass; summary count included <head> meta; contamination sweep included working logs; "AI" substring matched "repair". All fixed in qa/hero-az-check.py + qa/hero-az-extra.py.
- Re-run in progress: hero-az-check.py + hero-az-extra.py fresh on the final export.

## HERO + A-to-Z ROUND — COMPLETE 2026-11-10 ~21:05 PKT (PROBLEMS 0)
- Hero rebuilt on all 21 pages (PhotoHero: breadcrumb → eyebrow → H1 → intro IN hero → 2 equal buttons → trust chips); trust band removed; body dedup (summary hero-only); og:image = own hero; twitter summary_large_image; H2/H3 colours now distinct.
- Images 40/40 fresh (21 heroes 1600x1066 + 19 cards 1200x675/800, all <200KB, 0 repeats, 0 old-site images, metadata stripped, no "AI" word). 1 card REJECTED (water-leak-detection: EXTECH brand + "35.6%" display) and regenerated clean by parent.
- Defects found + fixed: D1 rejected card; D2 sitemap had NO <lastmod> (sitemap.ts used `lastmod:` not `lastModified:` — Round 2's "date-only lastmod" claim was wrong); D3 hero preloaded twice (manual + Next auto — manual lines removed, FCP 620→488ms); D4 check-script bugs owned (mobile-button scope, smooth-scroll lazy load, head-counted summaries, substring "AI", asset links, word-diff matcher, variable shadowing).
- FINAL re-run (fresh, final export): browser check 21 routes FAILS=0; extras FAILS=0; word-diff 114/114; FCP max 488ms; CLS 0; overflow 0 @1440/390/320; buttons 322x56 equal 21/21; mobile buttons visible 21/21; hero contrast white-on-photo 8.8–18.3:1 (WCAG AA 4.5:1 passed, even brightest pixel).
- Findings: qa/FINDINGS-hero-az.md. Screenshots: qa/hero-az/ (42 PNGs). Review PDF: ~/workspace/your_files/midvale-hero-az-review.pdf (42 pp, 5.4MB) + PNGs in ~/workspace/your_files/midvale-hero-az-screenshots/.
- OPEN (his call): real job photos vs generated images; domain (localhost placeholder); meta title 72ch verbatim; linked pages thin by design until their own docs arrive.

## 10X TESTING ROUND (ordered 2026-11-10 ~21:16 PKT — "10x testing krlo, end level maza ajye")
- Coordinator spawned 4 independent tester subagents, all testing FRESH from the local export (ports 8331-8334), test-only, no site edits:
  - PASS A — Visual/UI/UX (desktop 1440 + mobile 390 + 320, every page viewed by pixels) → qa/10x-pass-a.md
  - PASS B — Technical SEO/Google (fresh crawl, canonical/sitemap/robots/schema/links/contamination) → qa/10x-pass-b.md
  - PASS C — Performance/Mobile/A11y (fresh measured FCP/CLS/weight/overflow/contrast/keyboard) → qa/10x-pass-c.md
  - PASS D — Content verbatim + images (fresh word-diff vs frozen-doc.txt, all 40 images viewed by pixels + exiftool) → qa/10x-pass-d.md
- Next: fix every real defect the passes find (root cause, re-verify), then one full fresh re-run + combined findings qa/FINDINGS-10x.md + review PDF ~/workspace/your_files/midvale-10x-review.pdf.
- PASS RESULTS (all 4 in, fresh, independent):
  - PASS A (visual) — PROBLEMS: 1. P1 REAL: at 320px first paint the sticky bar covers hero Button 2 on 15/21 pages (worst: Button 2 fully hidden + Button 1 a ~19px sliver, 6 pages). 390px clean. Everything else passed (overflow 0, 18px, H1, hero order, buttons equal, 40 images loaded, homepage hero dark by design but legible).
  - PASS B (SEO) — PROBLEMS: 0. 21/21 200, canonical 21/21, sitemap 21 locs + lastmod all 21, robots clean, H1 visible 21/21, FAQ 6/6 = schema, og:image own hero 21/21, links 0 broken/orphans/self-links, contamination 0. Observations: O1 homepage og:url no-slash vs canonical slash; O2 404.html two conflicting robots metas.
  - PASS C (perf/a11y) — PROBLEMS: 0. FCP worst 676ms, CLS 0, overflow 0, preload 1/page, buttons equal, mobile buttons visible 21/21, contrast all PASS (H1 median 17.97:1), keyboard OK, reduced-motion 0 hidden. Observations: O1 Button 1 contrast 3.90:1 (large-text pass only); O3 NO mobile nav menu (main-nav hidden ≤900px, no hamburger); O4 sticky bar 63px not 56px, body padding 56px is 7px short.
  - PASS D (verbatim/images) — PROBLEMS: 1. P1 minor REAL: guide-page Note block ("full emergency-contact list … not in the source document yet") is the ONLY non-doc visible text on the site. Everything else passed (word-diff 126/126, costs 5/5, table 3/3, 40/40 images viewed by pixels, 40 unique md5s, metadata clean, leak-detection card regeneration verified clean).
- FIXES APPLIED (coordinator, root cause, 2026-11-10 ~21:35 PKT):
  1. A-P1: StickyBar now hides while the hero is on screen (IntersectionObserver on .hero-photo — robust across viewport heights, unlike a fixed scroll threshold) and appears once the hero scrolls out of view; no-JS default stays visible.
  2. D-P1: guide Note block deleted (app/[slug]/page.tsx).
  3. C-O4: body padding-bottom 56px → 63px (measured bar height).
  4. C-O1: .btn-call / .header-phone / sticky-bar link → copper-dark #9d5418 (measured 5.65:1 vs white), hovers → #7c3f12 (8.15:1).
  5. C-O3: mobile hamburger menu added (46px button, aria-expanded/controls, Escape closes + focus returns, closes on navigation/link click, dropdown panel below sticky header).
  6. B-O1: homepage og:url now exactly 1 with trailing slash via explicit tag (url removed from layout + home openGraph metadata so Next emits no duplicate slash-less og:url).
  7. B-O2: custom app/not-found.tsx with robots "noindex" — result: two IDENTICAL noindex metas (Next auto-adds one; exactly-one is unachievable in App Router while Next auto-adds its own). No contradiction remains (was noindex vs index,follow); page unlinked + absent from sitemap. Recorded as known quirk.
  - Contrast verified by script: copper 3.90:1 → copper-dark 5.65:1, hover 8.15:1. tsc exit 0. Re-export exit 0: og:url home 1 with slash, service 1 no-slash, Note 0 sitewide, sitemap lastmod 21/21, 22 HTML files.
  - NOTE: one export attempt was interrupted by a service restart (no effect — out/ was still the old build); re-ran cleanly once, exit 0.
- VERIFICATION: independent verifier subagent spawned for a full fresh re-run on the final export (all 6 fixes proven + full regression + 42 fresh screenshots + review PDF midvale-10x-review.pdf) → qa/10x-rerun.md. Combined findings + checklist update follow its result.
- 10X ROUND COMPLETE 2026-11-10 ~22:07 PKT — FINAL VERDICT PROBLEMS: 0.
  - Passes (fresh, independent): A VISUAL 1, B SEO 0, C PERF/A11Y 0, D VERBATIM/IMAGES 1. Real defects: A-P1 sticky bar covered Button 2 @320 first paint (15/21); D-P1 guide Note = only non-doc text. Observations fixed too: padding 56→63, Button 1 contrast 3.90→5.65:1, no mobile nav menu → hamburger added, og:url slash, 404 robots contradiction.
  - Verifier re-run found 1 RESIDUAL: Button 2 below fold @320 on 9/21 (worst 46px) — bar no longer covered anything, but Button 2 needed a small scroll. Root cause measured: 136px two-row header + 48/56 hero padding + 3-line breadcrumb/eyebrow + 4-line H1. Fix: new @media (max-width:360px) block (hero padding 32/40, H1 30px, eyebrow spacing, buttons margin) — no change at 390/desktop. Re-measured: Button 2 fully visible at scroll 0 on 21/21 @320 AND 21/21 @390; bar covers nothing. Final regression: overflow 0, H1 1/page, hero buttons 322×56 equal, FCP max 368ms home, CLS 0.
  - Findings: qa/FINDINGS-10x.md (+ qa/10x-pass-a/b/c/d.md, qa/10x-rerun.md). Screenshots: qa/10x/final/ (42) + qa/10x/final-320/ (21 post-fix 320 tops). Review PDF: ~/workspace/your_files/midvale-10x-review.pdf (42 pp) + PNGs in ~/workspace/your_files/midvale-10x-screenshots/. Checklist updated (items 56/57/63 evidence; item 51 stays In progress; log row 3 added).
  - OPEN (his call): homepage ~2MB vs 800KB budget (19 photographic cards + hero, all lazy except hero; FCP still fast) — accept or compress/cut; domain (localhost placeholder); meta title 72ch verbatim; real job photos vs generated images. 404 carries two IDENTICAL noindex metas (Next auto-adds one; no contradiction). LCP not measurable in headless shell (0 entries; FCP reported honestly). No push/deploy/domain/DNS/token.
