#!/usr/bin/env node
/**
 * Read-only all-sitemap responsive geometry smoke audit.
 * Serves only public static HTML from localhost. External requests are aborted;
 * no real analytics, CAPTCHA, lead submission or customer records are used.
 * Independent of the source-only sitemap and schema regression tools.
 */
'use strict';
const assert = require('node:assert/strict');
const { readFileSync, mkdirSync } = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const sitemap = readFileSync(path.join(__dirname, '..', 'sitemap.xml'), 'utf8');
const routes = [...sitemap.matchAll(/<loc>(https:\/\/www\.rawmaterialstrade\.com\/[^<]*)<\/loc>/g)]
  .map(match => new URL(match[1]).pathname);
assert.equal(routes.length, 408, 'Unexpected sitemap size: update the audit baseline after verifying new routes');
assert.equal(new Set(routes).size, routes.length, 'Duplicate sitemap route');

const widths = [390, 1440];
const extra = [320, 768, 1024, 1920, 2560];
const priority = new Set([
  '/', '/hu.html', '/de-at.html',
  '/en-catalogue.html', '/hu-termekkatalogus.html', '/de-at-produktkatalog.html',
  '/en-glicerin-99-5-food.html', '/hu-glicerin-99-5-food.html', '/de-at-glicerin-99-5-food.html',
  '/sales-representation-distribution-partner-central-europe.html',
  '/hu-ertekesitesi-kepviselet-disztribucios-partner.html',
  '/de-at-vertriebspartner-distribution-chemierohstoffe.html',
  '/ai-trust-center.html', '/hu-ai-bizalmi-kozpont.html', '/de-at-ai-vertrauenszentrum.html'
]);

async function main() {
  const browser = await chromium.launch({headless: true, args: ['--no-sandbox']});
  const errors = [];
  let checked = 0;
  mkdirSync('layout-screenshots', {recursive: true});
  try {
    for (const width of [...widths, ...extra]) {
      const targets = widths.includes(width) ? routes : routes.filter(r => priority.has(r));
      const context = await browser.newContext({viewport: {width, height: 900}, reducedMotion: 'reduce'});
      const page = await context.newPage();
      page.setDefaultTimeout(10000);
      await page.route('**/*', async route => {
        const url = route.request().url();
        if (url.startsWith('http://127.0.0.1:8765/')) return route.continue();
        return route.abort();
      });
      for (const route of targets) {
        const url = 'http://127.0.0.1:8765' + route;
        try {
          const response = await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 12000});
          if (!response || response.status() !== 200) {
            errors.push([route, width, 'HTTP ' + (response?.status() ?? 'NO_RESPONSE')]);
            continue;
          }
          const result = await page.evaluate(() => ({
            width: window.innerWidth,
            doc: document.documentElement.scrollWidth,
            body: document.body.scrollWidth,
            heading: [...document.querySelectorAll('h1')].filter(e => {
              const box=e.getBoundingClientRect();
              return box.width > 0 && box.height > 0;
            }).length
          }));
          checked++;
          const overflow = Math.max(result.doc, result.body) - result.width;
          if (overflow > 3) {
            errors.push([route, width, 'horizontal overflow ' + overflow + 'px']);
          }
          if (result.heading !== 1) {
            errors.push([route, width, 'visible h1 count ' + result.heading]);
          }
          if (errors.length >= 60) break;
        } catch (err) {
          errors.push([route, width, 'render exception ' + String(err).slice(0,160)]);
          if (errors.length >= 60) break;
        }
      }
      await context.close();
      console.log('VIEWPORT', width, 'checked', checked, 'issues', errors.length);
      if (errors.length >= 60) break;
    }
    console.log('RESULT', JSON.stringify({sitemapRoutes: routes.length, totalRenderedViews: checked,
      errors: errors.slice(0,60)}, null, 2));
    assert.equal(errors.length, 0, 'Responsive/semantic route smoke regression detected');
  } finally {
    await browser.close();
  }
}

main().catch(err => { console.error(err); process.exitCode = 1; });
