// Pure presentational panels — SERVER-SAFE module (no "use client").
// A Server Component may not import plain functions from a "use client"
// file, so the panels live here. No raster image anywhere on the site:
// fresh inline SVG/CSS branded panels only. No photo is claimed to be a
// real job photo; no AI word, no AI metadata.
import { ASSET_PREFIX } from "@/lib/content";
const GLYPHS: Record<string, JSX.Element> = {
  drop: <path d="M32 6C32 6 14 26 14 40a18 18 0 0 0 36 0C50 26 32 6 32 6Z" />,
  waves: (
    <path d="M6 22c8-8 16 8 24 0s16 8 24 0M6 34c8-8 16 8 24 0s16 8 24 0M6 46c8-8 16 8 24 0s16 8 24 0" />
  ),
  pipe: <path d="M10 14h30a8 8 0 0 1 8 8v10M10 26h22a8 8 0 0 1 8 8v14" />,
  home: <path d="M8 30 32 10l24 20M14 28v22h36V28M26 50V38h12v12" />,
  gauge: <path d="M12 44a20 20 0 1 1 40 0M32 44l10-12" />,
  shield: <path d="M32 6l22 8v16c0 14-10 24-22 28C20 54 10 44 10 30V14Z" />,
};

const SERVICE_GLYPH: Record<string, string> = {
  "emergency-water-extraction": "waves",
  "basement-flooding-cleanup": "waves",
  "window-well-flooding": "drop",
  "burst-pipe-water-damage": "pipe",
  "sewage-backup-cleanup": "shield",
  "water-heater-leak-cleanup": "gauge",
  "swamp-cooler-leak-water-damage": "home",
  "ceiling-water-damage": "drop",
  "crawl-space-water-damage": "home",
  "hardwood-floor-cabinet-drying": "home",
  "condo-apartment-water-damage": "home",
  "commercial-water-damage": "shield",
  "storm-flood-damage": "waves",
  "mold-remediation": "shield",
  "water-leak-detection": "gauge",
  "water-damage-repair": "home",
};

export function Panel({ glyph, tone, label }: { glyph: string; tone: number; label: string }) {
  return (
    <div className={`panel tone-${tone}`} role="img" aria-label={label}>
      <svg className="panel-ridge" viewBox="0 0 640 120" preserveAspectRatio="none" aria-hidden="true">
        <path d="M0 120 L90 40 L170 100 L260 20 L350 95 L440 45 L530 105 L640 30 L640 120 Z" />
      </svg>
      <svg className="panel-glyph" viewBox="0 0 64 64" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        {GLYPHS[glyph] || GLYPHS.drop}
      </svg>
      <span className="panel-tag">MIDVALE, UT</span>
    </div>
  );
}

export function servicePanel(slug: string, index: number) {
  return (
    <Panel
      glyph={SERVICE_GLYPH[slug] || "drop"}
      tone={index % 3}
      label={`${slug.replaceAll("-", " ")}, Midvale, UT`}
    />
  );
}

/* HERO + A-to-Z ROUND: photographic card image (16:9, height auto with
   aspect-ratio — width/height attrs alone must never set the box height).
   Replaces the SVG panel on service + area cards. One unique photo per
   card, different scene from that page's hero image. */
export function CardImage({ src, alt }: { src: string; alt: string }) {
  return <img className="card-img" src={ASSET_PREFIX + src} alt={alt} width={800} height={450} loading="lazy" />;
}
