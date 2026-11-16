import type { MetadataRoute } from "next";
import { SITE } from "@/lib/content";
import { DOC_PAGES } from "@/components/doc-page";

// Date-only lastmod (YYYY-MM-DD), real push dates — never a time, never invented.
// Split 2026-11-17: the 7 pages dated 2026-11-17 are the homepage + the 6 core
// service pages reviewed in the 2026-11-17 sitemap-date-split round. The other
// 24 pages keep 2026-11-16, the real last-push date (nav/footer + mold rounds
// both went live 2026-11-16). PREMISE GAP (recorded 2026-11-17): before this
// change ALL 31 pages were 2026-11-12 — so setting the 24 to 2026-11-16 IS a
// change, not a keep. The end state below is still correct per the real dates.
const LASTMOD_2026_11_17 = new Set([
  "/",
  "/emergency-water-extraction",
  "/water-damage-repair",
  "/basement-flooding-cleanup",
  "/burst-pipe-water-damage",
  "/sewage-backup-cleanup",
  "/mold-remediation",
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
