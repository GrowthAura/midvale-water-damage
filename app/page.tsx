import type { Metadata } from "next";
import Link from "next/link";
import { SITE, HERO, SERVICES, NEIGHBORHOODS, WHY_HOMES, PROCESS, CATEGORY_TABLE, COSTS, LOCATIONS, FAQ, HERO_IMAGE, CARD_IMAGE } from "@/lib/content";
import { HeroButtons, Reveal, JsonLd, TEL_HREF, PhotoHero } from "@/components/site";
import { CardImage } from "@/components/panels";

export const metadata: Metadata = {
  title: SITE.metaTitle,
  description: SITE.metaDescription,
  // NOTE: Next's Metadata API strips the trailing slash from the homepage
  // canonical AND og:url, so both are emitted as explicit tags below
  // (exactly one of each). No `url` in openGraph here, and none in the
  // root layout either, or Next would emit a second slash-less og:url.
  openGraph: { title: SITE.metaTitle, description: SITE.metaDescription, images: [{ url: SITE.base + HERO_IMAGE.home.src, alt: HERO_IMAGE.home.alt }] },
  twitter: { title: SITE.metaTitle, description: SITE.metaDescription, images: [SITE.base + HERO_IMAGE.home.src] },
};

const localBusiness = {
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  name: SITE.brand,
  telephone: SITE.phoneTel,
  url: SITE.base + "/",
  areaServed: [
    { "@type": "City", name: "Midvale", addressRegion: "UT", postalCode: "84047" },
    { "@type": "City", name: "Cottonwood Heights", addressRegion: "UT", postalCode: "84121" },
    { "@type": "City", name: "South Salt Lake", addressRegion: "UT", postalCode: "84115" },
    { "@type": "City", name: "Magna", addressRegion: "UT", postalCode: "84044" },
  ],
  openingHours: "Mo-Su 00:00-24:00",
};

const faqPage = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: FAQ.map((f) => ({
    "@type": "Question",
    name: f.q,
    acceptedAnswer: { "@type": "Answer", text: f.a },
  })),
};

const webSite = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: SITE.brand,
  url: SITE.base + "/",
};

const breadcrumb = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: [{ "@type": "ListItem", position: 1, name: "Home", item: SITE.base + "/" }],
};

export default function HomePage() {
  return (
    <>
      <link rel="canonical" href={SITE.base + "/"} />
      <meta property="og:url" content={SITE.base + "/"} />
      <JsonLd data={localBusiness} />
      <JsonLd data={faqPage} />
      <JsonLd data={webSite} />
      <JsonLd data={breadcrumb} />

      {/* 1 — HERO: photo hero. Intro is IN the hero, trust chips are IN the
          hero (the separate copper trust band is gone — no duplication). */}
      <PhotoHero image={HERO_IMAGE.home.src} alt={HERO_IMAGE.home.alt} eyebrow={HERO.eyebrow} h1={HERO.h1} intro={HERO.intro} trust={HERO.trust} />

      {/* 2 — What causes most water damage */}
      <section className="section">
        <div className="wrap">
          <Reveal>
            <h2>What causes most water damage in Midvale, UT homes?</h2>
            <p>
              Most Midvale water damage comes from frozen or burst pipes, worn water heaters, older sewer lines backing up, and spring snowmelt pushing water through basement walls and window wells.
            </p>
            <p>
              The calendar tells the story. Winter brings split pipes in rim joists, crawl spaces and hose bibs, plus ice dams on low-slope roofs. Spring snowmelt from the Wasatch soaks the valley&apos;s clay soil, and groundwater finds every crack in a basement slab. Summer cloudbursts overload older storm drains, and swamp coolers on Midvale rooftops overflow into attics. Water heaters, washers and supply lines fail any month of the year. Whatever the cause, the first few hours decide how much of your home can be dried and saved instead of torn out.
            </p>
          </Reveal>
        </div>
      </section>

      {/* 3 — Services: 16 image cards */}
      <section className="section alt" id="services">
        <div className="wrap">
          <Reveal>
            <h2>Water Damage Midvale UT Property Owners Call Us For</h2>
            <p>
              Every water problem needs a different plan. As a full-service water restoration company Midvale homeowners, renters, landlords and businesses can call any hour, we handle each one from first extraction to final repair.
            </p>
          </Reveal>
          <div className="card-grid">
            {SERVICES.map((s, i) => (
              <article className="card" key={s.slug}>
                <Link className="card-img-link" href={`/${s.slug}`}>
                  <CardImage src={CARD_IMAGE[s.slug].src} alt={CARD_IMAGE[s.slug].alt} />
                </Link>
                <div className="card-body">
                  <Link href={`/${s.slug}`}>
                    <h3>{s.h3}</h3>
                  </Link>
                  <p>
                    {s.summary} {s.anchor} (/{s.slug}/)
                  </p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* 4 — Neighborhoods */}
      <section className="section">
        <div className="wrap">
          <Reveal>
            <h2>Water Damage Help Across Every Midvale Neighborhood</h2>
            <p>
              Midvale is split by I-15, and the homes on each side flood in different ways. Our crew works both sides, so anyone who needs a water restoration company Midvale can rely on calls the same number for a townhome leak or a basement full of sewage.
            </p>
          </Reveal>
          <div className="split">
            {NEIGHBORHOODS.map((n) => (
              <div className="area-card" key={n.h3}>
                <h3>{n.h3}</h3>
                <p>{n.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5 — Why Midvale homes take on water */}
      <section className="section alt">
        <div className="wrap">
          <Reveal>
            <h2>Why Midvale Homes Take On Water</h2>
            <p>
              Midvale&apos;s water damage calls follow its housing, its utilities and its weather. Knowing the local pattern tells us where to look first.
            </p>
            <ul>
              {WHY_HOMES.map((w) => (
                <li key={w.lead}>
                  <strong>{w.lead}</strong> {w.rest}
                </li>
              ))}
            </ul>
          </Reveal>
        </div>
      </section>

      {/* 6 — Process */}
      <section className="section">
        <div className="wrap">
          <Reveal>
            <h2>How Our Water Mitigation Midvale 84047 Process Works</h2>
            <p>
              Every job follows the same order, built on IICRC S500 water drying steps, so nothing is missed and your insurer gets a clear record.
            </p>
          </Reveal>
          <ol className="steps">
            {PROCESS.map((p) => (
              <li key={p.lead}>
                <strong>{p.lead}</strong> {p.rest}
              </li>
            ))}
          </ol>
          <p style={{ marginTop: 24 }}>
            From the first phone call to the final walk-through, water mitigation Midvale 84047 homeowners receive is documented with dated photos and daily moisture readings.
          </p>
        </div>
      </section>

      {/* 7 — Water categories + table */}
      <section className="section alt">
        <div className="wrap">
          <Reveal>
            <h2>Clean, Gray or Sewage Water: Why the Category Matters</h2>
            <p>
              Clean water turns into gray water in about 48 hours as bacteria grow, so speed changes the whole job.
            </p>
          </Reveal>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  {CATEGORY_TABLE.headers.map((h) => (
                    <th key={h}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {CATEGORY_TABLE.rows.map((row) => (
                  <tr key={row[0]}>
                    {row.map((cell, i) => (
                      <td key={i}>{cell}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* 8 — Cost */}
      <section className="section">
        <div className="wrap">
          <Reveal>
            <h2>What Water Damage Restoration Midvale UT Jobs Usually Cost</h2>
            <p>Every home is different, but these general ranges give you a starting point:</p>
            <ul>
              {COSTS.map((c) => (
                <li key={c}>{c}</li>
              ))}
            </ul>
            <p>
              The final cost depends on the square footage, the water category, how long the water sat and what has to be rebuilt. When insurance covers the loss, you usually pay only your deductible.
            </p>
          </Reveal>
        </div>
      </section>

      {/* 9 — Insurance help */}
      <section className="section alt">
        <div className="wrap">
          <Reveal>
            <h2>Insurance Help for Midvale Homeowners, Renters and HOAs</h2>
            <p>
              Most Utah homeowners policies cover sudden water damage, like a burst pipe or a failed water heater. Gradual leaks, groundwater seepage and surface flooding are often excluded, and sewer backups usually need a separate backup endorsement. Condo owners deal with both an HOA master policy and their own HO-6, and renters rely on a renters policy for belongings.
            </p>
            <p>
              We give you what adjusters ask for: dated photos, moisture maps, daily drying logs and a clear list of removed materials. Good records are a big part of water mitigation Midvale 84047 claims moving smoothly. If water came from an upstairs unit, see Condo &amp; Apartment Water Damage (/condo-apartment-water-damage/).
            </p>
          </Reveal>
        </div>
      </section>

      {/* 10 — First 30 minutes */}
      <section className="section">
        <div className="wrap">
          <Reveal>
            <h2>What to Do in the First 30 Minutes</h2>
            <ul>
              <li>Shut off the main water valve, or the valve at the fixture that failed.</li>
              <li>Turn off power to wet rooms only if you can reach the panel without standing in water.</li>
              <li>Stop using sinks, toilets and showers if sewage is coming up a drain.</li>
              <li>Move rugs, electronics, photos and papers to a dry room.</li>
              <li>Take photos and video of everything before cleanup begins.</li>
              <li>
                Call <a href={TEL_HREF}>(385) 337-3560</a> so a crew is dispatched while you work.
              </li>
            </ul>
            <p>
              For sewer backups, the Midvale Water &amp; Sewer Emergency Contacts page (/midvale-water-sewer-emergency-contacts/) lists who to call about the public line.
            </p>
          </Reveal>
        </div>
      </section>

      {/* 11 — Nearby cities: 3 area cards */}
      <section className="section alt" id="areas">
        <div className="wrap">
          <Reveal>
            <h2>Nearby Cities We Serve</h2>
            <p>
              If you are searching for water damage restoration near me from just outside Midvale, the same crew covers these neighbors:
            </p>
          </Reveal>
          <div className="card-grid">
            {LOCATIONS.map((l, i) => (
              <article className="card" key={l.slug}>
                <Link className="card-img-link" href={`/locations/${l.slug}`}>
                  <CardImage src={CARD_IMAGE[l.slug].src} alt={CARD_IMAGE[l.slug].alt} />
                </Link>
                <div className="card-body">
                  <p>
                    <strong>{l.lead}</strong> {l.rest} {l.anchor} (/locations/{l.slug}/)
                  </p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* 12 — FAQ */}
      <section className="section" id="faq">
        <div className="wrap">
          <Reveal>
            <h2>Water Damage Restoration FAQ for Midvale, UT</h2>
          </Reveal>
          <div className="faq-list">
            {FAQ.map((f) => (
              <div className="faq-item" key={f.q}>
                <h3>{f.q}</h3>
                <p>{f.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 13 — Final CTA */}
      <section className="section final-cta">
        <div className="wrap">
          <Reveal>
            <h2>Water Damage Help in Midvale Starts With One Call</h2>
            <p>
              Water keeps spreading until someone stops it. Whether it is a split pipe in January, a flooded window well in April or a swamp cooler leak in July, water damage Midvale UT families and businesses face gets the same fast, careful response. Call now for water damage restoration Midvale UT residents can reach any hour, and a crew will be dispatched immediately.
            </p>
            <HeroButtons />
          </Reveal>
        </div>
      </section>
    </>
  );
}
