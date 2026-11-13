#!/usr/bin/env python3
"""Search Pexels (public search page, no API key) and list photo IDs with
descriptive name + keywords from the page's JSON-LD.
Usage: pexels-search.py "query" [max] [page]
Prints JSON: [{id, name, keywords, page_url}] in search order, deduped."""
import sys, json, re, urllib.request, urllib.parse

q = sys.argv[1]
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 20
page = sys.argv[3] if len(sys.argv) > 3 else "1"
url = "https://www.pexels.com/search/" + urllib.parse.quote(q) + "/?page=" + page
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"})
import time
html = None
for attempt in range(4):
    try:
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        break
    except Exception as e:
        if attempt == 3:
            raise
        time.sleep(2 * (attempt + 1))
html = html.replace("\\u002F", "/").replace("\\u0026", "&")
seen, out = set(), []
for m in re.finditer(r'\{"@type":"ImageObject","url":"[^"]*?/photo/([^/"]+?)-(\d+)/".*?"name":"((?:[^"\\]|\\.)*)"', html):
    slug, pid, name = m.group(1), m.group(2), m.group(3)
    if pid in seen:
        continue
    seen.add(pid)
    tail = html[m.end():m.end() + 2500]
    km = re.search(r'"keywords":"((?:[^"\\]|\\.)*)"', tail)
    kws = km.group(1) if km else ""
    out.append({"id": pid, "name": name, "slug": slug,
                "keywords": kws[:400],
                "page_url": f"https://www.pexels.com/photo/{slug}-{pid}/"})
    if len(out) >= mx:
        break
if not out:
    # Fallback: some search pages omit the ItemList JSON-LD; parse <img> tags.
    for pid, alt in re.findall(r'<img[^>]*images\.pexels\.com/photos/(\d+)/[^>]*alt="([^"]*)"', html):
        if pid in seen:
            continue
        seen.add(pid)
        out.append({"id": pid, "name": alt, "slug": "",
                    "keywords": "",
                    "page_url": f"https://www.pexels.com/photo/{pid}/"})
        if len(out) >= mx:
            break
print(json.dumps(out, indent=1))
