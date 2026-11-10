import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SITE, SERVICES, GUIDE, serviceBySlug, HERO_IMAGE } from "@/lib/content";
import { HeroButtons, Breadcrumb, JsonLd, PhotoHero } from "@/components/site";

// Flat routes: 16 services + 1 guide. No trailing slash (trailingSlash: false).
export function generateStaticParams() {
  return [...SERVICES.map((s) => ({ slug: s.slug })), { slug: GUIDE.slug }];
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const service = serviceBySlug(params.slug);
  if (params.slug === GUIDE.slug) {
    return {
      title: `${GUIDE.h1} | Water Damage Restoration Midvale UT`,
      description: GUIDE.sentence,
      alternates: { canonical: `${SITE.base}/${GUIDE.slug}` },
      openGraph: { title: `${GUIDE.h1} | Water Damage Restoration Midvale UT`, description: GUIDE.sentence, url: `${SITE.base}/${GUIDE.slug}`, images: [{ url: SITE.base + HERO_IMAGE[GUIDE.slug].src, alt: HERO_IMAGE[GUIDE.slug].alt }] },
      twitter: { title: `${GUIDE.h1} | Water Damage Restoration Midvale UT`, description: GUIDE.sentence, images: [SITE.base + HERO_IMAGE[GUIDE.slug].src] },
    };
  }
  if (!service) return {};
  const h1 = `${service.anchor} in Midvale, UT`;
  return {
    title: `${h1} | Water Damage Restoration Midvale UT`,
    description: service.summary,
    alternates: { canonical: `${SITE.base}/${service.slug}` },
    openGraph: { title: `${h1} | Water Damage Restoration Midvale UT`, description: service.summary, url: `${SITE.base}/${service.slug}`, images: [{ url: SITE.base + HERO_IMAGE[service.slug].src, alt: HERO_IMAGE[service.slug].alt }] },
    twitter: { title: `${h1} | Water Damage Restoration Midvale UT`, description: service.summary, images: [SITE.base + HERO_IMAGE[service.slug].src] },
  };
}

export default function LinkedPage({ params }: { params: { slug: string } }) {
  // Guide page — built ONLY from the one verbatim sentence in the Doc.
  if (params.slug === GUIDE.slug) {
    const url = `${SITE.base}/${GUIDE.slug}`;
    return (
      <>
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            itemListElement: [
              { "@type": "ListItem", position: 1, name: "Home", item: SITE.base + "/" },
              { "@type": "ListItem", position: 2, name: GUIDE.h1, item: url },
            ],
          }}
        />
        <PhotoHero
          image={HERO_IMAGE[GUIDE.slug].src}
          alt={HERO_IMAGE[GUIDE.slug].alt}
          eyebrow="WATER DAMAGE RESTORATION • MIDVALE, UTAH"
          h1={GUIDE.h1}
          intro={GUIDE.sentence}
          breadcrumb={<Breadcrumb items={[{ label: "Home", href: "/" }, { label: GUIDE.h1 }]} />}
        />
        <section className="page-body">
          <div className="wrap">
            <p style={{ marginTop: 28 }}>
              <Link href="/#services">See all Midvale services</Link>
            </p>
            <HeroButtons />
          </div>
        </section>
      </>
    );
  }

  const service = serviceBySlug(params.slug);
  if (!service) notFound();
  const h1 = `${service.anchor} in Midvale, UT`;
  const url = `${SITE.base}/${service.slug}`;
  const index = SERVICES.findIndex((s) => s.slug === service.slug);
  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "Service",
          name: service.anchor,
          serviceType: service.anchor,
          url,
          areaServed: { "@type": "City", name: "Midvale", addressRegion: "UT", postalCode: "84047" },
          provider: { "@type": "HomeAndConstructionBusiness", name: SITE.brand, telephone: SITE.phoneTel, url: SITE.base + "/" },
        }}
      />
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "BreadcrumbList",
          itemListElement: [
            { "@type": "ListItem", position: 1, name: "Home", item: SITE.base + "/" },
            { "@type": "ListItem", position: 2, name: service.anchor, item: url },
          ],
        }}
      />
      <PhotoHero
        image={HERO_IMAGE[service.slug].src}
        alt={HERO_IMAGE[service.slug].alt}
        eyebrow="WATER DAMAGE RESTORATION • MIDVALE, UTAH"
        h1={h1}
        intro={service.summary}
        breadcrumb={<Breadcrumb items={[{ label: "Home", href: "/" }, { label: service.anchor }]} />}
      />
      <section className="page-body">
        <div className="wrap">
          {/* Body dedup: the verbatim summary is the hero intro now — it is
              NOT repeated here. Body keeps the verbatim H2, the link back,
              and the call buttons. */}
          <h2 style={{ marginTop: 0 }}>{service.h3}</h2>
          <p>
            <Link href="/#services">See all Midvale services</Link>
          </p>
          <HeroButtons />
        </div>
      </section>
    </>
  );
}
