# INDEPENDENT RE-VERIFICATION — Midvale UT 10x nav-footer round
**Re-verifier:** independent agent (did not build or fix any of this work). **Date:** 2026-11-16.
**Method:** fresh measurements only — my own crawl script, my own Playwright scripts, my own hash implementation (calibrated against the corpus), viewed pixels. No edits, no rebuild, no push, no token.
**Tree verified as-is:** `~/workspace/midvale-water-damage/`, uncommitted. `git diff --stat` = 10 files (4 code + 4 deleted old images + hero recompressed + `lib/body-images.json`).
**My servers:** Pages build `out/` → http://127.0.0.1:8913/midvale-water-damage/ ; CF build `out-cloudflare/` → http://127.0.0.1:8914/.

## VERDICT: READY TO PUSH — P1 0 / P2 0 / P3 0
Every claim I could test re-measured clean. The push strictly improves the live site (2 of 4 reused images replaced, P3 prefetch 404 fixed, comment traces fixed) and introduces no new defect. **One open owner call remains (see §7): the 2 mold slots stay reused — they are unchanged from what is live today, so pushing does not make the reuse situation worse, but the owner must still decide non-Pexels source / real job photos / accept.**

## 0. Data fingerprint — PASS
`lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` — **matches the required value exactly**. No STOP condition triggered.

## 1. Route / SEO crawl (my own script, both builds) — PASS
- 31/31 routes 200, H1==1 with text == data `h1`, title == data `metaTitle`, meta description == data — **0 bad on both builds**.
- Canonical == og:url on every page; canonical ∈ sitemap locs — **0 bad both builds**. Sitemap locs == expected 31 absolute URLs exactly (Pages base + www base) — **set-match, 0 extra / 0 missing, both builds**. Lastmods all `2026-11-12` (date-only).
- Robots meta: legal 3 (`/privacy-policy`, `/terms-of-use`, `/disclaimer`) = `noindex, follow`; other 28 = `index, follow` — **0 bad both builds**. robots.txt: `Allow: /` + correct per-build `Sitemap:` line, no `Host:` line. llms.txt: 31 URLs both builds.
- JSON-LD blocks: **254 per build**. FAQ schema Q count == data FAQ count: **142/142 both builds**.
- Link graph: orphans **0** (min inbound 3 per non-home route); body self-links inside `<main>`: **0 both builds**.
- Old-site traces: `rg` over both exports (html/txt/xml) for localhost + Tulsa/Plano/Chesterfield/Apopka/Elyria/Belleville/Acworth/San Bruno/Pleasant Grove/Lancaster/Fort Myers/Naples/McDonough/Boynton/Broken Arrow/Cape Coral: **0 hits**.

## 2. Verbatim — PASS (segment proof re-measured; word-count gap investigated and resolved)
- `qa/reverify-segments.py` re-run by me on `out/`: **TOTAL segments 3040, missing 0**. CF variant on `out-cloudflare/`: **3040, missing 0**.
- My own word-multiset diff initially showed 7.68% "missing" — investigated, NOT content loss: on the homepage every data segment is present as a substring (116/116, 0 absent) and **every distinct data word appears in visible text (0 distinct words absent)**. The multiset gap is repeated common words counted multiple times in data (paragraph + list + FAQ repeats) rendered once — a counting artifact, same direction as Agent A's reconciled −0.21% (their doc-word counting method differs from mine). Sample pages (data vs visible-main words, multiset-missing %): home 2319/2115/9.6%, emergency 1947/1797/8.9%, mold 1817/1714/6.9%, can-mold blog 1606/1485/8.7%, about 1015/945/9.7%, ceiling 1749/1636/8.1%. Visible `<main>` words total 47,090 (identical to Agent A's count — cross-check).

## 3. Design / mobile / header / footer (Playwright, real Chromium) — PASS
- Desktop 1440 home (viewed `shots/reverify/reverify-desktop-home.png`): header Home / Services▾ / Areas + phone `(385) 337-3560` tel:+13853373560, `position: sticky, top: 0`. Dropdown opens with **exactly the 6 services in order** (emergency-water-extraction, water-damage-repair, basement-flooding-cleanup, burst-pipe-water-damage, sewage-backup-cleanup, mold-remediation). Escape closes it (aria true→false, links hidden). Outside click closes it. Clicking a dropdown item navigates to `/water-damage-repair`.
- Mobile 390 home (viewed `shots/reverify/reverify-mobile-menu.png`): hamburger opens (`aria-expanded=true`, `#main-nav.open`), 8 menu links incl. the 6 services in order + Areas; Escape closes (class back to `main-nav`). Header wraps to two rows at 390 (brand / hamburger+phone) — acceptable. First-paint H1 visible opacity 1, 34px mobile / 44px desktop.
- Footer (viewed `shots/reverify/reverify-desktop-footer-scrolled.png`): rows **10 / 3 / 2 / 5 / 3** on desktop AND mobile, dot separators render, call button `Call (385) 337-3560` tel:+13853373560, **0 iframes anywhere**, height **898.3px desktop / 1979.1px mobile** (matches claimed 898 / 1979). CF build: same rows, 898.3px, dropdown 6 in order, overflow 0, console 0.
- Sweep 93/93 (31 routes × 1440/390/320): **overflow 0 everywhere; H1 visible at first paint 93/93; Button 2 ("Request Emergency Help", tel:+13853373560) above fold 93/93** — worst @320 `/condo-apartment-water-damage` bottom 552/700; worst @390 `/condo-apartment-water-damage` + `/resources/basement-flooding-spring-snowmelt-utah` bottom 773/844; worst @1440 condo 663/900. **Console errors 0, failed requests 0 across all 93.** Worst-page numbers match Agent C's exactly (cross-check).
- Sticky mobile call bar: after scrolling, `Call (385) 337-3560 · 24/7` block, bottom edge at viewport bottom (844/844), tel:+13853373560.

## 4. P3 404-fix probes — PASS (fix confirmed working)
On the Pages build, 4 real clicks with network+console logging: Home nav from `/`, brand logo from `/`, Home nav from `/about`, brand logo from `/about` — **0 failed requests, 0 console errors, 0 `.txt?_rsc=` requests; all land on `/midvale-water-damage/`**. The pre-fix `/midvale-water-damage.txt?_rsc=…` 404 does NOT reproduce. Agent C's D-1 (intermittent prefetch 404) was observed BEFORE this fix round's code change; it is resolved for the click paths probed. (Limit: no long idle prefetch soak run — see §8.)

## 5. Images — PASS for the 2 replacements + hero; 2 mold slots CONFIRMED still reused (carried owner call, §7)
### Inventory / staleness
- File counts: public 329 / out 329 / out-cloudflare 329 — identical. Old files `emergency-water-extraction-2` + `ceiling-water-damage-3` (base + -400): **gone from both exports, 0 stale refs** (the only `ceiling-water-damage-3` matches in `index.html` are the card image `ceiling-water-damage-340.webp` — substring false positives; `emergency-water-extraction-2` count 0 in `index.txt`).
- Mold files restored byte-identical: sha256 mold-1 `fe5f076f615f50af…` / -400 `6359285936410bbc…`, mold-3 `e639c308e3d9a0d4…` / -400 `b57f04a5b0d8c6b…` — **all 4 match the claimed values exactly**.
- Hero recompressed: `basement-flooding-spring-snowmelt-utah.webp` **198,260 B (≤200 KB)**, renders fine as the homepage hero (viewed in `shots/reverify/reverify-desktop-home.png`).
- Metadata: 0 EXIF/XMP/ICC bytes in the 4 new files + hero (byte scan).

### The 2 REPLACED files — my own hash run (implementation calibrated: LSB packing reproduces the corpus's known-file hashes at distance 0 on a8 and a16)
- `water-extraction-yellow-wet-dry-vacuum.webp` (Pexels 6196579): md5 `8af1b5fdda2c7ed69c5dabd9e2c7a92d` (matches Agent B), **md5 hits 0, a8≤12 flags 0, closest cross-site a16 68** (Plano `wet-attic-reinsulate-split-480.webp`) — reproduces Agent B's 68 exactly. -400 variant: same 68.
- `ceiling-water-damage-renovation-stepladder.webp` (Pexels 7217923): md5 `d46e0c32379258713b153be7dbab8ae4` (matches Agent B), **md5 hits 0, closest cross-site a16 61** (Tulsa `carpet-pad-removal-480.webp`) — reproduces Agent B's 61 exactly. 16 a8≤12 flags, all Elyria `body-blog-elyria-flood-zones-black-river-1` at a8 12 / a16 92–93 (same as Agent B's final JSON — hash-noise, clearly different photo). -400 variant: same 61.
- Viewed pixels (me, full-size): yellow wet/dry vac body + corrugated hose on sunlit tiled floor, US home interior, no legible brand — matches alt exactly. Paint-splattered wooden stepladder + drop cloths + paint tray/can, white walls, wood floor — matches alt exactly.
- Slot renders (Playwright): ext vac loads 400×225 complete on `/emergency-water-extraction`; stepladder lazy-loads to 400×225 complete on scroll on `/ceiling-water-damage`; mold-1 loads 400×225 complete on `/mold-remediation`. **0 console errors on all 3 routes.**

### The 2 MOLD files — confirmed STILL the same photos (viewed pixels, my own eyes)
- `mold-remediation-1.webp` vs Boynton `mold-wall-growth-1200.jpg` (adj-60 side-by-side): identical mold band, crack, stain pattern — **SAME PHOTO, confirmed**.
- `mold-remediation-3.webp` vs Lancaster `mold-removal-lancaster-ca-sec1.webp` (adj-02 side-by-side): identical black mildew streaks and shapes — **SAME PHOTO, confirmed**.
- Both alts still accurate (green/black mold on white block wall; black mildew streaks on light wall).

### "Unfixable from Pexels" — I agree, on the evidence I spot-checked
- Named burned IDs verified genuinely used elsewhere: **9127236** live on Plano as `public/images/mold-wall-9127236.webp` (+400/+800); **18063447** live on Plano as `public/images/indoor-mold-18063447.webp` (+400/+800); **7506161** in Lancaster's img-scout pool AND **viewed pixel-identical to Midvale's own `swamp-cooler-leak-water-damage-1.webp`** (portrait original vs 16:9 band crop — same streaks, crack, speckles; my raw a16 was 42, a crop-offset evasion case, which is exactly why viewed pixels decide). 7506161 is not in Plano public/images — its "used" status is Lancaster pool + this site itself, as Agent B stated.
- I did not re-run the 9 Pexels searches (per task scope); I verified the rejection evidence for the 3 named IDs and the fix agent's list is internally consistent. The "no fitting fresh mold-streak wall photo on Pexels" conclusion stands on that evidence.

### Correction to a claim (not a site defect)
- Agent B wrote the 6196579 filename scan found "0 hits anywhere in ~/workspace". That wording is overstated: `6196579.jpg` exists as downloaded scout/candidate copies in Lancaster `work/img-scout/pool/` + `qa3-staging/cand/`, Acworth `qa/r3-new-images/` + `qa/az-fix-tmp/cand/`, and Elyria `qa/design-A-work/cand/` + `qa/image-place-work/r3-cand/th-vac/`. **None of these is a served/installed copy** (no hit in any `public/images`, `out/`, or export dir; hash net over 12,211 files incl. export dirs: md5 0 hits, closest a16 68). The substantive verdict — not live on any other site — stands; only the "0 hits anywhere" phrasing needs correcting to "0 served/installed hits".

## 6. Live spot-checks (curl; old build as expected) — PASS as far as curl reaches
- gh-pages home **200** (after -L), pages.dev home **200**; H1 verbatim `24/7 Water Damage Restoration in Midvale, UT 84047` on both; `/about` 200 both.
- Sitemap **31 locs** on both hosts; robots.txt correct per host (`Allow: /`, correct `Sitemap:` line).
- Live is the OLD build — local fixes are correctly NOT expected there. www 000 is not flagged (nameserver step pending, per instructions).
- Live browser render could NOT run: Playwright navigation to pages.dev failed in this sandbox (consistent with the known `ERR_TUNNEL_CONNECTION_FAILED` egress failure, not a site result). No live-render verdict claimed.

## 7. THE SINGLE OPEN OWNER CALL (carried, not a new defect)
**2 mold slots remain cross-site reused photos and will ship as-is if this round is pushed:** `/mold-remediation` slot 1 (Pexels 17401392, also live on Boynton Beach mold-after-leak / ac-leak pages) and slot 3 (Pexels 7434331, also live on Lancaster mold-removal pages). Pexels has no fitting fresh replacement (verified §5). Owner's three options, unchanged: (a) non-Pexels source, (b) real job photos, or (c) accept the reuse. Pushing this round does not worsen the situation — these exact photos are already live today — but the call is still open.

## 8. What I confirmed vs could not confirm / honesty notes
- Confirmed by my own measurements: §0–§6 above (data sha, 31/31 routes both builds, verbatim 3040/3040 both builds, FAQ 142/142, links 0/0, schema 254, design sweep 93/93, P3 clicks 0 bad, image hashes reproducing Agent B's 68/61 exactly, mold reuse by viewed pixels, hero ≤200 KB, live curl).
- Could not confirm: live browser render (sandbox egress failure — not a site result); the full 9-search Pexels exhaustion (spot-checked the 3 named burned IDs instead, per task scope); a long idle prefetch soak for Agent C's intermittent D-1 (my 4 click probes + 93-route sweep show 0 console errors, which covers the reported paths).
- My own errors, corrected in-run: my first two sweep runs recorded nothing (key typo `b2bottom` vs `b2_bottom` in MY script); the third run is the valid one. My first dropdown-Escape read used a wrong selector and said "not closed"; a proper aria/offsetParent re-probe shows Escape DOES close it. My first word-diff script undercounted data words (missed nested `segments` in list items) — the segment check + distinct-word check are the valid measurements.

## DEFECT LIST
None. P1 0 / P2 0 / P3 0. One carried owner call (§7).

## HOW TO REPRODUCE
- Crawl: `/tmp/reverify_check.py` → `/tmp/reverify_crawl.json` (my servers 8913 Pages / 8914 CF, both stopped after the run).
- Verbatim: `python3 qa/reverify-segments.py` → 3040/0; CF variant `/tmp/reverify-segments-cf.py` → 3040/0.
- Browser: `/tmp/reverify_browser.py` (header/footer/P3/CF) + `/tmp/reverify_sweep3.py` (93-row sweep) → `/tmp/reverify_browser.json`, `/tmp/reverify_sweep3.json`. Shots: `shots/reverify/`.
- Images: `/tmp/reverify_hash.py` (calibration: LSB packing = distance 0 on known corpus file) — vac a16 68, stepladder a16 61.
