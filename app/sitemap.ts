import type { MetadataRoute } from "next";
import { SITE } from "@/lib/content";
import { DOC_PAGES } from "@/components/doc-page";

// Date-only lastmod (YYYY-MM-DD), real build date — never a time, never invented.
const LASTMOD = "2026-11-12";

export default function sitemap(): MetadataRoute.Sitemap {
  return DOC_PAGES.map((page) => ({
    url: `${SITE.base}${page.route === "/" ? "/" : page.route}`,
    // NOTE: the field is `lastModified` — the earlier `lastmod` key was
    // silently dropped by Next and the built sitemap had NO lastmod at all
    // (caught by the hero-az extras check, 2026-11-10).
    lastModified: LASTMOD,
  }));
}
