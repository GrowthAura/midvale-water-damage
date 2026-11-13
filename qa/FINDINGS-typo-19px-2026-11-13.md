# Typography round — body 18px → 19px (Midvale) — 2026-11-13 ~06:00 PKT

Worker: typography only. File changed: `app/globals.css` ONLY. No image, manifest, push, or deploy.
Export: `npm run export` exit 0 (all 31 routes). Served `out/` locally under `/midvale-water-damage/` (port 8931, stopped after verification).

## CSS changes (old → new)
| Rule | Old | New |
|---|---|---|
| `body` font-size | 18px | 19px |
| `p, li, td, th` | 18px | 19px |
| `.lead` | 18px | 19px |
| `table` | 18px | 19px |
| `.hero-trust` | 18px | 19px |
| `.trust-band p` | 18px | 19px |
| `.contact-form input/textarea` | 18px | 19px |
| `.contact-form .radio-row input` | 18px | 19px |
| Comment "Body copy is never below 18px" | 18px | 19px |

Inherits verified at 19px (computed, real Chromium): `.hero p.intro`, `.card-body p`, FAQ answers (p/li), contact labels/legend (inherit from body, no explicit size).
Headings unchanged (computed): h1 44/34/24, h2 32/28, h3 24.

## Deliberately left below 19px (chrome, not body copy)
- `.brand-text` / `.brand-city` 18px (15px @<=360px) — header brand
- `.main-nav a` 18px — header nav
- `.header-phone` 18px — header call button
- `.eyebrow` 18px (14px @<=360px, load-bearing for Button 2) — hero kicker
- `.breadcrumb li` 18px — nav breadcrumb
- `.card-link` 18px — card link chrome
- `.panel-tag` 18px — image-panel label
- `.steps li::before` 18px — step counter numeral
- `.footer-brand` / `.footer-h` 18px — footer fine print
- `.sticky-bar a` 18px — mobile call bar
- `.btn` 18px @<=360px only — equal-height button rule (desktop .btn already 19px, untouched)

## Verification (real Chromium via Playwright, served export)
- Button 2 ("Request Emergency Help") scroll-0: **31/31 @320** (worst bottom 497.2px, viewport 844) and **31/31 @390** (worst bottom 766.8px). Worst pages @both: /condo-apartment-water-damage and /resources/basement-flooding-spring-snowmelt-utah. No hero-spacing fix needed — at ≤600px buttons sit above the intro (flex order), so the taller intro cannot push Button 2 down; the 19px bump moved nothing above the buttons.
- Overflow: **0 on all 31 pages @320/390/1440** (max scrollWidth−clientWidth = 0).
- Console errors: **0** across all 93 page loads. No page errors.
- Computed fonts: body 19px (93/93), p 19px (93/93), li 19px (90/93 — 3 None = pages with no matching li), card p 19px (3/3 where present), contact input 19px (3/3 viewports). `.lead` has no instances on the site (rule changed anyway, harmless).
- Visual spot checks: contact form @390 (labels/inputs clean, no overflow) and emergency-water-extraction @1440 (hero, equal buttons, trust line, H2 all clean). Screenshots: `qa/typo-contact-form-390.png`, `qa/typo-longpage-1440.png`.

## Script errors owned
1. First verification run died at page 27/31 (`TargetClosedError`, Chromium closed mid-run) — root cause: the VM `/tmp` tmpfs (512M) was 100% full (490M `/tmp/pg-mech-test`, another worker's data — NOT deleted). No results were saved (dump was end-of-run only).
2. Rerun fixed it: `domcontentloaded` + selector wait instead of `networkidle` (footer Maps iframe never idles), incremental per-page JSON save, per-page try/except, `--disable-dev-shm-usage`, `TMPDIR` pointed at `qa/tmp-pw/`. Completed 31/31.
3. The rerun's final font-summary print crashed on `sorted()` with a None (pages without `.card-body p` / `.lead`) — cosmetic only; the font counts were recomputed from the saved JSON and are reported above.

## Artifacts
- Script: `qa/typo-verify-19px.py` · Results JSON: `qa/typo-verify-19px-results.json` · Screenshots above.
- Temp server (port 8931) stopped; `qa/tmp-pw/` removed after the run.
