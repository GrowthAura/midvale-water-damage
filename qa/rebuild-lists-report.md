# Midvale UT — List Re-classification Report

Script: `qa/rebuild-lists.py` — re-classifies the 152 flat-`p` list groups from `qa/rebuild-parse-report.md` Appendix A into true `ul`/`ol` blocks, using only the glyphs rendered in the independent Drive text export `qa/r3-full-doc/doc-export.txt`. Patches `lib/pages-data.json` in place; the parser was NOT re-run and `pages-data.json` was NOT regenerated.

## Method (classification rule, exact, no exceptions)

- Groups were re-derived from `qa/r3-full-doc/doc-full.json` exactly the way `qa/rebuild-parser.py` formed them: maximal runs of consecutive bullet paragraphs sharing one `listId`, starting after each tab's intro / buttons / trust lines. Derived: **152 groups / 862 items**, per-tab counts identical to parse-report §5 — the inventory matches Appendix A.
- Export index: every line of `doc-export.txt` starting with a glyph was indexed by its text after stripping ONE leading glyph (`^\d+\. ` + at most one space for numbered, `^[*•\-] ` + at most one space for bulleted). Glyph lines found: **237 numbered + 629 bulleted = 866** over 3399 export lines, 848 distinct stripped texts.
- For each group, every item's full text (segments joined, exactly as in `pages-data.json`) had to match an export line EXACTLY, character-for-character, after glyph stripping — no fuzzy matching, no trimming of inner whitespace.
- Whole group classified `ol` only if EVERY item matches a NUMBERED line; `ul` only if EVERY item matches a BULLETED line. If any item has no exact match, or the group's matches mix numbered and bulleted, or two export lines match the same item text, the WHOLE group stays flat `{type:'p'}` and is listed below as UNCLASSIFIED with the exact reason.
- A classified group has its run of `{type:'p'}` blocks replaced by ONE block `{type:'ol'|'ul', items:[{segments:[...]}...]}` preserving item order and every segment (bold flags included) exactly. No word was changed. No h2/h3/table/faq block, meta, h1, intro, eyebrow, trustChips or `counts.words` was touched.

## Verdict

**Classified `ol`: 32 groups · Classified `ul`: 97 groups · Left UNCLASSIFIED: 23 groups** (of 152). Of the classified groups, 0 ol + 0 ul were classified by this run and 129 were already classified by a previous run. Items re-classified this run: 0 of 862.

## 1. Groups classified `ol` (in the file)

0 classified by this run, 32 by a previous run.
| # | Tab | Route | Items | First item (≤60 chars) |
|---:|---|---|---:|---|---|
| 2 | 1 | `/` | 6 | Stop the source. We shut off the water, isolate power in ... |
| 7 | 2 | `/about` | 7 | We answer, day or night. Your call is answered any hour, ... |
| 13 | 4 | `/emergency-water-extraction` | 4 | Minutes 0 to 10: make it safe. We confirm the water sourc... |
| 18 | 5 | `/basement-flooding-cleanup` | 7 | Stop the source and make it safe. We shut off water or id... |
| 22 | 6 | `/window-well-flooding` | 8 | Lower the water outside. We pump or remove water from the... |
| 26 | 7 | `/burst-pipe-water-damage` | 7 | Confirm the water is off. We make sure the source is shut... |
| 30 | 8 | `/sewage-backup-cleanup` | 7 | Stop all water use. No flushing, showers, laundry or dish... |
| 31 | 8 | `/sewage-backup-cleanup` | 8 | Protect and contain. Crews wear protective gear, and the ... |
| 33 | 9 | `/water-heater-leak-cleanup` | 6 | Shut off the cold water at the valve on the line into the... |
| 34 | 9 | `/water-heater-leak-cleanup` | 7 | Confirm the source is off and make the area safe. |
| 40 | 10 | `/swamp-cooler-leak-water-damage` | 7 | Stop the water. We confirm the cooler's water supply is o... |
| 43 | 11 | `/ceiling-water-damage` | 7 | Stop the source or confirm a plumber or roofer has. |
| 47 | 12 | `/crawl-space-water-damage` | 7 | Check safety. We confirm the water source is off and chec... |
| 52 | 13 | `/hardwood-floor-cabinet-drying` | 6 | Extract surface water right away, including from the seams. |
| 53 | 13 | `/hardwood-floor-cabinet-drying` | 5 | Remove the toe kick at the bottom front of the cabinets t... |
| 58 | 14 | `/condo-apartment-water-damage` | 7 | Knock on the unit above or call them. If no one answers, ... |
| 61 | 14 | `/condo-apartment-water-damage` | 7 | Find and stop the source with the help of the owner, tena... |
| 65 | 15 | `/commercial-water-damage` | 6 | Protect people and data. Isolate power in wet areas, and ... |
| 67 | 15 | `/commercial-water-damage` | 9 | Respond and assess with the owner or manager, and agree o... |
| 78 | 17 | `/mold-remediation` | 8 | Find the moisture. We locate the water source and make su... |
| 85 | 18 | `/water-leak-detection` | 5 | Turn off every faucet, appliance, irrigation system and t... |
| 87 | 18 | `/water-leak-detection` | 5 | Take readings in a dry area of the same home to set a bas... |
| 93 | 19 | `/water-damage-repair` | 5 | Final dry check. Moisture readings confirm walls, floors ... |
| 99 | 20 | `/locations/cottonwood-heights-ut` | 6 | Find the source: groundwater, a window well, a water heat... |
| 111 | 22 | `/locations/magna-ut` | 5 | Shutting off the main valve and finding where water trave... |
| 116 | 23 | `/midvale-water-sewer-emergency-contacts` | 5 | Stop using water. No flushing, showers, laundry or dishwa... |
| 118 | 23 | `/midvale-water-sewer-emergency-contacts` | 4 | Find the valve. In most Midvale homes it's in the basemen... |
| 128 | 27 | `/resources/frozen-pipes-midvale` | 6 | Shut off the main water valve first if you suspect a spli... |
| 129 | 27 | `/resources/frozen-pipes-midvale` | 7 | Shut off the main water valve. In most Midvale homes it's... |
| 131 | 28 | `/resources/winterize-swamp-cooler-utah` | 10 | Turn off the power. Switch the cooler off at the thermost... |
| 135 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 6 | Stop the water if you can. Knock on the door of the unit ... |
| 140 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 5 | Shut off the water at the fixture or your unit's main valve. |

## 2. Groups classified `ul` (in the file)

0 classified by this run, 97 by a previous run.
| # | Tab | Route | Items | First item (≤60 chars) |
|---:|---|---|---:|---|---|
| 1 | 1 | `/` | 6 | Older homes: about 43% of Midvale homes were built before... |
| 5 | 1 | `/` | 3 | Cottonwood Heights, UT 84121: snowmelt seepage, ice dams ... |
| 6 | 2 | `/about` | 8 | Burst and frozen pipes in older homes and new townhomes. |
| 8 | 2 | `/about` | 5 | Straight answers. We explain what we found, what we recom... |
| 9 | 2 | `/about` | 16 | Emergency Water Extraction (/emergency-water-extraction/) |
| 10 | 3 | `/contact` | 7 | Your address and the best callback number. |
| 11 | 3 | `/contact` | 6 | Name |
| 12 | 3 | `/contact` | 3 | Sewer backup: stop using water and call your sewer provid... |
| 14 | 4 | `/emergency-water-extraction` | 3 | Clean water (Category 1): a burst supply line, a failed w... |
| 15 | 4 | `/emergency-water-extraction` | 3 | Extraction and drying for one or two rooms: about $1,000 ... |
| 16 | 4 | `/emergency-water-extraction` | 4 | Shut off the main water valve or the fixture valve. |
| 17 | 4 | `/emergency-water-extraction` | 4 | Use a household vacuum. A shop vac can help with a small ... |
| 19 | 5 | `/basement-flooding-cleanup` | 3 | Small area, clean water, caught early: about $1,500 to $3... |
| 20 | 5 | `/basement-flooding-cleanup` | 7 | Slope soil away from the foundation so water drains out, ... |
| 23 | 6 | `/window-well-flooding` | 3 | One bedroom, clean water, caught early: about $1,500 to $... |
| 24 | 7 | `/burst-pipe-water-damage` | 4 | Main shut-off valve: usually in the basement or utility r... |
| 25 | 7 | `/burst-pipe-water-damage` | 6 | Water stopped or slowed to a trickle during a cold snap, ... |
| 27 | 7 | `/burst-pipe-water-damage` | 4 | First hour: water spreads across the floor, soaks carpet ... |
| 28 | 7 | `/burst-pipe-water-damage` | 3 | One wall or one room, caught fast: about $1,500 to $3,500 |
| 29 | 7 | `/burst-pipe-water-damage` | 8 | Disconnect garden hoses and drain outside faucets before ... |
| 32 | 8 | `/sewage-backup-cleanup` | 3 | Single bathroom or small area: about $1,500 to $4,000 |
| 35 | 9 | `/water-heater-leak-cleanup` | 4 | Ramblers and split-levels in Hillcrest and East Midvale: ... |
| 36 | 9 | `/water-heater-leak-cleanup` | 6 | Vinyl or laminate flooring lifting or feeling spongy near... |
| 37 | 9 | `/water-heater-leak-cleanup` | 3 | Small leak caught early, one room: about $1,200 to $2,500 |
| 41 | 10 | `/swamp-cooler-leak-water-damage` | 3 | Small ceiling stain, caught early: about $800 to $2,000 |
| 44 | 11 | `/ceiling-water-damage` | 6 | Paint that bubbles, peels or looks wrinkled. |
| 45 | 11 | `/ceiling-water-damage` | 3 | Small stain, dried and repainted: about $600 to $1,200 |
| 46 | 12 | `/crawl-space-water-damage` | 6 | A musty or earthy smell inside the house, stronger in roo... |
| 48 | 12 | `/crawl-space-water-damage` | 4 | Historic Main Street, Center Street and Holden Street: ol... |
| 49 | 12 | `/crawl-space-water-damage` | 5 | Electrical: old wiring, junction boxes and extension cord... |
| 50 | 12 | `/crawl-space-water-damage` | 7 | Insulate pipes in the crawl space and close foundation ve... |
| 51 | 12 | `/crawl-space-water-damage` | 3 | Small clean-water leak, caught early: about $1,500 to $3,000 |
| 54 | 13 | `/hardwood-floor-cabinet-drying` | 4 | Kitchens across Midvale: dishwasher, fridge ice-maker and... |
| 55 | 13 | `/hardwood-floor-cabinet-drying` | 5 | The water was sewage or outside floodwater. Sewage Backup... |
| 56 | 13 | `/hardwood-floor-cabinet-drying` | 8 | Shut off the water at the appliance or the main valve. |
| 57 | 13 | `/hardwood-floor-cabinet-drying` | 3 | One room of hardwood dried in place: about $1,500 to $3,000 |
| 59 | 14 | `/condo-apartment-water-damage` | 5 | Down through floors: from a bathroom, laundry or kitchen ... |
| 60 | 14 | `/condo-apartment-water-damage` | 4 | Photograph and list the tenant's damaged belongings separ... |
| 62 | 14 | `/condo-apartment-water-damage` | 5 | Bingham Junction and Jordan Bluffs: newer apartments, con... |
| 63 | 14 | `/condo-apartment-water-damage` | 3 | One unit, small leak caught early: about $1,500 to $3,500 |
| 66 | 15 | `/commercial-water-damage` | 7 | Restroom overflows from clogged toilets, failed flush val... |
| 68 | 15 | `/commercial-water-damage` | 5 | Evening: after closing, the crew extracts water, removes ... |
| 69 | 15 | `/commercial-water-damage` | 5 | What standard does your drying follow, such as IICRC S500? |
| 70 | 15 | `/commercial-water-damage` | 3 | Small office suite or shop, clean water: about $5,000 to ... |
| 71 | 15 | `/commercial-water-damage` | 6 | Know where the main water shut-off and sprinkler control ... |
| 73 | 16 | `/storm-flood-damage` | 6 | Don't walk through floodwater near outlets, appliances or... |
| 74 | 16 | `/storm-flood-damage` | 7 | Clear gutters, downspouts and the storm drain inlet in fr... |
| 75 | 16 | `/storm-flood-damage` | 6 | The water line on walls, furniture and appliances. |
| 76 | 16 | `/storm-flood-damage` | 3 | Garage or one room with shallow floodwater: about $3,000 ... |
| 79 | 17 | `/mold-remediation` | 5 | A leak was found days or weeks after it started. |
| 81 | 17 | `/mold-remediation` | 5 | Babies and young children. |
| 82 | 17 | `/mold-remediation` | 3 | Small area, such as under one sink or a short wall sectio... |
| 84 | 18 | `/water-leak-detection` | 8 | Your water bill jumps with no change in use. |
| 86 | 18 | `/water-leak-detection` | 7 | Shower and tub walls: failed valve cartridges, cracked sh... |
| 88 | 18 | `/water-leak-detection` | 5 | A floor plan or photos marked with wet areas. |
| 90 | 18 | `/water-leak-detection` | 5 | You know there's a leak but not where it is. |
| 91 | 18 | `/water-leak-detection` | 4 | Fall: check outside faucets and the swamp cooler line bef... |
| 92 | 18 | `/water-leak-detection` | 3 | Leak detection and moisture mapping for one area or room:... |
| 94 | 19 | `/water-damage-repair` | 4 | Insulation is replaced in exterior walls before drywall g... |
| 95 | 19 | `/water-damage-repair` | 5 | Wall finishes: drywall replaces soaked sections; paneling... |
| 96 | 19 | `/water-damage-repair` | 3 | Condos and townhomes: each unit gets its own scope, so th... |
| 97 | 19 | `/water-damage-repair` | 6 | Vinyl plank or tile instead of carpet in basements and la... |
| 98 | 19 | `/water-damage-repair` | 3 | One room, bottom of drywall, baseboards and paint: about ... |
| 100 | 20 | `/locations/cottonwood-heights-ut` | 5 | Rim joists and cantilevered floors in split-levels. |
| 101 | 20 | `/locations/cottonwood-heights-ut` | 16 | Emergency Water Extraction in Cottonwood Heights: standin... |
| 102 | 20 | `/locations/cottonwood-heights-ut` | 6 | Fort Union Blvd and the east bench. |
| 105 | 21 | `/locations/south-salt-lake-ut` | 16 | Emergency Water Extraction in South Salt Lake: standing w... |
| 106 | 21 | `/locations/south-salt-lake-ut` | 6 | The State Street corridor and the neighborhoods on either... |
| 107 | 21 | `/locations/south-salt-lake-ut` | 5 | Galvanized supply pipes that rust from the inside and lea... |
| 110 | 22 | `/locations/magna-ut` | 5 | Water heater failures in basement utility rooms, often ol... |
| 112 | 22 | `/locations/magna-ut` | 16 | Emergency Water Extraction in Magna: standing water remov... |
| 113 | 22 | `/locations/magna-ut` | 5 | Historic Main Street and the older town center. |
| 117 | 23 | `/midvale-water-sewer-emergency-contacts` | 4 | Water bubbling up from the street, sidewalk or park strip. |
| 119 | 23 | `/midvale-water-sewer-emergency-contacts` | 5 | Sewage has come into your home through any drain. |
| 120 | 24 | `/privacy-policy` | 6 | Respond to your request and contact you about it. |
| 121 | 24 | `/privacy-policy` | 3 | With companies that help run this website and its tools, ... |
| 122 | 24 | `/privacy-policy` | 3 | You can choose not to submit forms or share information. |
| 123 | 25 | `/terms-of-use` | 5 | Use the site in any way that breaks a law or regulation. |
| 124 | 27 | `/resources/frozen-pipes-midvale` | 7 | Rim joists: the band of framing where the floor sits on t... |
| 125 | 27 | `/resources/frozen-pipes-midvale` | 8 | Disconnect and drain garden hoses. |
| 126 | 27 | `/resources/frozen-pipes-midvale` | 5 | Keep the thermostat steady day and night, at least in the... |
| 127 | 27 | `/resources/frozen-pipes-midvale` | 4 | Little or no water comes out of a faucet when you turn it... |
| 130 | 28 | `/resources/winterize-swamp-cooler-utah` | 5 | Cracked water lines leak onto the roof deck every time th... |
| 133 | 28 | `/resources/winterize-swamp-cooler-utah` | 8 | Remove the cooler cover. |
| 134 | 28 | `/resources/winterize-swamp-cooler-utah` | 4 | Blown-in insulation soaks up water, packs down and gets h... |
| 136 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 2 | Dwelling or "walls-in" coverage for interior finishes the... |
| 137 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 5 | Separate photos for each unit, labeled with the unit number. |
| 138 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 7 | Washer hoses and drains in upstairs laundry closets. |
| 141 | 30 | `/resources/can-mold-grow-in-utah` | 5 | Moisture meters and thermal imaging find water you can't ... |
| 142 | 30 | `/resources/can-mold-grow-in-utah` | 6 | Finished basements: paneling and drywall over cold concre... |
| 146 | 30 | `/resources/can-mold-grow-in-utah` | 7 | Under the kitchen and bathroom sinks. |
| 147 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 6 | The floor-wall joint: the seam where the slab meets the f... |
| 148 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 7 | Move furniture, boxes, electronics and rugs off the floor. |
| 149 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 5 | Lower ground on the west side, closer to the Jordan River... |
| 150 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 5 | Clear leaves and debris from gutters, downspouts and wind... |
| 151 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 4 | Walk the basement every few days, especially along outsid... |
| 152 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 2 | Small area of seepage caught early: about $1,500 to $3,500 |

## 3. Groups left UNCLASSIFIED (still flat `{type:'p'}`)

| # | Tab | Route | Items | Exact reason |
|---:|---|---|---:|---|---|
| 3 | 1 | `/` | 5 | item 2 ambiguous match: 2 export lines (line 89 (ul), line 2624 (ul)) match 'Basement flooding cleanup: about $2,500 to $9,000' |
| 4 | 1 | `/` | 6 | item 6 ambiguous match: 4 export lines (line 103 (ul), line 543 (ul), line 2330 (ul), line 2587 (ul)) match 'Call (385) 337-3560 so a crew is dispatched while you work.' |
| 21 | 6 | `/window-well-flooding` | 7 | item 7 ambiguous match: 4 export lines (line 103 (ul), line 543 (ul), line 2330 (ul), line 2587 (ul)) match 'Call (385) 337-3560 so a crew is dispatched while you work.' |
| 38 | 9 | `/water-heater-leak-cleanup` | 7 | item 3 ambiguous match: 3 export lines (line 966 (ul), line 1566 (ul), line 3125 (ul)) match 'Replace rubber washer hoses with braided stainless hoses.' |
| 39 | 10 | `/swamp-cooler-leak-water-damage` | 6 | item 4 ambiguous match: 2 export lines (line 1030 (ul), line 2989 (ul)) match 'Water dripping from the vent grille.' |
| 42 | 11 | `/ceiling-water-damage` | 7 | item 7 ambiguous match: 2 export lines (line 1133 (ol), line 2481 (ul)) match 'Call (385) 337-3560 so a crew is dispatched.' |
| 64 | 14 | `/condo-apartment-water-damage` | 6 | item 1 ambiguous match: 3 export lines (line 966 (ul), line 1566 (ul), line 3125 (ul)) match 'Replace rubber washer hoses with braided stainless hoses.' |
| 72 | 16 | `/storm-flood-damage` | 8 | item 8 ambiguous match: 2 export lines (line 1781 (ol), line 2063 (ol)) match 'Rebuild. Water Damage Repair (/water-damage-repair/)' |
| 77 | 17 | `/mold-remediation` | 6 | item 6 ambiguous match: 2 export lines (line 1880 (ul), line 3220 (ul)) match 'Allergy-like symptoms that ease when you leave the house.' |
| 80 | 17 | `/mold-remediation` | 5 | item 2 ambiguous match: 2 export lines (line 1919 (ul), line 3228 (ul)) match 'Will you set up containment and negative air?' |
| 83 | 17 | `/mold-remediation` | 6 | item 5 ambiguous match: 2 export lines (line 1960 (ul), line 3238 (ol)) match 'Vent bathroom fans outside, not into the attic.' |
| 89 | 18 | `/water-leak-detection` | 5 | item 5 ambiguous match: 2 export lines (line 1781 (ol), line 2063 (ol)) match 'Rebuild. Water Damage Repair (/water-damage-repair/)' |
| 103 | 20 | `/locations/cottonwood-heights-ut` | 7 | item 2 ambiguous match: 3 export lines (line 2325 (ul), line 2476 (ul), line 2582 (ul)) match 'Turn off power to wet rooms if the panel is safe to reach.' |
| 104 | 20 | `/locations/cottonwood-heights-ut` | 4 | item 1 ambiguous match: 2 export lines (line 2335 (ul), line 2623 (ul)) match 'One room, clean water: about $1,000 to $4,500' |
| 108 | 21 | `/locations/south-salt-lake-ut` | 4 | item 2 ambiguous match: 2 export lines (line 91 (ul), line 2470 (ul)) match 'Sewage backup cleanup: about $3,000 to $12,000' |
| 109 | 21 | `/locations/south-salt-lake-ut` | 7 | item 2 ambiguous match: 3 export lines (line 2325 (ul), line 2476 (ul), line 2582 (ul)) match 'Turn off power to wet rooms if the panel is safe to reach.' |
| 114 | 22 | `/locations/magna-ut` | 7 | item 2 ambiguous match: 3 export lines (line 2325 (ul), line 2476 (ul), line 2582 (ul)) match 'Turn off power to wet rooms if the panel is safe to reach.' |
| 115 | 22 | `/locations/magna-ut` | 4 | item 1 ambiguous match: 2 export lines (line 2335 (ul), line 2623 (ul)) match 'One room, clean water: about $1,000 to $4,500' |
| 132 | 28 | `/resources/winterize-swamp-cooler-utah` | 7 | item 3 ambiguous match: 2 export lines (line 1030 (ul), line 2989 (ul)) match 'Water dripping from the vent grille.' |
| 139 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 7 | item 4 ambiguous match: 3 export lines (line 966 (ul), line 1566 (ul), line 3125 (ul)) match 'Replace rubber washer hoses with braided stainless hoses.' |
| 143 | 30 | `/resources/can-mold-grow-in-utah` | 5 | item 5 ambiguous match: 2 export lines (line 1880 (ul), line 3220 (ul)) match 'Allergy-like symptoms that ease when you leave the house.' |
| 144 | 30 | `/resources/can-mold-grow-in-utah` | 5 | item 3 ambiguous match: 2 export lines (line 1919 (ul), line 3228 (ul)) match 'Will you set up containment and negative air?' |
| 145 | 30 | `/resources/can-mold-grow-in-utah` | 8 | item 7 ambiguous match: 2 export lines (line 1960 (ul), line 3238 (ol)) match 'Vent bathroom fans outside, not into the attic.' |

## 4. Already classified by a previous run (left untouched)

| # | Tab | Route | Items | Kind |
|---:|---|---|---:|---|---|
| 1 | 1 | `/` | 6 | ul |
| 2 | 1 | `/` | 6 | ol |
| 5 | 1 | `/` | 3 | ul |
| 6 | 2 | `/about` | 8 | ul |
| 7 | 2 | `/about` | 7 | ol |
| 8 | 2 | `/about` | 5 | ul |
| 9 | 2 | `/about` | 16 | ul |
| 10 | 3 | `/contact` | 7 | ul |
| 11 | 3 | `/contact` | 6 | ul |
| 12 | 3 | `/contact` | 3 | ul |
| 13 | 4 | `/emergency-water-extraction` | 4 | ol |
| 14 | 4 | `/emergency-water-extraction` | 3 | ul |
| 15 | 4 | `/emergency-water-extraction` | 3 | ul |
| 16 | 4 | `/emergency-water-extraction` | 4 | ul |
| 17 | 4 | `/emergency-water-extraction` | 4 | ul |
| 18 | 5 | `/basement-flooding-cleanup` | 7 | ol |
| 19 | 5 | `/basement-flooding-cleanup` | 3 | ul |
| 20 | 5 | `/basement-flooding-cleanup` | 7 | ul |
| 22 | 6 | `/window-well-flooding` | 8 | ol |
| 23 | 6 | `/window-well-flooding` | 3 | ul |
| 24 | 7 | `/burst-pipe-water-damage` | 4 | ul |
| 25 | 7 | `/burst-pipe-water-damage` | 6 | ul |
| 26 | 7 | `/burst-pipe-water-damage` | 7 | ol |
| 27 | 7 | `/burst-pipe-water-damage` | 4 | ul |
| 28 | 7 | `/burst-pipe-water-damage` | 3 | ul |
| 29 | 7 | `/burst-pipe-water-damage` | 8 | ul |
| 30 | 8 | `/sewage-backup-cleanup` | 7 | ol |
| 31 | 8 | `/sewage-backup-cleanup` | 8 | ol |
| 32 | 8 | `/sewage-backup-cleanup` | 3 | ul |
| 33 | 9 | `/water-heater-leak-cleanup` | 6 | ol |
| 34 | 9 | `/water-heater-leak-cleanup` | 7 | ol |
| 35 | 9 | `/water-heater-leak-cleanup` | 4 | ul |
| 36 | 9 | `/water-heater-leak-cleanup` | 6 | ul |
| 37 | 9 | `/water-heater-leak-cleanup` | 3 | ul |
| 40 | 10 | `/swamp-cooler-leak-water-damage` | 7 | ol |
| 41 | 10 | `/swamp-cooler-leak-water-damage` | 3 | ul |
| 43 | 11 | `/ceiling-water-damage` | 7 | ol |
| 44 | 11 | `/ceiling-water-damage` | 6 | ul |
| 45 | 11 | `/ceiling-water-damage` | 3 | ul |
| 46 | 12 | `/crawl-space-water-damage` | 6 | ul |
| 47 | 12 | `/crawl-space-water-damage` | 7 | ol |
| 48 | 12 | `/crawl-space-water-damage` | 4 | ul |
| 49 | 12 | `/crawl-space-water-damage` | 5 | ul |
| 50 | 12 | `/crawl-space-water-damage` | 7 | ul |
| 51 | 12 | `/crawl-space-water-damage` | 3 | ul |
| 52 | 13 | `/hardwood-floor-cabinet-drying` | 6 | ol |
| 53 | 13 | `/hardwood-floor-cabinet-drying` | 5 | ol |
| 54 | 13 | `/hardwood-floor-cabinet-drying` | 4 | ul |
| 55 | 13 | `/hardwood-floor-cabinet-drying` | 5 | ul |
| 56 | 13 | `/hardwood-floor-cabinet-drying` | 8 | ul |
| 57 | 13 | `/hardwood-floor-cabinet-drying` | 3 | ul |
| 58 | 14 | `/condo-apartment-water-damage` | 7 | ol |
| 59 | 14 | `/condo-apartment-water-damage` | 5 | ul |
| 60 | 14 | `/condo-apartment-water-damage` | 4 | ul |
| 61 | 14 | `/condo-apartment-water-damage` | 7 | ol |
| 62 | 14 | `/condo-apartment-water-damage` | 5 | ul |
| 63 | 14 | `/condo-apartment-water-damage` | 3 | ul |
| 65 | 15 | `/commercial-water-damage` | 6 | ol |
| 66 | 15 | `/commercial-water-damage` | 7 | ul |
| 67 | 15 | `/commercial-water-damage` | 9 | ol |
| 68 | 15 | `/commercial-water-damage` | 5 | ul |
| 69 | 15 | `/commercial-water-damage` | 5 | ul |
| 70 | 15 | `/commercial-water-damage` | 3 | ul |
| 71 | 15 | `/commercial-water-damage` | 6 | ul |
| 73 | 16 | `/storm-flood-damage` | 6 | ul |
| 74 | 16 | `/storm-flood-damage` | 7 | ul |
| 75 | 16 | `/storm-flood-damage` | 6 | ul |
| 76 | 16 | `/storm-flood-damage` | 3 | ul |
| 78 | 17 | `/mold-remediation` | 8 | ol |
| 79 | 17 | `/mold-remediation` | 5 | ul |
| 81 | 17 | `/mold-remediation` | 5 | ul |
| 82 | 17 | `/mold-remediation` | 3 | ul |
| 84 | 18 | `/water-leak-detection` | 8 | ul |
| 85 | 18 | `/water-leak-detection` | 5 | ol |
| 86 | 18 | `/water-leak-detection` | 7 | ul |
| 87 | 18 | `/water-leak-detection` | 5 | ol |
| 88 | 18 | `/water-leak-detection` | 5 | ul |
| 90 | 18 | `/water-leak-detection` | 5 | ul |
| 91 | 18 | `/water-leak-detection` | 4 | ul |
| 92 | 18 | `/water-leak-detection` | 3 | ul |
| 93 | 19 | `/water-damage-repair` | 5 | ol |
| 94 | 19 | `/water-damage-repair` | 4 | ul |
| 95 | 19 | `/water-damage-repair` | 5 | ul |
| 96 | 19 | `/water-damage-repair` | 3 | ul |
| 97 | 19 | `/water-damage-repair` | 6 | ul |
| 98 | 19 | `/water-damage-repair` | 3 | ul |
| 99 | 20 | `/locations/cottonwood-heights-ut` | 6 | ol |
| 100 | 20 | `/locations/cottonwood-heights-ut` | 5 | ul |
| 101 | 20 | `/locations/cottonwood-heights-ut` | 16 | ul |
| 102 | 20 | `/locations/cottonwood-heights-ut` | 6 | ul |
| 105 | 21 | `/locations/south-salt-lake-ut` | 16 | ul |
| 106 | 21 | `/locations/south-salt-lake-ut` | 6 | ul |
| 107 | 21 | `/locations/south-salt-lake-ut` | 5 | ul |
| 110 | 22 | `/locations/magna-ut` | 5 | ul |
| 111 | 22 | `/locations/magna-ut` | 5 | ol |
| 112 | 22 | `/locations/magna-ut` | 16 | ul |
| 113 | 22 | `/locations/magna-ut` | 5 | ul |
| 116 | 23 | `/midvale-water-sewer-emergency-contacts` | 5 | ol |
| 117 | 23 | `/midvale-water-sewer-emergency-contacts` | 4 | ul |
| 118 | 23 | `/midvale-water-sewer-emergency-contacts` | 4 | ol |
| 119 | 23 | `/midvale-water-sewer-emergency-contacts` | 5 | ul |
| 120 | 24 | `/privacy-policy` | 6 | ul |
| 121 | 24 | `/privacy-policy` | 3 | ul |
| 122 | 24 | `/privacy-policy` | 3 | ul |
| 123 | 25 | `/terms-of-use` | 5 | ul |
| 124 | 27 | `/resources/frozen-pipes-midvale` | 7 | ul |
| 125 | 27 | `/resources/frozen-pipes-midvale` | 8 | ul |
| 126 | 27 | `/resources/frozen-pipes-midvale` | 5 | ul |
| 127 | 27 | `/resources/frozen-pipes-midvale` | 4 | ul |
| 128 | 27 | `/resources/frozen-pipes-midvale` | 6 | ol |
| 129 | 27 | `/resources/frozen-pipes-midvale` | 7 | ol |
| 130 | 28 | `/resources/winterize-swamp-cooler-utah` | 5 | ul |
| 131 | 28 | `/resources/winterize-swamp-cooler-utah` | 10 | ol |
| 133 | 28 | `/resources/winterize-swamp-cooler-utah` | 8 | ul |
| 134 | 28 | `/resources/winterize-swamp-cooler-utah` | 4 | ul |
| 135 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 6 | ol |
| 136 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 2 | ul |
| 137 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 5 | ul |
| 138 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 7 | ul |
| 140 | 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 5 | ol |
| 141 | 30 | `/resources/can-mold-grow-in-utah` | 5 | ul |
| 142 | 30 | `/resources/can-mold-grow-in-utah` | 6 | ul |
| 146 | 30 | `/resources/can-mold-grow-in-utah` | 7 | ul |
| 147 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 6 | ul |
| 148 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 7 | ul |
| 149 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 5 | ul |
| 150 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 5 | ul |
| 151 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 4 | ul |
| 152 | 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 2 | ul |

## 5. Word-count proof — before vs after (must be IDENTICAL)

`before` = stored `counts.words` per tab before the patch. `after` = stored `counts.words` after the patch (never edited by this script). `recomputed` = words counted fresh from the patched JSON by the parser's own counting rule (eyebrow + h1 + intro + raw trust line incl. its `·` separators + all block words incl. tables and FAQ).

| Tab | Route | Before | After (stored) | Recomputed | Check |
|---:|---|---:|---:|---:|---|
| 1 | `/` | 2107 | 2107 | 2107 | ✓ |
| 2 | `/about` | 929 | 929 | 929 | ✓ |
| 3 | `/contact` | 679 | 679 | 679 | ✓ |
| 4 | `/emergency-water-extraction` | 1762 | 1762 | 1762 | ✓ |
| 5 | `/basement-flooding-cleanup` | 1662 | 1662 | 1662 | ✓ |
| 6 | `/window-well-flooding` | 1744 | 1744 | 1744 | ✓ |
| 7 | `/burst-pipe-water-damage` | 1825 | 1825 | 1825 | ✓ |
| 8 | `/sewage-backup-cleanup` | 1699 | 1699 | 1699 | ✓ |
| 9 | `/water-heater-leak-cleanup` | 1678 | 1678 | 1678 | ✓ |
| 10 | `/swamp-cooler-leak-water-damage` | 1611 | 1611 | 1611 | ✓ |
| 11 | `/ceiling-water-damage` | 1601 | 1601 | 1601 | ✓ |
| 12 | `/crawl-space-water-damage` | 1617 | 1617 | 1617 | ✓ |
| 13 | `/hardwood-floor-cabinet-drying` | 1742 | 1742 | 1742 | ✓ |
| 14 | `/condo-apartment-water-damage` | 1708 | 1708 | 1708 | ✓ |
| 15 | `/commercial-water-damage` | 1651 | 1651 | 1651 | ✓ |
| 16 | `/storm-flood-damage` | 1609 | 1609 | 1609 | ✓ |
| 17 | `/mold-remediation` | 1673 | 1673 | 1673 | ✓ |
| 18 | `/water-leak-detection` | 1721 | 1721 | 1721 | ✓ |
| 19 | `/water-damage-repair` | 1516 | 1516 | 1516 | ✓ |
| 20 | `/locations/cottonwood-heights-ut` | 1729 | 1729 | 1729 | ✓ |
| 21 | `/locations/south-salt-lake-ut` | 1811 | 1811 | 1811 | ✓ |
| 22 | `/locations/magna-ut` | 1791 | 1791 | 1791 | ✓ |
| 23 | `/midvale-water-sewer-emergency-contacts` | 1236 | 1236 | 1236 | ✓ |
| 24 | `/privacy-policy` | 505 | 505 | 505 | ✓ |
| 25 | `/terms-of-use` | 450 | 450 | 450 | ✓ |
| 26 | `/disclaimer` | 291 | 291 | 291 | ✓ |
| 27 | `/resources/frozen-pipes-midvale` | 1633 | 1633 | 1633 | ✓ |
| 28 | `/resources/winterize-swamp-cooler-utah` | 1488 | 1488 | 1488 | ✓ |
| 29 | `/resources/upstairs-unit-leak-who-pays-utah` | 1490 | 1490 | 1490 | ✓ |
| 30 | `/resources/can-mold-grow-in-utah` | 1428 | 1428 | 1428 | ✓ |
| 31 | `/resources/basement-flooding-spring-snowmelt-utah` | 1446 | 1446 | 1446 | ✓ |
| **Total** | | **45832** | **45832** | **45832** | ✓ |

Total words before = total words after = **45832** (per-tab `counts.words` unchanged, and the fresh recomputation from the patched file agrees on every tab).

## 6. Block-type counts before vs after

| Block type | Before | After | Change |
|---|---:|---:|---|
| `p` | 862 | 862 | 0 |
| `ul` | 97 | 97 | 0 |
| `ol` | 32 | 32 | 0 |
| `h2` | 406 | 406 | 0 |
| `h3` | 259 | 259 | 0 |
| `table` | 43 | 43 | 0 |

No blocks changed on this run (all classified groups were already converted by a previous run); h2/h3/table counts are unchanged.

## 7. No-other-field check

Check run inside the script before writing the file: both the patched JSON and the file as read were normalised by expanding every `ul`/`ol` block back into its original `{type:'p'}` blocks (same segments, same order) and the two normalised forms were compared. Result: **identical** — no field outside the classified groups' blocks changed (meta, h1, intro, eyebrow, trustChips, hasButtonsLine, faqs, counts, routes, urls and every non-list block are byte-for-byte the same content). In addition, each patched block was asserted to hold exactly its group's original item texts, and the stored `counts.words` values were asserted unchanged.

## 8. Notes

- **Export census reconciles exactly.** 866 glyph lines = 862 list items + 4 extra numbered lines. The 4 extras are the tab-5 H3 headings under “Four Ways Midvale Basements Flood” (“Groundwater Seepage”, “Window Wells and Surface Runoff”, “Plumbing and Appliance Failures”, “Sewer Backups”, export lines 434–440), which the export renders as `1.`–`4.` but which the parser correctly emitted as `h3` blocks, not list items. Their stripped texts match no group item, so they cannot misclassify anything.
- **Zero items had no exact export match.** Every one of the 862 item texts matched at least one glyph line exactly — the export is fully matchable; nothing was left flat for lack of a match.
- **Why 23 groups are unclassified: two different causes.** 4 groups are genuinely mixed-kind — the same sentence is a numbered step in one tab and a bulleted item in another, so a per-item lookup cannot prove that group's glyph (e.g. “Call (385) 337-3560 so a crew is dispatched.” is `7.` in tab 11's process list but `*` in tab 21's checklist; “Vent bathroom fans outside, not into the attic.” is `*` in tab 17 but `8.` in tab 30). The other 19 are ambiguous only because the same item text recurs elsewhere in the doc and every matching export line carries the SAME glyph kind (e.g. “Call (385) 337-3560 so a crew is dispatched while you work.” matches 4 bulleted lines; “Basement flooding cleanup: about $2,500 to $9,000” matches 2 bulleted lines). Under the rule as written — two export lines matching the same item text disqualifies the group — all 19 stay flat. If the rule were relaxed to “ambiguous only when the matching lines disagree on kind”, 19 of the 23 would classify (114 ul + 34 ol, 4 unclassified) with no other change; that relaxation was NOT applied — it needs an explicit order.
- **Re-runnable:** a second run recognises the converted `ul`/`ol` blocks, leaves them untouched, and reports them as already classified; exit 0, file unchanged.

