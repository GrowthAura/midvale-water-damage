import type { Metadata } from "next";
import Link from "next/link";
import { HeroButtons } from "@/components/site";

// 10X FIX B-O2: the default 404 page carried TWO robots metas (layout's
// index,follow + Next's auto noindex). This custom 404 has exactly one:
// noindex. The page is unlinked and absent from the sitemap.
export const metadata: Metadata = {
  title: "Page Not Found | Water Damage Restoration Midvale UT",
  robots: "noindex",
};

export default function NotFound() {
  return (
    <section className="page-body">
      <div className="wrap">
        <h1>Page Not Found</h1>
        <p>Sorry — this page does not exist. You can go back to the homepage or call us any hour.</p>
        <p>
          {/* P3-1: no home prefetch here either — same basePath .txt 404. */}
          <Link href="/" prefetch={false}>Back to the homepage</Link>
        </p>
        <HeroButtons />
      </div>
    </section>
  );
}
