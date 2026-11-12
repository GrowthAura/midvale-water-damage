// Fresh Midvale components — written new for this site. No file copied
// from any past site. Design follows the locked Theme v2 skeleton only
// (header / hero / trust band / cards / process / FAQ / footer / sticky bar).
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { SITE, SERVICES, LOCATIONS, GUIDE, ASSET_PREFIX } from "@/lib/content";

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
   high-contrast. Content is never hidden by animation. ---------- */
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
  return (
    <section className="hero hero-photo">
      <img className="hero-img" src={ASSET_PREFIX + image} alt={alt} width={1600} height={900} fetchPriority="high" />
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
   via footer links. Menu button 46px, Escape closes, aria-expanded.) ---------- */
const HEADER_SERVICES = [
  "emergency-water-extraction",
  "sewage-backup-cleanup",
];

export function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuBtnRef = useRef<HTMLButtonElement>(null);
  const pathname = usePathname();
  // Close the menu on navigation and on Escape (focus returns to the button).
  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);
  useEffect(() => {
    if (!menuOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setMenuOpen(false);
        menuBtnRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [menuOpen]);
  return (
    <header className="site-header">
      <div className="wrap header-inner">
        <Link className="brand" href="/">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 32 32" width="30" height="30">
              <path d="M16 3C16 3 6 14 6 20a10 10 0 0 0 20 0C26 14 16 3 16 3Z" fill="#c26a24" />
            </svg>
          </span>
          <span className="brand-text">
            Water Damage Restoration
            <span className="brand-city">Midvale, UT</span>
          </span>
        </Link>
        <nav id="main-nav" className={`main-nav${menuOpen ? " open" : ""}`} aria-label="Main">
          <Link href="/" onClick={() => setMenuOpen(false)}>
            Home
          </Link>
          {HEADER_SERVICES.map((slug) => {
            const s = SERVICES.find((x) => x.slug === slug)!;
            return (
              <Link key={slug} href={`/${slug}`} onClick={() => setMenuOpen(false)}>
                {s.anchor}
              </Link>
            );
          })}
        </nav>
        <button
          type="button"
          className="menu-btn"
          ref={menuBtnRef}
          aria-expanded={menuOpen}
          aria-controls="main-nav"
          aria-label="Menu"
          onClick={() => setMenuOpen((v) => !v)}
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

/* ---------- footer (map on every page EXCEPT area pages) ---------- */
const FOOTER_SERVICES = [
  "emergency-water-extraction",
  "basement-flooding-cleanup",
  "burst-pipe-water-damage",
  "sewage-backup-cleanup",
  "storm-flood-damage",
  "mold-remediation",
  "water-leak-detection",
  "water-damage-repair",
];

export function Footer({ showMap }: { showMap: boolean }) {
  return (
    <footer className="site-footer">
      {showMap ? (
        <div className="footer-map">
          <iframe
            title="Map: Midvale, UT 84047"
            src="https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed"
            referrerPolicy="no-referrer-when-downgrade"
          />
        </div>
      ) : null}
      <div className="wrap footer-grid">
        <div>
          <p className="footer-brand">Water Damage Restoration Midvale UT</p>
          <p>
            24/7 water damage restoration in Midvale, UT 84047.
            <br />
            <a href={TEL_HREF}>{SITE.phoneDisplay}</a>
          </p>
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
        <nav aria-label="Nearby cities">
          <p className="footer-h">Nearby Cities We Serve</p>
          <ul>
            {LOCATIONS.map((l) => (
              <li key={l.slug}>
                <Link href={`/locations/${l.slug}`}>{l.anchor}</Link>
              </li>
            ))}
          </ul>
        </nav>
        <nav aria-label="Help">
          <p className="footer-h">Emergency Help</p>
          <ul>
            <li>
              <Link href={`/${GUIDE.slug}`}>Midvale Water &amp; Sewer Emergency Contacts</Link>
            </li>
            <li>
              <Link href="/#faq">Water Damage Restoration FAQ</Link>
            </li>
            <li>
              <Link href="/#services">All Midvale Services</Link>
            </li>
            <li>
              <a href={TEL_HREF}>Call {SITE.phoneDisplay}</a>
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

/* Footer with the map rule: map on every page EXCEPT area pages. */
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
    <nav className="breadcrumb" aria-label="Breadcrumb">
      <ol>
        {items.map((it, i) => (
          <li key={i}>
            {it.href ? <Link href={it.href}>{it.label}</Link> : <span aria-current="page">{it.label}</span>}
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
