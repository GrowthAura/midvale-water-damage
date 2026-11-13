# OPT1 — Content Visibility Audit — Midvale UT (Batch 2, Cycle 1)

**Date:** 2026-11-13 · **Method:** Playwright Chromium, rendered state (never curl alone). Local `out/` served on `/midvale-water-damage/` (port 8351). Desktop 1280×800 + mobile 390×844, each page measured at load AND after scrolling the whole page. `Visible` = actually rendered (display / visibility / opacity / clip / aria-hidden / layout-rect checks); below-fold text counts as visible because it renders — only content that is *not rendered* counts as hidden. Data `lib/pages-data.json` sha256 verified `21c6e7f2…d638f` (matches the assigned hash). Audit-only: no site source file was modified.

## Verdict
**PROBLEMS 0 — content 101% visible.** Every doc word renders; nothing is hidden behind an accordion, tab, reveal, or cutoff on desktop or mobile.

## Totals (31 routes)

- **Total visible words (body): 50213** — Stage 5 baseline ~51,060 (delta -847)
- **Main-body visible words: 46152** — Stage 5 baseline ~46,379 (delta -227)
- Baseline-delta note: the deltas are counting-method, **not missing content** — the verbatim diff against the doc is exactly 0 on all 31 pages. The Stage 5 baseline was approximate (“~”) and this count excludes the 552 `(/path/)` annotation tokens (link metadata that never renders) and tokenises “24/7”-style tokens as single words.
- **Unique prose words (main minus template blocks repeated on ≥10 pages): 45744**
- **Doc words (data `counts`): 45832** (expected doc tokens incl. eyebrow/H1/intro/chips/FAQ: see per-page table)
- **Hidden words in `<main>`: 0 at load, 0 after full scroll (desktop); mobile hidden-in-main at load: 0, after scroll: 0**
- **Hidden words outside `<main>` (header/footer/sticky chrome): 124 at load, 124 after scroll (desktop)** — see inventory; all of it is template chrome, no doc content.
- **FAQ: 142/142 rendered, 142/142 answers rendered-visible at load, 2928 answer words, 0 missing from DOM, 0 missing from visible text**
- **Verbatim: 0 doc tokens missing from visible main text across all pages; 749 extra tokens in visible main text (template chrome: buttons, nav, related cards, CTAs — expected, not doc words)**
- **Fullness: 31/31 FULL, 0 THIN, 0 EMPTY** (EMPTY = main <100, THIN = 100–300)

## PROBLEMS

None. 0 problems.

## Hidden-content inventory

Definition: text present in the DOM but NOT rendered at first paint (display:none / visibility:hidden / opacity:0 / height-0+overflow-hidden clip / aria-hidden / no layout rect), re-checked after scrolling the whole page. Below-fold content is NOT listed — it renders and is visible on scroll.

### Inside `<main>` (doc content lives here)
- **None. 0 words hidden inside `<main>` on any page, desktop or mobile, at load or after scroll.**

### Outside `<main>` (template chrome only)
- `/` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/about` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/contact` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/emergency-water-extraction` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/basement-flooding-cleanup` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/window-well-flooding` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/burst-pipe-water-damage` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/sewage-backup-cleanup` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/water-heater-leak-cleanup` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/swamp-cooler-leak-water-damage` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/ceiling-water-damage` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/crawl-space-water-damage` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/hardwood-floor-cabinet-drying` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/commercial-water-damage` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/storm-flood-damage` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/mold-remediation` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/water-leak-detection` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/water-damage-repair` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/locations/cottonwood-heights-ut` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/locations/south-salt-lake-ut` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/locations/magna-ut` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/midvale-water-sewer-emergency-contacts` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/privacy-policy` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/terms-of-use` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/disclaimer` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/resources/frozen-pipes-midvale` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/resources/winterize-swamp-cooler-utah` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/resources/upstairs-unit-leak-who-pays-utah` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/resources/can-mold-grow-in-utah` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/resources/basement-flooding-spring-snowmelt-utah` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”
- `/condo-apartment-water-damage` — 4 words — a. — display:none (div.sticky-bar) — “Call (385) 337-3560 · 24/7”

### Mechanisms checked (source + rendered state)

- **FAQ accordion: NONE EXISTS.** FAQ answers are plain `<h3>` + `<p>` inside `.faq-item` (components/doc-page.tsx, app/page.tsx) — no button, no collapse, no `details/summary`, no `aria-expanded`. All 142 answers are rendered-visible at load on every page.
- **Scroll-reveal: `.reveal { opacity: 1 }`** (app/globals.css:352) — wrapper only, content is never hidden; verified rendered: 0 words hidden in `<main>` after a full scroll-through on all 31 pages.
- **Tabs / “read more” cutoffs: none found** — no tab component, no truncated prose, no `max-height` clamp on prose in globals.css.
- **`display:none` in CSS is template chrome only:** desktop `.menu-btn`, mobile `.main-nav` when the menu is closed (≤900px, nav links — template, no doc words), `.sticky-bar` on desktop and while the hero is on screen on mobile (template call bar), `.table-wrap::after` scroll-fade pseudo-element (empty content, 0 words).
- **`[hidden]`, `aria-hidden=true`, closed `<details>`: 0 elements carrying doc text on any page.**

## FAQ — 142 Q&A

- Rendered `.faq-item`: **142/142**; answers rendered-visible at load: **142/142**; answer words total: **2928**; question words total: **1149**.
- Every FAQ question and answer string from `lib/pages-data.json` was checked verbatim (normalised) against the page DOM text and against the visible main text: **0 missing from DOM, 0 missing from visible text**. FAQ answers match the visible FAQ exactly — there is no separate hidden copy.

## Verbatim

- Expected visible text = doc text with `Phrase (/path/)` link annotations stripped (164 annotations, 552 tokens — link metadata that per lib/links.tsx must NEVER render as visible text; the anchor phrase stays visible). Against that: **0 doc tokens missing** from visible main text across 31 pages (0 expected — see PROBLEMS if >0). Extra tokens in visible main text: **749** — all template chrome inside `<main>` (the two call buttons, related-service/location/guide card text, process labels, final-CTA template copy on the homepage). Every missing-token check is a multiset comparison of normalised tokens (lowercase, punctuation stripped).

## Per-page table

| Route | Doc words | Total visible | Main visible | Unique prose | Hidden main (load → scroll) | FAQ rendered / ans. vis. | FAQ ans. words | Missing tokens | Fullness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `/` | 2107 | 2208 | 2077 | 2067 | 0 → 0 | 6 / 6 | 175 | 0 | FULL |
| `/about` | 929 | 1055 | 924 | 913 | 0 → 0 | 5 / 5 | 70 | 0 | FULL |
| `/contact` | 679 | 872 | 741 | 730 | 0 → 0 | 5 / 5 | 70 | 0 | FULL |
| `/emergency-water-extraction` | 1762 | 1897 | 1766 | 1755 | 0 → 0 | 6 / 6 | 136 | 0 | FULL |
| `/basement-flooding-cleanup` | 1662 | 1801 | 1670 | 1655 | 0 → 0 | 5 / 5 | 136 | 0 | FULL |
| `/window-well-flooding` | 1744 | 1887 | 1756 | 1741 | 0 → 0 | 5 / 5 | 131 | 0 | FULL |
| `/burst-pipe-water-damage` | 1825 | 1967 | 1836 | 1821 | 0 → 0 | 5 / 5 | 143 | 0 | FULL |
| `/sewage-backup-cleanup` | 1699 | 1841 | 1710 | 1695 | 0 → 0 | 5 / 5 | 151 | 0 | FULL |
| `/water-heater-leak-cleanup` | 1678 | 1812 | 1681 | 1666 | 0 → 0 | 5 / 5 | 104 | 0 | FULL |
| `/swamp-cooler-leak-water-damage` | 1611 | 1757 | 1626 | 1611 | 0 → 0 | 5 / 5 | 92 | 0 | FULL |
| `/ceiling-water-damage` | 1601 | 1741 | 1610 | 1595 | 0 → 0 | 5 / 5 | 112 | 0 | FULL |
| `/crawl-space-water-damage` | 1617 | 1760 | 1629 | 1614 | 0 → 0 | 5 / 5 | 101 | 0 | FULL |
| `/hardwood-floor-cabinet-drying` | 1742 | 1882 | 1751 | 1736 | 0 → 0 | 5 / 5 | 96 | 0 | FULL |
| `/condo-apartment-water-damage` | 1708 | 1848 | 1717 | 1702 | 0 → 0 | 5 / 5 | 74 | 0 | FULL |
| `/commercial-water-damage` | 1651 | 1791 | 1660 | 1649 | 0 → 0 | 5 / 5 | 66 | 0 | FULL |
| `/storm-flood-damage` | 1609 | 1748 | 1617 | 1602 | 0 → 0 | 5 / 5 | 80 | 0 | FULL |
| `/mold-remediation` | 1673 | 1810 | 1679 | 1664 | 0 → 0 | 5 / 5 | 106 | 0 | FULL |
| `/water-leak-detection` | 1721 | 1860 | 1729 | 1714 | 0 → 0 | 5 / 5 | 90 | 0 | FULL |
| `/water-damage-repair` | 1516 | 1650 | 1519 | 1504 | 0 → 0 | 5 / 5 | 97 | 0 | FULL |
| `/locations/cottonwood-heights-ut` | 1729 | 1864 | 1733 | 1718 | 0 → 0 | 5 / 5 | 101 | 0 | FULL |
| `/locations/south-salt-lake-ut` | 1811 | 1941 | 1810 | 1795 | 0 → 0 | 5 / 5 | 81 | 0 | FULL |
| `/locations/magna-ut` | 1791 | 1925 | 1794 | 1779 | 0 → 0 | 5 / 5 | 78 | 0 | FULL |
| `/midvale-water-sewer-emergency-contacts` | 1236 | 1374 | 1243 | 1232 | 0 → 0 | 5 / 5 | 116 | 0 | FULL |
| `/privacy-policy` | 505 | 654 | 523 | 512 | 0 → 0 | 0 / 0 | 0 | 0 | FULL |
| `/terms-of-use` | 450 | 600 | 469 | 458 | 0 → 0 | 0 / 0 | 0 | 0 | FULL |
| `/disclaimer` | 291 | 439 | 308 | 297 | 0 → 0 | 0 / 0 | 0 | 0 | FULL |
| `/resources/frozen-pipes-midvale` | 1633 | 1785 | 1654 | 1643 | 0 → 0 | 5 / 5 | 125 | 0 | FULL |
| `/resources/winterize-swamp-cooler-utah` | 1488 | 1633 | 1502 | 1491 | 0 → 0 | 5 / 5 | 93 | 0 | FULL |
| `/resources/upstairs-unit-leak-who-pays-utah` | 1490 | 1640 | 1509 | 1498 | 0 → 0 | 5 / 5 | 87 | 0 | FULL |
| `/resources/can-mold-grow-in-utah` | 1428 | 1578 | 1447 | 1436 | 0 → 0 | 5 / 5 | 106 | 0 | FULL |
| `/resources/basement-flooding-spring-snowmelt-utah` | 1446 | 1593 | 1462 | 1451 | 0 → 0 | 5 / 5 | 111 | 0 | FULL |

## Template blocks (repeated verbatim on ≥10 pages, excluded from “unique prose”)

- 31 pages, 6 words: “385 337 3560 request emergency help”
- 30 pages, 1 words: “home”
- 17 pages, 4 words: “general ranges for planning”

## Notes / limits

- Word counts count whitespace-separated tokens containing at least one alphanumeric character; phone numbers count as tokens (e.g. `(385) 337-3560` = 3 tokens). This matches the counting used for the Stage 5 baseline comparison.
- “Unique prose” is main visible words minus blocks whose normalised text is identical on ≥10 of the 31 pages (template chrome inside `<main>`). Doc prose does not repeat verbatim across 10 pages, so this isolates real content.
- Mobile pass (390×844, touch): main visible + hidden words measured the same way; mobile nav links are `display:none` until the menu opens (template chrome, 0 doc words) and the sticky call bar hides while the hero is on screen — both verified as template-only.
- Thinnest page is `/disclaimer` at 308 main visible words — FULL, but only 8 words above the THIN threshold (300); all 291 of its doc words are present and visible.
- Raw browser output: `/tmp/opt1-raw.json` (ephemeral). Machine-readable results: `qa/opt1-content.json`.
