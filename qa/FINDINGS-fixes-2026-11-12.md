# FINDINGS — Fix Re-verification, Midvale UT rebuild (2026-11-12, fix coordinator)

## Verdict
**PROBLEMS 0 — READY for re-push live.** All 6 problems the independent
verifier found (`qa/FINDINGS-rebuild-2026-11-12.md`) are fixed in code and
re-verified fresh on the FINAL built bytes. Nothing is pushed — the parent
pushes with the token.

- Source data untouched: `lib/pages-data.json` sha256 still
  `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`.
- Final build: `npm run export` exit 0, 35/35 static pages.
- Served locally on the `/midvale-water-damage/` subpath (mirror of `out/`,
  port 8324) for every browser check below.

## Per-problem fix + evidence

### P2-1 — 10 orphan routes (0 inbound links)
- **Fix:** new `<nav aria-label="About and resources">` in the Footer
  (`components/site.tsx`) linking all 10: About, Contact, Privacy Policy,
  Terms of Use, Disclaimer + the 5 blogs ("Frozen Pipes in Midvale",
  "Swamp Cooler Winterizing Checklist", "Upstairs Leak: Who Pays?",
  "Can Mold Grow in Utah?", "Basement Flooding & Spring Snowmelt").
  Footer is template chrome, exempt from body-link rules. Footer grid
  4 → 5 columns (`app/globals.css`).
- **Evidence:** `verify-rebuild.py` link graph — **orphans []** (was 10).
  Real click home footer → /about: correct H1, subpath kept.

### P2-2 — Button 2 below fold @320×568 on 28/31 pages (worst +221px)
- **Fix:** `≤360px`-only CSS (`app/globals.css`, nothing changes at 390 or
  desktop): header 136→110px (`.header-phone` hidden — hero Button 1 +
  sticky bar still call; brand + hamburger still wrap to two rows at 320,
  measured), hero padding-top 32→16, breadcrumb truncated to one line
  (nowrap + ellipsis, 14px), eyebrow 14px, H1 24px, hero-buttons margin
  8px, `.btn` min-height 48px.
- **Own error, caught by re-verification, fixed:** the first attempt kept
  Button 2 at 19px/28px padding — its "Request Emergency Help" wrapped to
  2 lines and grew to 49.6px vs Button 1's 48px. The re-run render sweep
  flagged all 31 pages "hero buttons unequal". Fixed by giving BOTH
  buttons the same 18px font + 0 16px padding at ≤360px (each fits one
  line at 48px tall). The final sweep shows **buttons unequal: []**.
- **Evidence:** full render sweep, 31/31 pages — Button 2 visible at
  scroll-0 @320 (worst bottom **493px**, was 789px; fold = 568px) AND
  @390 (worst 767px of 844px). Buttons equal 31/31 at every viewport.
  Screenshots eyeballed: Cottonwood + home @320 — header clean, breadcrumb
  one truncated line, both buttons fully visible, equal height.

### P2-3 — Contact page: no form (content describes one)
- **Fix:** new `components/contact-form.tsx` ("use client"), rendered in
  `components/doc-page.tsx` right after the verbatim "[Send My Request]"
  paragraph, on `/contact` only. Fields + labels EXACTLY from the Contact
  tab (Tab 3): Name; Phone number; Address or ZIP code; What happened
  (short description); Is the water still running? (Yes / No / Not sure
  radios); Best time to call. Submit button text verbatim
  "[Send My Request]". Honest notice: "Note: this form does not send on
  this preview site. For the fastest help, please call (385) 337-3560 —
  calling is faster than the form." Submit shows a call-first message.
  No verbatim text on the page was deleted or changed.
- **Evidence:** focused browser test — all 6 labels + 3 radios + submit
  text + notice exact; fill + submit shows the call-first message.
  The form is template chrome: `/contact` main words 769 (was 717),
  extra +52 form words, excluded from the content word-diff; verbatim
  diff stays 0 on all 31 pages.

### P3-1 — RSC prefetch 404 on every page load
- **Fix:** `prefetch={false}` on the brand Link, nav Home Link, footer
  `/#faq` + `/#services` Links, Breadcrumb conditional, and the
  `app/not-found.tsx` home Link (grep confirmed these were all the `/`
  links).
- **Evidence:** render sweep across 31 routes × 3 viewports —
  **console errors: [], failed requests: []**, 0 RSC 404s. Focused check
  on `/`, `/emergency-water-extraction`, `/contact`, `/about`: 0 console
  errors, 0 failed requests.

### P3-2 — Homepage table order inverted
- **Fix:** `app/page.tsx` section 7 — the paragraph "Clean water turns
  into gray water in about 48 hours…" moved to AFTER the water-category
  table (doc order: H2 → table block 51 → paragraph block 52). Content
  unchanged, order only.
- **Evidence:** homepage table position 23921 < gray-water paragraph
  position 24551 in built `out/index.html`; `verify-segments.py` —
  homepage 124 segments, **0 missing, 0 reordered**; all pages 0
  reordered.

### P3-3 — Mobile menu has no scroll lock
- **Fix:** Header `useEffect` (`components/site.tsx`): on menu open,
  body `position:fixed` + `top:-scrollY` + `left/right:0` +
  `overflow:hidden` (overflow:hidden alone does NOT lock scroll in
  Chromium). Scroll position captured in a ref and restored ONLY on an
  explicit close (Escape key / menu-button toggle) via double rAF.
- **Own error, caught by focused testing, fixed:** the first restore ran
  in the effect cleanup and fired after a menu-link navigation, dragging
  the NEW page back to the old scroll position (1500px). Restructured so
  the cleanup only clears styles — navigation never restores.
- **Evidence (final build, focused tests):** lock holds (scroll attempts
  do nothing while open); Escape restore exact at scroll 800 (delta 0)
  and 2000 (delta 0); toggle-close restore exact at 1200; menu-link click
  (Emergency) lands on the new page at **scrollY 0** with correct H1,
  subpath kept, menu closed; control (plain footer click, no menu) also
  lands at 0 — confirming Next scrolls to top on its own.

## Re-verification summary (final built bytes)

| Check | Result |
|---|---|
| `qa/verify-rebuild.py` (static) | PROBLEMS **1** — only the adjudicated localhost P3 (below). Orphans [], sitemap 31 locs (lastmod 2026-11-12, date-only), llms 31, gates: double-slash 0, unprefixed href/src 0, unprefixed img 0, favicon ok. Traces 0. Images 50 files, 0 md5 dups. All pages missing 0, all FULL (293–2,178 main words). |
| `qa/verify-segments.py` | 0 missing segments, 0 reordered across all pages (3,116 segments). |
| `qa/verify-render.py` (31 routes × 3 viewports, real browser) | **PROBLEMS 0.** Button 2 visible scroll-0 31/31 @320 AND @390; buttons equal 31/31; overflow 0; console errors 0; failed requests 0; no white screens; no ChunkLoadError. Real-click nav home → emergency, logo → home, footer → mold, header → sewage, breadcrumb → home — all correct H1, subpath kept. Mobile menu opens (flex, aria true), sticky bar works. |
| Focused menu tests (`/tmp/menu-final2.py`) | Lock + exact restore + nav-at-top — all pass (above). |
| Focused RSC + form + footer tests (`/tmp/fix-checks.py`) | 0 RSC 404s on 4 pages; form labels/radios/submit/notice exact, submit shows call-first message; footer click → /about correct. |

## Adjudications (not defects)
1. **P3 "localhost string in built HTML"** (verify-rebuild.py's only flag):
   carried over from the rebuild verdict — `localhost` appears only in
   JSON-LD/canonical/og/RSC placeholder values, **0 times in visible
   copy** (verified by HTML-parser scan of index/contact/about). Same
   adjudication as the rebuild verifier's A2.
2. **Mobile-nav "error" in verify-render.py output:** the script clicks
   `#main-nav a[href*='burst-pipe-water-damage']`, a link that does not
   exist in the header nav (it holds Home + Emergency + Sewage only).
   Script artifact, not a site defect — the menu itself is proven by the
   focused tests above (open/close/lock/restore/navigate).

## Files changed (vs pushed main 1cbf688)
- Modified: `app/globals.css` (P2-1 footer grid, P2-2 ≤360px rules,
  contact-form styles), `app/page.tsx` (P3-2 order), `app/not-found.tsx`
  (P3-1 prefetch), `components/site.tsx` (P2-1 footer nav, P3-1
  prefetch, P3-3 scroll lock), `components/doc-page.tsx` (P2-3 form
  hook), `qa/verify-rebuild.py` (checker fix: expected sitemap loc set
  — homepage `/` with slash; the old set flagged a false "mismatch").
- New: `components/contact-form.tsx`.
- Unchanged: `lib/pages-data.json` (sha256 verified), all images,
  all verbatim content.

## Notes for the re-push
- Review pack `~/workspace/your_files/midvale-rebuild-review.pdf` (31 pp)
  predates these fixes — regenerate after the push if he reviews again.
- Contact form cannot submit on GitHub Pages (static) — the honest notice
  on the form says so; on real PHP hosting it would need a handler.
  That is the state his order accepted.
- No token was used or requested by this fix round; nothing was pushed.
