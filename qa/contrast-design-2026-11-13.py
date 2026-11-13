#!/usr/bin/env python3
"""WCAG contrast ratios for the Midvale design-round palette.
Pairs are (text colour, background colour) as actually rendered.
AA minimum 4.5:1 for normal text; 3:1 for large text / UI.
"""
def lum(hexs):
    h = hexs.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ratio(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

PAIRS = [
    ("H2 pine #0e3b38 on white", "#0e3b38", "#ffffff"),
    ("H2 pine #0e3b38 on mist #e8efec (.section.alt)", "#0e3b38", "#e8efec"),
    ("H2 pine #0e3b38 on sand #f6f1e7 (.section.sand/.page-head)", "#0e3b38", "#f6f1e7"),
    ("H3 pine-2 #15524c on white", "#15524c", "#ffffff"),
    ("H3 pine-2 #15524c on mist #e8efec", "#15524c", "#e8efec"),
    ("H3 pine-2 #15524c on sand #f6f1e7", "#15524c", "#f6f1e7"),
    ("Body ink #1b2a28 on white", "#1b2a28", "#ffffff"),
    ("Body ink #1b2a28 on mist #e8efec", "#1b2a28", "#e8efec"),
    ("Body ink #1b2a28 on sand #f6f1e7", "#1b2a28", "#f6f1e7"),
    ("Muted #41524e on white (breadcrumb sep)", "#41524e", "#ffffff"),
    ("Brand-city copper-dark #9d5418 on white (was copper 3.90:1)", "#9d5418", "#ffffff"),
    ("Card-link copper-dark #9d5418 on white", "#9d5418", "#ffffff"),
    ("Body-link pine-2 #15524c on white", "#15524c", "#ffffff"),
    ("White on copper-dark #9d5418 (Button 1 / header phone / sticky bar)", "#ffffff", "#9d5418"),
    ("White on hover #7c3f12", "#ffffff", "#7c3f12"),
    ("White H2 on pine #0e3b38 (final CTA)", "#ffffff", "#0e3b38"),
    ("White th on pine #0e3b38", "#ffffff", "#0e3b38"),
    ("Footer link #dfeae7 on pine #0e3b38", "#dfeae7", "#0e3b38"),
    ("Footer hover #f2c89b on pine #0e3b38", "#f2c89b", "#0e3b38"),
    ("White H1 on hero photo bg #07211e (before shade)", "#ffffff", "#07211e"),
    ("Eyebrow #f2c89b on hero bg #07211e", "#f2c89b", "#07211e"),
    ("Hero intro #eef4f2 on hero bg #07211e", "#eef4f2", "#07211e"),
    ("Hero breadcrumb link #f2c89b on hero bg #07211e", "#f2c89b", "#07211e"),
    ("Steps number white on copper #c26a24", "#ffffff", "#c26a24"),
    ("Panel tag rgba white .9 on pine-2 (approx #15524c)", "#e6efec", "#15524c"),
]
worst = None
for name, fg, bg in PAIRS:
    r = ratio(fg, bg)
    verdict = "PASS AA" if r >= 4.5 else ("PASS large-only" if r >= 3 else "FAIL")
    if worst is None or r < worst[1]:
        worst = (name, r)
    print(f"{r:5.2f}:1  {verdict:15s} {name}")
print()
print(f"WORST: {worst[0]} at {worst[1]:.2f}:1")
