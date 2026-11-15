// Cycle 3 per-hero picture breakpoints (MEASURED 2026-11-14,
// qa/opt3-slots-mid.json — hero-box aspect at 390/481/560/640/700/767).
// For each hero, the viewport width where each crop stops being the best
// visible-fraction choice (object-fit: cover; visible = min(a,Ab)/max(a,Ab)).
// - mMax: widest viewport where the Cycle 2 -m crop (390-matched) wins.
// - midMax: widest viewport where the -mid crop (3:4, aspect 0.75) wins,
//   or null where it never wins (the 3 legal pages — boxes already ~1.0
//   wide at 481, so the landscape file takes over right after -m).
// The <picture> element in components/site.tsx reads this by hero slug.
// Fallback if a slug is missing: mMax 480, midMax 767 (simple scheme).
export const HERO_CROP_BP: Record<string, { mMax: number; midMax: number | null }> = {
  "about": { mMax: 516, midMax: 735 },
  "basement-flooding-cleanup": { mMax: 575, midMax: 752 },
  "basement-flooding-spring-snowmelt-utah": { mMax: 509, midMax: 730 },
  "burst-pipe-water-damage": { mMax: 554, midMax: 767 },
  "can-mold-grow-in-utah": { mMax: 475, midMax: 680 },
  "ceiling-water-damage": { mMax: 554, midMax: 767 },
  "commercial-water-damage": { mMax: 554, midMax: 752 },
  "condo-apartment-water-damage": { mMax: 570, midMax: 767 },
  "contact": { mMax: 511, midMax: 701 },
  "cottonwood-heights-ut": { mMax: 567, midMax: 767 },
  "crawl-space-water-damage": { mMax: 554, midMax: 767 },
  "disclaimer": { mMax: 534, midMax: null },
  "emergency-water-extraction": { mMax: 564, midMax: 752 },
  "frozen-pipes-midvale": { mMax: 489, midMax: 714 },
  "hardwood-floor-cabinet-drying": { mMax: 563, midMax: 752 },
  "home": { mMax: 534, midMax: 744 },
  "magna-ut": { mMax: 554, midMax: 767 },
  "midvale-water-sewer-emergency-contacts": { mMax: 515, midMax: 700 },
  "mold-remediation": { mMax: 542, midMax: 748 },
  "privacy-policy": { mMax: 534, midMax: null },
  "sewage-backup-cleanup": { mMax: 523, midMax: 735 },
  "south-salt-lake-ut": { mMax: 573, midMax: 767 },
  "storm-flood-damage": { mMax: 565, midMax: 767 },
  "swamp-cooler-leak-water-damage": { mMax: 564, midMax: 767 },
  "terms-of-use": { mMax: 534, midMax: null },
  "upstairs-unit-leak-who-pays-utah": { mMax: 515, midMax: 719 },
  "water-damage-repair": { mMax: 550, midMax: 748 },
  "water-heater-leak-cleanup": { mMax: 573, midMax: 767 },
  "water-leak-detection": { mMax: 554, midMax: 767 },
  "window-well-flooding": { mMax: 542, midMax: 745 },
  "winterize-swamp-cooler-utah": { mMax: 486, midMax: 659 },
};
