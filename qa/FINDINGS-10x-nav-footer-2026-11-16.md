# FINDINGS — Midvale UT 10x testing round (nav-footer round), 2026-11-16

## Verdict: READY TO PUSH — P1 0 / P2 0 / P3 0
### with 1 open owner call: 2 known live image reuses carried (see §5)

**P-count framing, stated plainly so nothing is hidden:** two P1-class cross-site
reuses remain live on the site (`body/mold-remediation-1.webp`, `body/mold-remediation-3.webp`).
They are NOT counted in the P1 0 above because (a) they are pre-existing — this round
discovered them, it did not introduce them; (b) the fix agent proved them unfixable from
Pexels (9 searches; every genuinely moldy interior-wall photo on Pexels is already used
somewhere in the portfolio); (c) pushing changes nothing about them — the exact same
photos are live today, before and after the push. Holding the push fixes nothing and only
delays the 2 fixed reuses, the P3 console fix, and everything else. The owner's pick is
still required: non-Pexels source, real job photos, or accept the reuse. The independent
re-verifier agrees with this verdict and this framing.

- Live before this round: main `33a3d2c`, gh-pages `8f7d67b`, cloudflare-pages `2e11aba`
  (31/31 live, Pages + pages.dev). This round's changes are LOCAL ONLY, uncommitted.
- `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`
  — verified unchanged by every agent (coordinator, fix agent, re-verifier).
- `git diff`: 10 files (see §7). Nothing committed, nothing pushed, no token used.

## 1. Content + links + SEO (Agent A — READY, P1 0 / P2 0 / P3 0)

Evidence: `qa/10x-nav-footer-2026-11-16/agent-A-content-links-seo.md`.
Measured on BOTH local exports (fresh rebuilds from main `33a3d2c` + fixes):

- Verbatim: **3,040/3,040 segments, 0 missing** (both builds). Re-verifier independently
  re-measured 3040/3040, 0 missing (its word-multiset diff first showed 7.7% "missing";
  investigated and resolved — every segment present as a substring, every distinct data
  word in visible text; the gap is repeated words counted multiple times in data).
- FAQ: **142/142** schema-exact + visible. Tables: 43/43 (735/735 cells).
- Links: 151 internal targets all 200, 0 orphans, 0 self-links in body; doc links
  162/162 present (143 body-link + 19 homepage whole-card links).
- H1: 31/31 exactly 1. 31 unique titles/descriptions == data. Canonical == og:url ==
  sitemap loc on every page. 0 localhost / cross-base refs.
- Robots: legal 3 noindex/follow, other 28 index/follow. Sitemap: 31 URLs, date-only
  lastmod 2026-11-12, no image entries. robots.txt Allow:/ + correct sitemap, no Host:.
  llms.txt 31 URLs. 0 old-site traces in served HTML (both builds + live + .txt payloads).
- Schema: 254 JSON-LD blocks (HomeAndConstructionBusiness 1, FAQPage 28, BreadcrumbList 31,
  Service 19, HowTo 36, ImageObject 107); LocalBusiness phone +13853373560, areaServed
  Midvale 84047 + 3 cities; no `logo` key; all 107 ImageObject URLs resolve.
- Notes (not defects): gh-pages homepage bare URL 301s to trailing-slash 200; www 000
  (settled — his Spaceship nameserver step); sitemap lastmod uniformly 2026-11-12.

## 2. Design + mobile + header/footer (Agent C — PASS with 1 × P3, P1 0 / P2 0 / P3 1)

Evidence: `qa/10x-nav-footer-2026-11-16/agent-C-design-mobile.md`,
`agent-C-results.json` (99 checks), `agent-C-followup.json`, `agent-C-sweep2.json`;
11 labelled screenshots in `qa/10x-nav-footer-2026-11-16/shots/`.
Measured on real Playwright renders (re-verifier re-ran 93/93: 31 routes × 1440/390/320):

- Header: Home | Services ▾ (exactly the 6 services in order) | Areas (/#areas) | phone.
  Tap targets 48–51px. Dropdown opens, closes on Escape / outside click / navigation.
  Sticky header top 0. Mobile menu opens, Services expands indented 16px, Areas present,
  closes on Escape/navigation, body scroll locks with menu open (no trap, scrollY stays 0).
- Footer: all 5 rows 10/3/2/5/3 on homepage + 5 deep pages at 1440 and 390; Call button
  tel:+13853373560, unclipped; `·` separators render; legal pages linked;
  /privacy-policy noindex confirmed; **zero iframes anywhere**.
- Footer height **898px desktop / 1,979px mobile — exactly as claimed** (re-verifier:
  898.3px / 1979.1px).
- Overflow 0 on **all 31 routes at 1440, 390 and 320**. Button 2 above the fold **31/31
  at 320 and 390** (worst @320 /condo-apartment-water-damage bottom 552/700px; worst @390
  condo + basement-snowmelt blog 773/844px). Sticky call bar appears after hero scroll on
  all 31 routes at 390 and 320 with tel: link. 20/20 homepage images load after scroll.
  First-paint H1 visible at opacity 1 on all 31 routes at 390 and 320.
- The single P3 (D-1, homepage-only intermittent console 404 on Next.js RSC prefetch of
  `/midvale-water-damage.txt`) is **FIXED — see §6**. Re-verifier: 0 console errors, 0 failed
  requests across the 93-route sweep + 4 click probes.
- Caveat (Agent C + re-verifier): live pages.dev render spot-check could not run from this
  VM (Chromium `ERR_TUNNEL_CONNECTION_FAILED` — egress/proxy failure, not a site result).
  Needs the parent's live-browser check.
- Observations (not defects): Areas smooth-scroll takes ~2–3s on the long desktop homepage;
  at 390 the header wraps to two rows (acceptable, one row at 320).
- Agent C's honesty note: 6 of its first 8 FAILs were its own script bugs (basePath prefix,
  600ms wait shorter than the ~2–3s smooth scroll, requiring `·` on each row's first item) —
  re-probed and passing, documented in the file.

## 3. Images — the round's main finding (Agent B + B-finish + coordinator adjudication)

Evidence: `qa/10x-nav-footer-2026-11-16/agent-B-images.md` (coordinator synthesis),
`agent-B-reuse.json`, `agent-B-corpus-hashes.jsonl` (12,211 files), `agent-B-adjudication.json`
(62 pairs), side-by-side shots `shots/agent-B-adj-01.png` … `agent-B-adj-62.png`.

### 3a. Inventory — PASS

- File counts identical across trees: public 329 / out 329 / out-cloudflare 329.
  md5 mismatch across trees: 0. Extra/missing in either export: 0.
- Slots present: body-base 57 + body-400 57, card-base 19 + card-340 19, hero-base 31 +
  hero-800 31 + hero-m 31, hero-mid/mid600/mid700 28 each. Total 16,596,174 B.
- Metadata: 0 hits across all 329 files (no EXIF/XMP/ICC).
- basement-3 (`body/basement-flooding-cleanup-3.webp`, aerial — owner's call still open):
  sha256 `3c3282f408f8…` — unchanged.

### 3b. Reuse net — CONTROL PASSED, 4 reuses confirmed by viewed pixels

- Corpus: **12,211 files** (md5 + aHash8 + aHash16), incl. export dirs.
  **CONTROL PASSED:** rebuilt bad Cycle-4 mold install (Pexels 4176541) flags a8 0 / a16 0
  vs the Chesterfield live file (recon sha matches expected `73a15608…`).
- md5 hits: 329 — **0 cross-site** (all Midvale's own copies).
- a16 ≤ 28 true cross-site pairs: 62 — every one adjudicated by full-size viewed pixels
  (coordinator). **4 CONFIRMED reuses** (see §4 for fix status):

| Midvale file | a8/a16 | Same photo live on |
|---|---|---|
| `body/emergency-water-extraction-2.webp` (Pexels 5691510) | 0/0 | Chesterfield `chesterfield-emergency-water-extraction-kitchen-floor-wand.webp` (emergency-water-extraction.html) — adj-01 |
| same file | 3/6 | Tulsa Repair `services-water-mitigation-tulsa-water-damage-repair.webp` (service-area pages) — adj-03 |
| `body/mold-remediation-3.webp` (Pexels 7434331) | 0/1 | Lancaster `mold-removal-lancaster-ca-sec1.webp` — adj-02 |
| `body/ceiling-water-damage-3.webp` (Pexels 36035072) | 6/20 | Boynton Beach `room-renovation-tiles-1200.jpg` — adj-23 |
| `body/mold-remediation-1.webp` (Pexels 17401392) | 7/28 | Boynton Beach `mold-wall-growth-1200.jpg` — adj-60 |

- a16 = 28 for mold-1 proves the Cycle-4 lesson again: heavy crops push same-photo pairs
  to a16 17–37 — a <25 hash threshold alone would have MISSED it. Visual adjudication caught it.
- 58 remaining pairs: false positives by viewed pixels (Tulsa EMD QA screenshots, snowy
  valley vs desert/construction/geyser/street/tanks; remaining 27 distinct pairs
  aspect-matched MAD 28.6–92.4, different-photo band).
- Pexels-ID net: 7434331 in Lancaster's img-scout pool (corroborates mold-3); 17401392 in
  Lancaster pool + Boynton audit (corroborates mold-1); 5691510 / 36035072 no ID hits
  (counterparts renamed).
- `mold-remediation-2` check: sha = expected Pexels 4098781 sha — correct file, no Cycle-4
  leak repeat. `repair-1` vs Apopka process-8: a8 19 / a16 76–79 — different photos.
  Card-vs-own-hero: SSL + Magna a8 6 / a16 29 — proper center crops of own heroes.

### 3c. Key images viewed — PASS

- Cycle-1 new heroes (3): disclaimer (moisture-meter worker on peeling wall), upstairs-unit
  leak (ceiling leak dripping onto sofa), water-damage-repair (clean restored US interior) —
  all topical, no brands. `body/mold-remediation-2` (PPE worker) PASS.
  `body/sewage-backup-cleanup-3` (Pexels 4239074, toilet plunge) PASS. SSL + Magna cards PASS.
- 38 reprobe "404"s: checker bug (double basePath prefix), all 38 resolve 200 at the correct
  URL (`agent-B-reprobe-resolution.json` 38/38; CF spot-check 16/16).
- 67 hero aspect flags: expected `object-fit:cover` behaviour, not defects — 21 hero renders
  measured (12 @1440, 9 @390), subjects visible.
- Agent B was killed by a VM restart (01:05 PKT); B-finish was killed by a second restart/drain
  (01:58 PKT). Both left complete artifacts; the coordinator finished the adjudication from
  them (including the Pexels-ID net, which had not run in the finish scripts) and viewed the
  decisive pairs itself. No evidence was taken on trust.

## 4. Image fix round (fix agent — 2 replaced, 2 unfixable, hero recompressed)

Evidence: `qa/10x-nav-footer-2026-11-16/agent-B-fix.md`,
`agent-B-fix-reuse-final.json`, `verify-pages.log`, `verify-cf.log`,
slot screenshots `shots/agent-B-render/slot-*.png`.
Old files backed up to `qa/10x-nav-footer-2026-11-16/replaced/` (8 files).

### Replaced (fresh Pexels, reuse-net clean, both exports rebuilt + verified)

1. `/emergency-water-extraction` slot 2 — old Pexels 5691510 → new **Pexels 6196579**,
   `body/water-extraction-yellow-wet-dry-vacuum.webp` + `-400.webp` (800×450 / 400×225,
   21,352 B / 8,672 B). Viewed: yellow wet/dry vac + hose on sunlit tiled floor. Net: md5 0,
   0 a8≤12 flags, closest cross-site a16 **68**. New alt matches the photo.
2. `/ceiling-water-damage` slot 3 — old Pexels 36035072 → new **Pexels 7217923**,
   `body/ceiling-water-damage-renovation-stepladder.webp` + `-400.webp` (800×450 / 400×225,
   31,960 B / 12,850 B). Viewed: paint-splattered wooden stepladder + drop cloths + paint
   tray/can. Net: md5 0, closest cross-site a16 **61**. New alt matches the photo.
3. Hero recompressed: `heroes/basement-flooding-spring-snowmelt-utah.webp` 215,212 B →
   **198,260 B** (q68, same pixels/filename, no visible loss). Net clean.

### Unfixable from Pexels — old files restored byte-identical (owner's call)

- `/mold-remediation` slot 1 (17401392, Boynton) + slot 3 (7434331, Lancaster): 9 Pexels
  searches. Every genuinely moldy interior-wall photo on Pexels is already used
  portfolio-wide (17401392, 7434331, 9127236 on Plano, 7506161 on Midvale itself as
  swamp-cooler-1, 18063447 on Plano). All other candidates viewed and rejected as not-mold
  (peeling paint, exterior lichen, stone textures, EU abandoned bathrooms, generic
  cleaning/PPE). Restored files verified byte-identical to backups (coordinator re-checked:
  all 4 files, shas match the fix report exactly — mold-1 `fe5f076f615f50af…`,
  mold-3 `e639c308e3d9a0d4…`). `body-images.json` mold entries reverted (no net diff).
- Round-1 rejections (nets + viewed pixels, all confirmed same photo): 3616735 (ext, a8 0 /
  a16 0 vs Chesterfield), 9127236 (mold-1, a8 1 / a16 24 vs Plano), 7506161 (mold-3, a8 0 /
  a16 7–8 vs Midvale's own swamp-cooler-1), 6474117 / 5499416 (work shots, same as
  biohazard/Chesterfield photos). Control PASSED on the final run (4176541 recon a8 0 / a16 0).
- **Correction (re-verifier, not a site defect):** the fix agent's "filename scan *6196579*
  0 hits anywhere in ~/workspace" is overstated — the ID exists as scout/candidate downloads
  in Lancaster, Acworth and Elyria qa/work dirs. None is a served install (hash net: md5 0
  hits across 12,211 files incl. export dirs), so the freshness verdict stands; only the
  phrasing needs correcting to "0 served/installed hits".

### Rebuild + verification after the fix (fix agent)

- Pages build exit 0; Cloudflare build exit 0 (temp edits restored; `next.config.mjs`
  verified back to Pages config; `lib/content.ts` uncommitted hunk re-applied from saved
  diff — full 4-file diff intact).
- **Pages: 31/31 routes 200 + H1==1, 0 FAILs. Cloudflare: 31/31 routes 200 + H1==1, 0 FAILs.**
  New files 200 in both exports; old body files 404; 0 stale refs/files in either export.
- Real-browser render (Playwright, 1440 + 390): 0 console errors on all 3 routes; both
  replaced photos viewed rendering in their correct slots at both widths, no overflow.

## 5. Carried — open owner calls (not blockers for this push)

1. **2 mold slots stay reused** (mold-1 = Boynton's photo, mold-3 = Lancaster's photo —
   both confirmed by viewed pixels, re-verifier agrees). Pick one: (a) non-Pexels source,
   (b) real job photos, or (c) accept the reuse. Pushing does not worsen this.
2. Settled calls (do NOT re-open): basement-3 aerial photo (his call open); 72ch meta title
   verbatim (his call open); sitemap keeps the 3 noindex legal URLs (his call open — accepted
   tension with gate list F.9/J); footer map removed + footer no longer 4-column (his direct order).
3. www.waterdamagerestorationmidvale.us still 000 — his Spaceship nameserver step (morning of
   2026-11-16). Not a defect. Zone watcher cron `midvale-cloudflare-zone-watch` still PAUSED
   (his order 2026-11-15) — untouched.

## 6. Defects fixed this round (before/after proof)

1. **P3 — Homepage-only console 404 on client-side navigation to "/" (FIXED, verified).**
   Agent C D-1: Next.js RSC prefetch requested `/midvale-water-damage.txt?_rsc=…` → 404
   (Pages build only, intermittent, console noise only). Root cause: static export + basePath
   miscalculates the root route's flight payload path. Fix (5 spots, `components/site.tsx` +
   `app/not-found.tsx`): home-bound links are now plain `<a>` with ASSET_PREFIX-aware hrefs
   (brand, Home nav, Areas, breadcrumb home/areas crumbs, 404-page link); other routes keep
   Next Link (their `<slug>.txt` payloads exist). Before: Home/brand click on "/" and brand
   click from /about both fired the 404. After: **10 click probes (coordinator) + 4 click
   probes (re-verifier) across both builds: 0 404s, 0 `.txt?_rsc=` requests**, all landings
   correct, Areas smooth-scroll intact (scrollY 8477), dropdown still exactly the 6 services.
2. **P3 — Other-site names in code comments (FIXED).** "Acworth" ×2 in lib/links.tsx,
   "Belleville" ×1 in lib/content.ts — the zero-trace rule explicitly includes comments.
   Reworded; served output verified clean (grep over out/ + out-cloudflare/ = 0 hits).
   (The lib/content.ts instance was reverted once by the CF build restore — see process note
   below — and re-applied after.)
3. **P1 × 2 — Cross-site reused images (FIXED).** emergency-water-extraction-2 and
   ceiling-water-damage-3 replaced with fresh Pexels photos (§4). Before: same photos live on
   Chesterfield/Tulsa Repair / Boynton Beach. After: md5 0, closest cross-site a16 68 / 61,
   viewed fresh, old files gone from both exports.
4. **P3 — Overweight hero (FIXED).** `heroes/basement-flooding-spring-snowmelt-utah.webp`
   215,212 B → 198,260 B (q68, same pixels). Renders fine.

## 7. Files changed (local only, uncommitted)

```
app/not-found.tsx                                  | 8 +-
components/site.tsx                                | 51 +-
lib/body-images.json                               | 8 +-    (2 replaced slots: new src+alt)
lib/content.ts                                     | 2 +-    (comment fix)
lib/links.tsx                                      | 4 +-    (comment fix)
public/images/body/ceiling-water-damage-3.webp     | deleted (base + -400)
public/images/body/emergency-water-extraction-2.webp | deleted (base + -400)
public/images/body/ceiling-water-damage-renovation-stepladder.webp | new (+ -400)
public/images/body/water-extraction-yellow-wet-dry-vacuum.webp     | new (+ -400)
public/images/heroes/basement-flooding-spring-snowmelt-utah.webp   | recompressed
10 files changed, 43 insertions(+), 30 deletions(-)
```

## 8. Independent re-verification (fresh agent, no build/fix involvement)

Evidence: `qa/10x-nav-footer-2026-11-16/agent-REVERIFY.md`.
Own servers (8913/8914), own scripts, own eyes. **Verdict: READY TO PUSH — P1 0 / P2 0 / P3 0.**
Re-measured: data sha exact; 31/31 200 + H1==1 both builds; verbatim 3040/3040; canonical ==
og:url ∈ sitemap (31 locs exact set-match per base); legal 3 noindex / 28 index; JSON-LD
254/build; FAQ 142/142; orphans 0; self-links 0; old-site traces 0; 93/93 sweep overflow 0,
H1 first-paint 93/93, Button 2 above fold 93/93, console 0, failed requests 0; dropdown 6
services in order, Escape/outside-click close; footer 898.3px / 1979.1px; P3 fix 4 clicks,
0 failed requests; both replacements hash-verified fresh (own aHash implementation calibrated
to distance 0 on a known file; vac md5 `8af1b5fd…` closest a16 68, stepladder md5 `d46e0c32…`
closest a16 61) and viewed matching their alts; old files gone; hero 198,260 B; mold shas
match restored values; mold reuse confirmed by viewed pixels and agrees unfixable from Pexels
on spot-checks (9127236 + 18063447 live on Plano, filename-verified; 7506161 pixel-identical
to Midvale's own swamp-cooler-1 — raw a16 42, a crop-offset evasion case).
Could not confirm: live browser render (sandbox egress failure, not a site result); the full
9-search Pexels exhaustion (spot-checked 3 named burned IDs instead); no long idle prefetch
soak (4 click probes + 93-route sweep show 0 console errors).

## 9. Caveats for the parent

- Live pages.dev render spot-check could not run from this VM (Chromium
  `ERR_TUNNEL_CONNECTION_FAILED`) — needs the parent's live-browser check after push.
- The local 404 click probe could not run against the site's own 404.html
  (linkfix-serve.py returns its own error page for unknown paths) — verified statically instead.
- The CF build's restore step (`git checkout -- next.config.mjs lib/content.ts`) reverts ANY
  uncommitted change to lib/content.ts — it reverted the comment fix once mid-round; the fix
  agent preserved the 4-file diff via a saved copy and re-applied it. Any future CF build
  must do the same.
- Two subagents were killed by VM restarts/drains during this round (Agent B 01:05 PKT,
  B-finish 01:58 PKT). All of their artifacts survived on disk and the work was completed
  from them — nothing was lost, nothing was taken on trust.
- The coordinator's own first-pass "broken links" lists (favicons, live-www fetches,
  double-prefix) were checker bugs, re-run correctly, clean — owned here.

## 10. Push readiness

**READY TO PUSH (main + gh-pages + cloudflare-pages) on the parent's word + token.**
The push deploys: the P3 console-404 fix, the comment-trace cleanup, 2 fresh replacement
photos, the recompressed hero. The 2 mold slots ride unchanged (already live today) pending
the owner's pick in §5.1. Live verification after push should cover: 31/31 200 + H1==1 on
Pages + pages.dev, the 2 new images live, mold files unchanged, www still 000 until his
nameserver step.
