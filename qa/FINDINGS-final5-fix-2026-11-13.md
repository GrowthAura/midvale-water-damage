# STAGE 5 FIX — FINAL FRIENDLY CHECK P2s FIXED — FINDINGS

**Date:** 2026-11-13 ~12:17–12:35 PKT (fix agent, single agent — no children)
**Scope:** Fix the 2 P2 card-photo/alt mismatches from Stage 5 (qa/FINDINGS-final-friendly-2026-11-13.md) + decide P3-1 (mold photo), then fresh targeted re-verification.
**Verdict: PROBLEMS 0 — WHOLE 6-HOUR WATCHDOG CHAIN DONE, BUILD READY FOR RE-PUSH** (re-push on his word + token only).
**No push made. No deploy, no token, no DNS. Local only.**

## 1. The 2 fixes (both P2s — one-photo swaps each)

### Fix 1 — cards/south-salt-lake-ut.webp (P2-1)
- **Before (wrong):** UTA TRAX Blue Line train — parent + Stage 5 coordinator both viewed it full-size. Original backed up: `qa/final5-fix/orig-backup/south-salt-lake-ut.webp` (sha256 `5ff26569…9022`, 149,334 B).
- **Hero verified first:** `public/images/heroes/south-salt-lake-ut.webp` viewed full-size by me — apartment block with lit windows/balconies (left) + warehouse buildings with roll-up doors (right) on a wet street at dusk. Matches its alt exactly: "Apartment and warehouse buildings in South Salt Lake, Utah at dusk".
- **New card:** center 16:9 crop of that hero (1600×1066 → 1600×900) resized to 1200×675, WebP q82. sha256 `120eb46562c2c4a10bf2d452543e79f357c4871b0aca3b14a331f4da66ded1c6`, 75,946 B (was 149,334 B — lighter). EXIF 0, ICC 0, XMP 0.
- **Viewed full-size after the swap (file + rendered homepage element screenshot `qa/final5-fix/card-rendered-ssl.png`):** apartment block + warehouses at dusk. Matches card alt exactly: "Apartment blocks and warehouse buildings in South Salt Lake, Utah". Train gone.

### Fix 2 — cards/magna-ut.webp (P2-2)
- **Before (wrong):** newer suburban subdivision with garages + white picket fence + snowy mountains — parent + Stage 5 coordinator both viewed it full-size. Original backed up: `qa/final5-fix/orig-backup/magna-ut.webp` (sha256 `0b37a9e4…1078`, 135,012 B).
- **Hero verified first:** `public/images/heroes/magna-ut.webp` viewed full-size by me — older brick storefronts with awnings + lit shop windows (left), older homes (right), historic Main Street at dusk with mountains behind. Matches its alt exactly: "Older homes on historic Main Street in Magna, Utah at dusk".
- **New card:** center 16:9 crop of that hero resized to 1200×675, WebP q82. sha256 `a9fe9a67c55eb8fed89326302d767dd7c266d53f4fa6a8dd537afea9c81ae98f`, 119,830 B (was 135,012 B — lighter). EXIF 0, ICC 0, XMP 0.
- **Viewed full-size after the swap (file + rendered homepage element screenshot `qa/final5-fix/card-rendered-magna.png`):** brick storefronts + older homes on Main Street at dusk. Matches card alt exactly: "Older brick homes and storefronts on historic Main Street in Magna, Utah". Subdivision gone.

**Reuse note:** both new cards are crops of the site's OWN page heroes (same page, same subject) — not another site's image. No cross-site reuse is possible. No code changed (same filenames/paths); card alts in `lib/content.ts:452–453` were already correct and are untouched.

## 2. P3-1 decision — mold-remediation-2.webp LEFT AS-IS
- Current photo re-viewed: worker in white protective suit + respirator + blue gloves treating a room with a fogging hose. Subject is correct and its alt is exact ("A worker in a white protective suit, respirator and blue gloves treating a room with a fogging hose"). Only washed-out (mean saturation 0.0475, re-measured).
- Pexels check (search page fetched 200 this time — the old 403 block did not apply): 6 candidates downloaded and **viewed full-size**, ALL rejected on topic:
  - 2414303 — foggy forest. 32497163 — home inspector at a crawl-space hatch. 10567236 — household "MULTI-PURPOSE CLEANER" spray bottle on a desk. 14965464 — street cleaner pressure-washing outdoor stone steps. 28576635 — gloved hands wiping a wall with sponge/spray (household cleaning). 35290675 — plumber working on a pump.
  - None is a mold-remediation fogging photo. No stronger fogging photo exists in this search — per the brief, no wrong photo forced. P3-1 stays open as a cosmetic observation, not a defect.

## 3. Fresh targeted re-verification (fresh export, this round)
- Export: `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage` (no trailing slash), exit 0. Served on `/midvale-water-damage/` (port 8350, `qa/linkfix-serve.py`; server stopped after). Data sha256 unchanged: `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f`.
- **Static (re-ran W1's `qa/final5-static.py` fresh → `qa/final5-fix-static.json`): 11/11 checks PASS** — fullness 31/31 FULL (46,379 main / 51,060 visible words; empty [] / thin []), verbatim 0 missing normalized / 0 changed (2,980 segments; 165 annotation tokens = expected link rendering: 143 body links + 22 dedupes), FAQ 142/142, tables 43/43, links 162 (143 body + 19 card; broken {} / orphans [] / self-links 0; all 31 routes curl 200), paren 0, localhost 0 (HTML + `_next` JS), double-slash 0, robots Allow:/ + no Host: + sitemap 31 locs, 404 exactly 1 noindex, 31/31 exactly 1 index,follow, JSON-LD 178 exact (parse errors 0, contentUrl 31/31 200, doubled subpath 0).
- **Render (`qa/final5-fix-render.py` → `qa/final5-fix/final5-fix-render.json`, 3 pages × 1440/390/320):** H1 1/page all 9; overflow 0 all 9; console 0 all 9; failed local requests 0 all 9; hero Button 2 scroll-0 all 9 (worst 738px @390 SSL vs 844 fold; @320 worst 519px vs 568).
- **Button 2 full sweep (31/31 × @320 + @390):** 31/31 scroll-0 both widths — worst 556px @320 (condo, 12px headroom, holds) and 768px @390. Below-fold: none.
- **Cards in the rendered homepage:** both element screenshots viewed (see §1); SSL card loads 1200×675 after scroll (currentSrc correct); Magna card loads 1200×675. Both `src` paths are the single-prefix card URLs.

## 4. Script artifacts adjudicated (not defects — owned plainly)
1. **First render run's Button 2 bottoms (10,716px etc.):** my script picked the LAST "Request Emergency Help" in the DOM — the footer CTA, not the hero button. Re-measured the FIRST match (hero button): all scroll-0. Script bug, not a site defect.
2. **SSL card `naturalWidth: 0` on first read:** lazy-load timing — the card sits far down the homepage (y≈8631); the measurement ran before the image finished loading after `scrollIntoView`. Re-measured after scroll + 2.5 s wait: 1200×675 loaded, and the element screenshot taken in the same run already showed the photo. Timing artifact, not a broken image.
3. **`pkill -f "linkfix-serve.py 8350"` matched my own shell (SIGTERM 15):** the pattern string appears in my own command line. Re-ran with the bracket trick (`linkfix-serve[.]py`) — server stopped cleanly (http=000 after). Harmless; same self-match pattern the SEO-fix-2 agent owned.

## 5. Chain status — DONE
Stages 0–5 all closed with PROBLEMS 0 on their final verification: photo-fill + 19px, UI/UX, SEO audit 1 + fix, SEO audit 2 + fix, schema + fix + re-verification, final friendly check + this fix. **The build is ready for re-push — on his word + token only.** Remaining known observations (not problems, carried): mobile LCP 2.9–3.7 s lab (re-measure on real hosting), Maps embed needs a real-network eyeball after push, Button 2 headroom @320 only ~12px on condo (watch item), header nav 3 links, weakest contrast 5.65:1 (AA pass), mold-remediation-2 washed-out (P3-1 above), accepted verbatim tensions (single-item home breadcrumb, 12 over-cap anchors, short legal titles).

## Files
- This findings file: `qa/FINDINGS-final5-fix-2026-11-13.md`
- Static re-run: `qa/final5-fix-static.json` (W1's Stage 5 output preserved as `qa/final5-static-stage5.json`)
- Render: `qa/final5-fix-render.py`, `qa/final5-fix/final5-fix-render.json`, screenshots `qa/final5-fix/*-1440.png`, `*-390.png`, `*-320.png`, `card-rendered-ssl.png`, `card-rendered-magna.png`
- Backups of the 2 wrong cards: `qa/final5-fix/orig-backup/` (south-salt-lake-ut.webp, magna-ut.webp)
- Changed source files: **2 image files only** — `public/images/cards/south-salt-lake-ut.webp`, `public/images/cards/magna-ut.webp`. No code, no data, no alt text changed.
