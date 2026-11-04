/* Sitewide B2B contact launcher — Raw Materials Trade, 2026-11-04 */
(function(){
  'use strict';
  if(!document.querySelector('link[data-rmt-contact-css]')){var css=document.createElement('link');css.rel='stylesheet';css.href='/assets/css/rmt-contact.v20261104.css';css.dataset.rmtContactCss='';document.head.appendChild(css);}
  if(document.querySelector('.rmt-contact')) return;
  var lang=(document.documentElement.lang||'en').toLowerCase();
  var copy=lang.indexOf('hu')===0?{launcher:'Kapcsolat',whatsapp:'WhatsApp',phone:'Hívás',email:'E-mail',close:'Kapcsolat menü bezárása'}:lang.indexOf('de')===0?{launcher:'Kontakt',whatsapp:'WhatsApp',phone:'Anrufen',email:'E-Mail',close:'Kontaktmenü schließen'}:{launcher:'Contact',whatsapp:'WhatsApp',phone:'Call',email:'Email',close:'Close contact menu'};
  var icon='<svg class="rmt-contact__icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.5 4.1 1.6 5.9L.2 24l6.5-1.7a11.8 11.8 0 0 0 5.4 1.3h.1c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.5-8.3Zm-8.4 18.1h-.1a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.9 1 1-3.8-.2-.4a9.8 9.8 0 1 1 8.6 4.8Zm5.4-7.3c-.3-.2-1.8-.9-2.1-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-1.9-.9-3.1-1.6-4.3-3.7-.3-.5.3-.5.9-1.6.1-.2.1-.4 0-.6-.1-.2-.7-1.7-.9-2.3-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.7 0 1.6 1.2 3.1 1.4 3.3.2.2 2.4 3.7 5.8 5.1 2.2.9 2.7.7 3.2.7.5-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.1-.3-.2-.5-.3Z"/></svg>';
  var wrap=document.createElement('div'); wrap.className='rmt-contact'; wrap.setAttribute('data-rmt-contact','');
  wrap.innerHTML='<div class="rmt-contact__menu" hidden>'+ '<a class="rmt-contact__item" href="https://wa.me/36205567917" target="_blank" rel="noopener noreferrer">'+icon+copy.whatsapp+'</a>' + '<a class="rmt-contact__item" href="tel:+36205567917">'+icon+copy.phone+'</a>' + '<a class="rmt-contact__item" href="mailto:nikoletta.kadar@rawmaterialstrade.com">'+icon+copy.email+'</a>' + '<button class="rmt-contact__item" type="button" data-rmt-close aria-label="'+copy.close+'">× '+copy.close+'</button></div>' + '<button class="rmt-contact__launcher" type="button" aria-expanded="false" aria-controls="rmt-contact-menu" aria-label="'+copy.launcher+'">'+icon+'<span>'+copy.launcher+'</span></button>';
  var menu=wrap.querySelector('.rmt-contact__menu'), launcher=wrap.querySelector('.rmt-contact__launcher'); menu.id='rmt-contact-menu';
  document.body.appendChild(wrap);
  function close(){menu.hidden=true;launcher.setAttribute('aria-expanded','false');}
  wrap.querySelector('[data-rmt-close]').addEventListener('click',function(){close();launcher.focus();});
  launcher.addEventListener('click',function(){var open=menu.hidden;menu.hidden=!open;launcher.setAttribute('aria-expanded',String(open));if(open){var first=menu.querySelector('a');if(first) first.focus();}else launcher.focus();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!menu.hidden){close();launcher.focus();}});
  document.addEventListener('click',function(e){if(!wrap.contains(e.target)&&!menu.hidden) close();});
  var footer=document.querySelector('footer');
  if(footer&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(entries){var r=entries[0].intersectionRatio>0;wrap.style.setProperty('--rmt-footer-offset',r?Math.ceil(entries[0].intersectionRect.height)+24+'px':'0px');}, {threshold:[0,.01]});io.observe(footer);}
})();
