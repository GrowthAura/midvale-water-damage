# CYCLE 1 — UI/UX + CSS FIX — Midvale UT — 2026-11-13

Implementer: Cycle 1 UI/UX + CSS fixer (F4).
Scope: `components/site.tsx`, `app/page.tsx`, `app/globals.css` ONLY.
Local only — no push, no deploy, no token, no DNS, no MEMORY.md edits.
Exports run by me (the only active worker): 4 fresh exports, all
`NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`
(no trailing slash), final export exit 0. Served locally on
`/midvale-water-damage/` (port 8401) for visual verification.
Data gate: `lib/pages-data.json` sha256
`21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` —
**UNCHANGED** (verified before the first edit and after the final export).

Sources: `qa/opt1-uiux.md` (P2-1 + P3-1/2/3), `qa/opt1-images-heroes-cards.md`
(P2-20 mobile hero crop, P3-3 hero attrs), `qa/opt1-fix-schema.md` (C-5 leftover).

## Verdict: ALL 7 FIXES DONE — 1 KNOWN LIMITATION RECORDED, 0 REGRESSIONS

| # | Fix | Result |
|---|---|---|
| 1 | P2-1 homepage card title echo (design) | DONE — 19/19 cards, anchor verbatim, screenshots before/after |
| 2 | C-5 `#breadcrumb` + `#hero-image` DOM ids | DONE — 30/31 + 31/31 (see note on the homepage) |
| 3 | P3-1 brand logo link 43px → 48px | DONE — 48px @1440/390/320, no layout break |
| 4 | P3-2 radio option labels 32px → 48px | DONE — 48px, form still 6 fields + verbatim submit |
| 5 | P3-3 breadcrumb links 24px | LEFT AS-IS (accepted — passes WCAG 24px minimum) |
| 6 | P2 mobile hero crop @390 | KNOWN LIMITATION — measured, no clean CSS fix (see §6) |
| 7 | Hero width/height attrs 1600×900 → 1600×1066 | DONE — 31/31, files PIL-verified 1600×1066 |

## 1. P2-1 — Card title echo → distinct CTA line (DONE)

**Change** (`app/page.tsx` + `app/globals.css`): the anchor phrase is no
longer the tail of the summary paragraph. Each card now renders its own
`<p class="card-cta">` under the summary — copper-dark (`#9d5418`,
~5.7:1 on white, AA), 700 weight, 18px, with a `→` bound to the last
word by a non-breaking space. The summary `<p>` keeps `flex: 1`, the CTA
takes `flex: 0 0 auto`, so every card in a row shows its CTA pinned to
the card bottom; hover deepens it to pine. The arrow is a separate
`aria-hidden` span — screen readers hear the anchor text only.

**Verbatim proof:** the 19 rendered CTA texts equal the 19 `anchor:`
strings in `lib/content.ts` exactly (checked programmatically: 0 missing,
0 extra). No anchor word was removed, reworded, or reordered. The only
added characters are 19 `→` glyphs (not words) + 19 `&nbsp;` joiners.

**Measured:** 19/19 `.card-cta` present; computed style identical on all
19 — `rgb(157, 84, 24)`, weight 700, 18px, `display: block`. Card grid
unchanged: 4 columns @1440, service rows 4/4/4/4, location row 3,
uniform card widths; CTA bottom spread per row **0px** (perfectly
aligned). Page height delta vs before: desktop +80px (4 rows × ~20px —
one CTA line per row, minus the anchor text leaving the summaries),
mobile +27px (the anchor leaving each summary roughly cancels the CTA
line it gains).

**Visual evidence:** `qa/opt1-fix-uiux/before/home-desktop-cards.png` vs
`qa/opt1-fix-uiux/after/home-desktop-cards.png` (1440) and
`home-m390-cards.png` (390). Before: every card ends in plain body text
repeating its title. After: the same words sit on their own copper
semibold line with an arrow — reads as a link/CTA, not duplicated prose.

**Refinement owned:** the first version used a normal space before `→`,
and on 5 cards the arrow wrapped onto its own line ("Window Well
Flooding" / "→"). Fixed with `&nbsp;→` — the arrow now always travels
with the last word ("Flooding →"). Re-exported + re-verified after the
change.

## 2. C-5 — `#breadcrumb` + `#hero-image` DOM ids (DONE)

**Change** (`components/site.tsx`): `id="breadcrumb"` on the Breadcrumb
`<nav>`, `id="hero-image"` on the PhotoHero `<img>` — the exact one-line
edits from `qa/opt1-fix-schema.md`. Pure id attributes; no visual or
content change.

**Measured on the fresh export:** `#hero-image` **31/31**;
`#breadcrumb` **30/31**. The one missing page is `/` — the homepage
never renders a Breadcrumb component (it IS Home; no breadcrumb nav
exists there by design), so there is no `<nav>` to hang the id on.
Adding a breadcrumb to the homepage would be a design change, not a
one-line id edit, so it was not done. The homepage's BreadcrumbList
`@id` (`.../#breadcrumb`) still exists in JSON-LD — a valid identifier
without a DOM anchor, exactly the state the schema auditor recorded as
acceptable (OBS-2). JSON-LD fragment presence: `#breadcrumb` 31/31,
`#hero-image` 31/31. Also confirmed in the same pass: `#service` 19/19,
`#howto-N` present on 25/31 pages (the other 6 — 3 legal + about +
contact + guide — have no HowTo, as F3 documented).

## 3. P3-1 — Brand logo link 43px → 48px (DONE)

**Change** (`app/globals.css`): `.brand { min-height: 48px; }`.
Header-inner is 72px, so no layout change at desktop.

**Measured:** `a.brand` **48px tall at 1440 (287.9×48), 390 (342×48)
and 320 (272×48)** — was 43px at all three widths.

**Regression I caused, owned + fixed:** the 48px brand lengthened the
sticky header at ≤360px (brand row 36→48px), which pushed the worst
Button 2 bottom at 320×568 from 556.2px to **568.2px — 0.2px past the
fold** on `/condo-apartment-water-damage`. My first compensation (hero
bottom padding 40→28px) did NOT move Button 2 at all — bottom padding
sits below the buttons; re-measured 568.2px, unchanged. The correct
repayment is inside the header: at ≤360px the header's two rows were
24px apart (`gap`), so `row-gap: 8px` on `.header-inner` repays 16px.
Hero bottom padding reverted to 40px. Final re-measurement: Button 2
worst @320 = **552.2px** (15.8px headroom — better than the 556.2px
before this task). The wrong-compensation attempt is documented in the
CSS comment so nobody repeats it.

## 4. P3-2 — Contact-form radio labels 32px → 48px (DONE)

**Change** (`app/globals.css`): `.contact-form .radio-row label {
min-height: 48px; }`. The native radio stays centred by `align-items`.

**Measured:** Yes 57×**48**, No 53×**48**, Not sure 104×**48** (were
57/53/104×32). Form untouched otherwise: 6 doc fields in order (Name,
Phone number, Address or ZIP code, What happened (short description),
Is the water still running? Yes/No/Not sure, Best time to call),
submit **"[Send My Request]" verbatim**. Screenshot:
`qa/opt1-fix-uiux/after/contact-desktop-form.png`.

## 5. P3-3 — Breadcrumb links 24px (LEFT AS-IS, accepted)

No change. Inline text navigation, 24px tall, meets the WCAG 2.2 AA
24px minimum exactly. Enlarging inline breadcrumb text would change
the hero stack on every inner page (breadcrumb wraps are already the
tightest part of the 320px fold budget). Recorded as accepted, as briefed.

## 6. P2 mobile hero crop — KNOWN LIMITATION (measured, no CSS fix)

**My own measurement first** (fresh export, 31 routes @390, real
`.hero-img` boxes — not the auditor's number, not the brief's number):

- Hero box heights @390: **488–1239px** (content-driven; tallest
  `/condo-apartment-water-damage` 1239px, shortest the 3 legal pages
  489px).
- True visible fraction of the 1600px-wide image: **min 21.0%, max
  53.2%, mean 26.9%**. Only the 3 short legal heroes exceed 30%
  (53.2%); 28/31 pages show **≤28.6%**.
- The auditor's "~24%" is close to the typical value (it is the scale
  factor for the tallest heroes, which happens to ≈ the visible fraction
  there). The brief's "~53%" is only the maximum (the 3 legal pages).
  Neither single number describes the site — the distribution above does.
- Wide scenes: `/` 24.2% (h 1072), `/about` 24.6% (1058),
  Cottonwood Heights 22.9% (1133), Magna 22.3% (1165), South Salt Lake
  22.1% (1176).

**Why no fix was applied:** the crop is caused by `object-fit: cover`
inside a content-height hero section — the box is tall because the H1 +
intro + stacked buttons + trust text are tall, not because of any
sizing rule. A CSS-only fix would have to either (a) shorten the hero
— impossible without hiding content (forbidden) or shrinking text
(the H1 30px floor and Button-2-above-fold gate forbid it), or (b)
letterbox the image (`contain`) — a 1600×1066 photo in a 390×1100 box
would render ~390×260 with ~400px dark bands top and bottom, worse
than the crop. `object-position` tuning changes which horizontal band
shows, not how much width is visible. Per-hero mobile crops would be
31 new image assets — out of scope for a CSS fixer. The only
height saving available (hero padding, ~30px) moves the visible
fraction by ~+0.6pp — not worth a layout touch.

**Mitigating facts (viewed, not assumed):** the hero photo sits under
a heavy dark shade (0.74–0.88 opacity) plus white text, so on mobile it
reads as an atmospheric backdrop, not an illustrative photo — the crop
does not destroy a subject the user can see. Centre-weighted heroes
(burst pipe, frozen pipe, mold) survive the crop; the wide scenes lose
their edges but keep their centre. Screenshots:
`qa/opt1-fix-uiux/after/*-m390-hero.png` (home, about, 3 locations).
Recorded as a known limitation with the measurements above; a real fix
needs per-hero mobile focal crops as new assets.

## 7. Hero width/height attrs 1600×900 → 1600×1066 (DONE)

**Change** (`components/site.tsx:63`): `height={900}` → `height={1066}`
on the PhotoHero `<img>` (same line as the `id="hero-image"` edit).

**Measured:** all 31 hero files re-verified with PIL on disk =
**1600×1066, 31/31** (including F2's 3 replacements — the C-4 caveat
is closed, no re-measure needed). Exported HTML: `width="1600"
height="1066"` on 31/31 hero imgs; **0 occurrences** of
`height="900"` anywhere in `out/**/*.html`. CSS
(`position: absolute; inset: 0; width/height: 100%`) still overrides
the box in practice, so no visible change — the reserved aspect ratio
is now factually correct.

## Re-verification (fresh export, exit 0, served on /midvale-water-damage/)

Script: `qa/opt1-fix-after.py` (Playwright, real Chromium) — raw data
`qa/opt1-fix-after.json`; baseline (pre-fix export) `qa/opt1-fix-baseline.py`
+ `qa/opt1-fix-baseline.json`.

| Gate | Before | After |
|---|---|---|
| Export exit code | 0 | **0** (4 exports run; final is the verified one) |
| `tsc --noEmit` | clean | **clean** |
| Data sha256 | 21c6e7f2… | **21c6e7f2… unchanged** |
| Button 2 scroll-0 @320 | 31/31, worst 556.2 | **31/31, worst 552.2** (fold 568) |
| Button 2 scroll-0 @390 | 31/31, worst 768.2 | **31/31, worst 773.1** (fold 844; +4.9 from brand growth, 70.9px headroom) |
| Overflow | 0 | **0 on 31/31** |
| Console errors | 0 | **0 on 31/31** |
| Card echo (P2-1) | 19/19 plain-text echo | **19/19 CTA lines, anchor verbatim** |
| Card grid @1440 | 4 cols, 4/4/4/4 | **unchanged: 4 cols, 4/4/4/4, loc 3** |
| Logo height | 43px @1440/390 | **48px @1440/390/320** |
| Radio labels | 32px | **48px** |
| `#breadcrumb` / `#hero-image` | 0 / 0 | **30/31 / 31/31** (see §2 note) |
| Hero attrs | 1600×900 | **1600×1066, 31/31** |
| Hero visible fraction @390 | 21.0–53.2%, mean 26.9% | **unchanged (no hero CSS change)** |
| Form | 6 fields, verbatim submit | **unchanged, verified** |
| Service pages before/after | — | **emergency + basement: desktop height delta 0px, m390 +5px** (brand growth only); no visual regression |

## Files changed (this task only)

- `components/site.tsx` — `id="hero-image"` + `height={1066}` on the
  hero `<img>`; `id="breadcrumb"` on the Breadcrumb `<nav>`.
- `app/page.tsx` — service + location cards: anchor phrase moved from
  the summary paragraph into its own `<p class="card-cta">` (+ `&nbsp;→`
  arrow span); no anchor word changed.
- `app/globals.css` — `.card-cta` rule (+ hover); `.brand` min-height
  48px; `.contact-form .radio-row label` min-height 48px;
  `@media (max-width: 360px)` `.header-inner` row-gap 8px (Button 2
  compensation, §3).
- `qa/opt1-fix-uiux.md` (this file), `qa/opt1-fix-baseline.py`,
  `qa/opt1-fix-baseline.json`, `qa/opt1-fix-after.py`,
  `qa/opt1-fix-after.json`, `qa/opt1-fix-uiux/before/` +
  `qa/opt1-fix-uiux/after/` (screenshots).

No push, no deploy, no token, no DNS. Nothing else modified by this task.
