# PASS D — CONTENT VERBATIM + IMAGES — Midvale UT (10x testing)

- Date: 2026-11-10 ~21:17–21:45 PKT. Tester: Pass D (independent).
- Scope: frozen doc vs built export ONLY. No site code/content/CSS/images edited.
- Sources: `frozen-doc.txt` (Google Doc "Midvale UT" 1ZmyWIOGUbUoaM-LRuffoWeO9xmojFAQLLaJDlYhRaDQ, homepage-only), `out/` (final static export), `public/images/heroes/` + `public/images/cards/`.
- Method: own fresh script `qa/10x/pass-d-diff.py` (written from scratch for this pass; prior-round scripts NOT reused). Images viewed by pixels: 2 PIL contact sheets (all 40) + 12 individually at full size. Metadata: exiftool on all 40 + byte-scan. No live browser used (file-based pass; no HTTP needed).
- Prior-round claims were treated as claims only and re-verified, not trusted.

## 1. VERDICT

**PASS D — PROBLEMS: 1** (one minor, real, reproduced — see P1 below). Everything else passed.

## 2. WORD-DIFF — HOMEPAGE (frozen-doc.txt vs out/index.html visible text)

- Checked: **126 items, 126 OK, 0 missing, 0 changed.**
- Counting rule: every non-empty doc line (headings, paragraphs, list items, table cells split on `|`, trust-band segments split on `·`, button labels as separate items) checked as a contiguous normalized string against homepage visible text (alt attributes excluded — they are not visible text). Meta Title + Meta Description checked separately against the `<head>` tags.
- Meta Title: verbatim, 72ch — `Water Damage Restoration Midvale UT | 24/7 Emergency Crew Dispatched Now`. Meta Description: verbatim.
- Cost ranges: **5/5 verbatim** — $1,000–$4,500 (extraction/drying 1–2 rooms), $2,500–$9,000 (basement), $1,500–$6,500 (burst pipe), $3,000–$12,000 (sewage), $1,500–$6,000 (mold small–mid).
- Category table: **3/3 rows verbatim** — Category 1 (clean) / burst supply line, water heater, fridge line; Category 2 (gray) / washer, dishwasher, toilet overflow without waste; Category 3 (black) / sewer backup, storm runoff, river or canal water.
- H1 on homepage: `24/7 Water Damage Restoration in Midvale, UT 84047` — doc H1 verbatim.

### Script errors owned (NOT site defects)
1. First run flagged 3 false "CHANGED": the two button labels were checked as one joined string (they are two separate `<a>` elements), and one sentence failed on `Damage .` — a space my own text extractor inserts where the period sits outside the link anchor. Fixed: check button labels separately; normalize space-before-punctuation on both sides. Re-ran: 126/126.
2. First run parsed 0 service pairs: paragraph lines carry their trailing `Anchor (/slug/)` annotation on the same line, so my "ends with `.`" test failed. Fixed: strip the annotation first. Re-ran: 16/16.
3. Slug matcher then missed 7 pairs where the doc H3 differs from the link-anchor text (e.g. H3 "Burst & Frozen Pipe Cleanup" vs anchor "Burst Pipe Water Damage"). Fixed: take the slug from each paragraph line's own annotation. Re-ran: 16/16 matched.

## 3. PER-PAGE VERBATIM TABLE (linked pages: doc H3 + summary paragraph only)

| Route | Doc title on page | Doc summary paragraph | Extra visible body text |
|---|---|---|---|
| /emergency-water-extraction | OK | OK verbatim | none |
| /basement-flooding-cleanup | OK | OK verbatim | none |
| /window-well-flooding | OK | OK verbatim | none |
| /burst-pipe-water-damage | OK | OK verbatim | none |
| /sewage-backup-cleanup | OK | OK verbatim | none |
| /water-heater-leak-cleanup | OK | OK verbatim | none |
| /swamp-cooler-leak-water-damage | OK | OK verbatim | none |
| /ceiling-water-damage | OK | OK verbatim | none |
| /crawl-space-water-damage | OK | OK verbatim | none |
| /hardwood-floor-cabinet-drying | OK | OK verbatim | none |
| /condo-apartment-water-damage | OK | OK verbatim | none |
| /commercial-water-damage | OK | OK verbatim | none |
| /storm-flood-damage | OK | OK verbatim | none |
| /mold-remediation | OK | OK verbatim | none |
| /water-leak-detection | OK | OK verbatim | none |
| /water-damage-repair | OK | OK verbatim | none |
| /locations/cottonwood-heights-ut | OK (doc line) | OK verbatim | none |
| /locations/south-salt-lake-ut | OK (doc line) | OK verbatim | none |
| /locations/magna-ut | OK (doc line) | OK verbatim | none |
| /midvale-water-sewer-emergency-contacts | OK | OK verbatim — "For sewer backups, the Midvale Water & Sewer Emergency Contacts page lists who to call about the public line." | **P1 — 3-sentence builder Note (see §6)** |

- Independent confirmation: a second sweep stripped every doc sentence + all known template chrome (header/nav/footer/trust chips/buttons/breadcrumb) from all 21 pages' visible text. The ONLY remaining sentences site-wide are the 3 Note sentences on the contacts page. All other leftovers were `<title>`-tag fragments and H1-suffix fragments, not content.
- H1 note (clarification, not a defect): inner-page H1s are the doc title + ` in Midvale, UT` (e.g. `Emergency Water Extraction in Midvale, UT`) and location H1s are `Water Damage Restoration <City>, UT`. The suffix is composed of doc words; no new factual claim. The prior round's "H1 verbatim" wording is loose — the H1 is a derived heading, not the literal doc H3.

## 4. SITEWIDE CONTENT SWEEP (all 21 routes, visible text)

- Em/en dashes (`—` / `–`): **0 pages**.
- Dangling "See and" / "See .": **0 pages**.
- Button 1 = number only `(385) 337-3560`: **21/21** (2 instances per page, hero + final CTA). Button 2 = `Request Emergency Help`: **21/21**.
- Phone: ONLY `(385) 337-3560` anywhere in `out/` HTML (22 files incl. 404.html). No (918)/(636)/(801) or any other number.
- Invented-claim words (licensed, certified, guaranteed/guarantee, 5-star, award-winning, #1, top-rated, BBB, fully insured, warranty): **0 hits** on any page. ("Best chance" is doc-verbatim; "IICRC S500" is doc-verbatim.)
- Real-job-photo claims ("real photo", "actual job", "our work", "job photo", "photos of our", "on-site photo", "taken on the job", etc.): **0 hits** in visible text, alts, or HTML. Nothing claims any image is a real job photo.
- Cross-site contamination (Tulsa/Plano/Chesterfield/Pleasant Grove/Lancaster/Fort Myers/Naples/Edmond): **0 hits** in `out/` HTML.
- FAQ/schema, canonicals, sitemap, overflow, performance: out of Pass D scope (Passes A–C); not re-checked here and no claim made.

## 5. IMAGES — PER-IMAGE TABLE (40/40)

Method: dimensions + KB + md5 measured from the real files; `out/images/` copies md5-matched to `public/` (40/40 match). All 40 viewed by pixels (contact sheets `qa/10x/sheets/heroes-sheet.jpg`, `qa/10x/sheets/cards-sheet.jpg`) + 12 individually at full size (leak-detection card + hero, storm hero, home hero, Cottonwood hero, window-well hero, sewage hero, Magna hero, emergency hero, mold card, swamp-cooler card, commercial hero). Alt text taken from the actual `<img>` tags in `out/` HTML. Metadata: exiftool on all 40 (only File/RIFF/Composite tags — no EXIF/XMP/C2PA/prompt/generator/GPS) + byte-scan. The byte-scan's 3 raw `XMP` hits were MY script's false positive: the bytes sit inside compressed VP8 payload surrounded by binary noise (offsets verified), no `<x:xmpmeta` packet, exiftool reports no XMP chunk on those files. Metadata verdict is CLEAN for all 40.

### 5a. Heroes — 21/21, all 1600×1066, all <200KB, 21 unique md5

| File | Dims | KB | md5 (12) | Topic / place verdict (pixels) | Alt verdict | Metadata |
|---|---|---|---|---|---|---|
| home.webp | 1600×1066 | 114.9 | da1e8639b3f9 | PASS — crew extracting flooded living room, Wasatch peaks through windows, truck unit at door | PASS — matches pixels exactly | clean |
| emergency-water-extraction.webp | 1600×1066 | 132.1 | b51c98453ca9 | PASS — crew + truck-mounted unit, hoses in flooded basement | PASS | clean |
| basement-flooding-cleanup.webp | 1600×1066 | 101.9 | ef9e2a75bc91 | PASS — flooded finished basement, worker + pump | PASS | clean |
| window-well-flooding.webp | 1600×1066 | 96.7 | 0b42ea2150f3 | PASS — snowmelt pouring through basement bedroom window, bed beside | PASS | clean |
| burst-pipe-water-damage.webp | 1600×1066 | 133.3 | 4306531bde73 | PASS — split copper pipe spraying in opened wall cavity | PASS | clean |
| sewage-backup-cleanup.webp | 1600×1066 | 122.6 | afa4dad0ce74 | PASS — crew in PPE cleaning sewage in bathroom; respirator markings illegible, no wordmark | PASS | clean |
| water-heater-leak-cleanup.webp | 1600×1066 | 74.5 | 254f4964a1b3 | PASS — leaking water heater + copper pipes, wet floor | PASS | clean |
| swamp-cooler-leak-water-damage.webp | 1600×1066 | 136.8 | ee9dbf0dc4e2 | PASS — rooftop swamp cooler on wet roof deck | PASS | clean |
| ceiling-water-damage.webp | 1600×1066 | 77.4 | 38f47f7dd113 | PASS — sagging stained ceiling, bucket, icicles at snowy window | PASS | clean |
| crawl-space-water-damage.webp | 1600×1066 | 127.6 | e5a2a0b04fb1 | PASS — technician, headlamp, dirt crawl space | PASS | clean |
| hardwood-floor-cabinet-drying.webp | 1600×1066 | 107.5 | 2ba4534aa7b0 | PASS — kitchen, drying mats + air movers on hardwood | PASS | clean |
| condo-apartment-water-damage.webp | 1600×1066 | 97.5 | 05ed27c1bb4e | PASS — leak through stacked-unit hallway ceiling, crew | PASS | clean |
| commercial-water-damage.webp | 1600×1066 | 123.5 | e8d4b67a4110 | PASS — dark restaurant after hours, chairs up, air movers + dehumidifier on wet carpet; wall pictures are mountain scenes, no legible text | PASS | clean |
| storm-flood-damage.webp | 1600×1066 | 120.0 | 716763d711fd | PASS w/ nit — flooded garage + storm runoff + car in rain exact; background hills read desert-red/sagebrush (see nit N1) | PASS | clean |
| mold-remediation.webp | 1600×1066 | 126.9 | b5dfe999d194 | PASS — containment sheeting + worker in PPE | PASS | clean |
| water-leak-detection.webp | 1600×1066 | 58.9 | be6966b10dc8 | PASS — technician, thermal camera (heat blobs only, no digits/letters), moisture probe, wet wall | PASS | clean |
| water-damage-repair.webp | 1600×1066 | 31.0 | 95a532fc1e15 | PASS w/ nit — newly rebuilt empty room, fresh floor/trim, work light; plain/bare (see nit N2) | PASS | clean |
| midvale-water-sewer-emergency-contacts.webp | 1600×1066 | 99.0 | 141b90222351 | PASS — utility truck, amber lights, wet street at night, manhole | PASS | clean |
| cottonwood-heights-ut.webp | 1600×1066 | 182.1 | 900a47435d20 | PASS — snowy bench homes below steep snowy Wasatch canyons; best place fit on site | PASS | clean |
| south-salt-lake-ut.webp | 1600×1066 | 115.4 | 9289cf8e466b | PASS — apartments + warehouses at dusk, wet street | PASS | clean |
| magna-ut.webp | 1600×1066 | 182.0 | 1633d2404e37 | PASS — historic brick Main Street storefronts + older homes, mountains, wet street; no legible signage | PASS | clean |

### 5b. Cards — 19/19, all 1200×675 except 3 at 1200×800, all <200KB, 19 unique md5

| File | Dims | KB | md5 (12) | Topic / place verdict (pixels) | Alt verdict | Metadata |
|---|---|---|---|---|---|---|
| emergency-water-extraction.webp | 1200×675 | 63.2 | eb5ebf14ac4d | PASS — submersible pump + hose in standing water | PASS | clean |
| basement-flooding-cleanup.webp | 1200×675 | 83.6 | e73c95860e50 | PASS — wet carpet/pad pulled back | PASS | clean |
| window-well-flooding.webp | 1200×675 | 119.5 | 404048811497 | PASS — window well half full of snowmelt water + ice | PASS | clean |
| burst-pipe-water-damage.webp | 1200×675 | 100.8 | dbe94e644a6a | PASS — frozen burst pipe joint spraying, ice | PASS | clean |
| sewage-backup-cleanup.webp | 1200×675 | 73.5 | 0ab85616734c | PASS — worker in PPE cleaning around floor drain | PASS | clean |
| water-heater-leak-cleanup.webp | 1200×800 | 48.5 | aebf4febd7c3 | PASS — corroded valve dripping on wet concrete (heater itself out of frame; see nit N3) | PASS (valve is plausibly the heater drain valve) | clean |
| swamp-cooler-leak-water-damage.webp | 1200×800 | 79.3 | b2e77e5013c5 | PASS — drain pan overflowing onto wet roof deck; exact alt match | PASS | clean |
| ceiling-water-damage.webp | 1200×675 | 28.1 | 66bd3e2904c4 | PASS — brown stain spreading, drip forming | PASS | clean |
| crawl-space-water-damage.webp | 1200×675 | 97.5 | cae9336ccb22 | PASS — wet joists + standing water, dirt crawl space | PASS | clean |
| hardwood-floor-cabinet-drying.webp | 1200×675 | 51.0 | 350183d1408e | PASS — drying mat + hose on cupped hardwood | PASS | clean |
| condo-apartment-water-damage.webp | 1200×675 | 35.3 | a691b89e081a | PASS — water dripping from ceiling light fixture into bucket | PASS | clean |
| commercial-water-damage.webp | 1200×675 | 46.2 | 88abe93f3de5 | PASS — air movers + dehumidifier on wet commercial carpet | PASS | clean |
| storm-flood-damage.webp | 1200×675 | 101.1 | 8b530de59b8d | PASS — sandbags + sump pump in muddy runoff water | PASS | clean |
| mold-remediation.webp | 1200×675 | 49.2 | aef3d0a800c6 | PASS — HEPA scrubber + ducting beside containment sheeting; no brand | PASS | clean |
| water-leak-detection.webp | 1200×800 | 42.2 | d0b4fe5cf513 | **PASS — REGENERATION VERIFIED: blank dark meter display, NO "EXTECH" wordmark, NO digits; thermal camera shows orange/blue heat pattern only, no legible text** | PASS | clean |
| water-damage-repair.webp | 1200×675 | 51.1 | 292c52793644 | PASS — fresh drywall texture + new white trim being finished | PASS | clean |
| cottonwood-heights-ut.webp | 1200×675 | 156.6 | 34f2fb48ecba | PASS — snowy bench homes below canyons | PASS | clean |
| south-salt-lake-ut.webp | 1200×675 | 74.0 | 04995fb1c485 | PASS — apartment blocks + warehouse buildings | PASS | clean |
| magna-ut.webp | 1200×675 | 68.0 | b30041366e1e | PASS — older brick homes + storefronts, historic Main Street | PASS | clean |

- Repeat check: **40 unique md5, 0 duplicates** (hash-level, not filename). No hero/card shares a file with another slot.
- Weights: max 182.1KB (cottonwood hero), min 28.1KB (ceiling card). **0 images ≥200KB.**
- "AI" word: 0 in any filename, path, or alt. No brand wordmark or readable text found in any of the 40 images at full-size inspection (12 individual) or sheet inspection (all 40).
- Wrong-city cues: none clear — no palm trees, skylines, or out-of-state signage. See nit N1 only.
- All 40 images are generated illustrations (per prior round; no real-job-photo claim anywhere on the site — verified in §4).

### Nits (not defects)
- N1 — `heroes/storm-flood-damage.webp`: background hills through the garage door read desert-red rock + sagebrush (southern-Utah look). Main subject is exact, and the Oquirrh foothills west of the valley are genuinely arid/rocky, so this is ambiguous, not a wrong-city cue. Not counted.
- N2 — `heroes/water-damage-repair.webp`: rebuilt room is empty/plain (work light, fresh floor, mountain view). On-topic, just bare. Not counted.
- N3 — `cards/water-heater-leak-cleanup.webp`: frame shows the corroded dripping valve only; the heater body is out of frame. Alt ("Corroded water heater valve…") still describes what is shown. Not counted.

## 6. PROBLEMS

### P1 (MINOR) — Builder placeholder Note visible on the contacts page — non-doc text on a verbatim-only page
- Route/file: `/midvale-water-sewer-emergency-contacts` — `out/midvale-water-sewer-emergency-contacts.html` (visible body text, "Note:" block).
- Evidence (verbatim from the page): "Note: the full emergency-contact list for this page is not in the source document yet. It will be added here when that list arrives. No phone numbers have been added in the meantime."
- Why it counts: the page's rule is verbatim-summary-only; this is 3 sentences of builder meta-text that appear nowhere in `frozen-doc.txt`, and my chrome-stripped sweep confirms it is the ONLY non-doc visible text on the entire site.
- Why it is minor, not major: it invents no facts, no phone numbers, no claims, and no false promise — it honestly says the list is missing. But it is user-facing build-status text on a page that should read as finished.
- Fix (for the builder, not done here — Pass D tests only): delete the Note block; the page then carries only its one verbatim doc sentence + template chrome.

## 7. FILES PRODUCED (this pass only)
- `qa/10x-pass-d.md` (this file)
- `qa/10x/pass-d-diff.py` + `qa/10x/pass-d-diff.log` + `qa/10x/pass-d-linked.log` (fresh diff script + outputs)
- `qa/10x/sheets/heroes-sheet.jpg`, `qa/10x/sheets/cards-sheet.jpg` (pixel-triage contact sheets)

PASS D — PROBLEMS: 1
