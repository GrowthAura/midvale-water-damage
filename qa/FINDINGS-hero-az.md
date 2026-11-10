# FINDINGS — Midvale UT HERO + A-to-Z Round (2026-11-10)

Order: Noorullah, ~20:32 PKT — "hero kisi ka bhi best nahi, maza nahi aa raha":
intro INTO the hero on every page, KILLER photographic hero images, 101% end
level; then EVERY page + EVERY section, SEO + user-friendly, user POV + Google
POV, everywhere; think proactively (khud bhi socho).

Local only. No push / deploy / domain / DNS / Vercel / GitHub / token.

## FINAL VERDICT — PROBLEMS 0

Final fresh re-run on the final export (`npm run export` exit 0):
- **Browser check (`qa/hero-az-check.py`): 21 routes, FAILS = 0**
- **Extras (`qa/hero-az-extra.py`): FAILS = 0**
- Screenshots: `qa/hero-az/` — 42 PNGs (desktop full + mobile top per page),
  viewed by pixels by the parent for home, emergency, mold, Cottonwood heroes
  + the home card grid; all other pages verified by the automated checks +
  their screenshots on disk.

## 1. BEFORE / AFTER — the hero (the core defect)

BEFORE (verified by parent before the round):
- Homepage: eyebrow + H1 + intro + 2 equal buttons + a flat SVG/CSS branded
  panel BELOW the buttons. Intro technically inside the hero section but the
  hero read flat/dead — no photo, weak visual punch. Trust band sat below.
- Service / guide / location pages: hero was just breadcrumb + H1 in a plain
  `.page-head` — NO intro in the hero, NO image in the hero at all; the SVG
  panel sat in the body below.

AFTER (one pattern on all 21 pages, `components/site.tsx` `PhotoHero`):
- breadcrumb (inner pages) → eyebrow → H1 (verbatim, exactly 1, visible) →
  INTRO inside the hero (homepage: doc lede verbatim; service pages: their
  verbatim homepage summary; location pages: their verbatim homepage line;
  guide: its one verbatim sentence) → the 2 equal buttons → trust chips.
- Trust band removed — chips now live INSIDE the hero, no duplication.
- Body dedup: the summary lives in the hero intro ONLY, not repeated in the
  body (body keeps verbatim H2 + link + buttons). Verified: each summary
  appears exactly 1× in visible body text on its page.
- Hero image: darkened photographic background + dark shade gradient
  `rgba(5,22,20,.84/.74/.88)`; `<img fetchPriority="high">`, exactly one
  `<link rel="preload">` (see defect D4); `og:image` = the page's own hero
  on all 21 pages; twitter card `summary_large_image`.
- H2/H3 distinction fixed proactively (was flat): H2 pine + copper accent
  bar, H3 pine-2 `#15524c`.
- Mobile ≤600px: hero order keeps buttons directly under H1 (proven
  Round-1 fix, re-verified).

## 2. MEASURED — final export

| Gate | Result |
|---|---|
| Routes 200 | 21/21 |
| H1 = 1, verbatim, visible | 21/21, white `rgb(255,255,255)` 21/21 |
| Hero section = 1, intro in hero | 21/21 |
| Hero image loaded (natural 1600×1066) | 21/21 |
| og:image == own hero | 21/21 |
| Self-canonical | 21/21 |
| Hero preload | exactly 1/page, 21/21 |
| Buttons equal | 21/21 — 322×56px desktop on every page |
| Mobile hero buttons fully visible at first paint (390×844, sticky bar 56px) | 21/21 — bottom max 694px < 788px limit |
| Body font | 18px on 21/21 |
| Overflow 1440 / 390 / 320 | 0 on 21/21 at all three widths |
| CLS | 0 on 21/21 |
| FCP | max 488ms (home 488ms; was 620ms before the preload fix) |
| Page weight | 495KB (lightest service page) – 1981KB (homepage, 20 images) |
| Word-diff vs frozen-doc.txt | 114/114 lines, 0 missing |
| Linked-page summaries exactly 1× in visible body | 16/16 services + guide + locations |
| Internal links | 45 hrefs, 0 missing files, 0 broken, 0 orphans, 0 self-links |
| Contamination (Tulsa/918/Edmond/Plano/Pleasant Grove/Lancaster/Fort Myers/McDonough/Broken Arrow/Owasso/Naples/Tukwila) | 0 in shipped code + out/ |
| Em/en dashes, dangling "See and"/"See." | 0 pages |
| Homepage extras | FAQ H3 6/6 = schema, service cards 16 + area cards 3, card photos 16+3, H2 12, H3 24, footer map home yes / area pages no |
| Sitemap | 21 locs, date-only lastmod `2026-11-10` on all |
| Robots | `Allow: /`, no `Host:` line |
| Images site-wide | 40 unique srcs, 0 repeats, 0 over 200KB, 0 metadata problems |

LCP: headless shell emits no LCP entries, so no LCP number is claimed.
Honest proxy: FCP max 488ms; the LCP element on every page is the hero
`<img>` (preloaded, fetchPriority high, WebP, near rendered size).

### Hero contrast — measured, not assumed
White H1 text vs the composited hero background (actual photo pixels +
overlay gradient at the H1's real position, WCAG formula), desktop 1440:
- Home: median 17.87:1, 90th-percentile 16.49:1, brightest pixel 9.83:1
- Emergency-water-extraction: 18.26 / 14.11 / 8.95
- Mold-remediation: 17.64 / 13.30 / 8.82
All far above WCAG AA 4.5:1 — even against the single brightest pixel
behind the H1. The darkened-hero order is met on every sampled page.

## 3. IMAGES — per-image decisions (40/40 fresh, 0 old-site images)

Generated fresh for Midvale by 11 worker subagents (media tool caps at 4
calls/agent/response), each image view-verified by pixels by its worker;
parent spot-viewed home, emergency, mold, Cottonwood heroes + the home
card grid. Normalized by `/tmp/normalize_images.py` (heroes 1600×1066,
cards 1200×675/800, quality 78, metadata stripped). Sidecar `.json` files
deleted, never shipped. No "AI" word in any filename/path/alt/metadata;
exiftool shows only File/RIFF/Composite tags (no EXIF/XMP/C2PA/prompt);
byte-scan clean. No image is claimed to be a real job photo anywhere.

- Heroes (21, 1600×1066, 31–182KB, total 2350KB): home 114KB,
  emergency-water-extraction 132KB, basement-flooding-cleanup 101KB,
  window-well-flooding 96KB, burst-pipe-water-damage 133KB,
  sewage-backup-cleanup 122KB, water-heater-leak-cleanup 74KB,
  swamp-cooler-leak-water-damage 136KB, ceiling-water-damage 77KB,
  crawl-space-water-damage 127KB, hardwood-floor-cabinet-drying 107KB,
  condo-apartment-water-damage 97KB, commercial-water-damage 123KB,
  storm-flood-damage 120KB, mold-remediation 126KB,
  water-leak-detection 58KB, water-damage-repair 31KB,
  midvale-water-sewer-emergency-contacts 98KB, cottonwood-heights-ut 182KB,
  south-salt-lake-ut 115KB, magna-ut 181KB. All ADOPTED.
- Cards (19, 1200×675/800, 28–156KB, total 1360KB): 18 ADOPTED as
  generated; **1 REJECTED + REGENERATED** — see D1 below.
- Zero repeats site-wide: 40 unique srcs. Zero images from any past site
  (not renamed/cropped/resized). No wrong-city cues (no palm trees etc.);
  Utah homes, Wasatch snowmelt, window wells, swamp coolers as briefed.
- Nit, not a defect: the water-leak-detection card's thermal-camera screen
  shows an orange/blue heat pattern (no letters/digits) — acceptable,
  it is the tool's display, not legible words.

## 4. DEFECTS FOUND + FIXED (with root cause)

### D1 — REJECTED CARD: water-leak-detection (real, found by worker cb0157a0)
The generated card showed a moisture meter with a visible brand wordmark
"EXTECH" on its housing and a display reading "35.6%" — violates the
no-text / no-letters / no-logos rule. The worker had used all 4 of its
calls and could not regenerate; it reported the rejection plainly.
FIX: parent regenerated it (blank unbranded meter, blank display), viewed
the pixels (clean: blank dark display, no brand, no digits, thermal camera
with orange/blue heat image, wet wall), normalized to 1200×800 / 42KB,
metadata-clean, replaced the rejected file. Re-exported + re-verified.

### D2 — SITEMAP HAD NO <lastmod> AT ALL (real, found by hero-az-extra)
`app/sitemap.ts` used the key `lastmod:` — but Next.js 14's
`MetadataRoute.Sitemap` field is `lastModified:`. The wrong key was
silently dropped (no excess-property error because the object is built
inside a `.map()`), so the built `sitemap.xml` had 21 locs and ZERO
lastmod entries. NOTE: Round 2 had claimed "date-only lastmod" — that
claim was wrong; it read the source, not the built file.
FIX: `lastModified: LASTMOD`. Built sitemap now has
`<lastmod>2026-11-10</lastmod>` on 21/21. Re-verified.

### D3 — HERO IMAGE PRELOADED TWICE (real, found on the re-run)
Every page emitted two identical
`<link rel="preload" as="image" href="...hero.webp" fetchPriority="high"/>`
tags: one manual (added in the rebuild) + one automatic from Next for the
`fetchPriority="high"` `<img>`. Browser dedupes the fetch, so it was
wasteful, not broken — fixed anyway.
FIX: removed the 4 manual preload lines (`app/page.tsx`,
`app/[slug]/page.tsx` ×2, `app/locations/[slug]/page.tsx`) + corrected
the two comments that described the manual preload. Re-export:
exactly 1 preload/page; FCP max improved 620ms → 488ms.

### D4 — CHECK-SCRIPT BUGS (owned plainly — script errors, NOT site defects)
Four rounds of the round's own checks flagged things that were not site
defects. Each was fixed in the script and the check re-run fresh; no
defect was invented to show work.
1. Run 1 (25 fails): mobile-button selector matched ALL `.btn` on each
   page (hero + body + final CTA) instead of hero-only — the hero buttons
   themselves were fully visible (tops 407–622, bottoms 463–694, limit
   788). Fixed: scope to `section.hero-photo .hero-buttons .btn`.
2. Run 1 (4 fails): lazy below-fold card images not yet loaded at check
   time. Fixed: scroll-through before the img check. Run 2 still missed
   the 3 area cards: the page has `scroll-behavior: smooth`, so stepped
   `scrollTo()` never reached the bottom. Fixed: set `scrollBehavior =
   'auto'` first + 1500ms wait. Run 3: 0 fails.
3. Run 2 extras (summary 5×, contamination, "AI", links, sitemap):
   - Summary count included `<head>` meta/og/twitter — fixed to count
     visible BODY text only (exactly 1× = hero only).
   - Contamination sweep included working logs (`PROGRESS.md` names the
     theme provenance) — scoped to shipped code (`app/`, `lib/`,
     `components/`, `public/`) + `out/` only.
   - "AI" check used substring matching and flagged
     "water-damage-rep**ai**r.webp" — fixed to whole-token matching.
   - Link check treated `/_next/`, `/images/`, `/favicon.svg` as pages —
     assets now skipped.
   - Sitemap lastmod — real defect D2 above, not a script bug.
4. Run 3 extras (word-diff 28 → 23 → 21 → 0): the naive contiguous
   matcher flagged lines whose every content word IS on the page — only
   URL slugs (live in href attrs), table `|` separators (`<td>`
   boundaries), and `[bracket]` button labels were "absent". Also a
   variable-shadowing bug: the link section reassigned `missing = []`,
   so the JSON field `word_diff_missing` reported the link list, not
   the word-diff list. Fixed: token-based word-diff (content words vs
   visible text + hrefs + alts), meta description checked against raw
   HTML (it is an attribute, not text), `missing_links` renamed.
   Final: 114/114, 0 missing — and the component proof stands: no doc
   word is missing from the page.
5. Contrast probe (my own script, 2 failed runs): plain `http.server`
   404s extensionless routes, and my custom server served the wrong
   cwd on the first attempt (directory listing, 0 hero sections).
   Fixed: mapping server with cwd=`out/`. The site was never at fault.

## 5. A-to-Z — every page / every section, both points of view

Checked all 21 routes + homepage sections in Theme v2 order + every
service/location/guide section, user POV and Google POV. What was
actually changed beyond the hero (proactive, "khud bhi socho"):
- H2/H3 hierarchy was flat (same pine colour) — H2 now pine + copper
  accent bar, H3 pine-2 `#15524c`.
- Trust chips were duplicated (hero + trust band) — band removed.
- Summary was duplicated (hero + body) — body deduped, hero-only.
- `og:image` was generic/missing per page — now each page's own hero.
- Twitter card was `summary` — now `summary_large_image`.
- Sitemap lastmod — D2 above.
- Duplicate hero preload — D3 above.
- Rejected card image — D1 above.

What was checked and left as-is (named, not forced):
- Service/location/guide pages are SHORT by design (H2 + link + buttons):
  the doc is homepage-only and linked pages carry ONLY their verbatim
  homepage summary. No invented content was added to fill them.
- Homepage is the heaviest page (1981KB, 20 images) — inherent to 16
  service + 3 area photographic cards; all images lazy except the hero,
  FCP 488ms, CLS 0.
- Meta title stays 72ch verbatim (over 60) — his call, flagged not
  rewritten.
- Footer map iframe renders blank in the sandbox (google.com unreachable
  there) — renders in a real browser; same caveat as Round 2.
- Canonical/sitemap/og still use the `http://localhost:3000` placeholder
  — no domain exists yet; swap when he gives one.
- About / Contact / Privacy not built — no doc content; do NOT invent.

## 6. OPEN ITEMS (his call — not decided silently)

1. Real job photos vs generated images: all 40 images are generated
   illustrations, never claimed as real job photos. If real Midvale job
   photos arrive, swap them in.
2. Domain: none yet — canonical/sitemap/og on localhost placeholder.
3. Meta title 72ch verbatim (over 60) — kept verbatim per his standing
   rule; rewrite needs his wording.
4. Service/location/guide pages are thin by design until their own docs
   arrive.
