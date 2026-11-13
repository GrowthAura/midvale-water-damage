# Midvale UT — Link-Fix — COORDINATOR FINDINGS
**Date:** 2026-11-13 ~01:21–02:15 PKT
**Coordinator:** fix coordinator (spawned 01:21 PKT). **Verifier:** independent, fresh — qa/FINDINGS-linkfix-verify-2026-11-13.md.
**Scope:** 31 routes, LOCAL ONLY. No push/deploy/token/DNS. Parent pushes with the token.

## THE DEFECT (caught by HIM, screenshot, he is right)
Homepage location cards showed "Water Damage Restoration Cottonwood Heights (/locations/cottonwood-heights-ut/)" — the raw path as VISIBLE text. 330 occurrences in built HTML site-wide. His words: internal linking was decided; asking which link then copy-pasting the path as text is the blunder. The rebuild brief's "keep them as plain visible text" instruction is DEAD, overridden by his correction + his standing doc-link standard. Parenthetical `Phrase (/path/)` = LINK ANNOTATION: phrase = anchor, path = href, NEVER visible text.

## 1. INVENTORY (qa/link-inventory.json — classifier /tmp/classify3.py)
165 annotations in lib/pages-data.json; **164 VISIBLE** (1 schema-only duplicate: /commercial-water-damage faqs[4].a duplicates blocks[58]; FAQ answers render from blocks, faqs[] is schema-only — parens stripped from schema via stripAnnotations).

| Route | Visible | Kept | Dup | | Route | Visible | Kept | Dup |
|---|---:|---:|---:|---|---:|---:|---:|
| `/` | 21 | 20 | 1 | | `/storm-flood-damage` | 5 | 5 | 0 |
| `/about` | 16 | 16 | 0 | | `/hardwood-floor-cabinet-drying` | 4 | 4 | 0 |
| `/locations/south-salt-lake-ut` | 13 | 13 | 0 | | `/condo-apartment-water-damage` | 4 | 4 | 0 |
| `/locations/magna-ut` | 9 | 9 | 0 | | `/resources/can-mold-grow-in-utah` | 4 | 4 | 0 |
| `/water-heater-leak-cleanup` | 8 | 7 | 1 | | `/resources/basement-flooding-spring-snowmelt-utah` | 4 | 4 | 0 |
| `/locations/cottonwood-heights-ut` | 8 | 8 | 0 | | `/sewage-backup-cleanup` | 3 | 3 | 0 |
| `/emergency-water-extraction` | 7 | 7 | 0 | | `/crawl-space-water-damage` | 3 | 3 | 0 |
| `/mold-remediation` | 7 | 7 | 0 | | `/midvale-water-sewer-emergency-contacts` | 3 | 3 | 0 |
| `/ceiling-water-damage` | 6 | 6 | 0 | | `/resources/frozen-pipes-midvale` | 3 | 3 | 0 |
| `/water-leak-detection` | 6 | 6 | 0 | | `/resources/winterize-swamp-cooler-utah` | 3 | 3 | 0 |
| `/water-damage-repair` | 6 | 6 | 0 | | `/window-well-flooding` | 2 | 2 | 0 |
| `/basement-flooding-cleanup` | 5 | 5 | 0 | | `/swamp-cooler-leak-water-damage` | 2 | 2 | 0 |
| `/burst-pipe-water-damage` | 5 | 5 | 0 | | `/resources/upstairs-unit-leak-who-pays-utah` | 2 | 2 | 0 |
| `/commercial-water-damage` | 5 | 5 | 0 | | `/contact` | 1 | 1 | 0 |

0 on /privacy-policy, /terms-of-use, /disclaimer. **Totals: 164 visible, 162 kept, 2 dup-dropped, 0 self-dropped, 0 bad targets.** Dup-dropped: (a) homepage Condo body copy — service card links it first; (b) /water-heater-leak-cleanup blocks[36] ul[1] — earlier "see" occurrence wins. Both render as plain phrase text. Legitimate parentheticals (phone "(385) 337-3560") are NOT path annotations — only `(/.../)` forms count. No annotations in headings, intro, eyebrow, meta. Table: /locations/south-salt-lake-ut blocks[14], 8 rows, col 2 cell = exactly "Service Name (/slug/)".

**Anchor rule** (Acworth parse_tabs.py ported, revised for Midvale): text after the LAST clause boundary in {". ", "! ", "? ", ": ", ", "}, then a "see "/"learn more about " marker AFTER that boundary only (case-insensitive — avoids ordinary verbs like "or see dark spots"), then strip leading separators/verb prefixes. **NO truncation** — full phrase kept (his rule: a link anchored on only part of his phrase counts as missing; deliberate deviation from Acworth's 5-word truncation). Anchor words: 2w x11, 3w x92, 4w x20, 5w x29, 6w x12, 8w x1. One deliberate decision: / blocks[62] anchor "the Midvale Water & Sewer Emergency Contacts page" (8w, full noun phrase incl. "the" and "page"). Per-segment vs per-unit anchors: 0 diffs. 0 cross-segment anchors. 0 units with >1 annotation.

## 2. THE FIX (data untouched — annotations stay verbatim in pages-data.json; renderer interprets them)
- **NEW lib/links.tsx** — normSlug, extractAnchor, splitAnnotated (parts concatenate EXACTLY to the annotation-stripped text), stripAnnotations, LinkParts component. One real bug caught by the compiler during the fix: a raw U+2028 character inside a regex literal ("Unterminated regular expression literal") — fixed to the `/\u2028/g` escape; data has 0 em/en dashes and 0 U+2028, so the normalisation is a no-op.
- **components/doc-page.tsx** — paragraphs/list items/table cells/FAQ answers render via splitAnnotated with a per-page shared `seen` Set in document order; FAQPage schema answers via stripAnnotations; stale "stays PLAIN text" header comment replaced.
- **app/page.tsx** — service cards (16) + location cards (3) each restructured to a SINGLE wrapping Link (class `card-wrap-link`) around image + H3 + summary; body copy #17 dup-drops to plain text, #18 links. `linkSeen` pre-populated with the 16 service slugs (cards are first in document order).
- **app/globals.css** — `.card-wrap-link { display:flex; flex-direction:column; flex:1; color:inherit; text-decoration:none; }` + `.body-link { text-decoration:none; }` (his 2026-11-13 rule: NO underline/dash under internal links).
- **Build:** `npm run export` exit 0, 35/35 static pages (coordinator + verifier re-ran it, exit 0 both).

## 3. VERBATIM ACCOUNTING
` (/path/)` tokens are LINK METADATA, not content words. Visible words drop by exactly **164 tokens** site-wide (1 per visible annotation, whitespace-token count). The verifier's splitter counts sub-tokens inside paths (552 total); both accountings reconcile — **0 missing content words** on all 31 pages (2,980 segments checked). Extra words 749 site-wide, all chrome (hero buttons, phone, breadcrumb, FAQ headings; /contact +52 = documented form chrome).

## 4. INDEPENDENT VERIFICATION — PROBLEMS 0 (P1 x0, P2 x0, P3 x0)
Verifier: qa/FINDINGS-linkfix-verify-2026-11-13.md (+ qa/verify-linkfix-static.json, qa/verify-linkfix-render.json, scripts qa/verify-linkfix.py, qa/verify-linkfix-render.py, server /tmp/linkfix-serve.py). Re-measured fresh, nothing trusted from the fixer.

| Gate | Result |
|---|---|
| Visible-text paren gate | PASS. `\(/[^)]+/\)` = 0 in rendered DOM innerText (body AND main) on 31/31 x 3 viewports, 0 in out/ HTML/TXT/XML/CSS. |
| Verbatim | PASS. 0 missing, 0 reordered, all 31 pages. |
| Links | PASS. 162 kept = 143 body-link + 19 card-wrap-link (per-page counts match inventory on all 31). 2 dup-dropped plain in place. 0 body self-links, 0 broken, 0 orphans. Footer intact (Services 8, Nearby 3, About & Resources 10, Help 4). |
| Cards | PASS. 19/19 single-link units, exactly 1 `<a>` per card, 0 nested, image + H3/lead + summary inside. |
| Fullness | PASS. 31/31 FULL (min 312 words, disclaimer). |
| H1/meta/FAQ/tables | PASS. H1 1/page, meta verbatim 31/31, FAQ 142/142 (schema = visible = stripped data), tables 43/43 cell-exact. |
| Button 2 scroll-0 | PASS. 31/31 @320 AND 31/31 @390 (worst bottom 493px vs 568 fold @320). Buttons equal everywhere. |
| Render | PASS. 0 white screens, console errors 0, failed requests 0, overflow 0 (93 views). Real-click nav 7/7 subpath kept. Mobile menu opens + scroll-locks (see note below). |
| Schema | PASS. All JSON-LD parses, 0 errors; FAQPage answers = visible answers. |
| CSS | PASS. Computed `text-decoration-line: none` on both link classes. Cards 3-across, equal heights, images 337x189 = 16:9. Pixel-diff of all 93 fresh screenshots vs pre-fix baseline: **0 differing pixels** — zero layout shift. |
| Review pack | REGENERATED. ~/workspace/your_files/midvale-linkfix-review.pdf — 31 pp, 6.0 MB. |

## 5. COORDINATOR SPOT-CHECKS (my own, on the verifier's artifacts)
Recomputed from qa/verify-linkfix-render.json + qa/verify-linkfix-static.json + fresh greps — all verifier numbers confirmed: Button 2 31/31 @320 (worst 493px, snowmelt resource) and 31/31 @390; console/failed/overflow all 0; desktop buttons equal 31/31; nav 7 clicks with correct H1s; static totals body 143 / card 19 / kept 162 = expected, missing 0, sitemap 31, llms 31, double-slash 0, unprefixed 0; data sha256 unchanged 21c6e7f2…; git status shows ONLY the fixer's files modified (PROGRESS.md, app/globals.css, app/page.tsx, components/doc-page.tsx + new lib/links.tsx) — verifier touched no sources; review pack 31 pages, 5,951,375 bytes.
- **Correction 1 (counting, not a defect): raw-byte paren matches = 22, not 7.** My byte scan over all of out/: 7 in framework JS chunks + 15 in .webp binaries. The verifier's list showed a 7-entry subset. None in HTML/TXT/XML/CSS, none visible, none an annotation string.
- **Correction 2 (counting, not a defect): ASCII annotation-pattern scan finds 2 matches, both exactly `(//)`** — inside the Next.js router error string ("Repeated forward-slashes (//)…") in the 258- and main- chunks. Not annotation strings. The verifier's "0" was a slip; the substance (no real annotation string in any JS/webp file) holds.
- **Mobile-menu click re-test:** the JSON's mobile_nav still carries the verifier's stale-locator timeout (it looked for a burst-pipe link that never existed in the 3-link header nav: Home + Emergency + Sewage). The focused re-test is documented in the findings (script /tmp/linkfix-menu-test.py, correct locator: opens, scroll-locks, click navigates with subpath kept, menu closes, lock releases). Menu open/lock state IS in the JSON; site.tsx is unchanged since the rebuild verification passed the same menu. No site defect.

## VERDICT — READY FOR RE-PUSH
PROBLEMS 0. The link-fix is verified ready; the parent pushes with the token. NOT pushed by the fixer or the verifier.
Still open (his call / later): canonicals/og/sitemap still localhost placeholder (swap on real domain); homepage ~2MB; meta title 72ch verbatim; real job photos vs generated images; footer map blank in sandbox; LCP re-measure on real hosting. DESIGN ROUND ordered 2026-11-13 ~01:30 PKT runs next (separate coordinator, after this fix — same build dir, no parallel edits).
