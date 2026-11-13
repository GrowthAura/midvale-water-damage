#!/usr/bin/env python3
"""W2 follow-up: (a) slow-scroll image re-verification for the 4 routes that showed
'broken' lazy images in run 3; (b) opacity-aware contrast audit (effective fg/bg
with opacity chain) on home + 3 service pages; (c) segmented full-page screenshots
for home + hardwood (full-page capture crashes on those two).
Updates qa/final5-render-desktop.json in place for the 4 image counts + 2 screenshots.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8350/midvale-water-damage"
ROOT = Path.home() / "workspace" / "midvale-water-damage"
SHOT = ROOT / "qa" / "render-final5" / "desktop"

IMG_ROUTES = ["/", "/mold-remediation", "/locations/cottonwood-heights-ut", "/locations/magna-ut"]
CONTRAST_ROUTES = ["/", "/emergency-water-extraction", "/mold-remediation", "/about"]
SEG_ROUTES = [("/", "home"), ("/hardwood-floor-cabinet-drying", "hardwood-floor-cabinet-drying")]

CONTRAST_JS = r"""
() => {
  function parseRGB(s){ const m=s.match(/[\d.]+/g); if(!m) return null; return m.slice(0,3).map(Number).concat(m.length>3?parseFloat(m[3]):1); }
  function effBg(el){ // walk up: first bg with alpha>0, composite over white
    let n=el, stack=[];
    while(n){ const bg=parseRGB(getComputedStyle(n).backgroundColor);
      if(bg && bg[3]>0){ stack.push(bg); if(bg[3]>=1) break; } n=n.parentElement; }
    let r=255,g=255,b=255;
    for(let i=stack.length-1;i>=0;i--){ const c=stack[i]; r=c[0]*c[3]+r*(1-c[3]); g=c[1]*c[3]+g*(1-c[3]); b=c[2]*c[3]+b*(1-c[3]); }
    return [r,g,b];
  }
  function effFg(el){ const cs=getComputedStyle(el); const c=parseRGB(cs.color); if(!c) return null;
    let a=c[3], n=el;
    while(n){ a*=parseFloat(getComputedStyle(n).opacity)||1; n=n.parentElement; }
    const bg=effBg(el);
    return [c[0]*a+bg[0]*(1-a), c[1]*a+bg[1]*(1-a), c[2]*a+bg[2]*(1-a)];
  }
  function lum(c){ const f=v=>{v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4);};
    return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]); }
  const rows=[];
  const els=[...document.querySelectorAll('header *, main *, footer *')].filter(e=>{
    if(e.children.length>0) return false; // leaf text nodes only
    const t=(e.innerText||'').trim(); if(!t) return false;
    const b=e.getBoundingClientRect(); if(b.width<=0||b.height<=0) return false;
    const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none') return false;
    return true; });
  for(const e of els){
    const fg=effFg(e), bg=effBg(e); if(!fg) continue;
    const L1=lum(fg), L2=lum(bg);
    const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    rows.push({ratio:Math.round(ratio*100)/100, text:(e.innerText||'').trim().slice(0,70),
      tag:e.tagName, cls:(e.className||'').toString().slice(0,40),
      size:getComputedStyle(e).fontSize});
  }
  rows.sort((a,b)=>a.ratio-b.ratio);
  return {sampled: rows.length, worst10: rows.slice(0,10)};
}
"""

results = {}
with sync_playwright() as p:
    # (a) slow image verification
    for path in IMG_ROUTES:
        b = p.chromium.launch(args=["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width":1440,"height":900})
        pg.goto(BASE + ("" if path=="/" else path), wait_until="networkidle", timeout=45000)
        pg.evaluate("""async () => {
          const H=document.documentElement.scrollHeight;
          for(let y=0;y<H;y+=400){ window.scrollTo(0,y); await new Promise(r=>setTimeout(r,250)); }
          window.scrollTo(0,0);
        }""")
        pg.wait_for_timeout(3000)
        try: pg.wait_for_load_state("networkidle", timeout=10000)
        except Exception: pass
        info = pg.evaluate("""() => {
          const imgs=[...document.querySelectorAll('img')];
          return {total: imgs.length,
                  broken: imgs.filter(i=>!(i.naturalWidth>0)||!i.complete).map(i=>(i.getAttribute('src')||'').split('/').pop()),
                  rendered: imgs.filter(i=>i.naturalWidth>0).length};
        }""")
        results[path] = {"slow_scroll_images": info}
        print(path, "slow-scroll images:", info)
        b.close()
    # (b) opacity-aware contrast
    for path in CONTRAST_ROUTES:
        b = p.chromium.launch(args=["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width":1440,"height":900})
        pg.goto(BASE + ("" if path=="/" else path), wait_until="networkidle", timeout=45000)
        pg.wait_for_timeout(800)
        c = pg.evaluate(CONTRAST_JS)
        results.setdefault(path, {})["contrast_opacity_aware"] = c
        print(path, "contrast sampled:", c["sampled"], "worst:", c["worst10"][0] if c["worst10"] else None)
        b.close()
    # (c) segmented full-page screenshots
    from PIL import Image
    import io
    for path, slug in SEG_ROUTES:
        b = p.chromium.launch(args=["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"])
        pg = b.new_page(viewport={"width":1440,"height":900})
        pg.goto(BASE + ("" if path=="/" else path), wait_until="networkidle", timeout=45000)
        H = pg.evaluate("document.documentElement.scrollHeight")
        segs = []
        y = 0
        while y < H:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(400)
            shot = pg.screenshot(full_page=False)
            segs.append(Image.open(io.BytesIO(shot)))
            y += 850
        total_h = sum(s.height for s in segs)
        canvas = Image.new("RGB", (1440, total_h), "white")
        off = 0
        for s in segs:
            canvas.paste(s, (0, off)); off += s.height
        # crop to true page height (last segment may overshoot)
        canvas = canvas.crop((0, 0, 1440, min(total_h, H)))
        canvas.save(str(SHOT / f"{slug}.png"))
        print(slug, "segmented full-page saved:", len(segs), "segments, page height", H, "->", (SHOT/f"{slug}.png").stat().st_size, "bytes")
        results.setdefault(path, {})["screenshot_segmented"] = {"segments": len(segs), "page_height": H}
        b.close()

# merge into JSON
jpath = ROOT / "qa" / "final5-render-desktop.json"
data = json.loads(jpath.read_text())
for r in data["results"]:
    upd = results.get(r["route"])
    if not upd: continue
    if "slow_scroll_images" in upd:
        r["img_total_slow"] = upd["slow_scroll_images"]["total"]
        r["img_rendered_slow"] = upd["slow_scroll_images"]["rendered"]
        r["img_broken_slow"] = upd["slow_scroll_images"]["broken"]
        r["img_rendered"] = upd["slow_scroll_images"]["rendered"]
        r["img_broken"] = upd["slow_scroll_images"]["broken"]
    if "contrast_opacity_aware" in upd:
        r["contrast_opacity_aware"] = upd["contrast_opacity_aware"]
    if "screenshot_segmented" in upd:
        r["screenshot_mode"] = "full_page_segmented"
        r["screenshot_segments"] = upd["screenshot_segmented"]["segments"]
data["followup"] = ("Slow-scroll re-check (400px steps, 250ms) for the 4 routes with lazy-image "
  "flags; opacity-aware contrast audit on 4 pages; segmented full-page screenshots for home + hardwood.")
jpath.write_text(json.dumps(data, indent=2))
print("JSON updated")
