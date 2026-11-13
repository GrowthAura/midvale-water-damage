# DESIGN ROUND — CSS / BODY-IMAGE RENDERER — FINDINGS 2026-11-13

Worker: design/CSS. Scope: `app/globals.css`, `components/doc-page.tsx`,
`app/not-found.tsx` only (site.tsx, page.tsx read, no changes needed).
LOCAL ONLY — no push/deploy/token/DNS. Data SHA verified before + after:
`21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`
(unchanged). Content words: 0 changed/added/removed (static verifier:
missing words 0 on 31/31 pages, see below).

## 1. What changed

### components/doc-page.tsx — body-image renderer (NEW)
- `loadBodyImages()` reads `lib/body-images.json` with `fs` at build time.
  Missing file / bad JSON / bad entry → `{}` → NO images, never a broken
  tag, never a failed build (proven: 2 exports with the file absent, exit 0).
- Contract honoured exactly:
  `{"<route>": [{"src": "/images/body/<slug>-N.webp", "alt": "...",
  "afterH2": <0-based index among the page's h2 blocks>, "layout":
  "split"|"sticky"}]}`. afterH2 counts EVERY h2 block in document order,
  INCLUDING the FAQ h2. Validation drops entries with a non-`/images/body/`
  src, non-`.webp` src, empty alt, non-integer/negative afterH2, or a layout
  other than split/sticky. One image per section (first valid entry wins).
- Blocks are grouped into H2-sections (heading + following blocks until the
  next H2); blocks before the first h2 (privacy/terms intro p) render
  unwrapped, exactly as before. FAQ state is section-local (the FAQ h2's
  following h3+p pairs are exactly its items) — output identical to the old
  flat loop. The shared `linkSeen` set is still consumed in document order
  across sections, so one-link-per-target is preserved.
- A section with an image renders as
  `.h2-section.with-image` > `.h2-section-text` (nodes) + `figure.body-img-fig`
  (`sticky` class for sticky layout) > `img.body-img` with
  `src={ASSET_PREFIX + src}`, `width={1200} height={675}`,
  `loading="lazy" decoding="async"`. Sections without an image render
  unwrapped — same DOM, same measure, same word count as before.
- Route `/` entries are ignored: the homepage is a bespoke component
  (`app/page.tsx`), not DocPage (see Open items).

### app/globals.css — design
- **No underlines (rule 3):** global `a { text-decoration: none;
  border-bottom: none; }` + same for `:hover/:focus/:active/:visited`.
  Removed the old `.main-nav a:hover` underline and the mobile-menu item
  `border-bottom` separators (spacing now separates menu items; the
  dropdown panel keeps its own bottom edge, which is not a link).
  Built CSS: `text-decoration:underline` occurrences = 0.
- **H2/H3 (rule 4):** H2 = pine `#0e3b38` + 72px copper underline bar;
  H3 = pine-2 `#15524c`, no bar. The bar previously applied ONLY to
  homepage `.section h2` — it now applies to `.page-body h2` too, so all
  31 pages share one H2 treatment. Heading SIZES unchanged (H1 44/34/24,
  H2 32/28, H3 24). Verified in built CSS
  (`.page-body h2:after,.section h2:after{...width:72px...}`) and rendered:
  H2 computed `rgb(14, 59, 56)` on 31/31 pages, H3 `rgb(21, 82, 76)`,
  `::after` bar 72×4px copper `rgb(194, 106, 36)`.
- **Body 18px (rule 5):** explicit `p, li, td, th { font-size: 18px; }`
  (was inherited-only). Breadcrumb at ≤360px raised 14px → 18px (it is
  listed body copy; single-line ellipsis truncation kept, so the hero
  cost is ~6px). Radio inputs given explicit `font-size: 18px`
  (their UA default computed 13.33px; labels were already 18px).
  Header/footer chrome stays exempt by the brief; the ≤360px eyebrow
  (14px) and brand text (15px) are hero/header chrome and load-bearing
  for Button 2 above the fold — left as-is, see verification.
- **Header/footer polish (rule 2):** brand-city copper `#c26a24` →
  copper-dark `#9d5418` (3.90:1 → 5.65:1, AA); brand-mark `flex-shrink: 0`;
  header phone padding 10px 18px → 10px 20px; footer grid padding
  48px → 56px top; footer headings `letter-spacing: 0.5px`; footer list
  spacing 8px → 10px; **footer-base bottom padding 96px → 32px on
  desktop** (the 96px was dead space — the sticky bar only exists ≤767px,
  where the 76px override still applies). Header/footer VISIBLE text:
  0 em/en dashes on all 31 pages (rendered innerText check; the 9 em
  dashes in site.tsx are all in code comments, never rendered).
  Bonus chrome fix (template chrome, not doc content): 404
  "Sorry — this page…" → "Sorry, this page…" in `app/not-found.tsx`.
  NOT touched: `components/contact-form.tsx` is outside my editable set
  and still carries two em dashes in its notice/sent text
  ("— calling is faster…", "Thanks — …") — flagging, not fixing.
- **Layout rhythm (rule 6):** `.section` padding 56px → 64px;
  `.page-body` padding 40px/64px → 48px/72px; H2 sections get a 48px beat
  (`.page-body .wrap > h2:not(:first-child) { margin-top: 48px; }`,
  first H2 flush under the hero; grid sections get the same 48px via
  `.h2-section.with-image`); mid-section H3 `margin-top: 36px`;
  list spacing 8px → 10px, `ul/ol` bottom 16px → 20px; table cell
  padding 14px → 16px, `.table-wrap` margin 24px 0 28px; FAQ item gap
  16px → 20px; note-box / contact-form top margin 28/32px → 32/36px.
- **Body-image grid CSS (rule 1):** `.h2-section.with-image` =
  `grid minmax(0,1fr) 400px, gap 40px, align-items: start`;
  `.body-img-fig.sticky { position: sticky; top: 96px; }` (72px sticky
  header + 24px air); `.body-img` = `width:100%; max-width:100%;
  aspect-ratio:16/9; height:auto; object-fit:cover; border-radius:14px`.
  ≤900px: single column, figure `order:-1` (image ABOVE the text, full
  width), sticky → static.
- **Contrast fix found by measurement:** steps counter number (white on
  copper `#c26a24`, 3.90:1 — 18px bold is below the large-text threshold,
  so it needed 4.5:1) → circle background now copper-dark `#9d5418`
  (5.65:1). `.trust-band` (white on copper) is dead CSS — unused in any
  tsx — left alone.

## 2. Contrast ratios (WCAG, script qa/contrast-design-2026-11-13.py)
All 25 measured pairs PASS AA (≥4.5:1). Worst = **5.65:1**
(brand-city / card-link / white-on-copper-dark, three-way tie).
- H2 pine on white 12.34:1, on mist 10.57:1, on sand 10.96:1
- H3 pine-2 on white 8.96:1, on mist 7.68:1, on sand 7.96:1
- Body ink on white 14.91:1, mist 12.77:1, sand 13.24:1
- Muted #41524e on white 8.26:1; body-link pine-2 on white 8.96:1
- White on copper-dark 5.65:1; white on hover #7c3f12 8.15:1
- White H2/th on pine 12.34:1; footer link #dfeae7 on pine 10.03:1,
  footer hover #f2c89b on pine 7.94:1
- Hero: white H1 on #07211e 16.86:1; eyebrow #f2c89b 10.85:1;
  intro #eef4f2 15.14:1 (before the dark shade; shade only darkens)

## 3. Verification — manifest ABSENT (final build)
- `npm run export` exit 0 (final build; temp manifest deleted before it).
- Render check `qa/verify-design-css.py` (Playwright, local subpath
  mirror port 8331), 31 routes × 3 viewports (1440/390/320), full JSON
  `qa/verify-design-css.json` (+ raw `qa/verify-design-css-raw.json`):
  - Overflow 0 at 320/390/1440 on 31/31 pages.
  - H1 = 1 on 31/31 pages (all viewports).
  - Button 2 visible at scroll-0: 31/31 @320 AND 31/31 @390. Worst
    Button 2 bottom: 497.2px @320 (margin 70.8px), 766.8px @390
    (margin 77.2px) — worst page `/resources/basement-flooding-spring-snowmelt-utah`.
    Buttons exactly equal (height + width) on all pages/viewports.
  - Underline computed-style: 1,313 links checked (header+main+footer).
    text-decoration violations: **0**. The ONLY border-bottom-width>0 hits
    (372 = 31 pages × 3 viewports × 4 buttons) are the hero/bottom
    `.btn` call buttons (tel: links, NOT `<a href="/...">`): their
    designed 2px FULL border (Button 1 transparent, Button 2 pine
    outline) — a button treatment, not an underline. Zero violations
    among internal `<a href="/...">` links (nav, header, footer,
    breadcrumb, .body-link, .card-wrap-link, card, FAQ links).
  - Body copy <18px: none except (a) hero eyebrow 14px @320 only
    (hero chrome, exempt + load-bearing for Button 2), and (b) radio
    INPUT controls 13.33px — FIXED (explicit 18px; re-verified 18px on
    /contact at all 3 viewports in the final spot-check).
  - Header dashes 0, footer dashes 0, on 31/31 pages (rendered text).
  - Visible `(/.../)` path text: 0 on 31/31 pages.
  - Contact form intact: form present, fields cf-name, cf-phone,
    cf-address, cf-what, water-running ×3, cf-best-time, submit.
  - Footer links: 27 per page on 31/31 (8 Services + 3 Cities +
    10 About/Resources + 4 Help + 2 phone links).
  - Console errors 0, failed local requests 0, on all pages/viewports
    (footer Google Maps iframe excluded as external; 0 external
    failures recorded in this sandbox run).
  - H2 colour rgb(14,59,56) / H3 rgb(21,82,76) uniform; H2 bar 72×4px.
  - Body images: 0 tags (manifest absent — correct).
- Static verifier `qa/verify-linkfix.py` on the final build
  (`qa/verify-linkfix-static.json`): **PROBLEMS []**. Missing words 0,
  kept links **162/162** (143 body + 19 card), orphans [], body-copy
  self-links [], visible paren-path 0, fullness FULL 31/31, sitemap 31,
  tables 43/43, FAQ 142/142, 0 double-slash, 0 unprefixed href/src.
  (Extra words 749 = known template chrome: hero buttons ×2/page +
  trust chips + header/footer words — same accounting as prior rounds;
  missing 0 is the verbatim gate.)
- Recomputed from rendered DOM with basePath stripped: internal links
  1,063 (desktop), orphans 0. Rendered self-links are header/footer
  chrome only (logo + footer nav pointing at the current page — exempt
  by the standing rule; body-copy self-links 0 per the static verifier).
- Visual spot-check: screenshots `qa/render-design/` (home, emergency,
  cottonwood × desktop + 390) — header, hero, equal buttons, H2 copper
  bar all render as designed; mobile 390 shows both buttons above the
  fold with the intro following.

## 4. Verification — manifest PRESENT (temp manifest, then deleted)
Temp manifest `lib/body-images.json` (7 routes incl. invalid entries;
test image files did NOT exist — tag/layout check only, their 404s
expected and filtered). Export exit 0. Focused check
`qa/verify-body-images.py`:
- `/emergency-water-extraction` afterH2 0 split: 1 grid, img 400×225
  (16:9), attrs 1200×675, loading lazy, decoding async, figure static,
  figTop == h2Top (aligned with section top). Overflow 0.
- `/locations/cottonwood-heights-ut` afterH2 2 sticky: 1 grid, figure
  `sticky`, computed `position: sticky` @1440, static @390/320.
  **Pin proven:** viewport 1440×500, scrolled 200px into the 608px
  section → figure top = exactly **96px** (top offset). When the grid
  scrolls fully past, the figure leaves with it (correct sticky
  containment; figure bottom == grid bottom at release).
- `/ceiling-water-damage` afterH2 1 ×2 entries: exactly 1 img, the
  FIRST entry (split/static); second entry ignored.
- `/about` afterH2 99 + bad layout "floating": 0 imgs. `/burst-pipe…`
  bad src prefix + empty alt: 0 imgs. `/mold-remediation` non-array
  value + unmatched route key: 0 imgs, no error. `/` homepage entry:
  0 body imgs (homepage is not DocPage).
- Mobile @390/@320 on image pages: figure ABOVE the text
  (figTop < h2Top), full width (342px @390, 272px @320), 16:9 height
  (192.4 / 153), sticky → static, overflow 0, Button 2 visible at
  scroll-0 (437.2px @320, 651.3px @390 emergency; 467.2px @320,
  693.8px @390 cottonwood).
- Temp manifest DELETED after the test; final export rebuilt without it
  (0 `body-img` tags in final HTML). The loader file is NOT in the repo
  state I hand over — image workers own the real manifest.

## 5. Script errors owned
- First render-verification run crashed in its own summary step
  (`TypeError` sorting a set containing `None`: privacy/terms/disclaimer
  have 0 h3 in main, so `h3color` is None there). No site file was at
  fault. Fixed the script (None-safe sets, dump raw results before the
  summary, `domcontentloaded` instead of `networkidle` — the footer
  Maps iframe stalls networkidle in this sandbox) and re-ran clean.
- First sticky scroll test was inconclusive (smooth `scroll-behavior`
  was still animating at measurement time). Re-ran with
  `behavior: 'instant'` + a short-viewport case; pin proven at 96px.

## 6. Open items (for the parent, not defects)
1. **Final wiring pass still needed:** the merged `lib/body-images.json`
   from the image workers has not arrived. Renderer + CSS are verified
   with a temp manifest (both paths), but the REAL manifest still needs
   its wiring verification pass (tags, sticky, overflow, Button 2) once
   it lands. Do NOT close this as verified until that pass runs.
2. **Homepage `/` body images:** DocPage never renders `/`. If the
   merged manifest contains `/` entries, they will be ignored until a
   homepage wiring pass is ordered (app/page.tsx is bespoke; its
   sections are not h2-block based, so `afterH2` has no meaning there).
3. **Contact-form em dashes** (`components/contact-form.tsx`, outside my
   editable set): notice "— calling is faster…" and sent text
   "Thanks — …" still carry em dashes. Header/footer are 0; the form is
   template chrome that needs either an edit-permission call or a
   follow-up worker.
4. **Button borders vs the naive check:** the `.btn` 2px full border is
   a designed button treatment (tel: links, not `<a href="/...">`).
   A future verifier that flags ANY border-bottom on ANY `<a>` will
   list the 4 buttons per page — that reading contradicts "keep the
   existing hero design and Button 2 behaviour", so the distinction is
   recorded here deliberately.
5. **Eyebrow 14px @≤360px** stays (hero chrome, exempt; raising it
   costs hero height against the Button 2 fold margin, currently
   70.8px @320 worst case).

## Files
- Changed: `app/globals.css`, `components/doc-page.tsx`,
  `app/not-found.tsx` (one comma).
- New QA: `qa/FINDINGS-design-css-2026-11-13.md` (this file),
  `qa/verify-design-css.py`, `qa/verify-design-css.json`,
  `qa/verify-design-css-raw.json`, `qa/verify-body-images.py`,
  `qa/contrast-design-2026-11-13.py`, `qa/render-design/*.png`
  (home/emergency/cottonwood desktop + 390; bodyimg-emergency-desktop).
- Temp `lib/body-images.json`: created for the present-path test, then
  DELETED. `lib/pages-data.json` untouched (sha above).
- `site.tsx` / `app/page.tsx`: read, no changes needed.
