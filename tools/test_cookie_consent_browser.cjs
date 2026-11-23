#!/usr/bin/env node
/* Browser regression of consent before traffic, acceptance and withdrawal.
 * Runs against local static site. All Google Analytics requests are mocked;
 * no data are sent to any real Google property or contact endpoint.
 */
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const { mkdirSync } = require('node:fs');
const path = require('node:path');

async function main() {
  const browser = await chromium.launch({headless: true, args: ['--no-sandbox']});
  const cases = [
    ['privacy-en.html', 'en'],
    ['privacy-hu.html', 'hu'],
    ['privacy-de-at.html', 'de-AT'],
  ];
  mkdirSync('consent-screenshots', {recursive: true});
  try {
    for (const [route, language] of cases) {
      for (const width of [390, 1440]) {
        const context = await browser.newContext({viewport: {width, height: 900}, locale: language});
        const page = await context.newPage();
        let gaRequests = 0;
        page.on('request', req => {
          if (/google(?:tagmanager|-analytics)\.com/.test(req.url())) gaRequests++;
        });
        await page.route('https://www.googletagmanager.com/**', async r =>
          r.fulfill({status: 200, body: '', contentType: 'application/javascript'}));
        await page.route('https://www.google-analytics.com/**', async r =>
          r.fulfill({status: 204, body: ''}));
        const response = await page.goto('http://127.0.0.1:8765/' + route,
                                         {waitUntil: 'domcontentloaded'});
        assert.equal(response.status(), 200, route + ': HTML not served');
        const banner = page.locator('#cookieBanner');
        assert.equal(await banner.isVisible(), true, route + ': initial consent panel not visible');
        await page.waitForTimeout(400);
        const rect = await banner.boundingBox();
        assert.ok(rect && rect.y < 900 && rect.y + rect.height > 0,
                  route + ': consent panel is rendered outside viewport');
        assert.equal(gaRequests, 0, route + ': GA request before opt-in');
        await page.locator('[data-analytics-reject]').click();
        assert.equal(await page.evaluate(() => localStorage.getItem('rmt.analytics.consent.v1')), 'reject');
        assert.equal(await banner.isVisible(), false, route + ': reject did not hide panel');

        await page.locator('[data-cookie-settings]').click();
        assert.equal(await banner.isVisible(), true, route + ': settings cannot reopen consent panel');
        await page.screenshot({path: path.join('consent-screenshots', language + '-' + width + '.png')});
        await page.locator('[data-analytics-accept]').click();
        assert.equal(await page.evaluate(() => localStorage.getItem('rmt.analytics.consent.v1')), 'accept');
        assert.equal(await page.evaluate(() => window.__rmtAnalyticsConsentGranted), true);
        await page.waitForTimeout(150);
        assert.ok(gaRequests > 0, route + ': analytics did not start after explicit consent');

        await page.locator('[data-cookie-settings]').click();
        await page.locator('[data-analytics-reject]').click();
        assert.equal(await page.evaluate(() => localStorage.getItem('rmt.analytics.consent.v1')), 'reject');
        assert.equal(await page.evaluate(() => window.__rmtAnalyticsConsentGranted), false);
        gaRequests = 0;
        await page.reload({waitUntil: 'domcontentloaded'});
        await page.waitForTimeout(150);
        assert.equal(gaRequests, 0, route + ': analytics ran again after withdrawal');
        assert.equal(await banner.isVisible(), false, route + ': stored reject not honored');
        console.log('PASS', route, width, 'opt-in/out and re-open');
        await context.close();
      }
    }
  } finally {
    await browser.close();
  }
}
main().catch(err => {console.error(err); process.exitCode = 1;});
