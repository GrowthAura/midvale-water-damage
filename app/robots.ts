import type { MetadataRoute } from "next";
import { SITE } from "@/lib/content";

// Robots is dynamic (uses SITE.base) so every export — GitHub Pages or a
// real domain — carries its own sitemap line. A static public/robots.txt
// hardcoded the Pages URL and leaked it into the Cloudflare export
// (caught 2026-11-14 before deploy). Allow: / and NO Host: line, per
// the standing rule.
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: "*", allow: "/" }],
    sitemap: `${SITE.base}/sitemap.xml`,
  };
}
