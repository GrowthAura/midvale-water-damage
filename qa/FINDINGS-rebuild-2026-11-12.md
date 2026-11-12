# Midvale UT — Full-Content Rebuild — INDEPENDENT VERIFICATION FINDINGS
**Date:** 2026-11-12 ~21:30 PKT (verifier ran 20:42–21:30 PKT)
**Verifier:** independent — did NOT build this site; verified fresh from `lib/pages-data.json` + the built `out/` export + the full doc (`qa/r3-full-doc/`).
**Scope:** 31 routes, local subpath mirror `http://localhost:8324/midvale-water-damage/` (clean-URL server, GitHub-Pages-style mapping).
**Data hash (re-verified first):** `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — EXACT match, no patching.

## VERDICT — NOT READY for re-push as-is (live site already pushed 21:35 PKT on his override — fixes + re-push to follow)

## PROBLEMS: 6 (P2 x3, P3 x3)

### P2-1 — 10 new routes are orphans: zero inbound links from any page
- Routes: `/about`, `/contact`, `/privacy-policy`, `/terms-of-use`, `/disclaimer`, `/resources/frozen-pipes-midvale`, `/resources/winterize-swamp-cooler-utah`, `/resources/upstairs-unit-leak-who-pays-utah`, `/resources/can-mold-grow-in-utah`, `/resources/basement-flooding-spring-snowmelt-utah`.
- Evidence: full link-graph over all 31 built pages (header + footer + body). Header nav links only Home + Emergency + Sewage. Footer links only 8 services + 3 locations + emergency-contacts + `#faq`/`#services` anchors + tel: links. Nothing anywhere links to the 10 new routes. They are reachable ONLY via sitemap / direct URL. Violates the locked "0 orphans" gate.
- Fix: add footer links (Help/Resources nav) to About / Contact / Privacy / Terms / Disclaimer + the 5 blogs.

### P2-2 — Button 2 below the fold at 320x568 on 28/31 pages (regression vs Nov 10 10x fix)
- Measured in a real browser (Playwright Chromium), scroll-0, viewport 320x568. Button 2 bottom vs 568px fold:
  - `/` 574 (+6px), `/about` 659 (+91), `/contact` 629 (+61), `/emergency-water-extraction` 690 (+122), `/basement-flooding-cleanup` 727 (+159), `/window-well-flooding` 659 (+91), `/burst-pipe-water-damage` 727 (+159), `/sewage-backup-cleanup` 659 (+91), `/water-heater-leak-cleanup` 727 (+159), `/swamp-cooler-leak-water-damage` 727 (+159), `/ceiling-water-damage` 690 (+122), `/crawl-space-water-damage` 727 (+159), `/hardwood-floor-cabinet-drying` 690 (+122), `/condo-apartment-water-damage` 765 (+197), `/commercial-water-damage` 690 (+122), `/storm-flood-damage` 690 (+122), `/mold-remediation` 652 (+84), `/water-leak-detection` 727 (+159), `/water-damage-repair` 659 (+91), `/locations/cottonwood-heights-ut` 789 (+221), `/locations/south-salt-lake-ut` 758 (+190), `/locations/magna-ut` 690 (+122), `/midvale-water-sewer-emergency-contacts` 652 (+84), `/resources/frozen-pipes-midvale` 765 (+197), `/resources/winterize-swamp-cooler-utah` 690 (+122), `/resources/upstairs-unit-leak-who-pays-utah` 727 (+159), `/resources/can-mold-grow-in-utah` 690 (+122), `/resources/basement-flooding-spring-snowmelt-utah` 758 (+190).
  - Pass at 320x568: only `/privacy-policy`, `/terms-of-use`, `/disclaimer` (short H1s/intros).
  - Pass at 390x844 and desktop 1440x900: 31/31. Buttons equal everywhere (272x56 @320, 342x56 @390).
- Cause: the full tab H1s/intros make the hero taller than the old summary-only pages; the Nov 10 `@media (max-width:360px)` fix predates full content. This is a regression against the locked gate ("Button 2 visible at scroll-0 @320 and @390").
- Fix: CSS tweak for ≤360px (tighter hero padding / H1 / intro, or trust chips to one row) — re-measure 31/31 @320 after.

### P2-3 — Contact page has NO form, but its own content describes one (his call on the fix)
- Built `out/contact.html`: 0 `<form>`, 0 `<input>`, 0 `<textarea>`, 0 `<select>`.
- The Contact tab (Tab 3) references a form three ways, all rendered verbatim on the page:
  - Intro: "Prefer to send details first? Use the form below and we'll call you back right away."
  - H2 "Request Form Fields" + 6-field list: Name / Phone number / Address or ZIP code / What happened (short description) / Is the water still running? (Yes / No / Not sure) / Best time to call.
  - Paragraph "[Send My Request]" (the submit-button text) + "For active leaks or sewage, calling is faster than the form."
- The page as built therefore promises a form that does not exist. Fix is HIS call: add the 6-field form (Pages is static — a form cannot submit there; same notice/call-first treatment as the other sites) or decide otherwise. Do NOT delete the verbatim text.

### P3-1 — Next.js RSC prefetch 404 on every page load (console error 31/31 pages)
- Every page load fires `GET /midvale-water-damage.txt?_rsc=<token>` → 404 + `console.error: Failed to load resource: the server responded with a status of 404`. 31 distinct URLs (one per page; token differs). All 3 viewports.
- Cause: the header logo links home, and Next.js prefetches it; the home route's flight payload is requested at `{basePath}.txt`, but the static export carries it as `{basePath}/index.txt` (`out/index.txt`). On GitHub Pages the same request 404s (no such file) — this is live-visible console noise, not a mirror artifact.
- Impact: none user-visible — real-click navigation works (5/5 tests pass; prefetch failure degrades gracefully to full navigation), pages render fully. Pre-existing Next.js basePath static-export quirk (same header + export structure in the original build), NOT introduced by the rebuild.
- Fix option: `prefetch={false}` on the home/logo link.

### P3-2 — Homepage table-order inversion (1 instance site-wide)
- Data order (doc): table block 51 (water-category table), then paragraph block 52: "Clean water turns into gray water in about 48 hours as bacteria grow, so speed changes the whole job."
- Render order: the paragraph sits BEFORE the table (render positions 35 vs 36). Content is present verbatim; order is swapped.
- Checked all 43 tables: the other 30 tables with a following paragraph render in correct order. Single instance.
- Fix: render the paragraph after the table on the homepage.

### P3-3 — Mobile menu has no scroll lock (Round 3 P3, still open)
- Measured @390: with the menu open (`#main-nav.open`, display flex), `document.body` overflow stays `visible` — the page behind the menu still scrolls.
- Menu itself works: opens, links are 342x56, clicking a link navigates (subpath kept, correct H1) and closes the menu (display none). Pre-existing, not a rebuild regression.

---

## ADJUDICATED — NOT defects (checker artifacts / documented placeholders)

- **A1 — Sitemap/llms "homepage loc mismatch" (my first run flagged P1): CHECKER ARTIFACT.** Actual sitemap loc is `http://localhost:3000/` (WITH trailing slash — correct homepage form); my expected set used `http://localhost:3000` (no slash). Sitemap: 31 `<loc>`, 31 date-only `<lastmod>2026-11-12</lastmod>`. llms.txt: 31 URLs. PASS.
- **A2 — "localhost strings in built HTML": DOCUMENTED PLACEHOLDER, not a leak.** Every occurrence is canonical / og:url / og:image / twitter:image / JSON-LD `url` fields + the RSC flight-payload mirror of the same metadata. No localhost in visible text or asset URLs. Swaps with the real domain when it lands.
- **A3 — First segment run's 3 homepage "missing segments": TOKENIZER ARTIFACT.** React comment nodes split `(/locations/.../)` paths in visible text; the browser renders them verbatim. Re-run with a slash-splitting tokenizer: 0 missing on all 31 pages.
- **A4 — First static run's "234 missing words" + FAQ mismatches: MY SCRIPT BUGS, not site defects.** (a) The `faqs` array duplicates the FAQ H3+answer blocks — I counted FAQ content twice. (b) Dict-iteration bug in the FAQ loop. (c) `visible_text()` decomposed the JSON-LD `<script>` tags inside `<main>` before the schema check ran. Corrected run: missing = 0 on all 31 pages; FAQ schema = visible on 28/28 FAQ pages. My errors, owned plainly.
- **A5 — The builder's 2 failed exec calls: grep-no-match exits on gates that pass.** Re-verified independently: all gates 0.

## PASS — verified fresh (no sampling; 31/31 pages)

| Gate | Result |
|---|---|
| Data integrity | sha256 exact match; 31 pages; 45,832 content words |
| Verbatim (segment-level) | 3,116 segments checked; **0 missing** on all 31 pages (eyebrow, H1, intro, trust chips, every block, every table row, every FAQ Q&A as contiguous token sequences) |
| Verbatim (word multiset) | missing = 0 on all 31 pages; extra words 12–28/page are all documented chrome (hero buttons, breadcrumb, FAQ section heading, related-links headings) — 0 invented content words |
| Content fullness | **All 31 FULL** — main-body content words: home 2,178; services 1,524–1,875; locations 1,763–1,875; blogs 1,470–1,669; about 979; contact 693; emergency-contacts 1,268; privacy 508; terms 455; disclaimer 293 (short by doc, not thin). 0 EMPTY, 0 THIN |
| H1 | Exactly 1/page, text verbatim, visible in a real browser — 31/31 x 3 viewports |
| Titles / meta descriptions | Verbatim 31/31 each |
| Headings | All data H2/H3 present; H3 totals match (incl. FAQ questions as H3) |
| Tables | 43/43 rendered, cell-exact (incl. the 3-column water-category table) |
| FAQ | 142/142 — FAQPage schema Q&A = visible Q&A exactly, on all 28 FAQ pages (6 home, 5 each elsewhere; 0 on the 3 legal pages) |
| Render (real browser) | 0 white screens, 0 "Application error", 0 ChunkLoadError, H1 visible 31/31 x 3 viewports; body text 2,821–14,013 chars/page |
| Overflow | 0 px on all pages at 1440, 390, 320 |
| Hero buttons | Equal on all pages/viewports (272x56 @320, 342x56 @390); Button 1 = phone number only; Button 2 visible at scroll-0 on desktop + 390, 31/31 |
| Real-click navigation | 5/5 desktop clicks keep the subpath + land on the correct H1 (home→emergency, logo→home, footer→mold, header→sewage, breadcrumb→home); 0 page errors during clicks. **P1a white-screen crash FIXED. P1b subpath-drop FIXED.** |
| Mobile menu | Opens, links 342x56, click navigates + closes menu; sticky bar `fixed` after scroll (JS hydration works) |
| Links | 0 broken internal links; 0 body self-links |
| Sitemap / robots / llms | 31 locs, date-only lastmod 2026-11-12; robots `Allow: /`, NO `Host:`; llms.txt 31 routes |
| Grep gates (built HTML) | `//midvale-water-damage` = 0; unprefixed root-relative href/src = 0; unprefixed `<img>` src = 0; favicon prefixed on all 32 HTML files |
| Old-site traces | 0 (cities, phones, names, domains, lorem/TODO, other-site terms) |
| Images | 50 files, 0 md5 dups in-site; **0 md5 matches vs 4,618 past-site files**; 10 new heroes: **0 aHash8 ≤8 flags** vs the same 4,618 files; heroes 1600x1066 (31), cards 1200x675 (16) / 1200x800 (3); no EXIF/XMP/ICC chunks; no generator markers; no "AI" word in filenames or alt text. LIMIT (honest): no Pexels-ID sourcing log exists for the 10 new heroes, so the ID-based check could not run — the hash-based check above is what passed. The raw-bytes "ai" hits my scanner flagged on 6 heroes are random `Ai` byte pairs inside compressed VP8 data (offsets 3406/7963/19422), not metadata — adjudicated as noise. |

## Per-page table (main-body words = visible words in `<main>`, incl. chrome; expected = data content words)

| Route | Main words | Expected | Missing | Extra | Fullness | H1 | Title | Meta | FAQ schema |
|---|---:|---:|---:|---:|---|---|---|---|---|---|
| `/` | 2190 | 2178 | 0 | 12 | FULL | ✓ | ✓ | ✓ | 6/6 |
| `/about` | 999 | 979 | 0 | 20 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/contact` | 717 | 693 | 0 | 24 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/emergency-water-extraction` | 1821 | 1800 | 0 | 21 | FULL | ✓ | ✓ | ✓ | 6/6 |
| `/basement-flooding-cleanup` | 1719 | 1698 | 0 | 21 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/window-well-flooding` | 1788 | 1765 | 0 | 23 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/burst-pipe-water-damage` | 1886 | 1863 | 0 | 23 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/sewage-backup-cleanup` | 1746 | 1724 | 0 | 22 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/water-heater-leak-cleanup` | 1734 | 1711 | 0 | 23 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/swamp-cooler-leak-water-damage` | 1655 | 1631 | 0 | 24 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/ceiling-water-damage` | 1658 | 1636 | 0 | 22 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/crawl-space-water-damage` | 1665 | 1642 | 0 | 23 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/hardwood-floor-cabinet-drying` | 1792 | 1770 | 0 | 22 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/condo-apartment-water-damage` | 1787 | 1762 | 0 | 25 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/commercial-water-damage` | 1713 | 1690 | 0 | 23 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/storm-flood-damage` | 1660 | 1638 | 0 | 22 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/mold-remediation` | 1739 | 1719 | 0 | 20 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/water-leak-detection` | 1776 | 1753 | 0 | 23 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/water-damage-repair` | 1575 | 1553 | 0 | 22 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/locations/cottonwood-heights-ut` | 1790 | 1763 | 0 | 27 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/locations/south-salt-lake-ut` | 1902 | 1875 | 0 | 27 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/locations/magna-ut` | 1862 | 1837 | 0 | 25 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/midvale-water-sewer-emergency-contacts` | 1287 | 1268 | 0 | 19 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/privacy-policy` | 528 | 508 | 0 | 20 | FULL | ✓ | ✓ | ✓ | 0/0 |
| `/terms-of-use` | 476 | 455 | 0 | 21 | FULL | ✓ | ✓ | ✓ | 0/0 |
| `/disclaimer` | 312 | 293 | 0 | 19 | FULL | ✓ | ✓ | ✓ | 0/0 |
| `/resources/frozen-pipes-midvale` | 1697 | 1669 | 0 | 28 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/resources/winterize-swamp-cooler-utah` | 1544 | 1524 | 0 | 20 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/resources/upstairs-unit-leak-who-pays-utah` | 1579 | 1553 | 0 | 26 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/resources/can-mold-grow-in-utah` | 1496 | 1470 | 0 | 26 | FULL | ✓ | ✓ | ✓ | 5/5 |
| `/resources/basement-flooding-spring-snowmelt-utah` | 1501 | 1477 | 0 | 24 | FULL | ✓ | ✓ | ✓ | 5/5 |

## Still-open Round 3 items (pre-existing, NOT introduced by the rebuild — not counted in the 6 above)
- Card images ≠ linked pages' hero images: spot-check aHash8 distances 22 / 34 / 33 (different photos). Theme kept the existing 40 images.
- Schema below the most-advanced bar: no HowTo / SpeakableSpecification / WebPage `@id`. Present: Service, City, HomeAndConstructionBusiness, BreadcrumbList, FAQPage, WebSite. llms.txt now exists (31 routes).
- Titles >60ch (e.g. homepage 72ch verbatim — his call, unchanged).
- Footer map renders blank in the sandbox (google.com unreachable; markup verified correct) — needs a real-browser check.
- LCP not measurable in the headless shell — no number invented. FCP was 368ms max on the old build; not re-measured here.

## Live state note
The site was pushed live 2026-11-12 ~21:35 PKT on his explicit override ("push now, don't wait for verification") — main `1cbf688` + gh-pages `4ebfd4f`, 31/31 URLs verified 200 live by the main agent. This verification ran on the local export, which was copied as-is to gh-pages, so the findings above apply to the live site too. The P2 items need fixing + a re-push. A live-subpath re-run (real browser on the Pages URL) is still owed after the fixes.

## Evidence files
- This log: `qa/FINDINGS-rebuild-2026-11-12.md`
- Static checks: `qa/verify-rebuild.py` → `qa/verify-rebuild-static.json`
- Segment-level verbatim: `qa/verify-segments.py` → `qa/verify-segments.json`
- Ordered diff (superseded — difflib misattributes repeated tokens; kept for the record): `qa/verify-ordered-diff.py` → `qa/verify-ordered-diff.json`
- Browser render + real-click nav: `qa/verify-render.py` → `qa/verify-render.json`, screenshots `qa/render/` (93 PNGs: 31 routes x desktop 1440 / mobile 390 / mobile 320)
- Images: `qa/verify-images-scoped.py` → `qa/verify-images.json`
- Review pack: `~/workspace/your_files/midvale-rebuild-review.pdf` (31 pages, desktop + mobile 390 per route, 6.0 MB)
- Local subpath server used: `/tmp/midvale-serve/serve.py` on port 8324 (clean-URL mapping, Pages-style)

## Method notes (for the record)
- The parser's `counts.words` EXCLUDES FAQ words (verified: my_total − counts.words = faqQ + faqA exactly, every page) and the `faqs` array duplicates the FAQ H3+answer blocks. My first static run double-counted FAQs — corrected before the verdict.
- The ordered-diff (difflib) run is unreliable for this content: repeated common words let the greedy matcher misattribute the FAQ block. The segment-level contiguous check + word multiset (both with the duplication corrected) are the arbiters.
- Nothing was pushed, deployed, or changed in any site source file by this verification. No token used. No MEMORY.md edits.
