(function () {
  'use strict';

  var MEASUREMENT_ID = 'G-13022PNK14';
  var CONSENT_KEY = 'rmt_consent_v2';
  var SCRIPT_ID = 'rmt-google-analytics';
  var analyticsLoaded = false;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  window.gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });
  window.gtag('set', 'ads_data_redaction', true);
  window.gtag('set', 'url_passthrough', false);

  function safeStorageGet(key) {
    try { return window.localStorage.getItem(key); } catch (error) { return null; }
  }

  function safeStorageSet(key, value) {
    try { window.localStorage.setItem(key, value); } catch (error) { /* Storage may be blocked. */ }
  }

  function readConsent() {
    var raw = safeStorageGet(CONSENT_KEY);
    if (!raw) return null;
    try {
      var parsed = JSON.parse(raw);
      return parsed && (parsed.analytics === 'granted' || parsed.analytics === 'denied') ? parsed.analytics : null;
    } catch (error) {
      return raw === 'granted' || raw === 'denied' ? raw : null;
    }
  }

  function saveConsent(value) {
    safeStorageSet(CONSENT_KEY, JSON.stringify({
      analytics: value,
      updatedAt: new Date().toISOString(),
      version: 2
    }));
  }

  function cleanUrl(value) {
    if (!value) return '';
    try {
      var url = new URL(value, window.location.origin);
      return url.origin + url.pathname;
    } catch (error) {
      return '';
    }
  }

  function getLanguage() {
    var lang = (document.documentElement.getAttribute('lang') || 'en').toLowerCase();
    if (lang.indexOf('hu') === 0) return 'hu';
    if (lang.indexOf('de') === 0) return 'de';
    return 'en';
  }

  function getCopy() {
    var lang = getLanguage();
    if (lang === 'hu') {
      return {
        label: 'Süti- és analitikai beállítások',
        text: 'Az oldal működéséhez szükséges helyi tárolást használunk. Hozzájárulás esetén a Google Analytics segít megérteni az oldalak használatát. Az analitika az engedélyezésig nem indul el.',
        accept: 'Analitika engedélyezése',
        reject: 'Csak szükséges',
        privacy: 'Adatvédelmi tájékoztató',
        settings: 'Süti beállítások'
      };
    }
    if (lang === 'de') {
      return {
        label: 'Cookie- und Analyse-Einstellungen',
        text: 'Wir verwenden technisch notwendigen lokalen Speicher. Mit Ihrer Einwilligung hilft Google Analytics uns, die Nutzung der Seiten zu verstehen. Die Analyse startet erst nach Ihrer Zustimmung.',
        accept: 'Analyse zulassen',
        reject: 'Nur erforderlich',
        privacy: 'Datenschutzerklärung',
        settings: 'Cookie-Einstellungen'
      };
    }
    return {
      label: 'Cookie and analytics settings',
      text: 'We use essential local storage for site functions. With your consent, Google Analytics helps us understand how the pages are used. Analytics does not start until you accept.',
      accept: 'Allow analytics',
      reject: 'Essential only',
      privacy: 'Privacy Policy',
      settings: 'Cookie settings'
    };
  }

  function getPrivacyUrl() {
    var lang = getLanguage();
    if (lang === 'hu') return '/privacy-hu.html';
    if (lang === 'de') return '/privacy-de-at.html';
    return '/privacy-en.html';
  }

  function deleteCookie(name, domain) {
    var domainPart = domain ? '; domain=' + domain : '';
    document.cookie = name + '=; Max-Age=0; path=/' + domainPart + '; SameSite=Lax';
  }

  function clearAnalyticsCookies() {
    var names = document.cookie.split(';').map(function (item) {
      return item.split('=')[0].trim();
    }).filter(function (name) {
      return name === '_ga' || name.indexOf('_ga_') === 0 || name === '_gid' || name === '_gat';
    });
    var host = window.location.hostname;
    var parts = host.split('.');
    var domains = ['', host, '.' + host];
    if (parts.length > 2) domains.push('.' + parts.slice(-2).join('.'));
    names.forEach(function (name) {
      domains.forEach(function (domain) { deleteCookie(name, domain); });
    });
  }

  function initInteractionEvents() {
    if (window.__rmtAnalyticsEventTracking) return;
    window.__rmtAnalyticsEventTracking = true;
    document.addEventListener('click', function (event) {
      if (!analyticsLoaded || readConsent() !== 'granted') return;
      var link = event.target && event.target.closest ? event.target.closest('a[href]') : null;
      if (!link) return;
      var href = link.getAttribute('href') || '';
      if (href.indexOf('mailto:') === 0) {
        window.gtag('event', 'contact_email_click', { contact_method: 'email' });
      } else if (href.indexOf('tel:') === 0) {
        window.gtag('event', 'contact_phone_click', { contact_method: 'phone' });
      } else if (href === '#contact' || href.indexOf('#contact') > -1) {
        window.gtag('event', 'contact_cta_click', { contact_method: 'form' });
      }
    }, true);
  }

  function loadGoogleAnalytics() {
    if (analyticsLoaded || document.getElementById(SCRIPT_ID)) return;
    analyticsLoaded = true;
    window.__rmtAnalyticsConsentGranted = true;

    window.gtag('consent', 'update', {
      analytics_storage: 'granted',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
    window.gtag('js', new Date());
    window.gtag('config', MEASUREMENT_ID, {
      send_page_view: true,
      page_location: cleanUrl(window.location.href),
      page_referrer: cleanUrl(document.referrer),
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_expires: 34128000,
      cookie_update: true,
      transport_type: 'beacon'
    });

    var script = document.createElement('script');
    script.id = SCRIPT_ID;
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(MEASUREMENT_ID);
    document.head.appendChild(script);
    initInteractionEvents();
  }

  function ensureBanner() {
    var copy = getCopy();
    var banner = document.getElementById('cookieBanner');
    if (!banner) {
      banner = document.createElement('div');
      banner.id = 'cookieBanner';
      banner.className = 'cookie-banner';
      banner.setAttribute('role', 'dialog');
      banner.setAttribute('aria-live', 'polite');
      banner.setAttribute('aria-modal', 'false');
      document.body.appendChild(banner);
    }
    banner.setAttribute('aria-label', copy.label);
    banner.innerHTML = '<div class="container"><div class="cookie-inner">' +
      '<p>' + copy.text + ' <a href="' + getPrivacyUrl() + '">' + copy.privacy + '</a></p>' +
      '<div class="cookie-actions">' +
      '<button class="btn-ck btn-ck-no" type="button" data-analytics-reject>' + copy.reject + '</button>' +
      '<button class="btn-ck btn-ck-ok" type="button" data-analytics-accept>' + copy.accept + '</button>' +
      '</div></div></div>';

    var accept = banner.querySelector('[data-analytics-accept]');
    var reject = banner.querySelector('[data-analytics-reject]');
    if (accept) accept.addEventListener('click', function () {
      saveConsent('granted');
      banner.classList.remove('visible');
      loadGoogleAnalytics();
      ensureSettingsButton();
    });
    if (reject) reject.addEventListener('click', function () {
      var wasGranted = readConsent() === 'granted' || analyticsLoaded;
      saveConsent('denied');
      window.__rmtAnalyticsConsentGranted = false;
      window.gtag('consent', 'update', {
        analytics_storage: 'denied',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied'
      });
      clearAnalyticsCookies();
      banner.classList.remove('visible');
      ensureSettingsButton();
      if (wasGranted) window.location.reload();
    });
    return banner;
  }

  function showBanner() {
    var banner = ensureBanner();
    banner.classList.add('visible');
    var firstButton = banner.querySelector('button');
    if (firstButton) window.setTimeout(function () { firstButton.focus(); }, 50);
  }

  function ensureSettingsButton() {
    var choice = readConsent();
    if (!choice) return;
    var copy = getCopy();
    var button = document.getElementById('cookieSettingsToggle');
    if (!button) {
      button = document.createElement('button');
      button.id = 'cookieSettingsToggle';
      button.type = 'button';
      button.className = 'cookie-settings-toggle';
      button.setAttribute('data-cookie-settings', '');
      document.body.appendChild(button);
    }
    button.textContent = copy.settings;
    button.setAttribute('aria-label', copy.settings);
  }

  function initConsentUi() {
    ensureBanner();
    document.addEventListener('click', function (event) {
      var trigger = event.target && event.target.closest ? event.target.closest('[data-cookie-settings]') : null;
      if (!trigger) return;
      event.preventDefault();
      showBanner();
    });

    var choice = readConsent();
    if (choice === 'granted') {
      loadGoogleAnalytics();
      ensureSettingsButton();
    } else if (choice === 'denied') {
      ensureSettingsButton();
    } else {
      window.setTimeout(showBanner, 500);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initConsentUi);
  } else {
    initConsentUi();
  }
})();
