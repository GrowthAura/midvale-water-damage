// Generic renderer for the 5 blog pages under /resources/ (REBUILD
// 2026-11-12, tabs 27-31). All content verbatim from lib/pages-data.json.
// Breadcrumb: Home -> page H1. No Service schema (blogs, not services).
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { SITE, HERO_IMAGE } from "@/lib/content";
import DocPage, {
  DOC_PAGES,
  docPageByRoute,
  heroKeyForRoute,
} from "@/components/doc-page";

const RESOURCE_ROUTES = DOC_PAGES.filter((p) =>
  p.route.startsWith("/resources/"),
);

export function generateStaticParams() {
  return RESOURCE_ROUTES.map((p) => ({
    slug: p.route.slice("/resources/".length),
  }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const page = docPageByRoute(`/resources/${params.slug}`);
  if (!page) return {};
  const hero = HERO_IMAGE[heroKeyForRoute(page.route)];
  return {
    title: page.metaTitle,
    description: page.metaDescription,
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

export default function ResourcePage({ params }: { params: { slug: string } }) {
  const page = docPageByRoute(`/resources/${params.slug}`);
  if (!page) notFound();
  return (
    <DocPage
      page={page}
      breadcrumbItems={[{ label: "Home", href: "/" }, { label: page.h1 }]}
      serviceKind={null}
    />
  );
}
