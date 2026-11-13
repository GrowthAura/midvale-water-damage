# FINDINGS — Midvale UT SEO Fix 1 (2026-11-13)

Coordinator: SEO FIX 1 coordinator (STAGE 2 of the 6-hour watchdog chain).
Fixes SEO audit 1 (qa/FINDINGS-seo-audit1-2026-11-13.md): PROBLEMS 11
(P1 1, P2 2, P3 8). Work in ~/workspace/midvale-water-damage/ only.
LOCAL ONLY — no push, no deploy, no token, no DNS, no MEMORY.md edits.
Data `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`
verified unchanged before and after. Content 1001% verbatim — 0 words changed.

## VERDICT: PROBLEMS 0 — READY FOR SEO AUDIT 2

All 11 audit problems are fixed or deliberately left unchanged with a recorded
reason (see §Left unchanged). Fresh export + full re-verification below.

## FIXES (each verified on the rebuilt out/)

### P1-1 — localhost base → live GitHub Pages URL (FIXED)
- Export built with `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`
  (no trailing slash — see the double-slash incident below).
- `public/robots.txt`: Sitemap line now
  `https://growthaura.github.io/midvale-water-damage/sitemap.xml`.
- `public/llms.txt`: all 31 URLs now on the Pages URL (0 localhost).
- `lib/content.ts`: comment updated to record the live Pages URL as the export
  base + a trailing-slash guard: the env value is stripped of a trailing `/`
  (`SITE.base` is always used as `base + "/"` or `base + route`, so a trailing
  slash would double-slash every absolute URL).
- Verified in rebuilt out/: **0 localhost** in HTML/XML/TXT/JSON-LD (the single
  remaining "localhost" string in out/ is inside Next.js's bundled WHATWG URL
  parser polyfill chunk — `"localhost"===s.host` framework code, not a site URL);
  canonicals 31/31 on the Pages URL (homepage with trailing slash, others
  no-slash); og:url 31/31; sitemap 31 locs, date-only lastmod 2026-11-12;
  robots `Allow: /`, no `Host:` line, Sitemap line on the Pages URL; llms 31/31;
  schema URLs 456 Pages-URL occurrences, 0 localhost.

### P2-1 — Maps iframe eager → lazy (FIXED)
- `components/site.tsx`: `loading="lazy"` added to the footer Maps iframe
  (embed src unchanged).
- Verified: 29 `<iframe>` tags in out/ (28 routes + 404.html), **all 29 carry
  `loading="lazy"`**; 0 iframes on the 3 location pages (unchanged — they never
  had one); in-DOM check: service page iframe has `loading="lazy"`, location
  page has no iframe. The embed still fails to load in this VM
  (ERR_TUNNEL_CONNECTION_FAILED — sandbox blocks google.com egress, same as
  audit 1; environmental, needs a real-network eyeball after push).

### P2-2 — Footer tap targets 26px → 48px (FIXED)
- `app/globals.css`: `.site-footer a` now `display: inline-flex;
  align-items: center; min-height: 48px` — covers all 27 footer links
  (8 services + 3 cities + 10 about/resources + 4 help + 2 phone links).
  Desktop header nav links (`.main-nav a`, the other 3 of the audit's 30
  counted targets) got the same 48px treatment.
- Verified in-browser: footer link min height **48px** at 320, 390 AND 1440
  (was 26px); header nav min 48px at 1440; no overlap, no layout break —
  footer screenshot @390 viewed (links evenly spaced, footer-base + sticky
  bar clean).

### P3-2 — Location serviceType generic → page H1 (FIXED)
- `components/doc-page.tsx`: location Service `serviceType` now `page.h1`,
  same pattern as the 16 service pages — truthful (the H1 IS the page's
  service name for that area).
- Verified in out/: cottonwood-heights-ut
  `"serviceType":"24/7 Water Damage Restoration in Cottonwood Heights, UT 84121"`,
  south-salt-lake-ut `"...Emergency Water Damage Restoration in South Salt Lake,
  UT 84115"`, magna-ut `"...Local Water Damage Restoration in Magna, UT 84044"`.

### P3-7 — Menu button 46x46 + header phone ~47px → 48px (FIXED)
- `app/globals.css`: `.menu-btn` 46px → 48px (width + height, ≤900px block);
  `.header-phone` gained `min-height: 48px; display: inline-flex;
  align-items: center`.
- Verified in-browser: menu button **48x48** at 320 and 390; header phone
  **48px** at 390 (was 46.6) and 50.6px at 1440 (was ~47). Header phone is
  hidden at ≤360px by design (hero Button 1 + sticky bar still call).

### P3-8 — 10 largest images 185–341 KB → optimized where quality holds (FIXED, 8/10)
- Trial: PIL re-encode at q75, method 6 (qa/img-opt-trial.py). 8 files saved
  12.3–25.0% (total **362,602 B, 19.9%** of those 8); 2 skipped (no saving:
  heroes/cottonwood-heights-ut.webp would have GROWN 2.8%, body/storm-flood-damage-1.webp
  saved only 1.4%).
- Quality adjudicated by viewed pixels at full size: the two highest-RMS
  candidates (body/cottonwood-heights-ut-2.webp RMS 1.68, cards/cottonwood-heights-ut.webp
  RMS 1.53 — both sky/gradient-heavy, the hardest case for compression) are
  visually identical to the originals — no banding, no blocking, no detail loss.
  All 8 adopted; originals backed up in qa/img-opt/orig-backup/.
- Adopted: body/magna-ut-1.webp 340,588→282,352; heroes/basement-flooding-spring-snowmelt-utah.webp
  276,840→215,212; cards/cottonwood-heights-ut.webp 217,136→174,328;
  body/mold-remediation-1.webp 203,824→157,214; body/water-leak-detection-2.webp
  200,484→157,424; body/cottonwood-heights-ut-2.webp 198,682→149,004;
  body/swamp-cooler-leak-water-damage-2.webp 198,018→160,428; heroes/magna-ut.webp
  186,350→163,358. Same filenames, dimensions, alt text — no content change.
  Total image weight 11,694,402 B → ~11,331,800 B.

### Hero lead paragraph 18px → 19px (ALREADY 19px — audit misread, guard added)
- Baseline measurement on the pre-fix build (qa/seo-fix1-measure.py, 31 routes ×
  320/390): `p.intro` computed font-size is **19px on all 62 measurements**.
  The audit's "first `<main>` paragraph 18px" was the eyebrow (`p.eyebrow`,
  18px @390 / 14px @≤360px) — chrome, not body copy; the intro follows it in
  DOM order. No rendered change was needed.
- Added an explicit `font-size: 19px` rule to `.hero p.intro` in globals.css so
  the body-copy requirement is documented in the stylesheet and guarded against
  future regressions. Rendered size unchanged (19px before and after).
- Button 2 headroom re-verified after all changes (the thin constraint):
  worst bottom **556.2px @320** (was 554.2 — +2px from the menu button 46→48,
  still ≤568 with 11.8px headroom) and **768.3px @390** (was 766.8, still <844).
  Screenshot @320 viewed: both buttons fully visible at scroll-0, intro follows.

## LEFT UNCHANGED (deliberate, with reason — verbatim wins)

- **P3-1 legal page titles** (Disclaimer 10ch, Terms of Use 12ch, Privacy Policy
  14ch): verbatim from the doc — changing them would break the verbatim rule.
  Observation only, as the audit ruled.
- **P3-5 12 body anchors over the 5-word cap** (11 × 6 words, 1 × 8): all are
  verbatim doc titles/phrases (link-annotation anchors). Shortening trades
  against the verbatim rule. Recorded as accepted tension with the anchor rule.
- **P3-3 homepage single-item BreadcrumbList**: a homepage breadcrumb with one
  item is standard; no truthful second item exists. Left as-is.
- **P3-6 homepage linked twice in `<main>` on the 3 location pages**: VERIFIED
  non-issue — both links are the breadcrumb nav on location pages
  (`app/locations/[slug]/page.tsx`: Home → `/`, "Nearby Cities We Serve" →
  `/#areas`), not body copy, targeting different anchors. No fix.
- **P3-4 breadcrumb Home href form**: VERIFIED and recorded. After the base
  swap: schema Home item = `https://growthaura.github.io/midvale-water-damage/`
  and canonical = the same URL — they match exactly. The visible breadcrumb
  Home href is the relative `/midvale-water-damage` (no trailing slash) — that
  is the form Next.js renders for `href="/"` under basePath; it cannot be
  changed without `trailingSlash: true`, which would break the locked no-slash
  URL rule for all 30 inner routes. Same resource, confirmed non-issue.

## MY OWN ERROR, CAUGHT BEFORE SHIPPING (owned plainly)
- First rebuild passed the env var WITH a trailing slash
  (`.../midvale-water-damage/`). `SITE.base` + route then produced **715
  double-slash absolute URLs** in out/ (canonicals, schema, sitemap, og:url
  all `.../midvale-water-damage//about`). The fresh static verifier flagged it
  immediately (sitemap loc set mismatch) — nothing was pushed, nothing shipped.
- Fixed by rebuilding with the env var WITHOUT the trailing slash AND adding
  the trailing-slash guard in `lib/content.ts` (see P1-1) so the mistake cannot
  recur at the next export or real-domain swap. Re-verified: double-slash 0.

## VERIFICATION (fresh, on the final rebuilt out/ — export exit 0)
- **Static** (qa/seo-fix1-static.py → qa/seo-fix1-static.json): **PROBLEMS 0** —
  31/31 FULL, verbatim missing words 0 (2,980 segments, 0 seg-miss, 0 reordered),
  H1 1/page, title/meta verbatim 31/31, links 143 body + 19 card = 162,
  orphans [], FAQ 142/142, tables 43/43, visible `(/.../)` 0 in HTML/TXT/XML/CSS,
  double-slash 0, unprefixed href/src 0. (The 8 JS/WEBP "paren" hits are framework
  JS regexes + webp binary bytes — same known noise as the link-fix round.)
- **Render** (qa/seo-fix1-measure.py post-fix + qa/seo-fix1-render.py):
  intro 19px, eyebrow 18px @390 / 14px @320 (chrome, accepted); Button 2
  31/31 @320 (worst 556.2px) and @390 (worst 768.3px); footer min 48px @320/390/1440;
  header nav min 48px @1440; header phone 48px @390 / 50.6px @1440; menu 48x48;
  overflow 0 @320/390/1440; console errors 0 @390 on 31/31; failed requests 0
  local (51 Maps-embed attempts, all sandbox-blocked google.com egress —
  environmental, same as audit 1).
- **Real clicks** (qa/seo-fix1-click2.py, wait_for_url-based): 4/4 — service
  card → emergency page, footer location link → cottonwood page, breadcrumb
  Home → homepage, mobile menu link → sewage page. Subpath kept on all.
  (Two of my own script errors owned: first click script used networkidle waits
  that return before client-side nav commits, and a wait pattern demanding a
  trailing slash the visible homepage href does not have. Both fixed, re-run clean.)
- **Images**: 107 webp on disk, 107 img tags; the 8 optimized files render
  correctly in the rebuilt out/ (byte sizes match the adopted q75 files).

## FILES CHANGED
- `lib/content.ts` — comment + trailing-slash guard (no default change).
- `public/robots.txt`, `public/llms.txt` — localhost → Pages URL.
- `components/site.tsx` — Maps iframe `loading="lazy"`.
- `components/doc-page.tsx` — location `serviceType: page.h1`.
- `app/globals.css` — footer/nav 48px tap targets, header phone 48px,
  menu button 48px, explicit hero-intro 19px.
- `public/images/**` — 8 files re-encoded q75 (originals in qa/img-opt/orig-backup/).
- Evidence: qa/seo-fix1-static.py/.json, qa/seo-fix1-measure.py, qa/seo-fix1-baseline.json,
  qa/seo-fix1-postfix.json, qa/seo-fix1-render.py/.json, qa/seo-fix1-click2.py,
  qa/seo-fix1-click-debug.py, qa/seo-fix1-shots.py, qa/seo-fix1-footer-390.png,
  qa/seo-fix1-hero-320.png, qa/img-opt-trial.py, qa/img-opt/ (candidates + backup).

## READINESS
**PROBLEMS 0 — ready for SEO audit 2** (fresh + independent re-check, per the
watchdog chain). I did not push, deploy, touch DNS, or use any token. Still open
(his call / later): real domain swap (Pages URL is the live base until he gives
one); Maps embed needs a real-network eyeball after push; the 6 honestly-empty
body-image slots from Stage 0; commercial-3 B&W P3 (open at his call).
