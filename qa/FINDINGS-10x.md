# FINDINGS — Midvale UT 10X TESTING ROUND (2026-11-10)

Order: Noorullah, ~21:16 PKT — "Good ab 10x testing krlo end end end end end level maza ajye".
Method: 4 independent tester passes (fresh, from the local export, never recycled),
then root-cause fixes by the coordinator, then an independent verifier re-run,
then a residual fix + final regression. Local only. No push / deploy / domain /
DNS / Vercel / GitHub / token touched at any point.

## FINAL VERDICT — PROBLEMS: 0 (after fixes + re-runs)

| Stage | Result |
|---|---|
| PASS A — Visual / UI / UX | PROBLEMS: 1 (320px sticky bar covered Button 2 on 15/21) |
| PASS B — Technical SEO / Google | PROBLEMS: 0 |
| PASS C — Performance / Mobile / A11y | PROBLEMS: 0 |
| PASS D — Content verbatim + images | PROBLEMS: 1 (guide-page Note = only non-doc text) |
| Independent verifier re-run (final export) | PROBLEMS: 1 (residual: Button 2 below fold at 320 on 9/21) |
| Residual fix + final regression | PROBLEMS: 0 — Button 2 fully visible at scroll 0, 21/21 at 320×700 and 390×844; overflow 0; H1 1/page; hero buttons 322×56 equal |

## 1. PASS RESULTS (fresh, independent)

### PASS A — Visual (qa/10x-pass-a.md) — PROBLEMS: 1
- 84 screenshots taken (every page: desktop 1440 full, mobile 390 top+full, 320 top) and
  viewed by pixels. Overflow 0 on 21/21 at all widths; body 18px on 21/21; H1 1/page
  visible; hero order on 21/21; buttons equal (322×56 desktop, 342×56 mobile); all 40
  images loaded, 0 repeats (md5), max 186KB; homepage cards 337×189 (16:9, height
  measured); H2/H3 colours distinct; 390px first paint clean on 21/21.
- **P1 (real, reproduced): at 320px first paint (320×700) the sticky call bar covered
  hero Button 2 on 15/21 pages.** Worst tier (6 pages: swamp-cooler, hardwood, condo,
  contacts guide, Cottonwood, South Salt Lake) — Button 2 fully hidden, Button 1 only
  a ~19px sliver (Button 2 bottom 746px vs bar top 637px, 109px hidden). Seen in the
  actual first-paint pixels, not just numbers. Same defect class as Chesterfield D1,
  but there 390px failed; here 390px passed and the failure was at 320px.
- Not defects: footer map blank in sandbox (markup verified correct, google.com
  unreachable here); category-table 3rd column swipe-reachable at 390px; sticky bar
  mid-page in full-page shots is a capture artifact; breadcrumbs wrapping to 2 lines
  is normal.
- Script errors owned: first run died on home mobile-full screenshot at 2x (capture
  limit) — fixed to 1x, re-ran; a `pkill` once matched the agent's own shell.

### PASS B — Technical SEO (qa/10x-pass-b.md) — PROBLEMS: 0
- Own fresh scripts (did not re-run hero-az-check.py). 200: 21/21; slash URL 404 as
  expected under trailingSlash:false (recorded, not a defect). Self-canonical exactly
  1/page, 21/21 == sitemap form, homepage keeps trailing slash. Sitemap: 21 locs,
  0 missing/extra, `<lastmod>2026-11-10</lastmod>` on ALL 21 — directly re-checking
  Round 2's false claim; no image entries, no noindex URL inside. robots: Allow:/,
  no Host: line, sitemap line consistent. Titles unique 21/21, descriptions unique
  21/21; homepage title 72ch verbatim + description verbatim vs frozen-doc. H1 exactly
  1/page, visible in real browser 21/21. FAQ schema 6/6 == visible H3 6/6 in order;
  all JSON-LD blocks parse, 0 errors. og:image + twitter:image == own hero 21/21;
  twitter summary_large_image 21/21; all 21 hero files exist (31–182KB). Links: 21
  distinct internal paths, 0 broken, 0 orphans, 0 body self-links; condo double-link
  on homepage confirmed exactly 2× as the documented exception. Contamination: 0
  across out/ + shipped source (incl. CSS comments); 0 "AI" whole-token hits;
  exiftool on all 40 images shows only File/RIFF/Composite tags. Noindex: only
  404.html, absent from sitemap.
- Observations (not counted): O1 — homepage og:url `http://localhost:3000` (no slash)
  vs canonical `http://localhost:3000/`; O2 — out/404.html had two conflicting robots
  metas (noindex + index,follow). O3 — 3 body anchors outside 3–5 words but all
  doc-verbatim titles (rewriting would break verbatim — not defects).
- Script error owned: run 1 falsely flagged 21 "duplicate body links" (breadcrumb/
  header links counted as body copy) — fixed with an explicit parent-walk, re-ran.

### PASS C — Performance / Mobile / A11y (qa/10x-pass-c.md) — PROBLEMS: 0
- FCP max 676ms (home; prior round's 488ms was run variance), DCL max 372ms, load max
  765ms, CLS 0 on 21/21, weight max 1941KB home / lightest 506KB. Overflow 0px on
  21/21 at 1440/390/320. LCP: 0 entries in this headless shell on all 21 routes
  (verified directly) — no LCP number claimed; LCP element is the preloaded hero img.
  Hero preload exactly 1 image/page on 21/21 (the second preload link is Next's
  automatic webpack-JS-chunk preload, not a hero duplicate). Buttons 322×56 desktop,
  342×56 mobile full-width equal, both visible at first paint 21/21 (worst Button 2
  bottom 694px vs bar top 781px = 87px clearance at 390). Images 0 broken on 21/21
  after stepped-scroll verification (40/40 slots). Contrast all PASS vs WCAG AA —
  H1 median 17.97:1 / p90 14.50:1 on rendered pixels, eyebrow 10.85, body 14.91,
  footer 12.34/10.03; Button 1 3.90:1 passes as large text (19px bold 700 → 3:1 bar).
  Keyboard: logical Tab order, focus outline visible; no dropdown/mobile menu exists
  (Escape N/A); reduced motion: 0 hidden elements.
- Observations (not counted): O1 — Button 1 contrast 3.90:1 passes only under the
  large-text rule (darkening copper buys margin); O2 — text links 24px tall (WCAG
  2.2 AA 24×24); O3 — NO mobile nav menu (.main-nav hides ≤900px, no hamburger);
  O4 — sticky bar measures 63px, not the claimed 56px; body padding-bottom 56px is
  7px short. O5 — FCP worst 676ms vs prior claim 488ms (variance, not regression).
- Script errors owned: first script jumped straight to page bottom (one lazy card
  falsely "broken" — re-probed properly, 0 broken); sticky-bar selector missed the
  real class (corrected); first pixel sample included white H1 glyphs (redone
  excluding glyph pixels).

### PASS D — Content verbatim + images (qa/10x-pass-d.md) — PROBLEMS: 1
- Word-diff homepage: 126/126 OK, 0 missing, 0 changed; meta title verbatim 72ch,
  description verbatim. Cost ranges 5/5 verbatim; category table 3/3 rows verbatim.
  Per-page verbatim: 16/16 service pages (H3 + summary verbatim, no extra body text),
  3/3 location lines verbatim, contacts doc sentence verbatim. Sitewide sweep (21/21):
  0 em/en dashes, 0 "See and"/"See ." fragments, Button 1 = number only, Button 2 =
  "Request Emergency Help", phone ONLY (385) 337-3560 (22 HTML files incl. 404),
  0 invented-claim words, 0 real-job-photo claims, 0 cross-site contamination.
- Images 40/40: heroes 1600×1066, cards 1200×675 (3 at 1200×800), max 182.1KB,
  0 ≥200KB, 40 unique md5s (0 repeats), out/ copies md5-match public/. Metadata clean
  on all 40 (exiftool File/RIFF/Composite only; no EXIF/XMP/C2PA/prompt/generator/GPS;
  no "AI" in filename/path/alt). All 40 viewed by pixels (2 contact sheets + 12
  individually at full size). Water-leak-detection card regeneration verified clean
  (blank dark meter display, no EXTECH wordmark, no digits). No brand wordmark or
  readable text in any image; no clear wrong-city cues. All 40 alts describe only
  what the pixels show.
- **P1 (minor, real, reproduced): builder placeholder Note on
  /midvale-water-sewer-emergency-contacts** ("Note: the full emergency-contact list
  for this page is not in the source document yet…") — the ONLY non-doc visible text
  on the entire site. It invents no facts/numbers/claims, but it is user-facing
  build-status text on a verbatim-only page.
- Nits (not defects): storm hero hills read desert-red/sagebrush (ambiguous — Oquirrh
  side is genuinely arid); water-damage-repair hero is a bare empty room; water-heater
  card shows the valve only (alt still accurate).
- Clarification: inner-page H1s are doc title + " in Midvale, UT" — derived from doc
  words, not the literal doc H3; the prior round's "H1 verbatim" wording was loose.
- Script errors owned: first run's 3 false "CHANGED" (button labels joined; anchor-
  boundary space before a period), a service-pair parser returning 0 pairs, a slug
  matcher missing 7 pairs where H3 ≠ anchor text, naive byte-scan flagging 3 false
  "XMP" hits (verified as compressed VP8 payload coincidences). Each fixed, re-run.

## 2. FIXES (coordinator, root cause — not patches)

1. **A-P1 sticky bar @320:** bar now stays hidden while the hero is on screen
   (IntersectionObserver on `.hero-photo` — robust across viewport heights, where a
   fixed scroll threshold is not) and appears once the hero scrolls out of view.
   No-JS default stays visible. File: components/site.tsx (StickyBar).
2. **D-P1 guide Note:** Note block deleted from app/[slug]/page.tsx. Guide page now
   carries only its verbatim sentence + link + buttons.
3. **C-O4 padding:** body padding-bottom 56px → 63px (measured bar height).
   File: app/globals.css.
4. **C-O1 contrast:** `.btn-call`, `.header-phone`, sticky-bar link → copper-dark
   #9d5418 (measured 5.65:1 vs white, was 3.90:1); hovers → #7c3f12 (8.15:1).
5. **C-O3 mobile menu:** accessible hamburger added — 46×46px button,
   aria-expanded/controls, Escape closes + focus returns, closes on navigation and
   on link click, dropdown panel below the sticky header. Files: components/site.tsx
   (Header), app/globals.css (.menu-btn, .main-nav.open).
6. **B-O1 og:url:** homepage og:url now exactly 1 WITH trailing slash via an explicit
   tag (same pattern as the canonical trick); `url` removed from layout + home
   openGraph metadata so Next emits no duplicate slash-less og:url.
7. **B-O2 404 robots:** custom app/not-found.tsx with robots "noindex". Result: two
   IDENTICAL noindex metas (Next auto-adds one; exactly-one is unachievable in App
   Router while Next auto-adds its own). No contradiction remains (was noindex vs
   index,follow); page unlinked + absent from sitemap. Recorded as a known quirk.
- Verification of fixes before re-run: tsc exit 0; re-export exit 0; og:url home
  exactly 1 with slash, service exactly 1 no-slash; Note 0 sitewide; sitemap lastmod
  21/21; 22 HTML files. (One export attempt was interrupted by a service restart
  with no effect — out/ was still the old build; re-ran cleanly once.)

## 3. INDEPENDENT VERIFIER RE-RUN (qa/10x-rerun.md) — PROBLEMS: 1 (residual)

- Fixes 2–7 all PROVEN by measurement: Note gone, word-diff 126/126; padding 63px,
  bar 63px, footer-base bottom = bar top at page bottom; contrast 5.65:1 on Button 1 /
  header phone / bar link; hamburger 46×46 opens (aria-expanded, panel 390×191), link
  navigates + closes, Escape closes + focus returns, keyboard-only flow, hidden at
  1440; og:url exactly 1/page == canonical on 21/21; 404 quirk as recorded.
- A-P1 PARTIAL: the filed defect is gone — bar hidden at scroll 0 on 21/21 at 320×700
  and 390×844, nothing covers either button; bar appears past the hero on 21/21
  (63px), real click lands on the bar link 21/21, hides again at top 21/21. BUT the
  brief's literal criterion (Button 2 fully visible at scroll 0 at 320×700) failed on
  9/21 pages: Button 2 sat 46px below the fold on 6 pages (swamp-cooler, hardwood,
  condo, contacts, Cottonwood, South Salt Lake), 15px on 2 (emergency, basement),
  3px on 1 (magna) — confirmed in pixels. Button 1 fully visible 21/21; at 390 both
  buttons fully visible 21/21.
- Regression (fresh, all 21): 200 21/21; H1 1/page visible 21/21; canonical = sitemap
  form 21/21; sitemap 21 locs + date-only lastmod 2026-11-10 on 21/21; robots Allow:/,
  no Host:; titles/descs unique 21/21, home title 72ch verbatim; FAQ 6/6 visible =
  schema; JSON-LD 0 errors; og/twitter = own hero 21/21; 0 broken links, 0 orphans,
  0 body self-links (only known dupe: condo 2× on home); overflow 0 at 1440/390/320;
  buttons 322×56 equal desktop; FCP max 600ms, CLS 0, weight max 2038KB; images 40/40
  load, 40 unique md5, max 182KB; hero preload 1/page; contamination 0 (raw `918`
  hits are only inside the CSS chunk hash `8458119918792bf4`); LCP: headless shell
  emits 0 LCP entries on 21/21 — no LCP number claimed.
- Verifier script errors owned: first run showed "Application error" crash screens —
  the verifier's mapping server didn't URL-decode paths, so page chunks 404'd
  (ChunkLoadError → React #423, 5/24 loads crashed); after adding unquote(): 0
  crashes in 24 loads, crashed screenshots discarded and re-taken. Also: menu probe
  clicked a non-existent nav link, smooth-scroll timing, run-1 desktop data lost to a
  crash (re-ran with incremental saves).
- Deliverables: 42 screenshots qa/10x/final/ + 21 supplementary 320px tops
  qa/10x/final-320/; review PDF ~/workspace/your_files/midvale-10x-review.pdf
  (42 pp, 29.5MB, pypdf-verified); PNGs in ~/workspace/your_files/midvale-10x-screenshots/.

## 4. RESIDUAL FIX + FINAL REGRESSION (coordinator)

- Cause measured (Playwright, 320×700, swamp-cooler): sticky header 136px (two rows
  at ≤600px) + hero padding 48/56 + breadcrumb 98px (3 lines) + eyebrow 92px
  (3 lines) + H1 170px (4 lines at 34px) + stacked buttons 156px → Button 2 bottom
  746px, 46px below the fold. Fix (globals.css, NEW `@media (max-width: 360px)`
  block, no change at 390px or desktop): hero padding 32px/40px, H1 30px, eyebrow
  letter-spacing 1px + margin-bottom 8px, hero-buttons margin-top 16px (~64px+ saved).
- Re-export exit 0. Fresh re-measurement (qa/10x/rerun-320.py, all 21 routes):
  **Button 2 fully visible at scroll 0 on 21/21 at 320×700 AND 21/21 at 390×844**;
  bar covers a button nowhere (0 cases); worst 320 below-fold 0px.
- Final regression (qa/10x/rerun-final.py, new export): overflow 0 on 21/21 at
  1440/390/320; H1 1/page on 21/21; hero buttons 322×56 equal on 21/21 (the second
  button pair — final CTA — is 402×56 equal to each other; an early run of this
  script flagged "21 bad" because its selector matched all 4 buttons — script bug,
  owned, not a site defect); FCP 368ms home / 120ms / 56ms, CLS 0, weights 728KB /
  168KB / 163KB at 390. 320px tops re-taken into qa/10x/final-320/ (post-fix).
- The review PDF (desktop full + mobile-390 top) is unaffected by the ≤360px-only
  change: desktop and 390px renders are pixel-identical, so no PDF rebuild was
  needed. The 320px tops in qa/10x/final-320/ are post-fix.

## 5. KNOWN QUIRKS / OPEN (not defects — his call)

- 404 carries two identical `noindex` metas (Next auto-adds one). No contradiction;
  page unlinked, absent from sitemap.
- LCP: headless shell emits 0 LCP entries — FCP + LCP element reported honestly,
  no LCP number invented. Homepage total weight ~2MB (19 photographic cards + hero,
  all lazy except the hero) exceeds the old 800KB budget from the SVG-panel build;
  FCP stays fast (max 676ms). Checklist item 51 stays In progress awaiting his call:
  accept the photographic homepage at ~2MB, or compress/cut cards.
- Footer map iframe blank in sandbox (google.com unreachable); markup verified correct.
- Images are generated illustrations, not real job photos. Meta title 72ch verbatim
  (over 60, NOT rewritten). Canonical/sitemap/og use localhost:3000 placeholder until
  a real domain is given. Linked pages thin by design until their own docs arrive.
  About/Contact/Privacy not built (no doc content). No push/deploy/domain/DNS/token.

## 6. FILES

- Pass findings: qa/10x-pass-a.md, qa/10x-pass-b.md, qa/10x-pass-c.md, qa/10x-pass-d.md
- Verifier: qa/10x-rerun.md (+ qa/10x/rerun-*.json, rerun-*.py), qa/10x/final/ (42 PNGs),
  qa/10x/final-320/ (21 post-fix 320px tops)
- Residual fix check: qa/10x/rerun-320.py + rerun-320.json, qa/10x/rerun-final.py + rerun-final.json
- Combined: qa/FINDINGS-10x.md (this file)
- Review PDF: ~/workspace/your_files/midvale-10x-review.pdf (42 pp) + PNGs in
  ~/workspace/your_files/midvale-10x-screenshots/
- Checklist workbook updated (10x evidence; item 51 stays In progress on the ~2MB homepage weight).
