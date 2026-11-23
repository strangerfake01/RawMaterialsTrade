#!/usr/bin/env node
"use strict";
/* Deterministic local consent state transitions. No browser, network or user data. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const controller = fs.readFileSync(path.join(__dirname, "..", "assets", "js", "analytics-consent.v20260713.js"), "utf8");

function button() {
  const handlers = {};
  return {
    addEventListener: (name, callback) => { handlers[name] = callback; },
    click: () => {
      assert.equal(typeof handlers.click, "function", "missing consent click handler");
      handlers.click();
    }
  };
}

function load(initialChoice) {
  const storage = new Map();
  if (initialChoice !== null) storage.set("rmt.analytics.consent.v1", initialChoice);
  const consent = button();
  const reject = button();
  const settings = button();
  const visibleClasses = new Set();
  const panel = {
    hidden: true, style: { display: "none" },
    classList: {
      toggle: (name, state) => state ? visibleClasses.add(name) : visibleClasses.delete(name),
      contains: (name) => visibleClasses.has(name)
    }
  };
  const appended = [];
  const cookieMutations = [];
  const on = {};
  const doc = {
    readyState: "loading",
    getElementById: (id) => id === "cookieBanner" ? panel : null,
    querySelectorAll: (selector) => ({
      "[data-analytics-accept]": [consent],
      "[data-analytics-reject]": [reject],
      "[data-cookie-settings]": [settings]
    })[selector] || [],
    addEventListener: (event, callback) => { on[event] = callback; },
    createElement: (tag) => {
      assert.equal(tag, "script", "unexpected DOM injection");
      return { src: "", async: false };
    },
    head: { appendChild: (element) => { appended.push(element.src); } },
    get cookie() { return "_ga=abc123; _ga_TEST=xyz; necessary=ok"; },
    set cookie(value) { cookieMutations.push(value); }
  };
  const storageApi = {
    getItem: (key) => storage.has(key) ? storage.get(key) : null,
    setItem: (key, value) => { storage.set(key, String(value)); }
  };
  const win = {};
  vm.runInNewContext(controller, {
    window: win,
    document: doc,
    localStorage: storageApi,
    location: { origin: "https://www.rawmaterialstrade.com",
      hostname: "www.rawmaterialstrade.com", pathname: "/privacy-en.html" },
    Date
  }, { filename: "analytics-consent.v20260713.js", timeout: 1000 });
  assert.equal(typeof on.DOMContentLoaded, "function", "no DOM readiness listener");
  on.DOMContentLoaded();
  return { consent, reject, settings, panel, appended, cookieMutations, win, storage };
}

const fresh = load(null);
assert.equal(fresh.panel.hidden, false, "no decision must show consent");
assert.equal(fresh.panel.classList.contains("visible"), true, "visible CSS state required");
assert.equal(fresh.win.__rmtAnalyticsConsentGranted, false);
assert.deepEqual(fresh.appended, [], "analytics may not load before opt-in");
fresh.reject.click();
assert.equal(fresh.storage.get("rmt.analytics.consent.v1"), "reject");
assert.equal(fresh.win.__rmtAnalyticsConsentGranted, false);
assert.equal(fresh.panel.hidden, true);
assert.equal(fresh.panel.classList.contains("visible"), false, "reject should remove visible CSS state");
assert.deepEqual(fresh.appended, [], "rejection must not load analytics");
fresh.settings.click();
assert.equal(fresh.panel.hidden, false, "settings must reopen after rejection");
assert.equal(fresh.panel.classList.contains("visible"), true, "reopen should restore CSS visibility");
fresh.consent.click();
assert.equal(fresh.storage.get("rmt.analytics.consent.v1"), "accept");
assert.equal(fresh.win.__rmtAnalyticsConsentGranted, true);
assert.equal(fresh.appended.length, 1, "acceptance should load exactly one analytics script");
assert.match(fresh.appended[0], /^https:\/\/www\.googletagmanager\.com\/gtag\/js\?id=G-/);
fresh.settings.click();
fresh.reject.click();
assert.equal(fresh.win.__rmtAnalyticsConsentGranted, false, "withdrawal must disable tracking");
assert.equal(fresh.storage.get("rmt.analytics.consent.v1"), "reject");
assert.equal(fresh.cookieMutations.some(x => x.startsWith("_ga=")), true, "GA cookies must be invalidated");
assert.equal(fresh.appended.length, 1, "withdrawal must not inject additional analytics scripts");

const priorReject = load("reject");
assert.equal(priorReject.panel.hidden, true);
assert.equal(priorReject.appended.length, 0);
priorReject.settings.click();
assert.equal(priorReject.panel.hidden, false);
const priorAccept = load("accept");
assert.equal(priorAccept.panel.hidden, true);
assert.equal(priorAccept.appended.length, 1);
priorAccept.settings.click();
priorAccept.reject.click();
assert.equal(priorAccept.win.__rmtAnalyticsConsentGranted, false);
console.log("PASS: fresh / reject / reopen / accept / withdraw / stored preferences; no pre-consent GA loading.");
