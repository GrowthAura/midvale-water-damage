#!/usr/bin/env python3
"""Supplementary checks for Midvale UI/UX audit: contrast worst pairs,
sticky bar after scroll, images after full scroll, FAQ toggle, Button 2
at scroll-0 on all routes at 320x568 (worst case) + 320x844 + 390x844,
table parents, card heights @1440, footer headings, screenshots."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8343/midvale-water-damage"
ROUTES = [
 "/", "/about", "/contact", "/emergency-water-extraction", "/basement-flooding-cleanup",
 "/window-well-flooding", "/burst-pipe-water-damage", "/sewage-backup-cleanup",
 "/water-heater-leak-cleanup", "/swamp-cooler-leak-water-damage", "/ceiling-water-damage",
 "/crawl-space-water-damage", "/hardwood-floor-cabinet-drying", "/condo-apartment-water-damage",
 "/commercial-water-damage", "/storm-flood-damage", "/mold-remediation",
 "/water-leak-detection", "/water-damage-repair", "/locations/cottonwood-heights-ut",
 "/locations/south-salt-lake-ut", "/locations/magna-ut",
 "/midvale-water-sewer-emergency-contacts", "/privacy-policy", "/terms-of-use",
 "/disclaimer", "/resources/frozen-pipes-midvale", "/resources/winterize-swamp-cooler-utah",
 "/resources/upstairs-unit-leak-who-pays-utah", "/resources/can-mold-grow-in-utah",
 "/resources/basement-flooding-spring-snowmelt-utah",
]

CONTRAST_JS = r"""
() => {
  const res=[];
  const cs=el=>getComputedStyle(el);
  const vis=el=>{const r=el.getBoundingClientRect();const s=cs(el);
    return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden';};
  function lum(rgb){const m=rgb.match(/[\d.]+/g);if(!m)return null;
    const c=m.slice(0,3).map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);});
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];}
  function bgOf(el){let e=el;while(e){const b=cs(e).backgroundColor;
    if(b&&!b.startsWith('rgba(0, 0, 0, 0)')&&b!=='transparent')return b;e=e.parentElement;}
    return 'rgb(255, 255, 255)';}
  document.querySelectorAll('body *').forEach(el=>{ if(!vis(el))return;
    if(el.children.length>0)return; const t=(el.textContent||'').trim(); if(!t)return;
    const s=cs(el); const L1=lum(s.color),L2=lum(bgOf(el)); if(L1==null||L2==null)return;
    const hi=Math.max(L1,L2),lo=Math.min(L1,L2); const r=(hi+0.05)/(lo+0.05);
    res.push({text:t.slice(0,50),size:parseFloat(s.fontSize),weight:s.fontWeight,
      fg:s.color,bg:bgOf(el),ratio:+r.toFixed(2),cls:(el.className||'').toString().slice(0,40)});});
  res.sort((a,b)=>a.ratio-b.ratio); return res.slice(0,12);
}
"""

BTN2_JS = r"""
() => {
  const out={vpH:window.innerHeight, btns:[]};
  const btns=[...document.querySelectorAll('.hero-buttons a, .hero-buttons button')];
  btns.forEach(b=>{const r=b.getBoundingClientRect();const s=getComputedStyle(b);
    out.btns.push({text:b.textContent.trim().slice(0,40),href:(b.getAttribute('href')||'').slice(0,40),
      w:+r.width.toFixed(1),h:+r.height.toFixed(1),top:+r.top.toFixed(1),bottom:+r.bottom.toFixed(1),
      size:parseFloat(s.fontSize),bg:s.backgroundColor});});
  const h1=document.querySelector('h1'); if(h1){const r=h1.getBoundingClientRect();const s=getComputedStyle(h1);
    out.h1={size:parseFloat(s.fontSize),lh:parseFloat(s.lineHeight),top:+r.top.toFixed(1),bottom:+r.bottom.toFixed(1)};}
  const hdr=document.querySelector('header'); if(hdr){const r=hdr.getBoundingClientRect();out.headerH=+r.height.toFixed(1);}
  return out;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    # --- contrast worst pairs @1440 + @390 (home + 3 sample pages) ---
    contrast = {}
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    for route in ["/", "/emergency-water-extraction", "/contact", "/about"]:
        pg.goto(BASE + route, wait_until="networkidle")
        contrast[route] = pg.evaluate(CONTRAST_JS)
    ctx.close()
    # --- Button 2 scroll-0 all routes, 320x568 / 320x844 / 390x844 ---
    btn2 = {}
    for (w, h) in [(320, 568), (320, 844), (390, 844)]:
        ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=True)
        pg = ctx.new_page()
        for route in ROUTES:
            pg.goto(BASE + route, wait_until="networkidle")
            btn2.setdefault(route, {})[f"{w}x{h}"] = pg.evaluate(BTN2_JS)
        ctx.close()
    # --- sticky bar, images after scroll, FAQ toggle, tables, cards, footer ---
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
    pg = ctx.new_page()
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.evaluate("window.scrollTo(0, 1200)"); pg.wait_for_timeout(600)
    sticky390 = pg.evaluate("""() => { const el=document.querySelector('.sticky-bar');
      if(!el) return {found:false}; const r=el.getBoundingClientRect(); const s=getComputedStyle(el);
      const a=el.querySelector('a'); const ar=a?a.getBoundingClientRect():null;
      return {found:true, display:s.display, h:+r.height.toFixed(1), top:+r.top.toFixed(1),
        linkH: ar?+ar.height.toFixed(1):null, bodyPadBottom:getComputedStyle(document.body).paddingBottom,
        coversFooter: r.top < window.innerHeight}; }""")
    # scroll to very bottom: does bar cover footer-base text?
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(600)
    sticky_bottom = pg.evaluate("""() => { const el=document.querySelector('.sticky-bar');
      const r=el.getBoundingClientRect();
      const elAt=document.elementFromPoint(window.innerWidth/2, window.innerHeight-10);
      return {barTop:+r.top.toFixed(1), barH:+r.height.toFixed(1),
        underBar: elAt? (elAt.textContent||'').trim().slice(0,60)+' <'+elAt.tagName+'>' : null,
        footerBaseVisible: !!document.querySelector('.footer-base')}; }""")
    # FAQ toggle
    pg.goto(BASE + "/", wait_until="networkidle")
    faq = pg.evaluate("""() => { const item=document.querySelector('.faq-item');
      if(!item) return {found:false};
      const q=item.querySelector('h3'); const a=item.querySelector('p');
      const before={h:+a.getBoundingClientRect().height.toFixed(1), disp:getComputedStyle(a).display, vis:getComputedStyle(a).visibility};
      q.click(); return {found:true, before, afterClick:{h:+a.getBoundingClientRect().height.toFixed(1), disp:getComputedStyle(a).display}}; }""")
    # images after full scroll (lazy load)
    pg.evaluate("""async () => { await new Promise(res=>{ let y=0;
      const t=setInterval(()=>{ y+=800; window.scrollTo(0,y);
        if(y>=document.body.scrollHeight){clearInterval(t);res();} },120); }); }""")
    pg.wait_for_timeout(1200)
    imgs = pg.evaluate("""() => { const bad=[];
      document.querySelectorAll('img').forEach(el=>{ const r=el.getBoundingClientRect();
        if(!el.complete||el.naturalWidth===0) bad.push({src:(el.getAttribute('src')||'').split('/').pop(),broken:true});
        else { const s=getComputedStyle(el);
          if(s.objectFit==='fill'||s.objectFit==='none') bad.push({src:(el.getAttribute('src')||'').split('/').pop(),fit:s.objectFit}); }});
      return {total:document.querySelectorAll('img').length, bad}; }""")
    # table parents @320
    ctx2 = b.new_context(viewport={"width": 320, "height": 844}, is_mobile=True)
    pg2 = ctx2.new_page()
    pg2.goto(BASE + "/", wait_until="networkidle")
    tables = pg2.evaluate("""() => { const out=[];
      document.querySelectorAll('table').forEach(t=>{ const r=t.getBoundingClientRect();
        const p=t.parentElement; const ps=getComputedStyle(p);
        out.push({w:+r.width.toFixed(1), parentTag:p.tagName, parentCls:(p.className||'').toString().slice(0,40),
          parentOverflowX:ps.overflowX, parentScrollW:p.scrollWidth, docOverflow:document.documentElement.scrollWidth-window.innerWidth}); });
      return out; }""")
    # card heights @1440 home
    ctx3 = b.new_context(viewport={"width": 1440, "height": 900})
    pg3 = ctx3.new_page()
    pg3.goto(BASE + "/", wait_until="networkidle")
    cards = pg3.evaluate("""() => { const rows={};
      document.querySelectorAll('.card-grid > *').forEach(c=>{ const r=c.getBoundingClientRect();
        const key=Math.round(r.top); (rows[key]=rows[key]||[]).push(+r.height.toFixed(1)); });
      return rows; }""")
    footer = pg3.evaluate("""() => { const out=[];
      document.querySelectorAll('.footer-h').forEach(h=>{ const s=getComputedStyle(h);
        out.push({text:h.textContent.trim(), size:parseFloat(s.fontSize), color:s.color}); });
      const links=[...document.querySelectorAll('.site-footer a')].map(a=>{const s=getComputedStyle(a);const r=a.getBoundingClientRect();
        return {size:parseFloat(s.fontSize), h:+r.height.toFixed(1), color:s.color};});
      const f=document.querySelector('.site-footer');
      return {heads:out, linkSize:new Set(links.map(l=>l.size)), linkH:new Set(links.map(l=>l.h)),
        linkColors:new Set(links.map(l=>l.color)), mapH: document.querySelector('.footer-map iframe')?.getBoundingClientRect().height}; }""")
    sections = pg3.evaluate("""() => { const out=[];
      document.querySelectorAll('section').forEach(s=>{ const cs=getComputedStyle(s);
        out.push({cls:(s.className||'').toString().slice(0,40), pt:parseFloat(cs.paddingTop), pb:parseFloat(cs.paddingBottom)}); });
      const p=document.querySelector('main p'); const ps=p?getComputedStyle(p):null;
      return {sections:out, bodyLH: ps?parseFloat(ps.lineHeight):null, bodySize: ps?parseFloat(ps.fontSize):null}; }""")
    # screenshots
    pg3.goto(BASE + "/", wait_until="networkidle")
    pg3.screenshot(path="/home/hatch/workspace/midvale-water-damage/qa/uiux-home-1440.png")
    ctx4 = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
    pg4 = ctx4.new_page()
    pg4.goto(BASE + "/", wait_until="networkidle")
    pg4.screenshot(path="/home/hatch/workspace/midvale-water-damage/qa/uiux-home-390.png")
    pg4.goto(BASE + "/emergency-water-extraction", wait_until="networkidle")
    pg4.screenshot(path="/home/hatch/workspace/midvale-water-damage/qa/uiux-service-390.png")
    ctx5 = b.new_context(viewport={"width": 320, "height": 568}, is_mobile=True)
    pg5 = ctx5.new_page()
    pg5.goto(BASE + "/emergency-water-extraction", wait_until="networkidle")
    pg5.screenshot(path="/home/hatch/workspace/midvale-water-damage/qa/uiux-service-320x568.png")
    pg5.goto(BASE + "/contact", wait_until="networkidle")
    pg5.screenshot(path="/home/hatch/workspace/midvale-water-damage/qa/uiux-contact-320.png", full_page=False)
    b.close()

    out = {"contrast": contrast, "btn2": btn2, "sticky390": sticky390,
           "sticky_bottom": sticky_bottom, "faq": faq, "imgs_after_scroll": imgs,
           "tables320": tables, "cards1440": cards, "footer": footer, "sections": sections}
    json.dump(out, open("/home/hatch/workspace/midvale-water-damage/qa/uiux-css-supp-2026-11-13.json", "w"), indent=1)
    print("done")
