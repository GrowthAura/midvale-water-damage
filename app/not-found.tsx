import type { Metadata } from "next";
import Link from "next/link";
import { HeroButtons } from "@/components/site";

// SEO FIX 2 (2026-11-13): Next.js auto-adds exactly ONE robots noindex to
// the not-found route (it renders before <title>, outside the metadata
// block). An explicit `robots` in this file's metadata renders a SECOND
// noindex after <description> — that was the duplicate. So: NO robots
// key here at all; the framework's single auto noindex is the only one.
// The page stays noindexed and stays unlinked / absent from the sitemap.
export const metadata: Metadata = {
  title: "Page Not Found | Water Damage Restoration Midvale UT",
};

export default function NotFound() {
  return (
    <section className="page-body">
      <div className="wrap">
        <h1>Page Not Found</h1>
        <p>Sorry, this page does not exist. You can go back to the homepage or call us any hour.</p>
        <p>
          {/* P3-1: no home prefetch here either — same basePath .txt 404. */}
          <Link href="/" prefetch={false}>Back to the homepage</Link>
        </p>
        <HeroButtons />
      </div>
    </section>
  );
}
