import type { Metadata } from "next";
import Link from "next/link";
import { splitAnnotated, LinkParts } from "@/lib/links";
import { SITE, HERO, SERVICES, NEIGHBORHOODS, WHY_HOMES, PROCESS, CATEGORY_TABLE, COSTS, LOCATIONS, FAQ, HERO_IMAGE, CARD_IMAGE } from "@/lib/content";
import { BUSINESS_ID, WEBSITE_ID, heroImageObject, webPageLd, cardImageObjects } from "@/lib/schema";
import { HeroButtons, Reveal, JsonLd, TEL_HREF, PhotoHero } from "@/components/site";
import { CardImage } from "@/components/panels";

export const metadata: Metadata = {
  title: SITE.metaTitle,
  description: SITE.metaDescription,
  robots: { index: true, follow: true },
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
  "@id": BUSINESS_ID,
  name: SITE.brand,
  description: SITE.metaDescription,
  telephone: SITE.phoneTel,
  url: SITE.base + "/",
  // The site's own footer map embed query
  // (https://www.google.com/maps?q=Midvale%2C%20UT%2084047&output=embed),
  // same query in canonical form.
  hasMap: "https://www.google.com/maps?q=Midvale,+UT+84047",
  areaServed: [
    { "@type": "City", name: "Midvale", address: { "@type": "PostalAddress", addressRegion: "UT", postalCode: "84047" } },
    { "@type": "City", name: "Cottonwood Heights", address: { "@type": "PostalAddress", addressRegion: "UT", postalCode: "84121" } },
    { "@type": "City", name: "South Salt Lake", address: { "@type": "PostalAddress", addressRegion: "UT", postalCode: "84115" } },
    { "@type": "City", name: "Magna", address: { "@type": "PostalAddress", addressRegion: "UT", postalCode: "84044" } },
  ],
  openingHours: "Mo-Su 00:00-24:00",
};

const faqPage = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": SITE.base + "/#faq",
  mainEntity: FAQ.map((f) => ({
    "@type": "Question",
    name: f.q,
    acceptedAnswer: { "@type": "Answer", text: f.a },
  })),
};

const webSite = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": WEBSITE_ID,
  name: SITE.brand,
  url: SITE.base + "/",
  publisher: { "@id": BUSINESS_ID },
  inLanguage: "en-US",
};

const breadcrumb = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "@id": SITE.base + "/#breadcrumb",
  itemListElement: [{ "@type": "ListItem", position: 1, name: "Home", item: SITE.base + "/" }],
};

const homeWebPage = webPageLd(
  { route: "/", metaTitle: SITE.metaTitle, metaDescription: SITE.metaDescription },
  true,
  // C-1 (Cycle 1): the homepage's own FAQPage + HowTo, as pure @id refs.
  [SITE.base + "/#faq", SITE.base + "/#howto-0"],
);

const homeHeroImage = heroImageObject("/", HERO_IMAGE.home);

// C-3 (Cycle 1): one ImageObject per homepage card image (16 service
// cards + 3 location cards, render order) — caption = alt verbatim,
// contentUrl = absolute single-prefix URL. 19 blocks.
const homeCardImages = cardImageObjects();

const homeHowTo = {
  "@context": "https://schema.org",
  "@type": "HowTo",
  "@id": SITE.base + "/#howto-0",
  name: "How Our Water Mitigation Midvale 84047 Process Works",
  step: PROCESS.map((p) => ({
    "@type": "HowToStep",
    name: p.lead,
    text: p.lead + " " + p.rest,
  })),
};

export default function HomePage() {
  // LINKFIX 2026-11-13: one link per target per page — the service cards
  // below are the FIRST occurrence of their targets in document order,
  // so their slugs start in the seen set; body copy after them dedupes
  // against it (the Condo paragraph renders as plain phrase text).
  const linkSeen = new Set<string>(SERVICES.map((s) => `/${s.slug}`));

  return (
    <>
      <link rel="canonical" href={SITE.base + "/"} />
      <meta property="og:url" content={SITE.base + "/"} />
      <JsonLd data={localBusiness} />
      <JsonLd data={faqPage} />
      <JsonLd data={webSite} />
      <JsonLd data={breadcrumb} />
      <JsonLd data={homeWebPage} />
      <JsonLd data={homeHeroImage} />
      <JsonLd data={homeHowTo} />
      {homeCardImages.map((img, i) => (
        <JsonLd key={`card-image-${i}`} data={img} />
      ))}

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
                {/* LINKFIX 2026-11-13: the card is ONE link unit — image +
                    H3 + summary paragraph (the doc's anchor phrase is the
                    link text; the ` (/slug/)` annotation never renders). */}
                <Link className="card-wrap-link" href={`/${s.slug}`}>
                  <span className="card-img-link">
                    <CardImage src={CARD_IMAGE[s.slug].src} alt={CARD_IMAGE[s.slug].alt} />
                  </span>
                  <div className="card-body">
                    <h3>{s.h3}</h3>
                    {/* CYCLE 1 UI/UX FIX (P2-1): the anchor phrase is the
                        doc's VERBATIM link text — it stays word-for-word,
                        but it is NOT body copy: it renders as its own
                        .card-cta line (teal semibold + arrow), pinned to
                        the bottom of the card body, so it reads as a link
                        affordance and never as duplicated prose. */}
                    <p>{s.summary}</p>
                    <p className="card-cta">
                      {s.anchor}
                      <span aria-hidden="true">&nbsp;→</span>
                    </p>
                  </div>
                </Link>
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
          {/* C-5 (Cycle 1): the homepage HowTo's fragment @id (#howto-0)
              resolves to this list — the same <ol> the HowTo steps come
              from (PROCESS, in order). */}
          <ol className="steps" id="howto-0">
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

      {/* 7 — Water categories + table (P3-2 fix 2026-11-12: doc order is
          H2 -> table -> "Clean water turns into gray water..." paragraph;
          the paragraph used to render BEFORE the table — swapped back). */}
      <section className="section alt">
        <div className="wrap">
          <Reveal>
            <h2>Clean, Gray or Sewage Water: Why the Category Matters</h2>
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
          <p>
            Clean water turns into gray water in about 48 hours as bacteria grow, so speed changes the whole job.
          </p>
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
              {/* LINKFIX 2026-11-13: annotation → real link. The Condo
                  target is already linked by its service card above, so
                  this renders as plain phrase text (one link per target). */}
              <LinkParts
                parts={splitAnnotated(
                  "We give you what adjusters ask for: dated photos, moisture maps, daily drying logs and a clear list of removed materials. Good records are a big part of water mitigation Midvale 84047 claims moving smoothly. If water came from an upstairs unit, see Condo & Apartment Water Damage (/condo-apartment-water-damage/).",
                  "/",
                  linkSeen,
                )}
                prefix="ins"
              />
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
              {/* LINKFIX 2026-11-13: annotation → real link (first and
                  only occurrence of this target on the page). */}
              <LinkParts
                parts={splitAnnotated(
                  "For sewer backups, the Midvale Water & Sewer Emergency Contacts page (/midvale-water-sewer-emergency-contacts/) lists who to call about the public line.",
                  "/",
                  linkSeen,
                )}
                prefix="first30"
              />
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
                {/* LINKFIX 2026-11-13: the card is ONE link unit (see the
                    service cards above). */}
                <Link className="card-wrap-link" href={`/locations/${l.slug}`}>
                  <span className="card-img-link">
                    <CardImage src={CARD_IMAGE[l.slug].src} alt={CARD_IMAGE[l.slug].alt} />
                  </span>
                  <div className="card-body">
                    {/* CYCLE 1 UI/UX FIX (P2-1): same as the service cards —
                        the anchor phrase stays verbatim as its own CTA line. */}
                    <p>
                      <strong>{l.lead}</strong> {l.rest}
                    </p>
                    <p className="card-cta">
                      {l.anchor}
                      <span aria-hidden="true">&nbsp;→</span>
                    </p>
                  </div>
                </Link>
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
