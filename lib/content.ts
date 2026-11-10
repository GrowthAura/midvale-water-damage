// Midvale UT — all content VERBATIM from Google Doc "Midvale UT"
// (1ZmyWIOGUbUoaM-LRuffoWeO9xmojFAQLLaJDlYhRaDQ).
// No word added, cut, shortened or paraphrased. Paths in parentheses in the
// Doc are LINK ANNOTATIONS only — the live form is no trailing slash.
// The Doc's 4-row water-category table (missed by the plain-text extract)
// is included verbatim from doc-raw.json.

export const SITE = {
  brand: "Water Damage Restoration Midvale UT",
  city: "Midvale",
  state: "UT",
  zip: "84047",
  phoneDisplay: "(385) 337-3560",
  phoneTel: "+13853373560",
  metaTitle:
    "Water Damage Restoration Midvale UT | 24/7 Emergency Crew Dispatched Now",
  metaDescription:
    "24/7 water damage restoration in Midvale, UT 84047. Extraction, drying, sewage and mold cleanup. Crew dispatched now. Call (385) 337-3560.",
  // LOCAL-ONLY placeholder base. No domain exists in the Doc (OPEN item 1).
  // Override with NEXT_PUBLIC_SITE_URL when the real domain arrives, then
  // regenerate sitemap/canonicals before any publish.
  base:
    process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000",
} as const;

export const HERO = {
  eyebrow: "WATER DAMAGE RESTORATION \u2022 MIDVALE, UTAH",
  h1: "24/7 Water Damage Restoration in Midvale, UT 84047",
  intro:
    "Burst pipe, flooded basement or sewage coming up the floor drain? Our water damage restoration Midvale UT crew is dispatched immediately, day or night, to stop the source, pull out standing water and dry your home or business before mold can take hold. From Bingham Junction townhomes to East Midvale ramblers, every job starts with moisture readings and photos your insurance adjuster can use. Call now and help is on the way.",
  trust: [
    "24/7 Emergency Line",
    "Local to Midvale 84047",
    "Clean, Gray & Sewage Water",
    "Insurance-Ready Photo Logs",
  ],
} as const;

export type Service = {
  slug: string;
  h3: string;
  anchor: string;
  summary: string;
};

// H3 + paragraph + link anchor, verbatim. The trailing "( /path/ )" annotation
// is stored as `slug`/`anchor` only and is NOT part of the paragraph text.
export const SERVICES: Service[] = [
  {
    slug: "emergency-water-extraction",
    h3: "Emergency Water Extraction",
    anchor: "Emergency Water Extraction",
    summary:
      "Truck-mounted and submersible pumps remove standing water fast, so carpet, pad and subfloors have the best chance of being saved.",
  },
  {
    slug: "basement-flooding-cleanup",
    h3: "Basement Flooding Cleanup",
    anchor: "Basement Flooding Cleanup",
    summary:
      "Finished basements in Midvale ramblers and split-levels hold water behind paneling and under carpet. We pump out, open what must be opened and dry the rest.",
  },
  {
    slug: "window-well-flooding",
    h3: "Window Well Flooding",
    anchor: "Window Well Flooding",
    summary:
      "When a window well fills with snowmelt or storm water, it pours straight into basement bedrooms. We remove the water and dry the window framing, walls and floors.",
  },
  {
    slug: "burst-pipe-water-damage",
    h3: "Burst & Frozen Pipe Cleanup",
    anchor: "Burst Pipe Water Damage",
    summary:
      "A split line inside a wall can soak insulation, drywall and floors in minutes. We dry the cavity, not just the surface.",
  },
  {
    slug: "sewage-backup-cleanup",
    h3: "Sewage Backup Cleanup",
    anchor: "Sewage Backup Cleanup",
    summary:
      "Sewage is Category 3 water. Our crew removes it, takes out contaminated materials, disinfects and cleans the air so the space is safe again.",
  },
  {
    slug: "water-heater-leak-cleanup",
    h3: "Water Heater & Appliance Leaks",
    anchor: "Water Heater Leak Cleanup",
    summary:
      "Hard water wears out tanks, valves and supply lines. We clean up after water heaters, washers, dishwashers, fridge lines and water softeners.",
  },
  {
    slug: "swamp-cooler-leak-water-damage",
    h3: "Swamp Cooler Leaks",
    anchor: "Swamp Cooler Leak Water Damage",
    summary:
      "A stuck float valve or clogged drain pan can soak a roof deck and attic insulation before any stain shows. We dry the attic and ceiling.",
  },
  {
    slug: "ceiling-water-damage",
    h3: "Ceiling Leaks & Ice Dams",
    anchor: "Ceiling Water Damage",
    summary:
      "Upstairs bathrooms, ice dams and roof leaks show up as stains or sagging drywall. We drain, dry and repair safely.",
  },
  {
    slug: "crawl-space-water-damage",
    h3: "Crawl Space Water Damage",
    anchor: "Crawl Space Water Damage",
    summary:
      "Older homes near Historic Main Street often sit over dirt crawl spaces. We remove water, dry the joists and treat the area.",
  },
  {
    slug: "hardwood-floor-cabinet-drying",
    h3: "Hardwood Floor & Cabinet Drying",
    anchor: "Hardwood Floor & Cabinet Drying",
    summary:
      "Floor drying mats and cavity drying can save cupped hardwood and kitchen cabinets that might otherwise be torn out.",
  },
  {
    slug: "condo-apartment-water-damage",
    h3: "Condo, Townhome & Apartment Leaks",
    anchor: "Condo & Apartment Water Damage",
    summary:
      "Water moves between stacked units fast. We trace it, dry every affected unit and keep separate records for owners, renters and HOAs.",
  },
  {
    slug: "commercial-water-damage",
    h3: "Commercial Water Damage",
    anchor: "Commercial Water Damage",
    summary:
      "Offices, shops and restaurants along Fort Union Blvd, Union Park and 7200 South get after-hours drying to keep doors open.",
  },
  {
    slug: "storm-flood-damage",
    h3: "Storm & Flash Flood Cleanup",
    anchor: "Storm Water Damage",
    summary:
      "Summer storms and runoff can push dirty water into garages and basements. We treat it as contaminated water and clean accordingly.",
  },
  {
    slug: "mold-remediation",
    h3: "Mold Remediation",
    anchor: "Mold Remediation",
    summary:
      "If a leak sat too long, we contain the area, run HEPA air scrubbers and remove mold at the source.",
  },
  {
    slug: "water-leak-detection",
    h3: "Leak Detection & Moisture Mapping",
    anchor: "Water Leak Detection",
    summary:
      "Thermal imaging and moisture meters find hidden water behind walls and under floors with few or no holes.",
  },
  {
    slug: "water-damage-repair",
    h3: "Water Damage Repair & Rebuild",
    anchor: "Water Damage Repair",
    summary:
      "Once everything is dry, we put drywall, texture, paint, flooring and trim back so the space looks like it did before.",
  },
];

export const NEIGHBORHOODS = [
  {
    h3: "West Midvale: Bingham Junction, Jordan Bluffs & Historic Main Street",
    body: "West of I-15, newer townhomes and apartments around Bingham Junction, Jordan Bluffs and View 72 see washer overflows, fire sprinkler discharges and leaks that travel between units. Closer to Main Street and Center Street, older bungalows have galvanized pipes, clay sewer lines and crawl spaces. Low ground near the Jordan River adds groundwater seepage in wet springs.",
  },
  {
    h3: "East Midvale: Union Park, Fort Union & Hillcrest",
    body: "East of State Street, 1960s to 1980s ramblers and split-levels around Hillcrest, Midvale City Park and Union Park have finished basements, window wells and aging water heaters. Along Fort Union Blvd and Union Park Ave, medical offices, retail and restaurants need fast commercial drying with as little downtime as possible.",
  },
];

export type LeadItem = { lead: string; rest: string };

export const WHY_HOMES: LeadItem[] = [
  {
    lead: "Older homes:",
    rest: "about 43% of Midvale homes were built before 1980, and the median home dates to 1986. Original supply lines, galvanized pipe and clay sewer laterals are common.",
  },
  {
    lead: "Stacked living:",
    rest: "more than half of Midvale homes are rented, and about a third of housing units sit in buildings with 10 or more units. One leak can reach several homes.",
  },
  {
    lead: "Hard water:",
    rest: "Midvale's water comes from city wells and the Jordan Valley Water Conservancy District, and its mineral content builds scale in water heaters, valves and appliance lines.",
  },
  {
    lead: "More than one sewer provider:",
    rest: "Midvalley Sewer District on 7800 South and Midvale City Public Works both serve parts of the city, so the first call on a backup depends on your street.",
  },
  {
    lead: "Clay soil and groundwater:",
    rest: "snowmelt and heavy watering saturate the valley's clay soil, and groundwater near the Jordan River presses on basement walls and slabs.",
  },
  {
    lead: "Swamp coolers and ice dams:",
    rest: "rooftop evaporative coolers overflow in summer, and freeze-thaw cycles build ice dams on low-slope roofs in winter.",
  },
];

export const PROCESS: LeadItem[] = [
  {
    lead: "Stop the source.",
    rest: "We shut off the water, isolate power in wet rooms and make the space safe.",
  },
  {
    lead: "Inspect and map.",
    rest: "Moisture meters and thermal imaging show how far the water traveled, including inside walls and under floors.",
  },
  {
    lead: "Extract.",
    rest: "Truck-mounted and submersible equipment removes standing water from carpet, pad and hard floors.",
  },
  {
    lead: "Remove what can't be saved.",
    rest: "Wet pad, swollen baseboards or contaminated drywall come out, and the rest stays.",
  },
  {
    lead: "Dry and dehumidify.",
    rest: "Air movers and LGR dehumidifiers run until readings match dry areas of the home, checked every day.",
  },
  {
    lead: "Clean, then rebuild.",
    rest: "Surfaces are cleaned and treated, then drywall, flooring and trim go back in.",
  },
];

// Verbatim 4-row table from doc-raw.json (header + 3 categories).
export const CATEGORY_TABLE = {
  headers: ["Water category", "Common Midvale source", "What it means for cleanup"],
  rows: [
    [
      "Category 1 (clean)",
      "Burst supply line, water heater, fridge line",
      "Carpet and pad can often be dried in place if work starts fast",
    ],
    [
      "Category 2 (gray)",
      "Washer, dishwasher, toilet overflow without waste",
      "Pad usually comes out; surfaces are cleaned and treated",
    ],
    [
      "Category 3 (black)",
      "Sewer backup, storm runoff, river or canal water",
      "Porous materials come out; full disinfection and air cleaning",
    ],
  ],
};

export const COSTS: string[] = [
  "Water extraction and drying for one or two rooms: about $1,000 to $4,500",
  "Basement flooding cleanup: about $2,500 to $9,000",
  "Burst pipe cleanup: about $1,500 to $6,500",
  "Sewage backup cleanup: about $3,000 to $12,000",
  "Mold remediation for small to mid-sized areas: about $1,500 to $6,000",
];

export const FIRST_30: string[] = [
  "Shut off the main water valve, or the valve at the fixture that failed.",
  "Turn off power to wet rooms only if you can reach the panel without standing in water.",
  "Stop using sinks, toilets and showers if sewage is coming up a drain.",
  "Move rugs, electronics, photos and papers to a dry room.",
  "Take photos and video of everything before cleanup begins.",
  "Call (385) 337-3560 so a crew is dispatched while you work.",
];

export type Location = {
  slug: string;
  city: string;
  zip: string;
  anchor: string;
  // Full verbatim sentence from "Nearby Cities We Serve" (lead-in + rest).
  lead: string;
  rest: string;
};

export const LOCATIONS: Location[] = [
  {
    slug: "cottonwood-heights-ut",
    city: "Cottonwood Heights",
    zip: "84121",
    anchor: "Water Damage Restoration Cottonwood Heights",
    lead: "Cottonwood Heights, UT 84121:",
    rest: "snowmelt seepage, ice dams and burst pipes in bench homes below the canyons.",
  },
  {
    slug: "south-salt-lake-ut",
    city: "South Salt Lake",
    zip: "84115",
    anchor: "Water Damage Restoration South Salt Lake",
    lead: "South Salt Lake, UT 84115:",
    rest: "apartment leaks, sewer backups and warehouse floods.",
  },
  {
    slug: "magna-ut",
    city: "Magna",
    zip: "84044",
    anchor: "Water Damage Restoration Magna",
    lead: "Magna, UT 84044:",
    rest: "older-home pipe failures, sewer lines and crawl spaces near Main Street.",
  },
];

export const GUIDE = {
  slug: "midvale-water-sewer-emergency-contacts",
  h1: "Midvale Water & Sewer Emergency Contacts",
  // The one verbatim sentence about this page in the Doc (from "What to Do
  // in the First 30 Minutes"). The parenthesised path annotation is dropped
  // on its own page so the page does not link to itself.
  sentence:
    "For sewer backups, the Midvale Water & Sewer Emergency Contacts page lists who to call about the public line.",
};

export const FAQ = [
  {
    q: "How fast can a crew reach my Midvale home?",
    a: "A crew is dispatched immediately after your call, day or night. Travel time depends on where you are in 84047 and traffic on I-15, State Street and 7200 South.",
  },
  {
    q: "Can wet carpet and pad be saved after a leak?",
    a: "Often, yes, if the water is clean and extraction starts within 24 to 48 hours. Pad soaked by gray water or sewage has to be removed.",
  },
  {
    q: "Can mold grow in Midvale when Utah air is so dry?",
    a: "Yes. Outdoor air is dry, but a wet wall cavity or carpet pad stays damp inside, and mold can start growing on wet drywall within 24 to 48 hours.",
  },
  {
    q: "Who do I call first for a sewer backup in Midvale?",
    a: "Stop using water, then call your sewer provider to check the public line. Midvalley Sewer District asks residents to call it first. After that, call a crew to clean up the sewage.",
  },
  {
    q: "How long does drying take?",
    a: "Most homes dry in about 3 to 5 days. Hardwood, crawl spaces and thick materials can take longer, and we only stop when readings match the dry parts of the home.",
  },
  {
    q: "Do you work with renters, landlords and property managers?",
    a: "Yes. As a water damage cleanup company used to multi-unit buildings, we keep separate records for each unit so owners, tenants and HOAs each get what they need.",
  },
];

export const ALL_ROUTES: string[] = [
  "/",
  ...SERVICES.map((s) => `/${s.slug}`),
  `/${GUIDE.slug}`,
  ...LOCATIONS.map((l) => `/locations/${l.slug}`),
];

// HERO + A-to-Z ROUND (2026-11-10): one UNIQUE darkened photographic hero
// image per page (21 heroes, 0 repeats) + one photographic card image per
// service/location card (19 cards, 0 repeats, different scene from the hero).
// All generated fresh for Midvale only — zero past-site images, no "AI" word
// in filename/path/alt/metadata, AI metadata stripped (exiftool + byte-scan),
// never claimed as real job photos (generated illustrations).
// Keys: "home", service slugs, GUIDE.slug, location slugs.
export type PageImage = { src: string; alt: string };
export const HERO_IMAGE: Record<string, PageImage> = {
  home: { src: "/images/heroes/home.webp", alt: "Restoration crew extracting standing water from a flooded Midvale home at dusk, Wasatch mountains in the background" },
  "emergency-water-extraction": { src: "/images/heroes/emergency-water-extraction.webp", alt: "Crew operating a truck-mounted extraction unit in a flooded Midvale basement" },
  "basement-flooding-cleanup": { src: "/images/heroes/basement-flooding-cleanup.webp", alt: "Flooded finished basement in a Midvale rambler, crew pumping out water" },
  "window-well-flooding": { src: "/images/heroes/window-well-flooding.webp", alt: "Basement window well filled with snowmelt water in Midvale, Utah" },
  "burst-pipe-water-damage": { src: "/images/heroes/burst-pipe-water-damage.webp", alt: "Split copper pipe spraying water inside a dark wall cavity" },
  "sewage-backup-cleanup": { src: "/images/heroes/sewage-backup-cleanup.webp", alt: "Crew in protective gear cleaning a sewage backup in a Midvale bathroom" },
  "water-heater-leak-cleanup": { src: "/images/heroes/water-heater-leak-cleanup.webp", alt: "Leaking water heater in a dark Midvale utility closet" },
  "swamp-cooler-leak-water-damage": { src: "/images/heroes/swamp-cooler-leak-water-damage.webp", alt: "Rooftop swamp cooler leaking onto a wet roof deck in Midvale" },
  "ceiling-water-damage": { src: "/images/heroes/ceiling-water-damage.webp", alt: "Sagging water-stained ceiling with ice dam on a low-slope Midvale roof" },
  "crawl-space-water-damage": { src: "/images/heroes/crawl-space-water-damage.webp", alt: "Technician with a headlamp in a dark dirt crawl space under a Midvale home" },
  "hardwood-floor-cabinet-drying": { src: "/images/heroes/hardwood-floor-cabinet-drying.webp", alt: "Cupped hardwood floor with drying mats and air movers in a Midvale kitchen" },
  "condo-apartment-water-damage": { src: "/images/heroes/condo-apartment-water-damage.webp", alt: "Water leaking through the ceiling of a stacked Midvale apartment unit" },
  "commercial-water-damage": { src: "/images/heroes/commercial-water-damage.webp", alt: "After-hours drying in a dark Midvale restaurant, air movers running" },
  "storm-flood-damage": { src: "/images/heroes/storm-flood-damage.webp", alt: "Storm runoff flooding a Midvale garage at night" },
  "mold-remediation": { src: "/images/heroes/mold-remediation.webp", alt: "Mold remediation containment with HEPA air scrubber in a Midvale home" },
  "water-leak-detection": { src: "/images/heroes/water-leak-detection.webp", alt: "Technician with a thermal imaging camera finding hidden water in a Midvale wall" },
  "water-damage-repair": { src: "/images/heroes/water-damage-repair.webp", alt: "Newly rebuilt room in a Midvale home, fresh drywall and trim" },
  "midvale-water-sewer-emergency-contacts": { src: "/images/heroes/midvale-water-sewer-emergency-contacts.webp", alt: "Utility crew truck with amber lights beside a sewer manhole on a dark Midvale street" },
  "cottonwood-heights-ut": { src: "/images/heroes/cottonwood-heights-ut.webp", alt: "Bench homes below the snowy Wasatch canyons in Cottonwood Heights, Utah" },
  "south-salt-lake-ut": { src: "/images/heroes/south-salt-lake-ut.webp", alt: "Apartment and warehouse buildings in South Salt Lake, Utah at dusk" },
  "magna-ut": { src: "/images/heroes/magna-ut.webp", alt: "Older homes on historic Main Street in Magna, Utah at dusk" },
};

export const CARD_IMAGE: Record<string, PageImage> = {
  "emergency-water-extraction": { src: "/images/cards/emergency-water-extraction.webp", alt: "Submersible pump and extraction hose in standing water on a basement floor" },
  "basement-flooding-cleanup": { src: "/images/cards/basement-flooding-cleanup.webp", alt: "Wet carpet and pad being pulled back in a flooded finished basement" },
  "window-well-flooding": { src: "/images/cards/window-well-flooding.webp", alt: "Basement window well half full of snowmelt water" },
  "burst-pipe-water-damage": { src: "/images/cards/burst-pipe-water-damage.webp", alt: "Burst frozen pipe joint with ice and water spraying in a dark crawl space" },
  "sewage-backup-cleanup": { src: "/images/cards/sewage-backup-cleanup.webp", alt: "Floor drain with sewage backup water in a dark basement bathroom" },
  "water-heater-leak-cleanup": { src: "/images/cards/water-heater-leak-cleanup.webp", alt: "Corroded water heater valve dripping onto a wet concrete floor" },
  "swamp-cooler-leak-water-damage": { src: "/images/cards/swamp-cooler-leak-water-damage.webp", alt: "Rooftop swamp cooler drain pan overflowing onto a wet roof deck" },
  "ceiling-water-damage": { src: "/images/cards/ceiling-water-damage.webp", alt: "Brown water stain spreading across a ceiling with a drip forming" },
  "crawl-space-water-damage": { src: "/images/cards/crawl-space-water-damage.webp", alt: "Wet floor joists and standing water in a dark dirt crawl space" },
  "hardwood-floor-cabinet-drying": { src: "/images/cards/hardwood-floor-cabinet-drying.webp", alt: "Cupped hardwood floor planks with a drying mat and air mover hose" },
  "condo-apartment-water-damage": { src: "/images/cards/condo-apartment-water-damage.webp", alt: "Water dripping from a ceiling light fixture in a dark apartment" },
  "commercial-water-damage": { src: "/images/cards/commercial-water-damage.webp", alt: "Air movers and a dehumidifier drying wet commercial carpet tiles" },
  "storm-flood-damage": { src: "/images/cards/storm-flood-damage.webp", alt: "Dirty storm runoff water flooding a garage floor with a sump pump" },
  "mold-remediation": { src: "/images/cards/mold-remediation.webp", alt: "HEPA air scrubber with ducting beside plastic containment sheeting" },
  "water-leak-detection": { src: "/images/cards/water-leak-detection.webp", alt: "Moisture meter pressed against a wet wall beside a thermal camera" },
  "water-damage-repair": { src: "/images/cards/water-damage-repair.webp", alt: "Fresh drywall texture and new white trim being finished in a room" },
  "cottonwood-heights-ut": { src: "/images/cards/cottonwood-heights-ut.webp", alt: "Bench homes below snowy Wasatch canyons in Cottonwood Heights, Utah" },
  "south-salt-lake-ut": { src: "/images/cards/south-salt-lake-ut.webp", alt: "Apartment blocks and warehouse buildings in South Salt Lake, Utah" },
  "magna-ut": { src: "/images/cards/magna-ut.webp", alt: "Older brick homes and storefronts on historic Main Street in Magna, Utah" },
};

export function serviceBySlug(slug: string): Service | undefined {
  return SERVICES.find((s) => s.slug === slug);
}

export function locationBySlug(slug: string): Location | undefined {
  return LOCATIONS.find((l) => l.slug === slug);
}
