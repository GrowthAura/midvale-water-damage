# Midvale — header nav + slim footer + legal noindex (2026-11-16)

Owner orders: (1) "footer piyra krdye... just important dall bus ur hata dye baqki"
(footer pretty, only the important things, remove the rest); (2) "header ma
areas wala dall dye usko link dye ur menu ma services dall dye us ma sari
services just jo important hye 5 6 baqki footer ma ur areas ma areas then
about us contact us ur then janam privacy policies no index" (header: Areas
link + Services menu with the 5-6 important services; the rest in the footer;
Areas in the footer; About + Contact; legal pages noindex).

## What changed (local only — commit + push pending at time of writing)

### Header — Services menu + Areas link (components/site.tsx)
- Nav is now: Home | Services ▾ (dropdown) | Areas | phone button.
- MENU_SERVICES (6, the important ones — my pick, stated so he can swap):
  emergency-water-extraction, water-damage-repair, basement-flooding-cleanup,
  burst-pipe-water-damage, sewage-backup-cleanup, mold-remediation.
- Areas links to the homepage #areas section (/#areas, prefetch={false} —
  the section already has id="areas", same target the location-page
  breadcrumbs already use).
- Dropdown: click-toggle, closes on Escape / outside click / navigation.
  Mobile: static indented list inside the open hamburger panel.
- The old inline HEADER_SERVICES (2 links) is gone.

### Footer — slim (components/site.tsx + app/globals.css)
- REMOVED: Google Maps iframe (320px) + the 5-column link grid.
- New: brand + 24/7 line + big copper "Call (385) 337-3560" button on top;
  then compact inline rows with dot separators: Services (the other 10),
  Areas (3 locations), Company (About, Contact), Resources (5 blogs),
  Legal (Privacy, Terms, Disclaimer); base bar unchanged verbatim.
- Why the blogs keep a footer row: the 5 blog pages have ZERO body-text
  inbound links — dropping them would orphan them (0-orphans rule).
  The guide page is body-linked 3x, so it needs no footer link.
- Footer heights: desktop 1,281px → 898px; mobile 2,642px → 1,979px.
  (Still long on mobile because every link keeps its 48px tap target —
  SEO FIX 1 2026-11-13 P2-2, deliberately not reduced.)
- FooterSwitch no longer takes showMap / computes isArea (map gone).
  Stale comment in app/locations/[slug]/page.tsx updated.
- The JSON-LD `hasMap` Google Maps URL stays (schema data, not a visible
  map) — 2 occurrences on the homepage (script + RSC payload), expected.

### Legal pages noindex (app/[slug]/page.tsx)
- generateMetadata: robots = { index: false, follow: true } for
  privacy-policy, terms-of-use, disclaimer; all other flat routes stay
  { index: true, follow: true }.
- Deliberately NOT changed: sitemap still lists all 31 URLs (his call if
  he wants the 3 legal URLs out of the sitemap too); llms.txt unchanged;
  footer links to the legal pages stay (noindex ≠ nofollow — they stay
  crawlable and non-orphan).

## Verification (local Pages export, NEXT_PUBLIC_SITE_URL = Pages URL)
- Build exit 0. Routes 31/31, H1==1 on all.
- Header: Services button + 6 menu links + Areas link on ALL 31 pages.
- Footer: all 23 footer links on ALL 31 pages. Map iframes 0.
- Orphans: 0 (min inbound 3, home inbound 90). Self-links 0 in body.
- Robots: legal 3 = "noindex, follow"; other 28 = "index, follow".
- Sitemap 31 locs, 0 localhost. Overflow 0 @1440 and @390.
- VIEWED: desktop header + open dropdown (clean, 6 services); mobile menu
  open + Services expanded (clean, indented, Areas below); desktop footer
  (clean rows); mobile footer (brand + call button + stacked rows, clean).
- DOM probe: footer-brand present + visible (34px desktop / 68px mobile);
  footer-phone button clientWidth == scrollWidth (175px, no overflow).
- Checker notes (own catches, fixed in the checker, not the site): the
  first footer-link check missed the leading "/" on service slugs; the
  first orphan check mapped the basePath root to "" instead of "/"; the
  Areas href renders as /midvale-water-damage#areas (no slash before # —
  Next's normal form for hash links, same as the old /#faq links).

## Open (his call)
- The 6 menu services are my pick — he can swap any.
- Sitemap: keep the 3 noindex legal URLs listed, or remove them (28)?
- Push: main + gh-pages + (new) Cloudflare auto-deploy — on his word.
