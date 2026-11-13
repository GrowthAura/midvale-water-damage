# FINDINGS — Midvale UT SEO Fix 2 (2026-11-13)

Fix agent for the 3 NEW P3s from SEO audit 2 (qa/FINDINGS-seo-audit2-2026-11-13.md,
verdict SHIPPABLE, P1 0 / P2 0 / P3 5). Stage 3 of the 6-hour watchdog chain.
Local only. No push/deploy/token/DNS. Data `lib/pages-data.json` sha256
`21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` verified
unchanged before, during and after (only source files edited, never data).

## VERDICT: PROBLEMS 0 — READY FOR STAGE 4 (advanced schema)

All 3 P3s fixed and re-verified fresh on a new export. No new problems found.

## FIX 1 — P3-1: 404.html duplicate noindex (ROOT CAUSE FOUND + FIXED)

**Before (audit 2):** `out/404.html` carried TWO `<meta name="robots"
content="noindex"/>` tags in `<head>` — one before `<title>`, one after
`<meta name="description">`. The page was correctly noindexed; the
duplication was a nit, not a leak.

**Root cause (traced, not guessed):** the two tags had DIFFERENT sources.
- Tag #1 (before `<title>`, outside the metadata block) is **Next.js's
  automatic noindex for the not-found route** — the framework injects it
  for `/_not-found` unconditionally. It also appears in the RSC flight
  payload as `initialHead`.
- Tag #2 (after `<description>`, in the normal metadata slot — the same
  slot where `index, follow` renders on a normal page) was the **explicit
  `robots: "noindex"` in `app/not-found.tsx`** (added by the 10X fix, whose
  comment wrongly blamed "layout's index,follow + Next's auto noindex").
  Page-level metadata overrides the layout's robots, which is why no
  `index, follow` appeared on the old 404.

**Fix, step 1 (not enough on its own):** removed the explicit `robots`
from `app/not-found.tsx`. Re-export proved the framework tag survives on
its own — but it also exposed a second problem: with nothing overriding
it, the **layout's `robots: { index: true, follow: true }` leaked onto
the 404**, giving the page TWO conflicting robots tags (`noindex` +
`index, follow`). A page-level robots value always duplicates the
framework tag, so no page-level override can produce a single tag.

**Fix, step 2 (the real fix):** moved `robots` OUT of the root layout
and onto the page metadata that covers all 31 real routes:
- `app/layout.tsx` — `robots` key REMOVED (comment explains why).
- `app/page.tsx` — added `robots: { index: true, follow: true }`.
- `app/[slug]/page.tsx`, `app/locations/[slug]/page.tsx`,
  `app/resources/[slug]/page.tsx` — added the same to each
  `generateMetadata` return (22 + 3 + 5 routes).

**After (fresh export):**
- `out/404.html`: exactly **1** robots tag, `<meta name="robots"
  content="noindex"/>` (the framework's auto tag, before `<title>`).
  Served 404.html on the subpath mirror: same single tag. A request for
  a missing page returns HTTP 404.
- All **31/31** real pages: exactly **1** robots tag each, `index,
  follow` (audit 2's "index, follow on 31/31" pass preserved exactly).

## FIX 2 — P3-2: Cottonwood card alt (lib/content.ts:451)

**Photo viewed full-size first** (`public/images/cards/cottonwood-heights-ut.webp`,
1200x675): a winding two-lane canyon highway with cars, through steep
rocky slopes with autumn foliage (gold/orange/green), a small stream in
the canyon bottom. No homes, no snow. The old alt — "Bench homes below
snowy Wasatch canyons in Cottonwood Heights, Utah" — was copied from the
hero's alt and factually wrong for this photo.

**New alt (exact string):**
"Winding canyon highway with cars through steep rocky autumn slopes in Cottonwood Canyon, Utah"

Renders in `out/index.html` (1 occurrence in the `<img>` tag; the second
grep hit is the RSC flight payload copy of the same tag).

## FIX 3 — P3-3: Basement-snowmelt hero alt (lib/content.ts:431)

**Photo viewed full-size first**
(`public/images/heroes/basement-flooding-spring-snowmelt-utah.webp`,
1600x1066): exterior of a house — beige siding, concrete foundation, a
white downspout discharging a stream of meltwater onto wet ground at the
foundation base, melting snow piles on both sides, muddy puddles, snowy
hills/mountains behind. No basement floor in frame. The old alt —
"Spring snowmelt water seeping across a Midvale basement floor" — was
wrong about the location (topic fit was right: snowmelt threatening a
basement).

**New alt (exact string):**
"Spring snowmelt water pooling at a home foundation as a downspout discharges, with melting snow piles and snowy hills behind"

Renders in `out/resources/basement-flooding-spring-snowmelt-utah.html`
(1 occurrence in the `<img>` tag; the second grep hit is the RSC flight
payload copy). Old alt: 0 occurrences anywhere in `out/`. Cottonwood old
alt: 0 occurrences anywhere in `out/`.

Alt text lives in `lib/content.ts` (chrome, not doc content) — safe to
rewrite; both new alts describe only what is actually visible in the
photos. No place claim is invented: "Cottonwood Canyon, Utah" is the
location page's own canyon; the snowmelt alt names no town.

## EXPORT + SERVE

- `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`
  (NO trailing slash — the fix-1 lesson), `npm run export` exit 0.
- Served `out/` on `/midvale-water-damage/` (port 8324,
  `qa/linkfix-serve.py`): homepage 200 + H1/phone confirmed, missing
  page returns HTTP 404, served `404.html` carries exactly 1 noindex.
- `/tmp/linkfix-serve.py` was missing again (VM replacement wiped /tmp)
  — restored from the persistent copy `qa/linkfix-serve.py` before the
  render run. That is an environment note, not a site defect.

## RE-VERIFICATION (fresh, on the new export)

**Static** (`qa/verify-linkfix.py` → `qa/verify-linkfix-static.json`):
- Fullness 31/31 FULL; missing words 0; segments missing 0, reordered 0.
- H1 1/page on 31/31 (h1_ok 31/31); title verbatim 31/31; meta
  verbatim 31/31.
- FAQ data 142 = visible 142 = JSON-LD 142, 0 mismatch pages.
- Tables 43 data = 43 rendered, 0 cell mismatch.
- Links: body 143 + card 19 = **162 intact**; self-links body 0;
  broken internal 0; unprefixed hrefs 0; orphans []; footer navs
  8/3/10/4; visible paren `(/.../)` in main text on 0 pages;
  JSON-LD parse errors 0.
- 0 localhost in HTML/XML/TXT. The single remaining `localhost` string
  in all of `out/` is the Next.js URL-parser polyfill chunk
  (`"localhost"===s.host`) — framework code, not a site URL (same
  adjudication as audit 2). Double-slash absolute URLs 0.
- **Static script's own "problems: 2" are verifier artifacts, NOT site
  defects:** `qa/verify-linkfix.py:536` hardcodes the expected sitemap /
  llms.txt URL set to `http://localhost:3000`. The actual sitemap has
  exactly 31 locs and llms.txt exactly 31 URLs, all on the Pages URL —
  the route sets match exactly, only the base differs, and the Pages
  base is the CORRECT behaviour (audit 2 P1-1 fix). Adjudicated, not
  a defect; the script was not edited.

**Render** (`qa/verify-linkfix-render.py`, Playwright Chromium, 31 routes
× 1440/390/320, served subpath → `qa/verify-linkfix-render.json`):
- **Render problems: 0** (script's own summary).
- Rendered-DOM paren `(/.../)`: 0 in body and main on all 93 loads.
- White screen 0; console errors 0; failed requests 0; overflow 0
  (overflow_px 0 on all 93 loads); H1 visible 31/31 × 3 viewports.
- Button 2 visible at scroll-0: 31/31 @320 (worst bottom **556.2px** vs
  568 fold — condo, 11.8px headroom, reproduces audit 2 exactly) and
  31/31 @390 (worst **768.2px** vs 844 fold — condo). Buttons equal on
  all pages (0 unequal). Link decoration: body-link `none`, card-wrap
  `none`.
- Real-click nav: 7/7 land correctly (card→emergency, logo→home,
  body link→emergency-contacts, inner body link→hardwood,
  footer→mold, header→sewage, breadcrumb→home), subpath kept on all
  except the known bare-root string-check artifact on breadcrumb→home
  (URL is the served subpath root; H1 correct — same adjudication as
  the design round). Desktop click errors [].
- Mobile nav: menu opens (`flex|main-nav open|aria:true`), scroll lock
  works (`hidden|fixed`). The script's one recorded error — a 30s
  timeout waiting for `#main-nav a[href*='burst-pipe-water-damage']` —
  is the same known verifier-expectation artifact as the design round:
  `#main-nav` carries only 3 links by design on desktop AND mobile
  (full nav lives in footer + cards + body links); not a site defect.
- Homepage card geometry: 19/19 cards, images 16:9 (ratio 1.778),
  link decoration `none`, 1 link per card (nested_a 1).

## FILES CHANGED (this fix only)

- `app/not-found.tsx` — explicit `robots: "noindex"` removed + comment
  corrected (framework auto noindex is the single source).
- `app/layout.tsx` — `robots` key removed + comment (why it moved).
- `app/page.tsx`, `app/[slug]/page.tsx`,
  `app/locations/[slug]/page.tsx`, `app/resources/[slug]/page.tsx` —
  `robots: { index: true, follow: true }` added to page metadata.
- `lib/content.ts` — 2 alt rewrites only (snowmelt hero, cottonwood
  card). No doc content touched; `lib/pages-data.json` sha256 unchanged.

## OWN ERRORS OWNED

- First fix attempt (remove explicit robots only) traded the duplicate
  noindex for a conflicting `noindex` + `index, follow` pair — caught
  by my own re-export check before any verification run, fixed
  properly by moving robots to page-level metadata. No bad build was
  ever presented as fixed.
- `pkill -f "linkfix-serve.py 8324"` matched my own shell's command
  line and SIGTERMed it (exit 15, harmless — the tail output had
  already printed). Server shutdown was then confirmed by port check
  (8324 free). Older serve processes on 8313/8314/8342 belong to prior
  stages and were left alone.
- Two aggregation scripts of mine failed on first run (wrong JSON key
  guesses: `h1`/`faq` vs `h1_ok`/`faq_data_count`; `tables_data` is a
  list) — fixed and re-run; the numbers above come from the corrected
  runs, not the failed ones.

## OPEN (not mine — carried, unchanged)

- P3-4 homepage single-item BreadcrumbList; P3-5 homepage twice in
  `<main>` on 3 location pages (breadcrumb nav, verified non-issue);
  P3-1 legal titles + P3-5 12 over-cap anchors (verbatim wins). All as
  recorded in audit 2. Maps embed still needs a real-network eyeball
  after push (sandbox-blocked google.com egress).
- Stage 4 (advanced schema) can start on this build. No push/deploy/
  token/DNS touched by this fix.
