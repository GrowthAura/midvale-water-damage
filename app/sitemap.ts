import type { MetadataRoute } from "next";
import { SITE, ALL_ROUTES } from "@/lib/content";

// Date-only lastmod (YYYY-MM-DD), real build date — never a time, never invented.
const LASTMOD = "2026-11-10";

export default function sitemap(): MetadataRoute.Sitemap {
  return ALL_ROUTES.map((route) => ({
    url: `${SITE.base}${route === "/" ? "/" : route}`,
    // NOTE: the field is `lastModified` — the earlier `lastmod` key was
    // silently dropped by Next and the built sitemap had NO lastmod at all
    // (caught by the hero-az extras check, 2026-11-10).
    lastModified: LASTMOD,
  }));
}
