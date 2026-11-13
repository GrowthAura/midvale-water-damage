import { SITE } from "@/lib/content";
import { DOC_PAGES } from "@/components/doc-page";

// llms.txt is dynamic (uses SITE.base) so every export lists its own
// URLs. The old static public/llms.txt hardcoded the Pages URL and
// leaked it into the Cloudflare export (caught 2026-11-14 before
// deploy). Same 31 routes as the sitemap, one URL per line.
export async function GET() {
  const lines = [`# ${SITE.brand}`, ""];
  for (const page of DOC_PAGES) {
    lines.push(
      `${SITE.base}${page.route === "/" ? "/" : page.route}`,
    );
  }
  return new Response(lines.join("\n") + "\n", {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
