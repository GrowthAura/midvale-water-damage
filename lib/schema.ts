// Shared JSON-LD schema helpers — SCHEMA ROUND (Stage 4, 2026-11-13)
// + CYCLE 1 SCHEMA ADVANCEMENT (Batch 2, 2026-11-13): C-1 WebPage
// mainEntity linkage, C-2 AboutPage/ContactPage subtypes, C-3
// ImageObject for the 76 non-hero images, C-4 measured 1600x1066
// hero width/height, C-5 DOM ids matching fragment @ids (in the
// components). C-6 (homepage ItemList) SKIPPED — weak/redundant.
// Schema <script> blocks only; no visible rendering changes.
// HONEST-ONLY: every string traces to doc data (metaTitle,
// metaDescription, h1, intro, FAQ Q&A, ordered-list steps, hero alt,
// phone, brand, cities/ZIPs) or to the site's own chrome (footer map
// query, .hero .intro / #faq .faq-item selectors). Nothing invented:
// no totalTime, supply, tool, priceRange, sameAs, reviews, ratings,
// aggregateRating, SearchAction/potentialAction, credentials,
// addresses, founder/employee, or any fact not in the doc/site.
import { SITE, SERVICES, LOCATIONS, CARD_IMAGE, type PageImage } from "@/lib/content";
import { stripAnnotations } from "@/lib/links";

export const BUSINESS_ID = SITE.base + "/#business";
export const WEBSITE_ID = SITE.base + "/#website";

// Homepage canonical keeps the trailing slash; all other pages no-slash.
export function pageUrl(route: string): string {
  return SITE.base + (route === "/" ? "/" : route);
}

export function heroImageObject(route: string, hero: PageImage) {
  return {
    "@context": "https://schema.org",
    "@type": "ImageObject",
    "@id": pageUrl(route) + "#hero-image",
    // Rendered hero src is ASSET_PREFIX + src, but SITE.base already
    // carries the /midvale-water-damage subpath, so the absolute URL is
    // SITE.base + src (single prefix).
    contentUrl: SITE.base + hero.src,
    caption: hero.alt,
    representativeOfPage: true,
    // C-4 (Cycle 1): measured from the site's own files with PIL —
    // ALL 31 hero files are 1600x1066. NEVER the 1600x900 hero <img>
    // attributes (OBS-3: they contradict the true file ratio).
    // CAVEAT: F2 (parallel worker) replaces 3 hero files (disclaimer,
    // upstairs-unit-leak, water-damage-repair); if a replacement file
    // does not measure 1600x1066, its width/height must be re-measured
    // and corrected — the coordinator's re-verifier checks dims per file.
    width: 1600,
    height: 1066,
  };
}

// C-3 (Cycle 1): generic ImageObject for a NON-hero image — same shape
// as the hero blocks (caption = alt verbatim, contentUrl = absolute
// single-prefix URL), no representativeOfPage, no dimensions (only the
// heroes carry measured width/height). suffix is the fragment @id, e.g.
// "#body-image-0" / "#card-image-3" — unique per page by construction.
export function imageObject(route: string, suffix: string, img: PageImage) {
  return {
    "@context": "https://schema.org",
    "@type": "ImageObject",
    "@id": pageUrl(route) + suffix,
    contentUrl: SITE.base + img.src,
    caption: img.alt,
  };
}

// C-3 (Cycle 1, homepage): one ImageObject per homepage card image, in
// render order — the 16 service cards, then the 3 location cards
// (SERVICES + LOCATIONS, exactly the order app/page.tsx renders them).
// 19 blocks, @ids #card-image-0..18 on the homepage URL.
export function cardImageObjects() {
  const cards: PageImage[] = [
    ...SERVICES.map((s) => CARD_IMAGE[s.slug]),
    ...LOCATIONS.map((l) => CARD_IMAGE[l.slug]),
  ];
  return cards.map((img, i) => imageObject("/", `#card-image-${i}`, img));
}

export type WebPageInput = {
  route: string;
  metaTitle: string;
  metaDescription: string;
};

export function webPageLd(
  page: WebPageInput,
  hasFaq: boolean,
  // C-1 (Cycle 1): full @id strings of the page's own nodes to link as
  // mainEntity — pure references, zero new claims. Empty = key omitted
  // (the 3 legal pages have no FAQ/Service/HowTo node of their own).
  mainEntityIds: string[] = [],
  // C-2 (Cycle 1): AboutPage for /about, ContactPage for /contact;
  // every other route stays plain WebPage. Subtype only — all values
  // carry over unchanged.
  pageType: "WebPage" | "AboutPage" | "ContactPage" = "WebPage",
) {
  const mainEntity =
    mainEntityIds.length === 0
      ? undefined
      : mainEntityIds.length === 1
        ? { "@id": mainEntityIds[0] }
        : mainEntityIds.map((id) => ({ "@id": id }));
  return {
    "@context": "https://schema.org",
    "@type": pageType,
    "@id": pageUrl(page.route),
    name: page.metaTitle,
    description: page.metaDescription,
    url: pageUrl(page.route),
    inLanguage: "en-US",
    isPartOf: { "@id": WEBSITE_ID },
    breadcrumb: { "@id": pageUrl(page.route) + "#breadcrumb" },
    primaryImageOfPage: { "@id": pageUrl(page.route) + "#hero-image" },
    ...(mainEntity ? { mainEntity } : {}),
    speakable: {
      "@type": "SpeakableSpecification",
      // The FAQ renders as <section id="faq"><div class="faq-list">
      // <div class="faq-item">…; the hero intro renders as
      // <p class="intro"> inside .hero — the site's own classes.
      cssSelector: hasFaq
        ? ["#faq .faq-item", ".hero .intro"]
        : [".hero .intro"],
    },
  };
}

// Minimal structural shape of a DocPageData (see components/doc-page.tsx)
// — enough for HowTo generation, without a type import cycle.
export type DocSegmentShape = { t: string; b: boolean };

export type DocBlockShape =
  | { type: "h2" | "h3"; text: string }
  | { type: "p"; segments: DocSegmentShape[] }
  | { type: "ul" | "ol"; items: { segments: DocSegmentShape[] }[] }
  | { type: "table"; headers: string[]; rows: string[][] };

export type HowToPageInput = {
  route: string;
  blocks: DocBlockShape[];
};

export type HowToStepLd = {
  "@type": "HowToStep";
  name?: string;
  text: string;
};

export type HowToLd = {
  "@context": "https://schema.org";
  "@type": "HowTo";
  "@id": string;
  name: string;
  step: HowToStepLd[];
};

// Map from block index -> HowTo index n + its h2 name, for every "ol"
// block that becomes a HowTo (has a preceding h2). SINGLE source of
// truth for both the HowTo @ids (#howto-N, see howToFromBlocks) and the
// matching DOM ids on the rendered <ol> elements (C-5, doc-page.tsx) —
// the two can never drift apart.
export function howToIndexByBlock(
  blocks: DocBlockShape[],
): Map<number, { n: number; h2: string }> {
  const out = new Map<number, { n: number; h2: string }>();
  let currentH2: string | null = null;
  let n = 0;
  blocks.forEach((b, i) => {
    if (b.type === "h2") {
      currentH2 = b.text;
      return;
    }
    if (b.type !== "ol") return;
    // Every ol block in the data has a preceding h2; without one there
    // is no honest name, so no block is emitted.
    if (currentH2 === null) return;
    out.set(i, { n, h2: currentH2 });
    n += 1;
  });
  return out;
}

// One HowTo per "ol" block, named after the preceding h2 (verbatim).
// No durations, tools or supplies — none are in the doc.
// Step text strips ` (/path/)` annotation tokens (link metadata, not
// content words); the anchor phrase itself stays as plain text.
// Bold lead = the item's first segment has b === true.
export function howToFromBlocks(page: HowToPageInput): HowToLd[] {
  const out: HowToLd[] = [];
  // Map.forEach iterates in insertion (document) order.
  howToIndexByBlock(page.blocks).forEach(({ n, h2 }, i) => {
    const b = page.blocks[i];
    if (b.type !== "ol") return; // unreachable — map holds ols only
    out.push({
      "@context": "https://schema.org",
      "@type": "HowTo",
      "@id": pageUrl(page.route) + "#howto-" + n,
      name: h2,
      step: b.items.map((item) => {
        const first = item.segments[0];
        const text = stripAnnotations(
          item.segments.map((s) => s.t).join(""),
        );
        const step: HowToStepLd =
          first && first.b
            ? { "@type": "HowToStep", name: first.t.trim(), text }
            : { "@type": "HowToStep", text };
        return step;
      }),
    });
  });
  return out;
}
