import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SITE, LOCATIONS, locationBySlug, HERO_IMAGE } from "@/lib/content";
import { HeroButtons, Breadcrumb, JsonLd, PhotoHero } from "@/components/site";

// Area pages: NO footer map (rule), no invented content — only the verbatim
// homepage summary sentence for that city.
export function generateStaticParams() {
  return LOCATIONS.map((l) => ({ slug: l.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const loc = locationBySlug(params.slug);
  if (!loc) return {};
  const h1 = `${loc.anchor}, UT`;
  const desc = `${loc.lead} ${loc.rest}`;
  return {
    title: `${h1} | Water Damage Restoration Midvale UT`,
    description: desc,
    alternates: { canonical: `${SITE.base}/locations/${loc.slug}` },
    openGraph: { title: `${h1} | Water Damage Restoration Midvale UT`, description: desc, url: `${SITE.base}/locations/${loc.slug}`, images: [{ url: SITE.base + HERO_IMAGE[loc.slug].src, alt: HERO_IMAGE[loc.slug].alt }] },
    twitter: { title: `${h1} | Water Damage Restoration Midvale UT`, description: desc, images: [SITE.base + HERO_IMAGE[loc.slug].src] },
  };
}

export default function LocationPage({ params }: { params: { slug: string } }) {
  const loc = locationBySlug(params.slug);
  if (!loc) notFound();
  const h1 = `${loc.anchor}, UT`;
  const url = `${SITE.base}/locations/${loc.slug}`;
  const index = LOCATIONS.findIndex((l) => l.slug === loc.slug);
  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "Service",
          name: loc.anchor,
          serviceType: "Water Damage Restoration",
          url,
          areaServed: { "@type": "City", name: loc.city, addressRegion: "UT", postalCode: loc.zip },
          provider: { "@type": "HomeAndConstructionBusiness", name: SITE.brand, telephone: SITE.phoneTel, url: SITE.base + "/" },
        }}
      />
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "BreadcrumbList",
          itemListElement: [
            { "@type": "ListItem", position: 1, name: "Home", item: SITE.base + "/" },
            { "@type": "ListItem", position: 2, name: "Nearby Cities We Serve", item: SITE.base + "/#areas" },
            { "@type": "ListItem", position: 3, name: loc.anchor, item: url },
          ],
        }}
      />
      <PhotoHero
        image={HERO_IMAGE[loc.slug].src}
        alt={HERO_IMAGE[loc.slug].alt}
        eyebrow="WATER DAMAGE RESTORATION • MIDVALE, UTAH"
        h1={h1}
        intro={`${loc.lead} ${loc.rest}`}
        breadcrumb={
          <Breadcrumb
            items={[
              { label: "Home", href: "/" },
              { label: "Nearby Cities We Serve", href: "/#areas" },
              { label: loc.anchor },
            ]}
          />
        }
      />
      <section className="page-body">
        <div className="wrap">
          {/* Body dedup: the verbatim city sentence is the hero intro now —
              it is NOT repeated here. */}
          <h2 style={{ marginTop: 0 }}>{loc.anchor}</h2>
          <p>
            <Link href="/#services">See all Midvale services</Link>
          </p>
          <HeroButtons />
        </div>
      </section>
    </>
  );
}
