#!/usr/bin/env python3
"""Publish-step subpath rewrite for the Midvale GitHub Pages PREVIEW.

OBSOLETE since the 2026-11-12 rebuild: next.config.mjs now sets
basePath + assetPrefix = "/midvale-water-damage", so the export is
ALREADY subpath-prefixed: the output is FLAT under out/ (out/index.html,
out/about.html, out/_next/...) with "/midvale-water-damage/" inside every
href/src — verified in the 2026-11-12 export (32 html files, 0
"//midvale-water-damage", 0 unprefixed href/src except the favicon, now
fixed via ASSET_PREFIX). Running this rewrite on a basePath build
would DOUBLE-prefix every URL (the regex matches the prefixed slash
too). A GUARD in main() refuses to run when any .html in SRC already
contains "/midvale-water-damage/" — this script is kept only as a
historical record and a safety net. DO NOT run it on a basePath build.

NEW gh-pages publish procedure (2026-11-12, see PROGRESS.md):
  copy out/* to the gh-pages branch root
  + .nojekyll, NO rewriting.

The OLD procedure below applied only to the pre-basePath root-relative
build: the github.io PREVIEW lives at the subpath /midvale-water-damage/,
so every root-relative URL in the built .html files had to be prefixed
with that subpath before the tree was published to gh-pages.

Skipped once on Plano (2026-11-05) -> every CSS/image 404'd and the
preview rendered completely unstyled. NEVER publish gh-pages without
this step.

Usage:  python3 publish_prefix.py [src_dir] [dest_dir]
Default src = ~/workspace/midvale-water-damage/out
Default dest = /tmp/midvale-ghpages (the gh-pages worktree)

Rule: in *.html files ONLY, rewrite a "/" that starts a site URL
(a slash NOT followed by another slash or ">", preceded by a quote or
comma+space) to "/midvale-water-damage/".
Untouched by design: absolute https:// URLs, tel: links, protocol-
relative // URLs, sitemap.xml / robots.txt (absolute localhost
placeholder already — known preview limit), canonical + OG URLs
(absolute already), .css files (the only "/" in the CSS is the
breadcrumb separator content:"/" — rewriting it would corrupt it),
.js files, .txt files.
"""
import os
import re
import shutil
import sys

PREFIX = "/midvale-water-damage"
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/workspace/midvale-water-damage/out")
DEST = sys.argv[2] if len(sys.argv) > 2 else "/tmp/midvale-ghpages"

# A site-URL slash: preceded by a quote (attribute value or JSON string
# start, e.g. href="/x) or by comma+space (srcset candidate), and NOT
# followed by ">" or "/" — the lookahead is essential: a bare "/>"
# closes a self-closing tag, and rewriting that slash corrupts the tag.
# The "/" is OUTSIDE the capture group: putting it inside emits
# "//midvale-water-damage/..." (protocol-relative host) and every
# CSS/image 404s while curl 200s still false-pass (Tulsa, 2026-11-07).
URL_SLASH = re.compile(r"""((?:["']|,\s*))/(?!>|/)""")


def rewrite_html(text):
    return URL_SLASH.sub(r"\1" + PREFIX + "/", text)


def main():
    # GUARD (2026-11-12 rebuild): refuse to run on a basePath build.
    # The export already contains "/midvale-water-damage/" in href/src;
    # rewriting it would DOUBLE-prefix every URL. Check SRC (the build
    # tree) and DEST (the tree about to be rewritten) — either one
    # already prefixed means STOP without changing anything.
    for tree in (SRC, DEST):
        if not os.path.isdir(tree):
            continue
        for root, _dirs, files in os.walk(tree):
            if ".git" in root:
                continue
            for name in files:
                if not name.endswith(".html"):
                    continue
                path = os.path.join(root, name)
                with open(path, encoding="utf-8") as f:
                    if PREFIX + "/" in f.read():
                        print(
                            f"REFUSAL: {path} already contains "
                            f'"{PREFIX}/" — this is a basePath build. '
                            "publish_prefix.py is OBSOLETE; the gh-pages "
                            "publish is now: copy "
                            "out/* to the gh-pages "
                            "branch root + .nojekyll, NO rewriting. "
                            "Nothing was changed."
                        )
                        sys.exit(1)
    changed = 0
    for root, _dirs, files in os.walk(DEST):
        if ".git" in root:
            continue
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                orig = f.read()
            new = rewrite_html(orig)
            if new != orig:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
                changed += 1
    print(f"rewrote {changed} html files in {DEST}")


if __name__ == "__main__":
    main()
