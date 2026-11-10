# FINDINGS — 10X RE-RUN (fresh, final export) — Midvale UT
Date: 2026-11-10 ~22:05 PKT. Tester: independent verifier (re-run). TEST ONLY — no
site code, content, CSS, or images were edited. Only this file, the screenshots,
the review PDF, and the run scripts/logs below were written.

## VERDICT — 10X RE-RUN — PROBLEMS: 1

Five of the six coordinator fixes verify clean with measurements. The sixth
(A-P1) is fixed in its filed form — the sticky bar no longer covers any hero
button on any page at any tested width — but the brief's literal 320px
criterion ("Button 1 AND Button 2 fully visible at scroll 0 at 320x700") is
NOT met on 9/21 pages: Button 2 sits 3–46px below the 700px fold there
(P1 below). Nothing else failed. Full regression counts are all green.

## METHOD
- Served the final export `out/` (export timestamp 2026-11-10 16:36 UTC; NOT
  re-exported — it was current) on 127.0.0.1:8335 with an extensionless-route
  mapping server (plain `python3 -m http.server` 404s extensionless routes —
  verified: `/emergency-water-extraction` → 404 on plain http.server, 200 on
  the mapping server; that is a server limitation, not a site defect).
- Python Playwright + headless Chromium. Desktop 1440x900, mobile 390x844,
  mobile 320x700. Stepped scroll before image measurement; instant scrolling
  for bar checks (the site sets `scroll-behavior: smooth`, so timed waits
  after smooth scrolls are unreliable — see script errors).
- Raw data: `qa/10x/rerun-results.json` (desktop + mobile per route,
  contrast, menu), `qa/10x/rerun-bar.json` (bar appear/tap/hover probe,
  42 entries), `qa/10x/rerun-diag.json` (crash probe, 24 loads),
  `qa/10x/rerun-diff.log` (word-diff), `/tmp/rerun-main.log` (run stdout).
- Scripts: `qa/10x/rerun-check.py`, `qa/10x/rerun-bar.py`,
  `qa/10x/rerun-diag.py`, `qa/10x/rerun-diff.py`, `qa/10x/rerun-pdf.py`.

## 1. PER-FIX VERDICTS

### Fix 1 — A-P1, sticky bar vs hero buttons at 320px — PARTIAL (see P1)
- Bar HIDDEN at scroll 0: 21/21 at 320x700, 21/21 at 390x844
  (`display: none`, class `sticky-bar bar-hidden`). Nothing covers either
  hero button anywhere — the filed defect (bar covering Button 2) is GONE.
- Button 1 fully visible at scroll 0 at 320x700: 21/21 (worst bottom 674px).
- Button 2 fully visible at scroll 0 at 320x700: 12/21. Below the fold on 9:
  46px below on 6 (swamp-cooler, hardwood, condo, contacts, cottonwood,
  south-salt-lake — bottom 746px), 15px below on 2 (emergency, basement —
  bottom 715px), 3px below on 1 (magna — bottom 703px). Seen in pixels:
  `swamp-cooler-leak-water-damage-mobile320-top.png` shows Button 1 full +
  only a ~10px sliver of Button 2 at the bottom edge; home shows both
  buttons fully (bottom 673px).
- At 390x844 Button 2 fully visible 21/21 (worst bottom 694px, viewport 844).
  At 1440 buttons visible 21/21.
- Bar APPEARS past the hero: 21/21 at 390 AND 21/21 at 320 (dedicated probe
  that scrolls to hero-bottom + 60px — the first run's scroll-to-900 was too
  shallow because heroes are 827–1096px tall at 390 and 983–1356px at 320).
  Bar is 63px tall, top = viewport-bottom − 63 (781 at 390, 637 at 320).
  Real mouse click on the bar centre lands on the bar link itself
  (`elementFromPoint` = the `<a>`) on 21/21 at both widths; URL unchanged
  after the tap (tel: link, no navigation). Scroll back to top → bar hidden
  again 21/21 at both widths.

### Fix 2 — D-P1, guide-page Note box deleted — VERIFIED FIXED
- `"not in the source document yet"` appears 0 times sitewide (grep over
  `out/` + fresh word-diff).
- Contacts page (`/midvale-water-sewer-emergency-contacts`) now carries only
  its one verbatim doc sentence — "For sewer backups, the Midvale Water &
  Sewer Emergency Contacts page lists who to call about the public line." —
  plus template chrome (header/nav/footer/trust/buttons). Word-diff:
  homepage 126/126 OK, 0 missing/changed; all 20 linked pages `extra=none`
  (see §3). The guide page now matches the doc exactly.

### Fix 3 — C-O4, body padding-bottom 63px = bar height — VERIFIED FIXED
- `body { padding-bottom: 63px; }` (in the ≤767px media query; desktop is
  0px, correct). Measured computed padding: 63px at 390 and 320 on 21/21.
- Rendered bar height measured: 63px on 21/21 at both widths.
- At page bottom (scrolled to max, bar visible): footer-base bottom = 781px
  at 390x844, bar top = 781px — footer content ends exactly where the bar
  begins; nothing is covered. 21/21.

### Fix 4 — C-O1, contrast ≥4.5:1 — VERIFIED FIXED
Computed (WCAG luminance from rendered styles, homepage):
| Element | Colours | Ratio | Verdict |
|---|---|---|---|
| Button 1 (white on copper-dark #9d5418) | rgb(255,255,255) / rgb(157,84,24) | **5.65** | PASS (was 3.90) |
| Header phone (same) | white / rgb(157,84,24) | **5.65** | PASS |
| Sticky-bar link (same) | white / rgb(157,84,24) | **5.65** | PASS |
| Button 2 (pine on white) | rgb(14,59,56) / white | 12.34 | PASS |
| Button 1 hover (#7c3f12) | white / rgb(124,63,18) | 8.15 | darker ✓ |
| Header phone hover (#7c3f12) | white / rgb(124,63,18) | 8.15 | darker ✓ |
- Observation (NOT counted): the sticky-bar link has no distinct `:hover`
  rule — on hover its background stays #9d5418 (5.65), it does not darken
  like Button 1 / header phone. No user impact on touch phones; contrast
  still passes at hover.

### Fix 5 — C-O3, mobile hamburger menu — VERIFIED FIXED
Tested at 390px on home AND emergency-water-extraction, plus 1440:
- Menu button visible, 46x46, `display: flex`, `aria-expanded="false"`,
  nav `display: none` initially — 2/2 pages.
- Click opens: `aria-expanded="true"`, nav `display: flex`, panel
  390x191 visible — 2/2.
- Clicking a nav link (Sewage Backup Cleanup) navigates AND closes the
  menu (`aria-expanded="false"`, nav hidden) — 2/2.
- Escape closes the open menu AND returns focus to the button — 2/2.
- Keyboard-only: Tab reaches the menu button in 2 Tabs (brand first),
  Enter opens it (`aria-expanded="true"`), Escape closes it
  (`aria-expanded="false"`) with focus back on the button — 2/2.
- At 1440 the button is hidden (`display: none`) and the normal nav shows
  (`display: flex`, 3 links) — verified.

### Fix 6 — B-O1, og:url — VERIFIED FIXED
- Exactly 1 `og:url` per page on 21/21, and `og:url` == canonical on 21/21.
- Homepage `og:url` == `http://localhost:3000/` (WITH trailing slash).
- All 20 inner pages `og:url` == their no-slash URL.
- Canonical exactly 1/page on 21/21; homepage with slash, inner no-slash.
  (Canonical was already correct; og:url now matches it.)

### Fix 7 — B-O2, 404 robots metas — RECORDED AS QUIRK (not a defect)
- `out/404.html` carries exactly two `<meta name="robots">` tags, BOTH
  `content="noindex"` — identical values, no contradiction. Live check:
  unknown path returns HTTP 404 serving that page; slash form of a service
  route returns 404; the 404 page is unlinked and absent from the sitemap
  (verified: no `404` in sitemap.xml). Both tags agree (most restrictive
  wins anyway), so this is a known quirk, NOT a defect — as briefed.

## 2. PROBLEM

### P1 (RESIDUAL A-P1) — At 320x700, hero Button 2 sits below the fold on 9/21 pages
- **Routes:** swamp-cooler-leak-water-damage, hardwood-floor-cabinet-drying,
  condo-apartment-water-damage, midvale-water-sewer-emergency-contacts,
  locations/cottonwood-heights-ut, locations/south-salt-lake-ut (Button 2
  bottom 746px = 46px below the 700px fold); emergency-water-extraction,
  basement-flooding-cleanup (715px = 15px below); locations/magna-ut
  (703px = 3px below).
- **Reproduction:** viewport 320x700, load the page, do not scroll. Button 1
  is fully visible; Button 2 is cut off at the bottom edge (only a sliver
  shows on the 46px pages). A short scroll (~46px) reveals it fully.
- **Why it counts:** the re-run brief's Fix-1 criterion is explicit —
  "Button 1 AND Button 2 fully visible at scroll 0 at 320x700" — and 9
  pages do not meet it. The cause is hero height at 320px (heroes are
  983–1356px tall there: wrapped breadcrumb + eyebrow + 3–4-line H1 +
  stacked buttons), not the bar.
- **Why it is residual, not the original defect:** the filed A-P1 defect was
  the bar COVERING Button 2 — that is fully fixed (bar hidden at scroll 0
  on 21/21; nothing overlaps either button). What remains is fold position,
  not overlap. Button 1 (the call action) is fully visible on 21/21, and
  at 390x844 (the primary mobile size) both buttons are fully visible
  on 21/21.
- **Context for the parent's call:** the sibling Pleasant Grove 10x round
  accepted the same 320px fold position as a documented limit ("hero
  buttons below fold at 320x700") rather than a must-fix. The coordinator
  may fix this the same way (shorten the 320px hero) or accept it as a
  limit here too — either way the measurement above is the evidence.
- **Fix (for the coordinator, not done here):** reduce 320px hero height
  enough that Button 2 bottom ≤ 700px on the 6 worst pages (needs ~46px:
  e.g. tighter hero padding / smaller H1 at ≤360px), then re-measure
  320x700 first paint on all 21.

## 3. REGRESSION (fresh, all 21 routes — no regressions found)

| Check | Result |
|---|---|
| HTTP 200 | 21/21; slash service form → 404 (expected, trailingSlash:false); unknown path → 404 |
| H1 | exactly 1/page, visible, 21/21; texts match Pass B table (home verbatim `24/7 Water Damage Restoration in Midvale, UT 84047`) |
| Self-canonical = sitemap form | 21/21, exactly 1/page (home with slash, inner no-slash) |
| Sitemap | 21 locs, 0 missing / 0 extra; `<lastmod>2026-11-10</lastmod>` date-only on 21/21 (single distinct value; read from the built file) |
| robots.txt | `User-agent: *` / `Allow: /` / `Sitemap: http://localhost:3000/sitemap.xml`; NO `Host:` line |
| Titles / meta descriptions | unique 21/21 each; home title 72ch verbatim; home description 138ch verbatim |
| FAQ | home only: 6 visible H3 questions == 6 FAQPage schema questions, same order; answers found in visible text; 0 FAQ schema on other pages |
| JSON-LD | parses, 0 errors on 21/21 (home: 4 blocks) |
| og:image + twitter:image | own hero on 21/21; `twitter:card` = `summary_large_image` 21/21 |
| Links | 21 distinct internal page paths, all HTTP 200, 0 broken; 0 orphans (all 21 reachable from homepage crawl); 0 self-links in body copy; 0 external hrefs |
| Body-copy link counts | one link per target per page, EXCEPT the known home exception: `/condo-apartment-water-damage` 2× on the homepage (card + insurance paragraph, as documented by Pass B) |
| Word-diff vs frozen-doc.txt | homepage 126/126 OK, 0 missing / 0 changed; cost ranges 5/5 verbatim; category table 3/3 verbatim; linked pages 16/16 service + 3/3 location + guide all OK, `extra=none` |
| Buttons | desktop 322x56 equal on 21/21; mobile 390 342x56; Button 1 = `(385) 337-3560` only, Button 2 = `Request Emergency Help`, 21/21 |
| Overflow | 0px on 21/21 at 1440, 390 AND 320 |
| Body font | 18px computed on 21/21 |
| FCP (desktop 1440) | max 600ms (home), min 176ms; DCL max 400ms; load max 800ms |
| LCP | this headless shell emits ZERO `largest-contentful-paint` entries on 21/21 (verified directly, same as Pass C) — **no LCP number is claimed**. Honest proxy: FCP + the LCP element is the preloaded hero `<img>` on every page (`fetchpriority="high"`, WebP 1600x1066) |
| CLS | 0 on 21/21 (layout-shift observer) |
| Weight (transfer) | max 2038KB (home, 20 images), min 502KB (water-damage-repair) |
| Images | 40/40 load (`naturalWidth > 0` after stepped scroll — home 20/20, every other route 1/1 hero); 40 unique srcs; 40 unique md5 on disk (21 heroes + 19 cards); max 182KB, min 28KB, 0 ≥ 200KB; exiftool on home hero shows only File/System tags (no EXIF/XMP/GPS) |
| Hero preload | exactly 1 image preload/page on 21/21 (own hero); total preload links 2/page — the second is the framework webpack JS chunk, not a hero duplicate |
| Meta robots (21 routes) | `index, follow` on 21/21 |
| Contamination sweep | 0 real hits (Tulsa/918-phone/Edmond/Plano/Pleasant Grove/Lancaster/Fort Myers/McDonough/Broken Arrow/Owasso/Naples/Tukwila/Oklahoma/Texas/Chesterfield) across `out/` + `app/` + `lib/` + `components/` + `public/`. Note: raw substring `918` appears only inside the CSS chunk hash `8458119918792bf4.css` — not a phone number; phone-form grep `(918` / `918-` / `918 ` = 0. Only phone anywhere: `(385) 337-3560`. Whole-token "AI" in filenames/alts = 0 (substring hits are `rep**ai**r` in "repair") |
| Footer map | iframe markup correct on home + service/guide pages (`title="Map: Midvale, UT 84047"`, `src="https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed"`); renders blank in this sandbox because google.com is unreachable (KNOWN caveat, not a defect); area pages have no map by design |

Per-route FCP / weight / images (desktop 1440, fresh):
home 600ms / 2038KB / 20 imgs; emergency 228 / 603 / 1; basement 328 / 573 / 1;
window-well 248 / 574 / 1; burst-pipe 280 / 604 / 1; sewage 408 / 594 / 1;
water-heater 376 / 552 / 1; swamp-cooler 220 / 615 / 1; ceiling 244 / 555 / 1;
crawl-space 288 / 605 / 1; hardwood 388 / 585 / 1; condo 280 / 575 / 1;
commercial 316 / 601 / 1; storm 272 / 591 / 1; mold 208 / 598 / 1;
leak-detection 176 / 530 / 1; water-damage-repair 240 / 502 / 1;
contacts 220 / 570 / 1; cottonwood 204 / 653 / 1; south-salt-lake 348 / 586 / 1;
magna 236 / 653 / 1. CLS 0 on all 21.

## 4. SCREENSHOTS VIEWED BY PIXELS
- Closely: home (mobile 320 + 390), emergency (desktop full + mobile 390),
  mold (desktop full), swamp-cooler (mobile 320 + 390), cottonwood
  (desktop full + mobile 390). All clean: hero photo reads, buttons equal
  and visible, no overflow, no crash, no bar at first paint, hamburger
  visible at 390/320.
- Pixel glance (contact sheets): all 21 mobile-390 tops + all 21 desktop
  tops — uniform, no crash screen, no missing hero, no broken layout.
- Note: desktop full-page shots show the fixed header repeated mid-image —
  a full-page-capture artifact of fixed elements, not a page defect
  (same class of artifact Pass A noted for the sticky bar).

## 5. SCRIPT ERRORS (mine — owned, NOT site defects)
1. **First run's "Application error" crash screens were MY server's fault,
   not the site's.** My first mapping server did not URL-decode paths, so
   the page JS chunk `/_next/static/chunks/app/%5Bslug%5D/page-*.js`
   returned 404 → `ChunkLoadError` → React #423 → the Next.js
   "Application error" screen on ~13% of loads (5/24 in the diagnostic
   probe; 6/63 screenshots in run 1). After adding `unquote()` the chunks
   return 200 and the diagnostic probe shows **0 crashes in 24 loads**,
   and the full re-run shows 0. The site was never at fault; the first
   run's screenshots from crashed loads were discarded and re-taken.
   (Plain `http.server` decodes URLs but 404s extensionless routes, so a
   mapping server is still required — it must decode.)
2. **Menu probe crashed run 1** because my script clicked a nav link to
   `/mold-remediation` — the header nav only contains Home + Emergency
   Water Extraction + Sewage Backup Cleanup (3 links). Fixed to click the
   sewage link; the menu then verified clean on both test pages.
3. **Smooth-scroll timing:** the site sets `scroll-behavior: smooth`, so
   `window.scrollTo(0, 900)` + 400ms waits caught mid-animation states
   (bar still hidden because the hero was still intersecting). Fixed with
   `behavior: 'instant'` + longer waits + a dedicated past-hero probe
   (scroll to hero-bottom + 60px).
4. **Run-1 desktop measurements were lost** when the menu crash aborted the
   script before its only (end-of-run) JSON write. Re-ran the full suite
   with incremental saves after each phase; nothing was lost the second time.
5. **A `pkill -f` twice matched my own shell** (the command line contained
   the server's own name) and killed the shell mid-command. Owned; used
   `fuser -k 8335/tcp` afterwards. No site impact.
6. A `python3 -c` page-count check had a shell-in-Python syntax slip; the
   PDF itself was fine (verified 42 pages afterwards with pypdf).

## 6. FILES
- Findings: `~/workspace/midvale-water-damage/qa/10x-rerun.md` (this file)
- Raw data: `qa/10x/rerun-results.json`, `qa/10x/rerun-bar.json`,
  `qa/10x/rerun-diag.json`, `qa/10x/rerun-diff.log`
- Scripts: `qa/10x/rerun-check.py`, `qa/10x/rerun-bar.py`,
  `qa/10x/rerun-diag.py`, `qa/10x/rerun-diff.py`, `qa/10x/rerun-pdf.py`
- Screenshots (42 required): `qa/10x/final/` — desktop full + mobile-390
  top per page; plus 21 supplementary 320px tops in `qa/10x/final-320/`
- Review PDF (42 pp): `~/workspace/your_files/midvale-10x-review.pdf`
  (29.5 MB); same 42 PNGs in
  `~/workspace/your_files/midvale-10x-screenshots/`
- Test server on port 8335 stopped after the run.

## 10X RE-RUN — PROBLEMS: 1
