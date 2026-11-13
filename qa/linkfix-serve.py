#!/usr/bin/env python3
"""Serve ~/workspace/midvale-water-damage/out/ under the
/midvale-water-damage/ subpath prefix (local GitHub Pages mirror).
Usage: python3 linkfix-serve.py <port>
Recreated 2026-11-13 after /tmp was wiped by a VM replacement.
Persistent copy: qa/linkfix-serve.py
"""
import os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, unquote

ROOT = os.path.expanduser("~/workspace/midvale-water-damage/out")
PREFIX = "/midvale-water-damage"

class H(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = unquote(urlparse(path).path)
        if p == PREFIX or p == PREFIX + "/":
            return os.path.join(ROOT, "index.html")
        if p.startswith(PREFIX + "/"):
            rel = p[len(PREFIX) + 1:]
        else:
            rel = p.lstrip("/")
        cand = os.path.join(ROOT, rel)
        if os.path.isdir(cand):
            return os.path.join(cand, "index.html")
        if os.path.isfile(cand):
            return cand
        if os.path.isfile(cand + ".html"):
            return cand + ".html"
        if os.path.isfile(os.path.join(cand, "index.html")):
            return os.path.join(cand, "index.html")
        return cand
    def log_message(self, *a):
        pass

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8324
ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
