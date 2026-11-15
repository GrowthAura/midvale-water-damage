# Midvale Cycle 4 FIX — Independent Re-verification — 2026-11-14

**Verdict: READY — PROBLEMS 2 (P1 0 / P2 0 / P3 2).**
Both Cycle 4 problems are closed by the fix. The two remaining problems are P3 polish items (one new, one carried/disclosed). Nothing blocks a clean close.

Scope: independent re-verification only. Read-only — no source, image, alt, export, push, deploy, DNS, or token touched. All numbers below are my own measurements from my own scripts (`qa/reverify4fix-*`).

## 0. Method note — one invalid run caught and discarded

My first reuse run (`qa/reverify4fix-reuse.py`, killed mid-run; then `reverify4fix-reuse2.py` first pass) returned `flags=0` for **every** target — including the Chesterfield live file against its own corpus entry. That is impossible for a working net, so I treated the run as invalid instead of reporting it: the corpus list had been built with relative `./` paths and was resolved against the wrong cwd, so every corpus entry failed to open. I fixed the path resolution, added an explicit corpus-sanity check (key live files must be present) and a hash-error counter, and re-ran from fresh disk reads. The valid run is `qa/reverify4fix-reuse.json` + `qa/reverify4fix-reuse2.log`. The invalid run's numbers are discarded, not reported as results.

## 1. P1-1 CLOSED — mold-remediation-2 replaced (4176541 → 4098781)

Installed files verified by sha256 + bytes against the fix claims — all match exactly:

| File | Claimed | Measured |
|---|---|---|
| `public/images/body/mold-remediation-2.webp` | `78f9d749…`, 26,986 B | `78f9d74984201b2d228374ea7b05af4c9afd4f95b1ae993c0241307d099d7321`, 26,986 B ✓ |
| `public/images/body/mold-remediation-2-400.webp` | `a517c214…`, 10,704 B | `a517c214dde8fe198403e37ff423b0953d76350adcae1af5d71d56f0d6d11897`, 10,704 B ✓ |
| Export copies in `out-cycle4/images/body/` | same shas | identical shas ✓ |
| Served bytes (local server, 200) | same shas | 800w + 400w both sha_match true ✓ |
| EXIF | 0 | 0 on all 4 installed files; info keys only `loop`/`background` ✓ |
| Dims | 800×450 / 400×225 | exact ✓ |

Alt in `lib/body-images.json` (`/mold-remediation`, index 1, afterH2 4, sticky) is the new text verbatim; old alt ("fogging a living room…") is 0× in the export. New alt appears 4× in built `mold-remediation.html` (alt + schema); old alt 0×.

### Corrected reuse net (my own, fresh disk reads)

Corpus: installed/exported images everywhere in `~/workspace` matching the specified globs (`*/public/images`, `*/images`, `*gh-pages*/images`, `*/out*/images`, `*/export*/images`, `*/dist*/images`, `*/build*/images`), excluding every `*midvale*` path and qa/candidates/raw/tmp/design dirs. **10,231 files, 0 hash errors** (fix worker reported 11,111 — the difference is my corpus excludes `assets/img` dirs, e.g. ~32k Pleasant Grove export copies; the specified globs do not include `assets/img`. The lowest flag that lives in `assets/img` was checked explicitly instead — see §1.3).

- New mold 800w + 400w + source + install crop: **md5 hits 0**; aHash8 ≤12 flags exist (89) but **minimum aHash16 among them 48** (source minimum 40) — decisively in the different-photo band (same ≈ 0–2, different ≈ 25+).
- Old bad shas (`73a15608…`, `82389941…`) are **0× in the corpus and 0× in `public/images/body/`** — the bad installs are gone from public/ and from every installed/exported copy the net covers.

### Control — the net catches the old photo (VALID)

The old bad install no longer exists on disk, so I reconstructed it from the Cycle 4 p3 log's documented source + crop band (`qa/opt4-p3-candidates/4176541.jpg`, 1200×801, band y0=63..738 → 800×450 WebP q82). The reconstruction (`qa/reverify4fix-bad-mold-recon.webp`, 25,842 B) has sha256 **exactly `73a156085b8ff5118dec2ffaf6c1d42dc34afbe82f7a7c2246b3df6c1953522a`** — byte-identical to the documented bad install. That reconstruction flags Chesterfield live **`aHash8 0 / aHash16 0`** (both `chesterfield-gh-pages/images/…` and `chesterfield-water-damage/out/images/…` copies). The raw 4176541 source vs the same Chesterfield file is a8 8 / a16 33 (different crop band — expected, not a control failure; the install-band reconstruction is the control). **Control reproduces: the net catches the exact reuse the Cycle 4 item-2 net missed.**

### Kill evidence for the first pick 4098760 — REPRODUCED

- `4098760.jpg` source vs Biohazard live `technician-bathroom-disinfection-oklahoma.jpg`: **a8 0 / a16 0**; corpus flags min a16 0 (public + out copies). The first pick was live on Biohazard — the kill is real.
- Filename net: `*4098760*` = 0 hits outside Midvale (its Biohazard install is descriptively named, so only the hash net catches it — which is why the corrected net matters).

### 4098781 is NOT 4098760 — viewed pixels + hashes

- Viewed full-size: 4098781 source = PPE worker (white suit, respirator, goggles, blue gloves) lifting a black sofa cushion in a bright living room, monstera plant, window light. 4098760/Biohazard = same worker in a **bathroom** with a pump sprayer, wiping a faucet, mirror + patterned tile. Different room, different action, different photo.
- Explicit pairs: 4098781 source vs Biohazard **a8 40 / a16 153**; install crop vs Biohazard **a8 21 / a16 93**; vs Chesterfield 4176541 **a8 46 / a16 167**. All far outside the same-photo band. (These reproduce the fix worker's numbers exactly.)
- Filename net: `*4098781*` = **0 hits anywhere outside Midvale**. Log net: `photos/4098781` = 0 hits in all 8 sites' qa dirs. No live install of 4098781 anywhere.

### 1.3 Lowest-flag adjudication (viewed pixels)

The lowest aHash flag for the installed mold files is Apopka `wet-flooring-water-damage-apopka.jpg` (**a8 6 / a16 35** — it lives under `assets/img/`, outside the specified-glob corpus, which is why my corpus minimum reads 48; the fix worker's 35 is reproduced exactly by explicit pair). Viewed full-size: it is a close-up of rubber boots + a scrub brush on a muddy wet floor — visually nothing like the PPE-worker crop. Coarse-hash artifact; **DIFFERENT**. Next flags (Tulsa river barge a16 40, Plano moisture-meter a16 48, Tulsa mold-wall a16 49) are unrelated photos.

### Relevance — P3-2 (carried, disclosed by fix worker)

The new mold photo is subject-correct for `/mold-remediation` (PPE remediation worker in a real bright living room, afterH2 4, sticky) but shows PPE furniture-handling, **not active fogging** — weaker on treatment action than the killed photo. No clean fogging photo exists outside the two contaminated families (4176xx = the killed photo's family; 40987xx = Biohazard's 4098760). This is the best clean candidate; a real job photo would beat it. Graded **P3** (not a reuse, not a wrong photo).

## 2. P2-1 CLOSED — water-damage-repair-1 replaced (5493659 → 6474123)

| File | Claimed | Measured |
|---|---|---|
| `public/images/body/water-damage-repair-1.webp` | `d1fdf52d…`, 9,302 B | `d1fdf52d0bdf243fd57f953afd6d89400897c0a940523281ab04869dff385ec5`, 9,302 B ✓ |
| `public/images/body/water-damage-repair-1-400.webp` | `06293b32…`, 3,710 B | `06293b3297c5bc19d925499b84995e2cf67bb86cd118ca9ba581a0dd2ad2d495`, 3,710 B ✓ |
| Export copies + served bytes (200) | same shas | identical / sha_match true ✓ |
| EXIF | 0 | 0 on both; dims 800×450 / 400×225 exact ✓ |

Alt in `lib/body-images.json` (`/water-damage-repair`, index 0, afterH2 2, split) is the new text verbatim; old alt ("drywall stilts…") 0× in the export. New alt 4× in built `water-damage-repair.html`.

- Reuse net: source **md5 0, 4 flags, min a16 60** (Tulsa toilet-overflow photo — different; reproduces the fix worker's 60 exactly); install crop + both installed files **md5 0, 0 flags**.
- Old bad shas (`c6ece3c4…`, `060cf540…`) are **0× in the corpus and 0× in `public/images/body/`**.
- Filename net: `*6474123*` = **0 hits anywhere outside Midvale**. Log net: `photos/6474123` = 0 hits in all 8 sites' qa dirs.
- Explicit pairs vs Plano Blackland live 6474308 (`site/assets/img/drywall-repair-after-water-damage-plano-tx.jpg` + `.webp`): source **a8 31 / a16 105–106**; install crop **a8 24 / a16 96–97**. Definitively different photos — viewed full-size: Plano's is a front view of the same worker smoothing a wall with a trowel by a window; ours is a back view smoothing compound along a wall-ceiling corner over green drywall + white patches. Same shoot, different photo. **Alt describes the rendered photo accurately** (worker, trowel, wall-ceiling corner, green drywall, white compound patches — all visible in the crop).

## 3. P3-1 (NEW) — mold alt describes the source, not the visible crop

The new mold alt — *"A worker in a white protective suit, respirator and blue gloves lifting a sofa cushion in a bright living room"* — describes the **source** photo accurately (all of it is visible in `qa/opt4-fix-candidates/4098781.jpg`: blue-gloved hands lifting the black cushion). But the installed 800×450 crop (band y0=100) cuts the frame at the worker's waist: **no sofa cushion and no blue gloves are visible in the rendered image** — I verified this on the installed file itself and on my own in-slot screenshots at 1440px and 390px (currentSrc `-400`, nw 400/351). A screen reader / Google sees an alt claiming an action and objects that are not in the picture. The photo itself is fine and subject-correct; only the alt overclaims for the crop. **P3.** Recommended one-line fix (coordinator's call): reword the alt to what the crop shows, e.g. a PPE worker in a white suit and respirator leaning over in a bright living room — or re-crop to include the cushion/gloves. Not a reuse, not a wrong photo, does not block READY.

## 4. Export + regression (out-cycle4, rebuilt fresh)

Export freshness: `mold-remediation.html`, `water-damage-repair.html`, `sitemap.xml` all dated 2026-11-14 12:37 UTC, after the installs (12:24–12:35). New shas + new alts present, old shas/alts 0 (checked across all built HTML). 28 mid600 files. Sitemap 31 locs = 31 routes; base `https://growthaura.github.io/midvale-water-damage` (31 refs); `robots.txt` Sitemap line on the same base; localhost 0 in sitemap/robots/both fixed pages; double-slash 0. `basement-flooding-cleanup-3.webp` sha `3c3282f4…` unchanged. `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` unchanged. 404.html present (32 built HTML files = 31 routes + 404).

Served render (real Chromium, Playwright, `qa/reverify4fix-render.py` → `qa/reverify4fix-render.json`):

| Check | Measured |
|---|---|
| Routes 200 | **31/31** |
| H1 == 1 | **31/31** |
| Overflow | **0 routes** (1440px) |
| Console errors | **0** |
| Images | **107/107 loaded** with a proper slow scroll (see note below) |
| Schema JSON-LD | **254 blocks, 0 parse errors**; contentUrls 107/107 |
| FAQ | **142/142** (schema `Question` blocks; visible `.faq-item` divs, answers present in `<main>` text) |
| Links | **0 broken / 0 self-links in `<main>` / 0 orphan sitemap routes / 0 missing asset refs** (static audit of all built HTML) |
| Button 2 | **31/31 @320 and 31/31 @390** |
| Bogus URL | real **404** status (python http.server default body — the server cannot serve the site's own 404.html; status is what was verified) |
| Hero sample @550px | home `home-mid600.webp` w 550 ✓; mold `mold-remediation-mid600.webp` w 550 ✓; repair hero served the `-m` variant (533w) — item 1 was already fully verified; no discrepancy found on the sample, full 496-probe matrix not redone |
| Fixed slots in place | mold `-400` + repair `-400` served at 1440 and 390; my own element screenshots viewed (`qa/reverify4fix-slot-{mold,repair}-{1440,390}.png`) — correct new photos in both slots |

Measurement notes (all resolved, none are site defects):
- My first render pass reported images 87/107 — a **measurement artifact**: lazy images below the fold had not loaded under my fast scroll. A slow scroll + 2.5 s wait (`qa/reverify4fix-imgprobe.py`) loads **all 107** (nw 400/244, complete true); the `-3` files also fetch HTTP 200 directly.
- My first render pass reported FAQ 0 — my selector counted `<details>` elements; this site's FAQs are `.faq-item` divs. Schema `Question` blocks = 142, matching `lib/pages-data.json` (142 FAQs).
- Rendered `<main>` word counts (e.g. mold 1,684) are lower than a naive pages-data word sum (1,859) because that sum counts block `type` tokens (`p`/`h2`/`h3`…) as words. The real fullness evidence is static: **1,013/1,013 content strings present verbatim** in the built HTML (the single "missing" string in my first pass was a link-annotation rendering artifact — the words are all present, the `/sewage-backup-cleanup/` path renders as a link, not parenthetical text). Rendered `<main>` innerText equals static `<main>` text exactly (mold 1,684/1,684, repair 1,531/1,531). **Fullness 31/31 FULL, verbatim 0 missing.**
- Failed requests 3 = the Google Maps embed (`google.com/maps?...output=embed`) — the sandbox has no external internet. Not a site defect.

## 5. Pack

`~/workspace/your_files/midvale-opt-cycle4-review.pdf` **exists: 62,420,945 B, modified 2026-11-14 12:56 UTC (17:56 PKT)** — changed vs the original Cycle 4 pack (62,422,681 B, 11:32), consistent with the parallel refresh having landed (4 shots re-taken, PDF rebuilt). I did **not** verify the pack's contents page by page — that is the refresh agent's scope; the file's presence/size/mtime is what I checked.

## 6. Carried notes (not problems of this fix)

- **Sewage-3 alt (pre-existing working-tree change, not the fix worker's):** `git diff lib/body-images.json` shows the sewage-backup-cleanup-3 alt changed from HEAD's "aerial view of a suburban neighborhood…" to "A gloved hand scrubbing a toilet bowl…". I viewed the image: it **is** a gloved hand scrubbing a toilet with a disinfectant bottle beside it — the working-tree alt is correct and HEAD's was wrong. A correct earlier-round fix; no action.
- The `-400` variants remain untracked in git (pre-existing state, noted by the fix worker); the export uses the files on disk, so no build impact.
- The two fixed slots' photos are the best clean candidates Pexels has in the exact context (see P3-2); a real job photo would beat both.

## Files produced (mine)

- `qa/reverify4fix-reuse2.py` + `qa/reverify4fix-reuse.json` + `qa/reverify4fix-reuse2.log` — corrected reuse net (10,231-file corpus, fresh disk reads; includes the byte-identical bad-install reconstruction `qa/reverify4fix-bad-mold-recon.webp`, sha `73a15608…`)
- `qa/reverify4fix-render.py` + `qa/reverify4fix-render.json` + `qa/reverify4fix-render.log` — served regression (31 routes)
- `qa/reverify4fix-imgprobe.py` — slow-scroll image/FAQ probe resolving the 87/107 artifact
- `qa/reverify4fix-shots.py` + `qa/reverify4fix-slot-{mold,repair}-{1440,390}.png` — in-slot screenshots, viewed
- `qa/reverify4fix-corpus.txt` / `qa/reverify4fix-corpus.sh` — corpus file list (42,615 installed/exported images found workspace-wide; 10,231 inside the specified globs)
- `qa/reverify4fix-reuse.py` — superseded first attempt (relative-path bug; kept for the record, results discarded)
