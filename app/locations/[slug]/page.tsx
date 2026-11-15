// Generic renderer for the 3 location pages (REBUILD 2026-11-12, tabs
// 20-22). All content verbatim from lib/pages-data.json. (The footer map
// the old comment here mentioned was removed 2026-11-16.)
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { SITE, LOCATIONS, HERO_IMAGE } from "@/lib/content";
import DocPage, {
  DOC_PAGES,
  docPageByRoute,
  heroKeyForRoute,
} from "@/components/doc-page";

const LOCATION_ROUTES = DOC_PAGES.filter((p) =>
  p.route.startsWith("/locations/"),
);

export function generateStaticParams() {
  return LOCATION_ROUTES.map((p) => ({
    slug: p.route.slice("/locations/".length),
  }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const page = docPageByRoute(`/locations/${params.slug}`);
  if (!page) return {};
  const hero = HERO_IMAGE[heroKeyForRoute(page.route)];
  return {
    title: page.metaTitle,
    description: page.metaDescription,
    robots: { index: true, follow: true },
    alternates: { canonical: `${SITE.base}${page.route}` },
    openGraph: {
      title: page.metaTitle,
      description: page.metaDescription,
      url: `${SITE.base}${page.route}`,
      images: [{ url: SITE.base + hero.src, alt: hero.alt }],
    },
    twitter: {
      title: page.metaTitle,
      description: page.metaDescription,
      images: [SITE.base + hero.src],
    },
  };
}

export default function LocationPage({ params }: { params: { slug: string } }) {
  const page = docPageByRoute(`/locations/${params.slug}`);
  if (!page) notFound();
  const loc = LOCATIONS.find((l) => l.slug === params.slug);
  return (
    <DocPage
      page={page}
      breadcrumbItems={[
        { label: "Home", href: "/" },
        { label: "Nearby Cities We Serve", href: "/#areas" },
        { label: page.h1 },
      ]}
      serviceKind="location"
      areaCity={loc?.city}
      areaZip={loc?.zip}
    />
  );
}
