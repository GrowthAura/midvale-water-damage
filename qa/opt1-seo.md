# CYCLE 1 OPT — Technical SEO Audit — Midvale UT (Batch 2)

**Date:** 2026-11-13 · **Verdict: READY — 0 blocking problems (P1 0 / P2 0 / P3 3 carried observations)**

**Method:** fresh export by coordinator (exit 0, `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`, no trailing slash), served on `/midvale-water-damage/` via `qa/linkfix-serve.py` on port 8325. Data `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` verified unchanged before, during and after. Audit-only: no site source file modified, no push/deploy/token/DNS. Evidence: `qa/opt1-static.json`, `qa/opt1-links.json`, `qa/opt1-perf.json` (+ the three `opt1-*.py` scripts). Perf numbers are LAB numbers (local loopback, unthrottled, cold cache, fresh context per load) — never field data. Schema depth is the schema worker's job; this audit covers schema presence + parse only.

## PROBLEMS

### P1 — 0

### P2 — 0

### P3 — 3 (all carried observations, none blocking)

**P3-1 — anchor-word-count** (sitewide (12 pages))
- 12 body-copy anchors exceed the 5-word anchor cap, all verbatim doc wording (accepted tension, carried from audits 1+2): 9x 'Water Heater & Appliance Leak Cleanup' (6w) on /basement-flooding-cleanup, /condo-apartment-water-damage, /crawl-space-water-damage, /emergency-water-extraction, /hardwood-floor-cabinet-drying, /water-leak-detection, /locations/south-salt-lake-ut, /about, /resources/upstairs-unit-leak-who-pays-utah; 2x 'Midvale Water & Sewer Emergency Contacts' (6w) on /contact, /resources/basement-flooding-spring-snowmelt-utah; 1x 8w 'the Midvale Water & Sewer Emergency Contacts page' on /. Both 6w anchors are verbatim substrings of the target pages' doc H1s (verified fresh this round). Shortening them would break the verbatim rule; no fix without his word.

**P3-2 — breadcrumb-double-link** (/locations/* (3 pages))
- Homepage linked twice inside <main> on all 3 location pages (carried from audits 1+2, observation only): 'Home' -> /midvale-water-damage and 'Nearby Cities We Serve' -> /midvale-water-damage#areas. Verified fresh: BOTH links sit inside <nav aria-label="Breadcrumb"> on all 3 pages. Breadcrumb nav, not body copy; body-copy duplicate targets 0 sitewide.

**P3-3 — breadcrumb-single-item-home** (/)
- Homepage carries a one-item BreadcrumbList (Home only), verified fresh by re-parse, with no visible breadcrumb navigation. Invisible markup, harmless; no second truthful item exists. Carried from audits 1+2.

## FIXED SINCE AUDIT 2 (all 3 audit-2 P3s closed, verified fresh)

- **P3-1 404.html duplicate noindex — FIXED:** out/404.html now carries exactly 1 <meta name="robots" content="noindex"/> (verified by grep + served 404 status); the duplicate tag is gone.

- **P3-2 cottonwood card alt wrong — FIXED:** Alt rewritten to 'Winding canyon highway with cars through steep rocky autumn slopes in Cottonwood Canyon, Utah'. I viewed images/cards/cottonwood-heights-ut.webp full-size this round: it IS a winding canyon highway with cars through steep rocky autumn slopes — alt now matches the photo exactly.

- **P3-3 snowmelt hero alt wrong — FIXED:** Alt rewritten to 'Spring snowmelt water pooling at a home foundation as a downspout discharges, with melting snow piles and snowy hills behind'. I viewed images/heroes/basement-flooding-spring-snowmelt-utah.webp full-size this round: it IS an exterior downspout discharging meltwater at a home foundation with snow piles and snowy hills behind — alt now matches the photo exactly.

## PASSES (all measured fresh)

- **Crawlability:** robots.txt HTTP 200, exact content `User-agent: * / Allow: / / Sitemap: https://growthaura.github.io/midvale-water-damage/sitemap.xml` (Allow present, no Host: line, served == file); sitemap exactly 31 locs, date-only lastmod `2026-11-12`, 0 duplicates, all 31 curl 200 via served subpath, homepage root `/` only, others no-slash, set == expected 31 canonical URLs; llms.txt lists all 31 routes on the Pages URL, HTTP 200.
- **Indexability:** meta robots exactly 1 `index, follow` on 31/31; canonical self-referential 31/31; og:url matches canonical 31/31; 404.html serves 404 with exactly 1 noindex tag and no canonical; 0 localhost occurrences and 0 double-slash absolute URLs anywhere in out/ HTML/XML/TXT (audit 2's single polyfill-chunk `localhost` string is gone in this fresh export); 120 distinct local resource refs checked, 0 non-200; 0 malformed `tel:` links (checked after the Tulsa GSC `tel+19183470890` root-cause note).
- **Meta:** title + description verbatim vs `pages-data.json` character-for-character on 31/31; 0 duplicate titles, 0 duplicate descriptions, 0 duplicate canonicals; title lengths 10–73ch, descriptions 47–138ch.
- **Headings:** exactly 1 H1 per page on 31/31, text matches the doc H1 every time; 0 skipped heading levels; H2 sequence matches doc blocks 406/406, H3 259/259; no H4+; viewport meta present 31/31.
- **Links:** 1,063 internal anchors checked on the served site, 0 broken, 0 external; body + card reconciles exactly: 143 body + 19 card = 162; 33 in-main breadcrumb links classified separately; orphans 0 (inbound min 5, max 30); body self-links 0; body duplicate targets 0.
- **Images/alt:** 107 webp on disk, 107 `<img>` tags, 0 missing/empty alt, 0 non-200 src, 0 missing width+height; total weight 11,243,230 B; all 8 q75 re-encodes match their fix-1 claimed sizes.
- **Schema (presence only):** 178 JSON-LD blocks across 31 pages (was 80 in audit 2 — schema best-ever work landed), 0 parse failures; per-page 3–8 blocks.
- **Mobile (93 in-browser loads):** horizontal overflow 0 at 320, 390 and 1440 on 31/31; body font 19px on all 31 routes × 3 viewports; `p.intro` 19px everywhere (eyebrow 14px @320 / 18px @390/1440 is chrome, not body copy); Button 2 visible at scroll-0 on 31/31 @320 (worst bottom 556.2px vs 568 fold — condo) AND @390 (worst 768.2px vs 844 — snowmelt resource); footer links min 48px; menu button 48×48 @320/390; nav links 58.6px menu-open @320/390, 48px @1440; header phone 48px @390, 50.6px @1440 (hidden ≤360px by design).
- **Performance (lab, see note below):** FCP medians 1568ms @320 / 1416ms @390 / 1984ms @1440; LCP medians 1624ms @320 / 1756ms @390 / 2204ms @1440 (max 3196 / 3108 / 3696ms); CLS median 0 at all viewports (max 0); 0 console errors across all 93 loads; 0 failed non-maps requests (Maps embed failures are sandbox-blocked google.com egress — environmental); LCP element `IMG.hero-img` on 93/93 loads.
- **Maps:** 29 iframes total (28 pages + 404.html), all `loading="lazy"`; embed itself does not load in this sandbox — environmental, needs a real-network eyeball after push.

## OBSERVATIONS (not problems)

- Titles 10-73ch, 25/31 over 60ch — all verbatim from the doc; Google truncates display but verbatim wins. No change without his word.
- Descriptions 47-138ch, 26/31 under 120ch — all verbatim from the doc.
- Legal titles short (Disclaimer 10ch / Terms of Use 12ch / Privacy Policy 14ch) — verbatim from the doc; carried accepted tension from audit 1.
- Image weight 11,243,230 B vs audit-2 11,331,800 B (-88,570 B, -0.8%). Top-10 files byte-identical to audit 2 and all 8 q75 re-encodes match their claimed sizes; out/ total == public/ total, so the export is faithful. Which sub-top-10 file(s) account for the delta is not established from available records (no per-file audit-2 manifest beyond top 10) — lighter is the direction the standing image-weight order wants; not a defect.
- Maps embeds do not load in this sandbox (google.com egress blocked) — environmental, needs a real-network eyeball after push. All 29 iframes carry loading=lazy (28 on pages + 1 on 404.html).
- Live mobile-width render in a real browser is still unconfirmed (sandbox Chromium cannot reach public internet); mobile verified on the byte-identical local export. His phone check remains the final confirmation.
- LCP/CLS are lab numbers only (see performance_lab_only.lcp_vs_audit2). No field data exists for this site.

**LCP lab note — read before comparing with audit 2:** LCP medians rose vs audit 2 (320: 672→1624ms, 390: 776→1756ms, 1440: 824→2204ms) AND FCP rose by the same factor (320: 612→1568ms), with CLS still 0 and the LCP element unchanged (`IMG.hero-img` 93/93). Hero files are byte-identical to audit 2 (top-10 image sizes identical) and total image weight is LOWER. Uniform FCP+LCP inflation with no site-side weight change is consistent with shared-cell CPU contention while parallel Batch 2 workers run — NOT evidence of a site regression. Lab only; re-measure on a quiet cell / real hosting before treating any LCP number as a regression.

## PER-PAGE TABLE

| Route | T | D | H1 | H2 | H3 | Canon | JSON-LD | Body/Card | Broken | Alt-miss | Ovf 320/390 | LCP 320/390/1440 | CLS max | B2 320/390 | Problems |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `/` | 72✓ | 138✓ | 1✓ | 12/12 | 24/24 | ✓ | 7 | 1/19 | 0 | 0 | 0/0 | 1812/2492/2580 | 0 | ✓/✓ | P3: breadcrumb-double-link; P3: breadcrumb-single-item-home |
| `/about` | 52✓ | 110✓ | 1✓ | 9/9 | 5/5 | ✓ | 5 | 16/0 | 0 | 0 | 0/0 | 1968/2692/3088 | 0 | ✓/✓ | — |
| `/contact` | 53✓ | 104✓ | 1✓ | 8/8 | 5/5 | ✓ | 4 | 1/0 | 0 | 0 | 0/0 | 1232/3108/1812 | 0 | ✓/✓ | — |
| `/emergency-water-extraction` | 69✓ | 116✓ | 1✓ | 12/12 | 11/11 | ✓ | 6 | 7/0 | 0 | 0 | 0/0 | 2296/2836/3180 | 0 | ✓/✓ | — |
| `/basement-flooding-cleanup` | 66✓ | 120✓ | 1✓ | 12/12 | 13/13 | ✓ | 6 | 5/0 | 0 | 0 | 0/0 | 1496/1416/2700 | 0 | ✓/✓ | — |
| `/window-well-flooding` | 61✓ | 108✓ | 1✓ | 12/12 | 15/15 | ✓ | 6 | 2/0 | 0 | 0 | 0/0 | 1420/1824/2204 | 0 | ✓/✓ | — |
| `/burst-pipe-water-damage` | 66✓ | 115✓ | 1✓ | 14/14 | 5/5 | ✓ | 6 | 5/0 | 0 | 0 | 0/0 | 3196/3096/2708 | 0 | ✓/✓ | — |
| `/sewage-backup-cleanup` | 64✓ | 109✓ | 1✓ | 14/14 | 9/9 | ✓ | 7 | 3/0 | 0 | 0 | 0/0 | 2488/1796/2024 | 0 | ✓/✓ | — |
| `/water-heater-leak-cleanup` | 68✓ | 112✓ | 1✓ | 13/13 | 11/11 | ✓ | 7 | 7/0 | 0 | 0 | 0/0 | 2800/1924/1984 | 0 | ✓/✓ | — |
| `/swamp-cooler-leak-water-damage` | 64✓ | 112✓ | 1✓ | 15/15 | 5/5 | ✓ | 6 | 2/0 | 0 | 0 | 0/0 | 1604/2592/1880 | 0 | ✓/✓ | — |
| `/ceiling-water-damage` | 63✓ | 106✓ | 1✓ | 12/12 | 15/15 | ✓ | 7 | 6/0 | 0 | 0 | 0/0 | 2568/2600/2296 | 0 | ✓/✓ | — |
| `/crawl-space-water-damage` | 64✓ | 112✓ | 1✓ | 14/14 | 10/10 | ✓ | 6 | 3/0 | 0 | 0 | 0/0 | 1808/2312/2712 | 0 | ✓/✓ | — |
| `/hardwood-floor-cabinet-drying` | 63✓ | 115✓ | 1✓ | 15/15 | 5/5 | ✓ | 7 | 4/0 | 0 | 0 | 0/0 | 1892/2200/1540 | 0 | ✓/✓ | — |
| `/condo-apartment-water-damage` | 62✓ | 117✓ | 1✓ | 15/15 | 5/5 | ✓ | 7 | 4/0 | 0 | 0 | 0/0 | 1488/1200/1620 | 0 | ✓/✓ | — |
| `/commercial-water-damage` | 71✓ | 109✓ | 1✓ | 16/16 | 10/10 | ✓ | 7 | 4/0 | 0 | 0 | 0/0 | 2816/1320/2096 | 0 | ✓/✓ | — |
| `/storm-flood-damage` | 61✓ | 113✓ | 1✓ | 14/14 | 15/15 | ✓ | 6 | 5/0 | 0 | 0 | 0/0 | 1624/1628/1792 | 0 | ✓/✓ | — |
| `/mold-remediation` | 57✓ | 113✓ | 1✓ | 16/16 | 11/11 | ✓ | 6 | 7/0 | 0 | 0 | 0/0 | 1612/1096/1392 | 0 | ✓/✓ | — |
| `/water-leak-detection` | 63✓ | 106✓ | 1✓ | 16/16 | 9/9 | ✓ | 8 | 6/0 | 0 | 0 | 0/0 | 1392/1388/2000 | 0 | ✓/✓ | — |
| `/water-damage-repair` | 69✓ | 110✓ | 1✓ | 15/15 | 5/5 | ✓ | 6 | 6/0 | 0 | 0 | 0/0 | 1284/1396/2864 | 0 | ✓/✓ | — |
| `/locations/cottonwood-heights-ut` | 68✓ | 114✓ | 1✓ | 13/13 | 14/14 | ✓ | 6 | 8/0 | 0 | 0 | 0/0 | 1592/1300/2500 | 0 | ✓/✓ | — |
| `/locations/south-salt-lake-ut` | 71✓ | 106✓ | 1✓ | 14/14 | 14/14 | ✓ | 5 | 13/0 | 0 | 0 | 0/0 | 2104/1440/2220 | 0 | ✓/✓ | — |
| `/locations/magna-ut` | 64✓ | 112✓ | 1✓ | 15/15 | 10/10 | ✓ | 6 | 9/0 | 0 | 0 | 0/0 | 1588/884/1204 | 0 | ✓/✓ | — |
| `/midvale-water-sewer-emergency-contacts` | 73✓ | 125✓ | 1✓ | 11/11 | 5/5 | ✓ | 6 | 3/0 | 0 | 0 | 0/0 | 1684/1876/2212 | 0 | ✓/✓ | — |
| `/privacy-policy` | 14✓ | 91✓ | 1✓ | 11/11 | 0/0 | ✓ | 3 | 0/0 | 0 | 0 | 0/0 | 796/1208/1708 | 0 | ✓/✓ | — |
| `/terms-of-use` | 12✓ | 47✓ | 1✓ | 12/12 | 0/0 | ✓ | 3 | 0/0 | 0 | 0 | 0/0 | 1132/1016/1036 | 0 | ✓/✓ | — |
| `/disclaimer` | 10✓ | 86✓ | 1✓ | 9/9 | 0/0 | ✓ | 3 | 0/0 | 0 | 0 | 0/0 | 680/1172/912 | 0 | ✓/✓ | — |
| `/resources/frozen-pipes-midvale` | 69✓ | 122✓ | 1✓ | 14/14 | 5/5 | ✓ | 6 | 3/0 | 0 | 0 | 0/0 | 1504/1988/2516 | 0 | ✓/✓ | — |
| `/resources/winterize-swamp-cooler-utah` | 65✓ | 127✓ | 1✓ | 13/13 | 5/5 | ✓ | 5 | 3/0 | 0 | 0 | 0/0 | 2012/2280/3696 | 0 | ✓/✓ | — |
| `/resources/upstairs-unit-leak-who-pays-utah` | 70✓ | 116✓ | 1✓ | 12/12 | 8/8 | ✓ | 6 | 2/0 | 0 | 0 | 0/0 | 1396/1212/2420 | 0 | ✓/✓ | — |
| `/resources/can-mold-grow-in-utah` | 64✓ | 113✓ | 1✓ | 14/14 | 5/5 | ✓ | 5 | 4/0 | 0 | 0 | 0/0 | 2008/1436/3116 | 0 | ✓/✓ | — |
| `/resources/basement-flooding-spring-snowmelt-utah` | 71✓ | 112✓ | 1✓ | 14/14 | 5/5 | ✓ | 4 | 4/0 | 0 | 0 | 0/0 | 2936/1756/2108 | 0 | ✓/✓ | — |

T/D = title/description length in chars (✓ = verbatim vs `pages-data.json`). LCP in ms, lab numbers only. B2 = Button 2 visible at scroll-0.
