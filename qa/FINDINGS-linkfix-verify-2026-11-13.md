# Midvale UT — Link-Fix — INDEPENDENT VERIFICATION FINDINGS
**Date:** 2026-11-13 ~01:40–02:10 PKT
**Verifier:** independent — did NOT build the link fix; verified fresh from `lib/pages-data.json` + `qa/link-inventory.json` + the rebuilt `out/` export + a real-browser render.
**Scope:** 31 routes, local subpath mirror `http://localhost:8324/midvale-water-damage/` (clean-URL server, GitHub-Pages-style mapping).
**Data hash (re-verified first):** `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — EXACT match to the rebuild-verified value; the fix touched no data.

## VERDICT — READY for re-push

## PROBLEMS: 0 (P1 x0, P2 x0, P3 x0)

## Build proof (re-run by me, not trusted from the fixer)
- `npm run export` exit 0, twice (35/35 static pages). All 32 HTML md5s changed between my two exports — adjudicated: Next.js embeds a random `buildId` per build (`TaCf0I86QpYxb6-Py0kIA` vs `RhtSeqqtn2MAs2uhPo4m-`); run-1 vs run-2 `out/index.html` is byte-identical after normalising only the buildId string. Content is deterministic; the fixer's `out/` (built from the same sources) differs only by its own buildId. No source file was modified by this verification.

## Per-gate results

| Gate | Result |
|---|---|
| 1. Visible-text paren gate | **PASS.** `\(/[^)]+/\)` = **0** in rendered DOM `innerText` (body AND main) on 31/31 pages x 3 viewports (Playwright/Chromium), and **0** in `out/` HTML/TXT/XML/CSS. Remaining raw-byte matches: 7 total — 4 in framework JS chunks (2x URL-scheme regex `(/^[a-zA-Z]{1,}:\/\//)` in `258-*` + `main-*` chunks, 2x `String.split` polyfill regexes in `polyfills-*`), 3 in `.webp` binaries (compressed-byte noise). An ASCII-only annotation scan (`\(/[a-z0-9\-/]+/\)`) over all JS chunks + all webp files returns **0** — none of the 7 is an annotation string and none is visible. (Fixer said "1 webp"; I count 3 webp files with raw-byte matches — all non-ASCII noise, not annotations.) |
| 2. Verbatim (annotation-adjusted) | **PASS.** Missing words **0** on all 31 pages; 2,980 segments checked, 0 missing, 0 reordered (annotations stripped from expected segments first). Accounting: expected visible = data content tokens − annotation path tokens (552 tokens subtracted site-wide across 164 visible annotations; per-page drops match the rebuild verifier's main-word counts exactly, e.g. home 2190→2115, about 999→945). Extra words 749 site-wide, per-page counts identical to the rebuild verifier's except `/contact` 76 vs 24 — the +52 is the documented contact-form chrome (6 fields + notice). All extras are chrome (hero buttons, phone, breadcrumb, FAQ section headings, form labels). |
| 3. Links | **PASS.** **162 kept links total: 143 `body-link` + 19 `card-wrap-link`** (per-page counts match `qa/link-inventory.json` on all 31 pages; every kept record's anchor text verified inside a link with the matching href). **2 dup-dropped** render as plain phrase text, verified in place: homepage Condo sentence ("If water came from an upstairs unit…") and `/water-heater-leak-cleanup` blocks[36] ul[1] ("Hardwood boards cupping…") — neither contains a `body-link`. **0 body self-links. 0 broken links** (every body/card href resolves to a built route under the basePath prefix). **0 orphans** (whole-page link graph incl. header/footer). Footer intact: Services 8, Nearby cities 3, **About & Resources 10** (About, Contact, Privacy, Terms, Disclaimer + 5 resources, hrefs exact), Help 4. |
| 4. Cards | **PASS.** 19/19 homepage cards are a SINGLE link unit: exactly 1 `<a>` per `article.card`, class `card-wrap-link`, 0 nested `<a>`, image + H3 (services) / `<strong>` lead (locations) + summary inside the link. Hrefs = the 16 service slugs + 3 location slugs. |
| 5. Fullness | **PASS. 31/31 FULL.** Main-body words 312–2,115 (min: `/disclaimer` 312; max: home 2,115). 0 EMPTY, 0 THIN. |
| 6. H1 / meta / FAQ / tables | **PASS.** H1 exactly 1/page, verbatim, 31/31. Meta title + description verbatim 31/31 each. **FAQ 142/142** — FAQPage schema answers = visible answers = stripped data answers on all 28 FAQ pages (0 on the 3 legal pages); schema answers contain no parens; all JSON-LD parses. **Tables 43/43** cell-exact (compared against annotation-stripped expected cells). |
| 7. Button 2 at scroll-0 | **PASS. 31/31 at 320px AND 31/31 at 390px** (rendered check). Worst Button 2 bottom @320x568: 493px (condo + snowmelt resource) vs the 568px fold; min 373px. Buttons equal on all pages/viewports. |
| 8. Render | **PASS.** Real browser, 31 routes x 3 viewports: 0 white screens, 0 "Application error", 0 ChunkLoadError, **console errors 0, failed requests 0**, overflow 0px everywhere, body text ≥500 chars on every view. Real-click nav 7/7 with subpath kept: card→emergency, body-link→emergency-contacts, inner body-link→hardwood, footer→mold, header→sewage, logo→home, breadcrumb→home. Mobile menu: opens (flex, aria-expanded true), scroll locks (body overflow hidden + position fixed), link click navigates + menu closes + lock releases. |
| 9. Schema | **PASS.** FAQPage answers equal visible answers (no parens) — see Gate 6. All `application/ld+json` blocks parse as JSON on all 31 pages (0 parse errors). |
| 10. CSS | **PASS.** Computed `text-decoration-line: none` on `.body-link` and `.card-wrap-link` on every sampled page. Card layout unchanged: cards 3-across at 1440px, equal heights within each row (503/503/503, 473/473/473…), card images rendered 337x189 = **16:9 (1.778)** on all 19 via `.card-img { aspect-ratio: 16/9; height: auto; object-fit: cover }`. Pixel-diff of all 93 fresh screenshots vs the pre-fix baseline (rebuild verification, 2026-11-12 17:01): **0 differing pixels** — zero layout shift, zero visual change. |
| 11. Review pack | **REGENERATED.** `~/workspace/your_files/midvale-linkfix-review.pdf` — 31 pages, 6.0 MB (desktop 1440 + mobile 390 per route, from the fresh screenshots). |
| 12. Findings | This file: `qa/FINDINGS-linkfix-verify-2026-11-13.md`. |

## Per-page table (main words = visible words in `<main>`; expected-visible = data content words − annotation path tokens)

| Route | Main | ExpVis | Missing | Extra | Full | Body | Card | SegMiss | FAQ | H1 | Title | Meta |
|---|---:|---:|---:|---:|---|---|---|---|---|---|---|---|---|
| `/` | 2115 | 2103 | 0 | 12 | FULL | 1 | 19 | 0 | 6/6 | ✓ | ✓ | ✓ |
| `/about` | 945 | 925 | 0 | 20 | FULL | 16 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/contact` | 764 | 688 | 0 | 76 | FULL | 1 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/emergency-water-extraction` | 1797 | 1776 | 0 | 21 | FULL | 7 | 0 | 0 | 6/6 | ✓ | ✓ | ✓ |
| `/basement-flooding-cleanup` | 1702 | 1681 | 0 | 21 | FULL | 5 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/window-well-flooding` | 1782 | 1759 | 0 | 23 | FULL | 2 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/burst-pipe-water-damage` | 1868 | 1845 | 0 | 23 | FULL | 5 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/sewage-backup-cleanup` | 1737 | 1715 | 0 | 22 | FULL | 3 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/water-heater-leak-cleanup` | 1706 | 1683 | 0 | 23 | FULL | 7 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/swamp-cooler-leak-water-damage` | 1650 | 1626 | 0 | 24 | FULL | 2 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/ceiling-water-damage` | 1636 | 1614 | 0 | 22 | FULL | 6 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/crawl-space-water-damage` | 1654 | 1631 | 0 | 23 | FULL | 3 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/hardwood-floor-cabinet-drying` | 1777 | 1755 | 0 | 22 | FULL | 4 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/condo-apartment-water-damage` | 1774 | 1749 | 0 | 25 | FULL | 4 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/commercial-water-damage` | 1700 | 1677 | 0 | 23 | FULL | 4 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/storm-flood-damage` | 1645 | 1623 | 0 | 22 | FULL | 5 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/mold-remediation` | 1714 | 1694 | 0 | 20 | FULL | 7 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/water-leak-detection` | 1756 | 1733 | 0 | 23 | FULL | 6 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/water-damage-repair` | 1555 | 1533 | 0 | 22 | FULL | 6 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/locations/cottonwood-heights-ut` | 1766 | 1739 | 0 | 27 | FULL | 8 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/locations/south-salt-lake-ut` | 1860 | 1833 | 0 | 27 | FULL | 13 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/locations/magna-ut` | 1833 | 1808 | 0 | 25 | FULL | 9 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/midvale-water-sewer-emergency-contacts` | 1278 | 1259 | 0 | 19 | FULL | 3 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/privacy-policy` | 528 | 508 | 0 | 20 | FULL | 0 | 0 | 0 | 0/0 | ✓ | ✓ | ✓ |
| `/terms-of-use` | 476 | 455 | 0 | 21 | FULL | 0 | 0 | 0 | 0/0 | ✓ | ✓ | ✓ |
| `/disclaimer` | 312 | 293 | 0 | 19 | FULL | 0 | 0 | 0 | 0/0 | ✓ | ✓ | ✓ |
| `/resources/frozen-pipes-midvale` | 1686 | 1658 | 0 | 28 | FULL | 3 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/resources/winterize-swamp-cooler-utah` | 1534 | 1514 | 0 | 20 | FULL | 3 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/resources/upstairs-unit-leak-who-pays-utah` | 1571 | 1545 | 0 | 26 | FULL | 2 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/resources/can-mold-grow-in-utah` | 1485 | 1459 | 0 | 26 | FULL | 4 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |
| `/resources/basement-flooding-spring-snowmelt-utah` | 1488 | 1464 | 0 | 24 | FULL | 4 | 0 | 0 | 5/5 | ✓ | ✓ | ✓ |

**Site totals:** main words 47,094; expected-visible 46,345; missing 0; extra 749; annotation path tokens subtracted 552; sitemap 31 locs, lastmod all `2026-11-12`; llms.txt 31 URLs; robots `Allow: /`, no `Host:`; grep gates `//midvale-water-damage` 0, unprefixed href/src 0.

## My script errors — owned plainly (all fixed, all re-run; none were site defects)
1. **Static checker, first run (33 flags):** three of my own bugs — (a) `norm_href` treated `/midvale-water-damage#faq` / `#services` footer anchor links as "unprefixed" (they ARE basePath-prefixed root+fragment links); (b) the table check compared raw data cells containing ` (/path/)` against stripped rendered cells; (c) the dup-dropped check tested "is this anchor text linked anywhere on the page", which the *kept* occurrence of the same target legitimately satisfies — the dup occurrence itself is covered by the targeted context check, which passed both cases. Fixed all three, re-ran: **PROBLEMS 0**.
2. **Render server, first run:** my serve script did not percent-decode request paths, so Chromium's encoded chunk URLs (`app/%5Bslug%5D/page-*.js`) 404'd and a few viewports intermittently showed "Application error" (body text 103) with ChunkLoadError. The built HTML itself references the chunk percent-encoded and the file on disk is `app/[slug]/…` — GitHub Pages decodes `%5B` the same way my fix does. Fixed the server (`urllib.parse.unquote`), curl-verified the encoded chunk URL 200, re-ran the full render: **0 console errors, 0 failed requests, 0 application errors on all 93 views**. The first run's paren counts (0 everywhere) already agreed with the clean re-run.
3. **Mobile-menu locator (inherited stale from the rebuild script):** `#main-nav a[href*='burst-pipe-water-damage']` timed out in both render runs — because the header nav only ever contains Home + Emergency + Sewage (3 links); no burst-pipe link exists there. Focused re-test with the real sewage link: menu opens, scroll locks, click navigates with subpath kept, menu closes, lock releases. My locator was wrong, not the site.

## Adjudicated — NOT defects
- **A1 — "logo→home / breadcrumb→home subpath_kept false" (checker artifact).** The landing URL is `http://localhost:8324/midvale-water-damage` (bare subpath root, no trailing slash) — correct; my check searched for `/midvale-water-damage/` with a trailing slash. The URL is the subpath root and the H1 is the homepage H1.
- **A2 — "localhost strings in built HTML" (documented placeholder, as in the rebuild verification).** Canonical / og:url / JSON-LD `url` fields only; 0 in visible copy. Swaps with the real domain when it lands.
- **A3 — Body-link anchors are visually indistinguishable from plain text.** Intended: his 2026-11-13 rule is no underline under internal links, and `.body-link` inherits colour. Verified by computed style (`text-decoration-line: none`) + the 0-pixel screenshot diff. A reader cannot tell a body link from plain text by looking — that is the design, not a defect.
- **A4 — Card image files: 16 are 1200x675, 3 are 1200x800 natural.** Pre-existing (rebuild findings), unchanged by this fix. All 19 *render* at 16:9 (337x189) via `aspect-ratio: 16/9` + `object-fit: cover`.

## Not re-verified in this round (unchanged by the link fix, out of scope)
- Image reuse vs past sites (rebuild verification: 0 md5 matches vs 4,618 past-site files; no image file changed in this fix).
- LCP / footer map tiles (sandbox egress blocks google.com; map markup unchanged).
- The design round ordered 2026-11-13 ~01:30 PKT runs after this verification in the same build dir — this verdict covers the link-fix build only.

## Evidence files
- This log: `qa/FINDINGS-linkfix-verify-2026-11-13.md`
- Static checks: `qa/verify-linkfix.py` → `qa/verify-linkfix-static.json`
- Browser render + real-click nav: `qa/verify-linkfix-render.py` → `qa/verify-linkfix-render.json`, screenshots `qa/render/` (93 PNGs: 31 routes x desktop 1440 / mobile 390 / mobile 320), local subpath server `/tmp/linkfix-serve.py` (port 8324)
- Focused re-tests: `/tmp/linkfix-menu-test.py` (mobile menu, correct locator), `/tmp/linkfix-cardshot.py` (card grid + body-link close-ups, viewed by pixels)
- Pre-fix screenshot baseline (for the pixel diff): `/tmp/linkfix-render-before/` (93 PNGs, rebuild verification 2026-11-12)
- Review pack: `~/workspace/your_files/midvale-linkfix-review.pdf` (31 pages, 6.0 MB) — built by `qa/build-review-pdf-linkfix.py`
- Nothing was pushed, deployed, or changed in any site source file by this verification. No token used. No MEMORY.md edits.
