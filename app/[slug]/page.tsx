// Generic renderer for the 22 flat slugs (REBUILD 2026-11-12): 16 services
// (tabs 4-19) + guide (tab 23) + about (tab 2) + contact (tab 3) +
// privacy (tab 24) + terms (tab 25) + disclaimer (tab 26). All content
// verbatim from lib/pages-data.json. No trailing slash.
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { SITE, SERVICES, HERO_IMAGE } from "@/lib/content";
import DocPage, {
  DOC_PAGES,
  docPageByRoute,
  heroKeyForRoute,
} from "@/components/doc-page";

const FLAT_ROUTES = DOC_PAGES.filter((p) => /^\/[^/]+$/.test(p.route));

export function generateStaticParams() {
  return FLAT_ROUTES.map((p) => ({ slug: p.route.slice(1) }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const page = docPageByRoute(`/${params.slug}`);
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

export default function FlatPage({ params }: { params: { slug: string } }) {
  const page = docPageByRoute(`/${params.slug}`);
  if (!page) notFound();
  const isService = SERVICES.some((s) => s.slug === params.slug);
  return (
    <DocPage
      page={page}
      breadcrumbItems={[{ label: "Home", href: "/" }, { label: page.h1 }]}
      serviceKind={isService ? "service" : null}
    />
  );
}
