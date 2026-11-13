#!/usr/bin/env python3
"""W2 rerun — Midvale UT final friendly check, Stage 5: DESKTOP render checks (1440x900).
Fixes vs run 1: (a) buttons measured on the HERO pair (.hero-buttons), since the
<header> itself holds only the phone link; (b) scroll-through before measuring so
loading=lazy images below the fold actually fetch; (c) fresh page per route +
browser restart every 10 routes to avoid the target crashes seen on long
resource pages; (d) viewport-only screenshot fallback if full-page crashes.
Writes qa/final5-render-desktop.json (overwrite) and qa/render-final5/desktop/*.png.
"""
import json, re, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8350/midvale-water-damage"
ROOT = Path.home() / "workspace" / "midvale-water-damage"
SHOT = ROOT / "qa" / "render-final5" / "desktop"
SHOT.mkdir(parents=True, exist_ok=True)

sitemap = (ROOT / "out" / "sitemap.xml").read_text()
locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
routes = [loc.replace("https://growthaura.github.io/midvale-water-damage", "") or "/" for loc in locs]

MEASURE_JS = r"""
() => {
  const r = {};
  const h1s = [...document.querySelectorAll('h1')];
  const vis = h1s.filter(h => { const b=h.getBoundingClientRect(); const cs=getComputedStyle(h);
    return b.width>0 && b.height>0 && cs.visibility!=='hidden' && cs.display!=='none' && parseFloat(cs.opacity)>0; });
  r.h1_count=h1s.length; r.h1_visible=vis.length;
  r.h1_text=vis.length?vis[0].innerText.trim().slice(0,120):'';
  r.title=document.title;
  r.scrollWidth=document.documentElement.scrollWidth; r.innerWidth=window.innerWidth;
  function box(el){ if(!el) return null; const b=el.getBoundingClientRect(); const cs=getComputedStyle(el);
    return {x:Math.round(b.x*10)/10,y:Math.round(b.y*10)/10,w:Math.round(b.width*10)/10,h:Math.round(b.height*10)/10,
      bottom:Math.round(b.bottom*10)/10, text:(el.innerText||'').trim().replace(/\s+/g,' ').slice(0,60),
      visible:b.width>0&&b.height>0&&cs.visibility!=='hidden'&&parseFloat(cs.opacity)>0}; }
  // hero button pair = FIRST .hero-buttons (the above-fold hero one)
  const hb = document.querySelector('.hero-buttons');
  r.hero_btn_call = hb ? box(hb.querySelector('.btn-call')) : null;
  r.hero_btn_help = hb ? box(hb.querySelector('.btn-help')) : null;
  r.hero_btn_pairs = document.querySelectorAll('.hero-buttons').length;
  // header phone link (the only button-like element actually inside <header>)
  r.header_phone = box(document.querySelector('header .header-phone'));
  const imgs=[...document.querySelectorAll('img')];
  r.img_total=imgs.length;
  r.img_broken=imgs.filter(i=>!(i.naturalWidth>0)||!i.complete).map(i=>(i.getAttribute('src')||'').slice(0,120));
  r.img_rendered=r.img_total-r.img_broken.length;
  const small=[];
  const navLinks=[...document.querySelectorAll('header nav a, header .main-nav a')];
  navLinks.forEach(a=>{const b=a.getBoundingClientRect(); if(b.height>0&&b.height<48) small.push({where:'header-nav',text:(a.innerText||'').trim().slice(0,30),h:Math.round(b.height*10)/10});});
  const footLinks=[...document.querySelectorAll('footer a')];
  footLinks.forEach(a=>{const b=a.getBoundingClientRect(); if(b.height>0&&b.height<48) small.push({where:'footer',text:(a.innerText||'').trim().slice(0,30),h:Math.round(b.height*10)/10});});
  const menu=document.querySelector('.menu-btn');
  r.menu_btn = menu ? {h:Math.round(menu.getBoundingClientRect().height*10)/10, w:Math.round(menu.getBoundingClientRect().width*10)/10, visible:getComputedStyle(menu).display!=='none'} : null;
  r.tap_small=small;
  r.nav_min_h = navLinks.length? Math.min(...navLinks.map(a=>a.getBoundingClientRect().height)) : null;
  r.footer_min_h = footLinks.length? Math.min(...footLinks.map(a=>a.getBoundingClientRect().height)) : null;
  r.nav_link_count=navLinks.length; r.footer_link_count=footLinks.length;
  // body copy font-size: visible <p> in main, excluding eyebrow + hero text
  const ps=[...document.querySelectorAll('main p')].filter(p=>{const b=p.getBoundingClientRect();
    if(!(b.width>0&&b.height>0)) return false;
    if(p.closest('.hero')||p.classList.contains('eyebrow')) return false;
    return (p.innerText||'').trim().length>20;}).slice(0,3);
  r.body_font_samples=ps.map(p=>({size:getComputedStyle(p).fontSize, text:p.innerText.trim().slice(0,50)}));
  const eb=document.querySelector('main .eyebrow');
  r.eyebrow_size = eb ? getComputedStyle(eb).fontSize : null;
  function lum(rgb){ const m=rgb.match(/[\d.]+/g); if(!m) return null;
    const c=m.slice(0,3).map(v=>{v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4);});
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
  function bgOf(el){ let n=el; while(n){ const bg=getComputedStyle(n).backgroundColor;
      if(bg && bg!=='rgba(0, 0, 0, 0)' && bg!=='transparent') return bg; n=n.parentElement; }
    return 'rgb(255, 255, 255)'; }
  let worst={ratio:99,text:'',color:'',bg:''};
  const els=[...document.querySelectorAll('main p, main li, main td, main dd')].filter(e=>{const b=e.getBoundingClientRect(); return b.width>0&&b.height>0&&(e.innerText||'').trim().length>0;});
  for(const e of els.slice(0,400)){
    const cs=getComputedStyle(e); const L1=lum(cs.color), L2=lum(bgOf(e)); if(L1===null||L2===null) continue;
    const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    if(ratio<worst.ratio) worst={ratio:Math.round(ratio*100)/100, text:(e.innerText||'').trim().slice(0,60), color:cs.color, bg:bgOf(e)};
  }
  r.worst_contrast=worst; r.contrast_sampled=Math.min(els.length,400);
  r.body_bg=getComputedStyle(document.body).backgroundColor;
  r.maps_iframe = !!document.querySelector('iframe[src*="google.com/maps"]');
  r.page_height = Math.round(document.documentElement.scrollHeight);
  return r;
}
"""

def slug_of(path):
    return "home" if path == "/" else path.strip("/").replace("/", "__")

results = []
with sync_playwright() as p:
    for idx, path in enumerate(routes):
        browser = p.chromium.launch(args=["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"])
        ctx = browser.new_context(viewport={"width":1440,"height":900})
        page = ctx.new_page()
        slug = slug_of(path)
        rec = {"route": path, "url": BASE + ("" if path == "/" else path), "slug": slug}
        console_errs, page_errs, failed_local, failed_env = [], [], [], []
        page.on("console", lambda m: console_errs.append(m.text[:300]) if m.type=="error" else None)
        page.on("pageerror", lambda e: page_errs.append(str(e)[:300]))
        def on_req_failed(req):
            u=req.url
            (failed_env if ("google.com" in u or "gstatic.com" in u) else failed_local).append(u[:160])
        def on_resp(resp):
            if resp.status>=400:
                u=resp.url
                (failed_env if ("google.com" in u or "gstatic.com" in u) else failed_local).append(f"{resp.status} {u[:160]}")
        page.on("requestfailed", on_req_failed)
        page.on("response", on_resp)
        try:
            resp = page.goto(rec["url"], wait_until="networkidle", timeout=45000)
            rec["http_status"] = resp.status if resp else None
            # scroll through whole page to trigger lazy images, then back to top
            page.evaluate("""async () => {
              const H=document.documentElement.scrollHeight;
              for(let y=0;y<H;y+=700){ window.scrollTo(0,y); await new Promise(r=>setTimeout(r,120)); }
              window.scrollTo(0,0);
            }""")
            page.wait_for_timeout(1500)
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            m = page.evaluate(MEASURE_JS)
            rec.update(m)
            rec["console_errors"]=console_errs; rec["page_errors"]=page_errs
            rec["failed_local"]=failed_local; rec["failed_env_google_maps"]=failed_env
            shot_ok = False
            for attempt in range(2):
                try:
                    page.screenshot(path=str(SHOT/f"{slug}.png"), full_page=True)
                    rec["screenshot"]=f"qa/render-final5/desktop/{slug}.png"; rec["screenshot_mode"]="full_page"
                    shot_ok = True; break
                except Exception as se:
                    rec["screenshot_note"]=f"full-page attempt {attempt+1} failed: {str(se)[:160]}"
            if not shot_ok:
                try:
                    page.screenshot(path=str(SHOT/f"{slug}.png"), full_page=False)
                    rec["screenshot"]=f"qa/render-final5/desktop/{slug}.png"; rec["screenshot_mode"]="viewport_only"
                except Exception as se2:
                    rec["screenshot"]=None; rec["screenshot_mode"]="FAILED"
                    rec["screenshot_error"]=str(se2)[:200]
            rec["ok"]=True
        except Exception as e:
            rec["ok"]=False; rec["error"]=str(e)[:500]
            print(f"ERROR {path}: {e}", file=sys.stderr)
        try: ctx.close()
        except Exception: pass
        try: browser.close()
        except Exception: pass
        results.append(rec)
        hb = rec.get("hero_btn_help") or {}
        print(f"{path}: H1 {rec.get('h1_visible')}/{rec.get('h1_count')} B2bottom={hb.get('bottom')} ovf={rec.get('scrollWidth')} console={len(console_errs)} failLocal={len(failed_local)} failEnv={len(failed_env)} imgs={rec.get('img_rendered')}/{rec.get('img_total')} shot={rec.get('screenshot_mode')}")
out = {"viewport":"1440x900","base":BASE,"routes_checked":len(results),
       "generated":time.strftime("%Y-%m-%d %H:%M %Z"),
       "method_notes":[
         "Hero button pair (.hero-buttons) measured: <header> holds only the phone link (.header-phone); 'Request Emergency Help' lives in the hero, above the fold at scroll-0.",
         "Scroll-through before measuring so loading=lazy images fetch; img counts are post-scroll.",
         "Google Maps embed failures counted separately as environmental (sandbox has no external internet)."],
       "results":results}
(ROOT/"qa"/"final5-render-desktop.json").write_text(json.dumps(out, indent=2))
print("WROTE qa/final5-render-desktop.json")
