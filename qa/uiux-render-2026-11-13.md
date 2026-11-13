# Midvale UT — UI/UX Render Audit (Stage 1)

**Date:** 2026-11-13 · **Auditor:** RENDER auditor (Stage 1 UI/UX round) · **Scope:** local audit only — no source edits, no push, no deploy, no token, no DNS.

## Method

- Served the built `out/` on the `/midvale-water-damage/` subpath at `http://127.0.0.1:8341/midvale-water-damage/` via the existing `qa/linkfix-serve.py` (accepts a port argument; no copy was needed).
- Site identity confirmed before screenshotting: homepage H1 = “24/7 Water Damage Restoration in Midvale, UT 84047”, phone (385) 337-3560 present, `/emergency-water-extraction` returns 200.
- Playwright Chromium, desktop viewport 1440×900 and mobile 390×844, full-page capture after a slow scroll (600px steps) so lazy images load; fonts/images waited on before capture. Raw metrics in `qa/uiux-render-data.json`.
- Per-page metrics: H1/H2/H3 lists, element counts (paragraphs, images, tables, lists, FAQ items), `scrollWidth` vs `clientWidth`, images with `naturalWidth == 0` after slow scroll (broken-local check), elements wider than the viewport, blank-band heuristic. Visual spot-checks on crops: home hero + service-card grid (desktop + mobile), emergency hero + mid-section (desktop + mobile), commercial mobile table, Magna desktop hero, frozen-pipes mobile hero, contact desktop top, home footer (desktop).
- `lib/pages-data.json` untouched (sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`, re-verified after the audit).

## Verdict

**31/31 routes rendered at desktop 1440 and mobile 390 — 62 full-page screenshots. P1: 0 · P2: 0 · P3 observations: 2 (both non-blocking, see below). No horizontal page overflow on any route at either width. 0 broken local images (214 image instances checked after slow scroll, 0 with `naturalWidth == 0`). Every route has exactly 1 H1. No blank bands, no cut-off elements, no misaligned grids found. Sticky header (top, 115px tall on mobile) and sticky body images (`.body-img-fig.sticky`, `top: 96px`) render correctly; sticky images appear at the right of text blocks on desktop and stack above/below on mobile with no overlap.**

## Defects by severity

### P1 — none

### P2 — none

### P3 — observations (not defects; no fix required for a pass)

**OBS-1 — Mobile tables are wider than the 390px viewport and need a horizontal swipe (18 routes).** Table widths 392–621px at 390px viewport (worst: `locations/magna-ut`, ~620–630px table, ~1.6× viewport; next: `storm-flood-damage` 450px, `commercial-water-damage` ~446–452px). Verified NOT clipped: every table sits in `.table-wrap { overflow-x: auto; }` (`app/globals.css:237`); probed live at 390px — wrapper `scrollWidth` (e.g. Magna 630) > `clientWidth` (342) with `overflow-x: auto`, so the full table is reachable by swiping, and the page itself never scrolls horizontally (`scrollWidth == clientWidth` on all 31 routes). Viewed the commercial table crop: the third column is cut at the right edge until swiped, with no visible scroll cue (no fade/shadow). Cosmetic only; a scroll hint would be a nice-to-have. Affected routes: home, basement-flooding-cleanup, burst-pipe-water-damage, ceiling-water-damage, commercial-water-damage, condo-apartment-water-damage, emergency-water-extraction, hardwood-floor-cabinet-drying, locations-magna-ut, locations-south-salt-lake-ut, resources-basement-flooding-spring-snowmelt-utah, resources-can-mold-grow-in-utah, resources-frozen-pipes-midvale, resources-upstairs-unit-leak-who-pays-utah, storm-flood-damage, water-damage-repair, water-heater-leak-cleanup, water-leak-detection.

**OBS-2 — Mobile sticky call bar covers the bottom ~50px of the viewport at scroll 0 (normal fixed-bar behaviour).** In full-page screenshots the bar appears to overlap the hero intro paragraph (e.g. home mobile: “…mold can take hold. From Bingham” runs under the “Call (385) 337-3560 · 24/7” bar). This is a full-page-capture artifact: the bar is fixed to the viewport bottom and the text scrolls under it in real use; no content is lost. Not a defect.

### Checked and explicitly NOT defects

- **Blank-band heuristic fired 1× per page on both widths** — every hit is `div.hero-shade` (the dark overlay div over the hero image, no text by design). Not a blank band; hero images render underneath it (viewed on home, emergency, Magna, frozen-pipes, contact).
- **“Wide” elements on mobile are only TABLE/THEAD/TBODY/TR** (see OBS-1). No other element exceeds the viewport on any route.
- **Footer Google Maps embed fails in this VM (ERR_TUNNEL_CONNECTION_FAILED, no route to google.com)** — the known open item, NOT counted as a defect. 0 local assets fail. Footer link columns themselves render clean (viewed home desktop footer: 5 aligned columns + copyright line).
- **Stale `_error` keys in `qa/uiux-render-data.json`** for swamp-cooler-leak-water-damage (m390), terms-of-use, water-damage-repair, water-heater-leak-cleanup, water-leak-detection, window-well-flooding are leftovers from the crashed intermediate run (see “Script errors” below); all 62 passes re-ran successfully afterwards and every entry now carries fresh metrics + a screenshot file. They are not failures.

## Script errors (owned plainly)

1. **First run died on `emergency-water-extraction` desktop: `Page.screenshot: Timeout 30000ms exceeded`** (full-page capture of a ~10,000px page). Fixed by raising the screenshot timeout to 180s with a retry, and by saving `uiux-render-data.json` incrementally after each route so a crash no longer loses collected metrics.
2. **Second run died on `swamp-cooler-leak-water-damage` m390: `Page.screenshot: Target crashed`** (renderer tab crash on a ~19,000px-tall mobile capture; the retry crashed the same way). Fixed with a segmented-screenshot fallback (viewport slices stitched with PIL) and per-viewport try/except so one crash cannot kill the run; metrics are now collected before the screenshot.
3. **A VM replacement mid-run wiped `/tmp`** (server + log gone) and **all Chromium binaries then failed to launch** (`SIGTRAP`, exit 133, on every Playwright build: headless-shell 1243/1248 and full chromium 1243 — even `--dump-dom about:blank`; `--version` still worked). Root cause found by probing: the default multi-process launch traps/hangs in this post-replacement VM (child/zygote process dies; main process then hangs or traps). **Workaround that works: launch with `--single-process --no-zygote --disable-gpu --disable-dev-shm-usage`** (verified: page loads, H1 correct). Single-process mode is fragile — one renderer crash kills the whole browser — so the script now launches a fresh browser per (route, viewport). No further launch failures after that change. `playwright install chromium-headless-shell` also fails here (`EPERM: operation not permitted, write`); not needed since the installed binaries work under the workaround.
4. **Two `nohup`/`setsid` background launches were silently killed** when their parent exec session ended (log stayed 0 bytes, process gone). The runs that completed were foreground `exec` calls that the runtime backgrounded. If this audit is re-run, launch it as a foreground exec and let the runtime background it; do not use `nohup`/`setsid` + `disown`.

## Per-route section catalogue

Counts are inside `<main>` at desktop width. Heights are full-page heights (px). Overflow = `scrollWidth > clientWidth`. Broken = local `<img>` with `naturalWidth == 0` after slow scroll. FAQ = `main [id*=faq], main details, main .faq` count.

### home — `/`

- **H1 (1):** 24/7 Water Damage Restoration in Midvale, UT 84047
- **Heights:** desktop 12781px · mobile 26728px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 47 · img 20 · table 1 · ul 3 · ol 1 · faq 1 · links 25 · body text 12656 chars
- **Counts (mobile):** p 47 · img 20 · table 1 · ul 3 · ol 1 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 13 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 0 · ~645px
  - “What causes most water damage in Midvale, UT homes?” — p 2 · img 0 · table 0 · lists 0 · ~462px
  - “Water Damage Midvale UT Property Owners Call Us For” — p 17 · img 16 · table 0 · lists 0 · ~3489px
  - “Water Damage Help Across Every Midvale Neighborhood” — p 3 · img 0 · table 0 · lists 0 · ~717px
  - “Why Midvale Homes Take On Water” — p 1 · img 0 · table 0 · lists 1 · ~742px
  - “How Our Water Mitigation Midvale 84047 Process Works” — p 2 · img 0 · table 0 · lists 1 · ~862px
  - “Clean, Gray or Sewage Water: Why the Category Matters” — p 1 · img 0 · table 1 · lists 0 · ~684px
  - “What Water Damage Restoration Midvale UT Jobs Usually Cost” — p 2 · img 0 · table 0 · lists 1 · ~554px
  - “Insurance Help for Midvale Homeowners, Renters and HOAs” — p 2 · img 0 · table 0 · lists 0 · ~462px
  - “What to Do in the First 30 Minutes” — p 1 · img 0 · table 0 · lists 1 · ~516px
  - “Nearby Cities We Serve” — p 4 · img 3 · table 0 · lists 0 · ~746px
  - “Water Damage Restoration FAQ for Midvale, UT” — p 6 · img 0 · table 0 · lists 0 · ~1192px
  - “Water Damage Help in Midvale Starts With One Call” — p 2 · img 0 · table 0 · lists 0 · ~449px
- **H2s (12):**
  - What causes most water damage in Midvale, UT homes?
  - Water Damage Midvale UT Property Owners Call Us For
  - Water Damage Help Across Every Midvale Neighborhood
  - Why Midvale Homes Take On Water
  - How Our Water Mitigation Midvale 84047 Process Works
  - Clean, Gray or Sewage Water: Why the Category Matters
  - What Water Damage Restoration Midvale UT Jobs Usually Cost
  - Insurance Help for Midvale Homeowners, Renters and HOAs
  - What to Do in the First 30 Minutes
  - Nearby Cities We Serve
  - Water Damage Restoration FAQ for Midvale, UT
  - Water Damage Help in Midvale Starts With One Call
- **Mobile wide elements:** table(s) [392]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### about — `/about`

- **H1 (1):** About Our Midvale Water Damage Restoration Team
- **Heights:** desktop 6741px · mobile 11429px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 19 · img 1 · table 1 · ul 3 · ol 2 · faq 1 · links 21 · body text 5723 chars
- **Counts (mobile):** p 19 · img 1 · table 1 · ul 3 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~629px
  - “Who handles water damage calls in Midvale, UT?” — p 15 · img 0 · table 1 · lists 4 · ~4852px
  - “About Us FAQ” — p 5 · img 0 · table 0 · lists 0 · ~744px
- **H2s (9):**
  - Who handles water damage calls in Midvale, UT?
  - Who We Are
  - Why Local Matters in Midvale
  - How We Work
  - What You Can Expect From Us
  - Who We Serve
  - Our Services
  - About Us FAQ
  - Talk to the Midvale Water Restoration Team

### basement-flooding-cleanup — `/basement-flooding-cleanup`

- **H1 (1):** Emergency Basement Flooding Cleanup in Midvale, UT 84047
- **Heights:** desktop 9188px · mobile 18089px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 32 · img 4 · table 1 · ul 2 · ol 2 · faq 1 · links 10 · body text 10153 chars
- **Counts (mobile):** p 32 · img 4 · table 1 · ul 2 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “Why does water come up through a Midvale basement floor with no leak?” — p 28 · img 3 · table 1 · lists 3 · ~7267px
  - “Basement Flooding FAQ” — p 5 · img 0 · table 0 · lists 0 · ~873px
- **H2s (12):**
  - Why does water come up through a Midvale basement floor with no leak?
  - Four Ways Midvale Basements Flood
  - Flooded Basement Midvale Homes: What's Inside the Walls Matters
  - Flood Cuts vs Drying the Wall Cavity
  - Sump Pump Failure Cleanup
  - Our Basement Water Removal Midvale Utah Process
  - Basement Apartments and Rentals
  - Basement Flooding Across Midvale Neighborhoods
  - What Basement Flooding Cleanup Midvale UT Costs
  - Keeping the Next Flood Out
  - Basement Flooding FAQ
  - A Flooded Basement in Midvale Needs Action Today
- **Mobile wide elements:** table(s) [397]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### burst-pipe-water-damage — `/burst-pipe-water-damage`

- **H1 (1):** Emergency Burst Pipe Water Damage Cleanup in Midvale, UT 84047
- **Heights:** desktop 9544px · mobile 18936px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 28 · img 4 · table 2 · ul 5 · ol 2 · faq 1 · links 10 · body text 10564 chars
- **Counts (mobile):** p 28 · img 4 · table 2 · ul 5 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “Where do pipes freeze first in Midvale homes?” — p 24 · img 3 · table 2 · lists 6 · ~7623px
  - “Burst Pipe FAQ” — p 5 · img 0 · table 0 · lists 0 · ~808px
- **H2s (14):**
  - Where do pipes freeze first in Midvale homes?
  - Turn It Off: Finding Your Shut-Off Fast
  - Signs a Pipe Has Already Split
  - Frozen Pipe Burst Midvale: Where It Happens by Home Type
  - Pipe Burst in Wall: Why Surface Drying Isn't Enough
  - Pipe Materials in Midvale Homes
  - Our Broken Pipe Cleanup Midvale Utah Process
  - Sudden Burst vs Slow Leak: What Insurance Usually Covers
  - Hour by Hour After a Pipe Bursts
  - Burst Pipes in Midvale Businesses and Rentals
  - What Burst Pipe Water Damage Midvale UT Costs
  - Freeze-Proofing Before the Next Cold Snap
  - Burst Pipe FAQ
  - Burst Pipe in Midvale? Stop the Damage Now
- **Mobile wide elements:** table(s) [396]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### ceiling-water-damage — `/ceiling-water-damage`

- **H1 (1):** Professional Ceiling Water Damage Repair in Midvale, UT 84047
- **Heights:** desktop 9216px · mobile 16981px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 33 · img 4 · table 1 · ul 2 · ol 3 · faq 1 · links 11 · body text 9473 chars
- **Counts (mobile):** p 33 · img 4 · table 1 · ul 2 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “What should I do if my Midvale ceiling is sagging with water?” — p 29 · img 3 · table 1 · lists 4 · ~7295px
  - “Ceiling Water Damage FAQ” — p 5 · img 0 · table 0 · lists 0 · ~808px
- **H2s (12):**
  - What should I do if my Midvale ceiling is sagging with water?
  - Ceiling Emergency: The Safe Order of Steps
  - Ceiling Leak Midvale: The Most Common Sources
  - Ceiling Types in Midvale Homes and What They Need
  - How We Repair Ceiling Water Damage
  - Why Wet Ceiling Insulation Matters
  - Ice Dams on Midvale Homes
  - Ceiling Leaks by Midvale Home Type
  - Signs of a Hidden Ceiling Leak
  - What Ceiling Water Damage Repair Midvale UT Costs
  - Ceiling Water Damage FAQ
  - Water Overhead? Get It Handled Before the Ceiling Fails
- **Mobile wide elements:** table(s) [393]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### commercial-water-damage — `/commercial-water-damage`

- **H1 (1):** 24/7 Commercial Water Damage Restoration in Midvale, UT 84047
- **Heights:** desktop 10017px · mobile 19121px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 32 · img 4 · table 1 · ul 5 · ol 3 · faq 1 · links 9 · body text 10713 chars
- **Counts (mobile):** p 32 · img 4 · table 1 · ul 5 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “How fast can a Midvale business reopen after water damage?” — p 28 · img 3 · table 1 · lists 7 · ~8096px
  - “Commercial Water Damage FAQ” — p 5 · img 0 · table 0 · lists 0 · ~711px
- **H2s (16):**
  - How fast can a Midvale business reopen after water damage?
  - Midvale Business Districts We Serve
  - Commercial Water Extraction Midvale: What Makes Business Jobs Different
  - Office Flood Cleanup Midvale: Keeping Work Moving
  - Common Causes of Business Water Damage in Midvale
  - Restaurants and Medical Offices: Extra Care
  - Business Water Damage Cleanup Process
  - Landlords, Tenants and Property Managers
  - After-Hours Drying: What a Night Looks Like
  - Protecting Inventory, Equipment and Records
  - Commercial Drying for Large Open Spaces
  - Questions to Ask Before Hiring Any Commercial Restoration Crew
  - What Commercial Water Damage Restoration Midvale UT Costs
  - Preparing Your Business Before a Leak
  - Commercial Water Damage FAQ
  - Water in Your Business? Get It Handled Tonight
- **Mobile wide elements:** table(s) [446]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### condo-apartment-water-damage — `/condo-apartment-water-damage`

- **H1 (1):** 24/7 Condo, Townhome & Apartment Water Damage Cleanup in Midvale, UT 84047
- **Heights:** desktop 10221px · mobile 19084px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 28 · img 4 · table 2 · ul 5 · ol 3 · faq 1 · links 9 · body text 10498 chars
- **Counts (mobile):** p 28 · img 4 · table 2 · ul 5 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~748px
  - “Who pays when water leaks from an upstairs condo in Midvale?” — p 24 · img 3 · table 2 · lists 7 · ~8212px
  - “Condo & Apartment Water Damage FAQ” — p 5 · img 0 · table 0 · lists 0 · ~711px
- **H2s (15):**
  - Who pays when water leaks from an upstairs condo in Midvale?
  - Water Leak From Upstairs Unit: What to Do First
  - How Water Moves Through Midvale's Stacked Buildings
  - Apartment Water Damage Midvale: Owners, Renters and Landlords
  - Townhome Water Leak Midvale: Shared Walls, Separate Owners
  - HOA Water Damage Responsibility: A General Guide
  - HO-6 Water Damage: What Unit Owners Should Know
  - How We Handle Multi-Unit Water Damage
  - Fire Sprinkler Discharges
  - Midvale Multi-Unit Communities We Serve
  - Most Common Leak Sources in Midvale Condos and Apartments
  - What Condo Water Damage Midvale UT Cleanup Costs
  - Preventing Unit-to-Unit Leaks
  - Condo & Apartment Water Damage FAQ
  - Leak in Your Building? Stop It From Spreading
- **Mobile wide elements:** table(s) [413]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### contact — `/contact`

- **H1 (1):** Call for 24/7 Water Damage Help in Midvale, UT 84047
- **Heights:** desktop 6730px · mobile 10743px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 27 · img 1 · table 2 · ul 3 · ol 1 · faq 1 · links 7 · body text 4337 chars
- **Counts (mobile):** p 27 · img 1 · table 2 · ul 3 · ol 1 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 4 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~629px
  - “What should I do while waiting for a water damage crew in Midvale?” — p 23 · img 0 · table 2 · lists 3 · ~4841px
  - “(no heading)” — p 6 · img 0 · table 0 · lists 0 · ~910px
  - “Contact FAQ” — p 5 · img 0 · table 0 · lists 0 · ~711px
- **H2s (8):**
  - What should I do while waiting for a water damage crew in Midvale?
  - Contact Water Damage Restoration Midvale
  - 24/7 Water Damage Help Midvale: What to Have Ready
  - Request Form Fields
  - Areas We Serve
  - Who to Call First for Utility Problems
  - Contact FAQ
  - Call Now

### crawl-space-water-damage — `/crawl-space-water-damage`

- **H1 (1):** Emergency Crawl Space Water Damage Cleanup in Midvale, UT 84047
- **Heights:** desktop 9006px · mobile 16838px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 29 · img 4 · table 1 · ul 5 · ol 2 · faq 1 · links 8 · body text 9620 chars
- **Counts (mobile):** p 29 · img 4 · table 1 · ul 5 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~629px
  - “Which Midvale homes have crawl spaces that flood?” — p 25 · img 3 · table 1 · lists 6 · ~7117px
  - “Crawl Space FAQ” — p 5 · img 0 · table 0 · lists 0 · ~776px
- **H2s (14):**
  - Which Midvale homes have crawl spaces that flood?
  - Signs Your Crawl Space Is Wet
  - What Floods Midvale Crawl Spaces
  - Why a Wet Crawl Space Is a Problem for the Whole House
  - Wet Crawl Space Drying Midvale: How We Do It
  - Wood Moisture: How We Know a Crawl Space Is Dry
  - Crawl Space Vapor Barrier After Drying
  - Crawl Spaces by Midvale Neighborhood
  - Crawl Space Hazards to Know Before Going In
  - Preventing the Next Crawl Space Flood
  - Crawl Spaces Under Rentals and Additions
  - What Crawl Space Water Damage Midvale UT Cleanup Costs
  - Crawl Space FAQ
  - Wet Crawl Space? Dry It Before It Damages the House

### disclaimer — `/disclaimer`

- **H1 (1):** Disclaimer
- **Heights:** desktop 3626px · mobile 5899px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 13 · img 1 · table 0 · ul 0 · ol 1 · faq 0 · links 5 · body text 2080 chars
- **Counts (mobile):** p 13 · img 1 · table 0 · ul 0 · ol 1 · faq 0
- **Sections (`<section>` in `<main>`, in order):** 2 sections
  - “(no heading)” — p 3 · img 1 · table 0 · lists 1 · ~414px
  - “General Information Only” — p 10 · img 0 · table 0 · lists 0 · ~1951px
- **H2s (9):**
  - General Information Only
  - Safety
  - Price Ranges
  - Insurance Information
  - Timelines and Results
  - Local Information
  - Third-Party Links
  - No Professional Relationship
  - Contact

### emergency-water-extraction — `/emergency-water-extraction`

- **H1 (1):** Rapid Emergency Water Extraction in Midvale, UT 84047
- **Heights:** desktop 10191px · mobile 18931px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 37 · img 4 · table 2 · ul 4 · ol 2 · faq 1 · links 12 · body text 10732 chars
- **Counts (mobile):** p 37 · img 4 · table 2 · ul 4 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~693px
  - “How fast should standing water be removed from a Midvale home?” — p 33 · img 3 · table 2 · lists 5 · ~8237px
  - “Emergency Water Extraction FAQ” — p 6 · img 0 · table 0 · lists 0 · ~1003px
- **H2s (12):**
  - How fast should standing water be removed from a Midvale home?
  - What Happens in the First 60 Minutes on Site
  - Water Removal Midvale Jobs: The Equipment and When We Use It
  - Can Wet Carpet and Pad Be Saved?
  - Standing Water Removal Midvale Utah Homes Need Most Often
  - Clean, Gray or Sewage: How the Water Category Changes Extraction
  - Why Midvale Floods Need Fast Extraction
  - Extraction for Landlords, Property Managers and HOAs
  - What Emergency Water Extraction Midvale UT Costs
  - While You Wait: Do This, Not That
  - Emergency Water Extraction FAQ
  - Standing Water in Midvale? Get It Out Now
- **Mobile wide elements:** table(s) [426]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### hardwood-floor-cabinet-drying — `/hardwood-floor-cabinet-drying`

- **H1 (1):** Fast Hardwood Floor & Cabinet Drying in Midvale, UT 84047
- **Heights:** desktop 9683px · mobile 19146px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 28 · img 4 · table 2 · ul 4 · ol 3 · faq 1 · links 9 · body text 10246 chars
- **Counts (mobile):** p 28 · img 4 · table 2 · ul 4 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~629px
  - “Can wet hardwood floors in Midvale be saved without tearing them out?” — p 24 · img 3 · table 2 · lists 6 · ~7794px
  - “Hardwood Floor & Cabinet FAQ” — p 5 · img 0 · table 0 · lists 0 · ~776px
- **H2s (15):**
  - Can wet hardwood floors in Midvale be saved without tearing them out?
  - Hardwood Floor Cupping, Crowning and Buckling
  - Wet Hardwood Floor Drying Midvale: How Floor Mats Work
  - Solid, Engineered, Laminate and Vinyl: What Can Be Saved
  - Cabinet Water Damage Drying Midvale: Keeping Counters in Place
  - Particleboard vs Plywood Cabinets
  - Subfloor Drying: The Part Nobody Sees
  - Where Midvale Floors and Cabinets Get Wet
  - When Replacement Makes More Sense
  - Why Utah's Dry Climate Changes How Floors Dry
  - What to Do Right Now If Your Floor or Cabinets Are Wet
  - Water Under Hardwood From Below
  - What Hardwood Floor Water Damage Midvale UT Drying Costs
  - Hardwood Floor & Cabinet FAQ
  - Wet Floors or Cabinets? Start Drying Today
- **Mobile wide elements:** table(s) [402]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### locations-cottonwood-heights-ut — `/locations/cottonwood-heights-ut`

- **H1 (1):** 24/7 Water Damage Restoration in Cottonwood Heights, UT 84121
- **Heights:** desktop 10137px · mobile 19147px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 31 · img 4 · table 1 · ul 5 · ol 2 · faq 1 · links 14 · body text 11024 chars
- **Counts (mobile):** p 31 · img 4 · table 1 · ul 5 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “Why do Cottonwood Heights basements take on water during spring runoff?” — p 27 · img 3 · table 1 · lists 6 · ~8536px
  - “Cottonwood Heights Water Damage FAQ” — p 5 · img 0 · table 0 · lists 0 · ~808px
- **H2s (13):**
  - Why do Cottonwood Heights basements take on water during spring runoff?
  - Cottonwood Heights Water Risks, Season by Season
  - Flooded Basement Cottonwood Heights Homes: What We Do
  - Burst Pipe Repair Cottonwood Heights: Winter Damage
  - Our Water Damage Services in Cottonwood Heights
  - Neighborhoods and Areas We Cover
  - Protecting a Cottonwood Heights Home From Water
  - Cottonwood Heights Homes and Where They Leak
  - What to Do First When Water Hits Your Cottonwood Heights Home
  - Why Fast Drying Matters More in Cottonwood Heights
  - What Water Damage Restoration Cottonwood Heights UT Costs
  - Cottonwood Heights Water Damage FAQ
  - Water in Your Cottonwood Heights Home? Call Now

### locations-magna-ut — `/locations/magna-ut`

- **H1 (1):** Local Water Damage Restoration in Magna, UT 84044
- **Heights:** desktop 10583px · mobile 19309px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 31 · img 4 · table 2 · ul 5 · ol 2 · faq 1 · links 15 · body text 11116 chars
- **Counts (mobile):** p 31 · img 4 · table 2 · ul 5 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~693px
  - “Why do older Magna homes near Main Street get pipe and sewer leaks?” — p 27 · img 3 · table 2 · lists 6 · ~8949px
  - “Magna Water Damage FAQ” — p 5 · img 0 · table 0 · lists 0 · ~711px
- **H2s (15):**
  - Why do older Magna homes near Main Street get pipe and sewer leaks?
  - Home Age and Pipe Material in Magna
  - Flooded Basement Magna: What Usually Causes It
  - Burst Pipe Cleanup Magna: West-Valley Winters
  - Our Water Damage Services in Magna
  - Areas We Cover in Magna
  - What to Do First If Water Hits Your Magna Home
  - Basement Mold After Flood in Older Homes
  - Older Home Water Damage: Prevention Checklist
  - Magna Homes and Where They Leak
  - Why Drying Matters in Magna's Cold Months
  - Crawl Spaces and Additions in Magna
  - What Water Damage Restoration Magna UT Costs
  - Magna Water Damage FAQ
  - Water in Your Magna Home? Call Now
- **Mobile wide elements:** table(s) [621]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### locations-south-salt-lake-ut — `/locations/south-salt-lake-ut`

- **H1 (1):** Emergency Water Damage Restoration in South Salt Lake, UT 84115
- **Heights:** desktop 10746px · mobile 19653px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 30 · img 4 · table 2 · ul 5 · ol 1 · faq 1 · links 19 · body text 11305 chars
- **Counts (mobile):** p 30 · img 4 · table 2 · ul 5 · ol 1 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “What should South Salt Lake renters do first when water floods their apartment?” — p 26 · img 3 · table 2 · lists 5 · ~9145px
  - “South Salt Lake Water Damage FAQ” — p 5 · img 0 · table 0 · lists 0 · ~776px
- **H2s (14):**
  - What should South Salt Lake renters do first when water floods their apartment?
  - Water Damage for Renters, Owners and Businesses
  - Problem-to-Service Guide for South Salt Lake
  - Sewage Backup Cleanup South Salt Lake
  - Our Water Damage Services in South Salt Lake
  - Areas We Cover in South Salt Lake
  - Older Homes, Older Pipes
  - Protecting Your Unit or Building
  - South Salt Lake Buildings and Where They Leak
  - Why Water Spreads Fast in Multi-Unit Buildings
  - What Water Damage Restoration South Salt Lake UT Costs
  - What to Do in the First 30 Minutes
  - South Salt Lake Water Damage FAQ
  - Water in Your South Salt Lake Home or Business? Call Now
- **Mobile wide elements:** table(s) [397]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### midvale-water-sewer-emergency-contacts — `/midvale-water-sewer-emergency-contacts`

- **H1 (1):** Midvale Water & Sewer Emergency Contacts (84047)
- **Heights:** desktop 7056px · mobile 14564px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 25 · img 1 · table 1 · ul 2 · ol 3 · faq 1 · links 8 · body text 7292 chars
- **Counts (mobile):** p 25 · img 1 · table 1 · ul 2 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~596px
  - “Which sewer district serves my Midvale street?” — p 21 · img 0 · table 1 · lists 4 · ~5199px
  - “Water & Sewer Emergency FAQ” — p 5 · img 0 · table 0 · lists 0 · ~841px
- **H2s (11):**
  - Which sewer district serves my Midvale street?
  - Midvale Sewer District Lookup: Contacts
  - Midvale Sewer Backup: Who to Call and in What Order
  - Midvale Water Emergency Number and Main Breaks
  - How to Shut Off Main Water Valve
  - Curb Stop Shut Off
  - Sandbags Salt Lake County Residents Can Use
  - When to Call a Restoration Crew
  - Storm and Flood Emergencies
  - Water & Sewer Emergency FAQ
  - Save This Page, and Our Number

### mold-remediation — `/mold-remediation`

- **H1 (1):** Professional Mold Remediation in Midvale, UT 84047
- **Heights:** desktop 10037px · mobile 18043px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 32 · img 4 · table 1 · ul 6 · ol 2 · faq 1 · links 12 · body text 10081 chars
- **Counts (mobile):** p 32 · img 4 · table 1 · ul 6 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “Can mold grow in Midvale homes when Utah air is so dry?” — p 28 · img 3 · table 1 · lists 7 · ~8115px
  - “Mold Remediation FAQ” — p 5 · img 0 · table 0 · lists 0 · ~841px
- **H2s (16):**
  - Can mold grow in Midvale homes when Utah air is so dry?
  - Signs You May Have Mold
  - Where Mold Hides in Midvale Homes
  - Musty Basement Smell: Mold or Just Damp?
  - Mold Removal Midvale: Our Remediation Process
  - Why Bleach and Paint Don't Fix Mold
  - Mold Inspection After Water Damage Midvale
  - Utah Has No State Mold License: What to Ask
  - Odor Removal After Mold
  - Mold in Midvale Rentals: Landlords and Tenants
  - Who Should Stay Away From Moldy Areas
  - Mold After a Midvale Water Event: Typical Timeline
  - What Mold Remediation Midvale UT Costs
  - Preventing Mold After a Leak
  - Mold Remediation FAQ
  - Mold in Your Midvale Home? Fix the Cause, Not Just the Spot

### privacy-policy — `/privacy-policy`

- **H1 (1):** Privacy Policy
- **Heights:** desktop 4697px · mobile 7613px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 17 · img 1 · table 0 · ul 3 · ol 1 · faq 0 · links 5 · body text 3192 chars
- **Counts (mobile):** p 17 · img 1 · table 0 · ul 3 · ol 1 · faq 0
- **Sections (`<section>` in `<main>`, in order):** 2 sections
  - “(no heading)” — p 3 · img 1 · table 0 · lists 1 · ~414px
  - “Information We Collect” — p 14 · img 0 · table 0 · lists 3 · ~3023px
- **H2s (11):**
  - Information We Collect
  - How We Use Information
  - Cookies and Analytics
  - How Information Is Shared
  - How We Protect Information
  - How Long We Keep Information
  - Your Choices
  - Children's Privacy
  - Links to Other Websites
  - Changes to This Policy
  - Contact

### resources-basement-flooding-spring-snowmelt-utah — `/resources/basement-flooding-spring-snowmelt-utah`

- **H1 (1):** Water Coming Up Through Your Basement Floor? Spring Snowmelt in Midvale
- **Heights:** desktop 8448px · mobile 15852px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 24 · img 1 · table 2 · ul 6 · ol 1 · faq 1 · links 9 · body text 8753 chars
- **Counts (mobile):** p 24 · img 1 · table 2 · ul 6 · ol 1 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 3 · img 1 · table 0 · lists 1 · ~589px
  - “Why does my Midvale basement flood in spring without rain?” — p 21 · img 0 · table 2 · lists 6 · ~6599px
  - “Spring Snowmelt FAQ” — p 5 · img 0 · table 0 · lists 0 · ~841px
- **H2s (14):**
  - Why does my Midvale basement flood in spring without rain?
  - How to Tell Groundwater From a Leak
  - Where Snowmelt Gets Into Midvale Basements
  - What to Do in the First Hour
  - Why Seepage Needs More Than a Shop Vac
  - Which Midvale Basements Seep Most
  - Fixes That Reduce Spring Seepage
  - Sandbags and Spring Prep
  - Does Insurance Cover Spring Seepage?
  - A Spring Checklist for Midvale Basements
  - Seepage and Mold: Why the Clock Matters
  - What It Generally Costs
  - Spring Snowmelt FAQ
  - Water Coming Up Through Your Basement Floor?
- **Mobile wide elements:** table(s) [425]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### resources-can-mold-grow-in-utah — `/resources/can-mold-grow-in-utah`

- **H1 (1):** Utah Is Too Dry for Mold? Why Wet Drywall Still Molds in Midvale
- **Heights:** desktop 8630px · mobile 16133px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 22 · img 1 · table 3 · ul 5 · ol 2 · faq 1 · links 9 · body text 8275 chars
- **Counts (mobile):** p 22 · img 1 · table 3 · ul 5 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 3 · img 1 · table 0 · lists 1 · ~534px
  - “Can mold grow in Utah if the air is so dry?” — p 19 · img 0 · table 3 · lists 6 · ~6836px
  - “Utah Mold FAQ” — p 5 · img 0 · table 0 · lists 0 · ~808px
- **H2s (14):**
  - Can mold grow in Utah if the air is so dry?
  - Outdoor Air vs Inside a Wet Wall
  - How Fast Mold Grows After a Leak
  - Why Fans and Open Windows Aren't Enough
  - Where Mold Hides in Midvale Homes
  - Signs Mold Has Already Started
  - Why Bleach and Paint Don't Fix It
  - Utah Has No State Mold License
  - How to Prevent Mold After Any Leak
  - The Cost of Waiting
  - Mold Risk by Room in Midvale Homes
  - A Quick Musty-Smell Checklist
  - Utah Mold FAQ
  - Had a Leak in Your Midvale Home?
- **Mobile wide elements:** table(s) [413]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### resources-frozen-pipes-midvale — `/resources/frozen-pipes-midvale`

- **H1 (1):** How to Keep Pipes From Freezing in Midvale, and What to Do If One Bursts
- **Heights:** desktop 8435px · mobile 15530px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 24 · img 1 · table 1 · ul 4 · ol 3 · faq 1 · links 8 · body text 9310 chars
- **Counts (mobile):** p 24 · img 1 · table 1 · ul 4 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 3 · img 1 · table 0 · lists 1 · ~566px
  - “At what temperature do pipes freeze in Midvale homes?” — p 21 · img 0 · table 1 · lists 6 · ~6609px
  - “Frozen Pipe FAQ” — p 5 · img 0 · table 0 · lists 0 · ~808px
- **H2s (14):**
  - At what temperature do pipes freeze in Midvale homes?
  - Where Midvale Pipes Freeze First
  - Why the Hose Bib Matters So Much
  - How to Keep Pipes From Freezing: A Midvale Checklist
  - Signs a Pipe Is Already Frozen
  - How to Thaw a Frozen Pipe Safely
  - What to Do in the First 15 Minutes After a Burst
  - Why Burst Pipe Damage Spreads Inside Walls
  - Does Insurance Cover Frozen Pipes in Utah?
  - Frozen Pipes in Midvale Rentals and Condos
  - Which Midvale Homes Are Most at Risk
  - Water Leak Alarms: A Cheap Early Warning
  - Frozen Pipe FAQ
  - Pipe Burst in Your Midvale Home?
- **Mobile wide elements:** table(s) [415]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### resources-upstairs-unit-leak-who-pays-utah — `/resources/upstairs-unit-leak-who-pays-utah`

- **H1 (1):** Upstairs Unit Leaked Into Yours? Who Pays in a Utah Condo or Apartment
- **Heights:** desktop 8206px · mobile 15400px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 24 · img 1 · table 1 · ul 4 · ol 3 · faq 1 · links 7 · body text 9025 chars
- **Counts (mobile):** p 24 · img 1 · table 1 · ul 4 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 3 · img 1 · table 0 · lists 1 · ~566px
  - “Who pays when an upstairs neighbor's leak damages my Utah condo?” — p 21 · img 0 · table 1 · lists 6 · ~6380px
  - “Upstairs Leak FAQ” — p 5 · img 0 · table 0 · lists 0 · ~744px
- **H2s (12):**
  - Who pays when an upstairs neighbor's leak damages my Utah condo?
  - What to Do First When Water Comes From Above
  - The Three Policies Involved
  - A General Guide to Who Covers What
  - What If the Upstairs Neighbor Was Careless?
  - Why Good Records Matter So Much
  - Common Unit-to-Unit Leak Sources in Midvale
  - Renters: Your Rights and Your Responsibilities
  - How to Protect Yourself Before It Happens
  - What If the Leak Started in Your Unit?
  - Upstairs Leak FAQ
  - Water Coming From the Unit Above?
- **Mobile wide elements:** table(s) [396]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### resources-winterize-swamp-cooler-utah — `/resources/winterize-swamp-cooler-utah`

- **H1 (1):** Swamp Cooler Winterizing Checklist for Midvale Homes
- **Heights:** desktop 7818px · mobile 14429px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 25 · img 1 · table 1 · ul 4 · ol 2 · faq 1 · links 8 · body text 8500 chars
- **Counts (mobile):** p 25 · img 1 · table 1 · ul 4 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 3 · img 1 · table 0 · lists 1 · ~534px
  - “When should Midvale homeowners winterize a swamp cooler?” — p 22 · img 0 · table 1 · lists 5 · ~6024px
  - “Swamp Cooler Winterizing FAQ” — p 5 · img 0 · table 0 · lists 0 · ~744px
- **H2s (13):**
  - When should Midvale homeowners winterize a swamp cooler?
  - Why Winterizing Matters
  - Step-by-Step Swamp Cooler Shutdown
  - Swamp Cooler Leak Signs to Catch Early
  - What Happens When You Skip It
  - Spring Start-Up Checklist
  - A Midvale Swamp Cooler Calendar
  - Hard Water and Your Cooler
  - Swamp Cooler or Central Air Condensate?
  - Side-Mount and Window Coolers
  - What a Cooler Leak Does to Your Attic
  - Swamp Cooler Winterizing FAQ
  - Stain Around Your Ceiling Vent?

### sewage-backup-cleanup — `/sewage-backup-cleanup`

- **H1 (1):** 24/7 Sewage Backup Cleanup in Midvale, UT 84047
- **Heights:** desktop 9560px · mobile 18102px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 30 · img 4 · table 2 · ul 1 · ol 3 · faq 1 · links 8 · body text 10280 chars
- **Counts (mobile):** p 30 · img 4 · table 2 · ul 1 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~629px
  - “Who do I call first for a sewer backup in Midvale?” — p 26 · img 3 · table 2 · lists 3 · ~7671px
  - “Sewage Backup FAQ” — p 5 · img 0 · table 0 · lists 0 · ~905px
- **H2s (14):**
  - Who do I call first for a sewer backup in Midvale?
  - Stop, Then Call: The Right Order
  - Sewer Backup Midvale: Public Main or Your Private Lateral?
  - Why Sewage Is Dangerous
  - Our Sewage Cleanup Midvale Utah Protocol
  - What Stays and What Goes
  - Floor Drain Backup in Older Midvale Homes
  - Toilet Sewage Overflow vs Main Line Backup
  - Getting Rid of the Smell
  - Insurance: The Sewer Backup Endorsement
  - Sewage Backups by Midvale Property Type
  - What Sewage Backup Cleanup Midvale UT Costs
  - Sewage Backup FAQ
  - Sewage in Your Home? Get It Cleaned Today

### storm-flood-damage — `/storm-flood-damage`

- **H1 (1):** Emergency Storm & Flash Flood Cleanup in Midvale, UT 84047
- **Heights:** desktop 10138px · mobile 18369px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 35 · img 4 · table 2 · ul 4 · ol 2 · faq 1 · links 10 · body text 10169 chars
- **Counts (mobile):** p 35 · img 4 · table 2 · ul 4 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~693px
  - “Why do Midvale streets and basements flood in summer storms?” — p 31 · img 3 · table 2 · lists 5 · ~8184px
  - “Storm & Flash Flood FAQ” — p 5 · img 0 · table 0 · lists 0 · ~744px
- **H2s (14):**
  - Why do Midvale streets and basements flood in summer storms?
  - Flash Flood Cleanup Midvale: Why Storm Water Is Different
  - Where Storm Water Gets Into Midvale Homes
  - Flood Damage Restoration Midvale Utah: Our Process
  - Storm Flooding Cleanup Safety: What Not to Do
  - Midvale's Storm Seasons
  - Flood Insurance vs Homeowners Insurance in Utah
  - Protecting Your Midvale Property Before the Next Storm
  - Storm Damage for Midvale Businesses
  - Storm Water Damage Across Midvale Neighborhoods
  - What to Photograph for a Flood or Storm Claim
  - What Storm Water Damage Midvale UT Cleanup Costs
  - Storm & Flash Flood FAQ
  - Storm Flooded Your Property? Start Cleanup Now
- **Mobile wide elements:** table(s) [450]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### swamp-cooler-leak-water-damage — `/swamp-cooler-leak-water-damage`

- **H1 (1):** Fast Swamp Cooler Leak Water Damage Repair in Midvale, UT 84047
- **Heights:** desktop 9132px · mobile 18237px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 28 · img 4 · table 3 · ul 2 · ol 2 · faq 1 · links 7 · body text 9474 chars
- **Counts (mobile):** p 28 · img 4 · table 3 · ul 2 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~629px
  - “Why is my swamp cooler leaking through the ceiling in Midvale?” — p 24 · img 3 · table 3 · lists 3 · ~7243px
  - “Swamp Cooler Leak FAQ” — p 5 · img 0 · table 0 · lists 0 · ~776px
- **H2s (15):**
  - Why is my swamp cooler leaking through the ceiling in Midvale?
  - Swamp Cooler Leaking Through Ceiling Midvale: Where the Water Comes From
  - Evaporative Cooler Leak Midvale: The Signs Before the Ceiling Fails
  - When a Cooler Freezes Before Winterizing
  - Why Wet Attic Insulation Has to Come Out
  - How We Repair Swamp Cooler Leak Damage
  - Which Midvale Homes Have Swamp Coolers
  - A Midvale Swamp Cooler Calendar
  - Side-Mount and Window Coolers
  - Swamp Cooler Leaks vs Central Air Condensate Leaks
  - What Adjusters Ask About Cooler Leaks
  - What Swamp Cooler Leak Water Damage Midvale UT Repair Costs
  - Swamp Cooler Overflow and Mold
  - Swamp Cooler Leak FAQ
  - Swamp Cooler Leaking? Protect Your Ceiling Today

### terms-of-use — `/terms-of-use`

- **H1 (1):** Terms of Use
- **Heights:** desktop 4457px · mobile 7004px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 17 · img 1 · table 0 · ul 1 · ol 1 · faq 0 · links 5 · body text 2805 chars
- **Counts (mobile):** p 17 · img 1 · table 0 · ul 1 · ol 1 · faq 0
- **Sections (`<section>` in `<main>`, in order):** 2 sections
  - “(no heading)” — p 3 · img 1 · table 0 · lists 1 · ~414px
  - “Use of the Website” — p 14 · img 0 · table 0 · lists 1 · ~2782px
- **H2s (12):**
  - Use of the Website
  - Website Content
  - Service Requests
  - Price Ranges and Estimates
  - Intellectual Property
  - Links to Other Websites
  - No Warranties
  - Limitation of Liability
  - Indemnity
  - Governing Law
  - Changes to These Terms
  - Contact

### water-damage-repair — `/water-damage-repair`

- **H1 (1):** Local Water Damage Repair & Rebuild in Midvale, UT 84047
- **Heights:** desktop 9202px · mobile 17563px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 29 · img 4 · table 2 · ul 5 · ol 2 · faq 1 · links 11 · body text 9534 chars
- **Counts (mobile):** p 29 · img 4 · table 2 · ul 5 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “Do I need a permit to rebuild after water damage in Midvale?” — p 25 · img 3 · table 2 · lists 6 · ~7281px
  - “Water Damage Repair FAQ” — p 5 · img 0 · table 0 · lists 0 · ~776px
- **H2s (15):**
  - Do I need a permit to rebuild after water damage in Midvale?
  - From Drying to Rebuild Without the Gap
  - Drywall Water Damage Repair Midvale
  - Flooring Water Damage Repair Midvale
  - Cabinets, Vanities and Trim
  - Basement Rebuild After Flood
  - Ceilings and Upper Floors
  - Repairs for Condos, Rentals and Businesses
  - How Insurance Handles the Rebuild
  - Typical Rebuild Timelines
  - Choosing Materials That Handle Water Better
  - What to Expect During the Rebuild
  - What Water Damage Repair Midvale UT Costs
  - Water Damage Repair FAQ
  - Ready to Put Your Home Back Together?
- **Mobile wide elements:** table(s) [412]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### water-heater-leak-cleanup — `/water-heater-leak-cleanup`

- **H1 (1):** Emergency Water Heater & Appliance Leak Cleanup in Midvale, UT 84047
- **Heights:** desktop 9539px · mobile 17518px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 31 · img 4 · table 1 · ul 4 · ol 3 · faq 1 · links 12 · body text 9941 chars
- **Counts (mobile):** p 31 · img 4 · table 1 · ul 4 · ol 3 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “Does Midvale's hard water make water heaters fail sooner?” — p 27 · img 3 · table 1 · lists 6 · ~7618px
  - “Water Heater & Appliance Leak FAQ” — p 5 · img 0 · table 0 · lists 0 · ~808px
- **H2s (13):**
  - Does Midvale's hard water make water heaters fail sooner?
  - The Appliances That Flood Midvale Homes Most
  - Water Heater Flooded Basement Midvale: The First 15 Minutes
  - General Lifespan of Common Water Sources
  - How We Clean Up Appliance Leaks
  - Second-Floor Laundry and Townhome Leaks
  - Water Heater Leaks by Midvale Home Type
  - Gas, Electric and Tankless: How Each One Fails
  - Hidden Appliance Leaks: Signs in Floors and Cabinets
  - What Water Heater Leak Cleanup Midvale UT Costs
  - Preventing the Next Appliance Flood
  - Water Heater & Appliance Leak FAQ
  - Appliance Leak in Midvale? Stop the Spread Now
- **Mobile wide elements:** table(s) [400]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### water-leak-detection — `/water-leak-detection`

- **H1 (1):** Local Water Leak Detection & Moisture Mapping in Midvale, UT 84047
- **Heights:** desktop 10191px · mobile 18982px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 34 · img 4 · table 1 · ul 6 · ol 4 · faq 1 · links 11 · body text 10396 chars
- **Counts (mobile):** p 34 · img 4 · table 1 · ul 6 · ol 4 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~629px
  - “How do you find a hidden water leak in a Midvale home without opening walls?” — p 30 · img 3 · table 1 · lists 9 · ~8303px
  - “Water Leak Detection FAQ” — p 5 · img 0 · table 0 · lists 0 · ~744px
- **H2s (16):**
  - How do you find a hidden water leak in a Midvale home without opening walls?
  - Signs You Have a Hidden Leak
  - The Simple Meter Test
  - Hidden Leak Detection Midvale: Our Tools
  - Leak Behind Wall: Where Midvale Leaks Hide
  - Slab Leaks and Under-Floor Leaks
  - How to Know Walls Are Dry
  - Moisture Mapping Midvale Utah: Reports for Insurance and Repairs
  - What Happens After We Find the Leak
  - Leak Detection for Condos, Rentals and Businesses
  - Hidden Leaks by Midvale Home Type
  - Leak Detection or a Plumber: Who to Call First?
  - Seasonal Leak Checks for Midvale Homes
  - What Water Leak Detection Midvale UT Costs
  - Water Leak Detection FAQ
  - Suspect a Hidden Leak? Find It Before It Spreads
- **Mobile wide elements:** table(s) [427]px wide in a 390px viewport — inside `.table-wrap` overflow-x:auto, swipeable (OBS-1).

### window-well-flooding — `/window-well-flooding`

- **H1 (1):** 24/7 Window Well Flooding Cleanup in Midvale, UT 84047
- **Heights:** desktop 9648px · mobile 17657px · **Overflow:** desktop no · mobile no · **Broken local images:** desktop 0 · mobile 0
- **Counts (desktop, in `<main>`):** p 37 · img 4 · table 1 · ul 2 · ol 2 · faq 1 · links 7 · body text 10148 chars
- **Counts (mobile):** p 37 · img 4 · table 1 · ul 2 · ol 2 · faq 1
- **Sections (`<section>` in `<main>`, in order):** 3 sections
  - “(no heading)” — p 4 · img 1 · table 0 · lists 1 · ~661px
  - “Why do Midvale window wells fill with water and flood the basement?” — p 33 · img 3 · table 1 · lists 3 · ~7726px
  - “Window Well Flooding FAQ” — p 5 · img 0 · table 0 · lists 0 · ~841px
- **H2s (12):**
  - Why do Midvale window wells fill with water and flood the basement?
  - What to Do the Minute a Window Well Overflows
  - Window Well Leak Into Basement Midvale: The Usual Causes
  - Basement Bedrooms and Egress Windows
  - How We Clean Up Window Well Flooding
  - Water Coming Through Basement Window Midvale: When It's More Than Rain
  - Preventing the Next Window Well Flood
  - Midvale's Two Window Well Seasons
  - Window Well Problems by Midvale Home Type
  - What Window Well Flooding Midvale UT Cleanup Costs
  - Window Well Flooding FAQ
  - Window Well Flooded? Get It Handled Today

## Screenshot inventory

All 62 files under `qa/uiux-render/` (full-page PNG, after slow scroll). Sizes are as captured:

- `home-desktop-full.png` — 4,652,362 bytes
- `home-m390-full.png` — 4,361,046 bytes
- `about-desktop-full.png` — 1,602,419 bytes
- `about-m390-full.png` — 1,318,966 bytes
- `basement-flooding-cleanup-desktop-full.png` — 2,545,382 bytes
- `basement-flooding-cleanup-m390-full.png` — 2,111,511 bytes
- `burst-pipe-water-damage-desktop-full.png` — 2,761,400 bytes
- `burst-pipe-water-damage-m390-full.png` — 2,235,870 bytes
- `ceiling-water-damage-desktop-full.png` — 2,310,296 bytes
- `ceiling-water-damage-m390-full.png` — 1,919,851 bytes
- `commercial-water-damage-desktop-full.png` — 2,780,468 bytes
- `commercial-water-damage-m390-full.png` — 2,297,610 bytes
- `condo-apartment-water-damage-desktop-full.png` — 2,707,122 bytes
- `condo-apartment-water-damage-m390-full.png` — 2,215,974 bytes
- `contact-desktop-full.png` — 1,383,295 bytes
- `contact-m390-full.png` — 1,030,441 bytes
- `crawl-space-water-damage-desktop-full.png` — 2,484,059 bytes
- `crawl-space-water-damage-m390-full.png` — 2,071,177 bytes
- `disclaimer-desktop-full.png` — 833,685 bytes
- `disclaimer-m390-full.png` — 590,229 bytes
- `emergency-water-extraction-desktop-full.png` — 2,775,386 bytes
- `emergency-water-extraction-m390-full.png` — 2,245,840 bytes
- `hardwood-floor-cabinet-drying-desktop-full.png` — 2,615,237 bytes
- `hardwood-floor-cabinet-drying-m390-full.png` — 2,148,423 bytes
- `locations-cottonwood-heights-ut-desktop-full.png` — 3,051,857 bytes
- `locations-cottonwood-heights-ut-m390-full.png` — 2,375,850 bytes
- `locations-magna-ut-desktop-full.png` — 3,025,013 bytes
- `locations-magna-ut-m390-full.png` — 2,398,892 bytes
- `locations-south-salt-lake-ut-desktop-full.png` — 2,866,398 bytes
- `locations-south-salt-lake-ut-m390-full.png` — 2,472,342 bytes
- `midvale-water-sewer-emergency-contacts-desktop-full.png` — 1,624,364 bytes
- `midvale-water-sewer-emergency-contacts-m390-full.png` — 1,413,438 bytes
- `mold-remediation-desktop-full.png` — 2,708,258 bytes
- `mold-remediation-m390-full.png` — 2,292,067 bytes
- `privacy-policy-desktop-full.png` — 853,457 bytes
- `privacy-policy-m390-full.png` — 726,655 bytes
- `resources-basement-flooding-spring-snowmelt-utah-desktop-full.png` — 1,870,074 bytes
- `resources-basement-flooding-spring-snowmelt-utah-m390-full.png` — 1,656,468 bytes
- `resources-can-mold-grow-in-utah-desktop-full.png` — 1,804,494 bytes
- `resources-can-mold-grow-in-utah-m390-full.png` — 1,579,540 bytes
- `resources-frozen-pipes-midvale-desktop-full.png` — 1,921,794 bytes
- `resources-frozen-pipes-midvale-m390-full.png` — 1,644,543 bytes
- `resources-upstairs-unit-leak-who-pays-utah-desktop-full.png` — 1,831,986 bytes
- `resources-upstairs-unit-leak-who-pays-utah-m390-full.png` — 1,653,403 bytes
- `resources-winterize-swamp-cooler-utah-desktop-full.png` — 1,735,529 bytes
- `resources-winterize-swamp-cooler-utah-m390-full.png` — 1,594,551 bytes
- `sewage-backup-cleanup-desktop-full.png` — 2,666,535 bytes
- `sewage-backup-cleanup-m390-full.png` — 2,229,256 bytes
- `storm-flood-damage-desktop-full.png` — 2,760,873 bytes
- `storm-flood-damage-m390-full.png` — 2,259,810 bytes
- `swamp-cooler-leak-water-damage-desktop-full.png` — 2,667,027 bytes
- `swamp-cooler-leak-water-damage-m390-full.png` — 1,869,532 bytes
- `terms-of-use-desktop-full.png` — 618,347 bytes
- `terms-of-use-m390-full.png` — 531,436 bytes
- `water-damage-repair-desktop-full.png` — 1,845,217 bytes
- `water-damage-repair-m390-full.png` — 1,633,437 bytes
- `water-heater-leak-cleanup-desktop-full.png` — 2,108,303 bytes
- `water-heater-leak-cleanup-m390-full.png` — 1,747,093 bytes
- `water-leak-detection-desktop-full.png` — 2,157,115 bytes
- `water-leak-detection-m390-full.png` — 1,836,637 bytes
- `window-well-flooding-desktop-full.png` — 2,175,790 bytes
- `window-well-flooding-m390-full.png` — 1,885,606 bytes

Total: 62 files, 128,091,036 bytes (122.2 MB). Crops used for visual checks live in `qa/uiux-render/crops/` (hero/cards/table/footer regions).

## Files

- Findings (this file): `qa/uiux-render-2026-11-13.md`
- Raw metrics: `qa/uiux-render-data.json` (31 routes × desktop/mobile, incl. per-image `naturalWidth`/displayed size and per-section element counts)
- Screenshots: `qa/uiux-render/*-desktop-full.png`, `qa/uiux-render/*-m390-full.png` (62 files)
- Audit script: `qa/uiux-render-audit.py` (serves nothing; expects the server on port 8341)
- Server: `qa/linkfix-serve.py 8341` (unchanged, reused as-is)
