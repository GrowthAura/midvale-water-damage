// Generic DocPage renderer (REBUILD 2026-11-12). Renders ONE page object
// from lib/pages-data.json — 1001% verbatim, no word added, cut or
// paraphrased. No builder-added links or words. Parenthetical "(...)" path
// text inside paragraphs stays PLAIN text (it is plain text in the data).
// Server component. Header/footer/sticky-bar/breadcrumb are template
// chrome and excluded from the verbatim word-diff, as before.
import type { ReactNode } from "react";
import { SITE, HERO_IMAGE } from "@/lib/content";
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

// HERO_IMAGE keys are route slugs: bare slug for flat + location pages,
// "resources/<slug>" for blogs, "home" for the homepage.
export function heroKeyForRoute(route: string): string {
  if (route === "/") return "home";
  if (route.startsWith("/locations/")) return route.slice("/locations/".length);
  if (route.startsWith("/resources/")) return route.slice(1);
  return route.slice(1);
}

export type BreadcrumbItem = { label: string; href?: string };

function renderSegments(segments: DocSegment[], keyPrefix: string): ReactNode[] {
  return segments.map((s, i) =>
    s.b ? (
      <strong key={`${keyPrefix}-${i}`}>{s.t}</strong>
    ) : (
      <span key={`${keyPrefix}-${i}`}>{s.t}</span>
    ),
  );
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
  const url = `${SITE.base}${page.route === "/" ? "/" : page.route}`;

  const breadcrumbLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
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
          mainEntity: page.faqs.map((f) => ({
            "@type": "Question",
            name: f.q,
            acceptedAnswer: { "@type": "Answer", text: f.a },
          })),
        }
      : null;

  const serviceLd =
    serviceKind === "service"
      ? {
          "@context": "https://schema.org",
          "@type": "Service",
          name: page.h1,
          serviceType: page.h1,
          url,
          areaServed: {
            "@type": "City",
            name: "Midvale",
            addressRegion: "UT",
            postalCode: "84047",
          },
          provider: {
            "@type": "HomeAndConstructionBusiness",
            name: SITE.brand,
            telephone: SITE.phoneTel,
            url: SITE.base + "/",
          },
        }
      : serviceKind === "location"
        ? {
            "@context": "https://schema.org",
            "@type": "Service",
            name: page.h1,
            serviceType: "Water Damage Restoration",
            url,
            areaServed: {
              "@type": "City",
              name: areaCity,
              addressRegion: "UT",
              postalCode: areaZip,
            },
            provider: {
              "@type": "HomeAndConstructionBusiness",
              name: SITE.brand,
              telephone: SITE.phoneTel,
              url: SITE.base + "/",
            },
          }
        : null;

  // Body blocks in order. The H2 containing "FAQ" opens
  // <section id="faq"><div className="faq-list">; each following h3 + its
  // answer p becomes one .faq-item; the next non-FAQ h2 (the closing-CTA
  // h2) closes the section and renders as a normal h2.
  const body: ReactNode[] = [];
  let inFaq = false;
  let faqH2 = "";
  let faqItems: ReactNode[] = [];
  let pendingQ: string | null = null;

  const flushFaq = (key: string) => {
    if (!inFaq) return;
    body.push(
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

  page.blocks.forEach((b, i) => {
    if (b.type === "h2") {
      if (b.text.includes("FAQ")) {
        flushFaq(`faq-${i}`);
        inFaq = true;
        faqH2 = b.text;
        return;
      }
      flushFaq(`faq-${i}`);
      body.push(<h2 key={i}>{b.text}</h2>);
      return;
    }
    if (b.type === "h3") {
      if (inFaq) {
        pendingQ = b.text;
        return;
      }
      body.push(<h3 key={i}>{b.text}</h3>);
      return;
    }
    if (b.type === "p") {
      if (inFaq && pendingQ !== null) {
        faqItems.push(
          <div className="faq-item" key={i}>
            <h3>{pendingQ}</h3>
            <p>{renderSegments(b.segments, `f${i}`)}</p>
          </div>,
        );
        pendingQ = null;
        return;
      }
      body.push(<p key={i}>{renderSegments(b.segments, `p${i}`)}</p>);
      // P2-3 (2026-11-12): the Contact tab names its submit button in this
      // paragraph ("[Send My Request]") — the actual form (template chrome,
      // excluded from the verbatim diff) renders right after it, where the
      // doc says the form belongs. Contact route only.
      if (
        page.route === "/contact" &&
        b.segments.map((s) => s.t).join("") === "[Send My Request]"
      ) {
        body.push(<ContactForm key={`contact-form-${i}`} />);
      }
      return;
    }
    if (b.type === "ul" || b.type === "ol") {
      const Tag = b.type;
      body.push(
        <Tag key={i}>
          {b.items.map((item, j) => (
            <li key={j}>{renderSegments(item.segments, `li${i}-${j}`)}</li>
          ))}
        </Tag>,
      );
      return;
    }
    if (b.type === "table") {
      body.push(
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
                    <td key={c}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>,
      );
      return;
    }
  });
  flushFaq("faq-end");

  return (
    <>
      {serviceLd ? <JsonLd data={serviceLd} /> : null}
      <JsonLd data={breadcrumbLd} />
      {faqLd ? <JsonLd data={faqLd} /> : null}
      <PhotoHero
        image={hero.src}
        alt={hero.alt}
        eyebrow={page.eyebrow ?? "WATER DAMAGE RESTORATION \u2022 MIDVALE, UTAH"}
        h1={page.h1}
        intro={page.intro}
        trust={page.trustChips}
        breadcrumb={<Breadcrumb items={breadcrumbItems} />}
      />
      <section className="page-body">
        <div className="wrap">
          {body}
          <HeroButtons />
        </div>
      </section>
    </>
  );
}
