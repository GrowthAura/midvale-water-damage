# FINDINGS — Midvale UT Fill + 19px Round (2026-11-13)

Coordinator: fill + polish coordinator (spawned 2026-11-13 ~05:19 PKT).
Order: user 2026-11-13 ~05:18 PKT — every service/location page 3–4 photos relevant to
that service + area; if no fitting photo exists, MAKE it (generate, inspired by that
service/area), then strip its metadata; text one side, photo the other, whole page;
body text 19px minimum except headings; every page, every section best ever.
Local only. Re-push only on his word + token (parent pushes).

Builds on the 10x-verified design build — the design round was NOT redone.

## Workers (2, parallel, both DONE and coordinator-verified against files)
- Image worker: 7 images (6 empty-slot fills + B&W commercial-3 replacement).
  Findings: qa/images-fill.json (7 entries). Scratch qa/gen-tmp/ deleted after conversion.
- Typography worker: 18px → 19px body copy in app/globals.css only.
  Findings: qa/FINDINGS-typo-19px-2026-11-13.md; script qa/typo-verify-19px.py.
- Independent verifier: fresh export + full re-verification + review pack regen.
  Findings: qa/FINDINGS-fill-19px-verify-2026-11-13.md.

## 1. Images — 6 empty slots filled + B&W commercial-3 replaced (all 7 GENERATED)
Quick Pexels check first per slot (as ordered): no fitting real photo exists for any
of the 7 slots. The only Pexels puddle photo found (7717858) is a concrete-floor
close-up already used on the Acworth site, so it was not used. Generation was
expected — the design round had already established no fitting photo for these
slots, and the Pexels colour search for commercial had already failed.

| # | File | Route / afterH2 (verified vs pages-data.json H2 order) | Fit (viewed at full size) |
|---|---|---|---|
| 1 | emergency-water-extraction-1.webp | /emergency-water-extraction, afterH2 1 "What Happens in the First 60 Minutes on Site", split | PASS — truck-mounted extraction unit, hoses into house, crew on flooded living-room floor; no legible text/logos |
| 2 | emergency-water-extraction-3.webp | /emergency-water-extraction, afterH2 3 "Can Wet Carpet and Pad Be Saved?", split | PASS — carpet lifted at edge, extractor vacuuming water, damp pad visible; glove print illegible |
| 3 | crawl-space-water-damage-1.webp | /crawl-space-water-damage, afterH2 1 "Signs Your Crawl Space Is Wet", split | PASS — low crawl space, wooden joists, damp dirt, flashlit puddle; no text |
| 4 | crawl-space-water-damage-2.webp | /crawl-space-water-damage, afterH2 2 "What Floods Midvale Crawl Spaces", split | PASS — white pipes along joists, drip pooling on damp dirt, wooden piers; tiny pipe print illegible |
| 5 | water-heater-leak-cleanup-2.webp | /water-heater-leak-cleanup, afterH2 2 "Water Heater Flooded Basement Midvale: The First 15 Minutes", split | PASS — water heater, water spreading across basement floor, man shutting valve holding mop; heater label illegible |
| 6 | south-salt-lake-ut-3.webp | /locations/south-salt-lake-ut, afterH2 3 "Sewage Backup Cleanup South Salt Lake", split | PASS — technician in gloves/boots extracting water from flooded apartment bathroom floor; no graphic mess, no legible text |
| 7 | commercial-water-damage-3.webp (OVERWRITTEN) | /commercial-water-damage, afterH2 10 "Commercial Drying for Large Open Spaces", split | PASS — large open office, five blue air movers + dehumidifier on wet floor, bright, full COLOUR; no legible text/branding. Old B&W file (Pexels 15043329) replaced; alt updated. Coordinator viewed it at full size: exact fit. |

Format/metadata (all 7): 1200x675 WebP q82, 50–128 KB, **0 EXIF** (PIL getexif;
files re-saved from scratch by PIL, which writes no EXIF/XMP; byte-scan: no Adobe /
Generated / XMP / ICC markers; exiftool not installed in this VM). No "AI" word in
filename, alt, lib/body-images.json, or qa/images-fill.json (substring scan clean).
No caption anywhere claims any generated image is a real job photo.

Manifest: lib/body-images.json = **19 routes, 57 body images, 3 per route** — the
4 fixed routes now have 3 each; commercial still 3. Existing entries untouched,
kept in afterH2 order; only the commercial-3 alt changed.

Per-page photo totals (hero + body, verifier-measured on the final build):
- **4 photos: all 19 service + location pages** (16 services + 3 locations) — target met.
- Homepage: 20 (hero + 19 cards). Other 11 pages (about, contact, guide, 5 resources,
  3 legal): 1 (hero). No empty body-image slots remain anywhere on the 19 pages.

## 2. Body text 19px (typography worker, app/globals.css only)
Bumped to 19px: body base, `p, li, td, th`, `.lead`, `table`, `.hero-trust`,
`.trust-band p`, contact-form inputs/textarea + radio inputs. Verified inheriting
at 19px by computed style (real Chromium): hero intro, card paragraphs, FAQ
answers (p/li), contact labels/legend, form inputs — 19px on 31/31 pages at
1440/390/320. Headings UNCHANGED (computed h1 44/34/24, h2 32/28, h3 24).

Deliberately left below 19px (chrome, not body copy — recorded, not a problem):
brand-text/brand-city 18px (15px @≤360px), main-nav links 18px, header-phone 18px,
eyebrow 18px (14px @≤360px, load-bearing for Button 2), breadcrumb 18px,
card-link 18px, panel-tag 18px, steps counter 18px, footer brand/headings 18px,
sticky-bar links 18px, .btn 18px @≤360px only (desktop .btn already 19px).

**Button 2 after the 19px bump: 31/31 @320 (worst bottom 497.2px) and 31/31 @390
(worst bottom 766.8px of the 844px viewport)** — worst pages: /condo-apartment-water-damage
and /resources/basement-flooding-spring-snowmelt-utah. No hero-spacing fix was
needed: at ≤600px the buttons sit ABOVE the intro (flex order), so the taller 19px
intro cannot push Button 2 down. Verified independently by the verifier (same
worst numbers, fresh run).

## 3. Independent verification — PROBLEMS 0 (fresh export, exit 0)
Verifier: qa/FINDINGS-fill-19px-verify-2026-11-13.md (+ evidence JSONs
qa/verify-fill-19px-static.json, qa/verify-fill-19px-render.json,
qa/brokenimgs-adjudication.json). Served out/ on /midvale-water-damage/, homepage
confirmed really Midvale (H1 + phone) before measuring.
- Data: lib/pages-data.json sha256 21c6e7f2…d638f — matches exactly. Fullness
  **31/31 FULL**, verbatim **0 missing words** (annotation-adjusted; extra 749 =
  header/footer/nav chrome only). H1 exactly 1/page, meta verbatim 31/31,
  FAQ **142/142** data/visible/JSON-LD, tables **43/43** cell-exact.
- Links: **162 = 143 body + 19 card**, 0 broken, 0 orphans (min inbound 5),
  0 body self-links, 0 unprefixed hrefs, 0 inventory mismatches. Visible
  `(/.../)` path text: 0 in rendered DOM and 0 in out/ HTML.
- Images: all 57 body images render (naturalWidth 1200 after full load + scroll);
  7 new files 1200x675 WebP, 0 EXIF, no "AI". Verifier spot-viewed 3 at full size
  (commercial-3, crawl-space-1, emergency-1) — exact topic fits.
- 19px: body 19px 31/31; headings unchanged. Only sub-19px elements: eyebrow
  kicker + breadcrumb (chrome, pre-existing, noted above).
- Button 2: 31/31 @320 AND @390 (worst 497.2 / 766.8px). Overflow 0 @320/390/1440.
  Console errors 0, page errors 0.
- Clicks/form: 6/6 real clicks kept the /midvale-water-damage/ subpath (5 card +
  1 body link, correct H1s). Contact form: 6 fields, all inputs 19px, submit
  "[Send My Request]" verbatim, honest non-send notice present.

## 4. Broken-image adjudication — ARTIFACT, not real (no fix made, none needed)
The cancelled full-page screenshot run (qa/fullpage-shoot.log, 5/31 routes shot)
flagged brokenImgs=3 homepage desktop, 5 homepage m390, 2 basement m390. The
verifier's fresh run flagged 19 @1440 + 23 @390 across 17 routes — every one
`loading=lazy`, nearly all the lowest image on the page, and **zero failed
requests for any local image in either run**. Targeted re-check (slow scroll +
scrollIntoView per image): **27 flagged srcs, 0 still broken** — every one reached
naturalWidth 1200. Network: 84 image requests tracked, all HTTP 200. Files: all
27 curl 200, out/ bytes identical to public/ bytes. The fast-scroll measurement
outran lazy-load triggering; counts varied run-to-run and width-to-width (shoot
log home m390 = 5, verifier run = 0). Evidence: qa/brokenimgs-adjudication.json.

## PROBLEMS
**P1 0 · P2 0 · P3 1 (environment, not a blocker)**
- P3-1 (environment): 56 failed requests, all the identical footer Google Maps
  embed (google.com/maps?...output=embed), all ERR_TUNNEL_CONNECTION_FAILED —
  this VM has no egress to google.com; 0 local assets failed. Pre-existing
  third-party embed, unchanged by this round. Needs a real-network eyeball check
  after push, not a code fix. (Known open item from earlier rounds: footer map
  blank in sandbox.)

Non-problem notes: eyebrow/breadcrumb chrome below 19px (above); typography
worker's first verification run died at page 27/31 (TargetClosedError — /tmp tmpfs
100% full from 490M /tmp/pg-mech-test, another worker's data, not deleted; rerun
with TMPDIR in-repo + --disable-dev-shm-usage completed 31/31); verifier's render
script crashed AFTER all 31 per-page measurements (incremental JSON saved) on a
JS syntax error in the click-section evaluate string — clicks + contact form
re-run cleanly in a separate script and merged into the same render JSON.
Both owned plainly by their workers; neither affects the verdict.

## Coordinator spot-checks (independent of both workers + verifier)
- Manifest: 19 routes, 57 total, 3 each — matches the worker's claim.
- Sampled files (commercial-3, crawl-space-1, emergency-1): 1200x675 RGB, EXIF 0,
  sizes 119/127/119 KB. No "AI"/generated markers in lib/body-images.json.
- Commercial-3 viewed at full size by me: large open office, wet floor, five blue
  air movers + dehumidifier, full colour, no legible text/branding — exact fit.
- Emergency desktop screenshot from the verifier's fresh set
  (qa/render-fill19px/emergency-water-extraction-desktop.png): hero clean, both
  buttons equal + visible, H2 pine + copper bar, 19px intro, no overflow, no dashes.
- Data hash 21c6e7f2b89bab95… re-verified by me; visible paren paths in out/ HTML = 0
  (fresh grep); CSS 19px rules present (body, p/li/td/th, .lead, hero-trust,
  trust-band, table, form inputs); review pack fresh (see below).

## Deliverables
- Review pack: ~/workspace/your_files/midvale-design-review.pdf — 31 pp, 5.9 MB,
  desktop 1440 + mobile 390 per route, from 62 fresh screenshots of this build
  (qa/render-fill19px/).
- This file: qa/FINDINGS-fill-19px-2026-11-13.md. Verifier findings:
  qa/FINDINGS-fill-19px-verify-2026-11-13.md. Image manifest: qa/images-fill.json.
  Typography findings: qa/FINDINGS-typo-19px-2026-11-13.md.
- PROGRESS.md updated with stage [8] FILL + 19px.

## Verdict
**PROBLEMS 0 — READY FOR RE-PUSH.** All 19 service+location pages at 4 photos
(hero + 3 body), 0 empty slots, B&W commercial-3 replaced with a colour photo,
body text 19px on all 31 pages with headings unchanged, Button 2 visible scroll-0
31/31 @320/@390, verbatim/links/fullness all clean, broken-image flags adjudicated
as lazy-load artifact with network evidence. The full-page screenshot job was
stopped because the build was changing — it re-runs on this final build (parent).
Parent pushes with the token on his word. OPEN: P3-1 footer Maps embed needs a
real-network eyeball check after push; 6 previously-empty slots are now generated
photos (not real job photos — his call whether to accept or supply real photos).
