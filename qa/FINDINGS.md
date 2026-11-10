# Midvale UT — Findings Log (local build, Next.js 14 static export)

Build dir: `~/workspace/midvale-water-damage/` — `npm run export` exit 0.
Source: Google Doc "Midvale UT" 1ZmyWIOGUbUoaM-LRuffoWeO9xmojFAQLLaJDlYhRaDQ.
Frozen copy: `frozen-doc.txt` (116 lines, 2,164 words by this count — includes
labels/table cells; gate is word-diff = 0, not the total).
Theme: locked Upgraded Next.js Theme v2 — Tulsa EMD skeleton + Edmond order,
proven 53/53 with 0 problems on Tulsa Water Damage Repair (2026-11-08).
ONLY design carried over; all code written fresh for Midvale.

## Final numbers (Round 2, fresh re-run on the final build)
- Routes: 21/21 return 200 (homepage `/` + 16 services + 1 guide + 3 locations).
  Flat `.html` per route in `out/` (no post-export step needed).
- H1: 1 per page, visible, verbatim on 21/21. H2 home 12/12, H3 home 24/24.
- FAQ: 6/6 visible, FAQPage schema exactly matches visible Q&A.
- Service cards 16/16, area cards 3/3, category table 3 rows, cost ranges 5/5.
- Word-diff vs frozen doc: 143 items checked, 0 missing.
- Links: 21 unique internal hrefs, 0 missing files, 0 broken, 0 orphans,
  0 self-links in main body copy. (The condo target is linked twice on the
  homepage — service card + insurance paragraph — both are DOC links; cards
  are exempt from the one-link rule per the checklist.)
- Canonical: 21/21 self-referencing, exact sitemap form (homepage keeps `/`).
  Sitemap: 21 locs, date-only lastmod 2026-11-10, no image entries.
  Robots: Allow:/, NO Host: line.
- Buttons: Button 1 "(385) 337-3560" only; Button 2 "Request Emergency Help";
  both measured exactly equal — 322 x 56 px desktop, full-width equal mobile.
- tel: links: 100% `tel:+13853373560` on every page.
- Overflow: 0 px at 1440 / 390 / 320 on 21/21 routes.
- Body text: computed 18px on 21/21; CSS has no font-size below 18px.
- Dashes: 0 em/en dashes in built HTML. Fragments: 0 ("See and", "See .", etc.).
- JSON-LD: 4 blocks on home (LocalBusiness + FAQPage + WebSite + BreadcrumbList),
  Service + BreadcrumbList on linked pages; parsed, 0 errors; values from doc only.
- Footer map: present on 18/18 non-area pages, absent on 3/3 area pages.
- Sticky mobile call bar + header phone visible at 390px on 21/21.
- Perf (mobile 390, measured): home FCP 268ms, DCL 252ms, load 298ms, CLS 0,
  437,711 bytes total. Service page FCP 140ms, CLS 0, 410,561 bytes.
  Homepage 438KB < 800KB budget. LCP: this headless Chromium shell emits ZERO
  largest-contentful-paint entries (verified directly); the hero's largest
  content is the H1 text, which paints at FCP, so FCP is the honest proxy.
- Images: 0 raster image files on the site. Hero + 16 service cards + 3 area
  cards use fresh inline SVG/CSS branded panels (Wasatch ridge + glyph).
  No photo from any past site, no stock/AI photo, no AI word, no AI metadata
  to strip (nothing to strip). No image is claimed to be a real job photo.
  GAP NAMED: if real Midvale job photos arrive, panels can be swapped per slot.
- Favicon: fresh-drawn classic drop SVG (pine tile + copper drop), verified
  legible at 16px; matches the header mark.
- Contamination sweeps (20 terms x source + out/): 0. No Tulsa/918/Plano/
  Pleasant Grove/Chesterfield/old-phone/old-domain traces in shipped code or
  output. (Working notes PROGRESS.md + the parent checklist name the locked
  theme source as required by checklist item 5; that is documentation, not
  shipped site content.)
- No-JS fetch: H1, FAQ Q1/Q6, category table, cost line, meta title all
  present in static HTML.
- Guarantee/ranking-promise wording in output: 0.

## Defects found in QA — all fixed, root cause stated, phase re-run
1. ROUND 1 (63 fails, 3 root causes):
   a. Buttons unequal WIDTH (20 pages): 192.6px vs 296px — same height, widths
      followed text length. Root cause: inline-flex with no width rule.
      Fix: `.hero-buttons .btn { flex: 1 1 0 }` — both now exactly 322x56.
   b. Mobile overflow +101px @390 / +171px @320 (21 pages): header phone
      `right=491` — header-inner never wrapped. Fix: wrap + brand full-width
      row at <=600px. Re-probed: 0 at all widths.
   c. Homepage canonical `http://localhost:3000` vs sitemap `.../`: Next's
      Metadata API strips the trailing slash. Fix: explicit single
      `<link rel="canonical" href=".../">` on the homepage (count verified 1).
2. First export failed (my script error, owned): imported a plain function
   (`servicePanel`) from a "use client" file into Server Components — Next
   returns undefined. Fix: moved panels to server-safe `components/panels.tsx`.
3. EXTRAS round 1 (4 fails):
   a. Trust-band separators: doc line uses " · " between chips; first render
      dropped the separators (list items). Fix: trust band renders the exact
      verbatim line.
   b. "Tulsa" in `app/globals.css` comment — removed (contamination sweep).
   c. Em dashes in built HTML — from panel aria-labels, map title, footer
      line and sticky bar (" — "). All replaced with "," / " · " / ":". Now 0.
   d. LCP None — headless-shell limitation (see Perf above); FCP proxy used.
   (2 of the 3 word-diff "misses" were script artefacts: link annotations
   mid-sentence and a space before "." from text-node joins; script fixed.)
4. VISUAL review (viewed pixels):
   a. Button 2 invisible on the pine hero — pine button on pine background.
      Fix: Button 2 is now white bg + pine text + pine border (visible on
      dark hero AND white inner pages), same 322x56 size.
   b. Header wrapped to 3 lines at desktop (nav too wide for 1120 wrap).
      Fix: header wrap 1240px, nav cut to Home + 2 best services (footer
      still carries 8, homepage all 16). Verified one line.
   c. Final CTA + all section headings BLANK in full-page captures — the
      Reveal component hid content (opacity 0) until scroll + JS; with JS off
      it stayed invisible forever. Fix: Reveal is now a plain wrapper, no
      hiding ever. Card hover keeps Tier-1 motion. Verified visible.
   d. Hero art panel too tall/empty (16:9 at 880px). Fix: 21/9 on hero only.
   e. Mobile hero buttons below the fold (long intro first). Fix: at <=600px
      the hero is a flex column with buttons ordered directly under the H1
      (DOM order unchanged). Verified in mobile screenshot.
   f. Footer map blank in full-page captures — iframe was `loading="lazy"`
      and captures never scroll. Fix: eager loading. The map request now
      fires; it FAILS in this sandbox (google.com unreachable from the VM),
      so the map area is blank HERE but will render in a real browser.
      The embed URL is the standard Google Maps embed for Midvale, UT 84047.

## Open items (need Noorullah's call — nothing silently decided)
1. DOMAIN: doc gives URL "/" only. Canonical/og/sitemap currently use the
   local-only placeholder `http://localhost:3000` (env `NEXT_PUBLIC_SITE_URL`
   overrides). Replace + regenerate before ANY publish.
2. Meta title is 72 chars (>60) — verbatim from the doc, NOT rewritten.
   His wording call if he wants it shorter. Description 138 chars (OK).
3. About / Contact / Privacy pages: NOT built — no content in the doc.
4. Guide page: only the one verbatim sentence + a labelled note that the
   contact list arrives with its own doc. No numbers invented.
5. Service/location pages: summary pages only (verbatim homepage summary).
   Full pages await their own docs.
6. No form backend: CTAs are tel: links only (no form in the doc).
7. No push / deploy / domain / DNS / Vercel / GitHub touched. No token used.
8. Google Maps embed renders in a real browser; it is blocked in this sandbox.
9. LCP is reported via the FCP proxy (headless-shell limitation, see Perf).

## Files
- Build: `~/workspace/midvale-water-damage/` (app/, lib/, components/,
  public/, `out/`, `frozen-doc.txt`, `PROGRESS.md`, `qa/`)
- QA Round 1: `qa/round1/findings.json` (re-run after fixes: 0 fails)
- QA Round 2: `qa/round2/findings.json` + `qa/round2/findings-extra.json`
  (final build: 0 + 0 fails) + 42 screenshots (21 desktop-full + 21 mobile-top)
- QA scripts: `qa/round1-check.py`, `qa/round2-check.py`, `qa/round2-extra.py`
- Screenshot PDF: `~/workspace/your_files/midvale-screenshots-review.pdf`
- Screenshot PNG backup: `~/workspace/your_files/midvale-screenshots/`
