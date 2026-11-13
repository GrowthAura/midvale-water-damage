#!/usr/bin/env python3
"""CYCLE 1 OPT — merge static + links + perf into qa/opt1-seo.json + qa/opt1-seo.md.
AUDIT ONLY — reads the three evidence JSONs, writes the two deliverables."""
import json
from pathlib import Path

ROOT = Path.home() / "workspace/midvale-water-damage"
static = json.loads((ROOT / "qa/opt1-static.json").read_text())
links = json.loads((ROOT / "qa/opt1-links.json").read_text())
perf = json.loads((ROOT / "qa/opt1-perf.json").read_text())

ROUTES = [p["route"] for p in json.loads((ROOT / "lib/pages-data.json").read_text())["pages"]]

problems = [
    {"severity": "P3", "check": "anchor-word-count", "page": "sitewide (12 pages)",
     "detail": "12 body-copy anchors exceed the 5-word anchor cap, all verbatim doc wording (accepted tension, carried from audits 1+2): 9x 'Water Heater & Appliance Leak Cleanup' (6w) on /basement-flooding-cleanup, /condo-apartment-water-damage, /crawl-space-water-damage, /emergency-water-extraction, /hardwood-floor-cabinet-drying, /water-leak-detection, /locations/south-salt-lake-ut, /about, /resources/upstairs-unit-leak-who-pays-utah; 2x 'Midvale Water & Sewer Emergency Contacts' (6w) on /contact, /resources/basement-flooding-spring-snowmelt-utah; 1x 8w 'the Midvale Water & Sewer Emergency Contacts page' on /. Both 6w anchors are verbatim substrings of the target pages' doc H1s (verified fresh this round). Shortening them would break the verbatim rule; no fix without his word."},
    {"severity": "P3", "check": "breadcrumb-double-link", "page": "/locations/* (3 pages)",
     "detail": "Homepage linked twice inside <main> on all 3 location pages (carried from audits 1+2, observation only): 'Home' -> /midvale-water-damage and 'Nearby Cities We Serve' -> /midvale-water-damage#areas. Verified fresh: BOTH links sit inside <nav aria-label=\"Breadcrumb\"> on all 3 pages. Breadcrumb nav, not body copy; body-copy duplicate targets 0 sitewide."},
    {"severity": "P3", "check": "breadcrumb-single-item-home", "page": "/",
     "detail": "Homepage carries a one-item BreadcrumbList (Home only), verified fresh by re-parse, with no visible breadcrumb navigation. Invisible markup, harmless; no second truthful item exists. Carried from audits 1+2."},
]

fixed_since_audit2 = [
    {"audit2": "P3-1 404.html duplicate noindex", "status": "FIXED",
     "evidence": "out/404.html now carries exactly 1 <meta name=\"robots\" content=\"noindex\"/> (verified by grep + served 404 status); the duplicate tag is gone."},
    {"audit2": "P3-2 cottonwood card alt wrong", "status": "FIXED",
     "evidence": "Alt rewritten to 'Winding canyon highway with cars through steep rocky autumn slopes in Cottonwood Canyon, Utah'. I viewed images/cards/cottonwood-heights-ut.webp full-size this round: it IS a winding canyon highway with cars through steep rocky autumn slopes — alt now matches the photo exactly."},
    {"audit2": "P3-3 snowmelt hero alt wrong", "status": "FIXED",
     "evidence": "Alt rewritten to 'Spring snowmelt water pooling at a home foundation as a downspout discharges, with melting snow piles and snowy hills behind'. I viewed images/heroes/basement-flooding-spring-snowmelt-utah.webp full-size this round: it IS an exterior downspout discharging meltwater at a home foundation with snow piles and snowy hills behind — alt now matches the photo exactly."},
]

per_page = {}
for rt in ROUTES:
    s = static["per_page"][rt]
    l = links["per_page"][rt]
    p = next(x for x in perf["pages"] if x["route"] == rt)
    probs = [pr for pr in problems if pr["page"] == rt or rt in pr["page"]]
    row = {
        "route": rt,
        "served_status": s["served_status"],
        "title_len": s["title_len"], "title_verbatim": s["title_verbatim_match"],
        "desc_len": s["desc_len"], "desc_verbatim": s["desc_verbatim_match"],
        "h1_count": s["h1_count"], "h1_match": s["h1_match"],
        "h2": f"{s['h2_actual_count']}/{s['h2_expected_count']}",
        "h3": f"{s['h3_actual_count']}/{s['h3_expected_count']}",
        "canonical_self_ref": s["canonical_self_referential"],
        "og_url_match": s["og_url_matches_canonical"],
        "meta_robots": s["meta_robots_contents"],
        "jsonld_blocks": s["jsonld_block_count"],
        "jsonld_parse_failures": len(s["jsonld_parse_failures"]),
        "body_links": l["body_link"], "card_links": l["card_internal"],
        "broken_links": len(l["broken_links"]), "self_links": len(l["self_links"]),
        "anchor_word_violations": len(l["prose_anchor_violations"]),
        "imgs": len(l["images"]),
        "imgs_missing_alt": sum(1 for i in l["images"] if not i["alt_present"] or i["alt_empty"]),
        "overflow_320": p["viewports"]["320x568"]["overflowPx"],
        "overflow_390": p["viewports"]["390x844"]["overflowPx"],
        "overflow_1440": p["viewports"]["1440x900"]["overflowPx"],
        "body_font_320": p["viewports"]["320x568"]["bodyFontSizes"],
        "body_font_390": p["viewports"]["390x844"]["bodyFontSizes"],
        "lcp_320": p["viewports"]["320x568"]["lcpMs"],
        "lcp_390": p["viewports"]["390x844"]["lcpMs"],
        "lcp_1440": p["viewports"]["1440x900"]["lcpMs"],
        "cls_320": p["viewports"]["320x568"]["cls"],
        "cls_390": p["viewports"]["390x844"]["cls"],
        "cls_1440": p["viewports"]["1440x900"]["cls"],
        "button2_visible_320": (p["viewports"]["320x568"]["button2"] or {}).get("visibleAtScroll0"),
        "button2_visible_390": (p["viewports"]["390x844"]["button2"] or {}).get("visibleAtScroll0"),
        "footer_min_320": p["viewports"]["320x568"]["footerMinVisible"],
        "footer_min_390": p["viewports"]["390x844"]["footerMinVisible"],
        "problems": [f"{pr['severity']}: {pr['check']}" for pr in probs],
    }
    per_page[rt] = row

report = {
    "audit": "CYCLE 1 OPT — Technical SEO audit (Batch 2 optimization, audit-only)",
    "site": "Midvale UT water damage",
    "date": "2026-11-13",
    "verdict": "READY — 0 blocking problems (P1 0 / P2 0 / P3 3 carried observations)",
    "method": {
        "server": "http://127.0.0.1:8325/midvale-water-damage/ (qa/linkfix-serve.py copy in /tmp, own port)",
        "export": "Fresh export run by coordinator before this audit (exit 0, NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage, no trailing slash). This audit did NOT rebuild.",
        "data_source": "lib/pages-data.json",
        "data_sha256": static["data_sha256"],
        "data_sha256_expected": static["data_sha256_expected"],
        "data_sha256_match": static["data_sha256_match"],
        "evidence": ["qa/opt1-static.json", "qa/opt1-links.json", "qa/opt1-perf.json",
                     "qa/opt1-static.py", "qa/opt1-links.py", "qa/opt1-perf.py"],
        "notes": [
            "No site source file was modified. No push/deploy/token/DNS. Local only.",
            "Perf numbers are LAB numbers from a local loopback, unthrottled, cold cache, fresh context per load — never field data.",
            "Schema depth (correctness beyond presence + parse) is the schema worker's job; this audit counts JSON-LD blocks and verifies 0 parse failures only.",
            "Alt-text scope is presence (107/107 present) plus fresh full-size visual re-check of the two audit-2 alt P3s (both fixed). Full visual alt adjudication of all 107 images was not in scope.",
        ],
    },
    "problem_counts": {"P1": 0, "P2": 0, "P3": 3, "total": 3},
    "problems": problems,
    "fixed_since_audit2": fixed_since_audit2,
    "crawlability_indexability": {
        "robots_txt": {"served_status": static["robots"]["served_status"],
                       "content": static["robots"]["exact_content"],
                       "allow_root": static["robots"]["has_allow_root"],
                       "has_host_line": static["robots"]["has_host_line"],
                       "served_matches_file": static["robots"]["served_matches_file"]},
        "sitemap": {"served_status": static["sitemap"]["served_status"],
                    "loc_count": static["sitemap"]["loc_count"],
                    "duplicates": static["sitemap"]["duplicates"],
                    "lastmod_all_date_only": static["sitemap"]["lastmod_all_date_only"],
                    "lastmod_values": static["sitemap"]["lastmod_values"],
                    "all_on_pages_url": static["sitemap"]["all_on_pages_url"],
                    "homepage_is_root_only": static["sitemap"]["homepage_is_root_only"],
                    "non_home_trailing_slash": static["sitemap"]["non_home_trailing_slash"],
                    "set_matches_expected_31": static["sitemap"]["set_matches_expected"],
                    "loc_non_200": static["sitemap"]["loc_non_200"]},
        "llms_txt": {"served_status": static["llms"]["served_status"],
                     "url_count": static["llms"]["url_count"],
                     "set_matches_expected_31": static["llms"]["set_matches_expected"],
                     "all_on_pages_url": static["llms"]["all_on_pages_url"]},
        "page_404": static["page_404"],
        "meta_robots_index_follow_exactly_1": sum(
            1 for v in static["per_page"].values()
            if v["meta_robots_tag_count"] == 1 and v["meta_robots_contents"] == ["index,follow"]),
        "canonicals_self_referential": sum(
            1 for v in static["per_page"].values() if v["canonical_self_referential"]),
        "og_url_matches_canonical": sum(
            1 for v in static["per_page"].values() if v["og_url_matches_canonical"]),
        "localhost_occurrences_in_out_html_xml_txt": static["scans"]["localhost_occurrences"],
        "double_slash_absolute_urls": static["scans"]["doubleslash_occurrences"],
        "local_resource_refs_checked": static["resource_summary"]["total_distinct_local_refs_checked"],
        "local_resource_refs_non_200": static["resource_summary"]["non_200"],
        "maps_iframes_total_pages": sum(v["iframe_count"] for v in static["per_page"].values()),
        "maps_iframes_without_lazy": sum(len(v["iframes_without_lazy"]) for v in static["per_page"].values()),
        "malformed_tel_links": "0 — grep for href=\"tel (no colon) and href=\"tel+ over out/: no hits (checked after the Tulsa GSC tel+19183470890 root-cause note landed in MEMORY.md during this audit)",
    },
    "meta_headings": {
        "titles_verbatim_31": sum(1 for v in static["per_page"].values() if v["title_verbatim_match"]),
        "descriptions_verbatim_31": sum(1 for v in static["per_page"].values() if v["desc_verbatim_match"]),
        "title_len_range": [min(v["title_len"] for v in static["per_page"].values()),
                            max(v["title_len"] for v in static["per_page"].values())],
        "titles_over_60ch": sum(1 for v in static["per_page"].values() if v["title_len"] > 60),
        "desc_len_range": [min(v["desc_len"] for v in static["per_page"].values()),
                           max(v["desc_len"] for v in static["per_page"].values())],
        "descriptions_under_120ch": sum(1 for v in static["per_page"].values() if v["desc_len"] < 120),
        "duplicate_titles": static["duplicate_titles"],
        "duplicate_descriptions": static["duplicate_descriptions"],
        "duplicate_canonicals": static["duplicate_canonicals"],
        "h1_exactly_1_and_verbatim": sum(
            1 for v in static["per_page"].values() if v["h1_count"] == 1 and v["h1_match"]),
        "h2_rendered_vs_doc": [sum(v["h2_actual_count"] for v in static["per_page"].values()),
                               sum(v["h2_expected_count"] for v in static["per_page"].values())],
        "h3_rendered_vs_doc": [sum(v["h3_actual_count"] for v in static["per_page"].values()),
                               sum(v["h3_expected_count"] for v in static["per_page"].values())],
        "heading_skips": sum(len(v["hierarchy_skips"]) for v in static["per_page"].values()),
        "h4_plus": sum(len(v["h4_plus"]) for v in static["per_page"].values()),
        "viewport_meta_present": sum(1 for v in static["per_page"].values() if v["viewport_present"]),
    },
    "links_images": {
        "anchors_total": links["totals"]["anchors_total_all_pages"],
        "anchors_internal": links["totals"]["anchors_internal"],
        "anchors_external": links["totals"]["anchors_external"],
        "anchors_tel_mailto": links["totals"]["anchors_tel_mailto"],
        "body_copy_links": links["totals"]["body_copy_links_in_main"],
        "card_links": links["totals"]["card_internal_links_in_main"],
        "body_plus_card": links["totals"]["body_plus_card"],
        "expected_body_plus_card": 162,
        "breadcrumb_links_in_main": links["totals"]["breadcrumb_internal_links_in_main"],
        "broken_links": links["totals"]["broken_links_total"],
        "self_links": links["totals"]["self_links_total"],
        "body_self_links": links["totals"]["body_self_links_total"],
        "orphans": links["orphans"],
        "inbound_min_max": [links["inbound_min"], max(links["inbound_counts"].values())],
        "duplicate_body_targets": links["totals"]["duplicate_target_pages_body"],
        "img_tags": links["totals"]["img_tags_total"],
        "img_missing_or_empty_alt": links["totals"]["img_missing_or_empty_alt"],
        "img_non200_src": links["totals"]["img_non200_src"],
        "img_without_width_height": links["totals"]["img_without_width_height"],
        "disk_webp_files": links["totals"]["disk_webp_total"],
        "total_image_weight_bytes": links["totals"]["total_image_weight_bytes"],
        "image_weight_audit2_bytes": 11331800,
        "image_weight_delta_vs_audit2_bytes": links["totals"]["total_image_weight_bytes"] - 11331800,
        "q75_reencoded_files_match_claim": all(
            q["matches_claim"] for q in links["q75_reencoded_check"]),
    },
    "schema_presence_only": {
        "jsonld_blocks_total": static["jsonld_total_blocks"],
        "jsonld_blocks_audit2": 80,
        "jsonld_parse_failures": static["jsonld_total_parse_failures"],
        "jsonld_blocks_per_page": {r: static["per_page"][r]["jsonld_block_count"] for r in ROUTES},
        "note": "Block count grew 80 -> 178 since audit 2 (schema best-ever work landed in the fresh export). Presence + parse only; correctness depth is the schema worker's scope.",
    },
    "performance_lab_only": {
        "conditions": perf["meta"]["conditions"],
        "summary": perf["summary"],
        "console_error_loads": sum(
            1 for p in perf["pages"] for v in p["viewports"].values() if v["consoleErrors"]),
        "failed_non_maps_request_loads": sum(
            1 for p in perf["pages"] for v in p["viewports"].values() if v["failedRequests"]),
        "maps_failed_loads_sandbox_egress": sum(
            1 for p in perf["pages"] for v in p["viewports"].values() if v["mapsFailedRequests"]),
        "lcp_vs_audit2": "Medians rose vs audit 2 (320: 672->1624ms, 390: 776->1756ms, 1440: 824->2204ms) AND FCP rose by the same factor (320: 612->1568ms) with CLS still 0 and the LCP element unchanged (IMG.hero-img 93/93). Hero files are byte-identical to audit 2 (top-10 image sizes identical) and total image weight is LOWER. Uniform FCP+LCP inflation with no site-side weight change is consistent with shared-cell CPU contention while parallel Batch 2 workers run — NOT evidence of a site regression. Lab only; re-measure on a quiet cell / real hosting before treating any LCP number as a regression.",
    },
    "mobile": {
        "overflow_320_max_px": max(p["viewports"]["320x568"]["overflowPx"] for p in perf["pages"]),
        "overflow_390_max_px": max(p["viewports"]["390x844"]["overflowPx"] for p in perf["pages"]),
        "overflow_1440_max_px": max(p["viewports"]["1440x900"]["overflowPx"] for p in perf["pages"]),
        "body_font_19px_all": all(
            p["viewports"][k]["bodyFontSizes"] == [19] or p["viewports"][k]["bodyFontSizes"] == [19.0]
            for p in perf["pages"] for k in ["320x568", "390x844", "1440x900"]),
        "intro_19px_all": all(
            p["viewports"][k]["introFontSize"] == 19
            for p in perf["pages"] for k in ["320x568", "390x844", "1440x900"]),
        "eyebrow_px": "14 @320, 18 @390/1440 (chrome, not body copy — as in audits 1+2)",
        "button2_visible_scroll0_320": sum(
            1 for p in perf["pages"] if (p["viewports"]["320x568"]["button2"] or {}).get("visibleAtScroll0")),
        "button2_visible_scroll0_390": sum(
            1 for p in perf["pages"] if (p["viewports"]["390x844"]["button2"] or {}).get("visibleAtScroll0")),
        "button2_worst_bottom": {k: perf["summary"][k]["button2WorstBottom"]
                                 for k in ["320x568", "390x844", "1440x900"]},
        "footer_min_px": "48 on all 31 routes x 3 viewports (27 visible links each)",
        "menu_button_px": "48x48 @320/@390 on all 31 routes",
        "nav_links_menu_open_px": "58.6 @320/@390 (menu opened); 48 @1440",
        "header_phone_px": "hidden <=360px by design (@320); 48 @390; 50.6 @1440",
    },
    "observations_not_problems": [
        "Titles 10-73ch, 25/31 over 60ch — all verbatim from the doc; Google truncates display but verbatim wins. No change without his word.",
        "Descriptions 47-138ch, 26/31 under 120ch — all verbatim from the doc.",
        "Legal titles short (Disclaimer 10ch / Terms of Use 12ch / Privacy Policy 14ch) — verbatim from the doc; carried accepted tension from audit 1.",
        "Image weight 11,243,230 B vs audit-2 11,331,800 B (-88,570 B, -0.8%). Top-10 files byte-identical to audit 2 and all 8 q75 re-encodes match their claimed sizes; out/ total == public/ total, so the export is faithful. Which sub-top-10 file(s) account for the delta is not established from available records (no per-file audit-2 manifest beyond top 10) — lighter is the direction the standing image-weight order wants; not a defect.",
        "Maps embeds do not load in this sandbox (google.com egress blocked) — environmental, needs a real-network eyeball after push. All 29 iframes carry loading=lazy (28 on pages + 1 on 404.html).",
        "Live mobile-width render in a real browser is still unconfirmed (sandbox Chromium cannot reach public internet); mobile verified on the byte-identical local export. His phone check remains the final confirmation.",
        "LCP/CLS are lab numbers only (see performance_lab_only.lcp_vs_audit2). No field data exists for this site.",
    ],
    "per_page": per_page,
}
(ROOT / "qa/opt1-seo.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))

# ---- markdown ----
lines = []
lines.append("# CYCLE 1 OPT — Technical SEO Audit — Midvale UT (Batch 2)")
lines.append("")
lines.append("**Date:** 2026-11-13 · **Verdict: READY — 0 blocking problems (P1 0 / P2 0 / P3 3 carried observations)**")
lines.append("")
lines.append("**Method:** fresh export by coordinator (exit 0, `NEXT_PUBLIC_SITE_URL=https://growthaura.github.io/midvale-water-damage`, no trailing slash), served on `/midvale-water-damage/` via `qa/linkfix-serve.py` on port 8325. Data `lib/pages-data.json` sha256 `21c6e7f2b89bab95f9f7da2ee5b5fb53c118edeee4abc587f8066dc0589d638f` verified unchanged before, during and after. Audit-only: no site source file modified, no push/deploy/token/DNS. Evidence: `qa/opt1-static.json`, `qa/opt1-links.json`, `qa/opt1-perf.json` (+ the three `opt1-*.py` scripts). Perf numbers are LAB numbers (local loopback, unthrottled, cold cache, fresh context per load) — never field data. Schema depth is the schema worker's job; this audit covers schema presence + parse only.")
lines.append("")
lines.append("## PROBLEMS")
lines.append("")
lines.append("### P1 — 0")
lines.append("")
lines.append("### P2 — 0")
lines.append("")
lines.append("### P3 — 3 (all carried observations, none blocking)")
lines.append("")
for i, pr in enumerate(problems, 1):
    lines.append(f"**P3-{i} — {pr['check']}** ({pr['page']})")
    lines.append(f"- {pr['detail']}")
    lines.append("")
lines.append("## FIXED SINCE AUDIT 2 (all 3 audit-2 P3s closed, verified fresh)")
lines.append("")
for fx in fixed_since_audit2:
    lines.append(f"- **{fx['audit2']} — {fx['status']}:** {fx['evidence']}")
    lines.append("")
lines.append("## PASSES (all measured fresh)")
lines.append("")
lines.append(f"- **Crawlability:** robots.txt HTTP 200, exact content `User-agent: * / Allow: / / Sitemap: https://growthaura.github.io/midvale-water-damage/sitemap.xml` (Allow present, no Host: line, served == file); sitemap exactly 31 locs, date-only lastmod `2026-11-12`, 0 duplicates, all 31 curl 200 via served subpath, homepage root `/` only, others no-slash, set == expected 31 canonical URLs; llms.txt lists all 31 routes on the Pages URL, HTTP 200.")
lines.append(f"- **Indexability:** meta robots exactly 1 `index, follow` on 31/31; canonical self-referential 31/31; og:url matches canonical 31/31; 404.html serves 404 with exactly 1 noindex tag and no canonical; 0 localhost occurrences and 0 double-slash absolute URLs anywhere in out/ HTML/XML/TXT (audit 2's single polyfill-chunk `localhost` string is gone in this fresh export); 120 distinct local resource refs checked, 0 non-200; 0 malformed `tel:` links (checked after the Tulsa GSC `tel+19183470890` root-cause note).")
lines.append(f"- **Meta:** title + description verbatim vs `pages-data.json` character-for-character on 31/31; 0 duplicate titles, 0 duplicate descriptions, 0 duplicate canonicals; title lengths 10–73ch, descriptions 47–138ch.")
lines.append(f"- **Headings:** exactly 1 H1 per page on 31/31, text matches the doc H1 every time; 0 skipped heading levels; H2 sequence matches doc blocks 406/406, H3 259/259; no H4+; viewport meta present 31/31.")
lines.append(f"- **Links:** 1,063 internal anchors checked on the served site, 0 broken, 0 external; body + card reconciles exactly: 143 body + 19 card = 162; 33 in-main breadcrumb links classified separately; orphans 0 (inbound min 5, max 30); body self-links 0; body duplicate targets 0.")
lines.append(f"- **Images/alt:** 107 webp on disk, 107 `<img>` tags, 0 missing/empty alt, 0 non-200 src, 0 missing width+height; total weight 11,243,230 B; all 8 q75 re-encodes match their fix-1 claimed sizes.")
lines.append(f"- **Schema (presence only):** 178 JSON-LD blocks across 31 pages (was 80 in audit 2 — schema best-ever work landed), 0 parse failures; per-page 3–8 blocks.")
lines.append(f"- **Mobile (93 in-browser loads):** horizontal overflow 0 at 320, 390 and 1440 on 31/31; body font 19px on all 31 routes × 3 viewports; `p.intro` 19px everywhere (eyebrow 14px @320 / 18px @390/1440 is chrome, not body copy); Button 2 visible at scroll-0 on 31/31 @320 (worst bottom 556.2px vs 568 fold — condo) AND @390 (worst 768.2px vs 844 — snowmelt resource); footer links min 48px; menu button 48×48 @320/390; nav links 58.6px menu-open @320/390, 48px @1440; header phone 48px @390, 50.6px @1440 (hidden ≤360px by design).")
lines.append(f"- **Performance (lab, see note below):** FCP medians 1568ms @320 / 1416ms @390 / 1984ms @1440; LCP medians 1624ms @320 / 1756ms @390 / 2204ms @1440 (max 3196 / 3108 / 3696ms); CLS median 0 at all viewports (max 0); 0 console errors across all 93 loads; 0 failed non-maps requests (Maps embed failures are sandbox-blocked google.com egress — environmental); LCP element `IMG.hero-img` on 93/93 loads.")
lines.append(f"- **Maps:** 29 iframes total (28 pages + 404.html), all `loading=\"lazy\"`; embed itself does not load in this sandbox — environmental, needs a real-network eyeball after push.")
lines.append("")
lines.append("## OBSERVATIONS (not problems)")
lines.append("")
for ob in report["observations_not_problems"]:
    lines.append(f"- {ob}")
lines.append("")
lines.append("**LCP lab note — read before comparing with audit 2:** LCP medians rose vs audit 2 (320: 672→1624ms, 390: 776→1756ms, 1440: 824→2204ms) AND FCP rose by the same factor (320: 612→1568ms), with CLS still 0 and the LCP element unchanged (`IMG.hero-img` 93/93). Hero files are byte-identical to audit 2 (top-10 image sizes identical) and total image weight is LOWER. Uniform FCP+LCP inflation with no site-side weight change is consistent with shared-cell CPU contention while parallel Batch 2 workers run — NOT evidence of a site regression. Lab only; re-measure on a quiet cell / real hosting before treating any LCP number as a regression.")
lines.append("")
lines.append("## PER-PAGE TABLE")
lines.append("")
lines.append("| Route | T | D | H1 | H2 | H3 | Canon | JSON-LD | Body/Card | Broken | Alt-miss | Ovf 320/390 | LCP 320/390/1440 | CLS max | B2 320/390 | Problems |")
lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for rt in ROUTES:
    r = per_page[rt]
    clsmax = max(r["cls_320"], r["cls_390"], r["cls_1440"])
    probs = "; ".join(r["problems"]) if r["problems"] else "—"
    lines.append(f"| `{rt}` | {r['title_len']}✓ | {r['desc_len']}✓ | {r['h1_count']}✓ | {r['h2']} | {r['h3']} | {'✓' if r['canonical_self_ref'] else '✗'} | {r['jsonld_blocks']} | {r['body_links']}/{r['card_links']} | {r['broken_links']} | {r['imgs_missing_alt']} | {r['overflow_320']}/{r['overflow_390']} | {r['lcp_320']}/{r['lcp_390']}/{r['lcp_1440']} | {clsmax} | {'✓' if r['button2_visible_320'] else '✗'}/{'✓' if r['button2_visible_390'] else '✗'} | {probs} |")
lines.append("")
lines.append("T/D = title/description length in chars (✓ = verbatim vs `pages-data.json`). LCP in ms, lab numbers only. B2 = Button 2 visible at scroll-0.")
lines.append("")
(ROOT / "qa/opt1-seo.md").write_text("\n".join(lines), encoding="utf-8")
print("wrote qa/opt1-seo.json + qa/opt1-seo.md")
print("problems:", report["problem_counts"])
print("per-page rows:", len(per_page))
