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
        <Header />
        <main>{children}</main>
        <FooterSwitch />
        <StickyBar />
      </body>
    </html>
  );
}
