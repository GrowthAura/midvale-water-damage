// Fresh Midvale components — written new for this site. No file copied
// from any past site. Design follows the locked Theme v2 skeleton only
// (header / hero / trust band / cards / process / FAQ / footer / sticky bar).
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { SITE, SERVICES, LOCATIONS, ASSET_PREFIX } from "@/lib/content";
import { HERO_CROP_BP } from "@/lib/hero-crops";

export const TEL_HREF = `tel:${SITE.phoneTel}`;

/* ---------- reveal wrapper: structural wrapper only.
   An earlier version hid content (opacity 0) until scroll + JS; that left
   section headings and the final CTA blank in full-page captures and
   invisible with JS off. Tier-1 motion now lives in card hover + hero
   only — no content is ever hidden. ---------- */
export function Reveal({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <div className={`reveal ${className}`}>{children}</div>;
}

/* ---------- hero buttons: Button 1 and Button 2, exactly equal ---------- */
export function HeroButtons() {
  return (
    <p className="hero-buttons">
      <a className="btn btn-call" href={TEL_HREF}>
        {SITE.phoneDisplay}
      </a>
      <a className="btn btn-help" href={TEL_HREF}>
        Request Emergency Help
      </a>
    </p>
  );
}

/* ---------- photo hero (HERO + A-to-Z ROUND): ONE pattern on all 21 pages.
   Order: breadcrumb (inner pages) -> eyebrow -> H1 (verbatim, exactly 1) ->
   INTRO inside the hero (verbatim) -> the 2 equal buttons -> trust chips.
   The hero image is a darkened photographic background (LCP image, preloaded
   automatically by Next from fetchPriority="high"); the dark shade keeps white text
   high-contrast. Content is never hidden by animation.
   CYCLE 2 SRCSET + MOBILE CROPS: <picture> serves the per-page portrait
   mobile crop (heroes/<slug>-m.webp, aspect matched to that page's 390px
   hero box, media <=700px — the measured crossover where the landscape
   file starts fitting again) and the <img> carries 800w/1600w srcset
   (sizes 100vw). The <picture> wrapper is unstyled/static, so the
   absolute .hero-img keeps .hero-photo as its containing block and the
   shade/content stacking is unchanged.
   CYCLE 3 TWO-WIDTH CROPS: a second, wider 3:4 crop (heroes/<slug>-mid.webp,
   800x1066) serves the mid range where the -m crop degrades (mean visible
   0.657 across 481-767) and the landscape file does not yet fit. Breakpoints
   are PER PAGE (lib/hero-crops.ts, measured 2026-11-14): -m applies to mMax
   (475-575), -mid to midMax (659-767), landscape above. The 3 legal pages
   have midMax null (boxes already ~1.0 wide at 481 — landscape wins right
   after -m) and get no -mid file or source. A blanket <=767 -mid source
   would REGRESS 481 (mid 0.678 vs -m 0.921) and 767 (mid 0.659 vs
   landscape 0.782); the per-page scheme never regresses any page. ---------- */
function variantSrc(src: string, suffix: string): string {
  return src.replace(/\.webp$/, `${suffix}.webp`);
}

export function PhotoHero({
  image,
  alt,
  eyebrow,
  h1,
  intro,
  breadcrumb,
  trust,
}: {
  image: string;
  alt: string;
  eyebrow: string;
  h1: string;
  intro: string;
  breadcrumb?: ReactNode;
  // Trust chips render ONLY when passed (page.trustChips). Null/omitted
  // (tabs 24-31) -> NO trust line, never invented chips.
  trust?: readonly string[] | null;
}) {
  // CYCLE 3: per-hero picture breakpoints (lib/hero-crops.ts). Fallback is
  // the simple scheme (-m <=480, -mid <=767) if a slug is ever missing.
  const heroSlug = image.split("/").pop()?.replace(/\.webp$/, "") ?? "";
  const cropBp = HERO_CROP_BP[heroSlug] ?? { mMax: 480, midMax: 767 };
  // SPEED 2026-11-17 (Fix 1): preload the LCP hero image. Whether Next
  // hoists these <link> tags into <head> is verified from the built HTML
  // after each build (see qa/FINDINGS-speed-best-ever-2026-11-17.md) —
  // if they land in <body> next to the <picture> they are harmless but
  // gain ~nothing, and the fix is judged on the measured LCP delta alone.
  const midMin = cropBp.mMax + 1;
  return (
    <section className="hero hero-photo">
      <link rel="preload" as="image" href={ASSET_PREFIX + variantSrc(image, "-m")} media={`(max-width: ${cropBp.mMax}px)`} fetchPriority="high" />
      {cropBp.midMax !== null && (
        <link rel="preload" as="image" href={ASSET_PREFIX + variantSrc(image, "-mid")} imageSrcSet={`${ASSET_PREFIX + variantSrc(image, "-mid600")} 600w, ${ASSET_PREFIX + variantSrc(image, "-mid700")} 700w, ${ASSET_PREFIX + variantSrc(image, "-mid")} 800w`} imageSizes="100vw" media={`(min-width: ${midMin}px) and (max-width: ${cropBp.midMax}px)`} fetchPriority="high" />
      )}
      <link rel="preload" as="image" href={ASSET_PREFIX + variantSrc(image, "-800")} imageSrcSet={`${ASSET_PREFIX + variantSrc(image, "-800")} 800w, ${ASSET_PREFIX + image} 1600w`} imageSizes="100vw" media={`(min-width: ${cropBp.midMax !== null ? cropBp.midMax + 1 : midMin}px)`} fetchPriority="high" />
      {/* CYCLE 1 UI/UX FIX (C-5): id="hero-image" — the hero ImageObject
          @id (#hero-image) resolves to this real DOM anchor.
          Attrs 1600x1066: every hero file measures 1600x1066 (PIL).
          CYCLE 2: <picture> + srcset — mobile portrait crop <=700px,
          800w/1600w above. Same alt, same photo, no layout change.
          CYCLE 3: two sources — -m to mMax, -mid to midMax (null = no
          -mid source, legal pages). Sources are evaluated in order;
          first match wins. */}
      <picture>
        <source media={`(max-width: ${cropBp.mMax}px)`} srcSet={ASSET_PREFIX + variantSrc(image, "-m")} sizes="100vw" />
        {cropBp.midMax !== null && (
          <source media={`(max-width: ${cropBp.midMax}px)`} srcSet={`${ASSET_PREFIX + variantSrc(image, "-mid600")} 600w, ${ASSET_PREFIX + variantSrc(image, "-mid700")} 700w, ${ASSET_PREFIX + variantSrc(image, "-mid")} 800w`} sizes="100vw" />
        )}
        <img id="hero-image" className="hero-img" src={ASSET_PREFIX + image} srcSet={`${ASSET_PREFIX + variantSrc(image, "-800")} 800w, ${ASSET_PREFIX + image} 1600w`} sizes="100vw" alt={alt} width={1600} height={1066} fetchPriority="high" decoding="async" />
      </picture>
      <div className="hero-shade" aria-hidden="true" />
      <div className="wrap hero-content">
        {breadcrumb}
        <p className="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        <p className="intro">{intro}</p>
        <HeroButtons />
        {trust && trust.length > 0 ? (
          <p className="hero-trust">{trust.join(" · ")}</p>
        ) : null}
      </div>
    </section>
  );
}

/* ---------- header (10X FIX C-O3: mobile had no nav menu — .main-nav was
   display:none <=900px with no hamburger; mobile users could only navigate
   via footer links. Menu button 46px, Escape closes, aria-expanded.)
   2026-11-16 (owner): nav is Home + Services menu (6 important services)
   + Areas (homepage #areas section). The other 10 services live in the
   footer; the guide page is body-linked, so it needs no nav link. ---------- */
const MENU_SERVICES = [
  "emergency-water-extraction",
  "water-damage-repair",
  "basement-flooding-cleanup",
  "burst-pipe-water-damage",
  "sewage-backup-cleanup",
  "mold-remediation",
];

export function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [servicesOpen, setServicesOpen] = useState(false);
  const menuBtnRef = useRef<HTMLButtonElement>(null);
  const dropRef = useRef<HTMLDivElement>(null);
  const menuScrollY = useRef(0);
  const pathname = usePathname();
  // Close the menu and the Services dropdown on navigation.
  useEffect(() => {
    setMenuOpen(false);
    setServicesOpen(false);
  }, [pathname]);
  // Restore the pre-menu scroll position — ONLY on an explicit close
  // (Escape / menu-button toggle), never on navigation: a menu-link click
  // navigates and Next scrolls the new page to top. The restore runs in a
  // double rAF so layout settles and it lands exactly.
  const restoreMenuScroll = () => {
    const y = menuScrollY.current;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => window.scrollTo(0, y));
    });
  };
  useEffect(() => {
    if (!menuOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setMenuOpen(false);
        setServicesOpen(false);
        restoreMenuScroll();
        menuBtnRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [menuOpen]);
  // Services dropdown: Escape closes it (desktop, menu closed); a click
  // outside the dropdown closes it. A service-link click navigates, which
  // closes it via the pathname effect above.
  useEffect(() => {
    if (!servicesOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setServicesOpen(false);
    };
    const onDown = (e: MouseEvent) => {
      if (dropRef.current && !dropRef.current.contains(e.target as Node)) {
        setServicesOpen(false);
      }
    };
    document.addEventListener("keydown", onKey);
    document.addEventListener("mousedown", onDown);
    return () => {
      document.removeEventListener("keydown", onKey);
      document.removeEventListener("mousedown", onDown);
    };
  }, [servicesOpen]);
  // P3-3 scroll lock while the mobile menu is open (2026-11-12): body
  // position:fixed + overflow:hidden (overflow:hidden alone does NOT lock
  // scroll in Chromium). Scroll position is captured here and restored
  // ONLY by explicit closes (Escape / menu-button toggle) via
  // restoreMenuScroll — the cleanup below only clears styles, so a
  // menu-link navigation can never be dragged back to the old position.
  useEffect(() => {
    if (!menuOpen) return;
    menuScrollY.current = window.scrollY;
    const body = document.body;
    body.style.position = "fixed";
    body.style.top = `-${menuScrollY.current}px`;
    body.style.left = "0";
    body.style.right = "0";
    body.style.overflow = "hidden";
    return () => {
      body.style.position = "";
      body.style.top = "";
      body.style.left = "";
      body.style.right = "";
      body.style.overflow = "";
    };
  }, [menuOpen]);
  return (
    <header className="site-header">
      <div className="wrap header-inner">
        {/* P3-1 (10x round 2026-11-16): home links are plain <a>, NOT Next
            Link. The static export carries the home flight payload as
            /midvale-water-damage/index.txt, but a Link to "/" fetches it
            as /midvale-water-damage.txt -> 404 console noise on every
            client-side navigation home (prefetch={false} only stopped
            the prefetch path, not the click path). A plain anchor does a
            clean document load with no RSC fetch. Other routes keep
            Link — their <slug>.txt payloads exist and prefetch fine.
            href is ASSET_PREFIX + "/" so it is /midvale-water-damage/
            on the Pages build and / on the Cloudflare build. */}
        <a className="brand" href={`${ASSET_PREFIX}/`}>
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 32 32" width="30" height="30">
              <path d="M16 3C16 3 6 14 6 20a10 10 0 0 0 20 0C26 14 16 3 16 3Z" fill="#c26a24" />
            </svg>
          </span>
          <span className="brand-text">
            Water Damage Restoration
            <span className="brand-city">Midvale, UT</span>
          </span>
        </a>
        <nav id="main-nav" className={`main-nav${menuOpen ? " open" : ""}`} aria-label="Main">
          <a href={`${ASSET_PREFIX}/`} onClick={() => setMenuOpen(false)}>
            Home
          </a>
          <div className="nav-drop" ref={dropRef}>
            <button
              type="button"
              className="nav-drop-btn"
              aria-expanded={servicesOpen}
              aria-haspopup="true"
              onClick={() => setServicesOpen((v) => !v)}
            >
              Services <span aria-hidden="true" className="nav-caret">▾</span>
            </button>
            <ul className={`nav-drop-list${servicesOpen ? " open" : ""}`}>
              {MENU_SERVICES.map((slug) => {
                const s = SERVICES.find((x) => x.slug === slug)!;
                return (
                  <li key={slug}>
                    <Link
                      href={`/${slug}`}
                      onClick={() => {
                        setMenuOpen(false);
                        setServicesOpen(false);
                      }}
                    >
                      {s.anchor}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
          {/* Areas = the homepage "Nearby Cities We Serve" section (#areas,
              same target the location-page breadcrumbs already use).
              Plain <a> like the other home links (P3-1, see brand above):
              a Link to /#areas fetches the root flight payload from
              inner pages and 404s the same way. html has
              scroll-behavior: smooth, so the native hash jump still
              smooth-scrolls. */}
          <a href={`${ASSET_PREFIX}/#areas`} onClick={() => setMenuOpen(false)}>
            Areas
          </a>
          {/* Contact/About are inner routes — Next Link is fine (only home
              links must be plain <a> per the P3-1 rule). Order: Home |
              Services | Areas | Contact Us | About Us | phone. */}
          <Link href="/contact" onClick={() => setMenuOpen(false)}>
            Contact Us
          </Link>
          <Link href="/about" onClick={() => setMenuOpen(false)}>
            About Us
          </Link>
        </nav>
        <button
          type="button"
          className="menu-btn"
          ref={menuBtnRef}
          aria-expanded={menuOpen}
          aria-controls="main-nav"
          aria-label="Menu"
          onClick={() => {
            // Toggle-close restores the pre-menu scroll position (same as
            // Escape); opening just opens. Never restores on navigation.
            if (menuOpen) restoreMenuScroll();
            setMenuOpen((v) => !v);
          }}
        >
          <span aria-hidden="true" />
        </button>
        <a className="header-phone" href={TEL_HREF}>
          {SITE.phoneDisplay}
        </a>
      </div>
    </header>
  );
}

/* ---------- footer: multi-column (2026-11-17, owner: like all the other
   sites — columns, not rows). Map on top, then a 6-column grid: brand
   (drop mark, name, tagline, big copper Call button) | Services (the 10
   footer services) | Areas (3 cities) | Company (About, Contact) |
   Resources (5 blogs) | Legal (Privacy, Terms, Disclaimer). Same links
   as the slim footer — none added, none removed. Base bar verbatim. ---------- */
const FOOTER_SERVICES = [
  "window-well-flooding",
  "water-heater-leak-cleanup",
  "swamp-cooler-leak-water-damage",
  "ceiling-water-damage",
  "crawl-space-water-damage",
  "hardwood-floor-cabinet-drying",
  "condo-apartment-water-damage",
  "commercial-water-damage",
  "storm-flood-damage",
  "water-leak-detection",
];

const FOOTER_BLOGS = [
  { href: "/resources/frozen-pipes-midvale", label: "Frozen Pipes in Midvale" },
  { href: "/resources/winterize-swamp-cooler-utah", label: "Swamp Cooler Winterizing Checklist" },
  { href: "/resources/upstairs-unit-leak-who-pays-utah", label: "Upstairs Leak: Who Pays?" },
  { href: "/resources/can-mold-grow-in-utah", label: "Can Mold Grow in Utah?" },
  { href: "/resources/basement-flooding-spring-snowmelt-utah", label: "Basement Flooding & Spring Snowmelt" },
];

export function Footer({ showMap }: { showMap: boolean }) {
  return (
    <footer className="site-footer">
      {/* Footer map restored 2026-11-16 (was removed in 33a3d2c): Midvale
          embed, first child of <footer>, before the grid. Shown on every
          page EXCEPT /locations/* (FooterSwitch gating below) — those
          pages carry their own city map, no double maps. */}
      {showMap ? (
        <div className="footer-map">
          <iframe
            title="Map: Midvale, UT 84047"
            src="https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed"
            referrerPolicy="no-referrer-when-downgrade"
            loading="lazy"
          />
        </div>
      ) : null}
      <div className="wrap footer-grid">
        <div>
          <div className="footer-brand-row">
            <span className="footer-brand-mark" aria-hidden="true">
              <svg viewBox="0 0 32 32" width="30" height="30">
                <path d="M16 3C16 3 6 14 6 20a10 10 0 0 0 20 0C26 14 16 3 16 3Z" fill="#c26a24" />
              </svg>
            </span>
            <p className="footer-brand">Water Damage Restoration Midvale UT</p>
          </div>
          <p className="footer-tag">24/7 water damage restoration in Midvale, UT 84047.</p>
          <a className="footer-phone" href={TEL_HREF}>
            Call {SITE.phoneDisplay}
          </a>
        </div>
        <nav aria-label="Services">
          <p className="footer-h">Services</p>
          <ul>
            {FOOTER_SERVICES.map((slug) => {
              const s = SERVICES.find((x) => x.slug === slug)!;
              return (
                <li key={slug}>
                  <Link href={`/${slug}`}>{s.anchor}</Link>
                </li>
              );
            })}
          </ul>
        </nav>
        <nav aria-label="Areas">
          <p className="footer-h">Areas</p>
          <ul>
            {LOCATIONS.map((l) => (
              <li key={l.slug}>
                <Link href={`/locations/${l.slug}`}>{l.anchor}</Link>
              </li>
            ))}
          </ul>
        </nav>
        <nav aria-label="Company">
          <p className="footer-h">Company</p>
          <ul>
            <li>
              <Link href="/about">About</Link>
            </li>
            <li>
              <Link href="/contact">Contact</Link>
            </li>
          </ul>
        </nav>
        <nav aria-label="Resources">
          <p className="footer-h">Resources</p>
          <ul>
            {FOOTER_BLOGS.map((b) => (
              <li key={b.href}>
                <Link href={b.href}>{b.label}</Link>
              </li>
            ))}
          </ul>
        </nav>
        <nav aria-label="Legal">
          <p className="footer-h">Legal</p>
          <ul>
            <li>
              <Link href="/privacy-policy">Privacy Policy</Link>
            </li>
            <li>
              <Link href="/terms-of-use">Terms of Use</Link>
            </li>
            <li>
              <Link href="/disclaimer">Disclaimer</Link>
            </li>
          </ul>
        </nav>
      </div>
      <div className="wrap footer-base">
        <p>
          Water Damage Restoration Midvale UT · Midvale, UT 84047 ·{" "}
          <a href={TEL_HREF}>{SITE.phoneDisplay}</a>
        </p>
      </div>
    </footer>
  );
}

/* Footer with the map rule (restored 2026-11-16, old rule from 33a3d2c^):
   map on every page EXCEPT area pages. */
export function FooterSwitch() {
  const pathname = usePathname();
  const isArea = pathname !== null && pathname.startsWith("/locations/");
  return <Footer showMap={!isArea} />;
}

/* ---------- sticky mobile call bar (every page, always tappable) ----------
   10X FIX A-P1: at 320px first paint the fixed bar covered hero Button 2 on
   15/21 pages (tall wrapped hero, viewport 700px). The bar now stays hidden
   while the hero is on screen and appears only once the hero has scrolled
   out of view (IntersectionObserver — robust across viewport heights, where
   a fixed scroll threshold is not). No-JS default: bar visible. ---------- */
export function StickyBar() {
  const [heroGone, setHeroGone] = useState(false);
  useEffect(() => {
    const hero = document.querySelector(".hero-photo, .hero");
    if (!hero) {
      setHeroGone(true);
      return;
    }
    const io = new IntersectionObserver(
      ([entry]) => setHeroGone(!entry.isIntersecting),
      { threshold: 0 }
    );
    io.observe(hero);
    return () => io.disconnect();
  }, []);
  return (
    <div className={`sticky-bar${heroGone ? "" : " bar-hidden"}`}>
      <a href={TEL_HREF}>Call {SITE.phoneDisplay} · 24/7</a>
    </div>
  );
}

export function Breadcrumb({ items }: { items: { label: string; href?: string }[] }) {
  return (
    // CYCLE 1 UI/UX FIX (C-5): id="breadcrumb" — the BreadcrumbList @id
    // (#breadcrumb) resolves to this real DOM anchor.
    <nav id="breadcrumb" className="breadcrumb" aria-label="Breadcrumb">
      <ol>
        {items.map((it, i) => (
          <li key={i}>
            {it.href ? (
              it.href === "/" || it.href.startsWith("/#") ? (
                // P3-1 (10x round 2026-11-16): home crumbs are plain <a> —
                // a Next Link to "/" fetches the root flight payload as
                // /midvale-water-damage.txt (404) under basePath; a plain
                // anchor does a clean document load with no RSC fetch.
                <a href={`${ASSET_PREFIX}${it.href}`}>{it.label}</a>
              ) : (
                <Link href={it.href}>{it.label}</Link>
              )
            ) : (
              <span aria-current="page">{it.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

export function JsonLd({ data }: { data: object }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
