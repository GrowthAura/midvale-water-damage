# Midvale UT — Live LCP / CLS / FCP measurement (Cycle 2, item 3)

**Date:** 2026-11-14 ~03:35 PKT
**Site:** https://midvale-water-damage.pages.dev (Cloudflare Pages, 31 routes)
**Scope:** measurement ONLY. No site file modified, no push/deploy/DNS.
**Headline: real LCP / FCP / CLS could NOT be measured from this cell — Chromium has no egress here (proven 3 ways, see §1). What follows is the honest curl fallback: TTFB, byte counts, and render-blocking analysis. No LCP/FCP/CLS number in this report is invented — every figure is a measurement actually run, and the unmeasured metrics are labelled NOT MEASURED.**

## 1. Method — and why there is no browser number

- **Attempt 1 — Playwright + system Chromium 153.0.8010.12** (`~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`, Python Playwright, fresh context per run = cold cache, viewports 1440×900 / 390×844, `PerformanceObserver` for LCP/FCP/layout-shift, 2 runs × 6 pages × 2 viewports = 24 navigations). **Result: 24/24 failed — `net::ERR_TUNNEL_CONNECTION_FAILED`.**
- **Attempt 2 — explicit egress proxy with auth** (proxy taken from the cell's own `https_proxy` env var, passed to `chromium.launch(proxy=...)`): same failure on `example.com`, `google.com`, and the live site — so it is **not site-specific**.
- **Attempt 3 — direct, no proxy** (`--no-proxy-server`, proxy env vars emptied): `net::ERR_SSL_PROTOCOL_ERROR`.
- **Control — curl from the same cell, same minute:** 200 on all three hosts (`example.com` TTFB 1.88 s, `google.com` 0.73 s, live homepage 1.28 s). curl reaches the internet; Chromium does not.
- **Conclusion:** this sandbox cell blocks Chromium egress entirely. The `/opt/meta-chromium/chrome` wrapper additionally refuses to start here ("Hatch WebGL domain policy is required for browser startup"). **LCP, FCP, CLS: NOT MEASURED. This is a cell limitation, not a site problem.**
- **Fallback actually run:** `curl` timing + per-resource sizing for the same 6 pages × 2 UAs × 2 runs (script `qa/lcp-measure-curl.py`, raw JSON `qa/lcp-live-curl-2026-11-14.json`; failed browser runs logged in `qa/lcp-live-2026-11-14.json`; downloaded HTML evidence in `qa/tmp-chrome-lcp/`). TMPDIR was pointed at `qa/tmp-chrome-lcp/` throughout; `/tmp` (96% full) was never used by Chromium. Profile junk deleted; 1.8 MB of downloaded HTML evidence kept.

## 2. Per-page table (curl fallback — measured, not browser metrics)

`TTFB` = time to first byte via this cell's egress proxy (see §3 — inflated by the measurement path). `HTML` = page bytes. `Hero` = hero `.webp` bytes actually served (identical file both viewports — §4). `Initial` = HTML + CSS + JS + eager images, **uncompressed** (curl without `--compressed`); real browsers transfer far less via brotli (§5). `Full` = initial + all lazy images. LCP / FCP / CLS columns are **NOT MEASURED** (see §1) — shown as such rather than filled with estimates.

| Page | Viewport | TTFB run 1 / run 2 | HTML | Hero bytes | Initial transfer (uncompressed) | Full page (uncompressed) | LCP | LCP element | FCP | CLS |
|---|---|---|---|---|---|---|---|---|---|---|
| / (home) | desktop 1440×900 | 1,892 / 1,120 ms | 98,353 B | 117,632 B (114.9 KB) | 683,215 B (667 KB) | 1,317,125 B (1.26 MB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| / (home) | mobile 390×844 | 2,777 / 2,113 ms | 98,353 B | 117,632 B (114.9 KB) | 683,215 B (667 KB) | 1,317,125 B (1.26 MB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /emergency-water-extraction | desktop | 1,300 / 1,608 ms | 71,186 B | 135,252 B (132.1 KB) | 675,961 B (660 KB) | 800,665 B (782 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /emergency-water-extraction | mobile | 1,699 / 1,278 ms | 71,186 B | 135,252 B (132.1 KB) | 675,961 B (660 KB) | 800,665 B (782 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /basement-flooding-cleanup | desktop | 1,597 / 2,003 ms | 66,855 B | 139,640 B (136.4 KB) | 676,018 B (660 KB) | 845,454 B (826 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /basement-flooding-cleanup | mobile | 2,310 / 2,087 ms | 66,855 B | 139,640 B (136.4 KB) | 676,018 B (660 KB) | 845,454 B (826 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /mold-remediation | desktop | 1,188 / 896 ms | 68,876 B | 129,972 B (126.9 KB) | 668,371 B (653 KB) | 858,833 B (839 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /mold-remediation | mobile | 1,200 / 966 ms | 68,876 B | 129,972 B (126.9 KB) | 668,371 B (653 KB) | 858,833 B (839 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /burst-pipe-water-damage | desktop | 1,507 / 1,300 ms | 71,591 B | 136,456 B (133.3 KB) | 677,570 B (662 KB) | 841,988 B (822 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /burst-pipe-water-damage | mobile | 2,227 / 2,196 ms | 71,591 B | 136,456 B (133.3 KB) | 677,570 B (662 KB) | 841,988 B (822 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /locations/magna-ut | desktop | 2,666 / 1,092 ms | 75,292 B | 163,358 B (159.5 KB) | 708,173 B (692 KB) | 995,493 B (972 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| /locations/magna-ut | mobile | 1,675 / 1,555 ms | 75,292 B | 163,358 B (159.5 KB) | 708,173 B (692 KB) | 995,493 B (972 KB) | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED |

**Aggregates (24 TTFB runs):** median **1,603 ms**, range **896–2,777 ms**. Desktop median 1,404 ms; mobile median 1,893 ms. **Hero bytes (6 pages):** median 135,854 B (~132.7 KB), range 117,632–163,358 B. **All 6 pages returned HTTP 200 on every run; HTML byte-identical run 1 vs run 2 and desktop vs mobile.**

## 3. What dominates LCP — evidence from the fallback

**1. TTFB dominates, and it is measurement-path noise, not the site.**
Every resource — HTML and every subresource — shows 0.9–3.1 s TTFB through this cell's proxy, with 3× run-to-run variance on the *same* URL (e.g. `/locations/magna-ut` desktop 2,666 → 1,092 ms; home mobile 2,777 → 2,113 ms). A slow origin would be consistently slow; this pattern (everything slow, wildly variable) is the egress-proxy path. A real visitor hits a Cloudflare edge directly, not this proxy. One real site-side note: HTML is served `Cache-Control: public, max-age=0, must-revalidate`, so even real users pay an origin revalidation round-trip for HTML on every visit — but Cloudflare Pages HTML TTFB from a nearby edge is normally tens-to-low-hundreds of ms, not 1.6 s.

**2. Hero bytes are the second LCP cost — and the same file serves mobile.**
Heroes are 115–160 KB each (median ~133 KB), all 1600×1066 `.webp`, preloaded with `fetchpriority="high"` on every page. The preload is good (hero fetch starts with the HTML parse), but on a slow mobile connection a 133 KB hero is still the largest single LCP input after TTFB. **No `srcset` exists anywhere on the site (0/24 images across the 6 pages)** and the HTML is byte-identical for desktop and mobile UAs — mobile downloads the exact same 1600 px hero as desktop. This is the concrete remaining win (Cycle 2 srcset item): a mobile-sized hero (~40–60 KB) would cut the mobile hero payload by ~60%.

**3. Render-blocking JS/CSS is minimal — not the bottleneck.**
One CSS file, 13,421 B (3,814 B brotli). Eight JS files totalling ~454–456 KB uncompressed, but **7 of 8 are `async`** and the one non-async file is `polyfills-…js` with a `noModule` attribute (modern browsers skip it entirely — effective JS ≈ 341–344 KB uncompressed). Nothing heavy blocks first paint. The JS weight (~140 KB brotli, estimated from the measured 31% ratio on the main chunk) affects total transfer and main-thread work, not LCP directly.

**4. CLS: NOT MEASURED, but structurally low-risk (inference only, not a measurement).**
The hero `<img>` carries explicit `width="1600" height="1066"` attributes and all non-hero images are `loading="lazy"` (home: 1 eager / 19 lazy; service pages: 1 eager / 3 lazy), so layout-shift sources are limited. This is a code-structure observation, **not** a CLS reading — a real CLS number still needs a browser run.

## 4. Verdict — is Cycle 1's mobile LCP (2.9–3.7 s) real or lab noise?

**Mostly lab noise — supported, not proven.** The Cycle 1 report itself noted FCP rose by the same factor as LCP with byte-identical heroes, i.e. the whole render pipeline shifted together, which is the signature of CPU/network contention in the measurement environment, not of page weight. This round's independent evidence points the same way:

- TTFB alone is ~1.6 s median *in this cell's measurement path*, with 3× variance — add a ~133 KB hero download on top and a 2.9–3.7 s lab LCP is fully explained by the path, without any page defect.
- The page itself is light where LCP cares: 13 KB CSS, async JS, preloaded hero, lazy below-fold images. Nothing in the measured bytes predicts a 3 s+ LCP on a normal connection.
- **But:** no real LCP number exists yet, so "real-user LCP is fine" is an inference, not a measurement. The honest statement is: **Cycle 1's 2.9–3.7 s is not credible as a real-user figure; the true mobile LCP is very likely well under 2.5 s on a decent connection, and the remaining real optimisation is the mobile hero size (srcset), not TTFB or render-blocking.**

**To close this item properly:** run the ready-made script `qa/lcp-measure.py` (Playwright, PerformanceObserver, 2 runs × 6 pages × 2 viewports, cold cache) on any machine with real internet egress — or run PageSpeed Insights / WebPageTest against `https://midvale-water-damage.pages.dev/` — and compare against the curl baselines above.

## 5. Brotli spot-check (what a real browser actually transfers)

curl `--compressed` (brotli, as a browser negotiates) vs uncompressed:

| Resource | Uncompressed | Brotli | Ratio |
|---|---|---|---|
| Homepage HTML | 98,353 B | 14,602 B | 15% |
| CSS `91ddd4ea44d0af2f.css` | 13,421 B | 3,814 B | 28% |
| Main JS chunk `fd9d1056-….js` | 172,834 B | 54,053 B | 31% |

So the "Initial transfer (uncompressed)" column above (~660–692 KB) overstates real transfer: text assets compress to ~15–31%, putting a realistic initial-load transfer at roughly **~280–330 KB** (HTML ~15 KB + CSS ~4 KB + JS ~140 KB est. + hero 115–160 KB, images don't compress). The JS brotli total is an estimate from the measured chunk ratio, not a per-file measurement.

## 6. Method + tool versions

- **Browser attempt:** Python Playwright + Chromium 153.0.8010.12 (`~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`), `python3 --version` 3.12.3, Node 24.22.1 (not used for measurement). Script: `qa/lcp-measure.py` (kept for re-use on a machine with egress).
- **Curl fallback:** `curl` (system) via `qa/lcp-measure-curl.py`; each page fetched 2× per UA (desktop UA Chrome/153 Linux, mobile UA Chrome/153 Android Pixel 7); every unique subresource (1 CSS, 8 JS, 6 heroes, 15 body images, 18 card images = 48 resources) fetched once and sized. Raw data: `qa/lcp-live-curl-2026-11-14.json`; failed browser log: `qa/lcp-live-2026-11-14.json`; page HTML: `qa/tmp-chrome-lcp/*.html`.
- **Environment:** shared cell, 1.5 CPU / 6 GB; `/tmp` 96% full (512 MB tmpfs) — TMPDIR redirected to `qa/tmp-chrome-lcp/`, profile junk removed after the run.
- **Limits:** no LCP/FCP/CLS; no render screenshots; TTFB figures are proxy-path figures, not real-user figures; JS brotli total is a ratio estimate (see §5).

## 7. Files

- This report: `qa/opt2-lcp-live-2026-11-14.md`
- Curl data: `qa/lcp-live-curl-2026-11-14.json`
- Browser attempt log (24 errors): `qa/lcp-live-2026-11-14.json`
- Scripts: `qa/lcp-measure.py` (browser, re-usable off-cell), `qa/lcp-measure-curl.py` (fallback)
- HTML evidence: `qa/tmp-chrome-lcp/*.html` (24 files, 1.8 MB)
