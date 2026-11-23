#!/usr/bin/env node
/* Isolated public RFQ form regression. All third-party calls intercepted locally;
 * no production Worker POST, Cloudflare request, analytics or inbox delivery.
 */
'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const cases = [
 ['index.html','buyer'], ['hu.html','buyer'], ['de-at.html','buyer'],
 ['sales-representation-distribution-partner-central-europe.html','supplier_partnership'],
 ['hu-ertekesitesi-kepviselet-disztribucios-partner.html','supplier_partnership'],
 ['de-at-vertriebspartner-distribution-chemierohstoffe.html','supplier_partnership']
];
const origin='http://127.0.0.1:8765';
const worker='https://muddy-voice-db90.6ymnrwgnv9.workers.dev/api/contact';
const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers':'Accept,Content-Type','Cache-Control':'no-store'};
const turnstileJs = 'window.turnstile={render:function(el,opts){var x=document.createElement("input");'+
  'x.type="hidden";x.name="cf-turnstile-response";x.value="LOCAL-TEST";el.appendChild(x);'+
  'Promise.resolve().then(function(){if(opts.callback)opts.callback();});return 1;},reset:function(){}};';

async function one(browser, routeName, expected) {
 const ctx=await browser.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});
 const page=await ctx.newPage();
 let posts=[], ga=0, unexpectedPost=[];
 await page.route('**/*', async route => {
   const req=route.request(), url=req.url();
   if(url.startsWith(origin+'/')) return route.continue();
   if(url.startsWith(worker)) {
     if(req.method()==='OPTIONS')return route.fulfill({status:204,headers:cors});
     if(url.endsWith('/config'))return route.fulfill({status:200,headers:cors,
       contentType:'application/json',body:JSON.stringify({ok:true,siteKey:'LOCAL-TEST',action:'contact_form'})});
     if(req.method()==='POST' && url===worker) {
       posts.push(req.postData()||'');
       return route.fulfill({status:200,headers:cors,contentType:'application/json',
         body:JSON.stringify({ok:true,confirmationSent:true})});
     }
   }
   if(url.startsWith('https://challenges.cloudflare.com/turnstile/'))
     return route.fulfill({status:200,contentType:'application/javascript',body:turnstileJs});
   if(url.includes('googletagmanager.com/')||url.includes('google-analytics.com/')) {
     ga++;return route.fulfill({status:204,body:''});
   }
   if(req.method()==='POST')unexpectedPost.push(url);
   return route.abort();
 });
 try {
   const response=await page.goto(origin+'/'+routeName+'#contact',{waitUntil:'domcontentloaded',timeout:15000});
   assert.equal(response.status(),200,routeName+' static page missing');
   await page.locator('[data-analytics-reject]').click();
   assert.equal(await page.locator('input[name="request_type"]').inputValue(),expected);
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
   await page.evaluate(() => document.querySelector('#formStartedAt').value=String(Date.now()));
   await page.locator('#inquiryForm button[type="submit"]').click();
   assert.equal(posts.length,0,routeName+': early anti-spam gate bypassed');
   await page.evaluate(() => document.querySelector('#formStartedAt').value=String(Date.now()-6000));
   await page.locator('#inquiryForm button[type="submit"]').click();
   await page.waitForFunction(() => document.querySelector('#formStatus')?.classList.contains('success'),null,{timeout:10000});
   assert.equal(posts.length,1,routeName+': expected exactly one mocked successful submission');
   assert.ok(posts[0].includes('name="request_type"'),routeName+': missing role in form data');
   assert.ok(posts[0].includes(expected),routeName+': wrong submitted role');
   assert.equal(ga,0,routeName+': analytics request despite refusal');
   assert.deepEqual(unexpectedPost,[],routeName+': unexpected POST');
   console.log('PASS MOCK RFQ',routeName,expected);
 } finally {await ctx.close();}
}

(async () => {
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try {for(const [p,role] of cases)await one(browser,p,role);}
 finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
