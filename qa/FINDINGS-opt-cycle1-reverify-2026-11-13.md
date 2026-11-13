# CYCLE 1 INDEPENDENT RE-VERIFICATION — Midvale UT — 2026-11-13

**Verifier:** independent re-verifier (did NOT do the audits or the fixes). Fresh reads only — nothing taken from worker/coordinator reports on trust.
**Scope:** `~/workspace/midvale-water-damage/`, existing `out/` served on `/midvale-water-damage/` (port 8410, `qa/linkfix-serve.py` copied to `/tmp`). No `npm run export` re-run, no push/deploy/token/DNS, no MEMORY.md edits.
**Data gate:** `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — **MATCHES, verified before and after all checks** (re-checked at the end; Cycle 2 srcset work was running in the same dir in parallel — the 4 new-image shas and all weights re-verified identical at the end).

## VERDICT: READY FOR CYCLE 1 CLOSE — PROBLEMS 0 (P1 0 / P2 0 / P3 0)

Every Cycle 1 fix reproduced fresh. Three probe artifacts of my own were found, investigated, and adjudicated as non-defects (see §7) — no defect was invented and no pass was assumed. Carried observations (not problems): mobile hero crop known limitation, breadcrumb 24px accepted, footer Google Maps embed unverifiable in this VM.

## 1. IMAGES — resize (F1) — PASS

PIL on every file (107/107), exiftool per file (EXIF/XMP/ICC groups only).

| Set | Files | Dims | Weight |
|---|---|---|---|
| Heroes | 31 | 1600×1066, 0 bad | 3,721,012 B |
| Cards | 19 | 680×383, 0 bad | 633,910 B (~634 KB) |
| Body | 57 | 800×450, 0 bad | 2,833,532 B (~2.83 MB) |
| **All** | **107** | | **7,188,454 B (~7.19 MB)** |

- EXIF/XMP/ICC: **0 on all 107** (first pass of my own script also flagged filesystem tags `FileSize`/`VP8Version` and exiftool-computed `Composite:ImageSize` — my filter bug, not metadata; corrected filter = EXIF/XMP/ICC_Profile/IFD0/GPS/MakerNotes groups only → 0).
- Quality — 6 heaviest files viewed full-size by me: `body/magna-ut-1.webp` (145,698 B), `body/mold-remediation-3.webp` (95,264 B), `body/window-well-flooding-3.webp` (90,154 B), `body/storm-flood-damage-1.webp` (89,322 B), `body/swamp-cooler-leak-water-damage-2.webp` (88,620 B), `body/cottonwood-heights-ut-2.webp` (85,596 B). All sharp — detail intact (mold staining, corrugated metal + droplets, flooded-street reflections, roof cooler + desert hills, aerial city + snow mountains), no blocking or smearing. PASS.

## 2. IMAGES — 3 new heroes + 1 body swap (F2) — PASS (viewed full-size by me)

| File | Alt (kept) | My viewed verdict |
|---|---|---|
| `heroes/disclaimer.webp` (1600×1066, 123,354 B, sha `3443f783…`) | "Technician inspecting a water-damaged wall with a moisture meter in a dark room" | Technician kneeling, pin-type moisture meter pressed to a severely stained/peeling wall, wet floor, tool belt, dark room — matches exactly. Photorealistic. Generated (honestly labelled by the worker; not a real job photo). |
| `heroes/upstairs-unit-leak-who-pays-utah.webp` (1600×1066, 116,246 B, sha `b52193f6…`) | "Water dripping from an apartment ceiling into the unit below in Midvale" | Water streaming/dripping from a large brown-stained peeling ceiling into the furnished living room below (sofa + coffee table getting wet), daylight through windows — matches exactly. Photorealistic. Generated (honestly labelled). |
| `heroes/water-damage-repair.webp` (1600×1066, 109,092 B, sha `b4d6e070…`) | "Newly rebuilt room in a Midvale home, fresh drywall and trim" | Renovated living room, fresh light-gray walls, white crown molding, hardwood floors — matches exactly. Real Pexels photo 40701216 (Akron, Ohio home — the alt's "Midvale home" is stock-photo attribution, as the worker's report itself notes; alt kept verbatim per task). |
| `body/magna-ut-1.webp` (800×450, 145,698 B, sha `787af0bd…`) | "Aerial view of a Utah home surrounded by vibrant autumn trees" | Aerial drone shot of a Utah home amid red/orange maples, blue spruce and pines — matches exactly. Real Pexels photo 5587966 (Woodland Hills, UT). |

**Reuse re-check (my own script `qa/reverify-reuse.py`, fresh disk reads):** corpus 2,268 image files across 34 site dirs (every `public/images/` + `images/`). md5 hits: **0 for all 4**. Closest aHash8: disclaimer 4, upstairs 10, water-damage-repair 12, magna 16. Pexels-ID grep for `40701216` and `5587966` across all `*/qa/IMAGE-LOG*.md` + `CARD-IMAGE-LOG*.md`: **0 hits**; no non-Midvale `.md` in the workspace mentions `40701216`.
- **Adjudication (viewed full-size by me):** the disclaimer's aHash8=4 flag is Plano 3 `wet-tile-9376351.webp` (three size variants) — a black-and-white photo of wet patterned floor tiles with a palm-frond shadow. Completely different subject from the technician-with-meter image; aHash16=43 confirms different. The aHash8 similarity is a dark-tone coincidence. **DIFFERENT, not a reuse. CLEAR.** The other three closest matches are all aHash8 ≥ 10 with aHash16 58–89 — clearly different photos, no adjudication needed. **All 4: reuse nets CLEAR.**

## 3. IMAGES — alt rewrites — PASS (photos viewed full-size by me)

- `cards/burst-pipe-water-damage`: new alt "Split copper pipe spraying water inside an opened wall cavity with wet wooden studs" present in `lib/content.ts`; old alt gone. Photo: split copper pipe spraying water inside an opened wall cavity with wet studs and torn drywall — no ice, no crawl space. **Exact.**
- `body/cottonwood-heights-ut-3`: new alt "Snowy city rooftops in the Salt Lake Valley with snow-capped mountains under low cloud" present in `lib/body-images.json` (entry verified); old alt gone. Photo: elevated view over snowy city rooftops with snow-capped mountains under low cloud — no street visible. **Exact.**

## 4. SCHEMA — 254 blocks — PASS

Top-level `@type` counts (one per JSON-LD block, fresh parse of `out/`): BreadcrumbList **31**, FAQPage **28**, WebPage **29**, AboutPage **1**, ContactPage **1**, ImageObject **107**, HowTo **36**, Service **19**, HomeAndConstructionBusiness **1**, WebSite **1** — **total 254, exactly as specified**. Nested: Question 142, Answer 142, HowToStep 233, ListItem 64, SpeakableSpecification 31, City 23, PostalAddress 23, inline providers 19.
- Parse errors: **0** (all JSON-LD blocks parse on all 31 pages).
- `@id` refs: resolve site-wide — the only per-page "unresolved" ref was `#website`, which is defined once on the homepage and validly referenced from all 30 other pages. Site-wide unresolved: **0**.
- `contentUrl`: **107/107 unique, all curl 200** via the local server (including all 76 new body/card URLs).
- Hero ImageObject width/height: **31/31 are 1600×1066** (matches PIL-measured files).
- DOM ids: `#breadcrumb` **30/31** (homepage has no breadcrumb nav by design — no element to hang it on), `#hero-image` **31/31**, `#service` **19/19**, `#howto-N` present on exactly the 25 pages that have HowTo blocks (36 blocks = 36 ids; 6 pages have no HowTo: contact, south-salt-lake, privacy, terms, disclaimer, basement-flooding-spring-snowmelt) — **0 mismatches between HowTo block count and DOM ids per page**.
- Honest trace (spot-checked vs `lib/pages-data.json`): FAQPage questions + answers verbatim on `/`, `/emergency-water-extraction`, `/mold-remediation` (6/6, 6/6, 5/5); Service name/description taken from doc intro text; HomeAndConstructionBusiness telephone `+13853373560` = doc phone (385) 337-3560; BreadcrumbList structure correct; WebSite `inLanguage: en-US`. **0 invented claims found in the sample.**

## 5. UI/UX — card echo fix + 48px targets + hero attrs — PASS (rendered + viewed by me)

- Homepage @1440 (screenshot `qa/reverify-home-1440-cards.png` viewed): each card ends in its own copper-dark bold CTA line with `→` ("Emergency Water Extraction →", etc.), pinned to the card bottom — reads as a distinct link affordance, **not** duplicated prose. @390 (screenshot viewed): same, single column, clean.
- CTA texts: **19/19 match the `anchor:` strings in `lib/content.ts` exactly** (sorted-set equality, arrow stripped). Computed style identical on all 19: `rgb(157, 84, 24)`, weight 700, 18px, `display: block`, `<p class="card-cta">`.
- Grid: @1440 services **4 columns, rows 4/4/4/4** (16 cards); locations **3 columns, 1 row of 3**; @390/@320 single column. (My first probe used wrong selectors and returned 0 cards — corrected to `#services article.card` / `#areas article.card` and re-measured.)
- Logo link: **48px tall @1440 (288×48), @390 (342×48), @320** — verified in the rendered DOM at all three widths.
- Radio labels: **Yes/No/Not sure all 48px**; form still 6 fields (name, phone, address, what-happened, water-running radios, best-time) + submit **"[Send My Request]" verbatim**.
- Hero `<img>` attrs: **1600×1066 on 31/31** in `out/`; 0 `height="900"` left.

## 6. REGRESSION (full, fresh) — PASS

| Check | Result |
|---|---|
| Fullness | 31/31 FULL — visible main words min 312/page (rendered DOM); no EMPTY/THIN page |
| Verbatim | **0 missing** — segment-level check, 3,040 unique doc segments (h1/intro/blocks incl. list items + table headers/cells/FAQ q+a, link annotations stripped) all present verbatim in visible main text. (My first token-multiset attempt reported 82 then ~1,900 "missing" tokens — two method bugs of mine: link-annotation path tokens counted as doc words, and FAQ content double-counted via blocks + faqs list. The segment-substring method, which matches the prior verifiers' approach, gives 0. The raw data was re-checked, not assumed.) |
| FAQ | **142/142 visible at load + 142/142 in schema** (rendered DOM, all 3 viewports; 0 closed `<details>`) |
| Tables | **43/43 rendered** (matches doc count per page) |
| Links | **0 broken, 0 self-links, 0 orphans** — every internal href curls 200 via the local server; no page links to itself in body; every route is linked from somewhere on the site (header/footer included) |
| Visible paren | 0 link annotations `(/path/)` in visible main text on 31/31. One non-defect noted: `/contact` shows "(Yes / No / Not sure)" — form radio-label copy, not an annotation. |
| localhost | 1 occurrence in all of `out/` — inside `polyfills-*.js` (Next.js router error string), 0 in any HTML/TXT/XML/CSS. Adjudicated non-defect (same as prior rounds). |
| Double-slash | **0** (`//midvale-water-damage` in `out/`) |
| Sitemap | **31 locs**, set == routes exactly, **31/31 curl 200** |
| 404 | Returns **404**, robots **noindex**; exactly 1 noindex page site-wide |
| Robots meta | **31/31 exactly 1 `index, follow`** |
| Button 2 scroll-0 | **31/31 @320 (worst bottom 552px ≤ 568px gate) and 31/31 @390 (worst 773px ≤ 844px gate)**. Note: the gate viewport heights are 320×568 and 390×844 (my first pass used a 700px-high viewport and flagged five @390 "fold" failures at 742–773px — wrong threshold; re-measured against the correct 844px gate, all pass; worst values reproduce the fix report's 552.2 / 773.1 exactly). |
| Overflow | **0 @320 / @390 / @1440** (93 measurements) |
| Console | **0 errors** on 93 page loads (after clean re-measures; see §7) |
| Images render | **107/107** at all 3 viewports (see §7 for the lazy-load adjudication) |
| Real-click nav | **3/3 keep subpath**: homepage card → `/burst-pipe-water-damage` (H1 correct); logo → home; footer link → `/mold-remediation` (URL + H1 correct, confirmed in a focused re-check after a timing race in my first attempt read the URL before the router updated) |
| Hidden words in `<main>` | **0** at all 3 viewports (rendered DOM, script/style excluded) |
| FAQ answers visible at load | **142/142** (see above) |

## 7. Probe artifacts found and adjudicated (mine, not site defects)

1. **JSON-LD counted as "hidden words"** — my first hidden-words probe counted `<script type="application/ld+json">` text inside `<main>` (display:none by nature) as ~500 hidden words/page. Fixed the probe to exclude script/style/noscript/template; re-measured: **0 hidden words**.
2. **Lazy-load image flags** — on @320 the first re-run flagged 3 bottom-row homepage card images (nw=0); a focused re-check flagged the 3 location cards instead. Cause: `loading="lazy"` cards far below the fold had not loaded at measurement time (homepage is 30,625px tall @320). Proof: slow scroll to the true bottom → **all 20 homepage images load, 0 bad**; the 3 files serve HTTP 200; 0 failed requests. Same class as the prior rounds' adjudicated lazy flags. Not a defect.
3. **Browser resource exhaustion (environment)** — the VM repeatedly killed Chromium mid-run (`TargetClosedError`, `ERR_INSUFFICIENT_RESOURCES`, `Page crashed`, "Failed to fetch RSC payload" for `*.txt?_rsc=` prefetches). All such failures were re-run cleanly (single-process launch, resumable per-viewport scripts, per-route partial saves). Proof the RSC failures are noise: the payload `.txt` files curl **200**; clean re-measures show **0 console errors** on all 93 loads. The footer Google Maps embed also cannot load in this VM (no google.com egress) — carried P3 environment note, needs a real-network eyeball after push.
4. **My own script bugs, owned plainly** — (a) metadata filter initially flagged filesystem/exiftool-computed tags as "leftover metadata" (corrected to EXIF/XMP/ICC groups only → 0); (b) verbatim token method double-counted FAQ content and counted annotation paths (corrected to the segment method → 0 missing); (c) render script registered route handlers per-route and used a 700px fold threshold (corrected; Button 2 re-measured against 568/844); (d) one click script raced the router (re-checked focused → URL + H1 correct); (e) my first card-grid probe used wrong class names (corrected selectors → 4/4/4/4 measured). None of these touched the site; all were re-measured clean.

## 8. Carried observations (not problems)

- **O-1 Mobile hero crop (audit P2-20, known limitation):** fixer measured visible fraction @390 min 21.0% / max 53.2% / mean 26.9%; no clean CSS fix exists (content-height hero box); dark shade makes the photo an atmospheric backdrop on mobile. No fix was claimed; recorded as a known limitation, not blocking.
- **O-2 Breadcrumb links 24px** left as-is by design (WCAG 2.2 AA 24px minimum, accepted).
- **O-3 Water-damage-repair hero alt** says "in a Midvale home" for a real Pexels photo taken in Akron, Ohio — stock-photo attribution, alt kept verbatim per task. Same class as all stock photos on the site.
- **O-4 Card `<img>` attrs** are `width="800" height="450"` while files are 680×383 — aspect ratios match (1.777 vs 1.776), no distortion observed; hero attrs (the gated check) are exact.
- **O-5 Footer Google Maps embed** fails in this VM only (no google.com egress); needs a real-network eyeball after push.

## Evidence files (all under `~/workspace/midvale-water-damage/qa/`)

- `reverify-static.py` / `reverify-static.json` — dims, weights, metadata, schema counts, @id resolution, contentUrl curls, DOM ids, hero attrs, sitemap/robots/404, canonicals/H1
- `reverify-visible.py` / `reverify-visible.json` — visible-text fullness, tables, links (broken/self/orphans), visible paren
- `reverify-segments.py` / `reverify-segments.json` — 3,040-segment verbatim check (0 missing)
- `reverify-reuse.py` / `reverify-reuse.json` — fresh-disk reuse net, 2,268-file corpus (md5 0, closest aHash8 4/10/12/16)
- `reverify-render-320.json`, `reverify-render-390.json`, `reverify-render-1440.json` — per-route render: overflow, Button 2, console, failed requests, images, hidden words, FAQ visibility
- `reverify-home-1440.json`, `reverify-home-390.json`, `reverify-home-320.json` — grid, CTA texts/styles, logo 48px
- `reverify-contact-radios.json`, `reverify-contact-clicks.json` — radio 48px, form fields, submit verbatim, real clicks
- `reverify-home-1440-cards.png`, `reverify-home-390-cards.png` — card/CTA screenshots viewed by me
- `FINDINGS-opt-cycle1-reverify-2026-11-13.md` (this file)

## Verdict restated

**PROBLEMS 0 — READY FOR CYCLE 1 CLOSE.** All Cycle 1 fixes verified fresh: resize exact (19×680×383, 57×800×450, weights 634 KB / 2.83 MB / 7.19 MB, metadata 0, quality sharp); 3 heroes + magna swap match their alts on viewed pixels with reuse nets clear; both alt rewrites exact; schema 254 blocks exact with 0 parse errors, refs resolving, 107/107 contentUrls 200; card CTA distinct with 19/19 verbatim texts; logo/radio 48px; full regression clean (31/31 FULL, verbatim 0, FAQ 142/142, tables 43/43, links 0 broken/orphans/self, Button 2 31/31 @320/@390, overflow 0, console 0, images 107/107, clicks keep subpath).
