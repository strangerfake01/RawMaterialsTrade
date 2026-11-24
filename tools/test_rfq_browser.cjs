#!/usr/bin/env node
/* Isolated public RFQ form regression. All third-party calls are intercepted;
 * no production Worker POST, Cloudflare request, analytics transmission or inbox delivery.
 */
'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const cases = [
 ['index.html','buyer','en'], ['hu.html','buyer','hu'], ['de-at.html','buyer','de-at'],
 ['sales-representation-distribution-partner-central-europe.html','supplier_partnership','en'],
 ['hu-ertekesitesi-kepviselet-disztribucios-partner.html','supplier_partnership','hu'],
 ['de-at-vertriebspartner-distribution-chemierohstoffe.html','supplier_partnership','de-at']
];
const origin='http://127.0.0.1:8765';
const worker='https://muddy-voice-db90.6ymnrwgnv9.workers.dev/api/contact';
const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers':'Accept,Content-Type','Cache-Control':'no-store'};
const turnstileJs = 'window.turnstile={render:function(el,opts){var x=document.createElement("input");'+
  'x.type="hidden";x.name="cf-turnstile-response";x.value="LOCAL-TEST";el.appendChild(x);'+
  'Promise.resolve().then(function(){if(opts.callback)opts.callback();});return 1;},reset:function(){}};';

const manufacturerMessages={
  "sales-representation-distribution-partner-central-europe.html": [
    "Thank you. Your manufacturer enquiry has been sent.",
    "Thank you. Your manufacturer enquiry has been sent. A confirmation email has been sent to the address provided."
  ],
  "hu-ertekesitesi-kepviselet-disztribucios-partner.html": [
    "Köszönjük! Gyártói megkeresését elküldtük.",
    "Köszönjük! Gyártói megkeresését elküldtük. A megadott e-mail-címre automatikus visszaigazolást küldtünk."
  ],
  "de-at-vertriebspartner-distribution-chemierohstoffe.html": [
    "Vielen Dank. Ihre Herstelleranfrage wurde gesendet.",
    "Vielen Dank. Ihre Herstelleranfrage wurde gesendet. Eine automatische Eingangsbestätigung wurde an die angegebene E-Mail-Adresse gesendet."
  ]
};

async function eventCalls(page, names) {
  // An empty gtag.js mock leaves the real local consent queue intact.
  return page.evaluate(eventNames => Array.from(window.dataLayer || [])
    .map(entry => Array.from(entry))
    .filter(entry => entry[0]==='event' && eventNames.includes(entry[1])),names);
}
const leadCalls=page=>eventCalls(page,['generate_lead']);
const funnelCalls=page=>eventCalls(page,['form_start','form_submit_attempt']);

async function one(browser, routeName, expected, language, consent,
                   {confirmationSent=true,query=''}={}) {
  const label=routeName+' / '+consent+' / confirmation '+confirmationSent+(query?' / routed role':'');
  const dimensions={
    form_name:expected==='supplier_partnership'?'manufacturer_partnership':'b2b_inquiry',
    form_language:language,lead_type:expected
  };
  const funnelPayload=Object.assign({page_language:language,page_path:'/'+routeName},dimensions);
  const ctx=await browser.newContext({
    viewport:{width:390,height:900}, reducedMotion:'reduce', serviceWorkers:'block'
  });
  const page=await ctx.newPage();
  const posts=[], unexpectedPosts=[], unexpectedAnalytics=[];
  let tagLoads=0;
  let releaseSuccess;
  const successReleased=new Promise(resolve=>{releaseSuccess=resolve;});
  const accepted=consent!=='reject';
  const consentAfterFocus=consent==='accept-after-focus';
  // Hold the accepted response so the pre-success check observes real pending
  // fetch state, and a consent withdrawal can be exercised before completion.
  if(!accepted)releaseSuccess();

  try {
    await page.route('**/*', async route => {
      const req=route.request(), url=req.url(), method=req.method(), dest=new URL(url);
      if(dest.origin===origin && ['GET','HEAD'].includes(method))return route.continue();
      if(url===worker || url===worker+'/config') {
        if(method==='OPTIONS')return route.fulfill({status:204,headers:cors});
        if(method==='GET' && url===worker+'/config')return route.fulfill({status:200,headers:cors,
          contentType:'application/json',body:JSON.stringify({ok:true,siteKey:'LOCAL-TEST',action:'contact_form'})});
        if(method==='POST' && url===worker) {
          posts.push(req.postData()||'');
          await successReleased;
          return route.fulfill({status:200,headers:cors,contentType:'application/json',
            body:JSON.stringify({ok:true,confirmationSent})});
        }
      }
      if(dest.origin==='https://challenges.cloudflare.com' &&
         dest.pathname==='/turnstile/v0/api.js' && method==='GET') {
        return route.fulfill({status:200,contentType:'application/javascript',body:turnstileJs});
      }
      if(dest.origin==='https://www.googletagmanager.com' &&
         dest.pathname==='/gtag/js' && method==='GET') {
        tagLoads++;
        return route.fulfill({status:200,contentType:'application/javascript',body:''});
      }
      if(/(?:^|\.)(?:googletagmanager\.com|google-analytics\.com|analytics\.google\.com)$/.test(dest.hostname))
        unexpectedAnalytics.push(dest.origin);
      if(method==='POST')unexpectedPosts.push(dest.origin);
      return route.abort();
    });
    const response=await page.goto(origin+'/'+routeName+query+'#contact',
      {waitUntil:'domcontentloaded',timeout:15000});
    assert.equal(response.status(),200,label+': static page missing');

    if(!accepted || consentAfterFocus)await page.locator('[data-analytics-reject]').click();
    if(consentAfterFocus) {
      await page.locator('#name').fill('Browser Test');
      assert.deepEqual(await funnelCalls(page),[],label+': first focus without consent was tracked');
      await page.locator('[data-cookie-settings]').click();
    }
    if(accepted) {
      await Promise.all([page.waitForResponse(res =>
        res.request().method()==='GET' &&
        res.url().startsWith('https://www.googletagmanager.com/gtag/js?'),{timeout:10000}),
        page.locator('[data-analytics-accept]').click()]);
    }
    assert.equal(await page.evaluate(() => window.__rmtAnalyticsConsentGranted),
      accepted,label+': consent state');
    assert.equal(await page.locator('input[name="request_type"]').inputValue(),expected,
      label+': wrong form role');
    await page.waitForFunction(() => {
      const submit=document.querySelector('#inquiryForm button[type="submit"]');
      const token=document.querySelector('#inquiryForm input[name="cf-turnstile-response"]');
      return !!submit && !submit.disabled && !!token?.value;
    },null,{timeout:15000});

    await page.locator('#name').fill('Browser Test');
    await page.locator('#company').fill('Example Test Organization');
    await page.locator('#email').fill('test@example.invalid');
    await page.locator('#country').fill('Test Country');
    if(await page.locator('#product').count())await page.locator('#product').fill('Test product');
    if(await page.locator('#message').count())await page.locator('#message').fill('Internal mocked test: not a real RFQ.');
    await page.locator('#consentGdpr').check();
    await page.locator('#consentDisclaimer').check();
    const answer=await page.evaluate(() => Number(document.querySelector('#challengeA').value)+
                                       Number(document.querySelector('#challengeB').value));
    await page.locator('#humanAnswer').fill(String(answer));
    const submit=page.locator('#inquiryForm button[type="submit"]');
    await page.evaluate(() => document.querySelector('#formStartedAt').value=String(Date.now()));
    await submit.click();
    assert.equal(posts.length,0,label+': early form submission was not blocked');
    assert.deepEqual(await leadCalls(page),[],label+': premature lead before a valid RFQ');

    await page.evaluate(() => document.querySelector('#formStartedAt').value=String(Date.now()-6000));
    await Promise.all([page.waitForRequest(req=>req.method()==='POST' && req.url()===worker,
      {timeout:10000}),submit.click()]);
    if(accepted) {
      assert.equal(await page.locator('#formStatus').evaluate(el=>el.classList.contains('info')),true,
        label+': expected form to await the Worker response');
      assert.deepEqual(await leadCalls(page),[],label+': lead before Worker success');
    }
    if(consent==='withdraw-in-flight') {
      await page.locator('[data-cookie-settings]').click();
      await page.locator('[data-analytics-reject]').click();
      assert.equal(await page.evaluate(() => window.__rmtAnalyticsConsentGranted),false,
        label+': withdrawal was not effective before the response');
    }
    releaseSuccess();
    await page.waitForFunction(() => document.querySelector('#formStatus')?.classList.contains('success'),
      null,{timeout:10000});
    assert.equal(posts.length,1,label+': expected exactly one mocked successful submission');
    assert.ok(posts[0].includes('name="request_type"'),label+': missing role in form data');
    assert.ok(posts[0].includes(expected),label+': wrong submitted role');
    assert.equal(tagLoads,accepted?1:0,label+': unexpected tag loader count');
    if(manufacturerMessages[routeName]) {
      assert.equal(await page.locator('#formStatus').innerText(),
        manufacturerMessages[routeName][confirmationSent?1:0],label+': inaccurate manufacturer success message');
    }
    const expectedFunnel=accepted ? [
      ['event','form_start',funnelPayload],
      ['event','form_submit_attempt',funnelPayload],
      ['event','form_submit_attempt',funnelPayload]
    ] : [];
    assert.deepEqual(await funnelCalls(page),expectedFunnel,label+': wrong start/attempt event role, count or data');
    const expectedLead=accepted&&consent!=='withdraw-in-flight' ?
      [['event','generate_lead',dimensions]] : [];
    // An exact payload comparison rejects all extra form values, not just
    // known personal fields, plus wrong roles/languages and duplicate events.
    assert.deepEqual(await leadCalls(page),expectedLead,label+': wrong lead event count or data');
    assert.deepEqual(unexpectedAnalytics,[],label+': transport attempted beyond mock analytics loader');
    assert.deepEqual(unexpectedPosts,[],label+': unexpected POST');
    console.log('PASS MOCK RFQ',routeName,expected,consent);
  } finally {
    releaseSuccess();
    await ctx.close();
  }
}

(async () => {
  const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  try {
    for(const [page,role,language] of cases) {
      await one(browser,page,role,language,'reject');
      await one(browser,page,role,language,'accept');
    }
    await one(browser,...cases[3],'withdraw-in-flight');
    for(const entry of cases.slice(3))await one(browser,...entry,'accept',{confirmationSent:false});
    await one(browser,'index.html','supplier_partnership','en','accept-after-focus',
      {query:'?type=supplier&product=RMTQA_NO_ANALYTICS_QUERY'});
  } finally {
    await browser.close();
  }
})().catch(e=>{console.error(e);process.exitCode=1;});
