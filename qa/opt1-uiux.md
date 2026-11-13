# FINDINGS — Midvale UT Cycle 1 (Batch 2) UI/UX Audit A-to-Z

**Auditor:** Cycle 1 UI/UX auditor (audit-only; no source file modified).
**When:** 2026-11-13 ~18:45–19:45 PKT.
**Method:** fresh export already run by parent (exit 0, `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`, no trailing slash); served from existing `out/` on `/midvale-water-damage/` via `qa/linkfix-serve.py` port 8351. Real Chromium (Playwright), 31 routes × 3 viewports (1440×900, 390×844, 320×568). Slow-scroll lazy-image load, full-page screenshots desktop + mobile 390 for all 31 routes (62 files in `qa/opt1-uiux/`).
**Raw data:** `qa/opt1-uiux.json` (per-route measurements), `qa/opt1-adjudicate.json` (re-probes), scripts `qa/opt1-uiux.py`, `qa/opt1-adjudicate.py`, `qa/opt1-shots.py`.

## VERDICT: PROBLEMS 4 — P1 0 · P2 1 · P3 3 — NOT READY (one real P2)

The site is in strong shape: overflow 0, console 0, contrast AA pass, buttons equal + in-fold everywhere, images 0 broken, form exact. The one real defect is visible on the homepage's main conversion element (all 19 cards repeat their title in plain text). The three P3s are minor sub-48px tap targets that all pass the WCAG 24px minimum.

Raw run flagged 267 items; every category except the 4 below was re-probed with a corrected method and cleared as a verifier-script artifact (see "Adjudication — cleared flags"). Nothing was waived on trust.

## PROBLEMS

### P2-1 — Homepage cards repeat the title as plain text at the end of every card description
- **Routes:** `/` only (16 service cards + 3 location cards, 19/19).
- **What:** each card's description `<p>` renders `{summary} {anchor}` (`app/page.tsx` ~L147) and `{lead} {rest} {anchor}` (~L347), so the card ends with its own title/city phrase in plain body text — e.g. "...have the best chance of being saved. **Emergency Water Extraction**", "...below the canyons. **Water Damage Restoration Cottonwood Heights**".
- **Evidence:** `qa/opt1-uiux/home-desktop-full.png`, `crop-home-d-cards.png` (rows 1–2), `crop-home-d-faq.png` (location cards).
- **Context:** the LINKFIX 2026-11-13 comment in `app/page.tsx` says the anchor phrase is deliberate link text (the card is one link unit; the doc's anchor phrase is the link text). Visually it reads as duplicated copy — a reader sees the title twice. Fix is a design call: style the anchor as a distinct affordance (e.g. "Learn more →") or drop the echo from the rendered paragraph. This was not flagged in the Stage 1 UI/UX round (PROBLEMS 0), so it is either accepted-by-design or missed there — flagging it here because a user reads it as a copy error.

### P3-1 — Header brand logo link 43px tall (31/31 routes, all viewports)
- `a.brand` measures 288×43 @1440 and 342×43 @390 — 5px under the 48px tap-target bar. Passes WCAG 2.2 AA 24px minimum; 288–342px wide, easily tappable. Cosmetic.
- Evidence: `crop-home-d-hero.png`, `crop-home-m-hero.png`.

### P3-2 — Contact-form radio option labels 32px tall (`/contact`)
- Labels "Yes" 57×32, "No" 53×32, "Not sure" 104×32; the native 13px radio sits inside a 32px label. Passes WCAG 24px minimum. Cosmetic.
- Evidence: `crop-contact-d-form.png`.

### P3-3 — Breadcrumb links 24px tall (30/31 routes, all but `/`)
- Breadcrumb "Home" + current-page links render 24px tall (e.g. 51×24). Inline text navigation; meets WCAG 2.2 AA 24px minimum exactly. Cosmetic.
- Evidence: `crop-emerg-d-hero.png`.

## 1. Render — all 31 routes × 1440 / 390 / 320

- **H1** visible on 31/31 at all widths; min 30px @320 (≥ H2 28px). **Overflow 0** on 31/31 at all widths. **Console errors 0. Failed requests 0 local, 0 Maps** (no Maps request observed; sandbox cannot reach google.com — known environment limit).
- **Hero buttons exactly equal** on 31/31 at all widths. **Button 2 ("Request Emergency Help") visible at scroll-0 on 31/31 @320 AND 31/31 @390.** Worst bottom @320: **556px** (`/condo-apartment-water-damage`, 12px headroom vs 568px fold); worst @390: **768px** (`/condo-apartment-water-damage` + `/resources/basement-flooding-spring-snowmelt-utah`, 76px headroom vs 844px fold).
- **Images: brokenImgs 0.** All 36 distinct "broken" flags from the raw run were lazy-load timing (see adjudication); re-probe with 200ms/step scroll + 1.5s settle + per-image load wait: 0 bad across 176 images. All files exist on disk; 0 missing alt; 0 zero-display renders.
- **Body text 19px:** all real body `p`/`li` = 19px on every route/viewport. The only sub-19px text is the intentional 18px `.eyebrow` kicker and 18px breadcrumb items (nav chrome, not body copy).
- **Contrast: 0 WCAG AA failures** on any route/viewport. Worst measured ratio **5.65:1** (copper-dark phone text). No text sits over a background image (hero text is over a dark overlay, measured clean).
- **Tables @390:** scroll cue opacity 1 at scroll-0 on overflowing tables, 0 at max scroll, 0 on fitting tables (after corrected re-probe; see adjudication).
- **Homepage card grid @1440:** 16 cards, 4 cols, rows 4/4/4/4, card width 247px uniform, image height 138px uniform. No orphan row.
- **Contact form:** 6 doc fields, exact — Name, Phone number, Address or ZIP code, What happened (short description), Is the water still running? (Yes/No/Not sure), Best time to call — matching the doc's "Request Form Fields" list verbatim (`lib/pages-data.json`, `/contact`). Submit **"[Send My Request]" verbatim**. Form note ("does not send on this preview site") is the expected static-export notice.
- **Mobile menu @390:** opens (nav display flex), body `overflow: hidden`, scroll locked, menu link navigates to homepage correctly.
- **Sticky tel bar @390:** "Call (385) 337-3560 · 24/7" is `position: fixed`, bottom, 63px tall, visible once the hero scrolls out of view (IntersectionObserver toggles `.bar-hidden`). Works as designed.
- **Real clicks:** service card → emergency page; body link → hardwood page; logo → home; footer About → about; mobile menu link → home. All kept the `/midvale-water-damage/` subpath.

## 2. Per-section review (visual, from full-page screenshots)

- **Hero (all routes):** clean. H1 + intro + both buttons + trust chips all above the fold at desktop and mobile. Hero photo dark with readable overlay text. Desktop trust bar wraps to 2 lines ("Insurance-Ready Photo Logs" on line 2) — cosmetic. Mobile header stacks to 2 rows (brand line, then menu button + phone) — acceptable. Evidence: `crop-home-d-hero.png`, `crop-home-m-hero.png`, `crop-emerg-d-hero.png`.
- **Trust bar:** present on homepage + service pages (65px), chips readable, good contrast.
- **Intro / body sections:** 19px body copy, comfortable line length, no cramped or orphaned text seen in sampled sections. Service pages carry the content in one long `page-body` block (e.g. 8,237px @1440 on emergency) — reads fine, headings break it up.
- **Service cards (homepage):** 4-col grid, uniform images, aligned rows — except P2-1 (title echo at the end of every card description). Location cards have the same echo (P2-1). Evidence: `crop-home-d-cards.png`, `crop-home-d-faq.png`.
- **Process steps:** present on homepage ("How Our Water Mitigation Midvale 84047 Process Works", 862px @1440) and service pages; no layout defect measured (section heights normal, no overflow).
- **FAQ:** open (not accordions), all items visible — 6 on homepage, 5–6 per page. Clean cards, no truncation. Evidence: `crop-home-d-faq.png`.
- **Final CTA:** clean, both buttons equal, centered. Evidence: `crop-home-d-cta-footer.png`, `crop-home-m-cta-footer.png`.
- **Footer:** 5-column grid @1440, single column @390, all links ≥48px (min-height fix holds at both widths). Map iframe sits above the grid (see OBS-1).

## 3. Observations (not problems)

- **OBS-1 — Footer map blank in sandbox:** the footer opens with a 320px Google Maps iframe that cannot load here (no route to google.com), so full-page captures show a blank dark band above the footer grid (measured: 440px from final-CTA button bottom to first footer heading = 64px CTA padding + 320px map + 56px footer-grid padding). Known limitation, NOT a defect — the map loads on real browsers. His phone check is the remaining confirmation.
- **OBS-2 — Button 2 headroom is thinnest on `/condo-apartment-water-damage`** (556px @320, 12px headroom). Holds, but any hero growth on that route would push Button 2 below the 320px fold.
- **OBS-3 — Card row heights vary by row** (526/558/588/618px) with content length; cards within a row stretch uniform (verified in screenshots).
- **OBS-4 — Environment:** Chromium headless shell segfaulted once mid-run (signal 11); the local server on port 8351 died twice and was restarted; one desktop screenshot needed a retry (page crash under memory pressure). All measurements re-run clean via resume-from-partial; no data lost. Screenshots: 62/62 full-page (desktop + m390) present in `qa/opt1-uiux/`.

## Adjudication — cleared raw flags (267 raw → 4 final)

| Raw flag | Count | Why cleared |
|---|---|---|
| Broken images in rendered DOM | ~50 | All 36 distinct srcs exist on disk, no srcset, `loading="lazy"`. Re-probe (200ms/step scroll + 1.5s settle + per-image load wait): 0 bad, 176 imgs checked. Raw run scrolled too fast (50ms steps + 400ms wait). |
| Body text < 19px | ~93 | Only 18px `.eyebrow` kickers (intentional) + 18px breadcrumb LIs (nav chrome). Corrected selector (`.eyebrow` excluded): 0 body-copy violations. |
| Table scroll cue still ON at max scroll | ~20 | Synchronous read before the scroll listener fired. Re-probe with real `scrollTo` + 400ms wait: cue 0 at max scroll on all overflowing tables. |
| Contact form field count != 6 | 1 | Form has 8 inputs = 6 doc fields (radio group counts once). Doc spec verified exact; submit verbatim. |
| Tap targets < 48px (footer/menu/tel bar) | — | Footer links 0 <48px at desktop AND mobile; menu button 48×48; sticky tel bar 63px. Only brand (P3-1), radio labels (P3-2), breadcrumbs (P3-3) remain, all ≥24px WCAG minimum. |

## Files

- `qa/opt1-uiux.json` — per-route measurements + adjudicated problems + observations
- `qa/opt1-adjudicate.json` — re-probe results (images / tables / fonts / taps / tel bar)
- `qa/opt1-uiux.py`, `qa/opt1-adjudicate.py`, `qa/opt1-shots.py` — audit scripts
- `qa/opt1-uiux/` — 62 full-page screenshots (`<slug>-desktop-full.png`, `<slug>-m390-full.png`) + 11 section crops (`crop-*.png`)
