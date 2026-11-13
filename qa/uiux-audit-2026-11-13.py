#!/usr/bin/env python3
"""Stage 1 UI/UX CSS/typography/component audit for Midvale UT site.
Serves out/ on http://127.0.0.1:8343/midvale-water-damage/ (linkfix-serve.py).
Measures computed styles across ALL 31 routes at 320 / 390 / 1440.
READ-ONLY audit: no source edits. Output: qa/uiux-css-2026-11-13.json
"""
import json, re, sys
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

JS_COLLECT = r"""
() => {
  const out = {h1:[],h2:[],h3:[],bodyBelow19:[],allTextSizes:{},contrast:[],
    sections:[],overflow:0,scrollW:0,innerW:0,buttons:[],header:{},footer:{},
    sticky:{},hamburger:{},form:{},cards:[],tables:[],faq:[],breadcrumb:[],
    trust:[],tapTargets:[],imgs:[]};
  const cs = el => getComputedStyle(el);
  const vis = el => { const r = el.getBoundingClientRect(); const s = cs(el);
    return r.width>0 && r.height>0 && s.display!=='none' && s.visibility!=='hidden'; };
  function lum(rgb){ const m=rgb.match(/[\d.]+/g); if(!m) return null;
    const c=m.slice(0,3).map(v=>{v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4);});
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
  function bgOf(el){ let e=el; while(e){ const b=cs(e).backgroundColor;
      if(b && !b.startsWith('rgba(0, 0, 0, 0)') && b!=='transparent') return b; e=e.parentElement; }
    return 'rgb(255, 255, 255)'; }
  function ratio(fg,bg){ const L1=lum(fg),L2=lum(bg); if(L1==null||L2==null) return null;
    const hi=Math.max(L1,L2),lo=Math.min(L1,L2); return (hi+0.05)/(lo+0.05); }
  const txt = (el)=> (el.textContent||'').trim().replace(/\s+/g,' ').slice(0,60);

  document.querySelectorAll('h1,h2,h3').forEach(el=>{ if(!vis(el)) return;
    const s=cs(el); out[el.tagName.toLowerCase()].push({text:txt(el),
      size:parseFloat(s.fontSize), lh:parseFloat(s.lineHeight)||null, color:s.color,
      weight:s.fontWeight, family:s.fontFamily.slice(0,40), bg:bgOf(el),
      ratio:ratio(s.color,bgOf(el))}); });

  // body copy: p / li inside main (or article) — real copy
  const main = document.querySelector('main')||document.body;
  main.querySelectorAll('p,li').forEach(el=>{ if(!vis(el)) return;
    const s=cs(el); const sz=parseFloat(s.fontSize);
    out.allTextSizes[sz]=(out.allTextSizes[sz]||0)+1;
    if(sz<19) out.bodyBelow19.push({tag:el.tagName, size:sz, cls:(el.className||'').toString().slice(0,50),
      text:txt(el), color:s.color, ratio:ratio(s.color,bgOf(el))}); });

  // contrast sweep: all visible text-bearing leaf elements
  document.querySelectorAll('body *').forEach(el=>{ if(!vis(el)) return;
    if(el.children.length>0) return; const t=(el.textContent||'').trim(); if(!t) return;
    const s=cs(el); const sz=parseFloat(s.fontSize); const r=ratio(s.color,bgOf(el));
    if(r==null) return; const large = sz>=24 || (sz>=18.66 && parseInt(s.fontWeight)>=700);
    const min = large?3:4.5;
    if(r<min+0.5) out.contrast.push({text:txt(el), size:sz, weight:s.fontWeight,
      fg:s.color, bg:bgOf(el), ratio:+r.toFixed(2), min, cls:(el.className||'').toString().slice(0,60)}); });

  document.querySelectorAll('section').forEach(el=>{ if(!vis(el)) return;
    const s=cs(el); out.sections.push({cls:(el.className||'').toString().slice(0,60),
      pt:parseFloat(s.paddingTop), pb:parseFloat(s.paddingBottom)}); });

  out.overflow = document.documentElement.scrollWidth - window.innerWidth;
  out.scrollW = document.documentElement.scrollWidth; out.innerW = window.innerWidth;

  // buttons: anchors/buttons with visible text, esp. hero CTAs
  document.querySelectorAll('a,button').forEach(el=>{ if(!vis(el)) return;
    const s=cs(el); const r=el.getBoundingClientRect();
    const t=txt(el); if(!t) return;
    out.buttons.push({text:t, tag:el.tagName, href:(el.getAttribute('href')||'').slice(0,60),
      size:parseFloat(s.fontSize), w:+r.width.toFixed(1), h:+r.height.toFixed(1),
      bg:s.backgroundColor, color:s.color, ratio:ratio(s.color,bgOf(el)),
      top:+r.top.toFixed(1), cls:(el.className||'').toString().slice(0,60)}); });

  const hdr=document.querySelector('header'); if(hdr){ const s=cs(hdr); const r=hdr.getBoundingClientRect();
    out.header={h:+r.height.toFixed(1), bg:s.backgroundColor, position:s.position,
      brand:(hdr.querySelector('a')||{}).textContent? (hdr.querySelector('a').textContent||'').trim().slice(0,60):'',
      navLinks:[...hdr.querySelectorAll('nav a')].map(a=>a.textContent.trim()).slice(0,12),
      phoneLink: !![...hdr.querySelectorAll('a')].find(a=>/385/.test(a.textContent||''))}; }
  const ftr=document.querySelector('footer'); if(ftr){ const r=ftr.getBoundingClientRect();
    out.footer={h:+r.height.toFixed(1),
      linkGroups:[...ftr.querySelectorAll('h2,h3,h4,strong,div')].filter(e=>e.children.length===0&&e.textContent.trim().length>2&&e.textContent.trim().length<40).map(e=>e.textContent.trim()).slice(0,12),
      links:[...ftr.querySelectorAll('a')].map(a=>a.textContent.trim()).filter(Boolean),
      mapIframe: !!ftr.querySelector('iframe')}; }

  // sticky call bar: fixed-position bottom element
  document.querySelectorAll('body *').forEach(el=>{ const s=cs(el);
    if(s.position==='fixed' && (s.bottom==='0px'||parseFloat(s.bottom)===0)){
      const r=el.getBoundingClientRect(); if(r.height>0&&r.width>100)
        out.sticky={cls:(el.className||'').toString().slice(0,80), h:+r.height.toFixed(1),
          text:txt(el), visible:r.top<window.innerHeight}; }});

  const ham=document.querySelector('button[aria-label*="menu" i],button[aria-expanded],button[aria-controls]');
  if(ham){ const r=ham.getBoundingClientRect(); out.hamburger={found:true,
    label:ham.getAttribute('aria-label'), expanded:ham.getAttribute('aria-expanded'),
    w:+r.width.toFixed(1), h:+r.height.toFixed(1), visible:vis(ham)}; }
  else out.hamburger={found:false};

  const form=document.querySelector('form'); if(form){
    out.form={inputs:[...form.querySelectorAll('input,textarea,select')].map(i=>({type:i.type||i.tagName,
      name:i.name, required:i.required, placeholder:(i.placeholder||'').slice(0,30)})),
      labels:[...form.querySelectorAll('label')].map(l=>l.textContent.trim()).slice(0,15),
      radios:[...form.querySelectorAll('input[type=radio]')].map(i=>({name:i.name,value:i.value,checked:i.checked})),
      submit:[...form.querySelectorAll('button[type=submit],input[type=submit]')].map(b=>({text:(b.textContent||b.value||'').trim(),
        h:+b.getBoundingClientRect().height.toFixed(1), w:+b.getBoundingClientRect().width.toFixed(1)}))}; }

  document.querySelectorAll('[class*=card],article').forEach(el=>{ if(!vis(el)) return;
    const r=el.getBoundingClientRect(); const img=el.querySelector('img');
    if(img){ const ir=img.getBoundingClientRect(); const s=cs(img);
      out.cards.push({cls:(el.className||'').toString().slice(0,50), h:+r.height.toFixed(1),
        imgW:+ir.width.toFixed(1), imgH:+ir.height.toFixed(1), objFit:s.objectFit,
        natural:img.naturalWidth+'x'+img.naturalHeight, src:(img.getAttribute('src')||'').split('/').pop()}); }});

  document.querySelectorAll('table').forEach(el=>{ if(!vis(el)) return;
    const r=el.getBoundingClientRect(); out.tables.push({w:+r.width.toFixed(1),
      scrollW:el.scrollWidth, overflow: el.scrollWidth>r.width+1, rows:el.querySelectorAll('tr').length}); });

  document.querySelectorAll('details, [class*=faq], [class*=accordion]').forEach(el=>{ if(!vis(el)) return;
    out.faq.push({tag:el.tagName, cls:(el.className||'').toString().slice(0,50),
      open: el.open!==undefined? el.open : null, text:txt(el)}); });

  document.querySelectorAll('nav[aria-label*=bread i], [class*=breadcrumb], ol li a').forEach(el=>{ if(!vis(el)) return;
    if(/breadcrumb/i.test(el.className||'')||/breadcrumb/i.test(el.getAttribute('aria-label')||''))
      out.breadcrumb.push({text:txt(el)}); });
  document.querySelectorAll('[class*=trust], [class*=badge], [class*=guarantee]').forEach(el=>{ if(!vis(el)) return;
    out.trust.push({cls:(el.className||'').toString().slice(0,50), text:txt(el)}); });

  // tap targets on mobile: all interactive elements
  document.querySelectorAll('a,button,input,select,textarea,summary').forEach(el=>{ if(!vis(el)) return;
    const r=el.getBoundingClientRect();
    if(r.width<44||r.height<44) out.tapTargets.push({text:txt(el), tag:el.tagName,
      w:+r.width.toFixed(1), h:+r.height.toFixed(1), cls:(el.className||'').toString().slice(0,50)}); });

  // images: broken / distorted
  document.querySelectorAll('img').forEach(el=>{ const r=el.getBoundingClientRect();
    if(!el.complete||el.naturalWidth===0) out.imgs.push({src:(el.getAttribute('src')||'').slice(0,80), broken:true});
    else if(r.width>0 && Math.abs((el.naturalWidth/el.naturalHeight)-(r.width/r.height))>0.15)
      out.imgs.push({src:(el.getAttribute('src')||'').split('/').pop(), distorted:true,
        natural:el.naturalWidth+'x'+el.naturalHeight, shown:+r.width.toFixed(0)+'x'+r.height.toFixed(0)}); });
  return out;
}
"""

def main():
    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for width in (320, 390, 1440):
            ctx = b.new_context(viewport={"width": width, "height": 844 if width < 500 else 900},
                                device_scale_factor=1, is_mobile=width < 500)
            pg = ctx.new_page()
            for route in ROUTES:
                url = BASE + (route if route != "/" else "/")
                try:
                    pg.goto(url, wait_until="networkidle", timeout=30000)
                except Exception as e:
                    results.setdefault(route, {})[str(width)] = {"error": f"goto: {e}"}
                    continue
                try:
                    d = pg.evaluate(JS_COLLECT)
                except Exception as e:
                    results.setdefault(route, {})[str(width)] = {"error": f"collect: {e}"}
                    continue
                d["title"] = pg.title()
                # Button 2 at scroll-0: find hero CTA (non-phone) — record topmost CTA pair
                results.setdefault(route, {})[str(width)] = d
                # hamburger interaction on mobile
                if width < 500:
                    try:
                        ham = pg.query_selector('button[aria-label*="menu" i],button[aria-expanded]')
                        if ham and ham.is_visible():
                            ham.click(timeout=3000)
                            pg.wait_for_timeout(400)
                            nav = pg.evaluate("""() => {
                              const n=document.querySelector('nav, [class*=mobile-nav], [class*=menu]');
                              const links=[...document.querySelectorAll('header a, nav a')].filter(a=>{const r=a.getBoundingClientRect(); return r.width>0&&r.height>0;}).map(a=>a.textContent.trim());
                              return {openLinks:links}; }""")
                            results[route][str(width)]["hamburgerAfterClick"] = nav
                            ham.click(timeout=3000); pg.wait_for_timeout(300)
                    except Exception as e:
                        results[route][str(width)]["hamburgerAfterClick"] = {"error": str(e)}
                # FAQ accordion interaction (desktop pass only, once per route)
                if width == 1440:
                    try:
                        faq = pg.evaluate("""() => {
                          const out=[];
                          const items=[...document.querySelectorAll('details')];
                          items.slice(0,3).forEach(d=>{ const s=d.querySelector('summary'); if(!s) return;
                            const before=d.open; s.click(); out.push({q:s.textContent.trim().slice(0,50), before, after:d.open}); });
                          return out; }""")
                        results[route][str(width)]["faqClick"] = faq
                    except Exception as e:
                        results[route][str(width)]["faqClick"] = {"error": str(e)}
            ctx.close()
        b.close()
    with open("/home/hatch/workspace/midvale-water-damage/qa/uiux-css-2026-11-13.json", "w") as f:
        json.dump(results, f, indent=1)
    print("routes:", len(results), "widths done")

if __name__ == "__main__":
    main()
