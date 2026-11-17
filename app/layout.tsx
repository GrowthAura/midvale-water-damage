import type { Metadata } from "next";
import { SITE, ASSET_PREFIX } from "@/lib/content";
import { Header, StickyBar, FooterSwitch } from "@/components/site";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(SITE.base),
  title: SITE.metaTitle,
  description: SITE.metaDescription,
  // SEO FIX 2 (2026-11-13): robots lives on the PAGE metadata (app/page.tsx
  // + the three generateMetadata renderers), NOT here. The root layout's
  // robots leaked onto the 404 page, which Next also auto-noindexes —
  // giving the 404 two conflicting robots tags (noindex + index,follow).
  // With no robots key here, the 404 carries only Next's single auto
  // noindex, and the 31 real pages keep their explicit index,follow.
  // Next's Metadata API does NOT apply basePath to icons (verified in the
  // built HTML: a bare "/favicon.svg" stayed bare on all 32 pages) —
  // so the icon path is hand-prefixed with ASSET_PREFIX, like plain <img>.
  icons: { icon: `${ASSET_PREFIX}/favicon.svg` },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: SITE.brand,
    title: SITE.metaTitle,
    description: SITE.metaDescription,
  },
  twitter: {
    card: "summary_large_image",
    title: SITE.metaTitle,
    description: SITE.metaDescription,
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {/* SPEED ITERATION 2 (P1 fix, 2026-11-17): anchor guard for Fix 3's
            content-visibility:auto. The browser's native fragment scroll
            estimates skipped sections at contain-intrinsic-size (1200px) —
            the services section alone is 8,796px tall on mobile — so a
            #areas jump landed ~8,700px off with the target unrendered
            (verifier reproduced 3x hash + real menu tap + cross-page).
            NOTE: this must be a RAW inline <script> as the first child
            of <body>, not next/script beforeInteractive — the Script
            component renders only into the RSC flight payload in a static
            export (no <script> element in the built HTML, verified), so
            it executes only at hydration, too late for the cold-load
            fragment scroll. This raw tag executes during parsing, BEFORE
            the body lays out: if the URL carries a hash it adds
            html.cv-anchor (see globals.css — content-visibility:visible
            on the skipped blocks), so the native jump is computed against
            TRUE heights; a capture-phase click listener does the same
            synchronously before any same-page hash click's default jump;
            a hashchange listener re-scrolls after disarming. Once
            disarmed the page stays fully rendered for that view (the
            jumped-to sections render anyway) — Lighthouse runs carry no
            hash, so the speed gain is untouched. ~700 bytes, no
            dependencies, no visual change; a no-op when no hash is
            involved. */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){function d(){document.documentElement.classList.add('cv-anchor');}function t(){try{var h=location.hash;return h.length>1?document.querySelector(h):null;}catch(e){return null;}}if(location.hash){d();}document.addEventListener('click',function(e){var el=e.target&&e.target.closest?e.target.closest('a[href*="#"]'):null;if(!el){return;}if((el.getAttribute('href')||'').indexOf('#')>=0){d();}},true);window.addEventListener('hashchange',function(){d();var el=t();if(el){requestAnimationFrame(function(){el.scrollIntoView();});}});})();`,
          }}
        />
        <Header />
        <main>{children}</main>
        <FooterSwitch />
        <StickyBar />
      </body>
    </html>
  );
}
