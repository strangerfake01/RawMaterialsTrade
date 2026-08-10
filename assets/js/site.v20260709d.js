/* Raw Materials Trade Kft. — static, crawlable catalogue enhancement */
const FORM_ENDPOINT = (window.RMT_FORM_CONFIG&&window.RMT_FORM_CONFIG.endpoint)||'https://muddy-voice-db90.6ymnrwgnv9.workers.dev/api/contact';
function getLang(){const path=window.location.pathname.toLowerCase();const file=path.split('/').pop()||'';if(file==='hu.html'||file.startsWith('hu-')||file==='ai-profile-hu.html'||path.match(/\/hu\//))return'hu';if(file==='de-at.html'||file.startsWith('de-at-')||file==='ai-profile-de-at.html'||path.match(/\/de-at\//))return'de-at';return'en'}
const FORM_TEXT={
  en:{gdpr:'Please acknowledge the privacy notice.',disc:'Please acknowledge the product documentation disclaimer.',sending:'Sending…',sent:'Thank you — your enquiry has been sent. We will respond within 1–2 business days.',mailto:'Your email client has been opened with a pre-filled message.',fail:'The form could not be sent. Your entries have been kept. Please try again or email',robot:'Please complete the security calculation correctly.',fast:'Please wait a few seconds before sending the form.'},
  hu:{gdpr:'Kérjük, erősítse meg az adatkezelési tájékoztató tudomásulvételét.',disc:'Kérjük, vegye tudomásul a termékdokumentációs nyilatkozatot.',sending:'Küldés…',sent:'Köszönjük — megkeresése elküldve. 1–2 munkanapon belül válaszolunk.',mailto:'Az e-mail-kliens előre kitöltött üzenettel megnyílt.',fail:'Az űrlapot nem sikerült elküldeni. A megadott adatok megmaradtak. Próbálja újra, vagy írjon e-mailt:',robot:'Kérjük, adja meg helyesen a biztonsági számítás eredményét.',fast:'Kérjük, várjon néhány másodpercet az űrlap elküldése előtt.'},
  'de-at':{gdpr:'Bitte bestätigen Sie, dass Sie die Datenschutzerklärung zur Kenntnis genommen haben.',disc:'Bitte bestätigen Sie den Produktdokumentations-Hinweis.',sending:'Wird gesendet…',sent:'Vielen Dank — Ihre Anfrage wurde gesendet. Wir melden uns innerhalb von 1–2 Werktagen.',mailto:'Ihr E-Mail-Programm wurde mit einer vorausgefüllten Nachricht geöffnet.',fail:'Das Formular konnte nicht gesendet werden. Ihre Eingaben bleiben erhalten. Bitte versuchen Sie es erneut oder schreiben Sie an',robot:'Bitte lösen Sie die Sicherheitsrechnung korrekt.',fast:'Bitte warten Sie einige Sekunden, bevor Sie das Formular senden.'}
};
function initNav(){
  const t=document.getElementById('navToggle');
  const n=document.getElementById('siteNav');
  const h=document.querySelector('.site-header');
  if(h){h.classList.remove('header-hidden','is-hidden');h.removeAttribute('data-hidden');}
  if(!t||!n)return;
  const setOpen=(open)=>{
    n.classList.toggle('open',!!open);
    t.classList.toggle('active',!!open);
    t.setAttribute('aria-expanded',open?'true':'false');
    document.documentElement.classList.toggle('nav-open',!!open);
  };
  const isMobileNav=()=>window.matchMedia('(max-width: 767px)').matches;
  t.addEventListener('click',(e)=>{e.preventDefault();if(!isMobileNav()){setOpen(false);return;}setOpen(!n.classList.contains('open'));});
  n.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
  document.addEventListener('click',e=>{if(!t.contains(e.target)&&!n.contains(e.target))setOpen(false);});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')setOpen(false);});
  window.addEventListener('resize',()=>{if(!isMobileNav())setOpen(false);}, {passive:true});
  window.addEventListener('orientationchange',()=>setTimeout(()=>{if(!isMobileNav())setOpen(false);},160), {passive:true});
  window.addEventListener('scroll',()=>{if(h){h.classList.remove('header-hidden','is-hidden');h.removeAttribute('data-hidden');}}, {passive:true});
}
function initCookieBanner(){/* Managed by analytics-consent.v20260713.js */}
function initFAQ(){document.querySelectorAll('.faq-item').forEach(item=>{item.querySelector('.faq-q')?.addEventListener('click',()=>{const o=item.classList.contains('open');document.querySelectorAll('.faq-item').forEach(i=>i.classList.remove('open'));if(!o)item.classList.add('open');});});}
function initCatalogue(){
  const search=document.getElementById('productSearch');
  const chips=[...document.querySelectorAll('.filter-chip')];
  const cards=[...document.querySelectorAll('.product-card')];
  const accordions=[...document.querySelectorAll('.category-accordion')];
  const result=document.getElementById('resultCount');
  const no=document.getElementById('noResults');
  let filter='all';

  const lang=getLang();
  const labels={
    en:{suggest:'Closest product matches',empty:'No close product name found. Try a shorter word, CAS number or category.'},
    hu:{suggest:'Legközelebbi terméktalálatok',empty:'Nem találtunk közeli terméknevet. Próbáljon rövidebb szót, CAS-számot vagy kategóriát.'},
    'de-at':{suggest:'Naheliegende Produkttreffer',empty:'Kein naher Produktname gefunden. Versuchen Sie ein kürzeres Wort, eine CAS-Nummer oder eine Kategorie.'}
  }[lang]||{suggest:'Closest product matches',empty:'No close product name found. Try a shorter word, CAS number or category.'};

  function normalize(str){
    return String(str||'')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g,'')
      .replace(/[–—−]/g,'-')
      .replace(/[^a-z0-9%]+/g,' ')
      .replace(/\s+/g,' ')
      .trim();
  }
  function levenshtein(a,b){
    a=normalize(a);b=normalize(b);
    if(a===b)return 0;
    if(!a.length)return b.length;
    if(!b.length)return a.length;
    if(a.length>b.length){const t=a;a=b;b=t;}
    let prev=Array.from({length:a.length+1},(_,i)=>i);
    for(let j=1;j<=b.length;j++){
      const cur=[j];
      for(let i=1;i<=a.length;i++){
        cur[i]=Math.min(cur[i-1]+1,prev[i]+1,prev[i-1]+(a[i-1]===b[j-1]?0:1));
      }
      prev=cur;
    }
    return prev[a.length];
  }
  function titleOf(card){
    return (card.querySelector('.product-title-block h3,.product-title,.product-summary h3,h3')?.textContent||card.dataset.name||'').trim();
  }
  function hrefOf(card){
    return card.querySelector('a.product-detail-link,a[href$=".html"]')?.getAttribute('href')||'';
  }
  function productInfo(card){
    const title=titleOf(card);
    return {card,title,href:hrefOf(card),hay:normalize(`${title} ${card.dataset.name||''} ${card.textContent||''}`),cats:card.dataset.categories||''};
  }
  const products=cards.map(productInfo);
  function scoreProduct(info,rawQuery){
    const q=normalize(rawQuery);
    if(!q)return 9999;
    const hay=info.hay;
    const title=normalize(info.title);
    if(hay.includes(q))return title.includes(q)?0:1;
    const qTokens=q.split(' ').filter(Boolean);
    const hTokens=hay.split(' ').filter(Boolean);
    let total=0, matched=0;
    for(const qt of qTokens){
      if(qt.length<2)continue;
      let best=999;
      for(const ht of hTokens){
        if(ht.includes(qt)||qt.includes(ht)){best=0;break;}
        if(qt.length>=3 && ht.length>=3){
          const d=levenshtein(qt,ht);
          if(d<best)best=d;
        }
      }
      const tolerance=qt.length<=4?1:Math.max(1,Math.floor(qt.length*.32));
      if(best<=tolerance){matched++;total+=best;} else total+=6;
    }
    if(!qTokens.length)return 9999;
    return matched?total+(qTokens.length-matched)*4:9999;
  }
  function closeAll(){accordions.forEach(cat=>{cat.open=false;});}
  function openOnly(target){accordions.forEach(cat=>{cat.open=(cat===target);});}
  function ensureSuggestionBox(){
    if(!search)return null;
    let box=document.getElementById('productSuggestions');
    if(box)return box;
    box=document.createElement('div');
    box.id='productSuggestions';
    box.className='product-suggestions';
    box.setAttribute('role','listbox');
    box.setAttribute('aria-label',labels.suggest);
    search.parentElement?.appendChild(box);
    return box;
  }
  function suggestionCandidates(q){
    const nq=normalize(q);
    if(nq.length<2)return [];
    return products
      .map(info=>({...info,score:scoreProduct(info,q)}))
      .filter(info=>info.score<9999)
      .sort((a,b)=>a.score-b.score || a.title.localeCompare(b.title))
      .slice(0,8);
  }
  function renderSuggestions(q){
    const box=ensureSuggestionBox();
    if(!box)return;
    const nq=normalize(q);
    if(nq.length<2){box.classList.remove('visible');box.innerHTML='';return;}
    const matches=suggestionCandidates(q);
    box.innerHTML='';
    const help=document.createElement('div');
    help.className='suggestion-help';
    help.textContent=labels.suggest;
    box.appendChild(help);
    if(!matches.length){
      const empty=document.createElement('div');
      empty.className='product-suggestion-empty';
      empty.textContent=labels.empty;
      box.appendChild(empty);
      box.classList.add('visible');
      return;
    }
    matches.forEach(info=>{
      const btn=document.createElement('button');
      btn.type='button';
      btn.className='product-suggestion-item';
      btn.setAttribute('role','option');
      const name=document.createElement('span');
      name.className='product-suggestion-name';
      name.textContent=info.title;
      const meta=document.createElement('span');
      meta.className='product-suggestion-meta';
      meta.textContent=(info.card.dataset.name||'').replace(/\s+/g,' ').trim();
      btn.appendChild(name);btn.appendChild(meta);
      btn.addEventListener('click',()=>{
        if(info.href){window.location.href=info.href;return;}
        search.value=info.title;
        applyVisibility();
        box.classList.remove('visible');
      });
      box.appendChild(btn);
    });
    box.classList.add('visible');
  }
  function productMatchesQuery(card,q){
    const nq=normalize(q);
    if(!nq)return true;
    const info=products.find(p=>p.card===card)||productInfo(card);
    return scoreProduct(info,nq)<=Math.max(2,Math.floor(nq.length*.55));
  }
  function applyVisibility(){
    const q=(search?.value||'').trim();
    let visible=0;
    cards.forEach(card=>{
      const cats=(card.dataset.categories||'').split(/\s+/);
      const okCat=filter==='all'||cats.includes(filter);
      const okQ=!q||productMatchesQuery(card,q);
      const show=okCat&&okQ;
      card.classList.toggle('hidden',!show);
      if(show) visible++;
    });
    accordions.forEach(cat=>{
      const hasVisible=!!cat.querySelector('.product-card:not(.hidden)');
      cat.style.display=hasVisible?'':'none';
      if(!hasVisible) cat.open=false;
    });
    if(result) result.textContent=visible;
    if(no) no.classList.toggle('visible',visible===0);
    renderSuggestions(q);
    return {q,visible};
  }
  function run(source='init'){
    applyVisibility();
    if(source==='init') closeAll();
    if(source==='filter'){
      const box=document.getElementById('productSuggestions');
      if(box)box.classList.remove('visible');
      if(filter==='all'){closeAll();return;}
      const target=accordions.find(cat=>(cat.dataset.category||'')===filter && cat.style.display!=='none');
      if(target){openOnly(target);target.scrollIntoView({behavior:'smooth',block:'nearest'});} else closeAll();
      return;
    }
    if(source==='search'){
      closeAll();
    }
  }
  search?.addEventListener('input',()=>run('search'));
  search?.addEventListener('focus',()=>renderSuggestions(search.value));
  document.addEventListener('click',e=>{
    const box=document.getElementById('productSuggestions');
    if(box && search && !box.contains(e.target) && !search.contains(e.target)) box.classList.remove('visible');
  });
  search?.addEventListener('keydown',e=>{if(e.key==='Escape'){document.getElementById('productSuggestions')?.classList.remove('visible');}});
  chips.forEach(btn=>btn.addEventListener('click',()=>{
    chips.forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    filter=btn.dataset.cat||'all';
    run('filter');
  }));
  accordions.forEach(acc=>acc.addEventListener('toggle',()=>{
    if(acc.open) accordions.forEach(other=>{if(other!==acc)other.open=false;});
  }));
  run('init');
}
function setDocsValue(docsSelect, requested){
  if(!docsSelect||!requested)return;
  const d=String(requested).toLowerCase();
  const wantsAll=(d.includes('sds')&&d.includes('tds')&&d.includes('coa'))||d.includes('all')||d.includes('mindegyik')||d.includes('alle');
  if(wantsAll){
    const all=[...docsSelect.options].find(o=>/multiple|all|több|mindegyik|mehrere|alle/i.test(o.text));
    if(all){docsSelect.value=all.value||all.text;return;}
  }
  const tokens=d.split(/[\/,+;|]/).map(x=>x.trim()).filter(Boolean);
  for(const token of tokens){
    const opt=[...docsSelect.options].find(o=>o.text.toLowerCase().includes(token)||String(o.value).toLowerCase().includes(token));
    if(opt){docsSelect.value=opt.value||opt.text;return;}
  }
}
function buildPrefillMessage(lang, product, docs){
  const hasDocs=docs&&String(docs).toLowerCase().includes('sds');
  if(lang==='hu') return `Érdeklődés a következő termékkel kapcsolatban: ${product}${hasDocs ? '\nIgényelt dokumentáció: '+docs : ''}`;
  if(lang==='de-at') return `Anfrage zum Produkt: ${product}${hasDocs ? '\nBenötigte Dokumentation: '+docs : ''}`;
  return `Inquiry regarding product: ${product}${hasDocs ? '\nRequested documentation: '+docs : ''}`;
}
function initProductPrefill(){document.querySelectorAll('.product-prefill').forEach(a=>a.addEventListener('click',()=>{const p=a.dataset.product||'';const d=a.dataset.docs||'';setTimeout(()=>{const product=document.getElementById('product');const docs=document.getElementById('docs');const msg=document.getElementById('message');const lang=getLang();if(product&&p)product.value=p;if(docs&&d)setDocsValue(docs,d);if(msg&&!msg.value&&p){msg.value=buildPrefillMessage(lang,p,d);}},60);}));}
function initLanguagePreference(){
  document.querySelectorAll('.lang-switcher a[lang]').forEach(a=>a.addEventListener('click',()=>{try{localStorage.setItem('rmtLangSelected',a.getAttribute('lang')||'en')}catch(_){}}));
  const path=window.location.pathname||'/';
  const isEnglishHome=path==='/'||/\/index\.html$/i.test(path)||/\/en\.html$/i.test(path);
  if(!isEnglishHome)return;
  let selected='';try{selected=localStorage.getItem('rmtLangSelected')||''}catch(_){}
  if(selected)return;
  const langs=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'']).map(v=>String(v).toLowerCase());
  const preferred=langs.find(v=>v.startsWith('hu')||v.startsWith('de'))||'';
  if(!preferred)return;
  const isHu=preferred.startsWith('hu');
  const target=isHu?'/hu.html':'/de-at.html';
  const copy=isHu
    ?{text:'Szeretné magyarul megnyitni az oldalt?',open:'Magyar oldal',stay:'Maradok angolul'}
    :{text:'Möchten Sie die Website auf Deutsch öffnen?',open:'Deutsche Website',stay:'Auf Englisch bleiben'};
  const bar=document.createElement('aside');
  bar.className='language-suggestion';
  bar.setAttribute('role','region');
  bar.setAttribute('aria-label',isHu?'Nyelvi javaslat':'Sprachvorschlag');
  bar.innerHTML=`<p>${copy.text}</p><div><a class="language-suggestion-primary" href="${target}">${copy.open}</a><button type="button">${copy.stay}</button></div>`;
  bar.querySelector('a').addEventListener('click',()=>{try{localStorage.setItem('rmtLangSelected',isHu?'hu':'de-at')}catch(_){}});
  bar.querySelector('button').addEventListener('click',()=>{try{localStorage.setItem('rmtLangSelected','en')}catch(_){}bar.remove();});
  document.body.appendChild(bar);
}

function initForm(){
  const form=document.getElementById('inquiryForm'),status=document.getElementById('formStatus');
  if(!form)return;
  const lang=getLang(),t=FORM_TEXT[lang]||FORM_TEXT.en;
  const endpoint=FORM_ENDPOINT;
  form.action=endpoint;
  form.dataset.endpoint='cloudflare-worker';
  const started=document.getElementById('formStartedAt');
  const aField=document.getElementById('challengeA');
  const bField=document.getElementById('challengeB');
  const answer=document.getElementById('humanAnswer');
  const question=document.getElementById('humanQuestion');
  const turnstileBox=document.getElementById('turnstileContainer');
  const submitButton=form.querySelector('button[type="submit"]');
  let widgetId=null;
  let turnstileReady=false;

  const turnstileText={
    en:'Please complete the Cloudflare security check.',
    hu:'Kérjük, végezze el a Cloudflare biztonsági ellenőrzést.',
    'de-at':'Bitte führen Sie die Cloudflare-Sicherheitsprüfung durch.'
  }[lang]||'Please complete the Cloudflare security check.';

  function show(type,msg){if(!status)return;status.className='form-status '+type;status.textContent=msg;}
  function newMathChallenge(){
    const a=Math.floor(Math.random()*7)+2,b=Math.floor(Math.random()*8)+1;
    if(aField)aField.value=String(a);if(bField)bField.value=String(b);if(answer)answer.value='';
    if(question)question.textContent=`${a} + ${b} =`;if(started)started.value=String(Date.now());
  }
  async function loadScript(src){
    if(document.querySelector(`script[src="${src}"]`))return;
    await new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=src;s.async=true;s.defer=true;s.onload=resolve;s.onerror=reject;document.head.appendChild(s);});
  }
  async function initTurnstile(){
    if(!turnstileBox)return;
    try{
      const response=await fetch(`${endpoint}/config`,{headers:{Accept:'application/json'},cache:'no-store',credentials:'same-origin'});
      const cfg=await response.json().catch(()=>null);
      if(!response.ok||!cfg||cfg.ok!==true||!cfg.siteKey)throw new Error('turnstile_config_unavailable');
      await loadScript('https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit');
      await new Promise((resolve,reject)=>{let tries=0;const wait=()=>{if(window.turnstile)return resolve();if(++tries>100)return reject(new Error('turnstile_load_timeout'));setTimeout(wait,50)};wait()});
      turnstileBox.hidden=false;
      widgetId=window.turnstile.render(turnstileBox,{sitekey:cfg.siteKey,action:cfg.action||'contact_form',theme:'light',size:'flexible',language:lang==='de-at'?'de':lang,'refresh-expired':'auto','refresh-timeout':'auto',callback:()=>{turnstileReady=true;show('','')},'expired-callback':()=>{turnstileReady=false},'error-callback':()=>{turnstileReady=false;show('error',turnstileText)}});
      if(submitButton)submitButton.disabled=false;
    }catch(err){
      console.error('Turnstile initialization failed',err);
      if(submitButton)submitButton.disabled=true;
      show('error',`${t.fail} office@rawmaterialstrade.com`);
    }
  }
  newMathChallenge();
  if(submitButton)submitButton.disabled=true;
  initTurnstile();

  form.addEventListener('submit',async e=>{
    e.preventDefault();
    if(!form.checkValidity()){form.reportValidity();return;}
    const gdpr=document.getElementById('consentGdpr'),disc=document.getElementById('consentDisclaimer');
    if(gdpr&&!gdpr.checked){show('error',t.gdpr);return;}if(disc&&!disc.checked){show('error',t.disc);return;}
    const expected=Number(aField?.value||0)+Number(bField?.value||0);
    if(!answer||Number(answer.value)!==expected){show('error',t.robot);answer?.focus();return;}
    if(Date.now()-Number(started?.value||Date.now())<4000){show('error',t.fast);return;}
    const token=form.querySelector('input[name="cf-turnstile-response"]')?.value||'';
    if(!turnstileReady||!token){show('error',turnstileText);return;}
    show('info',t.sending);if(submitButton)submitButton.disabled=true;
    try{
      const data=new FormData(form);
      data.set('submitted_at',new Date().toISOString());data.set('page_url',window.location.href);data.set('page_title',document.title||'');data.set('language',lang);data.set('form_source','rawmaterialstrade.com');
      const response=await fetch(endpoint,{method:'POST',body:data,headers:{Accept:'application/json'},credentials:'same-origin'});
      const payload=await response.json().catch(()=>null);
      if(!response.ok||!payload||payload.ok!==true)throw new Error(payload?.code||payload?.message||`HTTP ${response.status}`);
      show('success',(payload.confirmationSent===true?form.dataset.successMsg:form.dataset.successBasicMsg)||t.sent);if(window.__rmtAnalyticsConsentGranted&&typeof window.gtag==='function'){window.gtag('event','generate_lead',{form_name:'b2b_inquiry',form_language:lang});}form.reset();newMathChallenge();turnstileReady=false;
      if(window.turnstile&&widgetId!==null)window.turnstile.reset(widgetId);
    }catch(err){
      console.error('RMT form submission failed',err);show('error',`${t.fail} office@rawmaterialstrade.com`);turnstileReady=false;
      if(window.turnstile&&widgetId!==null)window.turnstile.reset(widgetId);
    }finally{if(submitButton)submitButton.disabled=false;}
  });
}

function initQueryPrefill(){
  const params=new URLSearchParams(window.location.search);
  const p=params.get('product')||'';
  const d=params.get('docs')||'';
  if(!p&&!d)return;
  const product=document.getElementById('product');
  const docs=document.getElementById('docs');
  const msg=document.getElementById('message');
  const lang=getLang();
  if(product&&p) product.value=p;
  if(docs&&d) setDocsValue(docs,d);
  if(msg&&p&&!msg.value) msg.value=buildPrefillMessage(lang,p,d);
}


function initCertificateModals(){
  const triggers=[...document.querySelectorAll('[data-cert-src]')];
  if(!triggers.length)return;
  const overlay=document.createElement('div');
  overlay.className='cert-modal';
  overlay.innerHTML='<div class="cert-modal-dialog" role="dialog" aria-modal="true" aria-label="Certificate preview"><div class="cert-modal-header"><div class="cert-modal-title"></div><button type="button" class="cert-modal-close" aria-label="Close">×</button></div><div class="cert-modal-body"></div></div>';
  document.body.appendChild(overlay);
  const titleEl=overlay.querySelector('.cert-modal-title');
  const bodyEl=overlay.querySelector('.cert-modal-body');
  const closeBtn=overlay.querySelector('.cert-modal-close');
  const close=()=>{overlay.classList.remove('open');bodyEl.innerHTML='';};
  const open=(src,title,alt)=>{titleEl.textContent=title||'';bodyEl.innerHTML='';const img=document.createElement('img');img.src=src;img.alt=alt||title||'Certificate';bodyEl.appendChild(img);overlay.classList.add('open');};
  triggers.forEach(btn=>btn.addEventListener('click',e=>{e.preventDefault();open(btn.getAttribute('data-cert-src')||'',btn.getAttribute('data-cert-title')||btn.textContent.trim(),btn.getAttribute('data-cert-alt')||btn.getAttribute('data-cert-title')||'Certificate');}));
  closeBtn.addEventListener('click',close);
  overlay.addEventListener('click',e=>{if(e.target===overlay)close();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&overlay.classList.contains('open'))close();});
}


function initCategoryVisualState(){
  document.querySelectorAll('.category-accordion').forEach(details=>{
    const summary=details.querySelector('.category-summary');
    const sync=()=>summary&&summary.classList.toggle('open',details.open);
    details.addEventListener('toggle',sync);
    sync();
  });
}


function initHeroHoverVideo(){
  const canHover = window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  if(!canHover) return;
  document.querySelectorAll('.hero[data-hero-hover="true"]').forEach(hero=>{
    const video = hero.querySelector('.hero-hover-video');
    if(!video) return;
    let prepared=false;
    const start=()=>{
      if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      hero.classList.add('hero-video-active');
      if(!prepared){ video.load(); prepared=true; }
      const p=video.play();
      if(p && typeof p.catch==='function') p.catch(()=>{});
    };
    const stop=()=>{
      hero.classList.remove('hero-video-active');
      video.pause();
      try{ video.currentTime=0; }catch(e){}
    };
    hero.addEventListener('pointerenter', start, {passive:true});
    hero.addEventListener('pointerleave', stop, {passive:true});
    hero.addEventListener('focusin', start);
    hero.addEventListener('focusout', stop);
  });
}


function initHeroParallax(){
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const desktop = window.matchMedia && window.matchMedia('(min-width: 900px)').matches;
  if(reduce || !desktop) return;
  const heroes=[...document.querySelectorAll('.hero, .product-hero-rich, .product-hero-detail, .ai-profile-hero')]
    .filter(el=>!el.closest('header, footer'));
  if(!heroes.length) return;
  heroes.forEach(el=>el.classList.add('hero-parallax-enabled'));
  let ticking=false;
  const update=()=>{
    const vh=window.innerHeight || document.documentElement.clientHeight || 900;
    heroes.forEach(el=>{
      const r=el.getBoundingClientRect();
      if(r.bottom < -80 || r.top > vh + 80) return;
      const center=r.top + r.height/2;
      const progress=(center - vh/2) / vh;
      const depth=el.classList.contains('has-hover-media') ? 34 : 22;
      const y=Math.max(-42, Math.min(42, progress * -depth));
      el.style.setProperty('--hero-parallax-y', y.toFixed(2)+'px');
    });
    ticking=false;
  };
  const request=()=>{ if(!ticking){ ticking=true; window.requestAnimationFrame(update); } };
  update();
  window.addEventListener('scroll', request, {passive:true});
  window.addEventListener('resize', request, {passive:true});
}

function initSmoothScroll(){document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const id=a.getAttribute('href');if(id&&id.length>1){const el=document.querySelector(id);if(el){e.preventDefault();el.scrollIntoView({behavior:'smooth',block:'start'});}}}));}
document.addEventListener('DOMContentLoaded',()=>{initLanguagePreference();initNav();initCookieBanner();initFAQ();initCatalogue();initProductPrefill();initQueryPrefill();initCertificateModals();initCategoryVisualState();initHeroHoverVideo();initHeroParallax();initForm();initSmoothScroll();});
