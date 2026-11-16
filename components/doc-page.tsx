// Generic DocPage renderer (REBUILD 2026-11-12). Renders ONE page object
// from lib/pages-data.json — 1001% verbatim, no word added, cut or
// paraphrased. No builder-added links or words.
// LINKFIX 2026-11-13 (user correction — overrides the rebuild brief):
// parenthetical `Phrase (/path/)` annotations are LINK annotations —
// phrase = anchor, path = href — and must NEVER render as visible text.
// lib/links.tsx interprets them at render time (first occurrence of a
// target per page links; later ones and self-links render as plain
// phrase text). The data keeps annotations verbatim; the renderer strips
// the ` (/path/)` tokens (link metadata, not content words) — visible
// words drop by exactly the annotation token count.
// Server component. Header/footer/sticky-bar/breadcrumb are template
// chrome and excluded from the verbatim word-diff, as before.
import type { ReactNode } from "react";
import { Fragment } from "react";
import fs from "fs";
import path from "path";
import { splitAnnotated, stripAnnotations, LinkParts } from "@/lib/links";
import { SITE, HERO_IMAGE, ASSET_PREFIX } from "@/lib/content";
import {
  BUSINESS_ID,
  pageUrl,
  heroImageObject,
  imageObject,
  webPageLd,
  howToFromBlocks,
  howToIndexByBlock,
} from "@/lib/schema";
import { Breadcrumb, HeroButtons, JsonLd, PhotoHero } from "@/components/site";
import ContactForm from "@/components/contact-form";
import pagesData from "@/lib/pages-data.json";

export type DocSegment = { t: string; b: boolean };

export type DocBlock =
  | { type: "h2" | "h3"; text: string }
  | { type: "p"; segments: DocSegment[] }
  | { type: "ul" | "ol"; items: { segments: DocSegment[] }[] }
  | { type: "table"; headers: string[]; rows: string[][] };

export type DocFaq = { q: string; a: string };

export type DocPageData = {
  tab: number;
  route: string;
  url: string;
  metaTitle: string;
  metaDescription: string;
  eyebrow: string | null;
  h1: string;
  intro: string;
  trustChips: string[] | null;
  hasButtonsLine: boolean;
  blocks: DocBlock[];
  faqs: DocFaq[];
  counts: {
    words: number;
    h2: number;
    h3: number;
    faq: number;
    tables: number;
    dashesStripped: number;
  };
};

export const DOC_PAGES: DocPageData[] = (
  pagesData as { pages: DocPageData[] }
).pages;

export function docPageByRoute(route: string): DocPageData | undefined {
  return DOC_PAGES.find((p) => p.route === route);
}

// BODY IMAGES (DESIGN ROUND 2026-11-13): lib/body-images.json is built
// separately by image workers and may NOT exist yet — a missing file,
// unreadable file, bad JSON or bad entry means NO images, never a broken
// tag and never a failed build. Contract:
//   {"<route>": [{"src": "/images/body/<slug>-N.webp", "alt": "...",
//                  "afterH2": <0-based index among the page's h2 blocks>,
//                  "layout": "split"|"sticky"}]}
// afterH2 counts EVERY h2 block in document order, INCLUDING the FAQ h2.
// One image per section (first valid entry wins). Route "/" is NOT
// rendered by DocPage (the homepage is a bespoke component in
// app/page.tsx), so a "/" entry is ignored here. Invalid entries are
// dropped silently — the manifest is another worker's file, and a bad
// row must never break a page.
type BodyImage = {
  src: string;
  alt: string;
  afterH2: number;
  layout: "split" | "sticky";
};

function loadBodyImages(): Record<string, BodyImage[]> {
  try {
    const raw = fs.readFileSync(
      path.join(process.cwd(), "lib", "body-images.json"),
      "utf8",
    );
    const data: unknown = JSON.parse(raw);
    if (!data || typeof data !== "object" || Array.isArray(data)) return {};
    const out: Record<string, BodyImage[]> = {};
    for (const [route, list] of Object.entries(
      data as Record<string, unknown>,
    )) {
      if (!Array.isArray(list)) continue;
      const imgs: BodyImage[] = [];
      for (const e of list) {
        if (!e || typeof e !== "object") continue;
        const { src, alt, afterH2, layout } = e as Record<string, unknown>;
        if (
          typeof src !== "string" ||
          !src.startsWith("/images/body/") ||
          !src.endsWith(".webp")
        )
          continue;
        if (typeof alt !== "string" || alt.trim() === "") continue;
        if (
          typeof afterH2 !== "number" ||
          !Number.isInteger(afterH2) ||
          afterH2 < 0
        )
          continue;
        if (layout !== "split" && layout !== "sticky") continue;
        imgs.push({ src, alt, afterH2, layout });
      }
      if (imgs.length > 0) out[route] = imgs;
    }
    return out;
  } catch {
    return {};
  }
}

const BODY_IMAGES = loadBodyImages();

// HERO_IMAGE keys are route slugs: bare slug for flat + location pages,
// "resources/<slug>" for blogs, "home" for the homepage.
export function heroKeyForRoute(route: string): string {
  if (route === "/") return "home";
  if (route.startsWith("/locations/")) return route.slice("/locations/".length);
  if (route.startsWith("/resources/")) return route.slice(1);
  return route.slice(1);
}

export type BreadcrumbItem = { label: string; href?: string };

function renderSegments(
  segments: DocSegment[],
  ownSlug: string,
  seen: Set<string>,
  keyPrefix: string,
): ReactNode[] {
  return segments.map((s, i) => {
    // LINKFIX 2026-11-13: interpret `Phrase (/path/)` annotations —
    // kept links render as body links, dup/self anchors as plain text.
    const nodes = (
      <LinkParts
        parts={splitAnnotated(s.t, ownSlug, seen)}
        prefix={`${keyPrefix}-${i}`}
      />
    );
    return s.b ? (
      <strong key={`${keyPrefix}-${i}`}>{nodes}</strong>
    ) : (
      <span key={`${keyPrefix}-${i}`}>{nodes}</span>
    );
  });
}

export default function DocPage({
  page,
  breadcrumbItems,
  serviceKind,
  areaCity,
  areaZip,
}: {
  page: DocPageData;
  breadcrumbItems: BreadcrumbItem[];
  // Service schema ONLY for the 16 service slugs + 3 location slugs.
  // Anything else -> no Service schema, nothing invented.
  serviceKind?: "service" | "location" | null;
  areaCity?: string;
  areaZip?: string;
}) {
  const hero = HERO_IMAGE[heroKeyForRoute(page.route)];
  const url = pageUrl(page.route);

  const breadcrumbLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "@id": url + "#breadcrumb",
    itemListElement: breadcrumbItems.map((it, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: it.label,
      item:
        i === breadcrumbItems.length - 1
          ? url
          : `${SITE.base}${it.href ?? "/"}`,
    })),
  };

  const faqLd =
    page.faqs.length > 0
      ? {
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "@id": url + "#faq",
          mainEntity: page.faqs.map((f) => ({
            "@type": "Question",
            name: f.q,
            // LINKFIX 2026-11-13: schema answers must equal the visible
            // answers — strip the ` (/path/)` annotation tokens.
            acceptedAnswer: { "@type": "Answer", text: stripAnnotations(f.a) },
          })),
        }
      : null;

  const serviceLd =
    serviceKind === "service"
      ? {
          "@context": "https://schema.org",
          "@type": "Service",
          "@id": url + "#service",
          name: page.h1,
          serviceType: page.h1,
          description: page.intro,
          image: { "@id": url + "#hero-image" },
          url,
          areaServed: {
            "@type": "City",
            name: "Midvale",
            address: {
              "@type": "PostalAddress",
              addressRegion: "UT",
              postalCode: "84047",
            },
          },
          provider: {
            "@type": "HomeAndConstructionBusiness",
            "@id": BUSINESS_ID,
            name: SITE.brand,
            telephone: SITE.phoneTel,
            url: SITE.base + "/",
          },
        }
      : serviceKind === "location"
        ? {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": url + "#service",
            name: page.h1,
            // SEO FIX 1 2026-11-13 (P3-2): location serviceType was the
            // generic "Water Damage Restoration"; the page H1 is the
            // truthful, page-specific service name — same pattern as the
            // 16 service pages (serviceType: page.h1).
            serviceType: page.h1,
            description: page.intro,
            image: { "@id": url + "#hero-image" },
            url,
            areaServed: {
              "@type": "City",
              name: areaCity,
              address: {
                "@type": "PostalAddress",
                addressRegion: "UT",
                postalCode: areaZip,
              },
            },
            provider: {
              "@type": "HomeAndConstructionBusiness",
              "@id": BUSINESS_ID,
              name: SITE.brand,
              telephone: SITE.phoneTel,
              url: SITE.base + "/",
            },
          }
        : null;

  const heroImageLd = heroImageObject(page.route, hero);
  const howToLd = howToFromBlocks(page);
  // C-1 (Cycle 1): WebPage mainEntity — pure @id refs to the page's
  // own nodes, in a fixed order (FAQ, Service, then HowTos in
  // document order). Zero new claims; refs only.
  const webPageMainEntityIds: string[] = [];
  if (page.faqs.length > 0) webPageMainEntityIds.push(url + "#faq");
  if (serviceLd) webPageMainEntityIds.push(url + "#service");
  for (const h of howToLd) webPageMainEntityIds.push(h["@id"]);
  // C-2 (Cycle 1): AboutPage / ContactPage subtypes by route.
  const webPageType =
    page.route === "/about"
      ? "AboutPage"
      : page.route === "/contact"
        ? "ContactPage"
        : "WebPage";
  const webPageLdData = webPageLd(
    page,
    page.faqs.length > 0,
    webPageMainEntityIds,
    webPageType,
  );
  // C-5 (Cycle 1): block index -> HowTo index, the same map that
  // generates the HowTo @ids — the rendered <ol> elements get the
  // matching id="howto-N" (see renderSection).
  const howToBlockIds = howToIndexByBlock(page.blocks);

  // Body blocks in order, grouped into H2-sections: each section is one
  // h2 block plus the blocks that follow it until the next h2. h2Index
  // is the 0-based index of the section's h2 among the page's h2 blocks
  // (FAQ h2 included — it matches the manifest's afterH2 counting).
  // Blocks before the first h2 (privacy/terms intro p) form a lead
  // section (h2Index -1) that renders unwrapped, exactly as before.
  type H2Section = { h2Index: number; blocks: { b: DocBlock; i: number }[] };
  const sections: H2Section[] = [];
  {
    let cur: H2Section = { h2Index: -1, blocks: [] };
    let h2Count = 0;
    page.blocks.forEach((b, i) => {
      if (b.type === "h2") {
        if (cur.blocks.length > 0) sections.push(cur);
        cur = { h2Index: h2Count, blocks: [{ b, i }] };
        h2Count += 1;
      } else {
        cur.blocks.push({ b, i });
      }
    });
    if (cur.blocks.length > 0) sections.push(cur);
  }

  // LINKFIX 2026-11-13: one link per target per page — the shared
  // first-occurrence set, consumed in document order by the body loop
  // (sections render in order, so document order is preserved).
  const linkSeen = new Set<string>();

  // Render one H2-section's blocks. FAQ state is section-local: the H2
  // containing "FAQ" opens <section id="faq"><div className="faq-list">;
  // each following h3 + its answer p becomes one .faq-item; the section
  // end flushes it. Output is identical to the old flat loop — the FAQ
  // h2's following blocks until the next h2 are exactly its items.
  function renderSection(sec: H2Section): ReactNode[] {
    const nodes: ReactNode[] = [];
    let inFaq = false;
    let faqH2 = "";
    let faqItems: ReactNode[] = [];
    let pendingQ: string | null = null;

    const flushFaq = (key: string) => {
      if (!inFaq) return;
      nodes.push(
        <section id="faq" key={key}>
          <h2>{faqH2}</h2>
          <div className="faq-list">{faqItems}</div>
        </section>,
      );
      inFaq = false;
      faqH2 = "";
      faqItems = [];
      pendingQ = null;
    };

    for (const { b, i } of sec.blocks) {
      if (b.type === "h2") {
        if (b.text.includes("FAQ")) {
          flushFaq(`faq-${i}`);
          inFaq = true;
          faqH2 = b.text;
          continue;
        }
        flushFaq(`faq-${i}`);
        nodes.push(<h2 key={i}>{b.text}</h2>);
        continue;
      }
      if (b.type === "h3") {
        if (inFaq) {
          pendingQ = b.text;
          continue;
        }
        nodes.push(<h3 key={i}>{b.text}</h3>);
        continue;
      }
      if (b.type === "p") {
        if (inFaq && pendingQ !== null) {
          faqItems.push(
            <div className="faq-item" key={i}>
              <h3>{pendingQ}</h3>
              <p>{renderSegments(b.segments, page.route, linkSeen, `f${i}`)}</p>
            </div>,
          );
          pendingQ = null;
          continue;
        }
        nodes.push(<p key={i}>{renderSegments(b.segments, page.route, linkSeen, `p${i}`)}</p>);
        // P2-3 (2026-11-12): the Contact tab names its submit button in this
        // paragraph ("[Send My Request]") — the actual form (template chrome,
        // excluded from the verbatim diff) renders right after it, where the
        // doc says the form belongs. Contact route only.
        if (
          page.route === "/contact" &&
          b.segments.map((s) => s.t).join("") === "[Send My Request]"
        ) {
          nodes.push(<ContactForm key={`contact-form-${i}`} />);
        }
        continue;
      }
      if (b.type === "ul" || b.type === "ol") {
        const Tag = b.type;
        // C-5 (Cycle 1): an <ol> that carries a HowTo gets the matching
        // DOM id (same howToIndexByBlock map as the HowTo @ids); a <ul>
        // or an <ol> with no preceding h2 gets no id.
        const hid = b.type === "ol" ? howToBlockIds.get(i) : undefined;
        nodes.push(
          <Tag key={i} id={hid !== undefined ? `howto-${hid.n}` : undefined}>
            {b.items.map((item, j) => (
              <li key={j}>{renderSegments(item.segments, page.route, linkSeen, `li${i}-${j}`)}</li>
            ))}
          </Tag>,
        );
        continue;
      }
      if (b.type === "table") {
        nodes.push(
          <div className="table-wrap" key={i}>
            <table>
              <thead>
                <tr>
                  {b.headers.map((h) => (
                    <th key={h}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {b.rows.map((row, r) => (
                  <tr key={r}>
                    {row.map((cell, c) => (
                      <td key={c}>
                        <LinkParts
                          parts={splitAnnotated(cell, page.route, linkSeen)}
                          prefix={`t${i}-${r}-${c}`}
                        />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>,
        );
        continue;
      }
    }
    flushFaq(`faq-end-${sec.h2Index}`);
    return nodes;
  }

  // Compose the body: a section with an attached body image renders as a
  // 2-column grid (text | image; "sticky" pins the figure below the
  // sticky header) and stacks, image above text, on mobile. Sections
  // without an image render unwrapped, exactly as before — same DOM,
  // same measure, same word count.
  const images = BODY_IMAGES[page.route] ?? [];
  // C-3 (Cycle 1): one ImageObject per body image on this page —
  // @id #body-image-N in manifest order (the same validated list the
  // <img> tags render from), caption = alt verbatim, contentUrl =
  // absolute single-prefix URL. 57 blocks across the 19 pages that
  // carry body images; pages without body images get none.
  const bodyImageLd = images.map((img, i) =>
    imageObject(page.route, `#body-image-${i}`, img),
  );
  const body: ReactNode[] = [];
  for (const sec of sections) {
    const nodes = renderSection(sec);
    const img =
      sec.h2Index >= 0
        ? images.find((im) => im.afterH2 === sec.h2Index)
        : undefined;
    if (!img) {
      body.push(<Fragment key={`sec-${sec.h2Index}`}>{nodes}</Fragment>);
      continue;
    }
    body.push(
      <div key={`sec-${sec.h2Index}`} className="h2-section with-image">
        <div className="h2-section-text">{nodes}</div>
        <figure
          className={`body-img-fig${img.layout === "sticky" ? " sticky" : ""}`}
        >
          {/* CYCLE 2 SRCSET: 400w/800w (slot 400px @1440, ~342px @390);
              attrs corrected 1200x675 -> 800x450, the true file dims.
              Same photo, same alt, no layout change. */}
          <img
            src={ASSET_PREFIX + img.src}
            srcSet={`${ASSET_PREFIX + img.src.replace(/\.webp$/, "-400.webp")} 400w, ${ASSET_PREFIX + img.src} 800w`}
            sizes="(max-width: 900px) 90vw, 400px"
            alt={img.alt}
            width={800}
            height={450}
            loading="lazy"
            decoding="async"
            className="body-img"
          />
        </figure>
      </div>,
    );
  }

  return (
    <>
      {serviceLd ? <JsonLd data={serviceLd} /> : null}
      <JsonLd data={breadcrumbLd} />
      {faqLd ? <JsonLd data={faqLd} /> : null}
      <JsonLd data={webPageLdData} />
      <JsonLd data={heroImageLd} />
      {howToLd.map((h, i) => (
        <JsonLd key={`howto-${i}`} data={h} />
      ))}
      {bodyImageLd.map((b, i) => (
        <JsonLd key={`body-image-${i}`} data={b} />
      ))}
      <PhotoHero
        image={hero.src}
        alt={hero.alt}
        eyebrow={page.eyebrow ?? "WATER DAMAGE RESTORATION \u2022 MIDVALE, UTAH"}
        h1={page.h1}
        intro={page.intro}
        trust={page.trustChips}
        breadcrumb={<Breadcrumb items={breadcrumbItems} />}
      />
      {/* C-5 (Cycle 1): the Service node's fragment @id (#service)
          resolves to this section on the 19 Service pages — the body
          section is the page's service content. No id on other pages. */}
      <section className="page-body" id={serviceLd ? "service" : undefined}>
        <div className="wrap">
          {body}
          {/* Location map (2026-11-16): one per location page, after the
              verbatim body and before the call buttons. Built from the
              already-passed areaCity/areaZip — no new data field, no
              verbatim content moves. q= form, same as the footer map
              (verified live 2026-11-16: each URL 200, Google resolves to
              the named city). */}
          {serviceKind === "location" && areaCity && areaZip ? (
            <div className="location-map">
              <iframe
                title={`Map: ${areaCity}, UT ${areaZip}`}
                src={`https://www.google.com/maps?q=${areaCity.replace(/ /g, "+")}%2C%20UT%20${areaZip}&output=embed`}
                referrerPolicy="no-referrer-when-downgrade"
                loading="lazy"
              />
            </div>
          ) : null}
          <HeroButtons />
        </div>
      </section>
    </>
  );
}
