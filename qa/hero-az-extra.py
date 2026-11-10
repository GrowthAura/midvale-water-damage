"""Midvale HERO + A-to-Z extras: word-diff vs frozen doc, contamination sweeps,
image metadata (exiftool) + weights, sitemap/robots, dashes/fragments,
link resolution. Static checks on out/ + source. Writes qa/hero-az/findings-extra.json
"""
import json, os, re, html, subprocess
from html.parser import HTMLParser

BASE_DIR = "/home/hatch/workspace/midvale-water-damage"
OUT = os.path.join(BASE_DIR, "out")
QA = os.path.join(BASE_DIR, "qa", "hero-az")
os.makedirs(QA, exist_ok=True)
fails, notes = [], []

class TextExtract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.text = []
        self.head_text = []
        self.in_head = False
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "head":
            self.in_head = True
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag == "head":
            self.in_head = False
    def handle_data(self, data):
        if self.skip == 0:
            (self.head_text if self.in_head else self.text).append(data)

def norm(s):
    s = html.unescape(s)
    s = s.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,;:!?])", r"\1", s)
    return s

def check(cond, msg):
    if not cond:
        fails.append(msg)

# ---------- 1. word-diff: homepage visible text vs frozen-doc.txt ----------
frozen = open(os.path.join(BASE_DIR, "frozen-doc.txt")).read().splitlines()
home_html = open(os.path.join(OUT, "index.html")).read()
p = TextExtract(); p.feed(home_html)
visible = norm(" ".join(p.text))
head = " ".join(p.head_text)
missing, checked = [], 0
def content_tokens(line):
    # words that must exist on the page. Excludes annotations, not content:
    #   - URL slugs (route paths, live in href attrs, checked separately)
    #   - "|" table separators, "[" "]" button-label markers
    s = re.sub(r"\(/[^)]*\)", " ", line)
    s = re.sub(r"\(locations/[^)]*\)", " ", s)
    s = s.replace("|", " ").replace("[", " ").replace("]", " ")
    return [w.strip(".,;:!?()") for w in re.split(r"\s+", s) if w.strip(".,;:!?()")]

# page vocabulary: visible text + every href/alt (slugs live there)
page_vocab = norm(visible).lower()
page_vocab += " " + " ".join(re.findall(r'href="([^"]+)"', home_html)).lower()
page_vocab += " " + " ".join(re.findall(r'alt="([^"]+)"', home_html)).lower()

for line in frozen:
    line = line.strip()
    if not line:
        continue
    if line.startswith("Meta Title:"):
        checked += 1
        want = norm(line[len("Meta Title:"):])
        if want not in norm(head) and want not in home_html.replace("&amp;", "&"):
            missing.append("META-TITLE: " + line)
        continue
    if line.startswith("Meta Description:"):
        checked += 1
        want = norm(line[len("Meta Description:"):])
        # meta description is an ATTRIBUTE, not text — check raw HTML
        if want not in home_html.replace("&amp;", "&"):
            missing.append("META-DESC: " + line)
        continue
    if line.startswith("URL:"):
        checked += 1
        continue
    checked += 1
    absent = [w for w in content_tokens(line) if w.lower() not in page_vocab]
    if absent:
        missing.append(f"{line}  [absent words: {absent}]")
check(len(missing) == 0, f"word-diff missing {len(missing)}: {missing[:5]}")
print(f"word-diff: {checked} checked, {len(missing)} missing")

# ---------- 2. linked pages carry their verbatim summary in the hero ----------
import re as _re
SUMMARIES = {
    "emergency-water-extraction": "Truck-mounted and submersible pumps remove standing water fast",
    "basement-flooding-cleanup": "Finished basements in Midvale ramblers and split-levels hold water",
    "window-well-flooding": "When a window well fills with snowmelt or storm water",
    "burst-pipe-water-damage": "A split line inside a wall can soak insulation, drywall and floors",
    "sewage-backup-cleanup": "Sewage is Category 3 water.",
    "water-heater-leak-cleanup": "Hard water wears out tanks, valves and supply lines.",
    "swamp-cooler-leak-water-damage": "A stuck float valve or clogged drain pan can soak a roof deck",
    "ceiling-water-damage": "Upstairs bathrooms, ice dams and roof leaks show up as stains",
    "crawl-space-water-damage": "Older homes near Historic Main Street often sit over dirt crawl spaces.",
    "hardwood-floor-cabinet-drying": "Floor drying mats and cavity drying can save cupped hardwood",
    "condo-apartment-water-damage": "Water moves between stacked units fast.",
    "commercial-water-damage": "Offices, shops and restaurants along Fort Union Blvd",
    "storm-flood-damage": "Summer storms and runoff can push dirty water into garages",
    "mold-remediation": "If a leak sat too long, we contain the area",
    "water-leak-detection": "Thermal imaging and moisture meters find hidden water",
    "water-damage-repair": "Once everything is dry, we put drywall, texture, paint, flooring",
}
for slug, want in SUMMARIES.items():
    h = open(os.path.join(OUT, slug + ".html")).read()
    # visible BODY text only: <head> meta/og/twitter legitimately repeat the
    # summary (run-1 bug counted head occurrences and reported 5x)
    bp = TextExtract(); bp.feed(h)
    body_visible = norm(" ".join(bp.text))
    check(norm(want) in body_visible, f"{slug}: summary not in page body")
    n = body_visible.count(norm(want))
    check(n == 1, f"{slug}: summary appears {n}x in visible body (want exactly 1, hero only)")
print("linked-page summaries checked:", len(SUMMARIES))

# ---------- 3. contamination sweeps (old-theme traces) ----------
TERMS = ["Tulsa", "tulsa", "918", "tulsawaterdamage", "578-1166", "Edmond",
         "Plano", "plano", "Pleasant Grove", "pleasant-grove", "Lancaster",
         "Fort Myers", "McDonough", "Broken Arrow", "Owasso", "Naples",
         "waterdamagetulsa", "Tukwila"]
hits = []
# Scope: SHIPPED code only (app/, lib/, components/, public/). Working logs
# (PROGRESS.md, qa/, FINDINGS) legitimately name the theme provenance and
# are never shipped — run-1 swept them and false-flagged PROGRESS.md.
for sub in ("app", "lib", "components", "public"):
    for root, dirs, files in os.walk(os.path.join(BASE_DIR, sub)):
        if "node_modules" in root:
            continue
        for f in files:
            if f.endswith((".ts", ".tsx", ".css", ".json", ".svg", ".txt")):
                fp = os.path.join(root, f)
                try:
                    txt = open(fp, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for t in TERMS:
                    if t in txt:
                        hits.append(f"{fp.replace(BASE_DIR, '')}: {t!r}")
# out/ HTML sweep (built files must also be clean, excluding findings logs)
for root, dirs, files in os.walk(OUT):
    for f in files:
        if f.endswith((".html", ".xml", ".txt")):
            fp = os.path.join(root, f)
            txt = open(fp, encoding="utf-8", errors="ignore").read()
            for t in TERMS:
                if t in txt:
                    hits.append(f"out/{f}: {t!r}")
check(len(hits) == 0, f"contamination hits: {hits[:10]}")
print("contamination hits:", len(hits))

# ---------- 4. images: metadata + weights + filenames ----------
IMG_DIRS = [os.path.join(BASE_DIR, "public", "images", "heroes"),
            os.path.join(BASE_DIR, "public", "images", "cards")]
imgs = []
for d in IMG_DIRS:
    for f in sorted(os.listdir(d)):
        if f.endswith(".webp"):
            imgs.append(os.path.join(d, f))
check(len(imgs) == 40, f"image files {len(imgs)} != 40")
over = []
meta_problems = []
for fp in imgs:
    kb = os.path.getsize(fp) / 1024
    if kb > 200:
        over.append(f"{os.path.basename(fp)} {kb:.0f}KB")
    # "AI" as a standalone token only — run-1 used substring matching and
    # false-flagged "water-damage-repAIr.webp" (the word "repair" contains "ai")
    if "ai" in _re.split(r"[-_.]", os.path.basename(fp).lower()):
        meta_problems.append(f"AI in filename: {fp}")
    # exiftool: any EXIF/XMP/C2PA/generator tags?
    try:
        out = subprocess.run(["exiftool", "-a", "-G", "-s", fp],
                             capture_output=True, text=True, timeout=30).stdout
        bad = [l for l in out.splitlines()
               if any(k in l for k in ("EXIF:", "XMP:", "MakerNotes", "Software",
                                       "Creator", "Generator", "AI ", "JUMBF", "C2PA"))]
        if bad:
            meta_problems.append(f"{os.path.basename(fp)}: {bad[:3]}")
    except FileNotFoundError:
        notes.append("exiftool not installed — metadata check skipped")
        break
check(len(over) == 0, f"images over 200KB: {over}")
check(len(meta_problems) == 0, f"image metadata problems: {meta_problems[:5]}")
print(f"images: {len(imgs)}, over-200KB: {len(over)}, metadata problems: {len(meta_problems)}")

# ---------- 5. sitemap / robots ----------
sm = open(os.path.join(OUT, "sitemap.xml")).read()
locs = _re.findall(r"<loc>([^<]+)</loc>", sm)
check(len(locs) == 21, f"sitemap locs {len(locs)} != 21")
check("image:" not in sm and "<image" not in sm, "sitemap has image entries")
check(_re.search(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", sm) is not None, "sitemap lastmod not date-only")
rb = open(os.path.join(OUT, "robots.txt")).read()
check("Host:" not in rb, "robots has Host: line")
check("Allow: /" in rb, "robots missing Allow:/")
print("sitemap locs:", len(locs))

# ---------- 6. dashes + dangling fragments in built HTML ----------
bad_dash, bad_frag = [], []
for root, dirs, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            txt = open(os.path.join(root, f), encoding="utf-8").read()
            body = _re.sub(r"<script.*?</script>", "", txt, flags=_re.S)
            body = _re.sub(r"<style.*?</style>", "", body, flags=_re.S)
            if "—" in body or "–" in body:
                bad_dash.append(f)
            if _re.search(r"See and\b|See \.", body):
                bad_frag.append(f)
check(len(bad_dash) == 0, f"em/en dash in: {bad_dash}")
check(len(bad_frag) == 0, f"dangling fragments in: {bad_frag}")
print("dash/fragment pages:", len(bad_dash), len(bad_frag))

# ---------- 7. link resolution ----------
all_hrefs = set()
for root, dirs, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            txt = open(os.path.join(root, f), encoding="utf-8").read()
            for h in _re.findall(r'href="(/[^"#]*)', txt):
                all_hrefs.add(h)
missing_links = []
for h in sorted(all_hrefs):
    if h in ("", "/"):
        continue
    # assets are not pages: _next chunks, images, favicon, css/js
    if h.startswith(("/_next/", "/images/")) or h in ("/favicon.svg"):
        continue
    if _re.search(r"\.(js|css|webp|svg|png|jpg|xml|txt)$", h):
        continue
    fp = os.path.join(OUT, h.lstrip("/") + ".html")
    fp2 = os.path.join(OUT, h.lstrip("/"), "index.html")
    if not (os.path.exists(fp) or os.path.exists(fp2)):
        missing_links.append(h)
check(len(missing_links) == 0, f"links with no file: {missing_links}")
print("internal hrefs:", len(all_hrefs), "missing:", len(missing_links))

report = {"fails": fails, "fail_count": len(fails), "notes": notes,
          "word_diff_checked": checked, "word_diff_missing": missing,
          "contamination_hits": hits, "images": len(imgs), "images_over_200kb": over,
          "image_meta_problems": meta_problems, "sitemap_locs": len(locs),
          "internal_hrefs": len(all_hrefs), "links_missing": missing_links}
json.dump(report, open(os.path.join(QA, "findings-extra.json"), "w"), indent=2)
print(f"\nHERO-AZ EXTRAS DONE: FAILS={len(fails)}")
for f in fails:
    print(" FAIL:", f)
