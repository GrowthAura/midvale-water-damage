# CYCLE 1 — SCHEMA ADVANCEMENT FIX — Midvale UT — 2026-11-13

Implementer: Cycle 1 schema-advancement implementer (fix-only).
Scope: `lib/schema.ts`, `components/doc-page.tsx`, `app/page.tsx` ONLY.
Local only — no push, no deploy, no token, no DNS. **No `npm run export`
run** (the coordinator runs the single fresh export after all fix
workers report).
Data gate: `lib/pages-data.json` sha256
`21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` —
**UNCHANGED** (verified before and after the edits).

Source: auditor's candidates in `qa/opt1-schema.md` / `qa/opt1-schema.json`
(current state at audit: 178 blocks, PROBLEMS 0).

## Counts before → after

| Type (top-level) | Before | After | Delta |
|---|---|---|---|
| BreadcrumbList | 31 | 31 | 0 |
| FAQPage | 28 | 28 | 0 |
| WebPage | 31 | 29 | −2 (→ AboutPage / ContactPage) |
| AboutPage | 0 | 1 | +1 (C-2) |
| ContactPage | 0 | 1 | +1 (C-2) |
| ImageObject | 31 | 107 | +76 (C-3) |
| HowTo | 36 | 36 | 0 |
| Service | 19 | 19 | 0 |
| HomeAndConstructionBusiness | 1 | 1 | 0 |
| WebSite | 1 | 1 | 0 |
| **Total** | **178** | **254** | **+76** |

Nested (unchanged): Question 142, Answer 142, HowToStep 233, ListItem 64,
SpeakableSpecification 31, City 23, PostalAddress 23, inline
HomeAndConstructionBusiness providers 19.
Per-page counts: 31/31 match the auditor's baseline + the C-3 deltas
(homepage 7 → 26; the 19 body-image pages +3 each; all other pages
unchanged). Pure `{"@id"}` refs: 113 → **196** (+83, all C-1).
Unreferenced defined @ids: 114 → **107** = 31 WebPage page-URL ids
(nothing needs to point at a page's own URL) + 76 body/card ImageObject
ids (standalone definitions, exactly as C-3 specifies — no linking
property exists for them; the hero IS linked via `primaryImageOfPage`).
`#faq` (28), `#service` (19) and `#howto-N` (36) are now all referenced.

## C-1 — WebPage `mainEntity` linkage (strongest) — DONE

`lib/schema.ts`: `webPageLd()` takes an optional `mainEntityIds: string[]`
(full @id strings). Emitted as a single `{"@id": …}` object for one ref,
an array for several, and the key is omitted entirely when the list is
empty (the 3 legal pages — they have no FAQ/Service/HowTo node of their
own). Pure refs only — zero new claims.

`components/doc-page.tsx`: the ref list is built in fixed order — `#faq`
(if the page has FAQs), `#service` (if a Service block exists), then the
page's `#howto-N` ids in document order (from the real `howToFromBlocks`
output). `app/page.tsx`: homepage passes `[#faq, #howto-0]`.

Result: **83 mainEntity refs** — `#faq` 28, `#service` 19, `#howto-N` 36 —
on 28 of 31 pages (all but the 3 legal pages). Verified per page: the
emitted ref set equals the set computed independently from the page data
(FAQ presence + serviceKind + HowTo ids) on all 31 pages.

## C-2 — AboutPage / ContactPage subtypes — DONE

`lib/schema.ts`: `webPageLd()` takes an optional `pageType`
(`"WebPage" | "AboutPage" | "ContactPage"`, default `"WebPage"`).
`components/doc-page.tsx`: `/about` → `AboutPage`, `/contact` →
`ContactPage`, everything else `WebPage`. Subtype only — name,
description, url, `isPartOf`, breadcrumb, `primaryImageOfPage`,
`speakable` and (now) `mainEntity` all carry over unchanged.
Verified: AboutPage 1, ContactPage 1, WebPage 29.

## C-3 — ImageObject for the 76 non-hero images — DONE

`lib/schema.ts`: new `imageObject(route, suffix, img)` — same shape as
the hero blocks (`@id` = page URL + fragment, `contentUrl` = `SITE.base`
+ `src` (single prefix, the hero pattern), `caption` = alt verbatim),
no `representativeOfPage`, no width/height (only heroes carry measured
dimensions). New `cardImageObjects()` — the 19 homepage card images in
render order (16 service cards, then 3 location cards), `@id`
`#card-image-0..18` on the homepage URL.

`components/doc-page.tsx`: one block per body image, `@id`
`#body-image-N` in manifest order, built from the same validated
`BODY_IMAGES` list the `<img>` tags render from (so a manifest entry
that fails validation gets neither a tag nor a block). `app/page.tsx`:
the 19 card blocks render after the homepage HowTo.

Result: **+76 ImageObject blocks** (57 body + 19 cards), ImageObject
31 → 107. Verified: 57/57 body entries valid (19 routes × 3, distinct
files, non-empty alts, `afterH2` ascending per route so manifest order ==
render order); 19/19 card files distinct from hero files; captions ==
alt verbatim 107/107; `contentUrl` == `SITE.base + src` 107/107; files
exist in `public/` 107/107. Live curl of the 76 new `contentUrl`s is
DEFERRED to after the coordinator's export (per the task brief — `out/`
is the pre-fix export; URL shape verified in code now).

Note for later: F1 (parallel worker) already resized the card files to
680×383 and body files to 800×450. The C-3 blocks carry no dimensions,
so they are unaffected — but if width/height is ever added to them, it
must be measured from the resized files, not the old 1200px sizes.

## C-4 — width/height on the 31 hero ImageObjects — DONE

`lib/schema.ts`: `heroImageObject()` now carries `width: 1600,
height: 1066`. Measured by me with PIL on the site's own files:
**31/31 hero files are 1600×1066** — never the 1600×900 hero `<img>`
attributes (OBS-3). Verified: 31/31 emitted hero blocks carry
width 1600 / height 1066.

**CAVEAT (F2 interaction, for the coordinator):** F2 (parallel worker)
replaces 3 hero files (`disclaimer`, `upstairs-unit-leak-who-pays-utah`,
`water-damage-repair`). The 1600×1066 values are correct for the files
on disk at implementation time. If a replacement file does not measure
1600×1066, its width/height must be re-measured and corrected — the
re-verifier must check hero dims per file after the fresh export (this
is noted in a code comment at `lib/schema.ts` heroImageObject).

## C-5 — DOM ids matching fragment @ids — PARTIALLY DONE (2 of 4, see block)

Implemented (pure `id` attributes on existing elements, no visual or
content change):

- `#service` — `components/doc-page.tsx`: the `<section
  class="page-body">` gets `id="service"` exactly on the 19 Service
  pages (the body section is the page's service content); no id on
  other pages.
- `#howto-N` — `components/doc-page.tsx`: each content `<ol>` that
  carries a HowTo gets `id="howto-N"`, from the new shared
  `howToIndexByBlock()` map in `lib/schema.ts` — the SAME map that
  generates the HowTo `@id`s, so DOM ids and LD ids cannot drift apart
  (verified: map size == HowTo count on every page; all 35 doc-page
  content `<ol>`s are HowTo `<ol>`s, no orphans). `app/page.tsx`: the
  homepage process `<ol class="steps">` gets `id="howto-0"` (matches the
  homepage HowTo `@id`).

**NOT implemented — blocked by this task's file scope:** `#breadcrumb`
and `#hero-image`. Both elements live in `components/site.tsx`, which
is OUTSIDE the three files I may edit:

- `#breadcrumb` — the `<nav class="breadcrumb">` is rendered by the
  `Breadcrumb` component in `components/site.tsx` (~line 330).
- `#hero-image` — the hero `<img>` is rendered by `PhotoHero` in
  `components/site.tsx` (~line 63).

Adding a wrapper `<div id="breadcrumb">` around the component in
`doc-page.tsx` would have completed `#breadcrumb` without touching
`site.tsx`, but that adds a DOM element — the task orders "visible-
neutral id attributes only", so I did not do it. `#hero-image` has no
equivalent workaround at all (the `<img>` is inside `PhotoHero`).
Exact follow-up for the coordinator: one-line edits in
`components/site.tsx` — `id="breadcrumb"` on the Breadcrumb `<nav>`,
`id="hero-image"` on the PhotoHero `<img>` (31 pages each). Until then
the JSON-LD identifiers remain valid without DOM ids (auditor OBS-2);
the rendered-DOM check for the implemented ids (`#service`,
`#howto-N`) still needs the coordinator's fresh export, since no
export was run in this task.

## C-6 — Homepage ItemList of services — SKIPPED (as briefed)

No `ItemList` added. Reasoning (auditor's, agreed): the 19 services are
already carried as 19 Service blocks plus the WebPage/Breadcrumb graph
plus the homepage cards themselves — an ItemList would restate names +
URLs that already exist on the page, with no new information. Verified:
no `ItemList` string in either edited component.

## HowTo refactor (needed for C-1 + C-5)

`howToFromBlocks()` was refactored to typed output (`HowToLd` /
`HowToStepLd`) and to run off the new shared `howToIndexByBlock()`
map. The emitted blocks are **byte-identical** to an independent
recomputation from the raw page data (35 doc-page HowTos, 227 steps +
homepage 6 = 233 steps, names = preceding h2 verbatim, step text =
`stripAnnotations` of the joined segments, bold-lead rule unchanged).
No HowTo value changed — only the plumbing around it.

## Validation (no export run — coordinator runs the single fresh export)

- `npx tsc --noEmit`: **clean** (exit 0). One error found and fixed
  during the work: `for...of` over a `Map` needs a higher target —
  switched to `Map.forEach` (insertion-ordered).
- Verifier: `/tmp/schema-verify/verify.js` — compiles the REAL
  `lib/schema.ts` + `lib/content.ts` + `lib/links.tsx` to CJS, assembles
  every page's block set the way DocPage/HomePage do, and checks it.
  **48/48 checks PASS** (machine-readable:
  `qa/opt1-fix-schema-verify.json`). Checks include: totals + per-type
  counts + per-page counts vs the auditor's baseline + deltas; 196 pure
  refs, 0 unresolved; no duplicate @id definitions per page; mainEntity
  exact per page (83 refs); subtypes; HowTo refactor byte-identical;
  captions == alt 107/107; contentUrl shape + files exist 107/107;
  forbidden keys 0 (same list as the auditor); 966 URL strings scanned
  — localhost 0, double-slash 0, doubled subpath 0, off-base 0 (only
  allowed: `schema.org` context + the footer `hasMap` URL); WebPage
  name/description/url verbatim 31/31; Service name/description/refs
  19/19.
- Verifier's own corrections, owned plainly: the first run
  double-counted the homepage (pages-data.json holds a 31st "/" TAB
  entry that DocPage never renders — the homepage is bespoke in
  `app/page.tsx`; the verifier now excludes it) and had 4 expectation
  bugs of mine (key-order string comparison; unreferenced set missing
  the 76 standalone image ids; homepage's 6 HowTo steps left out of
  the 233 total; doc-page `<ol>` count 35 vs total HowTo 36). All four
  were fixed in the VERIFIER — the implementation was unchanged by
  them, and the final run passes 48/48.
- Honest limits (same as the auditor's): no live validator exists in
  this VM — Google Rich Results Test needs the live URL after push.
  Rendered-DOM confirmation of the new `#service` / `#howto-N` ids and
  live curl of the 76 new `contentUrl`s both need the coordinator's
  fresh export + re-verification. No `npm run export` was run here.

## Files changed

- `lib/schema.ts` — `webPageLd` (mainEntity + pageType), `heroImageObject`
  (width/height), new `imageObject` + `cardImageObjects`,
  `howToIndexByBlock` + typed `howToFromBlocks`.
- `components/doc-page.tsx` — mainEntity refs + pageType wiring, body
  ImageObject blocks, `id="service"`, `id="howto-N"` on content `<ol>`s.
- `app/page.tsx` — homepage mainEntity refs, 19 card ImageObject
  blocks, `id="howto-0"` on the process `<ol>`.
- `qa/opt1-fix-schema-verify.json` — machine-readable verification
  results (48 checks). `lib/pages-data.json` untouched (sha unchanged).
  No other file modified by this task.
