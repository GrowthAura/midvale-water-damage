# Agent C — Design + Mobile + Header/Footer — Midvale UT 10x round
**Date:** 2026-11-16 · **Checker:** Agent C (design/mobile/header/footer)
**Method:** Real Playwright Chromium renders only — never code-only. No push, no deploy, no token, no site files edited. `lib/pages-data.json` untouched.
**Builds tested:** Pages build `http://127.0.0.1:8908/midvale-water-damage` (primary, full checks) and Cloudflare build `http://127.0.0.1:8909` (spot checks, homepage). Live `https://midvale-water-damage.pages.dev` spot-check **COULD NOT RUN** — Chromium in this VM fails the navigation with `net::ERR_TUNNEL_CONNECTION_FAILED` (VM egress/proxy failure, not a site result). No live verdict is claimed.
**Raw data:** `agent-C-results.json` (99 checks), `agent-C-followup.json`, `agent-C-sweep2.json`; scripts `check.py`, `probe.py`.
**Screenshots:** `shots/` in this folder.

## Verdict
**PASS with 1 × P3. P1 0 / P2 0 / P3 1.**
Header nav + dropdown, mobile menu, slim footer, Button-2-above-fold, overflow, sticky bar, lazy images and first-paint all verified by measurement on real renders. The single defect is an intermittent homepage-only console 404 from a Next.js RSC prefetch (known P3-1 class, no visible impact).

## 1. Header (desktop 1440, homepage, Pages build)
| Check | Verdict | Measured evidence |
|---|---|---|
| Nav shows Home / Services▾ / Areas / phone | PASS | `navLinks=[Home 48px, Areas 48px]`, drop button `Services ▾` 48px, header phone `(385) 337-3560` visible, `position: sticky`, top 0 |
| Phone = tel: link | PASS | `href=tel:+13853373560` |
| Tap targets ≥48px | PASS | Heights `[48, 48, 48, 51]` (Home, Areas, Services btn, phone) |
| Services click → dropdown, exactly 6 in order | PASS | `emergency-water-extraction, water-damage-repair, basement-flooding-cleanup, burst-pipe-water-damage, sewage-backup-cleanup, mold-remediation` (hrefs carry the `/midvale-water-damage` basePath prefix, as expected on this build). Dropdown item heights all 48px |
| Closes on Escape | PASS | `open=false` after Escape |
| Closes on outside click | PASS | `open=false` after click at (720,500) |
| Closes on navigation to a service | PASS | Clicked 2nd item → URL `…/water-damage-repair`, `open=false` |
| Areas link scrolls to #areas | PASS | Click → `location.hash=#areas`, `#areas` top lands at `−0.0px`, scrollY 8477. **Note:** `scroll-behavior: smooth` — the 8,477px traverse takes ~2–3 s; a 600 ms wait reads scrollY ≈ 40 and looks broken. Re-measured at 1.5 s / 3 s: landed. Not a defect, just slow on this very long homepage |
| Sticky header on scroll | PASS | After scroll to 1500px, header `top=0`, `position: sticky` |
| Hero H1 readable | PASS | Viewed screenshot: white 44px H1 on photo + dark shade `linear-gradient(rgba(5,22,20,0.84)…0.88)`, `color=rgb(255,255,255)`; intro + both buttons legible, no overlap |

Screenshot: `shots/desktop-header-home.png`, `shots/desktop-header-dropdown-open.png` (viewed — dropdown clean, 6 items, no clipping).

## 2. Mobile menu (390×844, homepage)
| Check | Verdict | Measured evidence |
|---|---|---|
| Hamburger visible, phone visible | PASS | Menu button visible, 48×48px (≥48). Note: at 390 the header wraps to two rows — brand row, then hamburger + phone centred on row 2 (flex-wrap). Looks acceptable in the screenshot; at 320 the phone hides and it is one row |
| Hamburger opens panel | PASS | `#main-nav.open`, `aria-expanded=true` |
| Services expands to indented 6-service list | PASS | 6 items, same order as desktop; indent measured `itemLeft=40px` vs top-level `24px` (16px, from `.nav-drop-list padding-left:16px`) |
| Areas present in menu | PASS | `href=/midvale-water-damage#areas` (basePath-prefixed, correct on this build) |
| Closes on Escape | PASS | `open=false` |
| Closes on link navigation | PASS | Areas tap → `open=false`, scrollY 18794, `hash=#areas` (mobile page is taller, hence larger scrollY) |
| Page scrolls normally, menu closed | PASS | scrollTo 1200 → scrollY 1200; 2400 → 2400 |
| Scroll behaviour, menu open (trap check) | PASS — no trap | Menu open: `body position:fixed, top:0, overflow:hidden`; wheel scroll → scrollY stays 0 (page locked behind menu, by design); tap inside menu does not close it; menu stays open. No runaway/unstuck state observed. Escape/toggle close restores scroll |
| First paint shows text, zero scroll | PASS | H1 visible, opacity 1, 34px; intro visible |
| Hero / buttons at 390 | PASS | Button 2 bottom 542px vs viewport 844px |

Screenshot: `shots/mobile-menu-home.png`, `shots/mobile-menu-services-expanded.png` (viewed — indented 6-item list, Areas below, clean).

## 3. Footer (slim, all pages checked)
| Check | Verdict | Measured evidence |
|---|---|---|
| 5 rows, counts 10 / 3 / 2 / 5 / 3 | PASS | Verified by DOM on homepage + all 5 deep pages, desktop 1440 AND mobile 390: `Services 10, Areas 3, Company 2, Resources 5, Legal 3` on every page rendered |
| Call button working tel: link, text not clipped | PASS | `href=tel:+13853373560`, text `Call (385) 337-3560`, `clientWidth=175 = scrollWidth=175` (desktop and 390) |
| No map iframe anywhere | PASS | `iframes=[]` on homepage + all 5 deep pages (desktop); footer contains 0 iframes |
| Footer height | PASS | Desktop **898px** (claimed 898px — exact), mobile 390 **1979px** (claimed 1979px — exact) |
| Dot separators render | PASS | CSS `.site-footer li + li::before { content: "·" }` (globals.css:376); computed: 1st `li` in each row `none`, every following `li` `"·"`. Viewed in both footer screenshots |
| No text overflow / clipped button | PASS | Footer phone `cw == sw`; no overflow on any footer page (see §4) |
| Legal pages still linked + noindex | PASS | Privacy Policy / Terms of Use / Disclaimer linked in Legal row on every page; `/privacy-policy` has `robots=noindex, follow` |

Screenshots: `shots/desktop-footer-home.png` (+ `shots/desktop-footer-home-viewport.png`), `shots/mobile-footer-home.png` (+ `shots/mobile-footer-home-viewport.png`) — viewed, rows + separators clean. Note: the element-crop footer shots show the sticky header painted over the top/middle of the footer — that is a screenshot-compositing artifact of element screenshots with a sticky header, not a page defect; the `-viewport` shots show the real scrolled state cleanly.

## 4. Mobile / sweeps (all 31 routes)
| Check | Verdict | Measured evidence |
|---|---|---|
| Overflow 0 @1440 / 390 / 320 | PASS | `documentElement.scrollWidth − clientWidth = 0` on **all 31 routes at all three widths** (sweep320 + sweep390, 62 rows; plus 6 deep pages at 1440 and 390) |
| Button 2 ("Request Emergency Help") above the fold @320 AND @390 | PASS | **31/31 above fold at both widths.** Worst @320 (viewport 700): `/condo-apartment-water-damage` bottom **552px** (148px margin). Worst @390 (viewport 844): `/condo-apartment-water-damage` and `/resources/basement-flooding-spring-snowmelt-utah` bottom **773px** (71px margin). Button 2 is `tel:+13853373560`, 48px tall @320, 56px @390 |
| Console errors | **P3 — see defect D-1** | 0 errors on all 31 routes in both sweeps and on all 5 deep pages (desktop + mobile). Homepage only: one intermittent 404 (see below) |
| Sticky mobile call bar, every page | PASS | At hero: hidden (`display:none`, `bar-hidden`) by design. After scrolling past hero: visible `display:block`, 63px tall at viewport bottom, `Call (385) 337-3560 · 24/7`, `href=tel:+13853373560` — verified on **all 31 routes at 390 and at 320** (sweep2, 62/62). Hidden on desktop (`display:none`) |
| Lazy images load, no blank boxes | PASS | Homepage desktop: 20 imgs, `blank=[]`, `zeroBox=[]` after full scroll-through. Homepage mobile 390: 20 imgs, same |
| No content hidden by reveal | PASS | First-paint H1 visible with `opacity: 1` on **all 31 routes at 390 and at 320** (sweep2, 62/62), zero scrolling |

Screenshot: `shots/worst-button2-320-condo.png` (viewed — H1 + both buttons above the fold at 320, no overflow, no clipping). `shots/mobile-home-320.png` also saved.

## 5. Cloudflare build (http://127.0.0.1:8909, spot check)
| Check | Verdict | Measured evidence |
|---|---|---|
| Desktop header + dropdown | PASS | Home/Areas 48px, Services▾ 48px, phone `tel:+13853373560`; dropdown 6 in order |
| Footer rows + height | PASS | `Services 10, Areas 3, Company 2, Resources 5, Legal 3`, height 898px |
| Overflow / Button 2 / console @1440 | PASS | Overflow 0, Button 2 bottom 559/900, console errors 0 |
| Mobile menu @390 | PASS | Overflow 0, Button 2 bottom 542/844, menu expands to the 6 services |

## Defects
### D-1 (P3) — Homepage-only intermittent console 404: Next.js RSC prefetch of `/midvale-water-damage.txt`
- **Page/width:** `/` (homepage), desktop 1440 and mobile 390, Pages build only. Not on any deep page, not on the Cloudflare build, not in the 31-route sweeps.
- **Exact evidence:** failed request `http://127.0.0.1:8908/midvale-water-damage.txt?_rsc=8kzk2 :: HTTP 404`, console `Failed to load resource: the server responded with a status of 404 (File not found)`. Observed in the main run on both desktop (D22) and mobile (M17); in a follow-up run it fired on desktop but not on mobile — timing-dependent (Next prefetches the home flight payload when a home link is prefetched; the file lives at `/midvale-water-damage/index.txt`, so the root-relative `/midvale-water-damage.txt` 404s). This is the known P3-1 prefetch class from the rebuild.
- **Impact:** console noise only; no visible defect, no broken link, no failed asset.
- **Suggested fix:** stop the home-link RSC prefetch from requesting the bare `.txt` (same class as the earlier P3-1 fix).

## Observations (not defects)
- **O-1:** Areas smooth-scroll takes ~2–3 s on desktop (8,477px traverse). Fine on a long page; do not "fix" by breaking smooth scroll.
- **O-2:** At 390 the header wraps to two rows (brand / hamburger+phone). Acceptable; at 320 it is one row with the phone hidden.
- **O-3:** Live Pages spot-check could not run in this VM (`ERR_TUNNEL_CONNECTION_FAILED` reaching `midvale-water-damage.pages.dev`). Needs a live-browser check by the parent; nothing here implies a live problem — both local builds pass.

## Corrections to my own first-pass FAILs (honesty note)
The raw run logged 8 FAILs; 6 were my script's comparison bugs, re-verified as passes with corrected measurements in `agent-C-followup.json`:
- D4 / M7 (dropdown "wrong order"): the hrefs were correct but carried the `/midvale-water-damage` basePath prefix my comparator did not strip. Corrected order confirmed.
- D9 (Areas "doesn't scroll"): my 600 ms wait was shorter than the ~2–3 s smooth scroll. Re-measured: lands at top −0.0px.
- D15 (separators): my check wrongly required a `·` on the first `li` of each row; correct behaviour is first-item `none`, rest `·` — confirmed in CSS + computed styles.
- M8 (Areas "missing"): href is `/midvale-water-damage#areas` — correct modulo basePath.
- The remaining 2 raw FAILs are D22/M17 (the real P3 above, same root cause) and L (live check could-not-run).
