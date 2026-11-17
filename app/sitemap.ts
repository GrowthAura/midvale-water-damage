import type { MetadataRoute } from "next";
import { SITE } from "@/lib/content";
import { DOC_PAGES } from "@/components/doc-page";

// Date-only lastmod (YYYY-MM-DD), real push dates — never a time, never invented.
// Split 2026-11-17 (half/half, owner order 2026-11-17 ~13:10 PKT): 16 pages dated
// 2026-11-17 — the homepage + all 15 service pages (the 6 menu services + the 9
// other footer services except window-well-flooding). The other 15 pages keep
// 2026-11-16: window-well-flooding, the 3 locations, the 5 blogs, the guide,
// About, Contact, and the 3 legal pages.
const LASTMOD_2026_11_17 = new Set([
  "/",
  "/emergency-water-extraction",
  "/water-damage-repair",
  "/basement-flooding-cleanup",
  "/burst-pipe-water-damage",
  "/sewage-backup-cleanup",
  "/mold-remediation",
  "/water-heater-leak-cleanup",
  "/swamp-cooler-leak-water-damage",
  "/ceiling-water-damage",
  "/crawl-space-water-damage",
  "/hardwood-floor-cabinet-drying",
  "/condo-apartment-water-damage",
  "/commercial-water-damage",
  "/storm-flood-damage",
  "/water-leak-detection",
]);

export default function sitemap(): MetadataRoute.Sitemap {
  return DOC_PAGES.map((page) => ({
    url: `${SITE.base}${page.route === "/" ? "/" : page.route}`,
    // NOTE: the field is `lastModified` — the earlier `lastmod` key was
    // silently dropped by Next and the built sitemap had NO lastmod at all
    // (caught by the hero-az extras check, 2026-11-10).
    lastModified: LASTMOD_2026_11_17.has(page.route) ? "2026-11-17" : "2026-11-16",
  }));
}
