/* Raw Materials Trade: consent-first GA4. No analytics network requests before opt-in. */
(function () {
  'use strict';
  var MEASUREMENT_ID = 'G-13022PNK14';
  var STORAGE_KEY = 'rmt.analytics.consent.v1';
  var enabled = false;
  var loaded = false;
  var banner;
  function readChoice() {
    try { var value = localStorage.getItem(STORAGE_KEY); return value === 'accept' || value === 'reject' ? value : null; }
    catch (_) { return null; }
  }
  function saveChoice(choice) {
    try { localStorage.setItem(STORAGE_KEY, choice); } catch (_) { /* privacy fallback: per-page only */ }
  }
  function wipeCookies() {
    document.cookie.split(';').forEach(function (raw) {
      var name = raw.split('=')[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) return;
      var paths = ['/', location.pathname];
      var host = location.hostname;
      var domains = ['', host, '.' + host];
      domains.forEach(function (domain) { paths.forEach(function (path) {
        document.cookie = name + '=; Max-Age=0; path=' + path + '; SameSite=Lax' + (domain ? '; domain=' + domain : '');
      }); });
    });
  }
  function configureGtag() {
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('consent', 'default', {
      analytics_storage: 'denied', ad_storage: 'denied',
      ad_user_data: 'denied', ad_personalization: 'denied',
      functionality_storage: 'granted', security_storage: 'granted'
    });
  }
  function enable() {
    if (enabled) return;
    enabled = true;
    window.__rmtAnalyticsConsentGranted = true;
    configureGtag();
    window.gtag('consent', 'update', { analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
    window.gtag('config', MEASUREMENT_ID, { anonymize_ip: true, allow_google_signals: false,
      allow_ad_personalization_signals: false, cookie_expires: 60 * 60 * 24 * 395,
      page_location: location.origin + location.pathname });
    if (!loaded) {
      loaded = true;
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
      document.head.appendChild(script);
    }
  }
  function disable() {
    enabled = false;
    window.__rmtAnalyticsConsentGranted = false;
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', { analytics_storage: 'denied', ad_storage: 'denied',
        ad_user_data: 'denied', ad_personalization: 'denied' });
    }
    wipeCookies();
  }
  function showBanner(show) {
    if (banner) { banner.hidden = !show; banner.style.display = show ? '' : 'none'; }
  }
  function applyChoice(choice) {
    saveChoice(choice);
    if (choice === 'accept') enable(); else disable();
    showBanner(false);
  }
  function init() {
    banner = document.getElementById('cookieBanner');
    document.querySelectorAll('[data-analytics-accept]').forEach(function (b) {
      b.addEventListener('click', function () { applyChoice('accept'); });
    });
    document.querySelectorAll('[data-analytics-reject]').forEach(function (b) {
      b.addEventListener('click', function () { applyChoice('reject'); });
    });
    document.querySelectorAll('[data-cookie-settings]').forEach(function (b) {
      b.addEventListener('click', function () { showBanner(true); });
    });
    var existing = readChoice();
    if (existing === 'accept') enable(); else disable();
    showBanner(existing === null);
  }
  window.__rmtAnalyticsConsentGranted = false;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
