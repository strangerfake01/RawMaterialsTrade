/* Raw Materials Trade: consent-first GA4. No analytics network requests before opt-in. */
(function () {
  'use strict';
  var MEASUREMENT_ID = 'G-13022PNK14';
  var STORAGE_KEY = 'rmt.analytics.consent.v1';
  var enabled = false;
  var loaded = false;
  var banner;
  var settingsOpener = null;
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
      // gtag.js uses the registrable parent domain by default, including on www.
      // Restrict extra deletion attempts to the site's known first-party GA domain.
      if (host === 'rawmaterialstrade.com' || host.endsWith('.rawmaterialstrade.com')) {
        domains.push('rawmaterialstrade.com', '.rawmaterialstrade.com');
      }
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
  function showBanner(show, focusChoice) {
    if (banner) {
      banner.hidden = !show;
      banner.classList.toggle('visible', !!show);
      banner.style.display = show ? '' : 'none';
      if (show && focusChoice) {
        var choice = banner.querySelector('[data-analytics-reject]');
        if (choice) choice.focus();
      }
    }
  }
  function applyChoice(choice) {
    saveChoice(choice);
    if (choice === 'accept') enable(); else disable();
    showBanner(false);
    // Restore keyboard focus to the control that opened the preferences.
    if (settingsOpener) { settingsOpener.focus(); settingsOpener = null; }
  }
  // One shared consent control for every tracked entry route, including product pages.
  // The copy below is fixed internal text; no user input or form content is interpolated.
  function consentCopy() {
    var lang = (document.documentElement.lang || 'en').toLowerCase();
    if (lang.indexOf('hu') === 0) return {
      label: 'Süti- és analitikai beállítások',
      message: 'Az oldal működéséhez szükséges helyi tárolást használunk. A Google Analytics csak az Ön engedélye után indul el.',
      privacy: 'Adatvédelmi tájékoztató', privacyHref: '/privacy-hu.html',
      reject: 'Csak szükséges', accept: 'Analitika engedélyezése', settings: 'Süti beállítások'
    };
    if (lang.indexOf('de') === 0) return {
      label: 'Cookie- und Analyse-Einstellungen',
      message: 'Wir verwenden technisch notwendigen lokalen Speicher. Google Analytics startet erst nach Ihrer Zustimmung.',
      privacy: 'Datenschutzerklärung', privacyHref: '/privacy-de-at.html',
      reject: 'Nur erforderlich', accept: 'Analyse zulassen', settings: 'Cookie-Einstellungen'
    };
    return {
      label: 'Cookie and analytics settings',
      message: 'We use essential local storage. Google Analytics starts only after you give consent.',
      privacy: 'Privacy Policy', privacyHref: '/privacy-en.html',
      reject: 'Essential only', accept: 'Allow analytics', settings: 'Cookie settings'
    };
  }
  function ensureConsentControls() {
    var copy = consentCopy();
    var panel = document.getElementById('cookieBanner');
    if (!panel) {
      panel = document.createElement('div');
      panel.id = 'cookieBanner';
      panel.className = 'cookie-banner';
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-label', copy.label);
      panel.innerHTML = '<div class="container"><div class="cookie-inner"><p>' +
        copy.message + ' <a href="' + copy.privacyHref + '">' + copy.privacy + '</a></p>' +
        '<div class="cookie-actions"><button type="button" class="btn-ck btn-ck-no" data-analytics-reject>' +
        copy.reject + '</button><button type="button" class="btn-ck btn-ck-ok" data-analytics-accept>' +
        copy.accept + '</button></div></div></div>';
      document.body.appendChild(panel);
    }
    if (!document.querySelector('[data-cookie-settings]')) {
      var settings = document.createElement('button');
      settings.type = 'button';
      settings.className = 'cookie-settings-toggle';
      settings.setAttribute('data-cookie-settings', '');
      settings.setAttribute('aria-label', copy.settings);
      settings.textContent = copy.settings;
      document.body.appendChild(settings);
    }
    return panel;
  }
  function init() {
    banner = ensureConsentControls();
    document.querySelectorAll('[data-analytics-accept]').forEach(function (b) {
      b.addEventListener('click', function () { applyChoice('accept'); });
    });
    document.querySelectorAll('[data-analytics-reject]').forEach(function (b) {
      b.addEventListener('click', function () { applyChoice('reject'); });
    });
    document.querySelectorAll('[data-cookie-settings]').forEach(function (b) {
      b.addEventListener('click', function () { settingsOpener = b; showBanner(true, true); });
    });
    var existing = readChoice();
    if (existing === 'accept') enable(); else disable();
    showBanner(existing === null);
  }
  window.__rmtAnalyticsConsentGranted = false;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
