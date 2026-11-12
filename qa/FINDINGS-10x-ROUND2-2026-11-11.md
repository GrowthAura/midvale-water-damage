# Midvale UT — 10x QA ROUND 2 — FINDINGS LOG
**Date:** 2026-11-11 (evening PKT) | **Tester:** independent fresh round (did NOT copy Round 1 verdicts; every check re-measured)
**Site LIVE:** https://growthaura.github.io/midvale-water-damage/ — 21 pages, Next.js static export, GitHub Pages subpath `/midvale-water-damage/`
**Build dir:** `~/workspace/midvale-water-damage/` | **Phone ONLY:** (385) 337-3560
**Method note (mirror):** Chromium in this sandbox cannot reach the live domain directly (ERR_TUNNEL_CONNECTION_FAILED via proxy). The EXACT published bytes were mirrored with curl (21 pages + 73 local assets, 94 OK) and served at the same subpath `http://127.0.0.1:8342/midvale-water-damage/`. Mirror identity verified by md5 vs LIVE for sampled files: home, emergency-water-extraction, robots.txt, CSS `fea43d7f5f433f14.css`, hero `home.webp` — all MATCH. Live home + live inner page both HTTP 200 (curl). Every browser check below is mirror-only and is labelled as such.

## VERDICT — PROBLEMS 7 (1 CRITICAL, 2 P2, 4 P3)

| # | Sev | Defect | Status vs Round 1 |
|---|-----|--------|-------------------|
| P1 | CRITICAL | 20/20 inner pages show white React "Application error" — ChunkLoadError, no assetPrefix/basePath | CONFIRMED, unchanged |
| P2 | — | Titles 21/21 over 60ch (69–85ch) | CONFIRMED, unchanged |
| P2 | — | localhost:3000 canonicals / og / sitemap / robots on 21/21 | CONFIRMED, unchanged |
| P3 | — | Meta description 162ch on window-well-flooding | CONFIRMED, unchanged |
| P3 | — | Button 2 6px below fold @320×568 | CONFIRMED, unchanged |
| P3 | — | Water-category table 3rd column clipped @390 | CONFIRMED, unchanged |
| P3 | **NEW** | Mobile menu does NOT close on scroll | NEW in Round 2 |

---

## P1 — CRITICAL: 20/20 inner pages are a white error screen (live, re-verified with own eyes + curl)

**What the user sees (screenshot `shots/emergency-water-extraction-desktop-top.png`, viewed):** a white void with one centred line: *"Application error: a client-side exception has occurred (see the browser console for more information)."* No header, no hero, no H1, no buttons, no content, no footer — on every inner page, every viewport.

**Measured (sweep-round2.json, 21/21 pages × 4 viewports, fresh browser per page):**
- appError=True on 20/20 inner pages at desktop 1440, mobile 390, 320×700 and 320×568 (80/80 checks). Homepage appError=False everywhere.
- Every inner page: 3–7 console errors + 2–7 failed requests + exactly 1 pageerror per viewport.
- Console: `ChunkLoadError: Loading chunk 42 failed. (error: http://127.0.0.1:8342/_next/static/chunks/app/%5Bslug%5D/page-5ab7919444d9be38.js)` — same chunk hash as Round 1.
- Pageerror: `Minified React error #423` (hydration error).
- Failed requests on an inner page: the `[slug]` chunk requested BOTH prefixed (`/midvale-water-damage/_next/...` = 200, from the script tag) and unprefixed (`/_next/...` = 404, from the hydration loader). Live curl re-check: prefixed chunk 200, unprefixed 404 — mechanism confirmed against LIVE, not just the mirror.
- Rendered DOM on inner pages: `h1 = []`, `heroButtons = []`, `sections = []` — React unmounts everything after the hydration crash.

**Root cause (unchanged):** `next.config.mjs` has NO `assetPrefix` / `basePath` (only `output: "export"`, `trailingSlash: false`, `images.unoptimized`). The export rewrites script-tag srcs to the subpath, but the client-side chunk loader and RSC prefetch still request root-relative `/_next/...` and `/*.txt?_rsc=...`, which 404 on GitHub Pages.

**Homepage is hit by the same defect, lesser symptom:** on load the homepage fires 5 HTTP 404s (probe-round2.json, response log) — 2 unprefixed chunks (`/_next/static/chunks/390-3ec53ff4978d6c80.js`, `/_next/static/chunks/app/page-d5049d3965f74d9d.js`) + 3 unprefixed RSC prefetches (`/emergency-water-extraction.txt?_rsc=…`, `/index.txt?_rsc=…`, `/sewage-backup-cleanup.txt?_rsc=…`) — and logs 29–34 console "Failed to load resource: 404" errors per load (desktop 34, mobile390 30, 320×568 29). The homepage still renders because its own chunk loads via the prefixed script tag, but **no page on the site loads clean: soft-error count is >0 everywhere**.

**SEO consequence:** HTTP status is 200 and the SSR HTML is intact (H1 + summary present in raw HTML — a no-JS fetch sees content), but any JS-rendering crawler (including Googlebot's renderer) executes the hydration and lands on the error screen. 20/21 pages are effectively blank in a real browser.

**Fix (unchanged from Round 1):** set `assetPrefix` + `basePath` to `/midvale-water-damage/`, re-export, re-push, then re-run QA fresh on the deployed URL. Needs his word + token. **Do NOT call this site live-ready until the re-run passes.**

**Note on Round 1's locations chunk hash:** Round 1 cited a locations chunk `page-9135108d4f9a80e.js` as 404 both ways. That hash 404s on live in both forms because the live locations chunk filename differs — do not cite that hash as proof. The `[slug]` chunk evidence above (same hash, prefixed 200 / unprefixed 404) is the correct proof.

## P2 — Titles 21/21 over 60 characters (re-measured from audit-http-round2.json)

| Page | Title length |
|---|---|
| home | 72 — "Water Damage Restoration Midvale UT \| 24/7 Emergency Crew Dispatched Now" (verbatim doc title) |
| mold-remediation | 69 (shortest inner) |
| storm-flood-damage | 71 |
| magna-ut | 72 |
| ceiling / water-leak-detection / window-well | 73 |
| sewage-backup-cleanup | 74 |
| burst-pipe | 76 |
| commercial | 76 |
| basement / emergency-contacts / water-heater | 78 |
| emergency-water-extraction | 79 |
| south-salt-lake-ut | 82 |
| condo-apartment | 83 |
| swamp-cooler | 83 |
| hardwood-floor-cabinet-drying | 84 |
| cottonwood-heights-ut | 85 (longest) |

All 21 titles exceed Google's ~60ch display width. Pattern: every inner title is "Service in Midvale, UT | Water Damage Restoration Midvale UT" — the brand suffix alone costs ~40ch. His call (verbatim vs trim, Tulsa-U5 pattern). Home title is verbatim doc wording — do not trim without his word.

## P2 — localhost:3000 canonicals / og / sitemap / robots on 21/21 (re-measured)

- Canonicals: all 21 = `http://localhost:3000/...` (audit-http-round2.json).
- Sitemap: 21/21 `<loc>` = `http://localhost:3000/...`, 21/21 `<lastmod>` date-only `2026-11-10` (good format, wrong host).
- robots.txt (live, 200): `User-agent: * / Allow: / / Sitemap: http://localhost:3000/sitemap.xml`.
- Known state — domain pending. Swap `NEXT_PUBLIC_SITE_URL` + re-export + re-push when the real domain lands. Not a code bug, a placeholder that must not go live as-is.

## P3 — Meta description 162ch on window-well-flooding (re-measured)

All other descriptions ≤156ch (basement-flooding 156 is the next longest). window-well-flooding = 162ch: "When a window well fills with snowmelt or storm water, it pours straight into basement bedrooms. We …" — trim by ~4ch. Home desc 138ch, verbatim.

## P3 — Button 2 6px below the fold @320×568 (re-measured + viewed)

probe3-round2.json, 320×568: Button 1 "(385) 337-3560" top 446 / bottom 502; Button 2 "Request Emergency Help" top 518 / **bottom 574 vs 568 viewport** — 6px below fold. Screenshot `shots/home-mobile320x568-top.png` (viewed): Button 2 is visibly cut at the fold ("Request Emergency / Help" half-clipped). At 320×700 and 390×844 both buttons are fully visible. Hero at 320×568 is 1,105px tall (eyebrow wraps to 3 lines, H1 4 lines). Minor — same 6px as Round 1.

## P3 — Water-category table 3rd column clipped @390 (re-measured + viewed)

probe3-round2.json, 390px: table 377px wide inside 342px `.table-wrap` (`overflow-x: auto`); column widths [113, 132, 131]; 3rd column header "What it means for cleanup" right edge at **400px > 390 viewport** — not visible on first paint, reachable only by horizontal swipe with no visual cue. Desktop: all 3 columns visible, clean zebra table (screenshot `home-sec-d4-y7000.png`, viewed). Minor.

## P3 — NEW: Mobile menu does NOT close on scroll (found fresh this round)

probe4-round2.json, 390×844, two independent methods (window.scrollTo + real mouse-wheel scroll):
- Open menu → nav `main-nav open`, rect y=114 h=191, 3 links visible (Home / Emergency Water Extraction / Sewage Backup Cleanup).
- Scroll to y=900 → nav class STILL `main-nav open`, rect y=114 h=191, 3 links still visible and clickable (panel is absolutely positioned under the sticky header, so it rides along and keeps covering the hero when the user scrolls back).
- Escape closes it (class back to `main-nav`); hamburger toggle closes it.
- Same defect class as Chesterfield / Pleasant Grove / San Bruno Round 1. Minor UX — fix is a scroll listener + re-export + re-push (same deploy as the P1 fix).

## Low observations (not counted as PROBLEMS)

- **Live 404s on direct request (curl, confirmed live):** `site.webmanifest` 404, `llms.txt` 404, `favicon.ico` 404. The site uses `favicon.svg` (live 200) and declares no manifest link, so no page requests these — browsers auto-request `/favicon.ico` only. Add a `/favicon.ico` file and an `llms.txt` if the AEO pattern is wanted; not blocking.
- **Homepage weight (NOT re-measured this round; Round 1 number stands):** ~1.6 MB total, images 1,519,270 bytes (hero 117,632 + 19 cards). Decision still open with him (accept vs resize + re-push). FCP here is already fast, so this is weight/bandwidth, not speed.
- **Several hero/card photos have an AI-generated look** (overly polished, dramatic lighting — e.g. condo hallway crew, sewage hazmat crew, crawl-space worker). No "real job photo" claim appears anywhere on the site, and metadata is clean (see Images), so this is a design observation, not a defect. Real job photos would still be better.

---

## PASS — re-verified fresh this round

### (a) Images — ZERO repeats, ZERO old-site reuse, all viewed
- 40 images total: 21 heroes 1600×1066, 19 cards 1200×675/800, 3.8 MB site-wide. Max file 182 KB (heroes/cottonwood-heights-ut.webp, heroes/magna-ut.webp).
- md5: **0 duplicates within the site; 0 hits vs 5,606 past-site images** indexed from 39 dirs across the workspace (images-round2.json).
- Perceptual hash (dhash): within-site closest pair d=13 (crawl-space hero vs magna hero); vs past sites closest d=6, 7, 10, 11, 12, 12, 12, 12, 13. **All 5 closest pairs adjudicated by viewed pixels** (`dhash-pairs/A–E.jpg`): every pair is a completely different photo (tonal false positives — e.g. d=6 is an interior drying-lamp room vs a Texas lake sunset; d=7 is an air-scrubber machine vs a mold-stained wall). NOT duplicates.
- Metadata: 3 files flagged by a raw-byte scan for the string "xmp" — **adjudicated false positive by WebP chunk parsing**: all files contain ONLY a `VP8` lossy chunk, no EXIF/XMP/VP8X chunk at all. No AI metadata anywhere.
- Rendered: all 20 homepage images `complete=true`, natural sizes correct, display 337×189 (16:9 crop). Hero `home.webp` complete, 1440×633 display.
- Topic/place fit (viewed): hero = crew with extraction equipment at dusk (on-topic); burst-pipe card = spraying burst pipe; sewage card = floor-drain cleanup; water-heater card = leaking faucet; Magna hero = wet historic main street with mountains (good place fit); Cottonwood/South Salt Lake/Magna cards are distinct area photos. No image is repeated on any page; no city page uses another area's photo.

### (b) ZERO old-site traces
- Grep over the entire mirror (HTML/JS/CSS/JSON/TXT) for 16 other-site names, phones and domains (Tulsa, Lancaster, Plano, Naples, Stockbridge, Tukwila, Delaware, Biohazard, Laredo, Chesterfield, Pleasant Grove, San Bruno, Acworth, Apopka, Belleville, Elyria + their phones) = **0 hits**.
- Only phone anywhere in the HTML: (385) 337-3560 (155 occurrences). Only domains: `localhost` (placeholder, 336), `schema.org` (86), `google.com` (18, the map iframe).

### (c) No pointless line breaks / empty spaces
- 0 empty `<p>` on all 21 pages × 4 viewports; 0 double `<br>` (audit-http-round2.json); 0 "See and" / "See ." fragments in visible text.
- The single empty `<div>` >50px on the homepage is `.hero-shade` (632px, `aria-hidden="true"`) — the decorative gradient overlay over the hero photo, by design, not a gap.
- All 15 homepage sections render with healthy heights (header 73, hero 633, causes 434, services 3,409, neighborhoods 652, why 688, process 824, category table 574, cost 513, insurance 434, first-30-min 474, nearby cities 686, FAQ 1,131, final CTA 394, footer 960). No collapsed section, no orphaned lines, no weird gaps — verified in 7 desktop + 4 mobile section screenshots (viewed).

### (d) Text sizes — 18px rule holds
- Computed px (probe-round2.json + probe3-round2.json, desktop 1440 + mobile 390): body 18px/30.6px, H1 44px desktop / 34px mobile, H2 32px / 28px, H3 24px, footer 18px, eyebrow 18px, hero intro 18px (#EEF4F2 on dark hero), buttons 19px.
- **Full-DOM scan @390: ZERO elements with computed font-size < 18px.**
- Hero buttons equal: desktop 322×56 both; mobile390 342×56 both, stacked.
- H1 intro text is visible on mobile (not hidden).

### (e) H2/H3 colouring — BEST-EVER verdict: PASS, premium and consistent
- Computed colours (all 12 H2s, all 24 H3s): H2 = `rgb(14,59,56)` #0E3B38 deep teal, 700, with a short orange underline accent; H3 = `rgb(21,82,76)` #15524C, 700. The final-CTA H2 is white on the dark teal CTA band (intentional).
- Contrast (computed): H2 on white **12.34:1**, H3 on white **8.96:1**, body on white **14.91:1**, Button 1 white on burnt-orange #9D5418 **5.65:1** (AA pass — this was the 3.90→5.65 fix), Button 2 teal on white **12.34:1**, footer text on teal **10.03:1**, eyebrow peach on dark hero **8.74:1**, H1 white on dark hero **13.59:1**. Every heading/body/button passes WCAG AA with wide margin.
- Viewed verdict: the palette (deep teal + burnt orange + peach eyebrow + pale-mint section alternation) reads premium and coherent; hierarchy 44/32/24 is clear; the orange H2 underline is a consistent signature. No colour defect found. (Designer's note: the palette is handsome but the same teal is used for H2, H3, buttons and footer — differentiation comes from size/weight/accent, which works; nothing to change.)

### (f) LIVE testing — mirror method (see header)
- Mirror: 21 pages + 73 assets, 94 OK; 4 failures, all confirmed live 404s by direct curl (site.webmanifest, llms.txt, favicon.ico + the directory URL itself in the extras loop).
- Live curl: home 200, inner page 200, prefixed `[slug]` chunk 200, unprefixed chunk 404, trailing-slash inner URL 404, nonexistent page 404 ("Page Not Found"), robots.txt 200.
- Live HTML of an inner page does NOT contain "Application error" (SSR HTML is intact); the error appears only after JS hydration runs.

### (g) Soft errors — counts (0 allowed; all traced to P1)
- Homepage: 29–34 console 404 errors + 5 HTTP 404s per load (unprefixed chunks + RSC prefetches — P1 root cause); 0 pageerrors; 1–2 failed requests (1 = Google Maps embed, sandbox-blocked — see Not Verified; 1 = unprefixed chunk).
- Inner pages: 3–7 console errors + 2–7 failed requests + 1 pageerror (React #423) per viewport — all P1.
- No other JS errors, no other failed requests, no other 404s anywhere.

### (h) Every section — design review (viewed screenshots)
- **Header (sticky):** logo "Water Damage Restoration / Midvale, UT" + 3 nav links + orange phone button; clean. Mobile: two-row header (logo row, hamburger + phone row) — the hamburger sits centre-left, phone button right; slightly unusual placement but tidy, no overlap.
- **Hero:** dark crew photo + peach eyebrow + white H1 + 18px intro + equal buttons + trust strip. Rich, dimensional, not flat black. Good.
- **What causes…:** H2 + intro paragraph + seasonal paragraph. Clean, generous leading.
- **Services (15 cards + 4 area cards):** 3-column white cards on pale mint, photo top, teal H3, verbatim summary, orange underlined link. Photos on-topic. Card link text repeats the H3 wording (doc pattern) — visually fine.
- **Neighborhoods / Why Midvale / Process / Category table / Cost / Insurance / First 30 Minutes / Nearby Cities / FAQ / Final CTA:** all render cleanly with consistent H2 + orange accent, orange-dot bullets, generous spacing. Cost section shows doc-verbatim price ranges as bullets. No alignment or hierarchy defect found anywhere on the homepage.
- **Footer:** 4 columns (brand + Services + Nearby Cities + Emergency Help) + bottom bar. Link columns clean. Top ~300px of the footer is blank in the sandbox — that is the Google Maps iframe area (see Not Verified).
- **Inner pages:** cannot be design-reviewed in rendered form — P1 blocks the render on every inner page. SSR HTML checked instead: H1 = 1, summary paragraph present, hero image referenced, 1 H2, 0 H3 (thin by design — homepage-only doc).

### Content verbatim (re-measured with a corrected matcher)
- Homepage: **37/37 doc headings present** (H1 ×1, H2 ×12, H3 ×24); every doc body line present after adjudicating the 3 non-visible line classes (meta title/desc lines → `<title>`/`<meta>` verbatim; "[Call …] [Request Emergency Help]" ×2 → the two hero buttons; link-annotation sentences → present with the `(…/path/)` annotation stripped, the path being the href).
- Inner pages: **20/20 summaries are verbatim doc excerpts**, present in both the doc and the homepage (checked with a word-subsequence matcher; an earlier naive pass produced false "misses" from a matcher bug — a greedy partial match bridging a heading into the paragraph — fixed and re-run).
- Links: **all 20 doc link annotations exist on the homepage** with the doc's exact anchor text (each appears twice: in-copy link + card link — the doc itself repeats the condo target, preserved per rule). Homepage internal hrefs NOT in the doc: only the homepage itself, `#faq`, `#services`. **No builder-added content links; 0 body self-links.**
- FAQ: **6/6 questions as visible H3 = 6/6 FAQPage schema mainEntity.**
- JSON-LD: home BreadcrumbList + FAQPage + HomeAndConstructionBusiness + WebSite; service pages BreadcrumbList + Service; guide page BreadcrumbList only. No aggregateRating, no invented claims. "IICRC" hit is doc-verbatim ("built on IICRC S500 water drying steps"). "rating" hit is a substring false positive ("operating"/"separating" in alt text).

### Technical SEO (re-measured)
- H1 = 1 on all 21 pages. Overflow 0 on all 21 pages × 4 viewports. CLS 0 everywhere (measured).
- Sitemap 21/21, date-only lastmods 2026-11-10. robots Allow:/, no Host: line.
- Homepage FCP (headless, mirror): 740–1088ms. Inner FCP 476–2,608ms (measured on the error screen — meaningless for real UX). These are sandbox numbers, not real-world LCP (see Not Verified).
- Sticky bar: hidden at scroll 0 (`bar-hidden`), appears on mobile after scroll (fixed, 62.6px, "Call (385) 337-3560 · 24/7"), `display:none` on desktop by design. PASS — it no longer covers Button 2.
- No em/en dashes in visible content of the 21 pages.

---

## NOT VERIFIED (labelled, never passed/failed)
- **LCP in headless Chromium** — FCP numbers above are sandbox-only; re-measure LCP on real hosting with a real browser.
- **Footer map tiles** — the Google Maps iframe (`https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed`) is present in the footer but renders blank in this sandbox (Google unreachable, ERR_TUNNEL_CONNECTION_FAILED). Needs a real-browser check.
- **Real-browser rendering** — all browser checks were sandbox Chromium on the byte-identical mirror; a real-browser pass is still owed after the P1 fix.
- **Inner-page rendered design** — unmeasurable until P1 is fixed (SSR HTML only).
- **Homepage weight decision** — ~1.6 MB (Round 1 measurement, not re-measured this round); still awaiting his accept-vs-resize call.

## QA process notes (for the record)
- Sweep run 1 crashed at page 15/21 (renderer TargetClosedError — sandbox memory pressure on the 24,729px-tall mobile page). Re-ran as run 2 with a fresh browser per page + incremental JSON after every page: **21/21 pages completed, 84 viewport visits, 84 screenshots.**
- Image job hashed 5,606 past-site images (39 dirs); finished clean.
- Verbatim matcher bug found and fixed mid-round (greedy partial-match reset discarding the real match start); full doc check re-run after the fix — results above are from the corrected run.
- No site file was changed. No push/deploy/DNS. No other site touched.

## Files produced this round
- `qa/FINDINGS-10x-ROUND2-2026-11-11.md` (this file)
- `qa/10x-round2-2026-11-11/sweep-round2.json` (21 pages × 4 viewports)
- `qa/10x-round2-2026-11-11/images-round2.json` (md5 + dhash, 40 images vs 5,606 past)
- `qa/10x-round2-2026-11-11/probe-round2.json`, `probe3-round2.json`, `probe4-round2.json`
- `qa/10x-round2-2026-11-11/shots/` (84 sweep shots + section shots + menu probes)
- `qa/10x-round2-2026-11-11/dhash-pairs/` (5 adjudicated close pairs)
